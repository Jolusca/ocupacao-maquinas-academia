---
Disciplina: "[[TI0148_Sistemas_Embarcados]]"
Data: "2026-10-21"
Tipo: Proposta de Projeto
---

# Sistema de Ocupação e Recomendação de Equipamentos de Academia com STM32 (protótipo de baixo custo)

**Disciplina:** TI0148 – Sistemas Embarcados (2026.2)
**Equipe:** Antonio Marcos Justino Carneiro, João Victor Leandro Nunes, João Lucas Oliveira Mota, Anderson Moura Costa do Nascimento, Álvaro Siqueira Galvão
**Professor:** Dário Queiroz

> Versão para envio: `Proposta de Projeto - Ocupação de Máquinas de Academia.pdf` (gerado do `.tex` com tectonic). Slides: `Apresentação - Proposta Comercial e Técnica.pdf` (nesta pasta). A versão anterior (STM32WB com gateway Wi-Fi e MQTT) está em `Versões anteriores/` (nesta pasta).

## 1. Ideia

Nós sem fio com STM32 nos equipamentos detectam a ocupação. Um **PC de mesa** faz de servidor (recebe os dados por BLE, mantém estados, estatísticas e recomendação) e alimenta um **site** que mostra ao frequentador a próxima máquina livre da rotina dele. Os mesmos dados dão à **academia (o cliente do sistema)** estimativas de uso e frequência por equipamento, o ranking das máquinas mais e menos usadas e a base para a **manutenção preventiva**. Escala-alvo: até 100 equipamentos.

## 2. Protótipo (Fase 1, baixo custo) × Produto (Fase 2)

| | Protótipo | Produto (com investimento) |
|---|---|---|
| Nó | Blue Pill (STM32F103C8) + módulo BLE serial (HM-10/JDY-23) + sensor ultrassônico HC-SR04, alimentado por USB | STM32WB + ToF, a bateria, sem fios |
| Comunicação | PC conecta por BLE a 2 ou 3 nós | BLE advertising sem conexão, 100 nós |
| Escala de 100 | Emulador de nós | Nós reais |
| Detecção | Ultrassom | ToF e câmeras com visão computacional (PDI e ML, na borda, sem guardar imagens por LGPD) |

O servidor e o site são os mesmos nas duas fases. A câmera passa a ser mais uma fonte de eventos de ocupação.

## 3. Regras no nó

- Histerese: chegada a ≤ 70 cm, saída a ≥ 90 cm.
- Presença por mais de 5 s: ocupada. Ausência por mais de 90 s: livre.
- Quadro serial ao módulo BLE: `N02,1,17` (ID, estado com 1 = ocupada e 0 = livre, sequência), repetido como sinal de vida a cada 15 s.
- Servidor: nó sem sinal de vida fica *offline*; acumula tempo e número de usos; recomenda a primeira máquina livre da rotina ou a que liberar primeiro.
- Gestão e manutenção preventiva: com o tempo e a frequência de uso acumulados por equipamento, o servidor estima o uso de cada máquina, ordena as mais e as menos usadas, identifica horários de pico e alerta a manutenção quando o uso atinge um limite configurável (horas ou número de usos). O site tem o app do frequentador e o painel da gestão.
- Simulação (por recomendação do professor): **Altium Designer** (licença de estudante) para o esquemático e a simulação do circuito do nó, com o eco do HC-SR04 imitado por uma fonte de pulso. Pela pesquisa da equipe (`docs/03-pesquisas/Pesquisa - Altium para simulação.md`), o Altium não executa firmware de microcontrolador, O firmware roda no **Renode** (principal: Blue Pill F103, UART por socket TCP, sem ADC e SPI) e no **Wokwi** (alternativa visual: Blue Pill F103C8 e HC-SR04 pronto, com automação de testes). O Proteus (F103C6, só Windows) fica como opção. Pesquisa completa em `docs/03-pesquisas/Pesquisa - Simulação do sistema.md`.

## Premissas do protótipo (ambiente e comportamento ideais)

- Cada sensor instalado na posição correta, sem obstruções.
- Cobertura BLE adequada entre os nós e o servidor.
- Frequentadores com comportamento esperado: usam a máquina pelo tempo normal, descansam por períodos curtos e não ficam parados diante do sensor sem usar a máquina.
- Quem apenas passa é tratado pelo filtro de presença, sem cobrir todos os casos de uma academia real.
- A validação em academia real, com ruído e comportamentos imprevistos, é a etapa seguinte (piloto).

## 4. Orçamento do protótipo (estimativa, sem pesquisa de preços atual)

| Item | Qtd. | Unitário (R$) | Subtotal (R$) |
|---|---|---|---|
| Blue Pill STM32F103C8T6 | 3 | 35 a 60 | 105 a 180 |
| Módulo BLE serial | 3 | 30 a 55 | 90 a 165 |
| Sensor HC-SR04 | 3 | 10 a 15 | 30 a 45 |
| Protoboard e jumpers | 3 | 15 a 30 | 45 a 90 |
| Alimentação USB | 3 | 0 a 25 | 0 a 75 |
| Gravador ST-Link V2 (clone) | 1 | 40 a 70 | 40 a 70 |
| Adaptador BLE USB (se o PC não tiver) | 1 | 0 a 40 | 0 a 40 |
| Extras | | | 5 |
| **Total (3 nós)** | | | **315 a 670** |

Com 2 nós: R$ 225 a 485. Por pessoa (5 integrantes, 3 nós): R$ 63 a 134. **Plano B de custo zero:** nós simulados no Renode ou no Wokwi, sensor imitado e serial ou socket no lugar do BLE, com o mesmo servidor e site. Teste de viabilidade na semana 1 (nó mínimo enviando um quadro ao script do servidor).

## 5. Riscos

- O ultrassom pode pegar quem passa; o filtro de 5 s reduz, mas não elimina.
- Conexões BLE do PC limitam os nós reais; 100 nós exigem advertising (produto).
- Módulos BLE baratos variam: testar 1 antes de comprar os demais.
- Muitas Blue Pill usam clones do microcontrolador, o que pode exigir ajustes de gravação.
- Bancada por USB: a autonomia de bateria do produto é só estimada.
- A simulação não cobre o rádio BLE nem o eco real do HC-SR04, que são imitados. O Altium não simula firmware (pesquisa não exaustiva: não verifiquei versões recentes) e o firmware roda no Renode ou no Wokwi. Não verifiquei se o modelo de timer deles suporta captura de entrada com a precisão do eco; por isso o eco é medido por interrupção nas duas bordas e contador livre.
- Os resultados valem para o ambiente ideal das premissas, não para uma academia real.

## 6. Cronograma (6 semanas)

| Semana | Entrega |
|---|---|
| 1 | Especificação, Blue Pill gravada pelo ST-Link, medição do HC-SR04, módulo BLE na UART |
| 2 | Nó: histerese, temporizadores, quadro serial e sinal de vida |
| 3 | Servidor: conexão BLE, decodificação, estados e *offline* |
| 4 | Recomendação, estatísticas e API |
| 5 | Site e emulador de 100 nós |
| 6 | Testes de ponta a ponta, vídeo e relatório |


## 7. Pontos a confirmar com o professor

1. É aceito um protótipo com 2 ou 3 nós reais e um emulador para a escala de 100 equipamentos?
2. A Blue Pill (STM32F103C8) com módulo BLE externo é aceita como STM32 dos nós?
3. O Altium para o esquemático e a simulação do circuito do nó, com o Renode e o Wokwi para o firmware, atende à recomendação de simulação?
