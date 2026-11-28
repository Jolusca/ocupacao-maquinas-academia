---
Data: "2026-11-20"
Tipo: Ensaio
Participantes: Marcos (bancada em casa); código do `hal/` e `app/` na branch `firmware-hal`
---

# Ensaio: firmware v1 nas duas ESP32-C6 e alcance do enlace

**Contexto:** o plano de firmware (`docs/02-planejamento/Plano de Firmware - Funções e Divisão.md`) separou a lógica em `core/` (C puro, com o Anderson) e a camada de hardware `hal/` e `app/` (com o Marcos). Em 20/11/2026 a camada de hardware foi testada nas duas placas reais, antes de haver sensor, com **distância simulada** (`hal/dist_fake.c`) e com uma **implementação de referência local do `core/`** (não a do Anderson, que ainda era *stub*). Os firmwares e as ferramentas estão na branch `firmware-hal` (commit `b5005f6`).

## Placas
- **Gateway `N01`:** ESP32-C6FH4 rev v0.2, 4 MB, MAC `10:51:DB:1C:51:80`, ligado ao notebook. Também mede uma máquina (a confirmar, D1).
- **Sensor `N02`:** igual, MAC `10:51:DB:1C:61:64`, alimentado por fonte USB, sem computador.
- Os MACs da decisão de 18/11 estão corretos. O papel de cada placa sai do MAC em `app/config.h`.

## Resultados (canal 11; cada nó envia um quadro a cada 15 s como sinal de vida, mais um a cada mudança de estado)
| Cenário | Duração | Quadros do `N02` | Perda | RSSI do `N02` |
|---|---|---|---|---|
| Placas coladas | 30 min | 131 de 131 | 0 | −23 a −19 dBm |
| ~8 m, outro quarto | 30 min | 131 de 131 | 0 | mediana −72 (de −86 a −64) |
| ~10 m, com paredes | 15 min | 66 de 67 | 1,5% (1 quadro) | mediana −83 (de −86 a −78) |
| ~12 m e ~14 m, com paredes | 2 min cada | nenhum | 100% | abaixo do limite de recepção |

- Em todos os testes completos o sinal de vida saiu a cada **15,0 s** (variação de 0,1 s), as mudanças de estado se repetiram a cada **192,0 s** (ciclo do roteiro simulado) e não houve reinício.
- O estado do roteiro mudou nos instantes previstos: ocupada em ~25 s e livre em ~182 s de cada ciclo.
- **A 10 m, 2 quadros chegaram duplicados** (mesmo `seq`, no mesmo instante): o MAC não confirmou o primeiro envio e o sensor reenviou. O quadro perdido estava cercado de quadros com −79 e −83 dBm.
- **Limite neste caminho:** entre 10 e 12 m. O sensor funcionou a 10 m na mesma fonte, o que descarta fonte e placa como causa do silêncio a 12 e 14 m.
- Limites do ensaio: distâncias e paredes **estimadas pelo Marcos**, uma posição, amostras curtas (com 1 perda em 67, a perda real pode ir de menos de 1% a cerca de 8%) e sem o metal denso de uma academia (a geladeira custou ~30 dB no ensaio de 17/11).

## Defeitos encontrados e corrigidos
1. **Abrir a serial do C6 reiniciava a placa.** Ao abrir a porta, o Linux aciona DTR e RTS juntos (estado neutro no USB-Serial/JTAG). Desligar um e depois o outro passa pelo estado de reset. `tools/le_serial.py` agora **não mexe em DTR/RTS**. O servidor deve abrir a porta do mesmo jeito.
2. **O `N02` atrasava o sinal de vida quando ninguém lia a USB dele** (saía a cada 18 s em vez de 15 s): o `Serial.print` bloqueava. Corrigido com `Serial.setTxTimeoutMs(0)` em `app/app.ino`. Consequência: **sem leitor, a placa descarta o log em vez de esperar**.
3. **Fonte de alimentação ruim já deixou o sensor mudo duas vezes** (carregador de celular). Trocar a fonte resolveu nas duas. Regra: **testar cada fonte e cabo antes da apresentação**.

## Consequências para o servidor e o plano
- O servidor **deve aceitar `seq` repetido** sem tratá-lo como erro nem como mudança de estado.
- O timeout de offline de **45 s** (D4) fica no limite: um quadro perdido deixa 30 s sem notícia e dois seguidos chegam a 45 s. **Proposta: 60 s** (4 sinais de vida). Ainda é só proposta, depende de quem faz o servidor.
- Alcance prático do protótipo em casa: **até ~8 m e no máximo um cômodo**, para ter folga acima de 11 dB. No laboratório, medir de novo com a bancada e as máquinas.
- Quando o `core/` do Anderson ficar pronto (segunda 23/11), regravar as placas com `tools/build.sh upload` e repetir um ensaio curto.

## Ainda não testado
O HC-SR04 e o divisor de tensão (terça 24/11, laboratório), o `core/` real, metal no caminho, o canal no local da apresentação e o servidor lendo a serial do gateway.

**Alternativas descartadas:** repetir o teste de 12 m em outra posição (não necessário: o objetivo era achar o limite, e o ponto de controle a 10 m já o localiza).

**Cards relacionados (Trello):** Firmware do nó v1; Servidor: decodificar, estado por máquina e offline; Escolher a comunicação: BLE ou Wi-Fi.
