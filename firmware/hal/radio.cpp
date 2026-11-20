#include <Arduino.h>
#include <WiFi.h>
#include <esp_now.h>
#include <esp_wifi.h>
#include <string.h>
#include "radio.h"

/* Tamanho máximo de um quadro ESP-NOW (versão 1 do protocolo). */
static const size_t ESPNOW_MAX_PAYLOAD = 250;

/* O MAC já reenvia o quadro sozinho, mas a confirmação pode se perder; por isso
 * o envio é repetido até SEND_ATTEMPTS vezes. Mesmo assim um quadro pode se
 * perder, e tudo bem: o sinal de vida repete o estado de 15 em 15 s, então o
 * servidor não fica com informação errada por muito tempo. */
static const int SEND_ATTEMPTS = 3;

/* O callback de envio costuma chegar em poucos ms; passado este tempo, a
 * tentativa conta como perdida. */
static const uint32_t ACK_TIMEOUT_MS = 50;

/* Pausa entre tentativas, para o rádio esvaziar a fila de transmissão. */
static const uint32_t RETRY_GAP_MS = 10;

static uint8_t s_peer[6];

/* Resultado da última tentativa: -1 esperando, 0 falhou, 1 confirmado pelo MAC
 * do outro lado. É escrito pelo callback (tarefa do Wi-Fi) e lido por
 * radio_send (laço principal), daí o volatile.
 * Limitação conhecida: o callback não diz a que tentativa se refere. Um
 * callback muito atrasado da tentativa N poderia ser lido como resposta da N+1;
 * é raro com ACK_TIMEOUT_MS de 50 ms. */
static volatile int s_send_status = -1;

static void (*s_rx_cb)(const uint8_t *, const char *, int, int) = nullptr;

/* Callback de envio: só registra o resultado. */
static void on_sent(const wifi_tx_info_t *, esp_now_send_status_t status)
{
    s_send_status = (status == ESP_NOW_SEND_SUCCESS) ? 1 : 0;
}

/* Callback de recepção, na tarefa do Wi-Fi. Copia o payload para um buffer
 * próprio (o original deixa de valer quando a função retorna) e o termina com
 * '\0', para o texto poder ser tratado como string. */
static void on_recv(const esp_now_recv_info_t *info, const uint8_t *data,
                    int len)
{
    char text[ESPNOW_MAX_PAYLOAD + 1];

    /* Cast: len é positivo (checado antes), então cabe em size_t. */
    if ((s_rx_cb == nullptr) || (len <= 0) ||
        ((size_t)len > ESPNOW_MAX_PAYLOAD))
    {
        return;
    }
    memcpy(text, data, (size_t)len); /* cast: len > 0 */
    text[len] = '\0';
    s_rx_cb(info->src_addr, text, len, info->rx_ctrl->rssi);
}

bool radio_init(uint8_t channel, const uint8_t peer_mac[6])
{
    esp_now_peer_info_t peer_info = {};

    memcpy(s_peer, peer_mac, 6);

    /* O ESP-NOW usa a interface Wi-Fi, mas não precisa estar conectado a
     * roteador nenhum. */
    WiFi.mode(WIFI_STA);
    WiFi.disconnect();
    /* Sem economia de energia: o rádio fica sempre pronto para receber. */
    esp_wifi_set_ps(WIFI_PS_NONE);
    /* Os dois nós precisam estar no mesmo canal. */
    esp_wifi_set_channel(channel, WIFI_SECOND_CHAN_NONE);

    if (esp_now_init() != ESP_OK)
    {
        return false;
    }
    esp_now_register_send_cb(on_sent);
    esp_now_register_recv_cb(on_recv);

    memcpy(peer_info.peer_addr, s_peer, 6);
    /* Canal 0 = acompanha o canal atual da interface. */
    peer_info.channel = 0;
    /* Sem criptografia: o quadro é só "N02,1,17". */
    peer_info.encrypt = false;
    return esp_now_add_peer(&peer_info) == ESP_OK;
}

bool radio_send(const char *frame_text)
{
    size_t frame_len = strlen(frame_text);
    int attempt;
    uint32_t start_ms;

    if ((frame_len == 0) || (frame_len > ESPNOW_MAX_PAYLOAD))
    {
        return false;
    }

    for (attempt = 0; attempt < SEND_ATTEMPTS; attempt++)
    {
        s_send_status = -1;
        /* Cast: a API do ESP-NOW recebe bytes; o texto é ASCII. */
        if (esp_now_send(s_peer, (const uint8_t *)frame_text, frame_len) ==
            ESP_OK)
        {
            start_ms = millis();
            while ((s_send_status < 0) &&
                   ((millis() - start_ms) < ACK_TIMEOUT_MS))
            {
                delay(1);
            }
            if (s_send_status == 1)
            {
                return true;
            }
        }
        delay(RETRY_GAP_MS);
    }
    return false;
}

void radio_set_rx_cb(void (*cb)(const uint8_t *, const char *, int, int))
{
    s_rx_cb = cb;
}
