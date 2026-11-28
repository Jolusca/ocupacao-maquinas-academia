---
Disciplina: "[[TI0148_Sistemas_Embarcados]]"
Data: "2026-11-08"
Tipo: Plano
---

# Plano comprimido (início em 09/11/2026)

O [[Roadmap de Desenvolvimento]] original tinha 7 semanas e terminava em 11/12. Deslocado 14 dias, o M3 ia para 17/12 e a entrega para 24/12, depois do fim do semestre (11/12; avaliações finais de 12 a 18/12, notas até 19/12). Este plano começa na **segunda 09/11** e fecha a entrega na **quinta 10/12**: 4 semanas de trabalho mais a semana final. O quadro do Trello segue este plano.

## Marcos

| Marco | Data | Critério |
|---|---|---|
| M0 | qui 12/11 | Material em mãos, simulador escolhido e testado, Altium com licença, contrato do quadro e da API escrito, emulador v0 gerando quadros |
| M1 | qui 26/11 | Ponta a ponta: um nó real mede, decide, envia por BLE, e o servidor mostra o estado |
| M2 | qui 03/12 | Protótipo completo em ensaio: nós reais, app e painel, emulador de 100 nós, tabela de cenários testada |
| M3 | ter 08/12 | Protótipo congelado, roteiro ensaiado, vídeo de reserva gravado, professor avisado |
| Entrega | qui 10/12 | Relatório e código entregues |

A reunião com as empresas é marcada pelo professor depois do M3 e pode cair na quinta 10/12 ou nas avaliações finais (12 a 18/12).

## Semana a semana

Encontros às terças e quintas, 14h. A sexta 20/11 (Consciência Negra) não tem aula e não cai em dia de encontro.

| Semana | Prazos | Entregas |
|---|---|---|
| **S1** 9 a 13/11 | ter 10/11 e qui 12/11 (M0) | Grupo de WhatsApp, levantar e comprar o material, lista de material ao professor, licença do Altium, repositório; simulador definido, contrato do quadro e da API, nó mede o HC-SR04, emulador v0, servidor esqueleto |
| **S2** 16 a 19/11 | qui 19/11 | Máquina de estados do nó com testes no PC, firmware v1, servidor decodifica e marca offline, módulo BLE configurado, nó simulado nos cenários básicos |
| **S3** 23 a 26/11 | ter 24/11 e qui 26/11 (M1) | Servidor conecta por BLE a 1 nó real, estatísticas e recomendação v1, emulador v1 com 100 nós, API, esquemático no Altium, 2º nó, teste ponta a ponta |
| **S4** 30/11 a 03/12 | ter 01/12 e qui 03/12 (M2) | App do frequentador e painel da gestão, alerta de manutenção, calibração, tabela de cenários, carga com 100 nós, robustez, ensaio completo, funcionalidades congeladas, roteiro e material para as empresas |
| **S5** 07 a 10/12 | ter 08/12 (M3) e qui 10/12 | Correções do site, vídeo de reserva, ensaio final, professor avisado; relatório, ajustes finais e entrega |

## O que foi cortado para caber

Segue a ordem de cortes do roadmap original.

| Corte | O que mudou | Como desfazer |
|---|---|---|
| Ranking e horários de pico (corte nº 2) | Card foi para o Icebox. Saíram dois itens do checklist do painel da gestão ("Ranking de mais e menos usadas" e "Horários de pico") e um da tabela de cenários | Mover o card de volta ao Backlog e recolocar os itens |
| 3º nó (corte nº 3) | O card virou "Montar o 2º nó (3º só se sobrar tempo)" | Voltar o título |
| Simulação do circuito no Altium (corte nº 1) | Já estava no Icebox; fica só o esquemático | Mover o card do Icebox |
| Emulador em modo aleatório (corte nº 4) | Já estava no Icebox | Mover o card do Icebox |

O painel da gestão fica com ocupação em tempo real, uso por máquina e alertas de manutenção. A proposta citava o ranking das máquinas mais e menos usadas, então vale **avisar o professor** desse corte.

### Cortes de 13/11/2026 (escopo reduzido)

Depois que o professor indicou a Nucleo H533RE do laboratório e o protótipo ficou com 2 nós em protoboards com fonte de mesa, o escopo da disciplina encolheu. O que foi cortado vai para a fase da bolsa, se o projeto for aprovado. Detalhes e a lista de cards em [[Corte de Escopo - Cards do Trello]].

| Corte | O que mudou |
|---|---|
| Simulação do firmware (Renode, Wokwi, Proteus) e Altium | Cards de simulação arquivados; o nó roda na protoboard real e a lógica é testada em C no PC |
| Site completo | App do frequentador e painel da gestão viram uma página web simples |
| Emulador de 100 nós (v1), modo aleatório e teste de carga | Fica só o emulador v0 |
| Alerta de manutenção, estatísticas completas e API completa | Ficam só o estado, a recomendação básica e uma API mínima |
| 3º nó | Fora do plano; o protótipo tem 2 nós |
| Material para as empresas | Arquivado; a apresentação atual serve. Reabrir se o professor marcar a reunião |

Marcos afetados: o M0 não exige mais simulador nem Altium, e o M2 passa a exigir "2 nós reais" e "página web simples".

## Riscos específicos do plano comprimido

- **Peças:** a configuração do módulo BLE está prevista para qui 19/11. As peças compradas em 10/11 precisam chegar até cerca de 16/11. O plano B de nós simulados continua valendo.
- **Semana S2 curta:** só terça 17/11 e quinta 19/11, por causa do feriado de sexta.
- **Sem folga antes da entrega:** a reserva é a semana de avaliações finais (12 a 18/12), que não deve ser planejada como trabalho.
- **Cards demais por semana:** S1 e S4 têm 11 cards cada. Se a S1 atrasar, puxar da S2 só o que for essencial.
