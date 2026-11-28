---
Disciplina: "[[TI0148_Sistemas_Embarcados]]"
Data: "2026-11-08"
Tipo: Roadmap em cards
---

# Roadmap em cards (quadro do Trello)

Retrato do quadro em **08/11/2026**, gerado a partir do próprio Trello, com o **plano comprimido** ([[Plano Comprimido]]): início em 09/11 e entrega em 10/12. Quadro: https://trello.com/b/rjwRxeJL (privado, Workspace "Faculdade UFC"). Os cards **não têm responsáveis**, porque as frentes ainda não foram definidas.

São **82 cards** em 10 listas (11 em Base de Conhecimento, 4 em Marcos, 7 em Icebox, 31 em Backlog, 15 em Requisitos Não-Funcionais & Arquitetura, 3 em Dúvidas e Bloqueios, 11 em A Fazer). Os prazos caem às **14h dos dias de encontro** (terça e quinta). O quadro é a fonte atual; o arquivo `Roadmap - Cards do Trello.csv` guarda a primeira versão dos 52 cards do roadmap (com as datas do plano comprimido), usada na criação do quadro, e não inclui os cards acrescentados depois (base de conhecimento, riscos, decisões, grupo de WhatsApp e lista de material).

> **Atualização de 13/11/2026:** este arquivo, o `.csv`, o `.tex` e o `.pdf` são o retrato de **08/11**, antes do corte de escopo. Desde então o quadro mudou: o professor indicou a Nucleo H533RE, o protótipo ficou com 2 nós e o escopo da disciplina foi reduzido. Foram arquivados 16 cards, alterados 22 e criados 4; os cards abertos passaram de 93 para 81. As tabelas abaixo **não refletem** essas mudanças (ainda citam Blue Pill, 3 nós, Altium, site completo e emulador de 100 nós). O estado atual está no Trello e o que mudou em [[Corte de Escopo - Cards do Trello]].

## 1. Estrutura do quadro

Mesmo padrão dos quadros Melvin e Lucas: listas numeradas e um card "Sobre esta lista" no topo de cada uma.

| Lista | Para que serve |
|---|---|
| 1. Base de Conhecimento (Docs / Memória Técnica) | Pesquisas, proposta, lista de material e decisões já tomadas (cards "Decisão: ..."). Consultar aqui antes de decidir algo de novo. |
| 2. Marcos (M0 a M3) | Os marcos M0 a M3 do Roadmap. Cada um fecha quando todo o critério do checklist passa; só então vai para Concluído. |
| 3. Icebox (Banco de Ideias) | Ideias futuras ou "se sobrar tempo": ainda não priorizadas para entrar no Backlog. Inclui o que fica para depois do semestre (produto). |
| 4. Backlog (Pacotes de Trabalho por Semana) | Pacotes de trabalho das semanas S2 a S5, com checklist, mas ainda não sendo trabalhados. Na terça, puxar os da semana para A Fazer. |
| 5. Requisitos Não-Funcionais & Arquitetura | Premissas do protótipo, regras do nó e registros de risco, com a mitigação de cada um. |
| 6. Dúvidas e Bloqueios | Perguntas ao professor e coisas que travam o trabalho. Resolvida a dúvida, registrar a resposta no card e, se virar regra, criar um card de Decisão. |
| 7. A Fazer (To Do / Ready) | Cards prontos, com critério de aceite definido, aguardando alguém puxar. Esta lista concentra o que a equipe se comprometeu a fazer na semana. |
| 8. Em Execução (Doing / In Progress) | Sendo trabalhado agora. Limite recomendado: 5 cards em paralelo (1 por pessoa), para evitar gargalos. |
| 9. Revisão / Testes (Bancada ou Simulação) | Validação técnica: testado na bancada (osciloscópio, serial), no simulador (Renode ou Wokwi) ou revisado no encontro de quinta. |
| 10. Concluído (Done) | Entregue e verificado pelo critério do card. |

**Etiquetas**

