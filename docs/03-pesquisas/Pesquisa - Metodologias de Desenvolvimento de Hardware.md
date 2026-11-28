---
Disciplina: "[[TI0148_Sistemas_Embarcados]]"
Data: "2026-11-11"
Tipo: Pesquisa
---

# Pesquisa: metodologias de desenvolvimento de hardware e como aplicá-las ao nosso projeto

**Pergunta:** o que fazer, quando fazer, o que pode andar em paralelo e como evitar que alguém fique ocioso, sabendo que todos são alunos com outros compromissos e bolsas.

**Alcance:** 14 buscas na web, 2 páginas lidas e 1 PDF lido em parte (Backblaze, até a página 6 de 11). As fontes são em sua maioria blogs, guias de fornecedores e artigos de profissionais. **Não encontrei estudos acadêmicos sistemáticos** que comparem as metodologias em hardware. As partes que são raciocínio meu, e não das fontes, estão marcadas como **(minha sugestão)**.

## 1. Resposta curta

Não existe uma metodologia única de hardware que resolva isso. O que as fontes sustentam é uma combinação, e ela cabe bem no nosso caso:

1. **Modelo em V (marcos de integração):** hardware e software andam em trilhas paralelas e se encontram em pontos de sincronização definidos. Para nós, esses pontos são as quintas e os marcos M0 a M3.
2. **Kanban com limite de trabalho em andamento:** mais flexível que Scrum para hardware, porque os componentes estão em estágios diferentes ao mesmo tempo.
3. **Bala traçante e esqueleto andante (*tracer bullet*, *walking skeleton*):** montar cedo uma fatia fina que funciona de ponta a ponta e atacar os maiores riscos primeiro.
4. **Firmware primeiro no PC (*dual targeting*):** escrever a lógica de forma que rode no PC e na placa, para não depender do hardware.
5. **Estágios de protótipo (Proto, EVT, DVT, PVT):** nós estamos só na fase **Proto**.

## 2. O que cada metodologia diz e o que aproveitamos

| Método | O que as fontes dizem | O que levamos para o projeto |
|---|---|---|
| **Modelo em V** | Desenvolvimento de software, elétrica e mecânica avança em paralelo conforme os detalhes do sistema ficam prontos, e os ramos de hardware e software se encontram em pontos de sincronização. Pode começar antes de as especificações do hardware estarem fechadas. Os métodos de hardware são menos desenvolvidos que os de software. | Trilhas paralelas por frente e integração só em datas fixas (quinta). Testes por nível: unidade no PC, integração com emulador, sistema com hardware real. |
| **Scrum para hardware** | É mais correto dizer "agilidade" do que um método fixo. Sprints de hardware costumam ser mais longos que os de software (um autor fala em cerca de 2 vezes). Pontos de atrito: modularizar o físico é difícil, dá trabalho adicionar função a hardware pronto, e o ciclo construir-medir-aprender é caro. | Não adotar cerimônias de Scrum. Usar o ritmo que já temos (terça sincroniza, quinta integra), que é parecido com um sprint semanal. Como nosso hardware é de prateleira, a semana é curta o bastante. **(minha sugestão)** |
| **Kanban** | Relatos de equipes de hardware que saíram do Scrum para o Kanban. Útil quando vários componentes estão em estágios diferentes. Os sprints são alinhados a marcos de hardware, e não a um grande planejamento em cascata. | Quadro do Trello com colunas de fluxo, limite de itens em andamento e coluna **Bloqueado**. |
| **Espiral (Boehm)** | Cada volta é guiada pela análise de risco: planejar, construir um protótipo, testar e usar o resultado para planejar o próximo. As demais abordagens são casos particulares dele. Não achei fonte que aplique isso a hardware ou firmware de forma direta. | Atacar primeiro o que é mais incerto (BLE, medição do eco, ponte do simulador). **(a ligação com hardware é minha sugestão)** |
| **Bala traçante e esqueleto andante (Grenning)** | Em projetos de IoT do zero há mais incógnitas que certezas, e a equipe tende a ir para as tarefas conhecidas. Adiar riscos "não termina bem". A bala traçante dá visão da solução de um problema técnico, e o esqueleto andante mostra que o conceito é viável e que a equipe consegue entregar. | O M1 já é isso: um nó real até o servidor e o estado visível. Antes dele, uma versão mínima ponta a ponta com dados do emulador. |
| **Firmware duplo alvo (*dual targeting*)** | O código roda no PC e na placa. As dependências de hardware ficam atrás de uma interface (BSP ou HAL). O ciclo no PC é mais rápido. Testar na placa continua necessário depois (compilador, endianness, desempenho). É fraco para drivers, que se cobrem com mocks e stubs de GPIO, I2C etc. | Frente de firmware escreve histerese, filtros e quadro em C puro com testes no PC desde já. O que toca registrador fica numa camada fina. |
| **Estágios Proto, EVT, DVT, PVT** | O **Proto** costuma ser feito com placas de desenvolvimento de prateleira, sem caixa, às vezes fios soltos, e raramente com unidades completas. O EVT é a primeira montagem que une forma e função. DVT e PVT validam a produção. As fontes divergem sobre sobreposição de fases. | Somos Proto. Não há EVT, DVT ou PVT neste semestre; a seção "Depois do protótipo" do roadmap cobre o produto. |
| **Caminho crítico (CPM)** | A cadeia mais longa de tarefas dependentes define o prazo mínimo. Tarefas fora dela têm folga. O caminho crítico muda conforme as tarefas atrasam, e deve ser recalculado a cada marco. Para projeto pequeno, CPM formal é exagero: basta mapear dependências e vigiar a folga. | Mapa de dependências na seção 3 e revisão a cada quinta. |

