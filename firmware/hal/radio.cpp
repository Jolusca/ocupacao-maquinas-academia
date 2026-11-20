#include <Arduino.h>
#include <WiFi.h>
#include <esp_now.h>
#include <esp_wifi.h>
#include <string.h>
#include "radio.h"

static uint8_t s_peer[6];
static volatile int s_send_status = -1;   /* -1 esperando, 0 falhou, 1 confirmado pelo MAC */
static void (*s_rx_cb)(const uint8_t *, const char *, int, int) = nullptr;

static void on_sent(const wifi_tx_info_t *, esp_now_send_status_t status)
{
    s_send_status = (status == ESP_NOW_SEND_SUCCESS) ? 1 : 0;
}

static void on_recv(const esp_now_recv_info_t *info, const uint8_t *data, int len)
{
    if (!s_rx_cb || len <= 0 || len > 250) return;
    char txt[251];
    memcpy(txt, data, (size_t)len);
    txt[len] = '\0';
    s_rx_cb(info->src_addr, txt, len, info->rx_ctrl->rssi);
}

bool radio_init(uint8_t channel, const uint8_t peer_mac[6])
{
    memcpy(s_peer, peer_mac, 6);
    WiFi.mode(WIFI_STA);
    WiFi.disconnect();
    esp_wifi_set_ps(WIFI_PS_NONE);
    esp_wifi_set_channel(channel, WIFI_SECOND_CHAN_NONE);

    if (esp_now_init() != ESP_OK) return false;
    esp_now_register_send_cb(on_sent);
    esp_now_register_recv_cb(on_recv);

    esp_now_peer_info_t pi = {};
    memcpy(pi.peer_addr, s_peer, 6);
    pi.channel = 0;                 /* 0 = acompanha o canal atual */
    pi.encrypt = false;
    return esp_now_add_peer(&pi) == ESP_OK;
}

bool radio_send(const char *frame_text)
{
    size_t n = strlen(frame_text);
    if (n == 0 || n > 250) return false;

    for (int tentativa = 0; tentativa < 3; tentativa++) {
        s_send_status = -1;
        if (esp_now_send(s_peer, (const uint8_t *)frame_text, n) == ESP_OK) {
            uint32_t t0 = millis();
            while (s_send_status < 0 && (millis() - t0) < 50) delay(1);
            if (s_send_status == 1) return true;
        }
        delay(10);
    }
    return false;
}

void radio_set_rx_cb(void (*cb)(const uint8_t *, const char *, int, int))
{
    s_rx_cb = cb;
}