| Etiqueta | Cor |
|---|---|
| Essencial | preto |
| Docs e demo | amarelo |
| Arquitetura / Risco | azul-escuro |
| Importante | lima |
| BLE e servidor | verde |
| Emulador e testes | laranja |
| Simulação e hardware | azul-claro |
| Firmware do nó | azul |
| Se sobrar tempo | azul-claro suave |
| Maior risco (fazer primeiro) | laranja-escuro |
| Dúvida | rosa |
| Marco | vermelho-escuro |
| Site | roxo |
| Bug / Débito Técnico | vermelho |

Cada card tem no máximo uma etiqueta de frente, a prioridade (Essencial, Importante ou Se sobrar tempo) e, se for o caso, "Maior risco (fazer primeiro)" (o que mais pode dar errado vem antes do resto, regra da metodologia Onda), Marco ou Dúvida.

## 2. Rotina semanal

- **Terça 14h (sincronização):** puxar os cards da semana do Backlog para A Fazer e conferir o que falta.
- **Quinta 14h (integração):** testar o critério de pronto e mover para Concluído o que passou.
- **Entre os encontros:** cada pessoa pega um card, move para Em Execução (limite recomendado de 5 em paralelo) e marca o checklist.
- Se o prazo apertar, os cortes já foram aplicados (ver [[Plano Comprimido]]); novos cortes são decididos com o professor.

## 3. Como compartilhar o quadro

O quadro é privado: só quem for membro consegue abrir o link.

1. Abrir o quadro e clicar em **Compartilhar** (canto superior direito).
2. Convidar por e-mail ou usar **Criar link** (papel "Membro") e colar o link no grupo do WhatsApp.
3. Quando todos entrarem, desativar o link (**Delete link**).

---

# 4. Cards por lista

## Lista: 1. Base de Conhecimento (Docs / Memória Técnica) (11 cards)

_Pesquisas, proposta, lista de material e decisões já tomadas (cards "Decisão: ..."). Consultar aqui antes de decidir algo de novo._

### Proposta de Projeto (versão atual)
- **Etiquetas:** Docs e demo
- **Prazo:** sem prazo
- **Descrição:** Sistema de ocupação e recomendação de equipamentos de academia com STM32. Protótipo (Fase 1): Blue Pill + módulo BLE serial + HC-SR04, 2 a 3 nós reais e emulador para a escala de 100. Produto (Fase 2): STM32WB + ToF, a bateria, BLE advertising, visão computacional.
  
  Fonte no repositório: docs/01-proposta/Proposta de Projeto - Ocupação de Máquinas de Academia (.md, .tex e .pdf).

### Roadmap de Desenvolvimento (plano comprimido, M0 a M3)
- **Etiquetas:** Docs e demo
- **Prazo:** sem prazo
- **Descrição:** Marcos, encontros (terça e quinta, 14h), plano semana a semana, prioridades e cortes, riscos. Plano comprimido de 09/11 a 10/12/2026: M0 12/11, M1 26/11, M2 03/12, M3 08/12 e entrega 10/12. Semestre termina em 11/12/2026.
  
  Fonte no repositório: docs/02-planejamento/Roadmap de Desenvolvimento (.md, .tex e .pdf).

### Plano comprimido (cronograma vigente, 09/11 a 10/12)
- **Etiquetas:** Docs e demo
- **Prazo:** sem prazo
- **Descrição:** O roadmap original (7 semanas, a partir de 26/10) não cabia no semestre. Plano atual: S1 9 a 13/11, S2 16 a 19/11, S3 23 a 26/11, S4 30/11 a 3/12, S5 7 a 10/12. Marcos: M0 qui 12/11, M1 qui 26/11, M2 qui 03/12, M3 ter 08/12, entrega qui 10/12.
  
  Cortes aplicados: ranking e horários de pico (Icebox), 3º nó (só se sobrar tempo), simulação do circuito no Altium (só o esquemático) e emulador aleatório. Comunicar ao professor o corte do ranking.
  
  Fonte no repositório: docs/02-planejamento/Plano Comprimido.md.

