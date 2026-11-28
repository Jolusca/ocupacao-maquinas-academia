---
Disciplina: "[[TI0148_Sistemas_Embarcados]]"
Data: "2026-11-13"
Tipo: Plano
---

# Corte de escopo: o que fazer com cada card do Trello

Base: o retrato de 08/11/2026 (82 cards, guardado em `Versões anteriores/`; o [[Roadmap - Cards do Trello]] atual é o retrato de 13/11, com 71 cards). A decisão que gera este corte está em `docs/04-decisoes/2026-11-13 - Nucleo H533RE, 2 nós e escopo reduzido.md`.

**Escopo da disciplina (decidido em 13/11/2026):** 2 nós em 2 protoboards do laboratório, alimentados por fontes de mesa, com a placa STM32 Nucleo H533RE, sensor HC-SR04 e módulo de comunicação; um servidor no PC e **uma página web simples**; emulador só na versão v0. O resto (site completo, 100 nós emulados, manutenção preventiva, ranking, simulação e Altium) fica para a fase da bolsa, se o projeto for aprovado.

## O que foi aplicado no quadro (13/11/2026)

As tabelas abaixo partem do retrato de 08/11. Antes de aplicar, o quadro foi relido: vários cards já estavam em **Concluído** (inclusive os de Altium e as duas pesquisas de simulação) e foram deixados como estão, porque são trabalho feito. O card "Forma de Comunicação" (protobuf) é novo e também não foi tocado.

| Ação | Cards |
|---|---|
| Arquivados (reversível, pelo menu "Itens arquivados" do quadro) | 16 |
| Alterados (título, descrição ou checklist) | 22 |
| Criados | 4 |
| Cards abertos no quadro | de 93 para 81 |

Cards criados: Decisão da Nucleo H533RE e escopo reduzido; Comparativo de custos (planilha); Risco de disponibilidade das Nucleo; Escolher a comunicação (BLE ou Wi-Fi).

Nada foi excluído em definitivo. Itens de checklist já marcados foram preservados; no card "[S1] Comprar o que faltar" só se acrescentou uma nota na descrição. O estado do quadro antes da mudança ficou guardado fora do repositório para desfazer, se preciso.

Cards que a triagem de 08/11 mandava arquivar e que já estavam em Concluído, portanto ficaram: Pesquisa de Altium, Pesquisa de simulação, Decisão do Altium, Risco do Altium, Privacidade (LGPD), Esquemático do nó no Altium e Pedir a licença do Altium.

## Triagem de 08/11 (referência)

A lista a seguir foi a base do corte. A contagem desta triagem (23 a arquivar) inclui os 7 cards que já estavam em Concluído.

| Ação | Cards |
|---|---|
| Arquivar | 23 |
| Alterar | 23 |
| Manter | 36 |
| Criar | 4 novos |

## 1. Base de Conhecimento (11 cards)

| Card | Ação | O que fazer |
|---|---|---|
| Proposta de Projeto (versão atual) | Alterar | Na descrição, trocar "Blue Pill" por "Nucleo H533RE" e "2 a 3 nós" por "2 nós em protoboard, fonte de mesa" |
| Roadmap de Desenvolvimento (plano comprimido, M0 a M3) | Alterar | Acrescentar a linha: escopo reduzido em 13/11/2026 (ver Corte de Escopo) |
| Plano comprimido | Alterar | Acrescentar os cortes novos (simulação, Altium, site completo, emulador v1) à lista de cortes |
| Lista de material do protótipo | Alterar | Trocar o custo por "ver planilha Comparativo de custos" e colocar o link |
| Pesquisa: Altium para simulação | Arquivar | Altium não será usado |
| Pesquisa: simulação do sistema (Renode, Wokwi, Proteus) | Arquivar | O nó roda na protoboard real |
| Cadência da equipe e dias sem aula | Manter | |
| Decisão: protótipo com Blue Pill + BLE serial + HC-SR04 | Arquivar | Substituída pela decisão da Nucleo H533RE (card novo) |
| Decisão: 100 equipamentos por emulador de nós | Alterar | Dizer que o emulador fica só na v0 e a escala de 100 vai para a bolsa |
| Decisão: Altium só para circuito; firmware no Renode/Wokwi | Arquivar | Altium e simulador saíram |
| Decisão: eco do HC-SR04 por interrupção nas duas bordas | Alterar | A razão (simulador) caiu; o hardware real permite captura de entrada. Registrar qual será usada |

## 2. Marcos (4 cards)

