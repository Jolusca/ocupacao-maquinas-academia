#ifndef CONFIG_H
#define CONFIG_H
/* Configuração do nó. Um único firmware serve para as duas placas: o papel sai do MAC. */
#include <stdint.h>

/* --- Rede (ESP-NOW) --- */
#define CFG_CHANNEL 11   /* canal fixo; repetir a varredura de canais no local da apresentação */

/* --- Papéis por MAC (decisão de 18/11). Se trocar a placa, troque o MAC aqui. --- */
static const uint8_t CFG_MAC_GATEWAY[6] = { 0x10, 0x51, 0xDB, 0x1C, 0x51, 0x80 };  /* nó 1: ligado ao notebook */
static const uint8_t CFG_MAC_SENSOR[6]  = { 0x10, 0x51, 0xDB, 0x1C, 0x61, 0x64 };  /* nó 2: sensor remoto */
#define CFG_ID_GATEWAY 1   /* N01 */
#define CFG_ID_SENSOR  2   /* N02 */

/* D1 (a confirmar no grupo): o gateway também mede uma máquina? 1 = sim (N01), 0 = só recebe. */
#define CFG_GATEWAY_MEASURES 1

/* --- Distância --- */
#define CFG_USE_SENSOR 0   /* 0 = distância simulada (dist_fake), 1 = HC-SR04 */
#define CFG_PIN_TRIG 0     /* TODO: confirmar com a pinagem da placa (evitar GPIO8, GPIO9 e GPIO15) */
#define CFG_PIN_ECHO 1     /* o ECHO sai em 5 V: precisa de divisor de tensão até 3,3 V */

/* --- Tempo --- */
#define CFG_TIME_SCALE 1   /* 1 = tempo real; 10 = demonstração 10x mais rápida (relógio da lógica e do roteiro) */
#define CFG_SAMPLE_MS 100  /* intervalo entre leituras de distância (tempo real) */
#define CFG_LOG_MS 1000    /* intervalo do log de acompanhamento "# up=..." */

#endif
