#ifndef CONFIG_H
#define CONFIG_H
/* Configuração do nó. Um único firmware serve para todas as placas. */
#include <stdint.h>

/* --- Rede (ESP-NOW) --- */

/* Canal fixo. Repetir a varredura de canais no local da apresentação. */
#define CFG_CHANNEL 11

/* --- Identidade e papel --- */

/* Todos os nós rodam o mesmo firmware.
 *  - Papel: o nó que estiver com o notebook na USB vira o "coletor" (escreve os
 *    quadros na serial); os outros são sensores e mandam por rádio. Sai da USB
 *    sozinho; pode ser forçado com o comando "papel coletor|sensor|auto".
 *  - Número do nó (N01, N02...): gravado na flash com o comando "id N".
 *    Enquanto nada foi gravado, vale a tabela abaixo (pelo MAC da placa). Uma
 *    placa que não está na tabela fica sem número e avisa até receber "id N". */
typedef struct
{
    uint8_t mac[6];
    uint8_t id;
} cfg_default_id_t;

static const cfg_default_id_t CFG_IDS_PADRAO[] = {
    {{0x10, 0x51, 0xDB, 0x1C, 0x51, 0x80}, 1}, /* N01 */
    {{0x10, 0x51, 0xDB, 0x1C, 0x61, 0x64}, 2}, /* N02 */
};

/* O coletor também mede a máquina dele? 1 = sim, 0 = só recebe. */
#define CFG_SINK_MEASURES 1

/* --- Distância --- */

/* 0 = distância simulada (dist_fake), 1 = HC-SR04. */
#define CFG_USE_SENSOR 1

/* Pinos conferidos nas placas em 26/11 (evitar GPIO8, GPIO9 e
 * GPIO15). O ECHO sai em 5 V e precisa de divisor de tensão até 3,3 V. */
#define CFG_PIN_TRIG 0
#define CFG_PIN_ECHO 1

/* --- Tempo --- */

/* 1 = tempo real; 10 = demonstração 10x mais rápida. */
#define CFG_TIME_SCALE 1u
/* Intervalo entre leituras de distância (tempo real). */
#define CFG_SAMPLE_MS 100u
/* Intervalo do log de acompanhamento "# up=...". */
#define CFG_LOG_MS 1000u

#endif