### Lista de material do protótipo
- **Etiquetas:** Docs e demo
- **Prazo:** sem prazo
- **Descrição:** Itens, quantidades e custo estimado (R$ 315 a 670 para 3 nós; R$ 225 a 485 para 2). Plano B de custo zero: nós simulados no Renode ou no Wokwi.
  
  Fonte no repositório: docs/02-planejamento/Lista de Material.md.

### Pesquisa: Altium para simulação
- **Etiquetas:** Docs e demo
- **Prazo:** sem prazo
- **Descrição:** Conclusão: o Altium serve para esquemático e simulação do circuito (SPICE), mas não executa firmware de microcontrolador. Licença de estudante com e-mail institucional. Pesquisa não exaustiva, de 22/10/2026.
  
  Fonte no repositório: docs/03-pesquisas/Pesquisa - Altium para simulação.md.

### Pesquisa: simulação do sistema (Renode, Wokwi, Proteus)
- **Etiquetas:** Docs e demo
- **Prazo:** sem prazo
- **Descrição:** Renode é o principal para o firmware (Blue Pill F103, UART por socket TCP, sem ADC e SPI). Wokwi é a alternativa visual (Blue Pill F103C8 e HC-SR04 prontos). Proteus (F103C6, só Windows) fica como opção.
  
  Fonte no repositório: docs/03-pesquisas/Pesquisa - Simulação do sistema.md.

### Cadência da equipe e dias sem aula
- **Etiquetas:** Docs e demo
- **Prazo:** sem prazo
- **Descrição:** Encontros às terças e quintas, 14h, no horário da aula (bancada e laboratório). Início do projeto: segunda 09/11/2026; primeiro encontro terça 10/11.
  
  Datas do calendário da UFC (campus Fortaleza, o plano usa este; em Sobral podem ser outras):
  - 20/11 (sexta, Consciência Negra): sem aula. Não cai em dia de encontro; por isso o prazo da S2 ficou em quinta 19/11.
  - 11/12: fim do semestre. Avaliações finais de 12 a 18/12; síntese de notas até 19/12.
  
  Plano comprimido (08/11/2026): S1 9 a 13/11, S2 16 a 19/11, S3 23 a 26/11, S4 30/11 a 3/12 e S5 7 a 10/12. M3 em 08/12 e entrega em 10/12, antes do fim do semestre.
  
  Os dias sem aula do plano original (28/10, 2/11 e 4 a 6/11) já passaram e não afetam mais o cronograma.

### Decisão: protótipo com Blue Pill + BLE serial + HC-SR04
- **Etiquetas:** Docs e demo, Arquitetura / Risco
- **Prazo:** sem prazo
- **Descrição:** Registrada na Proposta (versão atual). Substituiu a versão STM32WB com gateway Wi-Fi e MQTT (arquivada em docs/01-proposta/Versões anteriores/). Motivo: baixo custo e disponibilidade das peças. Pendente de confirmação do professor (card em Dúvidas e Bloqueios).

### Decisão: 100 equipamentos por emulador de nós
- **Etiquetas:** Emulador e testes, Arquitetura / Risco
- **Prazo:** sem prazo
- **Descrição:** Registrada na Proposta. O PC conecta por BLE a poucos nós reais; 100 nós exigem advertising sem conexão (fase de produto). Para o protótipo, o emulador gera quadros no mesmo formato e o servidor e o site são os mesmos. Pendente de confirmação do professor.

### Decisão: Altium só para circuito; firmware no Renode/Wokwi
- **Etiquetas:** Simulação e hardware, Arquitetura / Risco
- **Prazo:** sem prazo
- **Descrição:** Pela pesquisa da equipe, o Altium não executa firmware. Pendente de confirmação do professor de que isso atende à recomendação de simulação.

### Decisão: eco do HC-SR04 por interrupção nas duas bordas
- **Etiquetas:** Firmware do nó, Arquitetura / Risco
- **Prazo:** sem prazo
- **Descrição:** Não se verificou se o modelo de timer do Renode ou do Wokwi suporta captura de entrada com a precisão do eco; por isso a medição usa interrupção nas duas bordas e um contador livre, que é mais simples de simular.

