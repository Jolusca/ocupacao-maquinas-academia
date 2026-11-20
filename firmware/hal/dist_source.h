#ifndef DIST_SOURCE_H
#define DIST_SOURCE_H
/* Fonte de distância em cm. O programa principal escolhe uma das duas e não precisa saber qual é.
 * now_ms é o relógio do programa (pode estar acelerado, ver CFG_TIME_SCALE em app/config.h).
 * Devolve valor < 0 quando a leitura é inválida (sem eco). */
#include <stdint.h>

#ifdef __cplusplus
extern "C" {
#endif

typedef int16_t (*dist_read_fn)(uint32_t now_ms);

/* Instantes de referência do roteiro simulado (dist_fake.c confere em tempo de compilação que a
 * tabela bate com estes valores). Os testes usam estas constantes em vez de repetir números. */
#define DIST_FAKE_CYCLE_MS                192000u  /* duração de uma volta completa */
#define DIST_FAKE_TRAINING_START_MS        20000u  /* a pessoa chega e fica (treino) */
#define DIST_FAKE_FINAL_ABSENCE_START_MS   92000u  /* a pessoa sai de vez (liberação) */

/* dist_fake.c (C puro, roda também no PC): roteiro com os cenários passante, treino, descanso e
 * liberação. A distância depende só de now_ms, então o resultado é sempre o mesmo. */
int16_t     dist_fake_read(uint32_t now_ms);
uint32_t    dist_fake_cycle_ms(void);               /* duração de uma volta completa do roteiro */
const char *dist_fake_step_name(uint32_t now_ms);   /* nome do passo atual, para o log */

/* hcsr04.cpp: lê o sensor de verdade (só na placa). */
int16_t     dist_hcsr04_read(uint32_t now_ms);

#ifdef __cplusplus
}
#endif

#endif
