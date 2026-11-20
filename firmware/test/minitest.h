#ifndef MINITEST_H
#define MINITEST_H
/* Mini-framework de teste: sem dependências, só <stdio.h>. */
#include <stdio.h>

static int mt_total = 0;
static int mt_fail  = 0;

#define CHECK(cond) do { mt_total++; if (!(cond)) { mt_fail++; \
    printf("  FALHOU %s:%d: %s\n", __FILE__, __LINE__, #cond); } } while (0)

#define CHECK_INT(got, want) do { mt_total++; long mt_g = (long)(got), mt_w = (long)(want); \
    if (mt_g != mt_w) { mt_fail++; \
    printf("  FALHOU %s:%d: %s = %ld (esperado %ld)\n", __FILE__, __LINE__, #got, mt_g, mt_w); } } while (0)

#define TEST(name) printf("- %s\n", name)

#define TEST_RESULT() do { printf("%s: %d verificacoes, %d falhas\n", __FILE__, mt_total, mt_fail); \
    return mt_fail ? 1 : 0; } while (0)

#endif
