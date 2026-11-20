#ifndef HCSR04_H
#define HCSR04_H
#include <stdbool.h>
#include <stdint.h>

/* Sensor ultrassônico HC-SR04 (só na placa).
 * - pulso de 10 us no TRIG; o eco é medido por interrupção nas duas bordas do
 *   ECHO;
 * - tempo limite de 30 ms e no mínimo 60 ms entre leituras (se chamar antes,
 *   devolve a última);
 * - evitar GPIO8, GPIO9 e GPIO15 (pinos de boot do ESP32-C6);
 * - o ECHO sai em 5 V: usar divisor de tensão até 3,3 V. */
bool hcsr04_init(int trig_pin, int echo_pin);

/* Distância de 2 a 400 cm, ou -1 se não houve eco ou ficou fora da faixa. */
int16_t hcsr04_measure_cm(void);

/* Mesma assinatura de dist_fake_read(): o programa principal escolhe uma das
 * duas e não precisa saber qual é. Devolve valor < 0 se a leitura é inválida.
 */
int16_t dist_hcsr04_read(uint32_t now_ms);
#endif