## Lista: 2. Marcos (M0 a M3) (4 cards)

_Os marcos M0 a M3 do Roadmap. Cada um fecha quando todo o critério do checklist passa; só então vai para Concluído._

### M0 - Ambientes e base prontos
- **Etiquetas:** Marco
- **Prazo:** qui 12/11/2026 14:00
- **Descrição:** Placas e módulos em mãos (do laboratório ou comprados), ambientes de simulação testados, quadro serial e API escritos, emulador v0 gerando quadros.
- **Checklist:**
  - [ ] Material em mãos
  - [ ] Simulador do firmware escolhido e testado
  - [ ] Altium com licença e esquemático iniciado
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
- **Descrição:** 2 a 3 nós reais, site (app e painel), emulador de 100 nós e cenários testados.
- **Checklist:**
  - [ ] 2 a 3 nós reais funcionando
  - [ ] App do frequentador e painel da gestão
  - [ ] Emulador de 100 nós
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

## Lista: 3. Icebox (Banco de Ideias) (7 cards)

_Ideias futuras ou "se sobrar tempo": ainda não priorizadas para entrar no Backlog. Inclui o que fica para depois do semestre (produto)._

### Simular o circuito do Eco no Altium (SPICE)
- **Etiquetas:** Simulação e hardware, Se sobrar tempo
- **Prazo:** sem prazo
- **Descrição:** Fonte de pulso imitando o Eco, divisor de tensão e carga.
- **Checklist:**
  - [ ] Montar o circuito
  - [ ] Rodar a simulação transiente
  - [ ] Conferir a tensão no pino do STM32

### Emulador em modo aleatório
- **Etiquetas:** Emulador e testes, Se sobrar tempo
- **Prazo:** sem prazo
- **Descrição:** Carga contínua com comportamentos aleatórios.
- **Checklist:**
  - [ ] Gerar comportamentos aleatórios
  - [ ] Comparar com o estado verdadeiro

### BLE falso com Bumble para testar o servidor
- **Etiquetas:** BLE e servidor, Se sobrar tempo
- **Prazo:** sem prazo
- **Descrição:** Periférico BLE emulado em Python, visto pelo bleak. Combinação ainda não verificada.
- **Checklist:**
  - [ ] Controlador virtual (VHCI no Linux)
  - [ ] Servidor GATT imitando o módulo
  - [ ] Servidor conectando por bleak

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

## Lista: 4. Backlog (Pacotes de Trabalho por Semana) (31 cards)

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

### [S2] Firmware do nó v1
- **Etiquetas:** Essencial, Firmware do nó
- **Prazo:** qui 19/11/2026 14:00
- **Descrição:** Integrar a máquina de estados ao hardware.
- **Checklist:**
  - [ ] Quadro com número de sequência
  - [ ] Sinal de vida a cada 15 s
  - [ ] Modo Sleep entre as medições
  - [ ] Quadro enviado pela UART

### [S2] Servidor: decodificar, estado por máquina e offline
- **Etiquetas:** Essencial, BLE e servidor
- **Prazo:** qui 19/11/2026 14:00
- **Descrição:** Estado de cada máquina a partir dos quadros.
- **Checklist:**
  - [ ] Decodificar quadros
  - [ ] Guardar o estado por máquina
  - [ ] Marcar offline sem sinal de vida
  - [ ] Detectar perdas pela sequência

### [S2] Simular o nó nos cenários básicos
- **Etiquetas:** Importante, Emulador e testes
- **Prazo:** qui 19/11/2026 14:00
- **Descrição:** Rodar o firmware no simulador escolhido com sensor imitado.
  
  **Critérios de aceite**
  - Dado que a máquina está livre, quando a distância fica em 70 cm ou menos por menos de 5 s e depois volta a 90 cm ou mais, então continua livre (passante).
  - Dado que a máquina está livre, quando a distância fica em 70 cm ou menos por mais de 5 s, então passa a ocupada (treino).
  - Dado que a máquina está ocupada, quando a ausência (90 cm ou mais) dura menos de 90 s, então continua ocupada (descanso).
  - Dado que a máquina está ocupada, quando a ausência dura mais de 90 s, então volta a livre (liberação).
