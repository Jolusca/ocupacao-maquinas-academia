#include "../core/occupancy.h"
#include "../hal/dist_fake.h"
#include "minitest.h"

/* Teste de integração: roda o roteiro da distância simulada (hal/dist_fake.c)
 * pela cadeia filtro de mediana + máquina de estados (core/occupancy.c), a cada
 * 100 ms, por 2 ciclos, e confere quando o estado muda. Passa quando o core
 * estiver correto.
 *
 * Os instantes esperados saem das constantes de hal/dist_fake.h e da
 * configuração da máquina de estados (presence_ms, absence_ms), então nada aqui
 * repete números do roteiro. */

#define STEP_MS 100u
#define TOLERANCE_MS                                                           \
    500u /* o filtro de mediana atrasa a decisão em até 1 leitura */

static void check_window(const char *name, uint32_t actual_ms,
                         uint32_t expected_ms)
{
    mt_total++;
    if ((actual_ms < expected_ms) || (actual_ms > (expected_ms + TOLERANCE_MS)))
    {
        mt_fail++;
        /* Casts: uint32_t para unsigned, que é o que o %u imprime. */
        printf("  FALHOU %s: mudou em %u ms (esperado entre %u e %u)\n", name,
               (unsigned)actual_ms, (unsigned)expected_ms,
               (unsigned)(expected_ms + TOLERANCE_MS));
    }
}

int main(void)
{
    occ_t occ;
    filter_t filter;
    const occ_cfg_t cfg = OCC_CFG_DEFAULT;
    const uint32_t cycle_ms = dist_fake_cycle_ms();
    /* quando o estado deve mudar, no 1o ciclo */
    const uint32_t busy_at_ms = DIST_FAKE_TRAINING_START_MS + cfg.presence_ms;
    const uint32_t free_at_ms =
        DIST_FAKE_FINAL_ABSENCE_START_MS + cfg.absence_ms;
    uint32_t busy_times[2] = { 0, 0 };
    uint32_t free_times[2] = { 0, 0 };
    int busy_count = 0;
    int free_count = 0;
    int changes = 0;
    uint32_t time_ms;

    TEST("a duração do roteiro é a das constantes");
    CHECK_INT(cycle_ms, DIST_FAKE_CYCLE_MS);

    TEST("roteiro simulado -> filtro -> máquina de estados (2 ciclos)");
    occ_init(&occ, &cfg);
    filter_init(&filter);
    for (time_ms = 0; time_ms < ((2 * cycle_ms) + 5000u); time_ms += STEP_MS)
    {
        int16_t dist_cm = dist_fake_read(time_ms);
        int16_t filtered_cm = filter_median3(&filter, dist_cm);

        if (occ_update(&occ, time_ms, filtered_cm))
        {
            changes++;
            if (occ_state(&occ) == OCC_BUSY)
            {
                if (busy_count < 2)
                {
                    busy_times[busy_count++] = time_ms;
                }
            }
            else
            {
                if (free_count < 2)
                {
                    free_times[free_count++] = time_ms;
                }
            }
        }
        /* pontos de verificação do 1o ciclo, relativos aos instantes
         * esperados */
        if (time_ms == (busy_at_ms - 1000u)) /* o passante não ocupou */
        {
            CHECK_INT(occ_state(&occ), OCC_FREE);
        }
        if (time_ms == (busy_at_ms + 5000u)) /* treino: ocupada */
        {
            CHECK_INT(occ_state(&occ), OCC_BUSY);
        }
        if (time_ms == (busy_at_ms + 60000u)) /* meio do descanso: continua */
        {
            CHECK_INT(occ_state(&occ), OCC_BUSY);
        }
        if (time_ms == (free_at_ms - 1000u)) /* ainda não passou de 90 s */
        {
            CHECK_INT(occ_state(&occ), OCC_BUSY);
        }
        if (time_ms == (free_at_ms + 1500u)) /* liberou */
        {
            CHECK_INT(occ_state(&occ), OCC_FREE);
        }
    }

    TEST("só 4 mudanças de estado em 2 ciclos");
    CHECK_INT(changes, 4);
    CHECK_INT(busy_count, 2);
    CHECK_INT(free_count, 2);

    TEST("instantes das mudanças");
    check_window("1a ocupada", busy_times[0], busy_at_ms);
    check_window("1a livre", free_times[0], free_at_ms);
    check_window("2a ocupada", busy_times[1], cycle_ms + busy_at_ms);
    check_window("2a livre", free_times[1], cycle_ms + free_at_ms);

    TEST_RESULT();
}
