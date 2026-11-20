#ifndef DIST_SOURCE_H
#define DIST_SOURCE_H
/* Fonte de distancia: o programa principal chama uma destas e nao sabe qual e. */
#include <stdint.h>

typedef int16_t (*dist_read_fn)(void);

/* Le um roteiro de cenarios (passante, treino, descanso, liberacao) com relogio acelerado.
 * Permite testar o sistema inteiro sem o sensor. */
int16_t dist_fake_read(void);

/* Le o HC-SR04 de verdade. */
int16_t dist_hcsr04_read(void);
#endif