- **Checklist:**
  - [ ] Passante (menos de 5 s) continua livre
  - [ ] Treino (mais de 5 s) vira ocupada
  - [ ] Descanso (menos de 90 s) continua ocupada
  - [ ] Liberação (mais de 90 s) volta a livre

### [S2] Configurar o módulo BLE
- **Etiquetas:** Essencial, BLE e servidor, Maior risco (fazer primeiro)
- **Prazo:** qui 19/11/2026 14:00
- **Descrição:** Colocar o módulo BLE serial para transmitir o quadro da UART.
- **Checklist:**
  - [ ] Configurar o módulo por comandos AT
  - [ ] Testar transparência UART para BLE com celular ou PC
  - [ ] Registrar nome, serviço e características

### [S3] Emulador v1: 100 nós com falhas
- **Etiquetas:** Importante, Emulador e testes
- **Prazo:** ter 24/11/2026 14:00
- **Descrição:** Emulador completo em modo roteirizado.
- **Checklist:**
  - [ ] 100 nós virtuais
  - [ ] Perdas de quadro, atraso, nós mortos e passantes
  - [ ] Modo roteirizado (cenários repetíveis)
  - [ ] Relógio acelerado
  - [ ] Comparar com o estado verdadeiro

### [S3] Esquemático do nó no Altium
- **Etiquetas:** Simulação e hardware, Importante
- **Prazo:** qui 26/11/2026 14:00
- **Descrição:** Esquemático do nó de protótipo.
- **Checklist:**
  - [ ] Blue Pill, HC-SR04 e módulo BLE
  - [ ] Divisor de tensão do Eco (5 V para 3,3 V)
  - [ ] Alimentação por USB
  - [ ] Exportar o PDF do esquemático

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
- **Checklist:**
  - [ ] Registrar cada uso com horário e duração
  - [ ] Tempo total, número de usos e duração média
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

### [S3] Montar o 2º nó (3º só se sobrar tempo)
- **Etiquetas:** Simulação e hardware, Importante
- **Prazo:** qui 26/11/2026 14:00
- **Descrição:** Replicar o nó e integrar ao servidor.
- **Checklist:**
  - [ ] Montar os nós
  - [ ] IDs diferentes por nó
  - [ ] Integrar ao servidor por BLE
  - [ ] Conferir dois nós ao mesmo tempo

### [S3] API: estado, recomendação, estatísticas e alertas
- **Etiquetas:** Essencial, BLE e servidor
- **Prazo:** qui 26/11/2026 14:00
- **Descrição:** Endpoints do contrato prontos para o site.
- **Checklist:**
  - [ ] Estado das máquinas
  - [ ] Recomendação por rotina
  - [ ] Estatísticas
  - [ ] Alertas

### [S4] Calibrar os tempos e limiares na bancada
- **Etiquetas:** Essencial, Firmware do nó
- **Prazo:** ter 01/12/2026 14:00
- **Descrição:** Ajustar valores com o hardware real.
- **Checklist:**
  - [ ] Limiares de 70 e 90 cm
  - [ ] Tempos de 5 s e 90 s
  - [ ] Intervalo do sinal de vida

### [S4] Site: app do frequentador
- **Etiquetas:** Essencial, Site
- **Prazo:** qui 03/12/2026 14:00
- **Descrição:** Frequentador informa a rotina e vê a próxima máquina.
- **Checklist:**
  - [ ] Tela para informar a rotina
  - [ ] Mostrar a próxima máquina livre
  - [ ] Mostrar estimativa de espera quando tudo está ocupado
  - [ ] Atualização em tempo real

### [S4] Site: painel da gestão
- **Etiquetas:** Importante, Site
- **Prazo:** qui 03/12/2026 14:00
- **Descrição:** Painel para a academia.
- **Checklist:**
  - [ ] Ocupação de cada equipamento em tempo real
  - [ ] Uso e frequência por máquina
  - [ ] Alertas de manutenção