| Card | Ação | O que fazer |
|---|---|---|
| M0 - Ambientes e base prontos | Alterar | Tirar do checklist "Simulador do firmware escolhido e testado" e "Altium com licença e esquemático iniciado" |
| M1 - Ponta a ponta mínimo | Manter | |
| M2 - Protótipo completo em ensaio | Alterar | "2 a 3 nós reais" vira "2 nós reais"; "App do frequentador e painel da gestão" vira "Página web simples"; tirar "Emulador de 100 nós" |
| M3 - Protótipo pronto e congelado | Manter | |

## 3. Icebox (7 cards)

Ficam como lista de coisas da bolsa. Sugestão: renomear a lista para "3. Icebox (bolsa e produto)".

| Card | Ação |
|---|---|
| Simular o circuito do Eco no Altium (SPICE) | Arquivar |
| Emulador em modo aleatório | Arquivar |
| BLE falso com Bumble para testar o servidor | Arquivar |
| Produto: nó STM32WB com ToF, a bateria e BLE advertising | Manter |
| Produto: visão computacional (PDI e ML) na borda | Manter |
| Piloto em uma academia interessada | Manter |
| Servidor: ranking e horários de pico | Manter |

## 4. Backlog (31 cards)

| Card | Ação | O que fazer |
|---|---|---|
| [S2] Máquina de estados do nó com testes no PC | Manter | |
| [S2] Firmware do nó v1 | Alterar | Tirar "Modo Sleep entre as medições" (o nó fica em fonte de mesa) |
| [S2] Servidor: decodificar, estado por máquina e offline | Manter | |
| [S2] Simular o nó nos cenários básicos | Arquivar | Os mesmos cenários são testados na bancada e nos testes em C |
| [S2] Configurar o módulo BLE | Manter | Se a equipe escolher Wi-Fi no lugar de BLE, este card muda de nome |
| [S3] Emulador v1: 100 nós com falhas | Arquivar | |
| [S3] Esquemático do nó no Altium | Arquivar | Vira um item no card do relatório (diagrama de ligação feito à mão ou em ferramenta livre) |
| [S3] Servidor: conexão BLE a 1 nó real | Manter | |
| [S3] Servidor: estatísticas de uso e recomendação v1 | Alterar | Manter só "Recomendação: dada a rotina, a primeira livre" e o registro de cada uso; tirar tempo total, número de usos e duração média |
| [S3] Teste ponta a ponta: nó real até o servidor | Manter | |
| [S3] Montar o 2º nó (3º só se sobrar tempo) | Alterar | Título: "Montar o 2º nó (protoboard, fonte de mesa)"; tirar a menção ao 3º nó |
| [S3] API: estado, recomendação, estatísticas e alertas | Alterar | Título: "API mínima: estado e recomendação"; tirar "Estatísticas" e "Alertas" do checklist |
| [S4] Calibrar os tempos e limiares na bancada | Manter | |
| [S4] Site: app do frequentador | Alterar | Título: "Página web simples: estado e próxima máquina"; manter só "Mostrar a próxima máquina livre" e "Atualização em tempo real" |
| [S4] Site: painel da gestão | Arquivar | Vai para a bolsa |
| [S4] Servidor: alerta de manutenção preventiva | Arquivar | Vai para a bolsa |
| [S4] Testar a tabela de cenários | Alterar | Tirar "100 nós emulados" e "Alerta de manutenção" do checklist |
| [S4] Teste de carga com 100 nós emulados | Arquivar | |
| [S4] Robustez: reconexão BLE e perdas | Arquivar | A reconexão já está no card "Servidor: conexão BLE a 1 nó real" |
| [S4] Ensaio completo do protótipo | Manter | |
| [S4] Congelar as funcionalidades | Manter | |
| [S4] Roteiro de demonstração de 5 a 7 minutos | Manter | |
| [S4] Material para as empresas | Arquivar | A apresentação atual serve. Reabrir se o professor marcar a reunião com as empresas |
| [S5] Correções e polimento do site | Arquivar | As correções entram em "Ajustes finais e correções" |
| [S5] Gravar o vídeo de reserva | Manter | |
| [S5] Avisar o professor: protótipo pronto | Manter | |
| [S5] Ensaio final | Manter | |
| [S5] Relatório da disciplina | Alterar | Acrescentar ao checklist "Diagrama de ligação do nó" e "O que fica para a fase da bolsa" |
| [S5] Ajustes finais e correções | Manter | |
| [S5] Entrega da disciplina | Manter | |
| [S5] Reunião com as empresas (data do professor) | Manter | |

## 5. Requisitos Não-Funcionais & Arquitetura (15 cards)

