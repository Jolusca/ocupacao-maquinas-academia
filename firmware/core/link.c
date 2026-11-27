#include "link.h"
#include <string.h>

void role_init(role_state_t *r, role_mode_t mode, bool host_present)
{
    r->mode     = mode;
    r->timing   = false;
    r->since_ms = 0;
    if (mode == ROLE_MODE_SINK) {
        r->role = ROLE_SINK;
    } else if (mode == ROLE_MODE_SENSOR) {
        r->role = ROLE_SENSOR;
    } else {
        r->role = host_present ? ROLE_SINK : ROLE_SENSOR;
    }
}

role_t role_update(role_state_t *r, uint32_t now_ms, bool host_present)
{
    bool     wants_sink;
    uint32_t wait_ms;

    if (r->mode == ROLE_MODE_SINK) {
        r->role = ROLE_SINK;
        return r->role;
    }
    if (r->mode == ROLE_MODE_SENSOR) {
        r->role = ROLE_SENSOR;
        return r->role;
    }

    wants_sink = host_present;
    if (wants_sink == (r->role == ROLE_SINK)) {
        r->timing = false; /* a USB concorda com o papel: nada a mudar */
        return r->role;
    }
    if (!r->timing) {
        r->timing   = true;
        r->since_ms = now_ms;
    }
    wait_ms = wants_sink ? ROLE_SINK_ON_MS : ROLE_SINK_OFF_MS;
    /* Subtracao sem sinal: vale mesmo quando o relogio de 32 bits da a volta. */
    if ((uint32_t)(now_ms - r->since_ms) >= wait_ms) {
        r->role   = wants_sink ? ROLE_SINK : ROLE_SENSOR;
        r->timing = false;
    }
    return r->role;
}

void role_set_mode(role_state_t *r, role_mode_t mode, bool host_present)
{
    role_t keep = r->role;

    role_init(r, mode, host_present);
    if (mode == ROLE_MODE_AUTO) {
        r->role = keep; /* nao muda de papel de supetao: a USB decide pela histerese */
    }
}

void sink_init(sink_link_t *s)
{
    memset(s, 0, sizeof(*s));
}

bool sink_on_beacon(sink_link_t *s, const uint8_t mac[6], uint32_t now_ms)
{
    bool changed = !s->known || (memcmp(s->mac, mac, 6) != 0);

    memcpy(s->mac, mac, 6);
    s->known          = true;
    s->last_beacon_ms = now_ms;
    s->fails          = 0; /* ouvimos o coletor agora: ele esta vivo */
    return changed;
}

bool sink_known(sink_link_t *s, uint32_t now_ms)
{
    if (s->known && ((uint32_t)(now_ms - s->last_beacon_ms) > LINK_SINK_TIMEOUT_MS)) {
        s->known = false;
    }
    return s->known;
}

const uint8_t *sink_mac(const sink_link_t *s)
{
    return s->mac;
}

void sink_on_delivery(sink_link_t *s, bool ok)
{
    if (ok) {
        s->fails = 0;
        return;
    }
    if (s->fails < 255u) {
        s->fails++;
    }
    if (s->fails >= LINK_SEND_FAIL_LIMIT) {
        s->known = false;
    }
}

bool link_beacon_due(bool sent_once, uint32_t last_ms, uint32_t now_ms)
{
    return !sent_once || ((uint32_t)(now_ms - last_ms) >= LINK_BEACON_PERIOD_MS);
}