### [S4] Servidor: alerta de manutenção preventiva
- **Etiquetas:** BLE e servidor, Importante
- **Prazo:** qui 03/12/2026 14:00
- **Descrição:** Alerta quando o uso acumulado atinge um limite.
  
  **Critérios de aceite**
  - Dado que o equipamento tem um limite configurado (horas ou número de usos), quando o uso acumulado atinge o limite, então o servidor gera o alerta.
  - Dado que existe um alerta, quando a gestão abre o painel, então o alerta aparece junto do equipamento.
- **Checklist:**
  - [ ] Limite configurável por equipamento (horas ou usos)
  - [ ] Gerar o alerta
  - [ ] Exibir no painel da gestão

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
  - [ ] 100 nós emulados
  - [ ] Alerta de manutenção
  - [ ] Registrar resultados

### [S4] Teste de carga com 100 nós emulados
- **Etiquetas:** Importante, Emulador e testes
- **Prazo:** qui 03/12/2026 14:00
- **Descrição:** Verificar o servidor e o site em escala.
- **Checklist:**
  - [ ] Painel atualiza em tempo aceitável
  - [ ] Recomendação correta com 100 máquinas
  - [ ] Medir o atraso do painel

### [S4] Robustez: reconexão BLE e perdas
- **Etiquetas:** BLE e servidor, Importante
- **Prazo:** qui 03/12/2026 14:00
- **Descrição:** Comportamento quando algo falha.
- **Checklist:**
  - [ ] Reconexão BLE
  - [ ] Nó que volta de offline
  - [ ] Perda de quadros

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

### [S4] Material para as empresas
- **Etiquetas:** Importante, Docs e demo
- **Prazo:** qui 03/12/2026 14:00
- **Descrição:** Apresentação comercial e resumo de uma página.
- **Checklist:**
  - [ ] Refazer a apresentação comercial a partir do deck atual
  - [ ] Resumo de uma página
  - [ ] Revisão

### [S5] Correções e polimento do site
- **Etiquetas:** Importante, Site
- **Prazo:** ter 08/12/2026 14:00
- **Descrição:** Corrigir problemas achados nos testes.
- **Checklist:**
  - [ ] Lista de problemas
  - [ ] Correções
  - [ ] Teste final do site

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

## Lista: 5. Requisitos Não-Funcionais & Arquitetura (15 cards)

_Premissas do protótipo, regras do nó e registros de risco, com a mitigação de cada um._

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

### Privacidade (LGPD) na fase de produto
- **Etiquetas:** Arquitetura / Risco
- **Prazo:** sem prazo
- **Descrição:** Na fase de produto, a detecção por câmeras com visão computacional roda na borda e não guarda imagens, por causa da LGPD. Não se aplica ao protótipo com ultrassom.

### Risco: atraso na entrega dos componentes
- **Etiquetas:** Arquitetura / Risco
- **Prazo:** sem prazo
- **Descrição:** Mitigação: Consultar antes o laboratório e comprar já o que faltar (S1). Plano B: nós simulados e o mesmo servidor e site. No plano comprimido, as peças precisam chegar até cerca de 16/11 para o módulo BLE ser configurado na S2 (19/11).

### Risco: módulo BLE barato instável
- **Etiquetas:** Arquitetura / Risco
- **Prazo:** sem prazo
- **Descrição:** Mitigação: Testar 1 antes de comprar os demais; avaliar outro módulo se falhar.

### Risco: ponte simulador–PC (socket ou serial) pode falhar
- **Etiquetas:** Arquitetura / Risco
- **Prazo:** sem prazo
- **Descrição:** Mitigação: Teste na S1; usar a bancada real como principal.

### Risco: Altium não simula firmware
- **Etiquetas:** Arquitetura / Risco
- **Prazo:** sem prazo
- **Descrição:** Mitigação: Usar só para esquemático e circuito; firmware no Renode ou no Wokwi (pesquisa já feita).