| Card | Ação | O que fazer |
|---|---|---|
| Regras do nó (histerese, filtros e quadro serial) | Manter | |
| Premissas do protótipo | Alterar | Acrescentar: 2 nós em protoboard, alimentados por fonte de mesa |
| Privacidade (LGPD) na fase de produto | Arquivar | Não se aplica ao protótipo |
| Risco: atraso na entrega dos componentes | Alterar | Mitigação nova: comprar em Fortaleza (Smart Kits, Aldeota) com retirada |
| Risco: módulo BLE barato instável | Manter | |
| Risco: ponte simulador–PC (socket ou serial) pode falhar | Arquivar | Sem simulador |
| Risco: Altium não simula firmware | Arquivar | Sem Altium |
| Risco: curva de aprendizado de STM32 e BLE | Manter | |
| Risco: prazo curto, semestre termina em 11/12 | Alterar | Atualizar a lista de cortes aplicados |
| Risco: falha na demonstração ao vivo | Manter | |
| Risco: poucos encontros presenciais (2 por semana) | Manter | |
| Risco: provas de outras disciplinas, feriados e eventos | Manter | |
| Risco: ultrassom pode pegar quem passa | Manter | |
| Risco: conexões BLE do PC limitam os nós reais | Arquivar | Com 2 nós o limite não aparece |
| Risco: Blue Pill com microcontrolador clone | Arquivar | A Blue Pill saiu do plano |

## 6. Dúvidas e Bloqueios (3 cards)

| Card | Ação | O que fazer |
|---|---|---|
| Confirmar 3 pontos da proposta com o professor | Alterar | Registrar as respostas já dadas (Nucleo H533RE do laboratório, 2 nós). Trocar as perguntas sobre Blue Pill e Altium por "O escopo reduzido (2 nós, página web simples, emulador v0) é aceito para a disciplina?" |
| Descobrir qual ESP o laboratório tem | Manter | Continua útil para decidir entre BLE e Wi-Fi |
| Listar as datas de provas de outras disciplinas | Manter | |

## 7. A Fazer (11 cards)

| Card | Ação | O que fazer |
|---|---|---|
| [S1] Criar o grupo de WhatsApp e adicionar o professor | Manter | |
| [S1] Levantar o material do laboratório | Alterar | Checklist novo: quantas Nucleo H533RE, 2 protoboards, 2 fontes de mesa, módulos BLE, cabo USB da placa, osciloscópio |
| [S1] Entregar a lista de material ao professor | Alterar | Anexar a planilha de custos no lugar do valor de "3 nós: R$ 315 a 670" |
| [S1] Comprar o que faltar | Alterar | Trocar "Blue Pill x3", "ST-Link" e "adaptador BLE" por: módulo BLE x2 (1 para testar), jumpers e extras; sensores HC-SR04 já comprados |
| [S1] Pedir a licença de estudante do Altium | Arquivar | |
| [S1] Criar o repositório de código | Manter | |
| [S1] Firmware do nó: medir a distância com o HC-SR04 | Alterar | Trocar "Blue Pill" por Nucleo H533RE e acrescentar "conferir o Echo (5 V) contra o limite do pino da placa" |
| [S1] Definir o simulador do firmware | Arquivar | |
| [S1] Escrever o contrato do quadro serial e da API | Manter | |
| [S1] Emulador v0: gerar quadros | Manter | |
| [S1] Servidor esqueleto: receber quadros | Manter | |

## Cards novos

1. **Decisão: Nucleo H533RE, 2 nós em protoboard e escopo reduzido** (Base de Conhecimento). Link para a nota em `docs/04-decisoes/`.
2. **Comparativo de custos (planilha)** (Base de Conhecimento). Link da planilha no Google Sheets.
3. **Risco: disponibilidade das Nucleo H533RE no laboratório** (Requisitos Não-Funcionais). Mitigação: confirmar a quantidade; se faltar uma, ver o card "Descobrir qual ESP o laboratório tem" e a planilha de custos.
4. **Escolher a comunicação: BLE ou Wi-Fi** (Dúvidas e Bloqueios). Critérios: custo na planilha, mudança de firmware e servidor, e se o professor aceita a troca.

## Conferência da contagem

| Lista | Arquivar | Alterar | Manter | Total |
|---|---|---|---|---|
| 1. Base de Conhecimento | 4 | 6 | 1 | 11 |
| 2. Marcos | 0 | 2 | 2 | 4 |
| 3. Icebox | 3 | 0 | 4 | 7 |
| 4. Backlog | 9 | 7 | 15 | 31 |
| 5. Requisitos Não-Funcionais | 5 | 3 | 7 | 15 |
| 6. Dúvidas e Bloqueios | 0 | 1 | 2 | 3 |
| 7. A Fazer | 2 | 4 | 5 | 11 |
| **Total** | **23** | **23** | **36** | **82** |