## 3. Aplicando ao nosso projeto

### 3.1 O que depende de hardware e o que não depende

**Pode começar agora, sem peça nenhuma** (faixa A):
- Contrato do quadro e da API (frentes 1, 3 e 5).
- Lógica do nó em C com testes no PC: histerese, filtros de 5 s e 90 s, montagem e leitura do quadro (frente 1).
- Emulador v0 gerando quadros (frente 5).
- Servidor esqueleto: decodificar, estado por máquina, marcar offline (frente 3).
- Site funcionando sobre uma API simulada, alimentada pelo emulador (frente 4).
- Configurar e testar o simulador de firmware, Renode ou Wokwi (frente 5).
- Licença do Altium, levantamento do laboratório e compras (frente 2).
- README de cada pasta e notas de decisão (todos).

**Precisa de hardware** (faixa B, bloqueada até as peças chegarem):
- Medir o HC-SR04 por interrupção e conferir o eco no osciloscópio.
- Divisor de tensão do eco (5 V para 3,3 V).
- UART real com o módulo BLE e configuração do módulo.
- Calibração dos tempos na bancada e montagem do 2º nó.

**Integração** (faixa C, só nas quintas): nó real até o servidor, site mostrando o estado, ensaio completo.

### 3.2 Caminho crítico

A cadeia que define o prazo é:

> peças em mãos → HC-SR04 lido no STM32 → BLE configurado → quadro saindo pelo BLE → servidor conectado por BLE (M1) → site mostrando o estado → ensaio (M2)

Tudo o que está na faixa A tem folga, **enquanto as peças não chegarem**. Quando elas chegam, a faixa B vira a crítica.

**Ponto mais urgente:** o roadmap diz que as peças precisam chegar até cerca de **16/11** para o BLE ser configurado em 19/11, e hoje é 11/11. Eu **não pesquisei prazos de entrega de componentes no Brasil** e não sei qual o prazo de cada fornecedor. As fontes que achei sobre prazos de componentes são de fornecedores e falam de peças industriais, então não servem como número para nós. A orientação delas (pedir o que tem prazo longo antes de precisar, ter alternativas) vale: **o pedido das peças é a primeira tarefa da frente 2**.

### 3.3 O M0 de quinta (12/11) como está escrito exige hardware

O critério do M0 inclui "placas e módulos em mãos" e "HC-SR04 lido por interrupção". Se as peças não estiverem na mão amanhã, o M0 falha por motivo que não depende de ninguém. **(minha sugestão)** Dividir em dois:

- **M0a (qui 12/11), sem hardware:** contrato do quadro e da API escrito, emulador v0 gerando quadros, servidor recebendo quadros do emulador, simulador de firmware definido e testado, licença do Altium pedida, pedido de peças feito.
- **M0b (quando as peças chegarem):** HC-SR04 lido e impresso na UART.

### 3.4 O que cada frente faz enquanto espera

A ideia é que ninguém fique parado esperando outra frente ou uma peça.

