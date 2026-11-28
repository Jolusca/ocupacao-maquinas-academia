---
Disciplina: "[[TI0148_Sistemas_Embarcados]]"
Data: "2026-11-08"
Tipo: Roadmap
---

# Roadmap de Desenvolvimento

> Versão em PDF com o gráfico de cronograma: `Roadmap de Desenvolvimento.pdf` (gerado do `.tex`). **Plano comprimido, de 09/11 a 10/12/2026**, atualizado em 08/11/2026. Resumo das mudanças em [[Plano Comprimido]].

## Premissas

- O desenvolvimento ocupa o **tempo restante do semestre** e continua valendo como trabalho da disciplina.
- Quando o protótipo estiver pronto, o professor marca a **reunião com as empresas**. O objetivo é chegar a esse protótipo antes da entrega.
- **O projeto começa em 09/11/2026 e o semestre termina em 11/12/2026** (calendário da UFC). As avaliações finais vão de 12 a 18/12 e a síntese de notas, até 19/12. O plano original tinha 7 semanas, a partir de 26/10; como o início ficou para 09/11, ele foi **comprimido para 4 semanas de trabalho mais a semana final** (5 semanas, de 09/11 a 10/12), com os cortes da seção "Prioridades e cortes".
- Dia sem aula no período: 20/11 (Consciência Negra, sexta-feira), que não cai em dia de encontro. Os demais dias ficam disponíveis para o projeto.
- Equipe de 5 pessoas, sem responsáveis definidos por frente. O roadmap lista pacotes de trabalho, não nomes.
- A equipe se encontra às **terças e quintas às 14h**, no horário da aula de Sistemas Embarcados, que está livre para o projeto, com acesso a bancada e laboratório (seção "Encontros da equipe").
- O acompanhamento é feito no **quadro do Trello** do projeto, que segue as datas deste documento.

## Marcos

| Marco | Data-alvo | Critério de conclusão |
|---|---|---|
| M0 | qui 12/11 (fim da S1) | Placas e módulos em mãos (do laboratório ou comprados), Altium, Renode e Wokwi testados, quadro serial e API escritos, emulador v0 gerando quadros |
| M1 | qui 26/11 (fim da S3) | Ponta a ponta mínimo: 1 nó real envia por BLE ao servidor, que mostra o estado da máquina |
| M2 | qui 3/12 (fim da S4) | Protótipo completo em ensaio: nós reais, site (app e painel), emulador de 100 nós, cenários testados; funcionalidades congeladas |
| M3 | ter 8/12 (S5) | **Protótipo pronto e congelado**, com roteiro de demonstração ensaiado e vídeo de reserva. Avisar o professor para marcar a reunião com as empresas |
| Entrega | qui 10/12 (S5) | Relatório e código entregues. O semestre termina em 11/12 |

## Encontros da equipe

Os encontros são às **terças e quintas, às 14h**, no horário da aula. São **dois por semana**, então o plano separa o que se faz juntos do que se faz entre eles.

- **Terça: sincronização.** Revisar o que ficou pronto, fixar a meta da semana, dividir os pacotes de trabalho e destravar dependências.
- **Quinta: integração e demonstração interna.** Juntar as partes, testar o critério de pronto da semana e registrar as pendências.
- **Bancada e laboratório:** usar os encontros para montar, ligar e depurar o hardware (por exemplo, o osciloscópio para o eco do HC-SR04 e o quadro serial). Antes de comprar, levantar o que o laboratório já tem (placas STM32, gravador ST-Link, módulos Bluetooth, sensores).
- **Entre os encontros:** cada pessoa avança no seu pacote (firmware, BLE e servidor, site, emulador, simulação e documentação), com o código no repositório compartilhado.

| Sem. | Terça 14h | Quinta 14h | Observação |
|---|---|---|---|
| S1 | 10/11: início, divisão dos pacotes, pedidos conferidos | 12/11: marco M0 | Antes de terça, consultar o laboratório sobre o que há disponível e fazer os pedidos do que faltar |
| S2 | 17/11: nó e servidor básico | 19/11: BLE configurado e nó simulado | Sexta 20/11 é feriado; a semana tem só dois encontros |
| S3 | 24/11: emulador v1 | 26/11: marco M1 (nó real até o servidor) | |
| S4 | 1/12: calibração na bancada | 3/12: marco M2 (ensaio completo) | Congelar as funcionalidades depois do M2 |
| S5 | 8/12: marco M3 e ensaio final | 10/12: entrega | Avisar o professor após o M3; fim do semestre em 11/12 |

## Plano semana a semana

