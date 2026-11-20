#include <Arduino.h>
#include <stdarg.h>
#include <stdio.h>
#include "serial_out.h"

void serial_emit_frame(const frame_t *f)
{
    char buf[FRAME_MAX_LEN];
    if (frame_encode(f, buf, sizeof buf) > 0) {
        Serial.print(buf);
        Serial.print('\n');
    } else {
        log_line("erro ao codificar quadro node=%u state=%u seq=%u", f->node, f->state, f->seq);
    }
}

void log_line(const char *fmt, ...)
{
    char buf[200];
    va_list ap;
    va_start(ap, fmt);
    vsnprintf(buf, sizeof buf, fmt, ap);
    va_end(ap);
    Serial.print("# ");
    Serial.print(buf);
    Serial.print('\n');
}
