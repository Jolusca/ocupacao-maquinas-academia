#include "../core/scheduler.h"
#include "minitest.h"

int main(void)
{
    tx_sched_t s;

    TEST("primeiro envio e devido, mesmo sem mudanca");
    sched_init(&s);
    CHECK(sched_due(&s, 0, false));
    CHECK_INT(sched_next_seq(&s, 0), 0);

    TEST("sinal de vida: devido so a partir de 15 s");
    CHECK(!sched_due(&s, 1, false));
    CHECK(!sched_due(&s, 14999, false));
    CHECK(sched_due(&s, 15000, false));

    TEST("mudanca de estado envia na hora");
    CHECK(sched_due(&s, 100, true));

    TEST("seq cresce de 1 em 1 e o relogio de 15 s recomeca no envio");
    CHECK_INT(sched_next_seq(&s, 15000), 1);
    CHECK(!sched_due(&s, 29999, false));
    CHECK(sched_due(&s, 30000, false));
    CHECK_INT(sched_next_seq(&s, 20000), 2);   /* envio por mudanca em 20 s */
    CHECK(!sched_due(&s, 34999, false));       /* proximo sinal de vida so em 35 s */
    CHECK(sched_due(&s, 35000, false));

    TEST("seq volta a 0 depois de 65535");
    sched_init(&s);
    uint16_t last = 0;
    for (long i = 0; i < 65536; i++) last = sched_next_seq(&s, (uint32_t)i);
    CHECK_INT(last, 65535);
    CHECK_INT(sched_next_seq(&s, 70000), 0);
    CHECK_INT(sched_next_seq(&s, 70001), 1);

    TEST("relogio de 32 bits que da a volta");
    sched_init(&s);
    (void)sched_next_seq(&s, 0xFFFFFF00u);
    CHECK(!sched_due(&s, 0xFFFFFF00u + 14000u, false));
    CHECK(sched_due(&s, 0xFFFFFF00u + 15000u, false));   /* passa por 0 */
    CHECK(sched_due(&s, 14744u, false));                 /* 0xFFFFFF00 + 15000 mod 2^32 */

    TEST_RESULT();
}
