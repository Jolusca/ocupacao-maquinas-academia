---
Disciplina: "[[TI0148_Sistemas_Embarcados]]"
Data: "2026-11-13"
Tipo: Roadmap em cards
---

# Roadmap em cards (quadro do Trello)

Retrato do quadro em **13/11/2026**, gerado a partir do próprio Trello **depois do corte de escopo** ([[Corte de Escopo - Cards do Trello]]): protótipo com a **Nucleo H533RE**, **2 nós**, servidor, **uma página web simples** e emulador v0. Plano de datas em [[Plano Comprimido]] (início em 09/11, entrega em 10/12). Quadro: https://trello.com/b/rjwRxeJL (privado, Workspace "Faculdade UFC", 5 membros).

São **71 cards** em 10 listas (10 em Base de Conhecimento, 4 em Marcos, 4 em Icebox, 20 em Backlog, 11 em Requisitos Não-Funcionais & Arquitetura, 4 em Dúvidas e Bloqueios, 7 em A Fazer, 1 em Em Execução, 10 em Concluído). 3 cards já têm responsáveis; os demais ainda não. Os prazos caem às **14h dos dias de encontro** (terça e quinta). O quadro é a fonte atual; este arquivo, o `.csv`, o `.tex` e o `.pdf` são um retrato e envelhecem. O retrato anterior (08/11, com Blue Pill e 3 nós) está em `Versões anteriores/`.

> **Mudanças desde 08/11:** 16 cards foram arquivados (simulação, Altium, emulador de 100 nós, painel da gestão, alerta de manutenção, riscos que perderam o sentido), 22 foram alterados e 4 criados (decisão da Nucleo H533RE, comparativo de custos, risco de disponibilidade das Nucleo, escolha entre BLE e Wi-Fi). Cards arquivados continuam recuperáveis no Trello.

## 1. Estrutura do quadro

Listas numeradas e um card "Sobre esta lista" por lista, usado aqui apenas como descrição (não entra na contagem).

| Lista | Cards | Para que serve |
|---|---|---|
| 1. Base de Conhecimento (Docs / Memória Técnica) | 10 | Pesquisas, proposta, lista de material e decisões já tomadas (cards "Decisão: ..."). Consultar aqui antes de decidir algo de novo. |
| 2. Marcos (M0 a M3) | 4 | Os marcos M0 a M3 do Roadmap. Cada um fecha quando todo o critério do checklist passa; só então vai para Concluído. |
| 3. Icebox (Banco de Ideias) | 4 | Ideias futuras ou "se sobrar tempo": ainda não priorizadas para entrar no Backlog. Inclui o que fica para depois do semestre (produto). |
| 4. Backlog (Pacotes de Trabalho por Semana) | 20 | Pacotes de trabalho das semanas S2 a S5, com checklist, mas ainda não sendo trabalhados. Na terça, puxar os da semana para A Fazer. |
| 5. Requisitos Não-Funcionais & Arquitetura | 11 | Premissas do protótipo, regras do nó e registros de risco, com a mitigação de cada um. |
| 6. Dúvidas e Bloqueios | 4 | Perguntas ao professor e coisas que travam o trabalho. Resolvida a dúvida, registrar a resposta no card e, se virar regra, criar um card de Decisão. |
| 7. A Fazer (To Do / Ready) | 7 | Cards prontos, com critério de aceite definido, aguardando alguém puxar. Esta lista concentra o que a equipe se comprometeu a fazer na semana. |
| 8. Em Execução (Doing / In Progress) | 1 | Sendo trabalhado agora. Limite recomendado: 5 cards em paralelo (1 por pessoa), para evitar gargalos. |
| 9. Revisão / Testes (Bancada ou Simulação) | 0 | Validação técnica: testado na bancada (osciloscópio, serial), no simulador (Renode ou Wokwi) ou revisado no encontro de quinta. |
| 10. Concluído (Done) | 10 | Entregue e verificado pelo critério do card. |

**Etiquetas**

| Etiqueta | Cor |
|---|---|
| Essencial | black |
| Docs e demo | yellow |
| Arquitetura / Risco | blue_dark |
| Importante | lime |
| BLE e servidor | green |
| Emulador e testes | orange |
| Simulação e hardware | sky |
| Firmware do nó | blue |
| Se sobrar tempo | sky_light |
| Maior risco (fazer primeiro) | orange_dark |
| Dúvida | pink |
| Marco | red_dark |
| Site | purple |
| Bug / Débito Técnico | red |

Cada card tem no máximo uma etiqueta de frente, a prioridade (Essencial, Importante ou Se sobrar tempo) e, se for o caso, "Maior risco (fazer primeiro)", Marco ou Dúvida.

## 2. Rotina semanal

- **Terça 14h (sincronização):** puxar os cards da semana do Backlog para A Fazer e conferir o que falta.
- **Quinta 14h (integração):** testar o critério de pronto e mover para Concluído o que passou.
- **Entre os encontros:** cada pessoa pega um card, move para Em Execução (limite recomendado de 5 em paralelo) e marca o checklist.
- Novos cortes são decididos com o professor (ver [[Plano Comprimido]]).

---

# 3. Cards por lista

## Lista: 1. Base de Conhecimento (Docs / Memória Técnica) (10 cards)

_Pesquisas, proposta, lista de material e decisões já tomadas (cards "Decisão: ..."). Consultar aqui antes de decidir algo de novo._

