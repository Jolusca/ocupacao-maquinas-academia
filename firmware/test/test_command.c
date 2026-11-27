#include "../core/command.h"
#include "minitest.h"

int main(void)
{
    cmd_t c;

    TEST("id: define o numero do no");
    CHECK_INT(cmd_parse("id 3", &c), CMD_OK);
    CHECK_INT(c.kind, CMD_ID);
    CHECK_INT(c.id, 3);

    TEST("id: aceita 1 a 99 e recusa o resto");
    CHECK_INT(cmd_parse("id 1", &c), CMD_OK);
    CHECK_INT(cmd_parse("id 99", &c), CMD_OK);
    CHECK_INT(c.id, 99);
    CHECK_INT(cmd_parse("id 0", &c), CMD_ERR_ARG);
    CHECK_INT(cmd_parse("id 100", &c), CMD_ERR_ARG);
    CHECK_INT(cmd_parse("id -1", &c), CMD_ERR_ARG);
    CHECK_INT(cmd_parse("id abc", &c), CMD_ERR_ARG);
    CHECK_INT(cmd_parse("id", &c), CMD_ERR_ARG);
    CHECK_INT(cmd_parse("id 2 3", &c), CMD_ERR_ARG);
    CHECK_INT(cmd_parse("id 99999999999999999999", &c), CMD_ERR_ARG);

    TEST("papel: auto, coletor e sensor");
    CHECK_INT(cmd_parse("papel auto", &c), CMD_OK);
    CHECK_INT(c.kind, CMD_ROLE);
    CHECK_INT(c.mode, ROLE_MODE_AUTO);
    CHECK_INT(cmd_parse("papel coletor", &c), CMD_OK);
    CHECK_INT(c.mode, ROLE_MODE_SINK);
    CHECK_INT(cmd_parse("papel sensor", &c), CMD_OK);
    CHECK_INT(c.mode, ROLE_MODE_SENSOR);
    CHECK_INT(cmd_parse("papel gateway", &c), CMD_ERR_ARG);
    CHECK_INT(cmd_parse("papel", &c), CMD_ERR_ARG);

    TEST("info e limpar");
    CHECK_INT(cmd_parse("info", &c), CMD_OK);
    CHECK_INT(c.kind, CMD_INFO);
    CHECK_INT(cmd_parse("limpar", &c), CMD_OK);
    CHECK_INT(c.kind, CMD_CLEAR);
    CHECK_INT(cmd_parse("info agora", &c), CMD_ERR_ARG);

    TEST("espacos e fim de linha (\\r\\n) nao atrapalham");
    CHECK_INT(cmd_parse("  id   7  \r\n", &c), CMD_OK);
    CHECK_INT(c.id, 7);
    CHECK_INT(cmd_parse("papel   sensor\n", &c), CMD_OK);

    TEST("linha vazia e comando desconhecido");
    CHECK_INT(cmd_parse("", &c), CMD_ERR_EMPTY);
    CHECK_INT(cmd_parse("   \r\n", &c), CMD_ERR_EMPTY);
    CHECK_INT(cmd_parse("reiniciar", &c), CMD_ERR_UNKNOWN);
    CHECK_INT(cmd_parse("ID 3", &c), CMD_ERR_UNKNOWN); /* so minusculas: um jeito so */

    TEST("quadro do servidor nao e comando (linhas de quadro e log passam batido)");
    CHECK_INT(cmd_parse("N02,1,17", &c), CMD_ERR_UNKNOWN);
    CHECK_INT(cmd_parse("# log", &c), CMD_ERR_UNKNOWN);

    TEST("comando que falha nao altera a estrutura");
    c.kind = CMD_INFO; c.id = 42;
    CHECK_INT(cmd_parse("id 0", &c), CMD_ERR_ARG);
    CHECK_INT(c.kind, CMD_INFO);
    CHECK_INT(c.id, 42);

    TEST_RESULT();
}
