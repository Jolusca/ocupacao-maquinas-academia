/* Programa principal do nó (ESP32-C6). Compile com tools/build.sh, que monta a
 * pasta plana do sketch.
 *
 * Todos os nós rodam este mesmo programa e todos medem uma máquina:
 *   mede -> filtra -> decide -> entrega o quadro
 *
 * O que muda é como o quadro é entregue, e isso depende do papel:
 *   coletor (o nó com o notebook na USB): escreve na serial, uma linha por
 *       quadro, os seus e os que recebe por ESP-NOW; avisa por rádio, a cada
 *       5 s, que é o coletor
 *   sensor (os demais): manda o quadro por ESP-NOW ao coletor que anunciou. Se
 *       o coletor some ou outro nó assume, acompanha sozinho.
 *
 * O papel sai da USB (automático) ou de um comando; o número do nó fica na
 * flash. Veja core/link.h e core/command.h. A lógica de decisão (core/) é C
 * puro; este arquivo só liga as peças. */
#include <Arduino.h>
#include <esp_mac.h>
#include <inttypes.h>
#include <string.h>

extern "C"
{
#include "command.h"
#include "frame.h"
#include "link.h"
#include "occupancy.h"
#include "scheduler.h"
}
#include "dist_fake.h"
#include "hcsr04.h"
#include "node_config.h"
#include "radio.h"
#include "serial_out.h"
#include "config.h"

/* "N99,1,65535" tem 11 caracteres; 32 dá margem e cabe em um item de fila
 * pequeno. */
static const size_t RX_TEXT_LEN = 32;
/* Itens esperando na fila de recepção: chegam poucos por minuto, então 16 é
 * folga. */
static const int RX_QUEUE_LEN = 16;
/* Quanto esperar o computador abrir a porta serial antes de seguir sem ele. */
static const uint32_t USB_WAIT_MS = 1500;
/* De quanto em quanto tempo olhar a USB para decidir o papel. */
static const uint32_t ROLE_POLL_MS = 200;
/* Tamanho máximo de uma linha de comando; o que passar disso é descartado. */
static const size_t CMD_LINE_LEN = 48;

typedef struct
{
    char text[RX_TEXT_LEN];
    uint8_t mac[6];
    int8_t rssi;
} rx_item_t;

static occ_t s_occ;
static filter_t s_filter;
static tx_sched_t s_sched;
static role_state_t s_role;
static sink_link_t s_link;
static bool s_peer_set = false; /* o rádio está mandando ao coletor? */
static bool s_beacon_sent = false;
static uint32_t s_last_beacon_ms = 0;
static uint32_t s_last_role_ms = 0;
static uint32_t s_last_warn_ms = 0;
static uint8_t s_node_id = 0; /* 0 = ainda sem número */
static QueueHandle_t s_rx_queue = nullptr;
static uint32_t s_last_sample_ms = 0;
static uint32_t s_last_log_ms = 0;
static int16_t s_dist_cm = -1;
static int16_t s_filtered_cm = -1;
static char s_cmd_line[CMD_LINE_LEN];
static size_t s_cmd_len = 0;

/* Relógio da lógica e do roteiro; CFG_TIME_SCALE > 1 acelera para
 * demonstrações. */
static uint32_t clock_ms()
{
    return millis() * CFG_TIME_SCALE;
}

static bool is_sink()
{
    return s_role.role == ROLE_SINK;
}

/* Há um computador do outro lado da USB? Um carregador não conta. */
static bool usb_host_present()
{
    return HWCDC::isPlugged();
}

static const char *role_name(role_t role)
{
    return (role == ROLE_SINK) ? "coletor" : "sensor";
}

static const char *mode_name(role_mode_t mode)
{
    if (mode == ROLE_MODE_SINK)
    {
        return "coletor";
    }
    if (mode == ROLE_MODE_SENSOR)
    {
        return "sensor";
    }
    return "auto";
}

/* Roda na tarefa do Wi-Fi: só copia o que chegou para a fila. A decodificação e
 * a escrita na serial acontecem no laço principal (drain_rx), para a tarefa do
 * Wi-Fi nunca esperar pela USB. */
