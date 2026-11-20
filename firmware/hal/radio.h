#ifndef RADIO_H
#define RADIO_H
#include <stdbool.h>
#include <stdint.h>

/* ESP-NOW: rádio Wi-Fi de 2,4 GHz, sem roteador e sem conexão. Canal fixo (11 nos ensaios). */

/* Liga o rádio no canal dado e registra o par (o outro nó). */
bool radio_init(uint8_t channel, const uint8_t peer_mac[6]);

/* Envia o texto do quadro ao par (unicast). Até 3 tentativas.
 * true somente se o MAC do outro lado confirmou a entrega. */
bool radio_send(const char *frame_text);

/* Registra quem trata os quadros recebidos. O callback roda na tarefa do Wi-Fi:
 * deve ser curto (copiar e sair), sem Serial nem bloqueio. */
void radio_set_rx_cb(void (*cb)(const uint8_t *mac, const char *payload, int len, int rssi));
#endif