### Comparativo de custos (planilha)
- **Etiquetas:** nenhuma
- **Prazo:** sem prazo
- **Descrição:** Preços de Fortaleza (Smart Kits, AutoCore) e de lojas online, com links, e 12 cenários de placa e comunicação para 2 nós: https://docs.google.com/spreadsheets/d/184wV1q2wVtxcjEutqSM5e8xseWzSOU_Mw-rwuuAy_5Q/edit

  A planilha está no Drive de um integrante; compartilhar com a equipe para todos abrirem.

### Decisão: Nucleo H533RE, 2 nós em protoboard e escopo reduzido
- **Etiquetas:** nenhuma
- **Prazo:** sem prazo
- **Descrição:** Contexto: o professor informou que a placa STM32 disponível no laboratório é a Nucleo H533RE; o protótipo fica com 2 nós em 2 protoboards, alimentados por fontes de mesa. Decisão: o escopo da disciplina é 2 nós reais, servidor no PC, página web simples e emulador v0. App completo, painel da gestão, 100 nós emulados, alerta de manutenção, ranking, simulação do firmware e Altium ficam para a fase da bolsa, se o projeto for aprovado. Consequências: a Blue Pill e o ST-Link saem da compra; os cards de simulação e de site completo foram arquivados. Fonte no repositório: docs/04-decisoes/2026-11-13 - Nucleo H533RE, 2 nós e escopo reduzido.md e docs/02-planejamento/Corte de Escopo - Cards do Trello.md.

### Forma de Comunicação
- **Etiquetas:** BLE e servidor
- **Prazo:** sem prazo
- **Descrição:** \#Exemplo de sintaxe do protobuf para o envio de dados dos nós

  syntax = "proto3";

  package fitness;

  enum MachineState {
    LIVRE = 0;
    OCUPADO = 1;
  }

  message MachineStatus {
    int32 machine_id = 1;
    MachineState state = 2;
  }

### Proposta de Projeto (versão atual)
- **Etiquetas:** Docs e demo
- **Prazo:** sem prazo
- **Descrição:** Sistema de ocupação e recomendação de equipamentos de academia com STM32. Protótipo (Fase 1): Blue Pill + módulo BLE serial + HC-SR04, 2 a 3 nós reais e emulador para a escala de 100. Produto (Fase 2): STM32WB + ToF, a bateria, BLE advertising, visão computacional.

  Fonte no repositório: docs/01-proposta/Proposta de Projeto - Ocupação de Máquinas de Academia (.md, .tex e .pdf).

  Atualização de 13/11/2026: o nó passa a usar a placa STM32 Nucleo H533RE (do laboratório) no lugar da Blue Pill, e o protótipo fica com 2 nós em protoboards, alimentados por fontes de mesa.

### Roadmap de Desenvolvimento (plano comprimido, M0 a M3)
- **Etiquetas:** Docs e demo
- **Prazo:** sem prazo
- **Descrição:** Marcos, encontros (terça e quinta, 14h), plano semana a semana, prioridades e cortes, riscos. Plano comprimido de 09/11 a 10/12/2026: M0 12/11, M1 26/11, M2 03/12, M3 08/12 e entrega 10/12. Semestre termina em 11/12/2026.

  Fonte no repositório: docs/02-planejamento/Roadmap de Desenvolvimento (.md, .tex e .pdf).

  Atualização de 13/11/2026: escopo da disciplina reduzido. Ver docs/02-planejamento/Corte de Escopo - Cards do Trello.md.

### Plano comprimido (cronograma vigente, 09/11 a 10/12)
- **Etiquetas:** Docs e demo
- **Prazo:** sem prazo
- **Descrição:** O roadmap original (7 semanas, a partir de 26/10) não cabia no semestre. Plano atual: S1 9 a 13/11, S2 16 a 19/11, S3 23 a 26/11, S4 30/11 a 3/12, S5 7 a 10/12. Marcos: M0 qui 12/11, M1 qui 26/11, M2 qui 03/12, M3 ter 08/12, entrega qui 10/12.

  Cortes aplicados: ranking e horários de pico (Icebox), 3º nó (só se sobrar tempo), simulação do circuito no Altium (só o esquemático) e emulador aleatório. Comunicar ao professor o corte do ranking.

  Fonte no repositório: docs/02-planejamento/Plano Comprimido.md.

  Atualização de 13/11/2026: novos cortes: simulação do firmware (Renode, Wokwi), Altium, site completo (fica uma página simples), emulador v1, teste de carga e alerta de manutenção. Vão para a fase da bolsa.

