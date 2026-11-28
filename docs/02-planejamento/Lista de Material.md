---
Disciplina: "[[TI0148_Sistemas_Embarcados]]"
Data: "2026-11-08"
Atualizado: "2026-11-13"
Tipo: Lista de material
---

# Lista de material do protótipo

Pedido do professor: listar o material necessário. Fontes: [[Proposta de Projeto - Ocupação de Máquinas de Academia]], o card "Comprar o que faltar" do [[Roadmap - Cards do Trello]] e a pesquisa de preços de 13/11/2026 na planilha **Comparativo de custos - Ocupação de Máquinas de Academia (com lojas de Fortaleza)** (Google Sheets, no Drive de um integrante; tem links de cada peça). Os preços são dos sites das lojas em 13/11/2026 e mudam: confirmar estoque e preço antes de comprar.

**Escopo atual (decisão de 13/11/2026):** 2 nós em 2 protoboards do laboratório, alimentados por fontes de mesa, com a placa Nucleo H533RE do laboratório. Ver `docs/04-decisoes/2026-11-13 - Nucleo H533RE, 2 nós e escopo reduzido.md`.

## Hardware (protótipo com 2 nós)

| Item | Qtd. | Origem | Preço unit. (R$) | Subtotal (R$) |
|---|---|---|---|---|
| Placa STM32 Nucleo H533RE | 2 | Laboratório (confirmar quantidade) | 0 | 0 |
| Protoboard | 2 | Laboratório | 0 | 0 |
| Fonte de mesa | 2 | Laboratório | 0 | 0 |
| Sensor ultrassônico HC-SR04 | 2 | Já comprados pela equipe | 0 | 0 |
| Módulo BLE serial BT04-E (BLE 4.2) | 2 | Smart Kits, Aldeota (retirada) | 25,90 | 51,80 |
| ou módulo BLE HM-10 (o da proposta) | 2 | Smart Kits, Aldeota (retirada) | 49,90 | 99,80 |
| Jumpers macho-fêmea, kit de 20 | 1 | Smart Kits, Aldeota (retirada) | 7,00 | 7,00 |
| Resistores do divisor de tensão do Eco e extras | | Estimativa da proposta | | 5,00 |
| **Total a comprar com BT04-E** | | | | **63,80** |
| **Total a comprar com HM-10** | | | | **111,80** |

Totais calculados à mão, sem frete (a compra é por retirada em Fortaleza). A planilha ainda considera protoboards comprados, então os totais dela são maiores. Se o laboratório não tiver as 2 Nucleo H533RE, a placa vira custo: a Nucleo-F446RE da Smart Kits custa R$ 369,90 e serve só de ordem de grandeza.

A Nucleo traz o ST-LINK, então **não é preciso gravador**. A Blue Pill e o ST-Link V2 do plano anterior saíram da lista.

**Instrumentos** (do laboratório): osciloscópio, para conferir o eco do HC-SR04 e o quadro serial.

**Observações**
- Comprar 1 módulo BLE e testar antes do segundo. Não confirmei se o BT04-E aceita os mesmos comandos AT do HM-10.
- O Eco do HC-SR04 sai em 5 V. Conferir no manual da Nucleo H533RE se o pino escolhido tolera 5 V; se não, manter o divisor de tensão.
- A comunicação (BLE ou Wi-Fi) ainda está em aberto: ver o card "Escolher a comunicação: BLE ou Wi-Fi" e as alternativas na planilha.
- Smart Kits (Aldeota) e AutoCore Robótica publicam preço no site; a AutoCore não tem HM-10.

## Software

| Item | Para quê | Situação |
|---|---|---|
| Ferramenta de build da Nucleo H533RE (STM32CubeIDE, ou `arm-none-eabi-gcc` com OpenOCD) | Compilar e gravar o firmware | A definir pela equipe |
| Python com `bleak` | Servidor: conexão BLE | Instalar |
| tectonic | Gerar os PDFs dos documentos | Instalado |

## Fora do escopo da disciplina (fase da bolsa)

Altium Designer, Renode, Wokwi e Proteus (simulação do firmware e do circuito); emulador de 100 nós; app e painel completos. O nó roda na protoboard real e a lógica de decisão é testada em C no PC.
