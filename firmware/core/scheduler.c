#include "scheduler.h"

void sched_init(tx_sched_t *s)
{
    s->last_tx_ms = 0;
    s->next_seq = 0;
    s->sent_once = false;
}

bool sched_due(const tx_sched_t *s, uint32_t now_ms, bool state_changed)
{
    return state_changed || !s->sent_once ||
           (uint32_t)(now_ms - s->last_tx_ms) >= SCHED_HEARTBEAT_MS;
}

uint16_t sched_next_seq(tx_sched_t *s, uint32_t now_ms)
{
    uint16_t seq = s->next_seq;

    s->next_seq = (uint16_t)(seq + 1u);
    s->last_tx_ms = now_ms;
    s->sent_once = true;

    return seq;
}
