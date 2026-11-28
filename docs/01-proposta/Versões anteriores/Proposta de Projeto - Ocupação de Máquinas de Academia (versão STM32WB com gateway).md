---
Disciplina: "[[TI0148_Sistemas_Embarcados]]"
Data: "2026-10-14"
Tipo: Proposta de Projeto
---

# Sistema Distribuído de Ocupação e Recomendação de Equipamentos de Academia com STM32WB, ToF e BLE

**Disciplina:** TI0148 – Sistemas Embarcados (2026.2)  
**Equipe:** Antonio Marcos Justino Carneiro, João Victor Leandro Nunes, João Lucas Oliveira Mota  
**Professor:** Dário Queiroz  

> Versão oficial para entrega: [`Proposta de Projeto - Ocupação de Máquinas de Academia.pdf`](file:///home/marcos/Notas/01_Disciplinas_2026.2/TI0148_Sistemas_Embarcados/Proposta%20de%20Projeto%20-%20Ocupa%C3%A7%C3%A3o%20de%20M%C3%A1quinas%20de%20Academia.pdf) (gerado a partir do `.tex` via `tectonic`).

---

## 1. Problema e Objetivo

Em academias com alta densidade de alunos, o praticante perde tempo circulando pelo salão para checar quais aparelhos da sua rotina de treino estão livres. A espera desorganizada gera filas, dispersão e estende desnecessariamente o treino.

O objetivo deste projeto é desenvolver um **sistema embarcado distribuído de ultra-baixo consumo** para monitorar a ocupação de **até 100 equipamentos** em tempo real e recomendar ao aluno a **próxima máquina disponível da sua ficha de treino**, otimizando o fluxo e os tempos de espera.

Diferente de abordagens centralizadas (inviáveis por exigirem centenas de metros de cabos analógicos pela academia), o projeto adota **nós sem fio compactos a bateria em cada máquina**, comunicando via **BLE Advertising** com um **STM32 Gateway com Wi-Fi**, que encaminha os eventos via **MQTT diretamente para o broker** pela rede sem fio da academia.

---

## 2. Arquitetura do Sistema

```
┌─────────────────────────────────┐
│     Nó Sensor (Máquinas 1..100) │
│     ToF (VL53L1X) ──I²C──       │
│     STM32WB + Bateria (2x AA)   │
└────────────────┬────────────────┘
                 │
          BLE Advertising (canais 37, 38, 39)
          (Sem conexão / Broadcaster)
                 ▼
┌─────────────────────────────────┐
│        STM32 Gateway            │
│       (GAP Observer contínuo)   │
│       Wi-Fi + Cliente MQTT      │
└────────────────┬────────────────┘
                 │
          Wi-Fi (MQTT direto)
                 ▼
┌─────────────────────────────────┐
│          Broker MQTT            │  (Servidor em nuvem ou
│        (Mosquitto Server)       │   servidor local da academia)
└────────────────┬────────────────┘
                 │
          WebSocket / MQTT
                 ▼
┌─────────────────────────────────┐
│       Aplicativo do Aluno       │  (Página Web / App mobile
│    (Recomendação em Tempo Real) │   com sincronização instantânea)
└─────────────────────────────────┘
```

### Esclarecimento: Gateway e Broker não são a mesma coisa
* **STM32 Gateway com Wi-Fi:** É o hardware concentrador de rádio e cliente de rede sem fio. Opera continuamente como **GAP Observer** capturando os anúncios de rádio dos 100 nós, faz o parse dos dados e conecta-se diretamente à rede Wi-Fi da academia, atuando como um **cliente MQTT** que despacha as mensagens diretamente ao broker sem necessidade de cabos de rede ou intermediários.
* **Broker MQTT:** É o serviço de mensageria de rede (ex.: Eclipse Mosquitto) hospedado no servidor da academia, em um Raspberry Pi ou na nuvem. Ele gerencia as filas, tópicos, permissões e distribui os dados aos clientes conectados com suporte a mensagens retidas (`Retain`).

---

## 3. Especificação dos Componentes e Dimensões

| Elemento | Descrição Técnica |
| :--- | :--- |
| **SoC do Nó** | **STM32WB55** (ou STM32WB15): Dual-core (Cortex-M4 a 64 MHz + Cortex-M0+ dedicado ao rádio BLE 5.0). Consumo em modo *Stop 2* de apenas $2{,}1\,\mu\text{A}$ com SMPS integrado. |
| **Sensor de Presença** | **VL53L1X (Time-of-Flight)**: Medição absoluta de distância por feixe infravermelho de 940 nm (até 1,3 m em modo curto), imune à cor ou textura das roupas dos alunos. Interface I²C com pino XSHUT para desligamento em repouso. |
| **Alimentação do Nó** | 2 pilhas alcalinas AA em série ($3{,}0\text{ V}$) ou 1 célula industrial Li-SOCl2 ER14505 ($3{,}6\text{ V}$, 2600 mAh). |
| **Gateway Concentrador** | Microcontrolador STM32 com conectividade Wi-Fi (ex.: STM32WB com módulo/coprocessador Wi-Fi de alta velocidade ST67W ou kit STM32 IoT Discovery B-U585I-IOT02A com Wi-Fi/BLE), alimentado na tomada (5V/USB), operando em escuta contínua de rádio BLE e atuando como cliente MQTT nativo. |
| **Conectividade do Gateway** | Wi-Fi 802.11 b/g/n (ou Wi-Fi 6), conectando-se diretamente ao ponto de acesso (roteador Wi-Fi) da academia e publicando mensagens MQTT diretamente no broker (porta 1883/8883) pela rede sem fio. |
| **Broker / Servidor** | Broker MQTT Mosquitto e backend leve para persistência e históricos. |
| **Frontend do Aluno** | Web App responsivo (HTML5/React/WebSocket) acessível no smartphone do aluno. |

### Dimensões Físicas do Nó
O sensor ToF mede $4{,}9 \times 2{,}5 \times 1{,}56\text{ mm}$ e o chip STM32WB mede $7 \times 7\text{ mm}$. A caixa plástica e as baterias determinam o tamanho do produto:

| Versão | Dimensões Aproximadas ($C \times L \times A$) |
| :--- | :--- |
| Placa de desenvolvimento NUCLEO-WB55RG | $70 \times 65 \times 15\text{ mm}$ |
| Protótipo de bancada (ToF, pilhas, placa de testes) | $\approx 100 \times 80 \times 35\text{ mm}$ |
| Placa própria (PCB) com STM32WB e ToF integrados | $\approx 40 \times 30 \times 5\text{ mm}$ |
| **Produto final encapsulado com 2 pilhas AA** | **$\approx 65 \times 40 \times 25\text{ mm}$** (tamanho próximo a uma caixa de fósforos pequena) |

### Requisitos Mecânicos e de Instalação na Máquina
1. **Janela Óptica:** Abertura frontal em acrílico translúcido para 940 nm protegendo o emissor/receptor do VL53L1X.
2. **Posicionamento:** Fixado na estrutura rígida da máquina, apontado diretamente para a região onde o aluno senta/apoia (evitando partes móveis sujeitas a choque mecânico).
3. **Isolamento de RF:** A antena do STM32WB deve ficar exposta para fora das chapas e tubos de aço da máquina, evitando o efeito de Gaiola de Faraday.
4. **Proteção:** Gabinete com grau de proteção IP54 contra suor, pó e produtos químicos de limpeza.
5. **Manutenção:** Tampa traseira com fecho para substituição fácil das pilhas a cada ano.

---

## 4. Protocolo de Comunicação e Mensagens

### BLE Advertising (Broadcaster / Observer)
Os nós operam em modo **Non-Connectable Undirected Advertising (`ADV_NONCONN_IND`)** transmitindo nos canais de anúncio 37, 38 e 39. Não há estabelecimento de conexão ponto a ponto, viabilizando o monitoramento simultâneo de 100 máquinas com zero sobrecarga de conexão.

O payload útil utiliza o campo *Manufacturer Specific Data* (AD Type `0xFF`), somando 10 bytes:
```
[ 0x09 ] [ 0xFF ] [ 0x0030 (ST) ] [ ID_Máquina (1B) ] [ Estado (1B) ] [ SeqNum (1B) ] [ Bat% (1B) ] [ Dist (2B) ]
```
* **Estado:** `0x00` = Livre, `0x01` = Ocupada, `0x02` = Descanso entre séries, `0xFE` = Falha no sensor.
* **SeqNum:** Contador incremental para descarte de duplicatas pelo Gateway.

### Tópicos e Payloads MQTT
O Gateway publica os eventos no tópico:
```
academia/aparelho/{id}/status
```
Com **QoS 1** e flag **`Retain = true`**. Exemplo de payload:
```json
{
  "id": 37,
  "estado": "ocupado",
  "bateria": 92,
  "rssi": -65,
  "ts": 1728945600
}
```
A flag `Retain` garante que qualquer novo smartphone que se conecte ao broker receba imediatamente o mapa de todas as máquinas sem aguardar novos disparos de rádio.

---

## 5. Gerenciamento de Energia e Autonomia da Bateria

O nó opera em **Duty Cycling Estrito**:
* Acorda do modo **Stop 2** a cada $1\text{ segundo}$;
* Habilita o VL53L1X e realiza medição óptica curta ($20\text{ ms}$ a $\approx 18\text{ mA}$);
* O Cortex-M4 processa a distância, avalia os temporizadores e volta ao repouso;
* O rádio BLE só transmite ao confirmar mudança de estado (3 rajadas de $3\text{ ms}$) ou em *heartbeat* periódico a cada $15\text{ segundos}$ ($3\text{ ms}$ a $5{,}2\text{ mA}$).

### Cálculo de Corrente Média ($I_{\text{médio}}$):
* $I_{\text{ToF}} = 18\text{ mA} \times \frac{20\text{ ms}}{1000\text{ ms}} = 360\,\mu\text{A}$
* $I_{\text{MCU\_ativo}} = 4\text{ mA} \times \frac{2\text{ ms}}{1000\text{ ms}} = 8\,\mu\text{A}$
* $I_{\text{BLE\_burst}} = 5{,}2\text{ mA} \times \frac{3\text{ ms}}{15000\text{ ms}} \approx 1\,\mu\text{A}$
* $I_{\text{Sleep}} = 2{,}1\,\mu\text{A (MCU)} + 5{,}0\,\mu\text{A (ToF standby)} \approx 7{,}1\,\mu\text{A}$
* **$I_{\text{médio\_total}} \approx 376\,\mu\text{A} \quad (\approx 0{,}38\text{ mA})$**

### Autonomia Estimada:
$$\text{Autonomia (2x AA, 2200 mAh)} = \frac{2200\text{ mAh}}{0{,}38\text{ mA} \times 24\text{ h}} \approx 241\text{ dias} \quad (\approx \mathbf{8\text{ meses}})$$

> [!TIP]
> **Amostragem Adaptativa:** Quando a máquina permanece desocupada por mais de 5 minutos, a amostragem do ToF passa de 1 Hz para 0,33 Hz (uma medição a cada 3 s). A corrente média cai para **$135\,\mu\text{A}$**, estendendo a autonomia para **mais de 1,5 ano**.

---

## 6. Lógica de Detecção e Algoritmo de Recomendação

### Filtros e Máquina de Estados no Firmware do Nó
* **Histerese de Distância:** Detecção de chegada com $\le 70\text{ cm}$; detecção de saída com $\ge 90\text{ cm}$ (evita oscilação na borda de detecção).
* **Filtro de Chegada (5 segundos):** A presença contínua precisa durar pelo menos 5 s para comutar para "Ocupado", ignorando passantes que apenas cruzam a frente do sensor.
* **Tolerância de Descanso (60 a 90 segundos):** Durante o descanso entre séries, o aluno costuma levantar ou mudar de posição. O estado permanece em "Ocupado/Descanso" e só volta a "Livre" após 90 s de ausência ininterrupta.

### Algoritmo de Recomendação no Aplicativo
1. O aluno seleciona seu treino do dia (ex.: Aparelhos `[12, 37, 5, 18]`);
2. O aplicativo consulta o estado retido no broker MQTT;
3. Se houver aparelho da rotina com estado `Livre`, indica imediatamente a primeira opção disponível;
4. Se todos os aparelhos da rotina estiverem `Ocupados`, o algoritmo estima pelo histórico de tempo de uso qual equipamento liberará primeiro e exibe o tempo estimado de espera.

---

## 7. Plano de Testes

| Cenário | Resultado Esperado |
| :--- | :--- |
| **Passante cruza o sensor (< 5 s)** | O nó ignora a leitura transitória e mantém o estado `Livre` |
| **Aluno senta para treinar (> 5 s)** | Comuta para `Ocupado`, transmite rajada BLE e broker atualiza app |
| **Aluno levanta para intervalo (< 60 s)** | Mantém o estado `Ocupado` (tolerância de descanso entre séries) |
| **Aluno finaliza e libera o aparelho (> 90 s)** | Comuta para `Livre` e publica atualização no broker |
| **Consulta pelo app com máquinas livres** | Recomenda a primeira máquina disponível da sequência de treino |
| **Todas as máquinas do treino ocupadas** | Recomenda a máquina com menor tempo previsto para conclusão |
| **Escalabilidade (100 nós em advertising)** | Gateway recebe e processa os pacotes nos 3 canais sem saturação |
| **Consumo elétrico em bancada** | Corrente em modo Stop 2 confirmada abaixo de $10\,\mu\text{A}$ com instrumentação |

---

## 8. Cronograma de Desenvolvimento (6 Semanas)

| Semana | Entrega Principal |
| :---: | :--- |
| **1** | Especificação fechada, integração I²C do sensor VL53L1X com STM32WB e configuração inicial da stack de rádio BLE. |
| **2** | Implementação dos modos de baixo consumo (*Stop 2*), histerese e temporizadores (5 s e 90 s) com medição de corrente. |
| **3** | Estruturação do pacote de *BLE Advertising* no nó e desenvolvimento do *GAP Observer* no STM32WB Gateway. |
| **4** | Integração da pilha Wi-Fi e cliente MQTT no STM32 Gateway, estabelecendo conexão direta com o broker Mosquitto. |
| **5** | Desenvolvimento do Web App do aluno, algoritmo de recomendação e emulador de nós para escala de 100 máquinas. |
| **6** | Ensaios de bancada ponta a ponta, análise de autonomia, vídeo demonstrativo e redação do relatório final. |

### Divisão de Tarefas
As atividades do projeto serão distribuídas entre os membros da equipe nas seguintes frentes (responsáveis a definir):
* **Nó sensor e baixo consumo:** Firmware do nó (integração I²C com sensor ToF VL53L1X, modos *Stop 2*, filtros de histerese, temporizadores de presença e transmissão *BLE Advertising*).
* **Gateway e conectividade de rede:** Firmware do STM32 Gateway (escuta *GAP Observer*, decodificação de pacotes brutos e cliente MQTT direto sobre Wi-Fi).
* **Infraestrutura, software e validação:** Configuração do broker MQTT, aplicativo web do aluno, algoritmo de recomendação, ensaios de bancada e documentação final.

---

## 9. Validação e Demonstração do Projeto

Para atendimento aos requisitos da disciplina:
1. **Protótipo de bancada funcional:** Nó real com placa NUCLEO-WB55 e sensor ToF operando a bateria;
2. **Gateway STM32 com Wi-Fi em tempo real:** Escuta de rádio ativa e despacho direto de mensagens via Wi-Fi para o broker MQTT;
3. **Emulador de carga:** Injeção de dados de máquinas virtuais adicionais para demonstrar a escala de 100 equipamentos e a recomendação de rotinas no aplicativo do aluno.
