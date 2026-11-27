#ifndef LINK_H
#define LINK_H
/* Quem entrega os dados ao notebook e como os outros nos o encontram.
 *
 * Todos os nos rodam o mesmo firmware. O "coletor" e o no que esta com o notebook na USB:
 * escreve na serial os quadros que recebe por radio (e os seus). Os demais sao "sensores"
 * e mandam os quadros por radio ao coletor.
 *
 *  - role_*: decide o papel do no. No modo automatico ele vira coletor quando ve o notebook
 *    na USB, com histerese (a USB pode oscilar alguns ms sem que ninguem tenha mexido no cabo).
 *  - sink_*: no sensor, guarda qual e o coletor atual, aprendido pelos avisos ("beacons") que
 *    o coletor manda por radio. Se o coletor some ou outro assume, o sensor acompanha.
 *
 * Codigo C puro: o tempo entra como argumento; nada de hardware. */
#include <stdbool.h>
#include <stdint.h>

/* Texto do aviso que o coletor transmite (broadcast). Nao comeca com 'N', entao nunca e
 * confundido com um quadro. */
#define LINK_BEACON_TEXT      "BCN"
#define LINK_BEACON_PERIOD_MS 5000u  /* um aviso a cada 5 s */
#define LINK_SINK_TIMEOUT_MS  20000u /* 4 avisos perdidos: o coletor sumiu */
#define LINK_SEND_FAIL_LIMIT  2      /* entregas seguidas sem confirmacao ate esquecer o coletor */

#define ROLE_SINK_ON_MS  2000u  /* notebook presente por 2 s: vira coletor */
#define ROLE_SINK_OFF_MS 10000u /* notebook ausente por 10 s: deixa de ser */

typedef enum {
    ROLE_MODE_AUTO   = 0, /* segue a USB */
    ROLE_MODE_SINK   = 1, /* sempre coletor */
    ROLE_MODE_SENSOR = 2  /* sempre sensor */
} role_mode_t;

typedef enum { ROLE_SENSOR = 0, ROLE_SINK = 1 } role_t;

typedef struct {
    role_mode_t mode;
    role_t      role;
    bool        timing;   /* a USB discorda do papel atual e a contagem esta correndo */
    uint32_t    since_ms; /* quando a discordancia comecou */
} role_state_t;

/* host_present: ha um computador do outro lado da USB agora. Ao ligar, o papel automatico ja
 * segue a USB sem esperar. */
void   role_init(role_state_t *r, role_mode_t mode, bool host_present);
/* Chame a cada poucas centenas de ms. Devolve o papel atual. */
role_t role_update(role_state_t *r, uint32_t now_ms, bool host_present);
/* Troca o modo em funcionamento. Forcar vale na hora; voltar ao automatico mantem o papel atual
 * e passa a seguir a USB pela histerese. */
void   role_set_mode(role_state_t *r, role_mode_t mode, bool host_present);

typedef struct {
    bool     known;
    uint8_t  mac[6];
    uint32_t last_beacon_ms;
    uint8_t  fails;
} sink_link_t;

void           sink_init(sink_link_t *s);
/* Chegou um aviso de coletor. true se o coletor mudou (apareceu ou e outro MAC): o chamador
 * deve registrar o novo MAC no radio. */
bool           sink_on_beacon(sink_link_t *s, const uint8_t mac[6], uint32_t now_ms);
/* true se ha coletor conhecido e ele avisou ha menos de 20 s. */
bool           sink_known(sink_link_t *s, uint32_t now_ms);
const uint8_t *sink_mac(const sink_link_t *s);
/* Resultado da entrega de um quadro ao coletor (ja com as tentativas do radio).
 * Falhas seguidas fazem o sensor esquecer o coletor e esperar um novo aviso. */
void           sink_on_delivery(sink_link_t *s, bool ok);

/* true se o coletor deve transmitir um aviso agora. */
bool link_beacon_due(bool sent_once, uint32_t last_ms, uint32_t now_ms);

#endif