static void on_rx(const uint8_t *mac, const char *payload, int len, int rssi)
{
    rx_item_t item;
    size_t copy_len;

    if (s_rx_queue == nullptr)
    {
        return;
    }
    /* Cast: len é positivo (o rádio só entrega itens com tamanho > 0). */
    copy_len = ((size_t)len < (sizeof(item.text) - 1))
                   ? (size_t)len
                   : (sizeof(item.text) - 1);
    memcpy(item.text, payload, copy_len);
    item.text[copy_len] = '\0';
    memcpy(item.mac, mac, 6);
    /* Cast: o RSSI do ESP-NOW vai de -128 a 0 dBm, cabe em int8_t. */
    item.rssi = (int8_t)rssi;
    /* Fila cheia: descarta; o sinal de vida repete o estado. */
    xQueueSend(s_rx_queue, &item, 0);
}

/* Aviso de coletor recebido por um sensor: aprende (ou troca) o coletor. */
static void on_beacon(const uint8_t mac[6])
{
    if (sink_on_beacon(&s_link, mac, millis()))
    {
        if (radio_set_peer(mac))
        {
            s_peer_set = true;
        }
        log_line("coletor %02X:%02X:%02X:%02X:%02X:%02X", mac[0], mac[1],
                 mac[2], mac[3], mac[4], mac[5]);
    }
}

/* Trata o que chegou por rádio. Coletor: valida cada quadro e o repassa à
 * serial. Sensor: só os avisos do coletor interessam. */
static void drain_rx()
{
    rx_item_t item;
    frame_t frame;
    int result;

    while (xQueueReceive(s_rx_queue, &item, 0) == pdTRUE)
    {
        if (strcmp(item.text, LINK_BEACON_TEXT) == 0)
        {
            if (!is_sink())
            {
                on_beacon(item.mac);
            }
            continue;
        }
        if (!is_sink())
        {
            continue; /* quadro de outro sensor (broadcast): não é comigo */
        }
        result = frame_decode(item.text, &frame);
        if (result == FRAME_OK)
        {
            serial_emit_frame(&frame);
            log_line("rx N%02u rssi=%d", frame.node, item.rssi);
        }
        else
        {
            log_line("quadro invalido (%d): %s", result, item.text);
        }
    }
}

/* Entrega um quadro: o coletor escreve na serial; o sensor envia por rádio. */
static void send_frame(const frame_t &frame)
{
    char text[FRAME_MAX_LEN];
    bool known;
    bool ok;

    if (is_sink())
    {
        serial_emit_frame(&frame);
        return;
    }
    if (frame_encode(&frame, text, sizeof(text)) <= 0)
    {
        log_line("erro ao codificar quadro");
        return;
    }

    known = sink_known(&s_link, millis());
    if (!known && s_peer_set)
    {
        /* O coletor sumiu: volta ao broadcast até ouvir um aviso. */
        radio_clear_peer();
        s_peer_set = false;
        log_line("coletor perdido: quadros por broadcast");
    }
    ok = radio_send(text);
    if (known)
    {
        sink_on_delivery(&s_link, ok);
        if (!ok)
        {
            /* Sem confirmação: reenvia por broadcast, para o quadro chegar
             * mesmo que o coletor tenha mudado e ainda não tenha se anunciado.
             * Se o envio direto tinha chegado e só o ACK se perdeu, o
             * servidor descarta o repetido pelo seq. */
            radio_broadcast(text);
            log_line("sem confirmacao do coletor (reenviado por broadcast): "
                     "%s",
                     text);
        }
    }
}

/* Passa a ser coletor ou deixa de ser: arruma o que depende do papel. */
static void on_role_changed()
{
    log_line("papel: %s", role_name(s_role.role));
    sink_init(&s_link);
    radio_clear_peer();
    s_peer_set = false;
    s_beacon_sent = false;
}

static void poll_role()
{
    role_t before = s_role.role;

    role_update(&s_role, millis(), usb_host_present());
    if (s_role.role != before)
    {
        on_role_changed();
    }
}

/* Coletor: avisa por rádio, a cada 5 s, que é o coletor. */
static void send_beacon()
{
    uint32_t real = millis();

    if (!is_sink() ||
        !link_beacon_due(s_beacon_sent, s_last_beacon_ms, real))
    {
        return;
    }
    radio_broadcast(LINK_BEACON_TEXT);
    s_beacon_sent = true;
    s_last_beacon_ms = real;
}