### Risco: curva de aprendizado de STM32 e BLE
- **Etiquetas:** Arquitetura / Risco
- **Prazo:** sem prazo
- **Descrição:** Mitigação: Começar pelo nó mínimo na S1; revisar em dupla.

### Risco: prazo curto, semestre termina em 11/12
- **Etiquetas:** Arquitetura / Risco
- **Prazo:** sem prazo
- **Descrição:** Mitigação: plano comprimido de 4 semanas de trabalho mais a semana final (M3 em 08/12, entrega em 10/12), com cortes já aplicados: ranking e horários de pico (Icebox), 3º nó (só se sobrar tempo) e simulação do circuito no Altium (só o esquemático). Se ainda apertar, decidir novos cortes com o professor.

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

### Risco: conexões BLE do PC limitam os nós reais
- **Etiquetas:** Arquitetura / Risco
- **Prazo:** sem prazo
- **Descrição:** Mitigação: 100 nós exigem advertising (produto). No protótipo, 2 a 3 nós reais e o emulador.

### Risco: Blue Pill com microcontrolador clone
- **Etiquetas:** Arquitetura / Risco
- **Prazo:** sem prazo
- **Descrição:** Mitigação: Pode exigir ajustes de gravação; conferir ao receber a placa.

## Lista: 6. Dúvidas e Bloqueios (3 cards)

_Perguntas ao professor e coisas que travam o trabalho. Resolvida a dúvida, registrar a resposta no card e, se virar regra, criar um card de Decisão._

### Confirmar 3 pontos da proposta com o professor
- **Etiquetas:** Essencial, Dúvida
- **Prazo:** ter 10/11/2026 14:00
- **Descrição:** Três perguntas da proposta. Marque cada item quando o professor responder e anote a resposta em um comentário neste card. Se a resposta mudar o plano, crie um card "Decisão: ..." na Base de Conhecimento.
- **Checklist:**
  - [ ] Aceita 2 a 3 nós reais com emulador para a escala de 100?
  - [ ] A Blue Pill com módulo BLE externo é aceita como STM32 dos nós?
  - [ ] Altium para esquemático e circuito, e simulador de firmware (Renode, Wokwi ou Proteus), atende à recomendação de simulação?

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

## Lista: 7. A Fazer (To Do / Ready) (11 cards)

_Cards prontos, com critério de aceite definido, aguardando alguém puxar. Esta lista concentra o que a equipe se comprometeu a fazer na semana._

### [S1] Criar o grupo de WhatsApp e adicionar o professor
- **Etiquetas:** Docs e demo, Essencial
- **Prazo:** ter 10/11/2026 14:00
- **Descrição:** Um dos primeiros pedidos do professor (Dário Queiroz). O texto de boas-vindas para fixar no grupo está em docs/02-planejamento/Grupo de WhatsApp.md. Sem prazo definido: é a primeira coisa a fazer.
- **Checklist:**
  - [ ] Criar o grupo no WhatsApp (nome sugerido: TI0148 - Ocupação de Máquinas de Academia)
  - [ ] Adicionar os 4 colegas: João Victor, João Lucas, Anderson e Álvaro
  - [ ] Adicionar o professor Dário Queiroz
  - [ ] Fixar a mensagem de boas-vindas com o link deste quadro do Trello
  - [ ] Convidar os 5 integrantes para o quadro do Trello (Compartilhar > link de convite)

### [S1] Levantar o material do laboratório
- **Etiquetas:** Essencial, Simulação e hardware
- **Prazo:** ter 10/11/2026 14:00
- **Descrição:** Antes de comprar, descobrir o que o laboratório já tem.
- **Checklist:**
  - [ ] Perguntar ao laboratório e ao professor
  - [ ] Listar placas STM32 (Blue Pill ou Nucleo) e gravador ST-Link
  - [ ] Listar módulos Bluetooth, sensores ultrassônicos e osciloscópio
  - [ ] Listar o que falta

