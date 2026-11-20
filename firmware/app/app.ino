/* Programa principal do nó (ESP32-C6). Compile com tools/build.sh, que monta a
 * pasta plana do sketch.
 *
 *   sensor remoto (N02): mede -> filtra -> decide -> envia o quadro por ESP-NOW
 *                        ao gateway
 *   gateway (N01):       recebe os quadros por ESP-NOW e os escreve na serial
 *                        USB (uma linha por quadro); se CFG_GATEWAY_MEASURES =
 * 1, também mede a sua própria máquina
 *
 * A lógica de decisão (core/) é C puro; este arquivo só liga as peças. */
#include <Arduino.h>
#include <esp_mac.h>
#include <inttypes.h>
#include <string.h>

extern "C"
{
#include "frame.h"
#include "occupancy.h"
#include "scheduler.h"
}
#include "dist_fake.h"
#include "hcsr04.h"
#include "radio.h"
#include "serial_out.h"
#include "config.h"

/* "N99,1,65535" tem 11 caracteres; 32 dá margem e cabe em um item de fila
 * pequeno. */
static const size_t RX_TEXT_LEN = 32;
/* Quadros esperando no gateway: chegam poucos por minuto, então 16 é folga. */
static const int RX_QUEUE_LEN = 16;
/* Quanto esperar o computador abrir a porta serial antes de seguir sem ele. */
static const uint32_t USB_WAIT_MS = 1500;

typedef struct
{
    char text[RX_TEXT_LEN];
    int8_t rssi;
} rx_item_t;

static occ_t s_occ;
static filter_t s_filter;
static tx_sched_t s_sched;
static bool s_is_gateway = false;
static bool s_measures = true; /* este nó mede uma máquina? */
static uint8_t s_node_id = 0;
static QueueHandle_t s_rx_queue = nullptr; /* só existe no gateway */
static uint32_t s_last_sample_ms = 0;
static uint32_t s_last_log_ms = 0;
static int16_t s_dist_cm = -1;
static int16_t s_filtered_cm = -1;

/* Relógio da lógica e do roteiro; CFG_TIME_SCALE > 1 acelera para
 * demonstrações. */
static uint32_t clock_ms()
{
    return millis() * CFG_TIME_SCALE;
}

/* Roda na tarefa do Wi-Fi: só copia o quadro para a fila. A decodificação e a
 * escrita na serial acontecem no laço principal (drain_rx), para a tarefa do
 * Wi-Fi nunca esperar pela USB. */
static void on_rx(const uint8_t *mac, const char *payload, int len, int rssi)
{
    rx_item_t item;
    size_t copy_len;

    (void)mac;
    if (s_rx_queue == nullptr)
    {
        return;
    }
    /* Cast: len é positivo (o rádio só entrega quadros com tamanho > 0). */
    copy_len = ((size_t)len < (sizeof(item.text) - 1))
                   ? (size_t)len
                   : (sizeof(item.text) - 1);
    memcpy(item.text, payload, copy_len);
    item.text[copy_len] = '\0';
    /* Cast: o RSSI do ESP-NOW vai de -128 a 0 dBm, cabe em int8_t. */
    item.rssi = (int8_t)rssi;
    /* Fila cheia: descarta; o sinal de vida repete o estado. */
    xQueueSend(s_rx_queue, &item, 0);
}

