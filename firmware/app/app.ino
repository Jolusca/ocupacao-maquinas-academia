/* Programa principal do nó (ESP32-C6). Compile com tools/build.sh, que monta a pasta plana do sketch.
 *
 *   sensor remoto (N02): mede -> filtra -> decide -> envia o quadro por ESP-NOW ao gateway
 *   gateway (N01):       recebe os quadros por ESP-NOW e os escreve na serial USB (uma linha por
 *                        quadro); se CFG_GATEWAY_MEASURES = 1, também mede a sua própria máquina
 *
 * A lógica de decisão (core/) é C puro; este arquivo só liga as peças. */
#include <Arduino.h>
#include <esp_mac.h>
#include <string.h>

extern "C" {
#include "frame.h"
#include "occupancy.h"
#include "scheduler.h"
}
#include "dist_source.h"
#include "hcsr04.h"
#include "radio.h"
#include "serial_out.h"
#include "config.h"

/* "N99,1,65535" tem 11 caracteres; 32 dá margem e cabe em um item de fila pequeno. */
static const size_t RX_TEXT_LEN = 32;
/* Quadros esperando no gateway: chegam poucos por minuto, então 16 é folga de sobra. */
static const int RX_QUEUE_LEN = 16;
/* Quanto esperar o computador abrir a porta serial antes de seguir sem ele. */
static const uint32_t USB_WAIT_MS = 1500;

struct RxItem {
    char   text[RX_TEXT_LEN];
    int8_t rssi;
};

static occ_t         g_occ;
static filter_t      g_filter;
static tx_sched_t    g_sched;
static bool          g_is_gateway = false;
static bool          g_measures = true;      /* este nó mede uma máquina? */
static uint8_t       g_node_id = 0;
static QueueHandle_t g_rx_queue = nullptr;   /* só existe no gateway */
static uint32_t      g_last_sample_ms = 0;
static uint32_t      g_last_log_ms = 0;
static int16_t       g_dist_cm = -1;
static int16_t       g_filtered_cm = -1;

/* Relógio da lógica e do roteiro; CFG_TIME_SCALE > 1 acelera para demonstrações. */
static uint32_t clock_ms()
{
    return (uint32_t)millis() * (uint32_t)CFG_TIME_SCALE;
}

/* Roda na tarefa do Wi-Fi: só copia o quadro para a fila. A decodificação e a escrita na serial
 * acontecem no laço principal (drain_rx), para a tarefa do Wi-Fi nunca esperar pela USB. */
static void on_rx(const uint8_t *mac, const char *payload, int len, int rssi)
{
    (void)mac;
    if (!g_rx_queue) return;
    RxItem it;
    size_t n = (size_t)len < sizeof(it.text) - 1 ? (size_t)len : sizeof(it.text) - 1;
    memcpy(it.text, payload, n);
    it.text[n] = '\0';
    it.rssi = (int8_t)rssi;
    xQueueSend(g_rx_queue, &it, 0);   /* fila cheia: descarta; o sinal de vida repete o estado */
}

/* Gateway: valida cada quadro recebido e o repassa à serial. */
static void drain_rx()
{
    RxItem it;
    while (xQueueReceive(g_rx_queue, &it, 0) == pdTRUE) {
        frame_t f;
        int r = frame_decode(it.text, &f);
        if (r == FRAME_OK) {
            serial_emit_frame(&f);
            log_line("rx N%02u rssi=%d", f.node, it.rssi);
        } else {
            log_line("quadro invalido (%d): %s", r, it.text);
        }
    }
}

/* Entrega um quadro: o gateway escreve na serial; o sensor remoto envia por rádio. */
static void send_frame(const frame_t &f)
{
    if (g_is_gateway) {
        serial_emit_frame(&f);
        return;
    }
    char txt[FRAME_MAX_LEN];
    if (frame_encode(&f, txt, sizeof txt) <= 0) {
        log_line("erro ao codificar quadro");
        return;
    }
    if (!radio_send(txt)) log_line("sem confirmacao do gateway: %s", txt);   /* o próximo sinal de vida repete o estado */
}

/* Descobre o papel desta placa pelo MAC. Com um MAC que não está em config.h não há o que fazer:
 * avisa na serial e fica parado, em vez de rodar com o papel errado. */
