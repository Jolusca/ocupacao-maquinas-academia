#include <Arduino.h>
#include "hcsr04.h"

/* TODO: validar com régua ou osciloscópio na primeira ligação com o sensor.
 * Este driver foi escrito e compilado, mas ainda não foi testado com o HC-SR04
 * de verdade. */

/* Largura do pulso de disparo, pela folha de dados. */
static const uint32_t TRIG_PULSE_US = 10;
/* Sem eco em 30 ms (~5 m): não há nada na frente. */
static const uint32_t ECHO_TIMEOUT_US = 30000;
/* O eco de uma medida precisa sumir antes da próxima. */
static const uint32_t MIN_INTERVAL_MS = 60;
/* O som anda ~1 cm a cada 29 us; o eco faz ida e volta. */
static const uint32_t US_PER_CM = 58;
/* Faixa útil do HC-SR04. */
static const int32_t MIN_CM = 2;
static const int32_t MAX_CM = 400;

static int s_trig = -1;
static int s_echo = -1;

/* Instantes (em us) da subida e da descida do ECHO e se cada um já foi visto
 * nesta medida. São escritos na interrupção e lidos no laço principal, por isso
 * volatile. */
static volatile uint32_t s_rise_us = 0;
static volatile uint32_t s_fall_us = 0;
static volatile bool s_got_rise = false;
static volatile bool s_got_fall = false;

static uint32_t s_last_ms = 0;
static int16_t s_last_cm = -1;

/* Interrupção nas duas bordas do ECHO: guarda quando o pulso subiu e quando
 * desceu. Roda em contexto de interrupção: curta, sem Serial. A descida só vale
 * depois de uma subida vista nesta medida; assim o eco atrasado de uma medida
 * anterior (que chega depois do tempo limite) não é confundido com o da medida
 * atual. */
static void IRAM_ATTR echo_isr()
{
    uint32_t now_us = micros();

    if (digitalRead(s_echo))
    {
        s_rise_us = now_us;
        s_got_rise = true;
    }
    else if (s_got_rise)
    {
        s_fall_us = now_us;
        s_got_fall = true;
    }
    else
    {
        /* Descida sem subida nesta medida: é eco atrasado, ignora. */
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
    uint32_t now_ms;
    uint32_t start_us;
    uint32_t echo_us;
    int32_t dist_cm;

    if (s_trig < 0)
    {
        return -1;
    }

    /* Chamadas mais próximas que MIN_INTERVAL_MS devolvem a última medida em
     * vez de disparar de novo. */
    now_ms = millis();
    if ((s_last_ms != 0) && ((now_ms - s_last_ms) < MIN_INTERVAL_MS))
    {
        return s_last_cm;
    }
    /* 0 significa "ainda não mediu". */
    s_last_ms = (now_ms != 0) ? now_ms : 1;

    s_got_rise = false;
    s_got_fall = false;
    digitalWrite(s_trig, HIGH);
    delayMicroseconds(TRIG_PULSE_US);
    digitalWrite(s_trig, LOW);

    /* Espera a interrupção ver a descida, com delay(1) para não travar as
     * outras tarefas (Wi-Fi). */
    start_us = micros();
    while ((!s_got_fall) && ((micros() - start_us) < ECHO_TIMEOUT_US))
    {
        delay(1);
    }

    if (!s_got_fall)
    {
        /* Sem eco: nada na frente. */
        s_last_cm = -1;
        return s_last_cm;
    }

    echo_us = s_fall_us - s_rise_us;
    /* Cast: echo_us <= 30000 us, então a distância (<= 517 cm) cabe em int32_t.
     * Arredonda para o cm mais próximo. */
    dist_cm = (int32_t)((echo_us + (US_PER_CM / 2)) / US_PER_CM);
    if ((dist_cm >= MIN_CM) && (dist_cm <= MAX_CM))
    {
        /* Cast: dist_cm está entre 2 e 400, cabe em int16_t. */
        s_last_cm = (int16_t)dist_cm;
    }
    else
    {
        s_last_cm = -1;
    }
    return s_last_cm;
}

int16_t dist_hcsr04_read(uint32_t now_ms)
{
    /* O sensor real não depende do relógio do programa. */
    (void)now_ms;
    return hcsr04_measure_cm();
}
