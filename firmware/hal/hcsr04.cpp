#include <Arduino.h>
#include "hcsr04.h"
#include "dist_source.h"

/* Escrito sem o sensor em maos: validar com regua ou osciloscopio na primeira vez que for ligado. */

static int s_trig = -1;
static int s_echo = -1;
static volatile uint32_t s_t_rise = 0;
static volatile uint32_t s_t_fall = 0;
static volatile bool s_got_rise = false;
static volatile bool s_got_fall = false;
static uint32_t s_last_ms = 0;
static int16_t  s_last_cm = -1;

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

    uint32_t now = millis();
    if (s_last_ms != 0 && (now - s_last_ms) < 60) return s_last_cm;
    s_last_ms = now ? now : 1;

    s_got_rise = false;
    s_got_fall = false;
    digitalWrite(s_trig, HIGH);
    delayMicroseconds(10);
    digitalWrite(s_trig, LOW);

    uint32_t t0 = micros();
    while (!s_got_fall && (micros() - t0) < 30000u) delay(1);

    if (!s_got_fall) {
        s_last_cm = -1;                       /* sem eco: nada na frente */
        return s_last_cm;
    }
    uint32_t us = s_t_fall - s_t_rise;
    int32_t cm = (int32_t)((us + 29u) / 58u); /* som: ~58 us por cm de ida e volta */
    s_last_cm = (cm >= 2 && cm <= 400) ? (int16_t)cm : -1;
    return s_last_cm;
}

extern "C" int16_t dist_hcsr04_read(uint32_t now_ms)
{
    (void)now_ms;
    return hcsr04_measure_cm();
}