### Lista de material do protótipo
- **Etiquetas:** Docs e demo
- **Prazo:** sem prazo
- **Descrição:** Itens, quantidades e custo estimado (R$ 315 a 670 para 3 nós; R$ 225 a 485 para 2). Plano B de custo zero: nós simulados no Renode ou no Wokwi.

  Fonte no repositório: docs/02-planejamento/Lista de Material.md.

  Atualização de 13/11/2026: custos e lojas de Fortaleza na planilha 'Comparativo de custos - Ocupação de Máquinas de Academia (com lojas de Fortaleza)' (https://docs.google.com/spreadsheets/d/184wV1q2wVtxcjEutqSM5e8xseWzSOU_Mw-rwuuAy_5Q/edit). O valor de 3 nós acima não vale mais: o protótipo tem 2 nós e a placa vem do laboratório.

### Cadência da equipe e dias sem aula
- **Etiquetas:** Docs e demo
- **Prazo:** sem prazo
- **Descrição:** Encontros às terças e quintas, 14h, no horário da aula (bancada e laboratório). Início do projeto: segunda 09/11/2026; primeiro encontro terça 10/11.

  Datas do calendário da UFC (campus Fortaleza, o plano usa este; em Sobral podem ser outras):
  - 20/11 (sexta, Consciência Negra): sem aula. Não cai em dia de encontro; por isso o prazo da S2 ficou em quinta 19/11.
  - 11/12: fim do semestre. Avaliações finais de 12 a 18/12; síntese de notas até 19/12.

  Plano comprimido (08/11/2026): S1 9 a 13/11, S2 16 a 19/11, S3 23 a 26/11, S4 30/11 a 3/12 e S5 7 a 10/12. M3 em 08/12 e entrega em 10/12, antes do fim do semestre.

  Os dias sem aula do plano original (28/10, 2/11 e 4 a 6/11) já passaram e não afetam mais o cronograma.

### Decisão: 100 equipamentos por emulador de nós
- **Etiquetas:** Emulador e testes, Arquitetura / Risco
- **Prazo:** sem prazo
- **Descrição:** Registrada na Proposta. O PC conecta por BLE a poucos nós reais; 100 nós exigem advertising sem conexão (fase de produto). Para o protótipo, o emulador gera quadros no mesmo formato e o servidor e o site são os mesmos. Pendente de confirmação do professor.

  Atualização de 13/11/2026: o emulador fica só na versão v0 (gerador simples de quadros). A escala de 100 nós fica para a fase da bolsa.

### Decisão: eco do HC-SR04 por interrupção nas duas bordas
- **Etiquetas:** Firmware do nó, Arquitetura / Risco
- **Prazo:** sem prazo
- **Descrição:** Não se verificou se o modelo de timer do Renode ou do Wokwi suporta captura de entrada com a precisão do eco; por isso a medição usa interrupção nas duas bordas e um contador livre, que é mais simples de simular.

  Atualização de 13/11/2026: o nó roda na placa real (sem simulador), então a captura de entrada do timer também pode ser usada. Registrar aqui qual foi escolhida.

## Lista: 2. Marcos (M0 a M3) (4 cards)

_Os marcos M0 a M3 do Roadmap. Cada um fecha quando todo o critério do checklist passa; só então vai para Concluído._

### M0 - Ambientes e base prontos
- **Etiquetas:** Marco
- **Prazo:** qui 12/11/2026 14:00
- **Descrição:** Placas e módulos em mãos (do laboratório ou comprados), ambientes de simulação testados, quadro serial e API escritos, emulador v0 gerando quadros.
- **Checklist:**
  - [ ] Material em mãos
  - [ ] Contrato do quadro e da API escrito
  - [ ] Emulador v0 gerando quadros

### M1 - Ponta a ponta mínimo
- **Etiquetas:** Marco
- **Prazo:** qui 26/11/2026 14:00
- **Descrição:** Um nó real envia por BLE ao servidor, que mostra o estado da máquina.
- **Checklist:**
  - [ ] Nó real medindo e decidindo estado
  - [ ] Módulo BLE enviando o quadro
  - [ ] Servidor recebendo e mostrando o estado

### M2 - Protótipo completo em ensaio
- **Etiquetas:** Marco
- **Prazo:** qui 03/12/2026 14:00
- **Descrição:** 2 nós reais em protoboard, página web simples e cenários testados.
- **Checklist:**
  - [ ] 2 nós reais funcionando
  - [ ] Página web simples
  - [ ] Tabela de cenários testada
  - [ ] Ensaio completo feito

### M3 - Protótipo pronto e congelado (avisar o professor)
- **Etiquetas:** Marco
- **Prazo:** ter 08/12/2026 14:00
- **Descrição:** Protótipo congelado, com roteiro de demonstração e vídeo de reserva. Depois do M3, avisar o professor para marcar a reunião com as empresas (pode cair nas avaliações finais, 12 a 18/12).
- **Checklist:**
  - [ ] Funcionalidades congeladas
  - [ ] Roteiro de demonstração ensaiado
  - [ ] Vídeo de reserva gravado
  - [ ] Professor avisado

## Lista: 3. Icebox (Banco de Ideias) (4 cards)

_Ideias futuras ou "se sobrar tempo": ainda não priorizadas para entrar no Backlog. Inclui o que fica para depois do semestre (produto)._

### Produto: nó STM32WB com ToF, a bateria e BLE advertising
- **Etiquetas:** Firmware do nó, Se sobrar tempo
- **Prazo:** sem prazo
- **Descrição:** Fase 2 da proposta, fora do semestre. Substitui a Blue Pill + módulo BLE + HC-SR04 e permite os 100 nós reais sem conexão.

### Produto: visão computacional (PDI e ML) na borda
- **Etiquetas:** Se sobrar tempo
- **Prazo:** sem prazo
- **Descrição:** Mais uma fonte de eventos de ocupação, sem guardar imagens (LGPD). Depende de investimento.

### Piloto em uma academia interessada
- **Etiquetas:** Se sobrar tempo
- **Prazo:** sem prazo
- **Descrição:** Validar fora do ambiente ideal, depois da reunião com as empresas.

### Servidor: ranking e horários de pico
- **Etiquetas:** BLE e servidor, Importante
- **Prazo:** sem prazo
- **Descrição:** Cálculos de gestão.

  **Cortado do plano comprimido (08/11/2026)**, ordem de cortes nº 2. Retomar se sobrar tempo. O painel da gestão fica com ocupação, uso por máquina e alertas.
- **Checklist:**
  - [ ] Ranking por tempo total e por frequência
  - [ ] Uso agregado por hora do dia

## Lista: 4. Backlog (Pacotes de Trabalho por Semana) (20 cards)

_Pacotes de trabalho das semanas S2 a S5, com checklist, mas ainda não sendo trabalhados. Na terça, puxar os da semana para A Fazer._

### [S2] Máquina de estados do nó com testes no PC
- **Etiquetas:** Essencial, Firmware do nó, Maior risco (fazer primeiro)
- **Prazo:** qui 19/11/2026 14:00
- **Descrição:** Lógica de decisão em C separada do hardware, compilada e testada no PC.

  **Critérios de aceite**
  - Dado que a máquina está livre, quando a distância fica em 70 cm ou menos por menos de 5 s e depois volta a 90 cm ou mais, então continua livre (passante).
  - Dado que a máquina está livre, quando a distância fica em 70 cm ou menos por mais de 5 s, então passa a ocupada (treino).
  - Dado que a máquina está ocupada, quando a ausência (90 cm ou mais) dura menos de 90 s, então continua ocupada (descanso).
  - Dado que a máquina está ocupada, quando a ausência dura mais de 90 s, então volta a livre (liberação).
- **Checklist:**
  - [ ] Histerese: chegada a 70 cm e saída a 90 cm
  - [ ] Ocupar após 5 s de presença
  - [ ] Liberar após 90 s de ausência
  - [ ] Testes unitários: passante, treino, descanso, liberação

### [S2] Configurar o módulo BLE
- **Etiquetas:** Essencial, BLE e servidor, Maior risco (fazer primeiro)
- **Prazo:** qui 19/11/2026 14:00
- **Descrição:** Colocar o módulo BLE serial para transmitir o quadro da UART.
- **Checklist:**
  - [ ] Configurar o módulo por comandos AT
  - [ ] Testar transparência UART para BLE com celular ou PC
  - [ ] Registrar nome, serviço e características

### [S3] Servidor: conexão BLE a 1 nó real
- **Etiquetas:** Essencial, BLE e servidor, Maior risco (fazer primeiro)
- **Prazo:** qui 26/11/2026 14:00
- **Descrição:** Conectar o servidor ao módulo por BLE (biblioteca bleak).
- **Checklist:**
  - [ ] Descobrir o módulo
  - [ ] Conectar e receber notificações
  - [ ] Reconectar se cair
  - [ ] Entregar os quadros à mesma fonte de eventos

### [S3] Servidor: estatísticas de uso e recomendação v1
- **Etiquetas:** Essencial, BLE e servidor
- **Prazo:** qui 26/11/2026 14:00
- **Descrição:** Estatísticas por equipamento e recomendação da próxima máquina.

  **Critérios de aceite**
  - Dado que a rotina do frequentador tem as máquinas A, B e C e A está ocupada, quando B está livre, então a recomendação é B (a primeira livre da rotina).
  - Dado que todas as máquinas da rotina estão ocupadas, quando se pede a recomendação, então a resposta é a que deve liberar primeiro.
  - Dado que um uso terminou, quando o servidor o registra, então guarda horário e duração e atualiza tempo total, número de usos e duração média.

  Atualização de 13/11/2026: escopo reduzido: só o registro de cada uso e a recomendação básica.
- **Checklist:**
  - [ ] Registrar cada uso com horário e duração
  - [ ] Recomendação: dada a rotina, a primeira livre
  - [ ] Se todas ocupadas, a que deve liberar primeiro

### [S3] Teste ponta a ponta: nó real até o servidor
- **Etiquetas:** Essencial, Maior risco (fazer primeiro), Emulador e testes
- **Prazo:** qui 26/11/2026 14:00
- **Descrição:** Critério do marco M1.
- **Checklist:**
  - [ ] Nó real mede e decide
  - [ ] Módulo BLE transmite
  - [ ] Servidor mostra o estado correto

### [S3] Montar o 2º nó (protoboard, fonte de mesa)
- **Etiquetas:** Simulação e hardware, Importante
- **Prazo:** qui 26/11/2026 14:00
- **Descrição:** Replicar o nó e integrar ao servidor.

  Atualização de 13/11/2026: o protótipo tem 2 nós; não há 3º nó.
- **Checklist:**
  - [ ] Montar o 2º nó
  - [ ] IDs diferentes por nó
  - [ ] Integrar ao servidor por BLE
  - [ ] Conferir dois nós ao mesmo tempo

### [S3] API mínima: estado e recomendação
- **Etiquetas:** Essencial, BLE e servidor
- **Prazo:** qui 26/11/2026 14:00
- **Descrição:** Endpoints do contrato prontos para o site.
- **Checklist:**
  - [ ] Estado das máquinas
  - [ ] Recomendação por rotina

### [S4] Calibrar os tempos e limiares na bancada
- **Etiquetas:** Essencial, Firmware do nó
- **Prazo:** ter 01/12/2026 14:00
- **Descrição:** Ajustar valores com o hardware real.
- **Checklist:**
  - [ ] Limiares de 70 e 90 cm
  - [ ] Tempos de 5 s e 90 s
  - [ ] Intervalo do sinal de vida

### [S4] Página web simples: estado e próxima máquina
- **Etiquetas:** Essencial, Site
- **Prazo:** qui 03/12/2026 14:00
- **Descrição:** Frequentador informa a rotina e vê a próxima máquina.
- **Checklist:**
  - [ ] Mostrar a próxima máquina livre
  - [ ] Atualização em tempo real

### [S4] Testar a tabela de cenários
- **Etiquetas:** Essencial, Emulador e testes
- **Prazo:** qui 03/12/2026 14:00
- **Descrição:** Executar e registrar cada cenário.

  **Critérios de aceite**
  - Dado que a máquina está livre, quando a distância fica em 70 cm ou menos por menos de 5 s e depois volta a 90 cm ou mais, então continua livre (passante).
  - Dado que a máquina está livre, quando a distância fica em 70 cm ou menos por mais de 5 s, então passa a ocupada (treino).
  - Dado que a máquina está ocupada, quando a ausência (90 cm ou mais) dura menos de 90 s, então continua ocupada (descanso).
  - Dado que a máquina está ocupada, quando a ausência dura mais de 90 s, então volta a livre (liberação).
- **Checklist:**
  - [ ] Passante
  - [ ] Treino
  - [ ] Descanso
  - [ ] Liberação
  - [ ] Nó sem sinal de vida (offline)
  - [ ] Registrar resultados

### [S4] Ensaio completo do protótipo
- **Etiquetas:** Essencial, Emulador e testes
- **Prazo:** qui 03/12/2026 14:00
- **Descrição:** Critério do marco M2.
- **Checklist:**
  - [ ] Passar pelo roteiro de ponta a ponta
  - [ ] Anotar falhas
  - [ ] Planejar correções para a S5

### [S4] Congelar as funcionalidades
- **Etiquetas:** Essencial, Docs e demo
- **Prazo:** qui 03/12/2026 14:00
- **Descrição:** Parar de acrescentar recursos e só corrigir erros.
- **Checklist:**
  - [ ] Definir o que entra na versão final
  - [ ] Marcar a versão no repositório

### [S4] Roteiro de demonstração de 5 a 7 minutos
- **Etiquetas:** Essencial, Docs e demo
- **Prazo:** qui 03/12/2026 14:00
- **Descrição:** Roteiro para a reunião com as empresas.
- **Checklist:**
  - [ ] Escrever o roteiro
  - [ ] Definir quem fala e quem opera
  - [ ] Ensaiar com cronômetro

### [S5] Gravar o vídeo de reserva
- **Etiquetas:** Essencial, Docs e demo
- **Prazo:** ter 08/12/2026 14:00
- **Descrição:** Vídeo da demonstração para o caso de falha ao vivo.
- **Checklist:**
  - [ ] Gravar a demonstração completa
  - [ ] Revisar e exportar

### [S5] Avisar o professor: protótipo pronto
- **Etiquetas:** Essencial, Docs e demo
- **Prazo:** ter 08/12/2026 14:00
- **Descrição:** Depois do M3, avisar para marcar a reunião com as empresas.
- **Checklist:**
  - [ ] Confirmar o M3
  - [ ] Enviar a mensagem ao professor

### [S5] Ensaio final
- **Etiquetas:** Essencial, Docs e demo
- **Prazo:** ter 08/12/2026 14:00
- **Descrição:** Ensaio completo antes da entrega.
- **Checklist:**
  - [ ] Rodar o roteiro completo
  - [ ] Conferir o vídeo de reserva

### [S5] Relatório da disciplina
- **Etiquetas:** Essencial, Docs e demo
- **Prazo:** qui 10/12/2026 14:00
- **Descrição:** Relatório final do projeto.
- **Checklist:**
  - [ ] Estrutura
  - [ ] Texto das seções
  - [ ] Resultados dos testes
  - [ ] Revisão
  - [ ] Diagrama de ligação do nó
  - [ ] O que fica para a fase da bolsa

### [S5] Ajustes finais e correções
- **Etiquetas:** Essencial, Docs e demo
- **Prazo:** qui 10/12/2026 14:00
- **Descrição:** Última semana de folga.
- **Checklist:**
  - [ ] Corrigir pendências
  - [ ] Conferir o repositório e os documentos

### [S5] Entrega da disciplina
- **Etiquetas:** Essencial, Docs e demo
- **Prazo:** qui 10/12/2026 14:00
- **Descrição:** Entrega final. O semestre termina em 11/12.
- **Checklist:**
  - [ ] Relatório entregue
  - [ ] Código entregue
  - [ ] Apresentação feita, se pedida

### [S5] Reunião com as empresas (data do professor)
- **Etiquetas:** Essencial, Docs e demo
- **Prazo:** qui 10/12/2026 14:00
- **Descrição:** Data definida pelo professor depois do M3 (terça 08/12). Pode cair na quinta 10/12 ou no período de avaliações finais (12 a 18/12). Ajustar o prazo quando houver data.
- **Checklist:**
  - [ ] Data confirmada pelo professor
  - [ ] Demonstração ensaiada
  - [ ] Material impresso ou pronto
  - [ ] Vídeo de reserva à mão

## Lista: 5. Requisitos Não-Funcionais & Arquitetura (11 cards)

_Premissas do protótipo, regras do nó e registros de risco, com a mitigação de cada um._

### Risco: disponibilidade das Nucleo H533RE no laboratório
- **Etiquetas:** nenhuma
- **Prazo:** sem prazo
- **Descrição:** Ainda não sabemos quantas Nucleo H533RE o laboratório tem. Mitigação: confirmar a quantidade com o professor; se faltar uma, ver a planilha de custos e o card 'Descobrir qual ESP o laboratório tem'.

### Regras do nó (histerese, filtros e quadro serial)
- **Etiquetas:** Firmware do nó, Arquitetura / Risco
- **Prazo:** sem prazo
- **Descrição:** - Histerese: chegada em 70 cm ou menos, saída em 90 cm ou mais.
  - Presença por mais de 5 s: ocupada. Ausência por mais de 90 s: livre.
  - Quadro serial: N<id>,<estado>,<seq>, por exemplo N02,1,17 (estado 1 = ocupada, 0 = livre). Repetido como sinal de vida a cada 15 s.
  - Servidor: nó sem sinal de vida fica offline; acumula tempo e número de usos; recomenda a primeira máquina livre da rotina ou a que liberar primeiro.

### Premissas do protótipo (ambiente e comportamento ideais)
- **Etiquetas:** Arquitetura / Risco
- **Prazo:** sem prazo
- **Descrição:** - Sensor instalado na posição correta, sem obstruções.
  - Cobertura BLE adequada entre os nós e o servidor.
  - Frequentadores usam a máquina pelo tempo normal, descansam por períodos curtos e não ficam parados diante do sensor sem usar a máquina.
  - Quem apenas passa é tratado pelo filtro de presença, sem cobrir todos os casos de uma academia real.
  - A validação em academia real (piloto) é a etapa seguinte. Os resultados valem para o ambiente ideal.

  Atualização de 13/11/2026: 2 nós em protoboards, alimentados por fontes de mesa.

### Risco: atraso na entrega dos componentes
- **Etiquetas:** Arquitetura / Risco
- **Prazo:** sem prazo
- **Descrição:** Mitigação: Consultar antes o laboratório e comprar já o que faltar (S1). Plano B: nós simulados e o mesmo servidor e site. No plano comprimido, as peças precisam chegar até cerca de 16/11 para o módulo BLE ser configurado na S2 (19/11).

  Atualização de 13/11/2026: mitigação nova: comprar em Fortaleza com retirada (Smart Kits, Aldeota).

### Risco: módulo BLE barato instável
- **Etiquetas:** Arquitetura / Risco
- **Prazo:** sem prazo
- **Descrição:** Mitigação: Testar 1 antes de comprar os demais; avaliar outro módulo se falhar.

### Risco: curva de aprendizado de STM32 e BLE
- **Etiquetas:** Arquitetura / Risco
- **Prazo:** sem prazo
- **Descrição:** Mitigação: Começar pelo nó mínimo na S1; revisar em dupla.

### Risco: prazo curto, semestre termina em 11/12
- **Etiquetas:** Arquitetura / Risco
- **Prazo:** sem prazo
- **Descrição:** Mitigação: plano comprimido de 4 semanas de trabalho mais a semana final (M3 em 08/12, entrega em 10/12), com cortes já aplicados: ranking e horários de pico (Icebox), 3º nó (só se sobrar tempo) e simulação do circuito no Altium (só o esquemático). Se ainda apertar, decidir novos cortes com o professor.

  Atualização de 13/11/2026: cortes novos: simulação, Altium, site completo, emulador v1 e alerta de manutenção. Ver Corte de Escopo.

### Risco: falha na demonstração ao vivo
- **Etiquetas:** Arquitetura / Risco
- **Prazo:** sem prazo
- **Descrição:** Mitigação: Vídeo de reserva e emulador como apoio.

### Risco: poucos encontros presenciais (2 por semana)
- **Etiquetas:** Arquitetura / Risco
- **Prazo:** sem prazo
- **Descrição:** Mitigação: Dividir o trabalho para andar entre os encontros e usar os encontros para integrar e destravar.

### Risco: provas de outras disciplinas, feriados e eventos
- **Etiquetas:** Arquitetura / Risco
- **Prazo:** sem prazo
- **Descrição:** Mitigação: levantar as datas na S1 e ajustar as semanas apertadas; a reunião com as empresas pode cair nas avaliações finais (12 a 18/12).

### Risco: ultrassom pode pegar quem passa
- **Etiquetas:** Arquitetura / Risco
- **Prazo:** sem prazo
- **Descrição:** Mitigação: O filtro de 5 s reduz, mas não elimina. Fora de escopo cobrir todos os casos de uma academia real.

## Lista: 6. Dúvidas e Bloqueios (4 cards)

_Perguntas ao professor e coisas que travam o trabalho. Resolvida a dúvida, registrar a resposta no card e, se virar regra, criar um card de Decisão._

### Escolher a comunicação: BLE ou Wi-Fi
- **Etiquetas:** nenhuma
- **Prazo:** sem prazo
- **Descrição:** Critérios: custo (planilha de custos), mudança no firmware e no servidor, e se o professor aceita a troca. Com a Nucleo, o caminho atual é módulo BLE serial (HM-10 ou BT04-E); Wi-Fi exigiria um modem (ESP-01) ou trocar a placa por ESP32.

### Confirmar 3 pontos da proposta com o professor
- **Etiquetas:** Essencial, Dúvida
- **Prazo:** ter 10/11/2026 14:00
- **Descrição:** Três perguntas da proposta. Marque cada item quando o professor responder e anote a resposta em um comentário neste card. Se a resposta mudar o plano, crie um card "Decisão: ..." na Base de Conhecimento.

  Atualização de 13/11/2026: o professor indicou a Nucleo H533RE do laboratório e o protótipo ficou com 2 nós. Falta confirmar o escopo reduzido (item novo abaixo).
- **Checklist:**
  - [ ] Aceita 2 a 3 nós reais com emulador para a escala de 100?
  - [ ] O escopo reduzido (2 nós, página web simples, emulador v0) é aceito para a disciplina?

### Descobrir qual ESP o laboratório tem
- **Etiquetas:** Importante, Dúvida
- **Prazo:** ter 10/11/2026 14:00
- **Descrição:** O professor comentou um ESP no laboratório, mas não sabemos o modelo. Marque cada item quando resolvido e anote a resposta em um comentário.
- **Checklist:**
  - [ ] Perguntar o modelo e a quantidade
  - [ ] Avaliar uso como ponte de rádio ou receptor
  - [ ] Confirmar com o professor se pode

### Listar as datas de provas de outras disciplinas
- **Etiquetas:** Importante, Dúvida
- **Prazo:** qui 12/11/2026 14:00
- **Descrição:** Levantar os períodos mais apertados da equipe. Marque cada item quando resolvido.
- **Checklist:**
  - [ ] Cada integrante lista as suas provas
  - [ ] Ajustar o plano das semanas apertadas

## Lista: 7. A Fazer (To Do / Ready) (7 cards)

_Cards prontos, com critério de aceite definido, aguardando alguém puxar. Esta lista concentra o que a equipe se comprometeu a fazer na semana._

### [S2] Firmware do nó v1
- **Etiquetas:** Essencial, Firmware do nó
- **Prazo:** qui 19/11/2026 14:00
- **Responsáveis:** Antonio Marcos Justino Carneiro, andersonmoura.cn
- **Descrição:** Integrar a máquina de estados ao hardware.
- **Checklist:**
  - [ ] Quadro com número de sequência
  - [ ] Sinal de vida a cada 15 s
  - [ ] Quadro enviado pela UART

### [S2] Servidor: decodificar, estado por máquina e offline
- **Etiquetas:** Essencial, BLE e servidor
- **Prazo:** qui 19/11/2026 14:00
- **Responsáveis:** João Lucas Mota, João Nunes, Álvaro Siqueira Galvão
- **Descrição:** Estado de cada máquina a partir dos quadros.
- **Checklist:**
  - [ ] Decodificar quadros
  - [ ] Guardar o estado por máquina
  - [ ] Marcar offline sem sinal de vida
  - [ ] Detectar perdas pela sequência

### [S1] Entregar a lista de material ao professor
- **Etiquetas:** Essencial, Simulação e hardware
- **Prazo:** ter 10/11/2026 14:00
- **Descrição:** O professor pediu a lista do material necessário. A lista está em docs/02-planejamento/Lista de Material.md (itens, quantidades e custo estimado do protótipo com 3 nós: R$ 315 a 670, estimativa sem pesquisa de preços atual). Depende do card "Levantar o material do laboratório", para riscar o que o laboratório já tem.

  Atualização de 13/11/2026: anexar a planilha de custos (versão com lojas de Fortaleza) no lugar da estimativa de 3 nós.
- **Checklist:**
  - [ ] Conferir a lista de material com a equipe
  - [ ] Marcar o que o laboratório já tem (card "Levantar o material do laboratório")
  - [ ] Fechar quantidades e custo do que falta comprar
  - [ ] Enviar a lista ao professor
  - [ ] Registrar a resposta do professor no card

### [S1] Firmware do nó: medir a distância com o HC-SR04
- **Etiquetas:** Essencial, Firmware do nó, Maior risco (fazer primeiro)
- **Prazo:** qui 12/11/2026 14:00
- **Descrição:** Nó mínimo: medir e imprimir pela UART.

  Atualização de 13/11/2026: a placa é a Nucleo H533RE. Conferir se o pino do Echo (5 V no HC-SR04) aguenta a tensão ou manter o divisor.
- **Checklist:**
  - [ ] Pulso de Trig de 10 microssegundos
  - [ ] Medir o Eco por interrupção nas duas bordas e contador livre
  - [ ] Converter o tempo em cm
  - [ ] Imprimir pela UART
  - [ ] Conferir com régua ou osciloscópio
  - [ ] Conferir o limite de tensão do pino do Echo na Nucleo H533RE

### [S1] Escrever o contrato do quadro serial e da API
- **Etiquetas:** Essencial, BLE e servidor
- **Prazo:** qui 12/11/2026 14:00
- **Descrição:** Documento que fixa a comunicação entre nó, servidor e site.
- **Checklist:**
  - [ ] Quadro N<id>,<estado>,<seq> (estado 1 = ocupada, 0 = livre)
  - [ ] Sinal de vida a cada 15 s e regra de offline
  - [ ] Endpoints da API: estado, recomendação, estatísticas, alertas
  - [ ] Exemplos de quadros e respostas

### [S1] Emulador v0: gerar quadros
- **Etiquetas:** Essencial, Emulador e testes
- **Prazo:** qui 12/11/2026 14:00
- **Descrição:** Script que gera quadros no formato do contrato e os entrega ao servidor.
- **Checklist:**
  - [ ] Gerar quadros de N nós
  - [ ] Entregar por socket TCP ou arquivo
  - [ ] Sinal de vida a cada 15 s

### [S1] Servidor esqueleto: receber quadros
- **Etiquetas:** Essencial, BLE e servidor
- **Prazo:** qui 12/11/2026 14:00
- **Descrição:** Servidor com fonte de eventos intercambiável (emulador, socket TCP ou serial; BLE depois).
- **Checklist:**
  - [ ] Estrutura do servidor
  - [ ] Fonte de eventos intercambiável
  - [ ] Receber e imprimir quadros do emulador

## Lista: 8. Em Execução (Doing / In Progress) (1 cards)

_Sendo trabalhado agora. Limite recomendado: 5 cards em paralelo (1 por pessoa), para evitar gargalos._

### [S1] Comprar o que faltar
- **Etiquetas:** Essencial, Simulação e hardware
- **Prazo:** ter 10/11/2026 14:00
- **Descrição:** Fazer os pedidos logo, por causa do prazo de entrega. Meta: 3 nós.

  Atualização de 13/11/2026: protótipo com 2 nós e Nucleo H533RE do laboratório; Blue Pill e ST-Link saem da compra. Itens marcados acima não foram desfeitos. Peças em Fortaleza: ver a planilha de custos.
- **Checklist:**
  - [x] Blue Pill (STM32F103C8) x3, se não houver no laboratório
  - [ ] Módulo BLE serial x3 (tipo HM-10 ou JDY-23); testar 1 antes de usar os demais
  - [ ] Sensor HC-SR04 x3
  - [x] Gravador ST-Link V2, se não houver
  - [x] Adaptador BLE USB, se o PC não tiver Bluetooth
  - [x] Protoboard, jumpers e resistores

## Lista: 9. Revisão / Testes (Bancada ou Simulação) (0 cards)

_Validação técnica: testado na bancada (osciloscópio, serial), no simulador (Renode ou Wokwi) ou revisado no encontro de quinta._

_Sem cards._

## Lista: 10. Concluído (Done) (10 cards)

_Entregue e verificado pelo critério do card._

### [S3] Esquemático do nó no Altium
- **Etiquetas:** Simulação e hardware, Importante
- **Prazo:** qui 26/11/2026 14:00 (feito)
- **Descrição:** Esquemático do nó de protótipo.
- **Checklist:**
  - [ ] Blue Pill, HC-SR04 e módulo BLE
  - [ ] Divisor de tensão do Eco (5 V para 3,3 V)
  - [ ] Alimentação por USB
  - [ ] Exportar o PDF do esquemático

### Decisão: Altium só para circuito; firmware no Renode/Wokwi
- **Etiquetas:** Simulação e hardware, Arquitetura / Risco
- **Prazo:** sem prazo
- **Descrição:** Pela pesquisa da equipe, o Altium não executa firmware. Pendente de confirmação do professor de que isso atende à recomendação de simulação.

### Pesquisa: simulação do sistema (Renode, Wokwi, Proteus)
- **Etiquetas:** Docs e demo
- **Prazo:** sem prazo
- **Descrição:** Renode é o principal para o firmware (Blue Pill F103, UART por socket TCP, sem ADC e SPI). Wokwi é a alternativa visual (Blue Pill F103C8 e HC-SR04 prontos). Proteus (F103C6, só Windows) fica como opção.

  Fonte no repositório: docs/03-pesquisas/Pesquisa - Simulação do sistema.md.

### [S1] Levantar o material do laboratório
- **Etiquetas:** Essencial, Simulação e hardware
- **Prazo:** ter 10/11/2026 14:00 (feito)
- **Responsáveis:** João Lucas Mota
- **Descrição:** Antes de comprar, descobrir o que o laboratório já tem.
- **Checklist:**
  - [ ] Perguntar ao laboratório e ao professor
  - [ ] Listar placas STM32 (Blue Pill ou Nucleo) e gravador ST-Link
  - [ ] Listar módulos Bluetooth, sensores ultrassônicos e osciloscópio
  - [ ] Listar o que falta

### Pesquisa: Altium para simulação
- **Etiquetas:** Docs e demo
- **Prazo:** sem prazo
- **Descrição:** Conclusão: o Altium serve para esquemático e simulação do circuito (SPICE), mas não executa firmware de microcontrolador. Licença de estudante com e-mail institucional. Pesquisa não exaustiva, de 22/10/2026.

  Fonte no repositório: docs/03-pesquisas/Pesquisa - Altium para simulação.md.

### [S1] Pedir a licença de estudante do Altium
- **Etiquetas:** Simulação e hardware, Importante
- **Prazo:** ter 10/11/2026 14:00 (feito)
- **Descrição:** Licença gratuita com e-mail institucional; a aprovação leva de 1 a 2 dias.
- **Checklist:**
  - [ ] Solicitar com o e-mail da UFC
  - [ ] Confirmar o e-mail de verificação
  - [ ] Instalar o Altium Designer

### Risco: Altium não simula firmware
- **Etiquetas:** Arquitetura / Risco
- **Prazo:** sem prazo
- **Descrição:** Mitigação: Usar só para esquemático e circuito; firmware no Renode ou no Wokwi (pesquisa já feita).

### [S1] Criar o repositório de código
- **Etiquetas:** Essencial, Docs e demo
- **Prazo:** ter 10/11/2026 14:00 (feito)
- **Descrição:** Repositório compartilhado da equipe.
- **Checklist:**
  - [x] Criar o repositório
  - [x] Pastas: firmware, servidor, site, emulador, docs
  - [x] Dar acesso aos 5 integrantes
  - [x] Escrever o README com como rodar cada parte

### Privacidade (LGPD) na fase de produto
- **Etiquetas:** Arquitetura / Risco
- **Prazo:** sem prazo
- **Descrição:** Na fase de produto, a detecção por câmeras com visão computacional roda na borda e não guarda imagens, por causa da LGPD. Não se aplica ao protótipo com ultrassom.

### [S1] Criar o grupo de WhatsApp e adicionar o professor
- **Etiquetas:** Docs e demo, Essencial
- **Prazo:** ter 10/11/2026 14:00 (feito)
- **Descrição:** Um dos primeiros pedidos do professor (Dário Queiroz). O texto de boas-vindas para fixar no grupo está em docs/02-planejamento/Grupo de WhatsApp.md. Sem prazo definido: é a primeira coisa a fazer.
- **Checklist:**
  - [ ] Criar o grupo no WhatsApp (nome sugerido: TI0148 - Ocupação de Máquinas de Academia)
  - [ ] Adicionar os 4 colegas: João Victor, João Lucas, Anderson e Álvaro
  - [ ] Adicionar o professor Dário Queiroz
  - [ ] Fixar a mensagem de boas-vindas com o link deste quadro do Trello
  - [ ] Convidar os 5 integrantes para o quadro do Trello (Compartilhar > link de convite)
