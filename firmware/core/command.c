#include "command.h"
#include <stddef.h>
#include <string.h>

#define CMD_MAX_WORDS 3

/* Separa a linha em palavras (copia em `buf`). Devolve quantas achou, ou -1 se tem palavras
 * demais ou a linha e longa demais. */
static int split_words(const char *line, char *buf, size_t buf_size, const char **words)
{
    size_t n = 0;
    int    count = 0;
    int    in_word = 0;
    size_t i;

    for (i = 0; line[i] != '\0'; i++) {
        char c = line[i];
        if (c == ' ' || c == '\t' || c == '\r' || c == '\n') {
            if (in_word) {
                if (n + 1 >= buf_size) {
                    return -1;
                }
                buf[n++] = '\0';
                in_word  = 0;
            }
            continue;
        }
        if (!in_word) {
            if (count >= CMD_MAX_WORDS + 1) {
                return -1;
            }
            words[count++] = &buf[n];
            in_word        = 1;
        }
        if (n + 1 >= buf_size) {
            return -1;
        }
        buf[n++] = c;
    }
    if (in_word) {
        buf[n] = '\0';
    }
    return count;
}

/* Inteiro de 1 a 99. true e preenche *out, ou false. */
static int parse_id(const char *s, uint8_t *out)
{
    unsigned v = 0;
    size_t   i;

    if (s[0] == '\0' || strlen(s) > 2) {
        return 0;
    }
    for (i = 0; s[i] != '\0'; i++) {
        if (s[i] < '0' || s[i] > '9') {
            return 0;
        }
        v = v * 10u + (unsigned)(s[i] - '0');
    }
    if (v < 1u || v > 99u) {
        return 0;
    }
    *out = (uint8_t)v;
    return 1;
}

int cmd_parse(const char *line, cmd_t *out)
{
    char        buf[64];
    const char *w[CMD_MAX_WORDS + 1];
    int         n = split_words(line, buf, sizeof(buf), w);
    cmd_t       c = {CMD_NONE, 0, ROLE_MODE_AUTO};

    if (n < 0) {
        return CMD_ERR_UNKNOWN;
    }
    if (n == 0) {
        return CMD_ERR_EMPTY;
    }

    if (strcmp(w[0], "id") == 0) {
        if (n != 2 || !parse_id(w[1], &c.id)) {
            return CMD_ERR_ARG;
        }
        c.kind = CMD_ID;
    } else if (strcmp(w[0], "papel") == 0) {
        if (n != 2) {
            return CMD_ERR_ARG;
        }
        if (strcmp(w[1], "auto") == 0) {
            c.mode = ROLE_MODE_AUTO;
        } else if (strcmp(w[1], "coletor") == 0) {
            c.mode = ROLE_MODE_SINK;
        } else if (strcmp(w[1], "sensor") == 0) {
            c.mode = ROLE_MODE_SENSOR;
        } else {
            return CMD_ERR_ARG;
        }
        c.kind = CMD_ROLE;
    } else if (strcmp(w[0], "info") == 0) {
        if (n != 1) {
            return CMD_ERR_ARG;
        }
        c.kind = CMD_INFO;
    } else if (strcmp(w[0], "limpar") == 0) {
        if (n != 1) {
            return CMD_ERR_ARG;
        }
        c.kind = CMD_CLEAR;
    } else {
        return CMD_ERR_UNKNOWN;
    }
    *out = c;
    return CMD_OK;
}