### [S1] Entregar a lista de material ao professor
- **Etiquetas:** Essencial, Simulação e hardware
- **Prazo:** ter 10/11/2026 14:00
- **Descrição:** O professor pediu a lista do material necessário. A lista está em docs/02-planejamento/Lista de Material.md (itens, quantidades e custo estimado do protótipo com 3 nós: R$ 315 a 670, estimativa sem pesquisa de preços atual). Depende do card "Levantar o material do laboratório", para riscar o que o laboratório já tem.
- **Checklist:**
  - [ ] Conferir a lista de material com a equipe
  - [ ] Marcar o que o laboratório já tem (card "Levantar o material do laboratório")
  - [ ] Fechar quantidades e custo do que falta comprar
  - [ ] Enviar a lista ao professor
  - [ ] Registrar a resposta do professor no card

### [S1] Comprar o que faltar
- **Etiquetas:** Essencial, Simulação e hardware
- **Prazo:** ter 10/11/2026 14:00
- **Descrição:** Fazer os pedidos logo, por causa do prazo de entrega. Meta: 3 nós.
- **Checklist:**
  - [ ] Blue Pill (STM32F103C8) x3, se não houver no laboratório
  - [ ] Módulo BLE serial x3 (tipo HM-10 ou JDY-23); testar 1 antes de usar os demais
  - [ ] Sensor HC-SR04 x3
  - [ ] Gravador ST-Link V2, se não houver
  - [ ] Adaptador BLE USB, se o PC não tiver Bluetooth
  - [ ] Protoboard, jumpers e resistores

### [S1] Pedir a licença de estudante do Altium
- **Etiquetas:** Simulação e hardware, Importante
- **Prazo:** ter 10/11/2026 14:00
- **Descrição:** Licença gratuita com e-mail institucional; a aprovação leva de 1 a 2 dias.
- **Checklist:**
  - [ ] Solicitar com o e-mail da UFC
  - [ ] Confirmar o e-mail de verificação
  - [ ] Instalar o Altium Designer

### [S1] Criar o repositório de código
- **Etiquetas:** Essencial, Docs e demo
- **Prazo:** ter 10/11/2026 14:00
- **Descrição:** Repositório compartilhado da equipe.
- **Checklist:**
  - [ ] Criar o repositório
  - [ ] Pastas: firmware, servidor, site, emulador, docs
  - [ ] Dar acesso aos 5 integrantes
  - [ ] Escrever o README com como rodar cada parte

### [S1] Firmware do nó: medir a distância com o HC-SR04
- **Etiquetas:** Essencial, Firmware do nó, Maior risco (fazer primeiro)
- **Prazo:** qui 12/11/2026 14:00
- **Descrição:** Nó mínimo: medir e imprimir pela UART.
- **Checklist:**
  - [ ] Pulso de Trig de 10 microssegundos
  - [ ] Medir o Eco por interrupção nas duas bordas e contador livre
  - [ ] Converter o tempo em cm
  - [ ] Imprimir pela UART
  - [ ] Conferir com régua ou osciloscópio

### [S1] Definir o simulador do firmware
- **Etiquetas:** Essencial, Simulação e hardware
- **Prazo:** qui 12/11/2026 14:00
- **Descrição:** Escolher entre Renode, Wokwi e Proteus. Detalhes em 'Pesquisa - Simulação do sistema'.
- **Checklist:**
  - [ ] Levantar o sistema operacional de cada integrante
  - [ ] Teste Renode: Blue Pill, UART por socket TCP e script Python lendo
  - [ ] Teste Wokwi: Blue Pill com HC-SR04 imprimindo a distância
  - [ ] Teste Proteus (se houver Windows): F103C6, COMPIM e par virtual
  - [ ] Registrar a decisão e avisar a equipe

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

## Lista: 8. Em Execução (Doing / In Progress) (0 cards)

_Sendo trabalhado agora. Limite recomendado: 5 cards em paralelo (1 por pessoa), para evitar gargalos._

## Lista: 9. Revisão / Testes (Bancada ou Simulação) (0 cards)

_Validação técnica: testado na bancada (osciloscópio, serial), no simulador (Renode ou Wokwi) ou revisado no encontro de quinta._

## Lista: 10. Concluído (Done) (0 cards)

_Entregue e verificado pelo critério do card._
