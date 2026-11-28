---
Disciplina: "[[TI0148_Sistemas_Embarcados]]"
Data: "2026-10-22"
Tipo: Pesquisa
---

# Pesquisa: Altium Designer como ambiente de simulação do projeto

**Contexto:** o professor recomendou o Altium para a simulação e disse que, como alunos, temos acesso. Ele pediu que as limitações fossem pesquisadas a fundo.

**Alcance desta pesquisa:** 4 buscas na web e leitura de 3 páginas oficiais do Altium (data: 22/10/2026). Não é exaustiva. O que não consegui confirmar está na seção "Não verificado".

## 1. O que o simulador do Altium faz

- É um simulador **de circuitos de sinais mistos** (analógico, digital e misto), baseado em SPICE.
- Totalmente compatível com **SPICE3f5**; suporta **XSPICE**; PSpice e LTspice têm **suporte parcial** (desde o Altium Designer 21).
- Análises que a página oficial lista: **transiente** (tipo osciloscópio) e **varredura AC** (resposta em frequência).
- Já vem instalado (extensão "Mixed Simulation").
- Cada componente precisa de um **modelo de simulação** associado, com fontes de sinal e sondas definidas.

## 2. Limitações encontradas

- **Não há evidência de que o Altium execute firmware de microcontrolador.** A documentação oficial lida não menciona isso, e um fórum de usuários diz que o Altium não faz simulação de microcontrolador (fórum antigo, a confirmar para as versões atuais).
- **Modelos criptografados** de fabricantes (PSpice, LTspice, HSpice, TINA-TI) só funcionam no simulador de origem. O Altium não os decifra.
- **Erros de modelo tipo "A"** ao importar modelos do LTspice (primitivas que o Altium não tem). Modelos OTA e SCHMITT do LTspice não são importáveis.
- **Mapeamento de pinos** de modelo pode falhar sem aviso (fonte secundária).
- **Circuitos muito grandes** podem esbarrar em limite de processamento (fonte secundária, a confirmar).
- **STM32:** a ST publica modelos **IBIS** de alguns chips (úteis para integridade de sinal), mas modelos **SPICE** do microcontrolador são raros. Os relatos são de fóruns, de anos diferentes.

## 3. Licença de estudante

- Gratuita, descrita como **totalmente funcional**, para estudante com **e-mail institucional**.
- Se a instituição não for reconhecida automaticamente, pode ser pedido comprovante de matrícula e carteirinha ao suporte do Altium.
- Renovável anualmente enquanto for estudante (a página também fala em reaplicar após 6 meses, então o prazo exato está ambíguo).
- A página consultada não cita limitação de recursos nem proibição de uso comercial.

## 4. O que isso significa para o projeto

| Parte do projeto | Dá para fazer no Altium? |
|---|---|
| **Esquemático e PCB do nó** (STM32F103, HC-SR04, módulo BLE, alimentação) | Sim. É o ponto forte da ferramenta. |
| **Circuito analógico do nó** (divisor de tensão do eco do HC-SR04, regulador, filtros) | Sim, no simulador de circuitos. O HC-SR04 não tem modelo SPICE, então se imita o eco com uma fonte de pulso. |
| **Firmware** (histerese, temporizadores, quadro serial) | **Não, pelo que achei.** Precisa de outro ambiente: Proteus (STM32F103C6), Wokwi ou o próprio hardware. |
| **Rádio BLE** | Nenhum simulador cobre. Troca-se por serial. |
| **Servidor, site e emulador de 100 nós** | Fora do escopo do Altium (software). |

**Proposta:** usar o **Altium para o esquemático e a simulação do circuito do nó**, e o **Proteus (F103C6) para o firmware**. Confirmar com o professor se isso atende à recomendação dele.

## 5. Não verificado

- Se as versões mais recentes do Altium (2025 e 2026) trazem alguma simulação de firmware ou cossimulação com microcontrolador.
- Se há modelo SPICE ou símbolo pronto de STM32F103 e de módulos BLE nas bibliotecas do Altium.
- Se a UFC é reconhecida automaticamente para a licença de estudante.
- Se o professor quer só esquemático e circuito ou também o firmware dentro do Altium.

## 6. Teste de viabilidade sugerido (1 a 2 horas)

1. Pedir a licença de estudante com o e-mail institucional (pode levar 1 ou 2 dias).
2. Montar um esquemático mínimo: fonte de pulso (imita o eco), divisor de tensão de 5 V para 3,3 V e um resistor de carga.
3. Rodar a simulação transiente e verificar a tensão no pino do STM32.
4. Procurar o símbolo do STM32F103 nas bibliotecas.

## Fontes

- [Altium: Mixed-Signal Circuit Simulation](https://www.altium.com/documentation/altium-designer/circuit-simulation)
- [Altium KB: Understand SPICE models supported in Altium](https://www.altium.com/documentation/knowledge-base/altium-designer/understand-spice-models-supported-in-altium)
- [Altium KB: Apply/renew student license](https://www.altium.com/documentation/knowledge-base/altium-designer/student-license)
- [Fórum Fedevel: firmware simulation of a uC in Altium](https://courses.fedevel.com/forum/altium-designer/21085-firmware-simulation-of-a-uc-in-altium-is-it-possible-how)
- [Fórum EDAboard: MCU simulation in Altium](https://www.edaboard.com/threads/mcu-simulation-in-altium.304048/)
- [ST Community: IBIS model availability](https://community.st.com/s/question/0D50X00009XkYjf/ibis-model-availability)
