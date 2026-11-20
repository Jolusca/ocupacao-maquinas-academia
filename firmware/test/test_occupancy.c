#include "../core/occupancy.h"
#include "minitest.h"

/* Alimenta a máquina com a mesma distância a cada 100 ms durante dur_ms.
 * Devolve quantas vezes o estado mudou. O relógio é global para encadear
 * cenários. */
static uint32_t s_now_ms = 1000;

static int feed(occ_t *occ, int16_t dist_cm, uint32_t dur_ms)
{
    int changes = 0;
    uint32_t elapsed_ms;

    for (elapsed_ms = 0; elapsed_ms < dur_ms; elapsed_ms += 100)
    {
        if (occ_update(occ, s_now_ms, dist_cm))
        {
            changes++;
        }
        s_now_ms += 100;
    }
    return changes;
}

static void fresh(occ_t *occ)
{
    const occ_cfg_t cfg = OCC_CFG_DEFAULT;

    occ_init(occ, &cfg);
    s_now_ms = 1000;
}

static void make_busy(occ_t *occ)
{
    fresh(occ);
    CHECK_INT(feed(occ, 60, 5100), 0);
    CHECK_INT(feed(occ, 60, 300), 1);
    CHECK_INT(occ_state(occ), OCC_BUSY);
}

int main(void)
{
    occ_t occ;
    filter_t filter;

    TEST("estado inicial e LIVRE");
    fresh(&occ);
    CHECK_INT(occ_state(&occ), OCC_FREE);

    TEST("passante: 2 s a 60 cm e vai embora -> continua LIVRE");
    fresh(&occ);
    CHECK_INT(feed(&occ, 60, 2000), 0);
    CHECK_INT(feed(&occ, 150, 10000), 0);
    CHECK_INT(occ_state(&occ), OCC_FREE);

    TEST("treino: presenca por mais de 5 s -> OCUPADA (uma unica mudanca)");
    fresh(&occ);
    CHECK_INT(feed(&occ, 60, 5100), 0); /* ate 5000 ms: ainda LIVRE */
    CHECK_INT(occ_state(&occ), OCC_FREE);
    CHECK_INT(feed(&occ, 60, 300), 1); /* passou de 5000 ms */
    CHECK_INT(occ_state(&occ), OCC_BUSY);
    CHECK_INT(feed(&occ, 60, 20000), 0); /* nao muda de novo */

    TEST("descanso: ausencia curta (60 s) -> continua OCUPADA");
    make_busy(&occ);
    CHECK_INT(feed(&occ, 150, 60000), 0);
    CHECK_INT(occ_state(&occ), OCC_BUSY);

    TEST("descanso: a ausencia precisa ser CONTINUA (volta a 60 cm zera)");
    make_busy(&occ);
    CHECK_INT(feed(&occ, 150, 60000), 0);
    CHECK_INT(feed(&occ, 60, 1000), 0);
    CHECK_INT(feed(&occ, 150, 60000),
              0); /* 120 s no total, nunca 90 s seguidos */
    CHECK_INT(occ_state(&occ), OCC_BUSY);

    TEST("liberacao: ausencia por mais de 90 s -> LIVRE");
    make_busy(&occ);
    CHECK_INT(feed(&occ, 150, 90000), 0); /* ate 90000 ms: ainda OCUPADA */
    CHECK_INT(occ_state(&occ), OCC_BUSY);
    CHECK_INT(feed(&occ, 150, 300), 1);
    CHECK_INT(occ_state(&occ), OCC_FREE);

    TEST("histerese: 80 cm (zona morta) sem presenca previa nunca ocupa");
    fresh(&occ);
    CHECK_INT(feed(&occ, 80, 60000), 0);
    CHECK_INT(feed(&occ, 71, 10000), 0);
    CHECK_INT(feed(&occ, 89, 10000), 0);
    CHECK_INT(occ_state(&occ), OCC_FREE);

    TEST("histerese: presenca que segue na zona morta continua valendo");
    fresh(&occ);
    CHECK_INT(feed(&occ, 60, 1000), 0);
    CHECK_INT(feed(&occ, 80, 4300),
              1); /* 1000 + 4300 ms de presenca continua */
    CHECK_INT(occ_state(&occ), OCC_BUSY);

    TEST("histerese: OCUPADA em 80 cm nao libera");
    make_busy(&occ);
    CHECK_INT(feed(&occ, 80, 200000), 0);
    CHECK_INT(occ_state(&occ), OCC_BUSY);

    TEST("limites: 70 cm conta como presenca");
    fresh(&occ);
    CHECK_INT(feed(&occ, 70, 5100), 0);
    CHECK_INT(feed(&occ, 70, 300), 1);

    TEST("limites: 90 cm conta como ausencia");
    make_busy(&occ);
    CHECK_INT(feed(&occ, 90, 90000), 0);
    CHECK_INT(feed(&occ, 90, 300), 1);
    CHECK_INT(occ_state(&occ), OCC_FREE);

    TEST("leitura invalida (-1) conta como ausencia");
    make_busy(&occ);
    CHECK_INT(feed(&occ, -1, 90000), 0);
    CHECK_INT(feed(&occ, -1, 300), 1);
    CHECK_INT(occ_state(&occ), OCC_FREE);
    fresh(&occ);
    CHECK_INT(feed(&occ, -1, 20000), 0); /* invalida nao ocupa */
    CHECK_INT(occ_state(&occ), OCC_FREE);

    TEST("relogio de 32 bits que da a volta");
    fresh(&occ);
    s_now_ms = 0xFFFFFF00u;
    CHECK_INT(feed(&occ, 60, 5100), 0);
    CHECK_INT(feed(&occ, 60, 300), 1);
    CHECK_INT(occ_state(&occ), OCC_BUSY);

    TEST("filter_median3: tira pico isolado");
    filter_init(&filter);
    CHECK_INT(filter_median3(&filter, 60),
              60); /* menos de 3 leituras: a ultima */
    CHECK_INT(filter_median3(&filter, 61), 61);
    CHECK_INT(filter_median3(&filter, 59), 60);  /* mediana de 60, 61, 59 */
    CHECK_INT(filter_median3(&filter, 200), 61); /* 61, 59, 200 -> 61 */
    CHECK_INT(filter_median3(&filter, 60), 60);  /* 59, 200, 60 -> 60 */
    CHECK_INT(filter_median3(&filter, 60), 60);  /* 200, 60, 60 -> 60 */
    CHECK_INT(filter_median3(&filter, 60), 60);

    TEST("filter_median3: leitura invalida isolada");
    filter_init(&filter);
    (void)filter_median3(&filter, 60);
    (void)filter_median3(&filter, 60);
    CHECK_INT(filter_median3(&filter, -1), 60); /* 60, 60, -1 -> 60 */
    CHECK_INT(filter_median3(&filter, 60), 60); /* 60, -1, 60 -> 60 */

    TEST_RESULT();
}
