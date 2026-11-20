#ifndef SERIAL_OUT_H
#define SERIAL_OUT_H

#ifdef __cplusplus
extern "C"
{
#endif
#include "frame.h"
#ifdef __cplusplus
}
#endif

/* Saída pela serial USB do gateway (o servidor lê essas linhas).
 * Uma linha por quadro, terminada em '\n' (ex.: "N02,1,17\n"). */
void serial_emit_frame(const frame_t *frame);

/* Linha de log: começa com "# " e o servidor ignora. Mantenha o texto em ASCII:
 * a serial é lida por ferramentas que não sabem de acentos. Linhas maiores que
 * o buffer interno são cortadas. */
void log_line(const char *fmt, ...);

#endif
