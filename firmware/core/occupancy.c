#include "occupancy.h"

void occ_init(occ_t *o, const occ_cfg_t *cfg)
{
    *o = (occ_t){ .cfg = *cfg, .state = OCC_FREE };
}

bool occ_update(occ_t *o, uint32_t now_ms, int16_t dist_cm)
{
    if (dist_cm < 0) {
        o->present = false;
    } else if (dist_cm <= o->cfg.arrive_cm) {
        o->present = true;
    } else if (dist_cm >= o->cfg.leave_cm) {
        o->present = false;
    }
    // Na zona morta -> preservar a condicao anterior e seu cronometro

    if (o->present == (o->state == OCC_BUSY)) {
        o->timing = false;
        o->since_ms = 0;
        return false;
    }

    if (!o->timing) {
        o->timing = true;
        o->since_ms = now_ms;
    }

    const uint32_t threshold_ms = o->present
        ? o->cfg.presence_ms : o->cfg.absence_ms;
    // Subtracao sem sinal -> volta do relogio de 32 bits
    if ((uint32_t)(now_ms - o->since_ms) > threshold_ms) {
        o->state = o->present ? OCC_BUSY : OCC_FREE;
        o->timing = false;
        o->since_ms = 0;
        return true;
    }

    return false;
}

occ_state_t occ_state(const occ_t *o)
{
    return o->state;
}

void filter_init(filter_t *f)
{
    *f = (filter_t){0};
}

int16_t filter_median3(filter_t *f, int16_t sample)
{
    f->buf[f->idx] = sample;
    f->idx = (uint8_t)((f->idx + 1u) % 3u);
    if (f->n < 3u) {
        ++f->n;
    }
    if (f->n < 3u) {
        return sample;
    }

    // p/ ordenar as copias locais sem alterar a ordem do buffer circular
    int16_t a = f->buf[0];
    int16_t b = f->buf[1];
    int16_t c = f->buf[2];
    int16_t tmp;
    if (a > b) {
        tmp = a;
        a = b;
        b = tmp;
    }
    if (b > c) {
        tmp = b;
        b = c;
        c = tmp;
    }
    if (a > b) {
        tmp = a;
        a = b;
        b = tmp;
    }
    return b;
}
