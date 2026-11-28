---
Disciplina: "[[TI0148_Sistemas_Embarcados]]"
Data: "2026-10-23"
Tipo: Pesquisa
---

# Pesquisa: como simular o sistema inteiro

Complementa [[Pesquisa - Altium para simulação]]. Esta nota cobre **todas as partes** do projeto: firmware do nó (STM32F103), sensor HC-SR04, módulo BLE, ponte com o PC, servidor, emulador e site.

**Alcance:** cerca de 12 buscas na web e leitura de 6 páginas oficiais (Renode, Wokwi, Bumble) em 23/10/2026. Não é exaustiva. O que não consegui confirmar está na seção 6.

## 1. Resumo

- **O firmware do nó roda em simulador.** Três opções reais: **Renode** (Blue Pill listada oficialmente), **Wokwi** (Blue Pill com o chip F103C8 e HC-SR04 nativo) e **Proteus** (F103C6, só Windows).
- **O que nenhum simulador cobre:** o módulo BLE (HM-10/JDY-23) e o eco real do HC-SR04. Ambos precisam ser imitados.
- **O Altium não executa firmware** (sem evidência em fontes oficiais), então serve ao esquemático e ao circuito.
- **Servidor, emulador e site** são software comum e se testam no PC.
- **Correção de uma dúvida anterior:** o Renode **tem** a Blue Pill F103 na lista oficial (`stm32f103.resc`).

## 2. Cobertura por parte do sistema

| Parte | Altium | Proteus | Renode | Wokwi | No PC |
|---|---|---|---|---|---|
| Esquemático e circuito do nó | **Sim** | Parcial | Não | Não | Não |
| Firmware STM32F103 | Não (sem evidência) | Sim (C6) | Sim | Sim (C8) | Só a lógica, compilada no PC |
| HC-SR04 (Trig e Eco) | Fonte de pulso imita | Só biblioteca de terceiros | Não achei modelo | **Parte nativa** | Não se aplica |
| UART do nó até o PC | Não se aplica | COMPIM (Windows) | **Socket TCP ou pty** | Não verificado | Sim |
| Módulo BLE | Não | Não | Não | Não | Bumble (parcial, não verificado com bleak) |
| Servidor, site, emulador | Não | Não | Não | Não | **Sim** |

## 3. O que encontrei em cada ferramenta

### Proteus
- Lista oficial de STM32 (revenda, datasheet reproduzido): **F103C4, C6, R4, R6, T4, T6**. **C8 não aparece.** A Blue Pill real é C8, então no Proteus usa-se o C6, com biblioteca comunitária e código compilado para C6.
- O VSM roda o **mesmo arquivo HEX** que o chip real; com arquivos de objeto a depuração é mais rica.
- **HC-SR04:** não há modelo nativo. A biblioteca de terceiros de Proteus 8 que achei **não temporiza eco real**: deriva a distância de botões.
- **Ponte com o PC:** o Proteus usa o modelo **COMPIM**, que precisa de um **par de portas virtuais** (com0com ou VSPD, no Windows). O programa do PC abre a outra ponta. A porta não pode estar aberta nos dois lados.
- **Linux:** não achei declaração oficial. Os relatos de uso com **Wine** são de 2014 a 2021 e falam de falhas de instalação e travamentos. **Risco real para quem usa Linux.**

### Renode (código aberto; Linux, Windows e Mac)
- A tabela oficial de placas lista a **STM32F103 Blue Pill** (`stm32f103.resc`).
- A plataforma do F103 define: **USART1 a 5, GPIO A a G, TIM1 a 14, DMA (modelo de variante G0), I²C1 e 2, EXTI (modelo de F4) e AFIO**. O RCC é parcial.
- **Não define:** **ADC, SPI**, RTC, watchdogs, USB, CAN. O nosso nó não usa ADC nem SPI, então não pesa.
- **UART para fora:** `emulation CreateServerSocketTerminal 12345 "term"` e `connector Connect sysbus.usart1 term` expõem a UART em um **socket TCP**, em qualquer sistema. Em Linux e Mac também há **pty**. Um script Python lê a porta como se fosse o nó.
- **Lacunas:** não achei modelo do HC-SR04 e não verifiquei se o modelo de timer suporta **captura de entrada** com a precisão necessária.

