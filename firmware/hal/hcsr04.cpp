#include <Arduino.h>
#include "hcsr04.h"
#include "dist_source.h"

/* TODO: validar com régua ou osciloscópio na primeira ligação com o sensor. Este driver foi escrito
 * e compilado, mas ainda não foi testado com o HC-SR04 de verdade. */

static const uint32_t TRIG_PULSE_US    = 10;     /* largura do pulso de disparo, pela folha de dados */
static const uint32_t ECHO_TIMEOUT_US  = 30000;  /* sem eco em 30 ms (~5 m): não há nada na frente */
static const uint32_t MIN_INTERVAL_MS  = 60;     /* o eco de uma medida precisa sumir antes da próxima */
static const uint32_t US_PER_CM        = 58;     /* o som anda ~1 cm a cada 29 us; o eco faz ida e volta */
static const int32_t  MIN_CM           = 2;      /* faixa útil do HC-SR04 */
static const int32_t  MAX_CM           = 400;

static int s_trig = -1;
static int s_echo = -1;

/* Instantes (em us) da subida e da descida do ECHO e se cada um já foi visto nesta medida.
 * São escritos na interrupção e lidos no laço principal, por isso volatile. */
static volatile uint32_t s_t_rise = 0;
static volatile uint32_t s_t_fall = 0;
static volatile bool s_got_rise = false;
static volatile bool s_got_fall = false;

static uint32_t s_last_ms = 0;
static int16_t  s_last_cm = -1;

/* Interrupção nas duas bordas do ECHO: guarda quando o pulso subiu e quando desceu.
 * Roda em contexto de interrupção: curta, sem Serial. A descida só vale depois de uma subida
 * vista nesta medida; assim o eco atrasado de uma medida anterior (que chega depois do tempo
 * limite) não é confundido com o da medida atual. */
static void IRAM_ATTR echo_isr()
{
    uint32_t t = micros();
    if (digitalRead(s_echo)) {
        s_t_rise = t;
        s_got_rise = true;
    } else if (s_got_rise) {
        s_t_fall = t;
        s_got_fall = true;
    }
}

bool hcsr04_init(int trig_pin, int echo_pin)
{
    s_trig = trig_pin;
    s_echo = echo_pin;
    pinMode(s_trig, OUTPUT);
    digitalWrite(s_trig, LOW);
    pinMode(s_echo, INPUT);
    attachInterrupt(digitalPinToInterrupt(s_echo), echo_isr, CHANGE);
    return true;
}

int16_t hcsr04_measure_cm(void)
{
    if (s_trig < 0) return -1;

    /* Chamadas mais próximas que MIN_INTERVAL_MS devolvem a última medida em vez de disparar de novo. */
    uint32_t now = millis();
    if (s_last_ms != 0 && (now - s_last_ms) < MIN_INTERVAL_MS) return s_last_cm;
    s_last_ms = now ? now : 1;   /* 0 significa "ainda não mediu" */

    s_got_rise = false;
    s_got_fall = false;
    digitalWrite(s_trig, HIGH);
    delayMicroseconds(TRIG_PULSE_US);
    digitalWrite(s_trig, LOW);

    /* Espera a interrupção ver a descida, com delay(1) para não travar as outras tarefas (Wi-Fi). */
    uint32_t t0 = micros();
    while (!s_got_fall && (micros() - t0) < ECHO_TIMEOUT_US) delay(1);

    if (!s_got_fall) {
        s_last_cm = -1;   /* sem eco: nada na frente */
        return s_last_cm;
    }
    uint32_t us = s_t_fall - s_t_rise;
    int32_t cm = (int32_t)((us + US_PER_CM / 2) / US_PER_CM);   /* arredonda para o cm mais próximo */
    s_last_cm = (cm >= MIN_CM && cm <= MAX_CM) ? (int16_t)cm : -1;
    return s_last_cm;
}

extern "C" int16_t dist_hcsr04_read(uint32_t now_ms)
{
    (void)now_ms;   /* o sensor real não depende do relógio do programa */
    return hcsr04_measure_cm();
}
