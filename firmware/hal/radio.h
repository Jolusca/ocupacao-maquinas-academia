#ifndef RADIO_H
#define RADIO_H
#include <stdbool.h>
#include <stdint.h>

/* ESP-NOW. Canal fixo (11 nos testes), sem Wi-Fi conectado. */
bool radio_init(uint8_t channel, const uint8_t peer_mac[6]);
/* Unicast ao par. Ate 3 tentativas. true se o MAC confirmou a entrega. */
bool radio_send(const char *frame_text);
void radio_set_rx_cb(void (*cb)(const uint8_t *mac, const char *payload, int len, int rssi));
#endif
