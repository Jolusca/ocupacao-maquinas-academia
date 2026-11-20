#include "../core/occupancy.h"
#include "../hal/dist_source.h"
#include "minitest.h"

/* Teste de integração: roda o roteiro da distância simulada (hal/dist_fake.c) pela cadeia
 * filtro de mediana + máquina de estados (core/occupancy.c), a cada 100 ms, por 2 ciclos,
 * e confere quando o estado muda. Passa quando o core estiver correto.
 *
 * Os instantes esperados saem das constantes de hal/dist_source.h e da configuração da máquina de
 * estados (presence_ms, absence_ms), então nada aqui repete números do roteiro. */

#define PASSO_MS 100u
#define TOLERANCIA_MS 500u   /* o filtro de mediana atrasa a decisão em até uma leitura */

static void checa_janela(const char *nome, uint32_t t, uint32_t esperado)
{
    mt_total++;
    if (t < esperado || t > esperado + TOLERANCIA_MS) {
        mt_fail++;
        printf("  FALHOU %s: mudou em %u ms (esperado entre %u e %u)\n", nome, (unsigned)t,
               (unsigned)esperado, (unsigned)(esperado + TOLERANCIA_MS));
    }
}

int main(void)
{
    occ_t o;
    filter_t f;
    const occ_cfg_t cfg = OCC_CFG_DEFAULT;
    const uint32_t ciclo = dist_fake_cycle_ms();
    /* quando o estado deve mudar, no 1º ciclo */
    const uint32_t ocupa = DIST_FAKE_TRAINING_START_MS + cfg.presence_ms;
    const uint32_t libera = DIST_FAKE_FINAL_ABSENCE_START_MS + cfg.absence_ms;
    uint32_t t_busy[2] = {0, 0}, t_free[2] = {0, 0};
    int nb = 0, nf = 0, mudancas = 0;

    TEST("a duração do roteiro é a das constantes");
    CHECK_INT(ciclo, DIST_FAKE_CYCLE_MS);

    TEST("roteiro simulado -> filtro -> máquina de estados (2 ciclos)");
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
        /* pontos de verificação do 1º ciclo, sempre relativos aos instantes esperados */
        if (t == ocupa - 1000u)   CHECK_INT(occ_state(&o), OCC_FREE);   /* o passante não ocupou */
        if (t == ocupa + 5000u)   CHECK_INT(occ_state(&o), OCC_BUSY);   /* treino: ocupada */
        if (t == ocupa + 60000u)  CHECK_INT(occ_state(&o), OCC_BUSY);   /* no meio do descanso: continua */
        if (t == libera - 1000u)  CHECK_INT(occ_state(&o), OCC_BUSY);   /* ainda não passou de 90 s ausente */
        if (t == libera + 1500u)  CHECK_INT(occ_state(&o), OCC_FREE);   /* liberou */
    }

    TEST("só 4 mudanças de estado em 2 ciclos");
    CHECK_INT(mudancas, 4);
    CHECK_INT(nb, 2);
    CHECK_INT(nf, 2);

    TEST("instantes das mudanças");
    checa_janela("1a ocupada", t_busy[0], ocupa);
    checa_janela("1a livre",   t_free[0], libera);
    checa_janela("2a ocupada", t_busy[1], ciclo + ocupa);
    checa_janela("2a livre",   t_free[1], ciclo + libera);

    TEST_RESULT();
}
