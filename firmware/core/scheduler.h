#ifndef SCHEDULER_H
#define SCHEDULER_H
/* Decide QUANDO enviar um quadro e entrega o numero de sequencia.
 * Envia quando: (a) o estado mudou, (b) passaram 15 s desde o ultimo envio (sinal de vida),
 * ou (c) ainda nao enviou nada. C puro: o tempo entra como argumento. */
#include <stdbool.h>
#include <stdint.h>

#define SCHED_HEARTBEAT_MS 15000u

typedef struct {
    uint32_t last_tx_ms;
    uint16_t next_seq;
    bool     sent_once;
} tx_sched_t;

void     sched_init(tx_sched_t *s);
/* true se deve enviar agora. now_ms pode dar a volta (uint32): use subtracao sem sinal. */
bool     sched_due(const tx_sched_t *s, uint32_t now_ms, bool state_changed);
/* Registra o envio (guarda now_ms) e devolve o seq a usar: 0, 1, 2, ..., 65535, 0, ... */
uint16_t sched_next_seq(tx_sched_t *s, uint32_t now_ms);

#endif
