#include "scheduler.h"

/* TODO (colega): implementar. Os testes estao em test/test_scheduler.c. */

void sched_init(tx_sched_t *s)
{
    (void)s;
}

bool sched_due(const tx_sched_t *s, uint32_t now_ms, bool state_changed)
{
    (void)s; (void)now_ms; (void)state_changed;
    return false;
}

uint16_t sched_next_seq(tx_sched_t *s, uint32_t now_ms)
{
    (void)s; (void)now_ms;
    return 0xFFFFu;
}
