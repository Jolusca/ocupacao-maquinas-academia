#ifndef HCSR04_H
#define HCSR04_H
#include <stdbool.h>
#include <stdint.h>

/* Sensor ultrassonico HC-SR04 (so na placa).
 * - pulso de 10 us no TRIG; o eco e medido por interrupcao nas duas bordas do ECHO;
 * - tempo limite de 30 ms e no minimo 60 ms entre leituras (se chamar antes, devolve a ultima);
 * - evitar GPIO8, GPIO9 e GPIO15 (boot do ESP32-C6);
 * - o ECHO sai em 5 V: usar divisor de tensao ate 3,3 V. */
bool    hcsr04_init(int trig_pin, int echo_pin);
int16_t hcsr04_measure_cm(void);   /* 2 a 400 cm, ou -1 se sem eco / fora da faixa */
#endif