| Frente | Sem hardware (faixa A) | Quando o hardware chega (faixa B) |
|---|---|---|
| 1. Firmware do nó | Histerese, filtros e quadro em C com testes no PC; camada fina de hardware com interface | Leitura do HC-SR04 por interrupção; UART real |
| 2. Hardware e BLE | Compras, laboratório, licença do Altium, esquemático do nó | Montar o 1º nó, divisor, configurar o BLE, 2º nó, osciloscópio |
| 3. Servidor e API | Decodificação, estados, offline, estatísticas e recomendação com dados do emulador | Conexão BLE com `bleak` em 1 nó real |
| 4. Site | App e painel sobre a API simulada | Trocar a fonte para o servidor real |
| 5. Simulação e emulador | Simulador de firmware, emulador v0 e v1 (100 nós, perdas, nós mortos), tabela de cenários | Comparar o nó real com o simulado, calibração |

Como o emulador e a API simulada cobrem a falta de hardware, as frentes 3, 4 e 5 não precisam esperar a 1 e a 2.

## 4. Como trabalhar com pouco tempo de cada um

As fontes **não tratam de membros em tempo parcial** (a busca sobre isso voltou sem nada específico). O que segue combina o que achei sobre Kanban e sobre Brooks com raciocínio meu.

**Do que as fontes dizem**
- **Limite de itens em andamento (WIP):** os limites devem refletir tamanho da equipe, habilidades e complexidade, para ninguém ficar sobrecarregado. Uma heurística de fornecedor é começar com metade do tamanho da equipe mais um e ajustar pelos dados (para 5 pessoas, cerca de 3 a 4 itens em andamento no quadro todo). Outra orientação é começar conservador. Uma guia da Microsoft diz que quem passa do limite em 3 ou mais itens com frequência deve rever o processo ou o limite.
- **Dependências visíveis:** usar coluna **Bloqueado** e marcas de cor ou etiqueta para dependência entre cards. Registrar por card: responsável, prazo, prioridade, dependência, definição de pronto e bloqueio.
- **Lei de Brooks:** acrescentar gente a um projeto atrasado costuma atrasá-lo mais, pelo tempo de ensinar e de coordenar. McConnell lembra que isso depende de o projeto estar de fato atrasado. Uma conclusão das fontes é **fixar o trabalho e as interfaces antes de colocar mais gente**. Para nós, isso reforça o contrato do quadro e da API.

**Minhas sugestões (não vêm das fontes)**
1. **Levantar a disponibilidade real de cada um** (horas por semana, dias fixos ocupados, bolsa, provas) e planejar com margem, não com o total. O roadmap já lista "datas de provas de outras disciplinas" como pendência.
2. **Cards pequenos**, que caibam em uma ou duas sessões curtas, para encaixar entre outros compromissos.
3. **Limite de 2 cards por pessoa em andamento.** O limite de equipe das fontes (3 a 4 no quadro) me parece baixo para 5 donos de frente trabalhando em paralelo. Testem e ajustem na S1.
4. **O item do caminho crítico vai para quem tem mais horas na semana** e tem sempre um apoio, para o caso de uma prova ou um compromisso de bolsa.
5. **Trabalho assíncrono por padrão**, com o repositório e o Trello como fonte de verdade. Os encontros de terça e quinta ficam para sincronizar e integrar, não para quem trabalha sozinho.
6. **Fila "se travar, faça isto":** cada pessoa deixa 2 ou 3 cards da faixa A no topo da sua fila, prontos para pegar quando a peça ou a dependência não chegar.
7. **Revisar o caminho crítico toda quinta**, como as fontes recomendam a cada marco.

## 5. O que não foi verificado

- Estudos acadêmicos sobre metodologias de hardware ou sobre equipes de estudantes: não encontrei.
- Prazos reais de entrega e disponibilidade das peças (Blue Pill, HM-10 ou JDY-23, HC-SR04, ST-Link) no Brasil, e o que o laboratório tem.
- A disponibilidade de cada integrante: sem esse dado, a divisão de carga é só uma proposta.
- O PDF da Backblaze foi lido só até a página 6 de 11, então não li a parte sobre os desafios específicos de hardware.
- A seção sobre estágios (EVT, DVT, PVT) vem de resumos de busca, não da leitura das páginas.
- Não achei fonte que aplique o modelo espiral a firmware ou hardware; a ligação é minha.

## Fontes

