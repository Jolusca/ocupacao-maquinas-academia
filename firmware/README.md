# firmware

Nós do protótipo: **ESP32-C6 SuperMini** (Arduino-ESP32, placa `esp32:esp32:esp32c6` com `CDCOnBoot=cdc`), sensor ultrassônico **HC-SR04** e comunicação por **ESP-NOW** (canal fixo, sem roteador).

```
Nó 2 (sensor) --ESP-NOW--> Nó 1 (gateway) --USB/serial--> servidor (Python) --> página web
```

O código é dividido em camadas para que a lógica seja testada no PC, sem placa:

| Pasta | O que tem | Precisa de placa? |
|---|---|---|
| `core/` | Lógica em C puro: quadro (`frame`), máquina de estados e filtro (`occupancy`), agendador de envio (`scheduler`) | Não |
| `hal/` | Camada de hardware: sensor (`hcsr04`), rádio ESP-NOW (`radio`), serial e log (`serial_out`) e a distância simulada (`dist_fake.c`, C puro, também roda no PC) | Sim (exceto `dist_fake.c`) |
| `app/` | Programa principal (`app.ino`) e configuração (`config.h`) | Sim |
| `tools/` | `build.sh` (compila e grava) e `le_serial.py` (lê o gateway no PC) | Não |
| `test/` | Testes do `core/`, teste de integração dos cenários e vetores do quadro (`frames.txt`) | Não |

## Como rodar os testes (no PC)

```
cd firmware
make test      # compila e roda test_frame, test_occupancy e test_scheduler
make clean
```

O `test_cenarios` junta o roteiro simulado (`hal/dist_fake.c`) com o `core/` e confere quando o estado muda (ocupa em ~25 s e libera em ~182 s). Precisa de `gcc` e `make` (no Windows, use o WSL ou o MSYS2). Os `.c` de `core/` começam como *stubs* e os testes **falham de propósito**: o trabalho é implementar até aparecer `TODOS OS TESTES PASSARAM`. Não altere os testes para fazê-los passar.

## Compilar e gravar as placas

Precisa do `arduino-cli` com o core `esp32:esp32` (3.x). O mesmo firmware serve para as duas placas: o papel (gateway `N01` ou sensor `N02`) sai do MAC, na tabela de `app/config.h`.

```
cd firmware
tools/build.sh                       # compila (esp32:esp32:esp32c6, CDCOnBoot=cdc)
tools/build.sh upload /dev/ttyACM0   # compila e grava na placa
```

O `arduino-cli` só compila a pasta do sketch, então o `build.sh` junta `app/`, `hal/` e `core/` em `build/sketch/`. Opções em `app/config.h`: canal, MACs, `CFG_USAR_SENSOR` (0 = distância simulada, 1 = HC-SR04), pinos do sensor e `CFG_TIME_SCALE` (acelera o relógio para demonstrar, por exemplo 10 = dez vezes mais rápido).

## Ler a serial do gateway (no PC)

```
python3 tools/le_serial.py [/dev/ttyACM0] -t 60 -v
```

Mostra os quadros, confere lacunas no `seq` e avisa se a placa reiniciou ao abrir a porta. Precisa do `pyserial`.

## Regras do nó

- **Presença:** distância de 70 cm ou menos. **Ausência:** 90 cm ou mais, ou leitura inválida (sem eco).
- **Histerese:** entre 70 e 90 cm mantém a condição anterior.
- **Livre para ocupada:** presença contínua por mais de 5 s. **Ocupada para livre:** ausência contínua por mais de 90 s. Se a condição contrária se interrompe antes, o cronômetro volta a zero.

## Quadro serial

`N<id>,<estado>,<seq>`, por exemplo `N02,1,17`: `id` de 1 a 99 com 2 dígitos, estado `1` = ocupada e `0` = livre, `seq` de 0 a 65535 (volta a 0). Enviado a cada mudança de estado e a cada 15 s como sinal de vida. O gateway escreve uma linha por quadro na serial; linhas que começam com `# ` são log e o servidor ignora. Casos de teste do formato em `test/frames.txt`.

## Cuidados com a placa

- Pinos de TRIG e ECHO fora de `GPIO8`, `GPIO9` e `GPIO15` (boot do ESP32-C6).
- O ECHO do HC-SR04 sai em 5 V: usar divisor de tensão até 3,3 V.
- Usar fonte e cabo USB bons: um carregador fraco já derrubou um nó nos ensaios.
- Canal do ESP-NOW fixo (11 nos ensaios); repetir a varredura de canais no local da apresentação.
