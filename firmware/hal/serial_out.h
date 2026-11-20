#ifndef SERIAL_OUT_H
#define SERIAL_OUT_H

#ifdef __cplusplus
extern "C" {
#endif
#include "frame.h"
#ifdef __cplusplus
}
#endif

/* Saida pela serial USB do gateway (o servidor le essas linhas).
 * Uma linha por quadro, terminada em '\n' (ex.: "N02,1,17\n"). */
void serial_emit_frame(const frame_t *f);

/* Linha de log: comeca com "# " e o servidor ignora. */
void log_line(const char *fmt, ...);

#endif
