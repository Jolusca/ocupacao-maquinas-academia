---
Data: "2026-11-18"
Tipo: Decisão
Participantes: equipe (validação em bancada por Marcos)
---

# Decisão: 2x ESP32-C6 SuperMini com ESP-NOW

**Contexto:** em 17/11/2026, testes em bancada com dois `ESP32-D0WD-V3` mostraram que o enlace por **ESP-NOW** é simples, rápido (~2 ms de RTT) e dispensa roteador ou pareamento, enquanto a recepção BLE do `D0WD-V3` foi fraca (−92 dBm). Em 18/11/2026, foram validados dois exemplares novos de **ESP32-C6 SuperMini** (`ESP32-C6FH4`, revisão `v0.2`, 4 MB de flash, USB-Serial/JTAG nativo) disponíveis para o projeto, substituindo a **Nucleo H533RE** + módulo BLE externo.

**Decisão:**
- **Hardware dos 2 nós:** 2x **ESP32-C6 SuperMini** (`ESP32-C6FH4`, 160 MHz, 4 MB flash):
  - **Nó 1 (Gateway/Master):** MAC `10:51:db:1c:51:80` (`/dev/ttyACM0`) — ligado ao PC por USB-C.
  - **Nó 2 (Sensor remoto):** MAC `10:51:db:1c:61:64` (`/dev/ttyACM1`) — alimentado por fonte/carregador USB-C estável.
- **Comunicação entre nós:** **ESP-NOW** (rádio Wi-Fi 2,4 GHz, sem roteador), com canal fixado após varredura prévia no local da apresentação (canal 11 nos testes de laboratório).
- **Arquitetura da entrega:** `Nó 2 ──ESP-NOW──▶ Nó 1 (gateway) ──USB/serial──▶ Servidor Python ──▶ página web simples`.
- **Lógica de detecção:** mantém a mesma máquina de estados em C (histerese 70/90 cm, 5 s e 90 s, sinal de vida a cada 15 s) e o sensor HC-SR04.

**Resultados de bancada (18/11/2026):**
- **Diagnóstico individual:**
  - Nó 1 (`...51:80`): Wi-Fi Scan 5–15 redes (melhor −52 dBm) · BLE Scan 9 dispositivos (melhor **−69 dBm**).
  - Nó 2 (`...61:64`): Wi-Fi Scan 8–23 redes (melhor −48 dBm) · BLE Scan 10 dispositivos (melhor **−69 dBm**).
- **Enlace ESP-NOW bidirecional entre os dois (250 pacotes de 16 B @ 50 pacotes/s, canal 11):**

| Cenário | Entrega | Perda | RSSI médio | RTT (`p50`) |
|---|---|---|---|---|
| Lado a lado | 250 / 250 | **0,0%** | −25,0 dBm | 2,36 ms |
| 3–4 m sem obstáculos | 248 / 250 | **0,8%** | −74,8 dBm | 2,36 ms |
| 8–10 m (outra sala: paredes, mesas, cadeiras) | 247 / 250 | **1,2%** | −82,4 dBm | 3,15 ms |
| ~10 m (mesmo cenário, reteste) | 250 / 250 | **0,0%** | −78,1 dBm | 2,36 ms |
| 12 m / 17 m / 20 m (2 salas) | 0 / 250 | **100,0%** | — | — |

**Alternativas descartadas:**
- **Nucleo H533RE + módulo BLE externo (BT04-E / HM-10):** exigiria compra dos módulos BLE, validação de comandos AT e integração UART extra com prazo curto até 10/12.
- **BLE entre nós:** dispensado nesta fase porque o ESP-NOW resolve a ponte sem pareamento e com latência de ~2,4 ms.
- **Manter `ESP32-D0WD-V3`:** os dois `ESP32-C6 SuperMini` novos são compactos, idênticos entre si e entregaram 0% a 1,2% de perda até ~10 m com paredes.

**Consequências:**
- **Firmware:** compilar para `esp32:esp32:esp32c6:CDCOnBoot=cdc` (porta `/dev/ttyACM*`); evitar pinos de *boot/strapping* (`GPIO8`, `GPIO9`, `GPIO15`); usar divisor de tensão no `Echo` do HC-SR04 (5 V → 3,3 V); usar cabo e fonte USB estáveis (evitar brownout no TX).
- **Servidor:** lê os quadros pela serial USB do Nó 1 (não precisa mais de `bleak` para a entrega da disciplina).
- **Fase da bolsa (produto):** o limite medido de ~10 m com paredes pela antena cerâmica reforça que, em salões maiores de academia, o produto final deve usar gateway com antena externa (u.FL/IPEX) e nós à bateria com sensor ToF (`VL53L1X`) e BLE Advertising (`nRF52840` ou `STM32WB55`).
- **Confirmado em 20/11/2026 (informado pelo Marcos):** o professor Dário Queiroz aceitou o uso dos 2x ESP32-C6 SuperMini no lugar da Nucleo H533RE.
- **Em aberto:** atualizar os cards correspondentes no Trello. Resultados do firmware v1 nas placas: `2026-11-20 - Firmware v1 testado nas placas C6 e alcance.md`.

**Cards relacionados:** Escolher a comunicação: BLE ou Wi-Fi; Risco: disponibilidade das Nucleo H533RE no laboratório; Decisão: Nucleo H533RE, 2 nós em protoboard e escopo reduzido (quadro do Trello).
