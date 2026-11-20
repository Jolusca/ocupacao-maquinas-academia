#include "../core/occupancy.h"
#include "minitest.h"

/* Alimenta a maquina com a mesma distancia a cada 100 ms durante dur_ms.
 * Devolve quantas vezes o estado mudou. `now` e global para encadear cenarios. */
static uint32_t now = 1000;

static int feed(occ_t *o, int16_t dist_cm, uint32_t dur_ms)
{
    int changes = 0;
    for (uint32_t t = 0; t < dur_ms; t += 100) {
        if (occ_update(o, now, dist_cm)) changes++;
        now += 100;
    }
    return changes;
}

static void fresh(occ_t *o)
{
    const occ_cfg_t cfg = OCC_CFG_DEFAULT;
    occ_init(o, &cfg);
    now = 1000;
}

static void make_busy(occ_t *o)
{
    fresh(o);
    CHECK_INT(feed(o, 60, 5100), 0);
    CHECK_INT(feed(o, 60, 300), 1);
    CHECK_INT(occ_state(o), OCC_BUSY);
}

int main(void)
{
    occ_t o;
    filter_t f;

    TEST("estado inicial e LIVRE");
    fresh(&o);
    CHECK_INT(occ_state(&o), OCC_FREE);

    TEST("passante: 2 s a 60 cm e vai embora -> continua LIVRE");
    fresh(&o);
    CHECK_INT(feed(&o, 60, 2000), 0);
    CHECK_INT(feed(&o, 150, 10000), 0);
    CHECK_INT(occ_state(&o), OCC_FREE);

    TEST("treino: presenca por mais de 5 s -> OCUPADA (uma unica mudanca)");
    fresh(&o);
    CHECK_INT(feed(&o, 60, 5100), 0);              /* ate 5000 ms: ainda LIVRE */
    CHECK_INT(occ_state(&o), OCC_FREE);
    CHECK_INT(feed(&o, 60, 300), 1);               /* passou de 5000 ms */
    CHECK_INT(occ_state(&o), OCC_BUSY);
    CHECK_INT(feed(&o, 60, 20000), 0);             /* nao muda de novo */

    TEST("descanso: ausencia curta (60 s) -> continua OCUPADA");
    make_busy(&o);
    CHECK_INT(feed(&o, 150, 60000), 0);
    CHECK_INT(occ_state(&o), OCC_BUSY);

    TEST("descanso: a ausencia precisa ser CONTINUA (volta a 60 cm zera o cronometro)");
    make_busy(&o);
    CHECK_INT(feed(&o, 150, 60000), 0);
    CHECK_INT(feed(&o, 60, 1000), 0);
    CHECK_INT(feed(&o, 150, 60000), 0);            /* 120 s no total, mas nunca 90 s seguidos */
    CHECK_INT(occ_state(&o), OCC_BUSY);

    TEST("liberacao: ausencia por mais de 90 s -> LIVRE");
    make_busy(&o);
    CHECK_INT(feed(&o, 150, 90000), 0);            /* ate 90000 ms: ainda OCUPADA */
    CHECK_INT(occ_state(&o), OCC_BUSY);
    CHECK_INT(feed(&o, 150, 300), 1);
    CHECK_INT(occ_state(&o), OCC_FREE);

    TEST("histerese: 80 cm (zona morta) sem presenca previa nunca ocupa");
    fresh(&o);
    CHECK_INT(feed(&o, 80, 60000), 0);
    CHECK_INT(feed(&o, 71, 10000), 0);
    CHECK_INT(feed(&o, 89, 10000), 0);
    CHECK_INT(occ_state(&o), OCC_FREE);

    TEST("histerese: presenca que segue na zona morta continua valendo");
    fresh(&o);
    CHECK_INT(feed(&o, 60, 1000), 0);
    CHECK_INT(feed(&o, 80, 4300), 1);              /* 1000 + 4300 ms de presenca continua */
    CHECK_INT(occ_state(&o), OCC_BUSY);

    TEST("histerese: OCUPADA em 80 cm nao libera");
    make_busy(&o);
    CHECK_INT(feed(&o, 80, 200000), 0);
    CHECK_INT(occ_state(&o), OCC_BUSY);

    TEST("limites: 70 cm conta como presenca");
    fresh(&o);
    CHECK_INT(feed(&o, 70, 5100), 0);
    CHECK_INT(feed(&o, 70, 300), 1);

    TEST("limites: 90 cm conta como ausencia");
    make_busy(&o);
    CHECK_INT(feed(&o, 90, 90000), 0);
    CHECK_INT(feed(&o, 90, 300), 1);
    CHECK_INT(occ_state(&o), OCC_FREE);

    TEST("leitura invalida (-1) conta como ausencia");
    make_busy(&o);
    CHECK_INT(feed(&o, -1, 90000), 0);
    CHECK_INT(feed(&o, -1, 300), 1);
    CHECK_INT(occ_state(&o), OCC_FREE);
    fresh(&o);
    CHECK_INT(feed(&o, -1, 20000), 0);             /* invalida nao ocupa */
    CHECK_INT(occ_state(&o), OCC_FREE);

    TEST("relogio de 32 bits que da a volta");
    fresh(&o);
    now = 0xFFFFFF00u;
    CHECK_INT(feed(&o, 60, 5100), 0);
    CHECK_INT(feed(&o, 60, 300), 1);
    CHECK_INT(occ_state(&o), OCC_BUSY);

    TEST("filter_median3: tira pico isolado");
    filter_init(&f);
    CHECK_INT(filter_median3(&f, 60), 60);          /* com menos de 3 leituras devolve a ultima */
    CHECK_INT(filter_median3(&f, 61), 61);
    CHECK_INT(filter_median3(&f, 59), 60);          /* mediana de 60, 61, 59 */
    CHECK_INT(filter_median3(&f, 200), 61);         /* 61, 59, 200 -> 61 */
    CHECK_INT(filter_median3(&f, 60), 60);          /* 59, 200, 60 -> 60 */
    CHECK_INT(filter_median3(&f, 60), 60);          /* 200, 60, 60 -> 60 */
    CHECK_INT(filter_median3(&f, 60), 60);

    TEST("filter_median3: leitura invalida isolada");
    filter_init(&f);
    (void)filter_median3(&f, 60);
    (void)filter_median3(&f, 60);
    CHECK_INT(filter_median3(&f, -1), 60);          /* 60, 60, -1 -> 60 */
    CHECK_INT(filter_median3(&f, 60), 60);          /* 60, -1, 60 -> 60 */

    TEST_RESULT();
}
