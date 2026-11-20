#include <stdlib.h>
#include <string.h>
#include "../core/frame.h"
#include "minitest.h"

static void encode_cases(void)
{
    char text[FRAME_MAX_LEN];
    frame_t frame;

    TEST("frame_encode: casos normais");
    frame = (frame_t){ 2, 1, 17 };
    CHECK_INT(frame_encode(&frame, text, sizeof(text)), 8);
    CHECK(strcmp(text, "N02,1,17") == 0);
    frame = (frame_t){ 1, 0, 0 };
    CHECK_INT(frame_encode(&frame, text, sizeof(text)), 7);
    CHECK(strcmp(text, "N01,0,0") == 0);
    frame = (frame_t){ 99, 1, 65535 };
    CHECK_INT(frame_encode(&frame, text, sizeof(text)), 11);
    CHECK(strcmp(text, "N99,1,65535") == 0);

    TEST("frame_encode: entradas invalidas");
    frame = (frame_t){ 0, 1, 1 };
    CHECK_INT(frame_encode(&frame, text, sizeof(text)), -1);
    frame = (frame_t){ 100, 1, 1 };
    CHECK_INT(frame_encode(&frame, text, sizeof(text)), -1);
    frame = (frame_t){ 2, 2, 1 };
    CHECK_INT(frame_encode(&frame, text, sizeof(text)), -1);

    TEST("frame_encode: buffer pequeno");
    frame = (frame_t){ 2, 1, 17 };
    CHECK_INT(frame_encode(&frame, text, 8), -1); /* falta espaco para o '\0' */
    CHECK_INT(frame_encode(&frame, text, 9), 8);
}

/* Troca as sequências "\n" e "\r" escritas no arquivo de vetores pelos
 * caracteres de controle de verdade. */
static void unescape(const char *src, char *dst)
{
    while (*src != '\0')
    {
        if ((src[0] == '\\') && (src[1] == 'n'))
        {
            *dst++ = '\n';
            src += 2;
        }
        else if ((src[0] == '\\') && (src[1] == 'r'))
        {
            *dst++ = '\r';
            src += 2;
        }
        else
        {
            *dst++ = *src++;
        }
    }
    *dst = '\0';
}

/* Devolve o próximo campo de uma linha separada por '|' e avança o cursor. */
static char *take_field(char **cursor)
{
    char *field = *cursor;
    char *sep = strchr(field, '|');

    if (sep != NULL)
    {
        *sep = '\0';
        *cursor = sep + 1;
    }
    else
    {
        *cursor = field + strlen(field);
    }
    return field;
}

static void vector_cases(const char *path)
{
    FILE *vec_file = fopen(path, "r");
    char line[256];
    char raw[256];
    char decoded[256];
    int count = 0;

    TEST("vetores de test/frames.txt");
    CHECK(vec_file != NULL);
    if (vec_file == NULL)
    {
        return;
    }
    while (fgets(line, sizeof(line), vec_file) != NULL)
    {
        char *cursor = line;
        char *kind;
        char *text;
        char *node_str;
        char *state_str;
        char *seq_str;
        /* valores sentinela: um erro de decodificação não pode alterá-los */
        frame_t frame = { 200, 200, 65000 };

        line[strcspn(line, "\r\n")] = '\0';
        if ((line[0] == '#') || (line[0] == '\0'))
        {
            continue;
        }
        kind = take_field(&cursor);
        text = take_field(&cursor);
        node_str = take_field(&cursor);
        state_str = take_field(&cursor);
        seq_str = take_field(&cursor);
        snprintf(raw, sizeof(raw), "%s", text);
        unescape(raw, decoded);
        count++;

        if (strcmp(kind, "OK") == 0)
        {
            CHECK_INT(frame_decode(decoded, &frame), FRAME_OK);
            CHECK_INT(frame.node, atoi(node_str));
            CHECK_INT(frame.state, atoi(state_str));
            CHECK_INT(frame.seq, atoi(seq_str));
        }
        else
        {
            int want =
                (strcmp(kind, "FMT") == 0) ? FRAME_ERR_FORMAT : FRAME_ERR_RANGE;
            int got = frame_decode(decoded, &frame);

            if (got != want)
            {
                printf("  vetor: [%s] tipo %s\n", raw, kind);
            }
            CHECK_INT(got, want);
            /* em caso de erro, frame não pode ter sido alterado */
            CHECK((frame.node == 200) && (frame.state == 200) &&
                  (frame.seq == 65000));
        }
    }
    fclose(vec_file);
    CHECK(count >= 20);
}

static void roundtrip(void)
{
    char text[FRAME_MAX_LEN];
    uint32_t node;
    uint32_t state;
    uint32_t seq;

    TEST("ida e volta: encode seguido de decode");
    for (node = 1; node <= 99; node += 7)
    {
        for (state = 0; state <= 1; state++)
        {
            for (seq = 0; seq <= 65535; seq += 4369)
            {
                frame_t original;
                frame_t decoded = { 0, 0, 0 };

                /* Casts: node (1..99), state (0..1) e seq (0..65535) cabem nos
                 * campos de 8 e 16 bits. */
                original.node = (uint8_t)node;
                original.state = (uint8_t)state;
                original.seq = (uint16_t)seq;
                CHECK(frame_encode(&original, text, sizeof(text)) > 0);
                CHECK_INT(frame_decode(text, &decoded), FRAME_OK);
                CHECK((original.node == decoded.node) &&
                      (original.state == decoded.state) &&
                      (original.seq == decoded.seq));
            }
        }
    }
}

int main(int argc, char **argv)
{
    encode_cases();
    vector_cases((argc > 1) ? argv[1] : "test/frames.txt");
    roundtrip();
    TEST_RESULT();
}
