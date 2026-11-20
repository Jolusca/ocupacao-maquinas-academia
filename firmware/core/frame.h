#ifndef FRAME_H
#define FRAME_H
/* Quadro do contrato: "N<id>,<estado>,<seq>", por exemplo "N02,1,17".
 *  - id: 1 a 99, sempre com 2 digitos (N01, N02, ..., N99)
 *  - estado: 1 = ocupada, 0 = livre
 *  - seq: 0 a 65535 (depois de 65535 volta a 0)
 * Codigo C puro: nao pode incluir nada de hardware. */
#include <stddef.h>
#include <stdint.h>

#define FRAME_MAX_LEN 16 /* "N99,1,65535" tem 11 caracteres; sobra espaco para '\n' e '\0' */

#define FRAME_OK          0
#define FRAME_ERR_FORMAT -1 /* nao tem o formato N<2 digitos>,<digitos>,<digitos> */
#define FRAME_ERR_RANGE  -2 /* formato certo, mas id fora de 1..99, estado fora de 0..1 ou seq acima de 65535 */

typedef struct {
    uint8_t  node;  /* 1..99 */
    uint8_t  state; /* 0 ou 1 */
    uint16_t seq;
} frame_t;

/* Escreve o texto do quadro em `out` (sem '\n'), terminado em '\0'.
 * Devolve o numero de caracteres escritos (sem contar o '\0') ou -1 se
 * node nao esta em 1..99, state nao e 0 ou 1, ou out_size nao comporta o texto + '\0'. */
int frame_encode(const frame_t *f, char *out, size_t out_size);

/* Le uma linha recebida. Aceita '\n' ou "\r\n" no final. Devolve FRAME_OK e preenche `f`,
 * ou FRAME_ERR_FORMAT / FRAME_ERR_RANGE (e nao altera `f`). Nao pode estourar com numeros grandes. */
int frame_decode(const char *line, frame_t *f);

#endif