/* Número do nó: o gravado na flash; senão o da tabela pelo MAC; senão 0. */
static uint8_t default_id(const uint8_t mac[6])
{
    size_t i;

    for (i = 0; i < (sizeof(CFG_IDS_PADRAO) / sizeof(CFG_IDS_PADRAO[0])); i++)
    {
        if (memcmp(mac, CFG_IDS_PADRAO[i].mac, 6) == 0)
        {
            return CFG_IDS_PADRAO[i].id;
        }
    }
    return 0;
}

static uint8_t load_id(const uint8_t mac[6])
{
    uint8_t id = node_cfg_id();

    return (id != 0) ? id : default_id(mac);
}

static void print_info()
{
    uint8_t mac[6];
    char sink_text[20];
    const uint8_t *sink;

    esp_read_mac(mac, ESP_MAC_WIFI_STA);
    /* Qual coletor este nó usa: ele mesmo, o que aprendeu pelos avisos, ou
     * nenhum (os quadros vão por broadcast). */
    if (is_sink())
    {
        snprintf(sink_text, sizeof(sink_text), "eu");
    }
    else if (sink_known(&s_link, millis()))
    {
        sink = sink_mac(&s_link);
        snprintf(sink_text, sizeof(sink_text), "%02X:%02X:%02X:%02X:%02X:%02X",
                 sink[0], sink[1], sink[2], sink[3], sink[4], sink[5]);
    }
    else
    {
        snprintf(sink_text, sizeof(sink_text), "nenhum");
    }
    log_line("config id=%u gravado=%u modo=%s papel=%s usb=%d coletor=%s "
             "mac=%02X:%02X:%02X:%02X:%02X:%02X",
             s_node_id, node_cfg_id(), mode_name(s_role.mode),
             role_name(s_role.role), usb_host_present() ? 1 : 0, sink_text,
             mac[0], mac[1], mac[2], mac[3], mac[4], mac[5]);
}

static void run_command(const cmd_t &cmd)
{
    uint8_t mac[6];
    role_t before = s_role.role;

    switch (cmd.kind)
    {
    case CMD_ID:
        node_cfg_save_id(cmd.id);
        s_node_id = cmd.id;
        log_line("ok id=%u gravado", s_node_id);
        break;
    case CMD_ROLE:
        node_cfg_save_mode(cmd.mode);
        role_set_mode(&s_role, cmd.mode, usb_host_present());
        log_line("ok modo=%s gravado", mode_name(cmd.mode));
        if (s_role.role != before)
        {
            on_role_changed();
        }
        break;
    case CMD_CLEAR:
        node_cfg_clear();
        esp_read_mac(mac, ESP_MAC_WIFI_STA);
        s_node_id = default_id(mac);
        role_set_mode(&s_role, ROLE_MODE_AUTO, usb_host_present());
        log_line("ok flash limpa; id=%u modo=auto", s_node_id);
        break;
    case CMD_INFO:
        print_info();
        break;
    default:
        break;
    }
}

/* Lê a serial e executa um comando por linha. Linhas que não são comando
 * (ou ruído) só geram um aviso. */
static void poll_commands()
{
    cmd_t cmd;
    int result;
    int c;

    while (Serial.available() > 0)
    {
        c = Serial.read();
        if (c < 0)
        {
            return;
        }
        if (c != '\n')
        {
            if (s_cmd_len < (CMD_LINE_LEN - 1))
            {
                s_cmd_line[s_cmd_len++] = (char)c; /* cast: c é 0..255 */
            }
            continue;
        }
        s_cmd_line[s_cmd_len] = '\0';
        s_cmd_len = 0;
        result = cmd_parse(s_cmd_line, &cmd);
        if (result == CMD_OK)
        {
            run_command(cmd);
        }
        else if (result == CMD_ERR_ARG)
        {
            log_line("comando com argumento invalido; use: id N | papel "
                     "auto|coletor|sensor | info | limpar");
        }
        else if (result == CMD_ERR_UNKNOWN)
        {
            log_line("comando desconhecido; use: id N | papel "
                     "auto|coletor|sensor | info | limpar");
        }
    }
}

static void init_radio()
{
    s_rx_queue = xQueueCreate(RX_QUEUE_LEN, sizeof(rx_item_t));
    /* Registra antes de iniciar o rádio, para não perder o 1o item. */
    radio_set_rx_cb(on_rx);
    /* TODO: decidir se uma falha aqui deve parar o nó; hoje só avisa e o nó
     * segue sem rádio. */
    if (!radio_init(CFG_CHANNEL))
    {
        log_line("falha ao iniciar o ESP-NOW");
    }
}