static void detect_role(const uint8_t mac[6])
{
    if (memcmp(mac, CFG_MAC_GATEWAY, 6) == 0) {
        g_is_gateway = true;
        g_node_id = CFG_ID_GATEWAY;
    } else if (memcmp(mac, CFG_MAC_SENSOR, 6) == 0) {
        g_is_gateway = false;
        g_node_id = CFG_ID_SENSOR;
    } else {
        for (;;) {
            log_line("MAC desconhecido %02X:%02X:%02X:%02X:%02X:%02X: ajuste CFG_MAC_* em config.h",
                     mac[0], mac[1], mac[2], mac[3], mac[4], mac[5]);
            delay(2000);
        }
    }
    g_measures = g_is_gateway ? (CFG_GATEWAY_MEASURES != 0) : true;
}

static void init_radio()
{
    const uint8_t *peer = g_is_gateway ? CFG_MAC_SENSOR : CFG_MAC_GATEWAY;
    if (g_is_gateway) {
        g_rx_queue = xQueueCreate(RX_QUEUE_LEN, sizeof(RxItem));
        radio_set_rx_cb(on_rx);   /* registra antes de iniciar o rádio, para não perder o primeiro quadro */
    }
    /* TODO: decidir se uma falha aqui deve parar o nó; hoje só avisa e o nó segue sem rádio. */
    if (!radio_init(CFG_CHANNEL, peer)) log_line("falha ao iniciar o ESP-NOW");
}

static void init_sensor()
{
#if CFG_USE_SENSOR
    if (g_measures && !hcsr04_init(CFG_PIN_TRIG, CFG_PIN_ECHO)) log_line("falha ao iniciar o HC-SR04");
#endif
}

static void log_boot(const uint8_t mac[6])
{
    log_line("boot papel=%s no=N%02u mac=%02X:%02X:%02X:%02X:%02X:%02X canal=%d mede=%d fonte=%s escala=%d",
             g_is_gateway ? "gateway" : "sensor", g_node_id,
             mac[0], mac[1], mac[2], mac[3], mac[4], mac[5],
             CFG_CHANNEL, g_measures ? 1 : 0, CFG_USE_SENSOR ? "hcsr04" : "simulada", CFG_TIME_SCALE);
}

void setup()
{
    Serial.begin(115200);
    /* Nunca bloquear se ninguém estiver lendo a USB (nó sem computador, ou servidor parado): descarta o
     * log em vez de atrasar o laço. Sem isso o sinal de vida do N02 saiu a cada 18 s em vez de 15 s. */
    Serial.setTxTimeoutMs(0);
    uint32_t t0 = millis();
    while (!Serial && (millis() - t0) < USB_WAIT_MS) delay(10);   /* USB nativa: espera o computador um instante, sem travar */

    uint8_t mac[6];
    esp_read_mac(mac, ESP_MAC_WIFI_STA);
    detect_role(mac);

    occ_cfg_t cfg = OCC_CFG_DEFAULT;
    occ_init(&g_occ, &cfg);
    filter_init(&g_filter);
    sched_init(&g_sched);

    init_radio();
    init_sensor();
    log_boot(mac);
}

void loop()
{
    uint32_t now = clock_ms();    /* relógio da lógica (pode estar acelerado) */
    uint32_t real = millis();     /* relógio real, para o ritmo de leitura e de log */

    if (g_is_gateway) drain_rx();

    if (g_measures && (real - g_last_sample_ms) >= (uint32_t)CFG_SAMPLE_MS) {
        g_last_sample_ms = real;
#if CFG_USE_SENSOR
        g_dist_cm = dist_hcsr04_read(now);
#else
        g_dist_cm = dist_fake_read(now);
#endif
        g_filtered_cm = filter_median3(&g_filter, g_dist_cm);
        bool changed = occ_update(&g_occ, now, g_filtered_cm);
        if (changed) {
            log_line("estado mudou -> %s (dist=%d cm)", occ_state(&g_occ) == OCC_BUSY ? "OCUPADA" : "LIVRE", g_filtered_cm);
        }
        /* Envia quando o estado muda e a cada 15 s (sinal de vida), conforme o agendador. */
        if (sched_due(&g_sched, now, changed)) {
            frame_t f = { g_node_id, (uint8_t)occ_state(&g_occ), 0 };
            f.seq = sched_next_seq(&g_sched, now);
            send_frame(f);
        }
    }

    if ((real - g_last_log_ms) >= (uint32_t)CFG_LOG_MS) {
        g_last_log_ms = real;
        log_line("up=%lu dist=%d filt=%d estado=%d", (unsigned long)(real / 1000u), g_dist_cm, g_filtered_cm, (int)occ_state(&g_occ));
    }
    delay(1);
}
