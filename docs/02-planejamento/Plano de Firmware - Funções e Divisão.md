---
Disciplina: "[[TI0148_Sistemas_Embarcados]]"
Data: "2026-11-20"
Tipo: Plano
---

# Plano de firmware: funções e divisão de tarefas (20 a 26/11)

Base: [[Plano Comprimido]] (M1 na quinta 26/11) e a decisão `docs/04-decisoes/2026-11-18 - 2x ESP32-C6 SuperMini e ESP-NOW.md`.

## Premissas

- **Placas:** 2x ESP32-C6 SuperMini estão com o Marcos. O Anderson não tem placa.
- **Protoboard, HC-SR04 e demais componentes:** ficam no laboratório, e o primeiro acesso da equipe é na **terça 24/11, às 14h**.
- **Meta:** M1 na quinta 26/11 (um nó real mede, decide, envia e o servidor mostra).
- **Estratégia:** tudo que não depende do sensor é feito e testado **antes da terça**, com uma distância simulada no lugar do HC-SR04. Na terça entra só o driver do sensor e a calibração.
- **Camadas:** a lógica fica em C puro (compila e testa no PC, sem placa). Só a camada de hardware depende da placa. O professor já confirmou o uso do ESP32-C6; se a placa mudar de novo, só a camada de hardware muda.

## Quem faz o quê

| Camada | Pasta | Precisa de placa? | Quem | Quando |
|---|---|---|---|---|
| Quadro (codificar e decodificar) | `firmware/core/frame.c` | Não | **Anderson** | sex 20 |
| Agendador de envio (sinal de vida, seq) | `firmware/core/scheduler.c` | Não | **Anderson** | sex 20 a sáb 21 |
| Máquina de estados + filtro | `firmware/core/occupancy.c` | Não | **Anderson** (Marcos revisa) | sáb 21 a dom 22 |
| Testes no PC (`make test`) | `firmware/test/` | Não | **Anderson** | junto de cada módulo |
| Rádio ESP-NOW | `firmware/hal/radio.c` | Sim (2 placas) | **Marcos** | sex 20 a sáb 21 |
| Saída serial e log | `firmware/hal/serial_out.c` | Sim | **Marcos** | sex 20 |
| Distância simulada (cenários) | `firmware/hal/dist_fake.c` | Sim | **Marcos** | sex 20 |
| Driver do HC-SR04 | `firmware/hal/hcsr04.c` | **Sensor (terça)** | **Marcos** | escreve sáb 21, testa ter 24 |
| Programa principal e papéis | `firmware/app/main.ino` | Sim | **Marcos** | sáb 21 a seg 23 |

O que o Anderson escreve no PC é o coração do sistema e não espera hardware. Se ele terminar cedo, pega o parser do servidor com os mesmos vetores de teste.

## Decisões a fechar já (afetam as duas frentes)

| # | Decisão | Recomendação |
|---|---|---|
| D1 | O gateway também mede uma máquina? | **Sim.** Gateway = `N01` (quadro local, direto na serial); sensor remoto = `N02` (por ESP-NOW). Assim as 2 placas monitoram 2 máquinas. Se não, o protótipo tem só 1 máquina. |
| D2 | Leitura inválida do HC-SR04 (sem eco, mais de ~4 m) | Conta como **ausência** (longe). |
| D3 | Zona entre 70 e 90 cm | **Mantém a condição anterior** (histerese): não zera nem reinicia os cronômetros. |
| D4 | Quando o servidor marca nó offline | **60 s** sem quadro (4 sinais de vida perdidos). Nos ensaios a 10 m um quadro se perdeu (30 s sem notícia) e dois seguidos chegariam a 45 s. O servidor também deve aceitar quadro com `seq` repetido. Combinar com quem faz o servidor. |
| D5 | Formato do quadro no ar | **Texto ASCII igual ao da serial** (`N02,1,17`), como no contrato do Trello. Isso descarta o JSON que eu sugeri antes. |
| D6 | Papéis das placas | Pela tabela de MAC no `config.h` (já funcionou nos testes). |

## Contrato do quadro (v1)

- **Quadro:** `N<id>,<estado>,<seq>` com `id` de 1 a 99 (2 dígitos), estado `1` = ocupada e `0` = livre, `seq` de 0 a 65535 (volta a 0 depois de 65535). Exemplo: `N02,1,17`.
- **Envio:** a cada mudança de estado e a cada **15 s** (sinal de vida). Repetir o estado torna a perda de um pacote inofensiva.
- **Serial do gateway:** uma linha por quadro, terminada em `\n`. Linhas que começam com `# ` são log e o servidor **ignora**.
- **Vetores de teste:** um arquivo `firmware/test/frames.txt` com quadros válidos e inválidos, usado pelo teste em C e pelo parser em Python.

## Funções (assinaturas para trabalharem em paralelo)

### `firmware/core/` (C puro, sem hardware)

```c
/* frame.h */
typedef struct { uint8_t node; uint8_t state; uint16_t seq; } frame_t;
int frame_encode(const frame_t *f, char *out, size_t out_size); /* tamanho do texto, ou -1 */
int frame_decode(const char *line, frame_t *f);                 /* 0 ok, -1 formato, -2 fora da faixa */

/* occupancy.h */
typedef enum { OCC_FREE = 0, OCC_BUSY = 1 } occ_state_t;
typedef struct { int16_t arrive_cm; int16_t leave_cm;           /* 70 e 90 */
                 uint32_t presence_ms; uint32_t absence_ms;     /* 5000 e 90000 */ } occ_cfg_t;
void occ_init(occ_t *o, const occ_cfg_t *cfg);
bool occ_update(occ_t *o, uint32_t now_ms, int16_t dist_cm);    /* true se o estado mudou; dist_cm < 0 = inválida */
occ_state_t occ_state(const occ_t *o);
void    filter_init(filter_t *f);
int16_t filter_median3(filter_t *f, int16_t sample);            /* mediana de 3 leituras */

/* scheduler.h */
void     sched_init(tx_sched_t *s);
bool     sched_due(const tx_sched_t *s, uint32_t now_ms, bool state_changed); /* mudou, 15 s, ou 1º envio */
uint16_t sched_next_seq(tx_sched_t *s, uint32_t now_ms);                      /* marca o envio e devolve o seq */
```

