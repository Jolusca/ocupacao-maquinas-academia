#ifndef HCSR04_H
#define HCSR04_H
#include <stdbool.h>
#include <stdint.h>

/* Pulso de 10 us no TRIG; eco medido por captura nas duas bordas; timeout de 30 ms;
 * no minimo 60 ms entre leituras. Evitar GPIO8, GPIO9 e GPIO15 (boot do ESP32-C6).
 * O ECHO sai em 5 V: usar divisor de tensao ate 3,3 V. */
bool    hcsr04_init(int trig_pin, int echo_pin);
int16_t hcsr04_measure_cm(void);   /* distancia em cm, ou -1 se sem eco (acima de ~4 m) */
#endif
