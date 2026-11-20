#ifndef CONFIG_H
#define CONFIG_H
/* Configuracao do no. Um unico firmware serve para as duas placas: o papel sai do MAC. */
#include <stdint.h>

/* --- Rede (ESP-NOW) --- */
#define CFG_CANAL 11                 /* canal fixo; repetir a varredura de canais no local da apresentacao */

/* --- Papeis por MAC (decisao de 18/11). Conferir com esptool/ensaio; se mudar a placa, mude aqui. --- */
static const uint8_t CFG_MAC_GATEWAY[6] = { 0x10, 0x51, 0xDB, 0x1C, 0x51, 0x80 };  /* no 1: ligado ao notebook */
static const uint8_t CFG_MAC_SENSOR[6]  = { 0x10, 0x51, 0xDB, 0x1C, 0x61, 0x64 };  /* no 2: sensor remoto */
#define CFG_ID_GATEWAY 1             /* N01 */
#define CFG_ID_SENSOR  2             /* N02 */

/* D1 (a confirmar no grupo): o gateway tambem mede uma maquina? 1 = sim (N01), 0 = so recebe. */
#define CFG_GATEWAY_TAMBEM_MEDE 1

/* --- Distancia --- */
#define CFG_USAR_SENSOR 0            /* 0 = distancia simulada (dist_fake), 1 = HC-SR04 */
#define CFG_PIN_TRIG 0               /* provisorio: confirmar com a pinagem da placa na terca (evitar 8, 9, 15) */
#define CFG_PIN_ECHO 1               /* o ECHO precisa de divisor de tensao (5 V -> 3,3 V) */

/* --- Tempo --- */
#define CFG_TIME_SCALE 1             /* 1 = tempo real; 10 = demonstracao 10x mais rapida (relogio da logica e do roteiro) */
#define CFG_AMOSTRA_MS 100           /* intervalo entre leituras de distancia (tempo real) */
#define CFG_LOG_MS 1000              /* intervalo do log de acompanhamento "# up=..." */

#endif
