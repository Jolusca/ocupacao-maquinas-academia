#include <Arduino.h>
#include <stdarg.h>
#include <stdio.h>
#include "serial_out.h"

/* Tamanho do buffer de uma linha de log; o que passar disso é cortado por vsnprintf. */
static const size_t LOG_BUF_LEN = 200;

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
    char buf[LOG_BUF_LEN];
    va_list ap;
    va_start(ap, fmt);
    vsnprintf(buf, sizeof buf, fmt, ap);
    va_end(ap);
    Serial.print("# ");
    Serial.print(buf);
    Serial.print('\n');
}
