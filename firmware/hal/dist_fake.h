#ifndef DIST_FAKE_H
#define DIST_FAKE_H
/* Distância simulada em cm, no lugar do sensor (roteiro com os cenários
 * passante, treino, descanso e liberação). Código C puro: roda também no PC.
 * now_ms é o relógio do programa (pode estar acelerado, ver CFG_TIME_SCALE em
 * app/config.h). A distância depende só de now_ms, então o resultado é sempre
 * o mesmo. */
#include <stdint.h>

#ifdef __cplusplus
extern "C"
{
#endif

/* Instantes de referência do roteiro (dist_fake.c confere em tempo de
 * compilação que a tabela bate com estes valores). Os testes usam estas
 * constantes em vez de repetir números. */

/* Uma volta completa do roteiro. */
#define DIST_FAKE_CYCLE_MS 192000u
/* A pessoa chega e fica (treino). */
#define DIST_FAKE_TRAINING_START_MS 20000u
/* A pessoa sai de vez (liberação). */
#define DIST_FAKE_FINAL_ABSENCE_START_MS 92000u

int16_t dist_fake_read(uint32_t now_ms);
uint32_t dist_fake_cycle_ms(void);

/* Nome do passo atual, para o log. */
const char *dist_fake_step_name(uint32_t now_ms);

#ifdef __cplusplus
}
#endif

#endif
