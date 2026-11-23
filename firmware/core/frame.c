#include "frame.h"

#include <stdio.h>
#include <string.h>

static int is_digit(char c)
{
    return c >= '0' && c <= '9';
}

static uint32_t read_number(const char **cursor)
{
    uint32_t value = 0;

    while (is_digit(**cursor)) {
        // Continua validando os digitos apos exceder a faixa do quadro.
        if (value <= UINT16_MAX) {
            value = value * 10u + (unsigned)(**cursor - '0');
        }
        ++*cursor;
    }

    return value;
}

int frame_encode(const frame_t *f, char *out, size_t out_size)
{
    char encoded[FRAME_MAX_LEN];

    if (f->node < 1 || f->node > 99 || f->state > 1) {
        return -1;
    }

    int length = snprintf(encoded, sizeof encoded, "N%02u,%u,%u",
                          (unsigned)f->node, (unsigned)f->state,
                          (unsigned)f->seq);
    if (length < 0 || (size_t)length >= sizeof encoded ||
        (size_t)length >= out_size) {
        return -1;
    }

    memcpy(out, encoded, (size_t)length + 1);
    return length;
}

int frame_decode(const char *line, frame_t *f)
{
    if (line[0] != 'N' || !is_digit(line[1]) || !is_digit(line[2]) ||
        line[3] != ',') {
        return FRAME_ERR_FORMAT;
    }

    unsigned node = (unsigned)(line[1] - '0') * 10u + (unsigned)(line[2] - '0');
    const char *cursor = line + 4;
    if (!is_digit(*cursor)) {
        return FRAME_ERR_FORMAT;
    }
    uint32_t state = read_number(&cursor);
    if (*cursor != ',' || !is_digit(cursor[1])) {
        return FRAME_ERR_FORMAT;
    }
    ++cursor;
    uint32_t seq = read_number(&cursor);

    if (*cursor == '\r' && cursor[1] == '\n') {
        ++cursor;
    }
    if (*cursor == '\n') {
        ++cursor;
    }
    if (*cursor != '\0') {
        return FRAME_ERR_FORMAT;
    }

    if (node == 0 || state > 1 || seq > UINT16_MAX) {
        return FRAME_ERR_RANGE;
    }

    *f = (frame_t){ .node = (uint8_t)node, .state = (uint8_t)state,
                    .seq = (uint16_t)seq };
    return FRAME_OK;
}
