#ifndef RADIO_H
#define RADIO_H
#include <stdbool.h>
#include <stdint.h>

/* ESP-NOW: rádio Wi-Fi de 2,4 GHz, sem roteador e sem conexão. Canal fixo (11
 * nos ensaios).
 *
 * Nenhum nó tem endereço fixo: o coletor se anuncia por broadcast e os
 * sensores registram o endereço dele (radio_set_peer). Sem coletor conhecido,
 * os quadros vão por broadcast, que o coletor também recebe. */

/* Liga o rádio no canal dado. Não registra nenhum par ainda. */
bool radio_init(uint8_t channel);

/* Define o coletor atual: os quadros passam a ir só a ele (unicast, com
 * confirmação). */
bool radio_set_peer(const uint8_t mac[6]);

/* Esquece o coletor: os quadros voltam a ir por broadcast. */
void radio_clear_peer(void);

/* Envia o texto do quadro. Com coletor definido: unicast, até 3 tentativas, e
 * true somente se o MAC do outro lado confirmou a entrega. Sem coletor:
 * broadcast em uma tentativa, e true se a transmissão saiu (ninguém confirma). */
bool radio_send(const char *frame_text);

/* Uma transmissão por broadcast (os avisos do coletor). true se saiu. */
bool radio_broadcast(const char *text);

/* Registra quem trata os quadros recebidos. O callback roda na tarefa do Wi-Fi:
 * deve ser curto (copiar e sair), sem Serial nem bloqueio. */
void radio_set_rx_cb(void (*cb)(const uint8_t *mac, const char *payload,
                                int len, int rssi));
#endif