### Wokwi (simulador no navegador e no VS Code)
- A Blue Pill do Wokwi é o **STM32F103C8** (o chip real), 72 MHz, 64 KB de flash e 20 KB de RAM.
- **Simulados:** núcleo, SysTick, GPIO, **USART**, I²C, SPI, **timers TIM1 a 4**, EXTI, RCC, AFIO, depuração GDB.
- **Parciais:** ADC1 só conversão básica; ADC2 ausente. **Não implementados:** **DMA, IWDG, PWR, RTC.**
- **HC-SR04 nativo:** Trig com pelo menos 10 µs; a largura do pulso do Eco é `µs ÷ 58 = cm`; o controle é um **cursor de 2 a 400 cm**.
- **Automação:** o Wokwi CI e a CLI usam **cenários em YAML** (`wait-serial`, `set-control`, `delay`). Não achei o nome do controle do HC-SR04 nesses cenários.
- **Firmware:** `wokwi.toml` aponta para `.elf`, `.hex` ou `.bin`.
- **Lacunas:** captura de entrada de timer não documentada; não verifiquei como a UART do Wokwi chega a um programa externo no PC.

### QEMU
- Sem máquina para F103 na versão principal. A mais próxima é a `stm32vldiscovery`, que usa o SoC **F100** (24 MHz) com periféricos limitados. Um patch de Blue Pill de 2018 não aparece concluído. **Não recomendado.**

### Altium
- Simulador SPICE com ponto de operação, varredura DC, transiente e varredura AC. **Sem evidência de executar firmware.** O CoDesigner (Ansys) é de térmica e integridade de sinal, não de firmware. Detalhes em [[Pesquisa - Altium para simulação]].

### BLE no PC
- **Bumble** (pilha Bluetooth em Python): "para emulação, teste e experimentação", com **controlador virtual** e servidor GATT. No Linux pode se ligar ao sistema por **VHCI** (`/dev/vhci`, se o driver estiver habilitado). Só suporta **controladores virtuais, não hosts virtuais**, e o projeto é descrito como ainda incompleto.
- Um periférico BLE falso (tipo HM-10) com Bumble, visto pelo `bleak` do servidor, é um caminho **plausível, mas não verificado**.

## 4. Arquitetura de simulação recomendada

Em camadas, da mais barata à mais fiel:

1. **Lógica do nó no PC.** A máquina de estados (histerese, 5 s, 90 s) escrita em C separado do hardware e compilada no PC, com testes unitários. É a camada mais barata e a que mais pega erro. *(Prática geral de engenharia, não vem das fontes acima.)*
2. **Servidor, emulador e site no PC.** O servidor tem uma **fonte de eventos intercambiável**: BLE real, socket TCP ou emulador. Relógio injetável para acelerar o teste.
3. **Firmware no simulador.** O nó roda em Renode, Wokwi ou Proteus; a UART sai por socket ou porta virtual para o mesmo servidor. O sensor é imitado.
4. **Bancada real.** 2 a 3 nós com BLE de verdade. O BLE só se valida aqui.

**Em paralelo:** Altium para esquemático e circuito do nó.

**Dica de projeto:** medir o Eco com **interrupção nas duas bordas e um contador livre**, em vez de depender de captura de entrada do timer. Fica mais portátil entre simuladores. *(Recomendação minha, a validar no teste.)*

## 5. Qual simulador escolher

