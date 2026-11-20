#include "../core/occupancy.h"
#include "../hal/dist_source.h"
#include "minitest.h"

/* Teste de integracao: roda o roteiro da distancia simulada (hal/dist_fake.c) pela cadeia
 * filtro de mediana + maquina de estados (core/occupancy.c), a cada 100 ms, por 2 ciclos,
 * e confere quando o estado muda. Passa quando o core do Anderson estiver correto.
 *
 * Linha do tempo de um ciclo (192 s), ver o comentario em hal/dist_fake.c:
 *   ~25 s vira OCUPADA | ate 182 s continua OCUPADA (descanso e volta) | ~182 s vira LIVRE */

#define PASSO_MS 100u

static void checa_janela(const char *nome, uint32_t t, uint32_t min_ms, uint32_t max_ms)
{
    mt_total++;
    if (t < min_ms || t > max_ms) {
        mt_fail++;
        printf("  FALHOU %s: mudou em %u ms (esperado entre %u e %u)\n", nome, (unsigned)t, (unsigned)min_ms, (unsigned)max_ms);
    }
}

int main(void)
{
    occ_t o;
    filter_t f;
    const occ_cfg_t cfg = OCC_CFG_DEFAULT;
    uint32_t ciclo = dist_fake_cycle_ms();
    uint32_t t_busy[2] = {0, 0}, t_free[2] = {0, 0};
    int nb = 0, nf = 0, mudancas = 0;

    TEST("o roteiro dura 192 s");
    CHECK_INT(ciclo, 192000);

    TEST("roteiro simulado -> filtro -> maquina de estados (2 ciclos)");
    occ_init(&o, &cfg);
    filter_init(&f);
    for (uint32_t t = 0; t < 2 * ciclo + 5000u; t += PASSO_MS) {
        int16_t d = dist_fake_read(t);
        int16_t filtrada = filter_median3(&f, d);
        if (occ_update(&o, t, filtrada)) {
            mudancas++;
            if (occ_state(&o) == OCC_BUSY) { if (nb < 2) t_busy[nb++] = t; }
            else                           { if (nf < 2) t_free[nf++] = t; }
        }
        /* pontos de verificacao do 1o ciclo */
        if (t == 24000u)  CHECK_INT(occ_state(&o), OCC_FREE);   /* o passante nao ocupou */
        if (t == 30000u)  CHECK_INT(occ_state(&o), OCC_BUSY);   /* treino: ocupada */
        if (t == 87000u)  CHECK_INT(occ_state(&o), OCC_BUSY);   /* descanso de 59 s: continua */
        if (t == 100000u) CHECK_INT(occ_state(&o), OCC_BUSY);   /* depois da volta: continua */
        if (t == 181000u) CHECK_INT(occ_state(&o), OCC_BUSY);   /* ainda nao passou de 90 s ausente */
        if (t == 183500u) CHECK_INT(occ_state(&o), OCC_FREE);   /* liberou */
    }

    TEST("so 4 mudancas de estado em 2 ciclos");
    CHECK_INT(mudancas, 4);
    CHECK_INT(nb, 2);
    CHECK_INT(nf, 2);

    TEST("instantes das mudancas");
    checa_janela("1a ocupada", t_busy[0], 25000u, 25500u);
    checa_janela("1a livre",   t_free[0], 182000u, 182600u);
    checa_janela("2a ocupada", t_busy[1], ciclo + 25000u, ciclo + 25500u);
    checa_janela("2a livre",   t_free[1], ciclo + 182000u, ciclo + 182600u);

    TEST_RESULT();
}
