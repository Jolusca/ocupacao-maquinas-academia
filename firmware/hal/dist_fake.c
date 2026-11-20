#include "dist_source.h"

/* Roteiro da distância simulada. Cada passo mantém a distância por dur_ms.
 *   200 cm = ninguém na frente (ausência)     60 cm = pessoa na frente (presença)
 *
 * Resultado esperado da máquina de estados (histerese 70/90 cm, 5 s para ocupar, 90 s para liberar):
 *   - o passante de 2 s não ocupa a máquina;
 *   - o treino de 8 s ocupa (passa de 5 s de presença);
 *   - o descanso de 60 s não libera (menos de 90 s de ausência);
 *   - a volta de 4 s zera o cronômetro de ausência;
 *   - a ausência final de 100 s libera (passa de 90 s).
 * Os instantes exatos ficam em dist_source.h; os _Static_assert abaixo impedem que a tabela
 * e essas constantes saiam de sincronia. */

enum {
    D_IDLE_1   = 10000,
    D_PASSERBY = 2000,
    D_IDLE_2   = 8000,
    D_WORKOUT  = 8000,
    D_REST     = 60000,
    D_RETURN   = 4000,
    D_RELEASE  = 100000
};

_Static_assert(D_IDLE_1 + D_PASSERBY + D_IDLE_2 == DIST_FAKE_TRAINING_START_MS,
               "o treino começa depois de D_IDLE_1 + D_PASSERBY + D_IDLE_2");
_Static_assert(D_IDLE_1 + D_PASSERBY + D_IDLE_2 + D_WORKOUT + D_REST + D_RETURN == DIST_FAKE_FINAL_ABSENCE_START_MS,
               "a ausência final começa depois da volta");
_Static_assert(D_IDLE_1 + D_PASSERBY + D_IDLE_2 + D_WORKOUT + D_REST + D_RETURN + D_RELEASE == DIST_FAKE_CYCLE_MS,
               "a soma dos passos é a duração do ciclo");

typedef struct {
    int16_t     dist_cm;
    uint32_t    dur_ms;
    const char *name;
} step_t;

static const step_t script[] = {
    { 200, D_IDLE_1,   "livre" },
    {  60, D_PASSERBY, "passante: 2 s a 60 cm" },
    { 200, D_IDLE_2,   "livre de novo" },
    {  60, D_WORKOUT,  "treino: 8 s a 60 cm" },
    { 200, D_REST,     "descanso: 60 s ausente" },
    {  60, D_RETURN,   "volta: 4 s a 60 cm" },
    { 200, D_RELEASE,  "liberacao: 100 s ausente" },
};

#define N_STEPS ((unsigned)(sizeof script / sizeof script[0]))

uint32_t dist_fake_cycle_ms(void)
{
    return DIST_FAKE_CYCLE_MS;
}

/* Acha o passo que está valendo em now_ms: reduz now_ms ao ciclo e anda pela tabela. */
static const step_t *step_at(uint32_t now_ms)
{
    uint32_t t = now_ms % DIST_FAKE_CYCLE_MS;
    for (unsigned i = 0; i < N_STEPS; i++) {
        if (t < script[i].dur_ms) return &script[i];
        t -= script[i].dur_ms;
    }
    return &script[0];   /* inalcançável: os _Static_assert garantem que a soma fecha o ciclo */
}

int16_t dist_fake_read(uint32_t now_ms)
{
    return step_at(now_ms)->dist_cm;
}

const char *dist_fake_step_name(uint32_t now_ms)
{
    return step_at(now_ms)->name;
}
