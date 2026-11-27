#include "../core/link.h"
#include "minitest.h"
#include <string.h>

static const uint8_t MAC_A[6] = {0x10, 0x51, 0xDB, 0x1C, 0x51, 0x80};
static const uint8_t MAC_B[6] = {0x10, 0x51, 0xDB, 0x1C, 0x61, 0x64};

int main(void)
{
    role_state_t r;
    sink_link_t s;

    TEST("papel automatico: ao ligar com o notebook ja na USB, comeca coletor");
    role_init(&r, ROLE_MODE_AUTO, true);
    CHECK_INT(r.role, ROLE_SINK);

    TEST("papel automatico: ao ligar sem notebook (fonte), comeca sensor");
    role_init(&r, ROLE_MODE_AUTO, false);
    CHECK_INT(r.role, ROLE_SENSOR);

    TEST("sensor vira coletor so depois de 2 s com o notebook presente");
    CHECK_INT(role_update(&r, 1000, true), ROLE_SENSOR);
    CHECK_INT(role_update(&r, 2999, true), ROLE_SENSOR);
    CHECK_INT(role_update(&r, 3000, true), ROLE_SINK);

    TEST("oscilacao curta da USB nao tira o papel de coletor (histerese de 10 s)");
    CHECK_INT(role_update(&r, 4000, false), ROLE_SINK);
    CHECK_INT(role_update(&r, 9000, false), ROLE_SINK);
    CHECK_INT(role_update(&r, 9500, true), ROLE_SINK); /* voltou: o relogio zera */
    CHECK_INT(role_update(&r, 12000, false), ROLE_SINK);
    CHECK_INT(role_update(&r, 21999, false), ROLE_SINK);
    CHECK_INT(role_update(&r, 22000, false), ROLE_SENSOR);

    TEST("oscilacao curta tambem nao faz um sensor virar coletor");
    role_init(&r, ROLE_MODE_AUTO, false);
    CHECK_INT(role_update(&r, 100, true), ROLE_SENSOR);
    CHECK_INT(role_update(&r, 1500, false), ROLE_SENSOR); /* sumiu antes de 2 s */
    CHECK_INT(role_update(&r, 2500, true), ROLE_SENSOR);  /* contagem recomecou */
    CHECK_INT(role_update(&r, 4400, true), ROLE_SENSOR);
    CHECK_INT(role_update(&r, 4500, true), ROLE_SINK);

    TEST("relogio de 32 bits que da a volta nao quebra a histerese");
    role_init(&r, ROLE_MODE_AUTO, false);
    CHECK_INT(role_update(&r, 0xFFFFFF00u, true), ROLE_SENSOR);
    CHECK_INT(role_update(&r, 0xFFFFFF00u + 2000u, true), ROLE_SINK);

    TEST("papel forcado ignora a USB");
    role_init(&r, ROLE_MODE_SINK, false);
    CHECK_INT(r.role, ROLE_SINK);
    CHECK_INT(role_update(&r, 100000, false), ROLE_SINK);
    role_init(&r, ROLE_MODE_SENSOR, true);
    CHECK_INT(r.role, ROLE_SENSOR);
    CHECK_INT(role_update(&r, 100000, true), ROLE_SENSOR);

    TEST("trocar o modo em funcionamento vale na hora");
    role_init(&r, ROLE_MODE_AUTO, false);
    role_set_mode(&r, ROLE_MODE_SINK, false);
    CHECK_INT(r.role, ROLE_SINK);
    role_set_mode(&r, ROLE_MODE_AUTO, false);
    CHECK_INT(role_update(&r, 0, false), ROLE_SINK); /* sai pela histerese, nao de supetao */
    CHECK_INT(role_update(&r, 10000, false), ROLE_SENSOR);

    TEST("sem aviso de coletor, o sensor nao conhece ninguem");
    sink_init(&s);
    CHECK(!sink_known(&s, 0));

    TEST("o primeiro aviso apresenta o coletor");
    CHECK(sink_on_beacon(&s, MAC_A, 1000));
    CHECK(sink_known(&s, 1000));
    CHECK(memcmp(sink_mac(&s), MAC_A, 6) == 0);

    TEST("aviso repetido do mesmo coletor nao conta como troca");
    CHECK(!sink_on_beacon(&s, MAC_A, 6000));

    TEST("o coletor e esquecido depois de 20 s sem aviso");
    CHECK(sink_known(&s, 6000 + 20000));
    CHECK(!sink_known(&s, 6000 + 20001));

    TEST("outro coletor assume: o novo MAC passa a valer");
    CHECK(sink_on_beacon(&s, MAC_A, 30000));
    CHECK(sink_on_beacon(&s, MAC_B, 31000));
    CHECK(memcmp(sink_mac(&s), MAC_B, 6) == 0);

    TEST("duas entregas seguidas sem confirmacao fazem esquecer o coletor");
    sink_init(&s);
    sink_on_beacon(&s, MAC_A, 0);
    sink_on_delivery(&s, false);
    CHECK(sink_known(&s, 100));
    sink_on_delivery(&s, false);
    CHECK(!sink_known(&s, 200));

    TEST("uma entrega boa zera a contagem de falhas");
    sink_init(&s);
    sink_on_beacon(&s, MAC_A, 0);
    sink_on_delivery(&s, false);
    sink_on_delivery(&s, true);
    sink_on_delivery(&s, false);
    CHECK(sink_known(&s, 100));

    TEST("depois de esquecer, o proximo aviso volta a apresentar o coletor");
    sink_init(&s);
    sink_on_beacon(&s, MAC_A, 0);
    sink_on_delivery(&s, false);
    sink_on_delivery(&s, false);
    CHECK(sink_on_beacon(&s, MAC_A, 5000));
    CHECK(sink_known(&s, 5000));

    TEST("o coletor manda um aviso a cada 5 s");
    CHECK(link_beacon_due(false, 0, 0));        /* ainda nao mandou nenhum */
    CHECK(!link_beacon_due(true, 1000, 5999));
    CHECK(link_beacon_due(true, 1000, 6000));
    CHECK(link_beacon_due(true, 0xFFFFFF00u, 0xFFFFFF00u + 5000u));

    TEST_RESULT();
}
