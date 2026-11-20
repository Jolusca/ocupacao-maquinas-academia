#ifndef OCCUPANCY_H
#define OCCUPANCY_H
/* Maquina de estados do no: decide livre/ocupada a partir da distancia (cm).
 * Codigo C puro: o tempo entra como argumento (now_ms), nunca le relogio nem pino.
 *
 * Regras (ver Plano de Firmware, decisoes D2 e D3):
 *  - presenca: distancia <= arrive_cm (70). ausencia: distancia >= leave_cm (90) ou leitura invalida (< 0).
 *  - entre 70 e 90 cm (zona morta) MANTEM a condicao anterior (histerese): nao zera nem reinicia o cronometro.
 *  - LIVRE -> OCUPADA: presenca continua por MAIS de presence_ms (5000 ms).
 *  - OCUPADA -> LIVRE: ausencia continua por MAIS de absence_ms (90000 ms).
 *  - se a condicao contraria se interrompe antes do tempo, o cronometro volta a zero.
 *  - estado inicial: LIVRE. */
#include <stdbool.h>
#include <stdint.h>

typedef enum { OCC_FREE = 0, OCC_BUSY = 1 } occ_state_t;

typedef struct {
    int16_t  arrive_cm;   /* 70 */
    int16_t  leave_cm;    /* 90 */
    uint32_t presence_ms; /* 5000 */
    uint32_t absence_ms;  /* 90000 */
} occ_cfg_t;

#define OCC_CFG_DEFAULT { 70, 90, 5000u, 90000u }

typedef struct {
    occ_cfg_t   cfg;
    occ_state_t state;
    bool        present;  /* condicao atual (com histerese) */
    bool        timing;   /* ha cronometro correndo? */
    uint32_t    since_ms; /* instante em que a condicao contraria ao estado comecou */
} occ_t;                  /* campos internos: o colega pode ajustar, os testes usam so a API */

void        occ_init(occ_t *o, const occ_cfg_t *cfg);
/* Devolve true somente na chamada em que o estado MUDOU. dist_cm < 0 = leitura invalida. */
bool        occ_update(occ_t *o, uint32_t now_ms, int16_t dist_cm);
occ_state_t occ_state(const occ_t *o);

/* Filtro de mediana de 3 leituras (tira picos isolados). Com menos de 3 leituras devolve a ultima. */
typedef struct {
    int16_t buf[3];
    uint8_t n;
    uint8_t idx;
} filter_t;

void    filter_init(filter_t *f);
int16_t filter_median3(filter_t *f, int16_t sample);

#endif