/* Gateway: valida cada quadro recebido e o repassa à serial. */
static void drain_rx()
{
    rx_item_t item;
    frame_t frame;
    int result;

    while (xQueueReceive(s_rx_queue, &item, 0) == pdTRUE)
    {
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

/* Entrega um quadro: o gateway escreve na serial; o sensor remoto envia por
 * rádio. */
static void send_frame(const frame_t &frame)
{
    char text[FRAME_MAX_LEN];

    if (s_is_gateway)
    {
        serial_emit_frame(&frame);
        return;
    }
    if (frame_encode(&frame, text, sizeof(text)) <= 0)
    {
        log_line("erro ao codificar quadro");
        return;
    }
    if (!radio_send(text))
    {
        /* O próximo sinal de vida repete o estado. */
        log_line("sem confirmacao do gateway: %s", text);
    }
}

/* Descobre o papel desta placa pelo MAC. Com um MAC que não está em config.h
 * não há o que fazer: avisa na serial e fica parado, em vez de rodar com o
 * papel errado. */
static void detect_role(const uint8_t mac[6])
{
    if (memcmp(mac, CFG_MAC_GATEWAY, 6) == 0)
    {
        s_is_gateway = true;
        s_node_id = CFG_ID_GATEWAY;
    }
    else if (memcmp(mac, CFG_MAC_SENSOR, 6) == 0)
    {
        s_is_gateway = false;
        s_node_id = CFG_ID_SENSOR;
    }
    else
    {
        for (;;)
        {
            log_line("MAC desconhecido %02X:%02X:%02X:%02X:%02X:%02X: ajuste "
                     "CFG_MAC_* em config.h",
                     mac[0], mac[1], mac[2], mac[3], mac[4], mac[5]);
            delay(2000);
        }
    }
    s_measures = s_is_gateway ? (CFG_GATEWAY_MEASURES != 0) : true;
}

static void init_radio()
{
    const uint8_t *peer = s_is_gateway ? CFG_MAC_SENSOR : CFG_MAC_GATEWAY;

    if (s_is_gateway)
    {
        s_rx_queue = xQueueCreate(RX_QUEUE_LEN, sizeof(rx_item_t));
        /* Registra antes de iniciar o rádio, para não perder o 1o quadro. */
        radio_set_rx_cb(on_rx);
    }
    /* TODO: decidir se uma falha aqui deve parar o nó; hoje só avisa e o nó
     * segue sem rádio. */
    if (!radio_init(CFG_CHANNEL, peer))
    {
        log_line("falha ao iniciar o ESP-NOW");
    }
}

static void init_sensor()
{
#if CFG_USE_SENSOR
    if (s_measures && !hcsr04_init(CFG_PIN_TRIG, CFG_PIN_ECHO))
    {
        log_line("falha ao iniciar o HC-SR04");
    }
#endif
}

static void log_boot(const uint8_t mac[6])
{
    log_line(
        "boot papel=%s no=N%02u mac=%02X:%02X:%02X:%02X:%02X:%02X canal=%d "
        "mede=%d fonte=%s escala=%u",
        s_is_gateway ? "gateway" : "sensor", s_node_id, mac[0], mac[1], mac[2],
        mac[3], mac[4], mac[5], CFG_CHANNEL, s_measures ? 1 : 0,
        CFG_USE_SENSOR ? "hcsr04" : "simulada", CFG_TIME_SCALE);
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
    detect_role(mac);

    occ_init(&s_occ, &cfg);
    filter_init(&s_filter);
    sched_init(&s_sched);

    init_radio();
    init_sensor();
    log_boot(mac);
}

void loop()
{
    /* Relógio da lógica (pode estar acelerado) e relógio real, que dita o
     * ritmo de leitura e de log. */
    uint32_t now = clock_ms();
    uint32_t real = millis();
    bool changed;
    frame_t frame;

    if (s_is_gateway)
    {
        drain_rx();
    }

    if (s_measures && ((real - s_last_sample_ms) >= CFG_SAMPLE_MS))
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

    if ((real - s_last_log_ms) >= CFG_LOG_MS)
    {
        s_last_log_ms = real;
        /* Cast: occ_state_t (0 ou 1) para o %d do log. */
        log_line("up=%" PRIu32 " dist=%d filt=%d estado=%d", real / 1000u,
                 s_dist_cm, s_filtered_cm, (int)occ_state(&s_occ));
    }
    delay(1);
}