| Situação | Sugestão |
|---|---|
| Quem usa **Linux** | **Renode** (script e CI) ou **Wokwi** (rápido e visual). O Proteus é só Windows e o Wine tem histórico ruim. |
| Quem usa **Windows** | Proteus com F103C6 (o do professor nos exemplos) ou os acima |
| Para **automatizar testes** (CI) | Renode ou Wokwi CI |
| Para **demonstrar** visualmente | Wokwi ou Proteus |

**Sugestão:** adotar o **Renode como principal** (livre, multiplataforma, UART por socket) e o **Wokwi como alternativa visual** com HC-SR04. Manter o Proteus só se o professor exigir, e para quem tiver Windows. Confirmar com o professor.

## 6. Não verificado

- Se o modelo de timer do Renode e do Wokwi suporta captura de entrada com a precisão do eco.
- Se existe modelo do HC-SR04 para o Renode (ou como imitá-lo bem).
- Como a UART do Wokwi chega a um programa externo no PC.
- Se o Proteus **oficial** hoje lista o C8, e se funciona em Wine atual.
- Se o Altium 25 e 26 mudaram algo sobre firmware (as notas oficiais não foram lidas).
- Se Bumble com VHCI e bleak funcionam juntos para um periférico BLE falso.
- Qual sistema operacional cada integrante da equipe usa.

## 7. Testes de viabilidade (1 a 2 horas cada)

1. **Renode:** carregar a Blue Pill (`stm32f103.resc`), firmware que imprime pela UART, expor em socket e ler com um script Python.
2. **Wokwi:** Blue Pill com HC-SR04 e firmware que mede o Eco e imprime a distância; mexer no cursor e conferir.
3. **Proteus (se houver Windows):** F103C6, COMPIM e par virtual com um script Python.
4. **Altium:** circuito do Eco (fonte de pulso e divisor de 5 V para 3,3 V).
5. **Bumble (opcional):** periférico BLE falso visto por `bleak`.

## Fontes

- [Renode: supported boards](https://renode.readthedocs.io/en/latest/introduction/supported-boards.html)
- [Renode: plataforma stm32f103.repl](https://raw.githubusercontent.com/renode/renode/master/platforms/cpus/stm32f103.repl)
- [Renode: UART integration](https://renode.readthedocs.io/en/latest/host-integration/uart.html)
- [Wokwi: STM32 Blue Pill](https://docs.wokwi.com/parts/board-stm32-bluepill)
- [Wokwi: HC-SR04](https://docs.wokwi.com/parts/wokwi-hc-sr04)
- [Wokwi: automation scenarios](https://docs.wokwi.com/wokwi-ci/automation-scenarios)
- [Wokwi: wokwi.toml](https://docs.wokwi.com/vscode/project-config)
- [Proteus VSM para ARM Cortex-M3 (datasheet)](https://cdn.robotshop.com/media/l/lab/rbd-lab-08/pdf/proteus-vsm-software-arm-cortex-m3-datasheet.pdf)
- [Proteus: Blue Pill (STM32F103C6)](https://deepbluembedded.com/stm32-proteus-library-bluepill-simulation-stm32f103c6/)
- [Proteus: modelo de porta serial e COMPIM](https://www.virtual-serial-port.org/article/com-port-in-proteus/)
- [Proteus no Wine (relatos de falha)](https://forum.winehq.org/viewtopic.php?p=96395)
- [Biblioteca HC-SR04 para Proteus 8](https://electronicstree.com/?p=7868)
- [Bumble: Python Bluetooth stack](https://google.github.io/bumble)
- [Bumble: transporte VHCI](https://google.github.io/bumble/transports/vhci.html)
- [QEMU: stm32vldiscovery](https://qemu.googlesource.com/qemu/+/refs/heads/block/hw/arm/stm32vldiscovery.c)
- [Altium: simulação de sinais mistos](https://www.altium.com/documentation/altium-designer/circuit-simulation)
- [Fórum Fedevel: firmware no Altium](https://courses.fedevel.com/forum/altium-designer/21085-firmware-simulation-of-a-uc-in-altium-is-it-possible-how)