static void init_sensor()
{
#if CFG_USE_SENSOR
    if (!hcsr04_init(CFG_PIN_TRIG, CFG_PIN_ECHO))
    {
        log_line("falha ao iniciar o HC-SR04");
    }
#endif
}

static void log_boot(const uint8_t mac[6])
{
    log_line("boot papel=%s modo=%s no=N%02u mac=%02X:%02X:%02X:%02X:%02X:%02X "
             "canal=%d fonte=%s escala=%u",
             role_name(s_role.role), mode_name(s_role.mode), s_node_id, mac[0],
             mac[1], mac[2], mac[3], mac[4], mac[5], CFG_CHANNEL,
             CFG_USE_SENSOR ? "hcsr04" : "simulada", CFG_TIME_SCALE);
}

/* Este nó mede uma máquina agora? Precisa de número; o coletor só mede se
 * CFG_SINK_MEASURES. */
static bool measures()
{
    if (s_node_id == 0)
    {
        return false;
    }
    return is_sink() ? (CFG_SINK_MEASURES != 0) : true;
}

void setup()
{
    uint8_t mac[6];
    uint32_t start_ms;
    occ_cfg_t cfg = OCC_CFG_DEFAULT;

    Serial.begin(115200);
    /* Nunca bloquear se ninguém estiver lendo a USB (nó sem computador, ou
     * servidor parado): descarta o log em vez de atrasar o laço. Sem isso o
     * sinal de vida do N02 saiu a cada 18 s em vez de 15 s. */
    Serial.setTxTimeoutMs(0);
    start_ms = millis();
    /* USB nativa: espera o computador um instante, sem travar. */
    while ((!Serial) && ((millis() - start_ms) < USB_WAIT_MS))
    {
        delay(10);
    }

    esp_read_mac(mac, ESP_MAC_WIFI_STA);
    s_node_id = load_id(mac);
    role_init(&s_role, node_cfg_mode(), usb_host_present());
    sink_init(&s_link);

    occ_init(&s_occ, &cfg);
    filter_init(&s_filter);
    sched_init(&s_sched);

    init_radio();
    init_sensor();
    log_boot(mac);
    if (s_node_id == 0)
    {
        log_line("sem numero de no: envie o comando 'id N'");
    }
}

void loop()
{
    /* Relógio da lógica (pode estar acelerado) e relógio real, que dita o
     * ritmo de leitura e de log. */
    uint32_t now = clock_ms();
    uint32_t real = millis();
    bool changed;
    frame_t frame;

    poll_commands();
    if ((real - s_last_role_ms) >= ROLE_POLL_MS)
    {
        s_last_role_ms = real;
        poll_role();
    }
    drain_rx();
    send_beacon();

    if (measures() && ((real - s_last_sample_ms) >= CFG_SAMPLE_MS))
    {
        s_last_sample_ms = real;
#if CFG_USE_SENSOR
        s_dist_cm = dist_hcsr04_read(now);
#else
        s_dist_cm = dist_fake_read(now);
#endif
        s_filtered_cm = filter_median3(&s_filter, s_dist_cm);
        changed = occ_update(&s_occ, now, s_filtered_cm);
        if (changed)
        {
            log_line("estado mudou -> %s (dist=%d cm)",
                     (occ_state(&s_occ) == OCC_BUSY) ? "OCUPADA" : "LIVRE",
                     s_filtered_cm);
        }
        /* Envia quando o estado muda e a cada 15 s (sinal de vida). */
        if (sched_due(&s_sched, now, changed))
        {
            frame.node = s_node_id;
            /* Cast: occ_state_t só vale 0 ou 1, cabe em uint8_t. */
            frame.state = (uint8_t)occ_state(&s_occ);
            frame.seq = sched_next_seq(&s_sched, now);
            send_frame(frame);
        }
    }
    else if ((s_node_id == 0) && ((real - s_last_warn_ms) >= 2000u))
    {
        s_last_warn_ms = real;
        log_line("sem numero de no: envie o comando 'id N'");
    }

    if ((real - s_last_log_ms) >= CFG_LOG_MS)
    {
        s_last_log_ms = real;
        /* Cast: occ_state_t (0 ou 1) para o %d do log. */
        log_line("up=%" PRIu32 " dist=%d filt=%d estado=%d", real / 1000u,
                 s_dist_cm, s_filtered_cm, (int)occ_state(&s_occ));
    }
    delay(1);
}
