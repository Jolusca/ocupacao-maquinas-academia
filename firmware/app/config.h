#ifndef CONFIG_H
#define CONFIG_H
/* Configuração do nó. Um único firmware serve para as duas placas: o papel sai
 * do MAC. */
#include <stdint.h>

/* --- Rede (ESP-NOW) --- */

/* Canal fixo. Repetir a varredura de canais no local da apresentação. */
#define CFG_CHANNEL 11

/* --- Papéis por MAC (decisão de 18/11) --- */

/* Se trocar a placa, troque o MAC aqui. */
/* Nó 1: ligado ao notebook. */
static const uint8_t CFG_MAC_GATEWAY[6] = {
    0x10, 0x51, 0xDB, 0x1C, 0x51, 0x80
};
/* Nó 2: sensor remoto. */
static const uint8_t CFG_MAC_SENSOR[6] = { 0x10, 0x51, 0xDB, 0x1C, 0x61, 0x64 };
#define CFG_ID_GATEWAY 1 /* N01 */
#define CFG_ID_SENSOR  2 /* N02 */

/* D1 (a confirmar no grupo): o gateway também mede uma máquina?
 * 1 = sim (N01), 0 = só recebe. */
#define CFG_GATEWAY_MEASURES 1

/* --- Distância --- */

/* 0 = distância simulada (dist_fake), 1 = HC-SR04. */
#define CFG_USE_SENSOR 0

/* TODO: confirmar os pinos com a pinagem da placa (evitar GPIO8, GPIO9 e
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
