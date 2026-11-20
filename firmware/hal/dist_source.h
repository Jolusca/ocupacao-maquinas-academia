#ifndef DIST_SOURCE_H
#define DIST_SOURCE_H
/* Fonte de distancia em cm. O programa principal escolhe uma das duas e nao precisa saber qual e.
 * now_ms e o relogio do programa (pode estar acelerado, ver CFG_TIME_SCALE em app/config.h).
 * Devolve valor < 0 quando a leitura e invalida (sem eco). */
#include <stdint.h>

#ifdef __cplusplus
extern "C" {
#endif

typedef int16_t (*dist_read_fn)(uint32_t now_ms);

/* dist_fake.c (C puro, roda tambem no PC): roteiro com os cenarios passante, treino, descanso e
 * liberacao. A distancia depende so de now_ms, entao o resultado e sempre o mesmo. */
int16_t     dist_fake_read(uint32_t now_ms);
uint32_t    dist_fake_cycle_ms(void);               /* duracao de uma volta completa do roteiro */
const char *dist_fake_step_name(uint32_t now_ms);   /* nome do passo atual, para o log */

/* hcsr04.cpp: le o sensor de verdade (so na placa). */
int16_t     dist_hcsr04_read(uint32_t now_ms);

#ifdef __cplusplus
}
#endif

#endif
