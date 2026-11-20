#ifndef MINITEST_H
#define MINITEST_H
/* Mini-framework de teste: sem dependências, só <stdio.h> e <inttypes.h>. */
#include <inttypes.h>
#include <stdio.h>

static int mt_total = 0;
static int mt_fail = 0;

#define CHECK(cond)                                                            \
    do                                                                         \
    {                                                                          \
        mt_total++;                                                            \
        if (!(cond))                                                           \
        {                                                                      \
            mt_fail++;                                                         \
            printf("  FALHOU %s:%d: %s\n", __FILE__, __LINE__, #cond);         \
        }                                                                      \
    } while (0)

/* Compara dois inteiros. Os casts para int64_t são seguros: int64_t comporta
 * qualquer tipo inteiro usado nos testes, e o valor só é convertido para a
 * comparação e a impressão. */
#define CHECK_INT(got, want)                                                   \
    do                                                                         \
    {                                                                          \
        int64_t mt_got = (int64_t)(got);                                       \
        int64_t mt_want = (int64_t)(want);                                     \
        mt_total++;                                                            \
        if (mt_got != mt_want)                                                 \
        {                                                                      \
            mt_fail++;                                                         \
            printf("  FALHOU %s:%d: %s = %" PRId64 " (esperado %" PRId64       \
                   ")\n",                                                      \
                   __FILE__, __LINE__, #got, mt_got, mt_want);                 \
        }                                                                      \
    } while (0)

#define TEST(name) printf("- %s\n", name)

#define TEST_RESULT()                                                          \
    do                                                                         \
    {                                                                          \
        printf("%s: %d verificacoes, %d falhas\n", __FILE__, mt_total,         \
               mt_fail);                                                       \
        return (mt_fail != 0) ? 1 : 0;                                         \
    } while (0)

#endif
