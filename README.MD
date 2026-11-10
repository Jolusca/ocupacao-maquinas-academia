# Ocupação de Máquinas de Academia (TI0148)

Projeto desenvolvido na disciplina de Sistemas Embarcados da Universidade Federal do Ceará (UFC), sob orientação do professor Dário Queiroz.

O sistema consiste em um protótipo de baixo custo projetado para monitorar a ocupação de equipamentos de academia em tempo real. A solução utiliza nós microcontrolados com comunicação BLE e sensores ultrassônicos para detectar o uso dos aparelhos, enviando os dados para um servidor central que disponibiliza as informações em uma interface web.

---

## Estrutura do Repositório

* **`firmware/`**: Código do microcontrolador (ESP/STM32) para leitura dos sensores e envio de dados via BLE.
* **`server/`**: Aplicação backend responsável por receber as leituras, processar o estado de ocupação e expor a API.
* **`web/`**: Dashboard interativo para visualização dos status dos equipamentos.
* **`docs/`**: Documentação técnica, esquemáticos de ligação e diagramas do sistema.

---

## Pré-requisitos

* PlatformIO ou Arduino IDE (para compilação do firmware)
* Python 3.x ou Node.js (para execução do servidor)
* Navegador web atualizado

---

## Como Executar

1. **Firmware**: Acesse o diretório `firmware/`, abra o projeto no seu ambiente de preferência e faça o upload do código para a placa.
2. **Servidor**: Acesse a pasta `server/`, instale as dependências necessárias e execute o arquivo principal (`main.py` ou equivalente).
3. **Web**: Acesse o diretório `web/`, inicialize o projeto e abra a aplicação no navegador para visualizar o monitoramento.


## Links úteis

link para o acompanhamento do planejamento e do progresso das tarefas no [Quadro do Trello do Projeto](https://trello.com/b/rjwRxeJL/ocupacao-de-maquinas-de-academia-ti0148).