- [Agile em projetos combinados de hardware e software (Cambridge)](https://www.cambridge.org/core/services/aop-cambridge-core/content/view/5978631E6BADD6EA7E8559938852B8D5/S2732527X22000165a.pdf/guidance_on_application_of_agile_in_combined_hardware_and_software_development_projects.pdf)
- [Agile for Hardware Development (Colab)](https://www.colabsoftware.com/agile-for-hardware-development)
- [Application of Scrum Methods to Hardware Development (Backblaze)](https://www.backblaze.com/blog/wp-content/uploads/2015/08/Scrum-for-Hardware-Development-V3.pdf)
- [Agile Hardware Development (ProductFlo)](https://productflo.io/blog/agile-hardware-development-unlocking-innovation-in-product-development-methods)
- [MAHD: Agile for Hardware (e-book)](https://agileforhardware.org/wp-content/uploads/2018/07/An-Intro-to-MAHD-Ebook-Final-7_25_18.pdf)
- [Modelo em V e teste de software embarcado (Code Intelligence)](https://www.code-intelligence.com/blog/everything-about-v-model-and-testing-embedded-software)
- [V-Model (itemis)](https://www.itemis.com/en/glossary/v-model/)
- [V-Model e a vida do desenvolvimento de produto (NI)](https://www.ni.com/en/solutions/aerospace-defense/electromechanical-systems-test/accelerating-the-product-development-lifecycle-with-faster-test-.html)
- [EVT, DVT e PVT (OpenBOM)](https://openbom.com/blog/evt-vs-dvt-vs-pvt-understanding-the-stages-of-product-development)
- [Hardware development lifecycle (Duro)](https://www.durolabs.co/blog/hardware-development-lifecycle/)
- [Proto, EVT e PVT no Embedded Artistry](https://embeddedartistry.com/fieldmanual-terms/engineering-validation-and-test/)
- [Simulando software embarcado (Beningo)](https://www.beningo.com/simulating-embedded-software-3-simple-tips-for-better-results/)
- [5 maneiras de uma HAL transformar seus projetos (Design News)](https://www.designnews.com/embedded-systems/5-surprising-ways-a-hardware-abstraction-layer-hal-can-transform-your-projects)
- [Embedded systems testing guide (HelpMeTest)](https://helpmetest.com/blog/embedded-systems-testing-guide/)
- [Comparação de simuladores Cortex-M: QEMU, Renode, Keil](https://industrialmonitordirect.com/blogs/knowledgebase/arm-cortex-m-simulators-qemu-renode-keil-comparison)
- [Dual targeting e prototipagem ágil de software embarcado (state-machine.com)](https://www.state-machine.com/dual-targeting-and-agile-prototyping-of-embedded-software-on-windows)
- [Para TDD embarcado, não se preocupe tanto com testar no alvo (Chernosky)](https://matthew-chernosky.squarespace.com/blog/for-embedded-tdd-dont-worry-so-much-about-testing-on-the-target)
- [O que aprendi no curso remoto de TDD de James Grenning (Embedded Artistry)](https://embeddedartistry.com/blog/2018/09/18/what-i-learned-from-james-grennings-remote-tdd-course/)
- [Attack IoT System Unknowns with Tracer Bullets (Grenning, Embedded Online Conference)](https://embeddedonlineconference.com/session/Attack_IoT_System_Unknowns_with_Tracer_Bullets)
- [Modelo espiral (Wikipedia)](https://en.wikipedia.org/wiki/Spiral_model)
- [Caminho crítico (ClickUp)](https://clickup.com/learn/topic/project-management/terms/critical-path/)
- [Caminho crítico (TeamGantt)](https://www.teamgantt.com/blog/critical-path)
- [Caminho crítico (Wrike)](https://www.wrike.com/projectmanagement/09/01/2010/Critical-Path-is-Easy-as-1-2-3)
- [Limites de WIP (Adobe)](https://business.adobe.com/blog/basics/wip-limits)
- [Kanban capacity planning (The Digital Project Manager)](https://thedigitalprojectmanager.com/project-management/kanban-capacity-planning/)
- [Boas práticas de Kanban (Azure Boards)](https://learn.microsoft.com/id-id/previous-versions/azure/devops/boards/boards/best-practices-kanban?view=tfs-2017)
- [Lei de Brooks (Wikipedia)](https://en.wikipedia.org/wiki/Brooks%27s_law)
- [É sempre ruim acrescentar gente a um projeto atrasado? (Electronic Design)](https://www.electronicdesign.com/archive/article/21760483/is-it-always-a-bad-idea-to-add-resources-to-a-late-project)
- [Guia do módulo HM-10 (Martyn Currey)](https://www.martyncurrey.com/?p=4463)
- [Prazos longos de componentes e riscos de EOL (Suntsu)](https://suntsu.com/blog/strategic-fixes-for-long-lead-times/)
