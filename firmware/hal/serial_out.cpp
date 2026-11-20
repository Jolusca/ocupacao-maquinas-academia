#include <Arduino.h>
#include <stdarg.h>
#include <stdio.h>
#include "serial_out.h"

/* Tamanho do buffer de uma linha de log; o que passar disso é cortado por
 * vsnprintf. */
static const size_t LOG_BUF_LEN = 200;

void serial_emit_frame(const frame_t *frame)
{
    char text[FRAME_MAX_LEN];

    if (frame_encode(frame, text, sizeof(text)) > 0)
    {
        Serial.print(text);
        Serial.print('\n');
    }
    else
    {
        log_line("erro ao codificar quadro node=%u state=%u seq=%u",
                 frame->node, frame->state, frame->seq);
    }
}

void log_line(const char *fmt, ...)
{
    char text[LOG_BUF_LEN];
    va_list args;

    va_start(args, fmt);
    vsnprintf(text, sizeof(text), fmt, args);
    va_end(args);
    Serial.print("# ");
    Serial.print(text);
    Serial.print('\n');
}