### `firmware/hal/` (depende da placa)

```c
/* dist_source.h */
int16_t dist_fake_read(void);       /* lê um roteiro: passante, treino, descanso, liberação (relógio acelerável) */
int16_t dist_hcsr04_read(void);     /* cm, ou < 0 se inválida */

/* hcsr04.h */
bool    hcsr04_init(int trig_pin, int echo_pin);
int16_t hcsr04_measure_cm(void);    /* pulso de 10 us, eco por captura nas duas bordas, timeout 30 ms, mín. 60 ms entre leituras */

/* radio.h */
bool radio_init(uint8_t channel, const uint8_t peer_mac[6]);  /* canal fixo (11) */
bool radio_send(const char *frame_text);                      /* unicast; até 3 tentativas; true se o MAC confirmou */
void radio_set_rx_cb(void (*cb)(const uint8_t *mac, const char *payload, int len, int rssi));

/* serial_out.h */
void serial_emit_frame(const frame_t *f);                     /* "N02,1,17\n" */
void log_line(const char *fmt, ...);                          /* "# ..." */
```

### Programa principal (`firmware/app/`)

1. `role_from_mac()` escolhe o papel: **sensor remoto** (`N02`) ou **gateway** (`N01` + recebe).
2. A cada ~100 ms: `dist_*_read()` → `filter_median3` → `occ_update`.
3. Se `sched_due(...)`: `frame_encode`; sensor remoto chama `radio_send`, gateway chama `serial_emit_frame`.
4. Gateway: no callback do rádio, `frame_decode` valida e `serial_emit_frame` repassa (descarta quadro inválido e registra com `log_line`).

## Git

Repositório compartilhado (público): https://github.com/Jolusca/ocupacao-maquinas-academia. O esqueleto está na branch `firmware-base` (commit `e2491c7`); a `main` não foi alterada.

- Anderson: `git fetch`, `git checkout -b firmware-core origin/firmware-base`, um commit por módulo e `git push -u origin firmware-core`.
- Pastas separadas: Anderson só em `firmware/core/`; Marcos em `firmware/hal/` e `firmware/app/`. Sem conflito.
- Segunda 23/11: com os testes passando, Marcos junta a `firmware-core` com o trabalho das placas.
- Em aberto (D10): o programa principal fica em `firmware/app/main.ino` (arduino-cli, já compilou para o C6) ou no `firmware/main.cpp` vazio que já existe (PlatformIO, não testado com o C6).

## Cronograma

| Dia | Marcos (com as placas) | Anderson (só PC) |
|---|---|---|
| **Sex 20/11** (sem aula) | Esqueleto de `firmware/`, `config.h`, rádio ESP-NOW, saída serial e `dist_fake`: o quadro vai do sensor remoto ao gateway e aparece na serial. | `frame` com vetores de teste e `scheduler`. |
| **Sáb 21 a dom 22** | Sinal de vida e perdas, teste de 30 min, driver do HC-SR04 escrito (sem testar), conferir que o Python lê a serial do gateway **sem resetar a placa**. | `occupancy` com os 4 cenários (passante, treino, descanso, liberação) e casos de borda (exatamente 70 e 90 cm, ruído isolado). |
| **Seg 23/11** | Integra o `core/` do Anderson, roda os 4 cenários com `dist_fake` e o servidor por cima. | Revisão cruzada e correções. |
| **Ter 24/11** (lab, 14h) | Liga o HC-SR04 com divisor de tensão no Echo, valida o driver com régua ou osciloscópio, calibra 70/90 cm. | Servidor e página com quadros reais. |
| **Qua 25/11** | 2º nó montado e ensaio, se os componentes puderem sair do laboratório; senão, ajustes sem hardware. | Ajustes. |
| **Qui 26/11** (M1) | Demonstração: um nó real mede, decide, envia e o servidor mostra. | |

## Riscos

- **Acesso ao laboratório:** os componentes ficam lá. Se não puderem sair, o sensor só é testado nas aulas (terça e quinta, 14h), o que aperta a calibração antes do M1. Por isso o resto roda antes, com a distância simulada.
- **Porta serial nativa do C6 (resolvido em 20/11):** desligar DTR e RTS ao abrir a porta reinicia a placa. O servidor deve abrir a porta sem mexer nos dois.
- **Eco do HC-SR04 em 5 V:** precisa de divisor de tensão. Conferir na terça se há resistores para o divisor no laboratório, e que o sensor é alimentado pelo pino de 5 V da placa.
- **Pinos de boot do C6:** evitar `GPIO8`, `GPIO9` e `GPIO15` para TRIG e ECHO.
- **Antena cerâmica:** alcance medido de ~10 m com paredes. Na terça, medir no lugar real da bancada e repetir a varredura de canais.
- **Documentos desatualizados:** `README.md`, `firmware/README.md`, `servidor/README.md`, a Lista de material e o Plano comprimido ainda falam em Nucleo e BLE. Atualizar agora que o professor confirmou o ESP32-C6.
