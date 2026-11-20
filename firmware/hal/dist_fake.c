#include "dist_source.h"

/* Roteiro da distancia simulada. Cada passo mantem a distancia por dur_ms.
 *   200 cm = ninguem na frente (ausencia)   60 cm = pessoa na frente (presenca)
 * Resultado esperado da maquina de estados (70 cm / 90 cm, 5 s e 90 s):
 *   0 a 20 s    LIVRE   (o passante de 2 s nao ocupa)
 *   ~25 s       vira OCUPADA (presenca por mais de 5 s)
 *   28 a 88 s   continua OCUPADA (descanso de 60 s, menos de 90 s)
 *   88 a 92 s   continua OCUPADA (a volta zera o cronometro de ausencia)
 *   ~182 s      vira LIVRE (ausencia por mais de 90 s)
 * O ciclo dura 192 s e se repete. */
typedef struct {
    int16_t     dist_cm;
    uint32_t    dur_ms;
    const char *nome;
} passo_t;

static const passo_t roteiro[] = {
    { 200,  10000u, "livre" },
    {  60,   2000u, "passante: 2 s a 60 cm" },
    { 200,   8000u, "livre de novo" },
    {  60,   8000u, "treino: 8 s a 60 cm" },
    { 200,  60000u, "descanso: 60 s ausente" },
    {  60,   4000u, "volta: 4 s a 60 cm" },
    { 200, 100000u, "liberacao: 100 s ausente" },
};

#define N_PASSOS ((unsigned)(sizeof roteiro / sizeof roteiro[0]))

uint32_t dist_fake_cycle_ms(void)
{
    uint32_t total = 0;
    for (unsigned i = 0; i < N_PASSOS; i++) total += roteiro[i].dur_ms;
    return total;
}

static const passo_t *passo_em(uint32_t now_ms)
{
    uint32_t t = now_ms % dist_fake_cycle_ms();
    for (unsigned i = 0; i < N_PASSOS; i++) {
        if (t < roteiro[i].dur_ms) return &roteiro[i];
        t -= roteiro[i].dur_ms;
    }
    return &roteiro[0];
}

int16_t dist_fake_read(uint32_t now_ms)
{
    return passo_em(now_ms)->dist_cm;
}

const char *dist_fake_step_name(uint32_t now_ms)
{
    return passo_em(now_ms)->nome;
}
