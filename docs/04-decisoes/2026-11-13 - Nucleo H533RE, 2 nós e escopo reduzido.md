---
Data: "2026-11-13"
Tipo: Decisão
Participantes: equipe e professor Dário Queiroz (placa e número de nós)
---

# Decisão: Nucleo H533RE, 2 nós em protoboard e escopo reduzido

**Contexto:** ao entrar na parte de firmware, o professor informou que a placa STM32 disponível no laboratório é a **Nucleo H533RE**, e ficou definido que o protótipo terá **2 nós**. A equipe pretende entregar, até o fim da disciplina, os 2 nós montados em 2 protoboards do laboratório, alimentados por fontes de mesa. A Nucleo não tem rádio, então o módulo BLE externo continua necessário. A versão completa do que foi proposto só será feita se o projeto for aprovado na bolsa.

**Decisão:**
- Placa do nó: Nucleo H533RE (do laboratório), no lugar da Blue Pill. O ST-LINK já vem na placa, então o gravador sai da compra.
- Protótipo da disciplina: 2 nós reais, servidor no PC, uma página web simples e o emulador só na versão v0.
- Ficam para a fase da bolsa: app do frequentador e painel da gestão completos, emulador de 100 nós e teste de carga, alerta de manutenção, ranking e horários de pico, simulação do firmware (Renode, Wokwi), Altium.
- Os 2 sensores HC-SR04 já foram comprados.

**Alternativas descartadas:**
- Trocar por ESP32 (BLE e Wi-Fi no próprio chip): custa o preço da placa por nó, tira o projeto do STM32 e a proposta fala em STM32. Só com aval do professor.
- Manter a Blue Pill: desnecessária, porque a Nucleo do laboratório custa zero.
- Manter simulação do firmware: o nó roda na protoboard real; a lógica de decisão continua testada no PC em C.

**Consequências:**
- Firmware: só a camada de hardware muda (medição do Echo, UART do módulo de comunicação); a máquina de estados em C não muda. Conferir se o pino do Echo (5 V) aguenta a tensão na Nucleo ou manter o divisor.
- Compra: ver a planilha "Comparativo de custos - Ocupação de Máquinas de Academia (com lojas de Fortaleza)". Peças podem ser retiradas em Fortaleza (Smart Kits, Aldeota).
- Trello: 16 cards arquivados, 22 alterados e 4 criados em 13/11/2026. Detalhes em `docs/02-planejamento/Corte de Escopo - Cards do Trello.md`.
- Em aberto: confirmar com o professor o escopo reduzido, a quantidade de Nucleo no laboratório e a escolha entre BLE e Wi-Fi.

**Cards relacionados:** Decisão: Nucleo H533RE, 2 nós em protoboard e escopo reduzido; Escolher a comunicação: BLE ou Wi-Fi; Risco: disponibilidade das Nucleo H533RE no laboratório (quadro do Trello).
