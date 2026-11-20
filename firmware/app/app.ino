/* Programa principal do no (ESP32-C6). Compilar com tools/build.sh (monta a pasta plana do sketch).
 *
 *   sensor remoto (N02): mede -> filtra -> decide -> envia o quadro por ESP-NOW ao gateway
 *   gateway (N01):       recebe os quadros por ESP-NOW e os escreve na serial USB (uma linha por quadro);
 *                        se CFG_GATEWAY_TAMBEM_MEDE = 1, tambem mede a sua propria maquina e escreve o quadro N01
 *
 * A logica de decisao (core/) e C puro; este arquivo so liga as pecas. */
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

struct RxItem {
    char   text[32];
    int8_t rssi;
};

static occ_t      g_occ;
static filter_t   g_filt;
static tx_sched_t g_sched;
static bool       g_gateway = false;
static bool       g_mede = true;
static uint8_t    g_node = 0;
static QueueHandle_t g_rxq = nullptr;
static uint32_t   g_ultima_amostra = 0;
static uint32_t   g_ultimo_log = 0;
static int16_t    g_dist = -1;
static int16_t    g_filtrada = -1;

/* Relogio da logica e do roteiro; CFG_TIME_SCALE > 1 acelera para demonstracoes. */
static uint32_t relogio_ms()
{
    return (uint32_t)millis() * (uint32_t)CFG_TIME_SCALE;
}

/* Roda na tarefa do Wi-Fi: so copia para a fila. */
static void on_rx(const uint8_t *mac, const char *payload, int len, int rssi)
{
    (void)mac;
    if (!g_rxq) return;
    RxItem it;
    size_t n = (size_t)len < sizeof(it.text) - 1 ? (size_t)len : sizeof(it.text) - 1;
    memcpy(it.text, payload, n);
    it.text[n] = '\0';
    it.rssi = (int8_t)rssi;
    xQueueSend(g_rxq, &it, 0);
}

static void drenar_rx()
{
    RxItem it;
    while (xQueueReceive(g_rxq, &it, 0) == pdTRUE) {
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

static void enviar(const frame_t &f)
{
    if (g_gateway) {                       /* gateway: o quadro local vai direto para a serial */
        serial_emit_frame(&f);
        return;
    }
    char txt[FRAME_MAX_LEN];
    if (frame_encode(&f, txt, sizeof txt) <= 0) {
        log_line("erro ao codificar quadro");
        return;
    }
    if (!radio_send(txt)) log_line("sem confirmacao do gateway: %s", txt);   /* o proximo sinal de vida repete o estado */
}

void setup()
{
    Serial.begin(115200);
    /* Nunca bloquear se ninguem estiver lendo a USB (no sem computador, ou servidor parado): descarta o
     * log em vez de atrasar o laco. Sem isso o sinal de vida do N02 saiu a cada 18 s em vez de 15 s. */
    Serial.setTxTimeoutMs(0);
    uint32_t t0 = millis();
    while (!Serial && (millis() - t0) < 1500) delay(10);    /* USB nativo: espera o host um instante, sem travar */

    uint8_t mac[6];
    esp_read_mac(mac, ESP_MAC_WIFI_STA);
    if (memcmp(mac, CFG_MAC_GATEWAY, 6) == 0) {
        g_gateway = true;
        g_node = CFG_ID_GATEWAY;
    } else if (memcmp(mac, CFG_MAC_SENSOR, 6) == 0) {
        g_gateway = false;
        g_node = CFG_ID_SENSOR;
    } else {
        for (;;) {
            log_line("MAC desconhecido %02X:%02X:%02X:%02X:%02X:%02X: ajuste CFG_MAC_* em config.h",
                     mac[0], mac[1], mac[2], mac[3], mac[4], mac[5]);
            delay(2000);
        }
    }
    g_mede = g_gateway ? (CFG_GATEWAY_TAMBEM_MEDE != 0) : true;

    occ_cfg_t cfg = OCC_CFG_DEFAULT;
    occ_init(&g_occ, &cfg);
    filter_init(&g_filt);
    sched_init(&g_sched);

    const uint8_t *peer = g_gateway ? CFG_MAC_SENSOR : CFG_MAC_GATEWAY;
    if (g_gateway) {
        g_rxq = xQueueCreate(16, sizeof(RxItem));
        radio_set_rx_cb(on_rx);
    }
    if (!radio_init(CFG_CANAL, peer)) log_line("falha ao iniciar o ESP-NOW");

#if CFG_USAR_SENSOR
    if (g_mede && !hcsr04_init(CFG_PIN_TRIG, CFG_PIN_ECHO)) log_line("falha ao iniciar o HC-SR04");
#endif

    log_line("boot papel=%s no=N%02u mac=%02X:%02X:%02X:%02X:%02X:%02X canal=%d mede=%d fonte=%s escala=%d",
             g_gateway ? "gateway" : "sensor", g_node,
             mac[0], mac[1], mac[2], mac[3], mac[4], mac[5],
             CFG_CANAL, g_mede ? 1 : 0, CFG_USAR_SENSOR ? "hcsr04" : "simulada", CFG_TIME_SCALE);
}

void loop()
{
    uint32_t agora = relogio_ms();
    uint32_t real = millis();

    if (g_gateway) drenar_rx();

    if (g_mede && (real - g_ultima_amostra) >= (uint32_t)CFG_AMOSTRA_MS) {
        g_ultima_amostra = real;
#if CFG_USAR_SENSOR
        g_dist = dist_hcsr04_read(agora);
#else
        g_dist = dist_fake_read(agora);
#endif
        g_filtrada = filter_median3(&g_filt, g_dist);
        bool mudou = occ_update(&g_occ, agora, g_filtrada);
        if (mudou) {
            log_line("estado mudou -> %s (dist=%d cm)", occ_state(&g_occ) == OCC_BUSY ? "OCUPADA" : "LIVRE", g_filtrada);
        }
        if (sched_due(&g_sched, agora, mudou)) {
            frame_t f = { g_node, (uint8_t)occ_state(&g_occ), 0 };
            f.seq = sched_next_seq(&g_sched, agora);
            enviar(f);
        }
    }

    if ((real - g_ultimo_log) >= (uint32_t)CFG_LOG_MS) {
        g_ultimo_log = real;
        log_line("up=%lu dist=%d filt=%d estado=%d", (unsigned long)(real / 1000u), g_dist, g_filtrada, (int)occ_state(&g_occ));
    }
    delay(1);
}
