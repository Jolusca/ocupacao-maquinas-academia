#include "../core/scheduler.h"
#include "minitest.h"

int main(void)
{
    tx_sched_t sched;
    uint16_t last_seq = 0;
    uint32_t count;

    TEST("primeiro envio e devido, mesmo sem mudanca");
    sched_init(&sched);
    CHECK(sched_due(&sched, 0, false));
    CHECK_INT(sched_next_seq(&sched, 0), 0);

    TEST("sinal de vida: devido so a partir de 15 s");
    CHECK(!sched_due(&sched, 1, false));
    CHECK(!sched_due(&sched, 14999, false));
    CHECK(sched_due(&sched, 15000, false));

    TEST("mudanca de estado envia na hora");
    CHECK(sched_due(&sched, 100, true));

    TEST("seq cresce de 1 em 1 e o relogio de 15 s recomeca no envio");
    CHECK_INT(sched_next_seq(&sched, 15000), 1);
    CHECK(!sched_due(&sched, 29999, false));
    CHECK(sched_due(&sched, 30000, false));
    CHECK_INT(sched_next_seq(&sched, 20000), 2); /* envio por mudanca em 20 s */
    CHECK(!sched_due(&sched, 34999, false)); /* proximo sinal de vida em 35 s */
    CHECK(sched_due(&sched, 35000, false));

    TEST("seq volta a 0 depois de 65535");
    sched_init(&sched);
    for (count = 0; count < 65536u; count++)
    {
        last_seq = sched_next_seq(&sched, count);
    }
    CHECK_INT(last_seq, 65535);
    CHECK_INT(sched_next_seq(&sched, 70000), 0);
    CHECK_INT(sched_next_seq(&sched, 70001), 1);

    TEST("relogio de 32 bits que da a volta");
    sched_init(&sched);
    (void)sched_next_seq(&sched, 0xFFFFFF00u);
    CHECK(!sched_due(&sched, 0xFFFFFF00u + 14000u, false));
    CHECK(sched_due(&sched, 0xFFFFFF00u + 15000u, false)); /* passa por 0 */
    CHECK(sched_due(&sched, 14744u, false)); /* 0xFFFFFF00 + 15000 mod 2^32 */

    TEST_RESULT();
}
