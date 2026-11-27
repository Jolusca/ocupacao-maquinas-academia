#ifndef COMMAND_H
#define COMMAND_H
/* Comandos de configuracao que o no aceita pela serial (uma linha por comando):
 *   id <1..99>                         numero do no (N01, N02, ...); fica gravado na flash
 *   papel auto | coletor | sensor      papel do no; fica gravado na flash
 *   info                               mostra a configuracao atual
 *   limpar                             apaga o que foi gravado (volta ao padrao)
 * So minusculas, para haver um jeito so de escrever. C puro. */
#include "link.h"
#include <stdint.h>

#define CMD_OK          0
#define CMD_ERR_EMPTY  -1 /* linha vazia: ignorar em silencio */
#define CMD_ERR_UNKNOWN -2 /* nao e um comando conhecido */
#define CMD_ERR_ARG    -3 /* comando conhecido, argumento faltando ou invalido */

typedef enum { CMD_NONE = 0, CMD_ID, CMD_ROLE, CMD_INFO, CMD_CLEAR } cmd_kind_t;

typedef struct {
    cmd_kind_t  kind;
    uint8_t     id;   /* CMD_ID */
    role_mode_t mode; /* CMD_ROLE */
} cmd_t;

/* Le uma linha (aceita '\n' ou "\r\n" no fim e espacos sobrando). Devolve CMD_OK e preenche
 * `out`, ou um CMD_ERR_* e nao altera `out`. */
int cmd_parse(const char *line, cmd_t *out);

#endif
