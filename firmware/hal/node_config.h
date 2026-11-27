#ifndef NODE_CONFIG_H
#define NODE_CONFIG_H
/* Configuração do nó guardada na flash (NVS), que sobrevive a desligar e a
 * regravar o programa: o número do nó e o modo do papel. Assim uma placa
 * reserva assume o lugar de outra por um comando na serial, sem editar o
 * código. */
#include <stdint.h>

#ifdef __cplusplus
extern "C"
{
#endif
#include "link.h"
#ifdef __cplusplus
}
#endif

/* Número do nó gravado, ou 0 se nada foi gravado. */
uint8_t node_cfg_id();
/* Modo do papel gravado (padrão: automático). */
role_mode_t node_cfg_mode();

void node_cfg_save_id(uint8_t id);
void node_cfg_save_mode(role_mode_t mode);
/* Apaga tudo o que foi gravado: volta ao padrão. */
void node_cfg_clear();

#endif
