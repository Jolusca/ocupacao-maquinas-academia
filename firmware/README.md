# firmware

Nós do protótipo: **ESP32-C6 SuperMini** (Arduino-ESP32, placa `esp32:esp32:esp32c6` com `CDCOnBoot=cdc`), sensor ultrassônico **HC-SR04** e comunicação por **ESP-NOW** (canal fixo, sem roteador).

```
Nó 2 (sensor) --ESP-NOW--> Nó 1 (gateway) --USB/serial--> servidor (Python) --> página web
```

O código é dividido em camadas para que a lógica seja testada no PC, sem placa:

| Pasta | O que tem | Precisa de placa? |
|---|---|---|
| `core/` | Lógica em C puro: quadro (`frame`), máquina de estados e filtro (`occupancy`), agendador de envio (`scheduler`) | Não |
| `hal/` | Cabeçalhos da camada de hardware: sensor (`hcsr04`), distância (`dist_source`), rádio (`radio`), serial (`serial_out`) | Sim |
| `app/` | Programa principal da placa (a fazer) | Sim |
| `test/` | Testes do `core/` e vetores do quadro (`frames.txt`) | Não |

## Como rodar os testes (no PC)

```
cd firmware
make test      # compila e roda test_frame, test_occupancy e test_scheduler
make clean
```

Precisa de `gcc` e `make` (no Windows, use o WSL ou o MSYS2). Os `.c` de `core/` começam como *stubs* e os testes **falham de propósito**: o trabalho é implementar até aparecer `TODOS OS TESTES PASSARAM`. Não altere os testes para fazê-los passar.

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