| Semana | Entregas | Critério de pronto |
|---|---|---|
| **S1** 9/11 a 13/11, fundações | Grupo de WhatsApp com o professor; levantamento do que o laboratório já tem, compra do que faltar (placas, módulos BLE, HC-SR04, ST-Link) e lista de material ao professor; licença do Altium pedida; repositório de código; simulador escolhido e testado (UART por socket e HC-SR04); contrato do quadro e da API; nó mínimo; emulador v0; servidor esqueleto | **M0** (qui 12/11): HC-SR04 lido por interrupção e contador e impresso na UART; servidor recebe quadros do emulador |
| **S2** 16/11 a 19/11 (feriado 20/11), nó e servidor básico | Histerese e filtros (5 s e 90 s) com testes no PC; firmware v1 com quadro, sequência e sinal de vida; servidor com decodificação, estado por máquina e *offline*; módulo BLE configurado; nó simulado nos cenários básicos | Cenários passante, treino, descanso e liberação corretos no simulador; quadro saindo pelo módulo BLE |
| **S3** 23/11 a 26/11, BLE e ponta a ponta | Servidor conecta por BLE a 1 nó real; estatísticas e recomendação v1; emulador v1 com 100 nós, perdas e nós mortos; API (estado, recomendação, estatísticas, alertas); esquemático do nó no Altium; 2º nó montado | **M1** (qui 26/11): nó real → servidor → estado visível |
| **S4** 30/11 a 3/12, site, testes e congelamento | Site (app do frequentador e painel da gestão); alerta de manutenção preventiva; calibração dos tempos na bancada; tabela de cenários; carga com 100 nós emulados; robustez (reconexão BLE, nó offline); ensaio completo; funcionalidades congeladas; roteiro de demonstração e material para as empresas | **M2** (qui 3/12): protótipo completo em ensaio e congelado |
| **S5** 7/12 a 10/12, demo e entrega | Correções do site; vídeo de reserva; ensaio final; professor avisado; relatório da disciplina; ajustes finais; entrega. Reunião com as empresas, marcada pelo professor (quinta 10/12 ou avaliações finais de 12 a 18/12) | **M3** (ter 8/12): protótipo pronto, avisar o professor. Entrega na quinta 10/12 |

## Prioridades e cortes

- **Essencial:** nó com filtros, BLE real, servidor com estados e *offline*, recomendação e app do frequentador.
- **Importante:** painel da gestão (ocupação, uso e frequência por máquina), alerta de manutenção preventiva e emulador de 100 nós.
- **Se sobrar tempo:** terceiro nó, ranking e horários de pico, simulação do circuito no Altium e emulador em modo aleatório.
- **Fora do semestre:** nó de produto com STM32WB e visão computacional.

Para caber no semestre, **os quatro cortes do roadmap original já foram aplicados**: (1) simulação do circuito no Altium, mantendo só o esquemático; (2) ranking e horários de pico, mantendo ocupação e uso por máquina; (3) terceiro nó; (4) emulador aleatório, mantendo o roteirizado. A proposta citava o ranking das máquinas mais e menos usadas, então **o corte (2) deve ser comunicado ao professor**. Se o prazo ainda apertar, os próximos cortes são decididos com o professor.

## Protótipo pronto: o que precisa funcionar na reunião

- 2 nós reais (3º se sobrar tempo) enviando por BLE e refletidos no site em segundos.
- Cenários do nó corretos ao vivo: passante ignorado, treino ocupa, descanso mantém, liberação volta a livre.
- App do frequentador mostrando a próxima máquina da rotina.
- Painel da gestão com ocupação, uso e frequência por máquina e alerta de manutenção.
- Emulador mostrando a escala de 100 equipamentos.
- Roteiro de 5 a 7 minutos ensaiado e **vídeo de reserva** para o caso de falha ao vivo.

## Riscos

| Risco | Mitigação |
|---|---|
| Atraso na entrega dos componentes | Consultar antes o laboratório e comprar já o que faltar (S1). As peças precisam chegar até cerca de 16/11 para o módulo BLE ser configurado na S2 (19/11). Plano B com nós simulados e o mesmo servidor e site |
| Módulo BLE barato instável | Testar 1 antes de comprar os demais; avaliar outro módulo se falhar |
| Ponte entre o simulador e o PC (socket ou serial) não funcionar | Teste na S1; usar a bancada real como principal |
| Altium não simular firmware | Usar só para esquemático e circuito; firmware no Renode ou no Wokwi (pesquisa já feita) |
| Curva de aprendizado de STM32 e BLE | Começar pelo nó mínimo na S1; revisar em dupla |
| Prazo curto: sem folga antes da entrega (10/12) | Os quatro cortes já aplicados; a reserva é o período de avaliações finais, que não deve ser planejado como trabalho; se a S1 atrasar, puxar da S2 só o que for essencial |
| Falha na demonstração ao vivo | Vídeo de reserva e emulador como apoio |
| Poucos encontros presenciais (2 por semana; a S2 tem só 2 por causa do feriado de 20/11) | Dividir o trabalho para andar entre os encontros e usar os encontros para integrar e destravar |
| Provas de outras disciplinas e eventos | Levantar as datas na S1 e ajustar as semanas apertadas; a reunião com as empresas pode cair nas avaliações finais (12 a 18/12) |

## Depois do protótipo

1. **Reunião com as empresas**, marcada pelo professor quando o M3 for atingido (terça 8/12), na quinta 10/12 ou no período de avaliações finais (12 a 18/12).
2. **Piloto** em uma academia interessada, para validar fora do ambiente ideal.
3. **Produto:** nó STM32WB com ToF, a bateria, com *BLE advertising*.
4. **Visão computacional** (PDI e ML), se houver investimento.

## A confirmar

- **Campus e calendário aplicável** (o plano usa o de Fortaleza; em Sobral o feriado municipal e outros eventos caem em outras datas).
- Datas de provas de outras disciplinas da equipe.
- Se o professor aceita o corte do ranking e dos horários de pico no painel da gestão.
- Se o professor aceita 2 a 3 nós reais com emulador, a Blue Pill como STM32 e o Altium para circuito com o Renode e o Wokwi para firmware.
