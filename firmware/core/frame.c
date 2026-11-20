#include "frame.h"

/* TODO (colega): implementar. Os testes estao em test/test_frame.c e test/frames.txt. */

int frame_encode(const frame_t *f, char *out, size_t out_size)
{
    (void)f; (void)out; (void)out_size;
    return -1;
}

int frame_decode(const char *line, frame_t *f)
{
    (void)line; (void)f;
    return FRAME_ERR_FORMAT;
}
