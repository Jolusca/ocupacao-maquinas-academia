#include "occupancy.h"

/* TODO (colega): implementar. Os testes estao em test/test_occupancy.c. */

void occ_init(occ_t *o, const occ_cfg_t *cfg)
{
    (void)o; (void)cfg;
}

bool occ_update(occ_t *o, uint32_t now_ms, int16_t dist_cm)
{
    (void)o; (void)now_ms; (void)dist_cm;
    return false;
}

occ_state_t occ_state(const occ_t *o)
{
    (void)o;
    return OCC_FREE;
}

void filter_init(filter_t *f)
{
    (void)f;
}

int16_t filter_median3(filter_t *f, int16_t sample)
{
    (void)f;
    (void)sample;
    return -1;
}
