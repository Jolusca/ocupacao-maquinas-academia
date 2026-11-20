#include <stdlib.h>
#include <string.h>
#include "../core/frame.h"
#include "minitest.h"

static void encode_cases(void)
{
    char buf[FRAME_MAX_LEN];
    frame_t f;

    TEST("frame_encode: casos normais");
    f = (frame_t){2, 1, 17};
    CHECK_INT(frame_encode(&f, buf, sizeof buf), 8);
    CHECK(strcmp(buf, "N02,1,17") == 0);
    f = (frame_t){1, 0, 0};
    CHECK_INT(frame_encode(&f, buf, sizeof buf), 7);
    CHECK(strcmp(buf, "N01,0,0") == 0);
    f = (frame_t){99, 1, 65535};
    CHECK_INT(frame_encode(&f, buf, sizeof buf), 11);
    CHECK(strcmp(buf, "N99,1,65535") == 0);

    TEST("frame_encode: entradas invalidas");
    f = (frame_t){0, 1, 1};
    CHECK_INT(frame_encode(&f, buf, sizeof buf), -1);
    f = (frame_t){100, 1, 1};
    CHECK_INT(frame_encode(&f, buf, sizeof buf), -1);
    f = (frame_t){2, 2, 1};
    CHECK_INT(frame_encode(&f, buf, sizeof buf), -1);

    TEST("frame_encode: buffer pequeno");
    f = (frame_t){2, 1, 17};
    CHECK_INT(frame_encode(&f, buf, 8), -1);  /* falta espaco para o '\0' */
    CHECK_INT(frame_encode(&f, buf, 9), 8);
}

static void unescape(const char *in, char *out)
{
    while (*in) {
        if (in[0] == '\\' && in[1] == 'n') { *out++ = '\n'; in += 2; }
        else if (in[0] == '\\' && in[1] == 'r') { *out++ = '\r'; in += 2; }
        else *out++ = *in++;
    }
    *out = '\0';
}

static void vector_cases(const char *path)
{
    FILE *fp = fopen(path, "r");
    char line[256];
    int n = 0;

    TEST("vetores de test/frames.txt");
    CHECK(fp != NULL);
    if (!fp) return;
    while (fgets(line, sizeof line, fp)) {
        char *kind, *text, *node, *state, *seq, *save = NULL;
        char raw[256], decoded[256];
        frame_t f = {200, 200, 65000};  /* valores sentinela: erro nao pode altera-los */

        line[strcspn(line, "\r\n")] = '\0';
        if (line[0] == '#' || line[0] == '\0') continue;
        /* separa por '|' preservando campos vazios */
        kind = line;
        text = strchr(kind, '|');  if (!text) continue;  *text++ = '\0';
        node = strchr(text, '|');  if (!node) continue;  *node++ = '\0';
        state = strchr(node, '|'); if (!state) continue; *state++ = '\0';
        seq = strchr(state, '|');  if (!seq) continue;   *seq++ = '\0';
        (void)save;
        strcpy(raw, text);
        unescape(raw, decoded);
        n++;

        if (strcmp(kind, "OK") == 0) {
            CHECK_INT(frame_decode(decoded, &f), FRAME_OK);
            CHECK_INT(f.node, atoi(node));
            CHECK_INT(f.state, atoi(state));
            CHECK_INT(f.seq, atoi(seq));
        } else {
            int want = strcmp(kind, "FMT") == 0 ? FRAME_ERR_FORMAT : FRAME_ERR_RANGE;
            int got = frame_decode(decoded, &f);
            if (got != want) printf("  vetor: [%s] tipo %s\n", raw, kind);
            CHECK_INT(got, want);
            CHECK(f.node == 200 && f.state == 200 && f.seq == 65000);  /* nao altera f em caso de erro */
        }
    }
    fclose(fp);
    CHECK(n >= 20);
}

static void roundtrip(void)
{
    char buf[FRAME_MAX_LEN];
    TEST("ida e volta: encode seguido de decode");
    for (int node = 1; node <= 99; node += 7)
        for (int st = 0; st <= 1; st++)
            for (long seq = 0; seq <= 65535; seq += 4369) {
                frame_t a = {(uint8_t)node, (uint8_t)st, (uint16_t)seq}, b = {0, 0, 0};
                CHECK(frame_encode(&a, buf, sizeof buf) > 0);
                CHECK_INT(frame_decode(buf, &b), FRAME_OK);
                CHECK(a.node == b.node && a.state == b.state && a.seq == b.seq);
            }
}

int main(int argc, char **argv)
{
    encode_cases();
    vector_cases(argc > 1 ? argv[1] : "test/frames.txt");
    roundtrip();
    TEST_RESULT();
}
