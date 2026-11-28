---
Data: "2026-11-25"
Tipo: Decisão
Participantes: Marcos (proposta); João Nunes (sugeriu ponte + API); a confirmar no grupo com João Lucas, Anderson e Álvaro
---

# Decisão: arquitetura do servidor (ponte + API num programa só, Mongo)

**Status:** PROPOSTA v2 (atualizada em 25/11 depois da conversa com o grupo), ainda sem um "fechado" explícito. Pontos em aberto no fim da nota. Diagrama: `2026-11-25 - Arquitetura v2 (ponte + API).png`. A v1 (API separada e hospedada) está em `2026-11-25 - Arquitetura (diagrama).png`.

**Atualização v2:** o João Nunes aceitou "se a ponte em Python for API também, aí show" (a API dele só ficaria pronta mais tarde) e o Marcos definiu que a página será mostrada **só no laboratório**. Por isso a API de leitura passou a ser parte da ponte, no notebook, sem hospedagem. A página abre no navegador do próprio notebook.

**Contexto:** o firmware (ESP32-C6 + ESP-NOW) e o formato do quadro estão definidos, mas o lado do servidor só tinha a linha "Servidor Python → página web simples" (nota de 18/11). Em 24/11 o grupo subiu `server/api_mongo.py` e `server/criaMaquinas.py` (Mongo no Atlas, com dados simulados em `maquina_N`/`ocupacao`) e discutiu quem grava no banco e como liberar o IP. "Servidor" estava com dois sentidos: o programa que lê a serial e a API que o front consome.

**Decisão proposta:**

```
Nó 2 (sensor + HC-SR04) ──ESP-NOW──▶ Nó 1 (gateway) ──USB/serial──▶ PONTE + API (um programa, no notebook) ◀──grava e lê──▶ Mongo (Atlas)
                                                                                   │
                                                                         HTTP/JSON │ GET /machines
                                                                                   ▼
                                                                    Página web (navegador do notebook)
```

- **Nós:** **N01 = gateway e também a máquina 1** (o firmware do gateway mede com um HC-SR04 próprio e imprime o próprio quadro na serial, sem rádio); **N02 = nó sensor remoto, máquina 2** (ESP-NOW). Decidido pelo Marcos em 25/11. Na quinta (26/11) precisam de **dois HC-SR04 ligados** (um em cada placa).
- **Quadro:** `N<id>,<estado>,<seq>` (ex.: `N02,1,17`); estado 1 = ocupada, 0 = livre; enviado ao mudar de estado e como sinal de vida a cada 15 s. Linhas da serial que começam com `# ` são log.
- **Ponte + API** (`server/bridge.py` e `server/api.py`, um programa só no notebook com o gateway): lê a serial, valida com `parse_frame`, ignora `seq` repetido, marca o nó **offline após 60 s** sem quadro, grava no Mongo e responde à página. Só as placas ESP-NOW falam por rádio; **nenhuma placa grava no banco**.
- **Coleções (banco `gym_occupancy`):**
  - `nodes`: `{node, name, state, seq, last_seen, online}`, um documento por nó (upsert por `node`).
  - `telemetry`: `{node, state, seq, ts}`, uma linha por mudança de estado (o sinal de vida só atualiza `last_seen`).
  - Nome da máquina: padrão `maquina_<n>`; mapeamento nó → máquina combinado pelo grupo.
- **API (feita, dentro da ponte):** só leitura, porta 8000 e só no próprio notebook (127.0.0.1) por padrão. `GET /health`, `GET /machines` (estado atual, da memória da ponte), `GET /machines/<n>` e `GET /machines/<n>/history?limit=50` (mudanças de estado, do Mongo; da memória se não houver banco). Usa só a biblioteca padrão. O front não guarda a chave do Mongo.
- **Segurança:** a ponte usa um usuário do Atlas com **leitura e escrita só** em `nodes` e `telemetry` (a API lê o histórico). A chave fica no `.env` (fora do git). Nos dias de teste o Atlas libera `0.0.0.0/0` (o IP do notebook muda); remover depois.
- **Front:** estatísticas, ordenação e visual. O estado de cada máquina e o offline vêm do servidor, não do front.

**Alternativas descartadas:**
- **Placas gravando direto no Mongo por Wi-Fi:** o nó sensor só usa ESP-NOW, sem roteador; o IP e as credenciais ficariam no firmware.
- **API separada e hospedada, com a ponte mandando `POST /ingest`:** tira a chave do Mongo do notebook, mas exige API hospedada antes do teste, token de envio e um ponto de falha novo. Só ajuda no IP se a API ficar num servidor com IP fixo (hospedagem gratuita costuma ter IP variável). Fica como plano para a bolsa; a ponte já separa "o que gravar" de "onde gravar".
- **Página hospedada fora do notebook:** não é preciso, pois a apresentação é só no laboratório (decidido em 25/11). Se um dia for preciso: função de servidor lendo o Mongo com usuário só de leitura (o IP da hospedagem é variável) ou túnel até o notebook.
- **Estado e estatística só no front:** o offline e o `seq` repetido precisam de um processo contínuo.

**Consequências:**
- **Firmware:** sem mudança; o gateway só imprime os quadros pela serial.
- **Servidor:** ponte e API em `server/` (29 testes), nas branches locais `servidor-ponte` e `firmware-integrado`; falta publicar. A ponte ainda não foi testada com o gateway real nem com o Mongo real.
- **Site:** consome a API em `http://localhost:8000` (CORS liberado); o simulador `criaMaquinas.py` deve gravar no formato novo (`node`, `state`, `seq`, `ts`), com alguns nós parando de enviar para testar o offline.
- **Plano:** teste do HC-SR04 real na quinta 26/11 à tarde; teste da ponte com o gateway e o Mongo reais.

**Em aberto (decidir com o grupo):**
1. Confirmar com o grupo a v2 (ponte + API num programa só) e se a API do João Nunes ainda é necessária.
2. As credenciais do João Nunes dão acesso ao projeto no Atlas (para cadastrar IP) ou só a um usuário do banco? O IP do laboratório precisa estar liberado em 26/11.
3. Notebook da demonstração de 10/12: não pode hibernar (os nós aparecem offline).
4. Nomes das máquinas (hoje `maquina_1` e `maquina_2`; para trocar, `--nome 1=supino --nome 2=leg_press`). O mapeamento N01 → máquina 1 e N02 → máquina 2 já está decidido.

**Cards relacionados:** criar o card "Decisão: arquitetura do servidor (ponte, Mongo e API)" na Base de Conhecimento do Trello depois da confirmação do grupo.
