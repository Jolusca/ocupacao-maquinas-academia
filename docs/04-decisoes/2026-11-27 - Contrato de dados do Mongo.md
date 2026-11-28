---
Data: "2026-11-27"
Tipo: Decisão
Participantes: Marcos (proposta); a confirmar no grupo (João Lucas, João Nunes, Anderson, Álvaro) só no fim, junto com o resto
---

# Decisão: contrato de dados do Mongo (banco, coleções e campos)

**Status:** PROPOSTA. O Marcos decidiu que o grupo só será avisado no final de tudo; até lá vale este contrato nos testes e na ponte. Nada foi publicado nem alterado no código por causa deste documento.

**Contexto:** a página web ainda **não existe**, então o formato que escolhermos é o que ela vai ler. Em 27/11, olhando o Atlas (cluster `OcupacaoMaquinas`), o que há hoje:

| Onde | Conteúdo | Campos |
|---|---|---|
| `gym_occupancy.nodes` | 3 documentos (`maquina_1` a `maquina_3`) | `name`, `ocupacao` (bool), `timestamp` |
| `gym_occupancy.telemetry` | 27 documentos | os mesmos 3; um por sorteio do simulador (`criaMaquinas.py`), não só nas mudanças |
| `ocupacao_db.maquinas` | 2 documentos manuais | `name`, `ocupacao`, `timestamp` e, num deles, `type: "flexora"` |

Tudo isso é de uma rodada de teste de 24 a 25/11. Nenhum leitor (página ou API) usa esses dados. A nossa ponte (`server/bridge.py`, branch `firmware-integrado`) grava um formato diferente (`node`, `state`, `seq`, `last_seen`, `online`).

**Decisão proposta:**

Banco **`gym_occupancy`**, duas coleções. O banco de testes `gym_occupancy_teste` tem a mesma estrutura e serve para ensaios sem sujar o oficial.

### `nodes` (estado atual): um documento por máquina

Gravado por upsert com chave `node`. É o que a página lê para a tela principal.

| Campo | Tipo | Significado |
|---|---|---|
| `node` | inteiro | número do nó (1 = N01, 2 = N02); é a chave |
| `name` | texto | nome da máquina; padrão `maquina_<n>` |
| `state` | inteiro 0/1 | **0 = livre, 1 = ocupada** |
| `seq` | inteiro 0 a 65535 | contador do último quadro aceito (volta a 0 depois de 65535) |
| `last_seen` | data/hora UTC | quando chegou o último quadro (sinal de vida ou mudança) |
| `online` | booleano | `false` se passaram mais de 60 s sem quadro (4 sinais de vida de 15 s) |

```json
{ "node": 2, "name": "maquina_2", "state": 1, "seq": 17,
  "last_seen": "2026-11-27T14:03:11.482+00:00", "online": true }
```

### `telemetry` (histórico): uma linha por MUDANÇA de estado

Só entra quando o estado muda, e o primeiro quadro de cada nó. O sinal de vida (a cada 15 s) **não** entra aqui, só atualiza `last_seen` em `nodes`. Por isso a coleção é pequena e um gráfico de "quanto tempo ocupada" é direto: o tempo entre duas linhas seguidas é a duração de um estado.

| Campo | Tipo | Significado |
|---|---|---|
| `node` | inteiro | número do nó |
| `state` | inteiro 0/1 | estado **novo** |
| `seq` | inteiro | `seq` do quadro que trouxe a mudança |
| `ts` | data/hora UTC | quando a ponte recebeu o quadro |

```json
{ "node": 2, "state": 1, "seq": 16, "ts": "2026-11-27T14:02:56.071+00:00" }
```

### Regras

- **Datas em UTC**; a página converte para o horário local.
- **`state` é 0/1**, como no quadro do firmware (`N02,1,17`). Não usamos `ocupacao` nem `timestamp`.
- **Um nó offline continua em `nodes`** com `online: false` e o último `state`. A página deve mostrar "sem sinal" em vez de livre ou ocupada.
- **`seq` repetido não grava nada de novo**, só renova `last_seen` (o rádio reenvia quando perde a confirmação).
- Só **a ponte grava**. Nenhuma placa fala com o banco, e a chave do Mongo fica só no notebook (`server/.env`, fora do git).

### O que a página lê

A página não precisa falar com o Mongo. A API da ponte (`http://localhost:8000`, só leitura, CORS liberado) já devolve os mesmos campos:

| Rota | Devolve |
|---|---|
| `GET /machines` | lista dos documentos de `nodes` (estado atual) |
| `GET /machines/<n>` | um nó, ou 404 |
| `GET /machines/<n>/history?limit=50` | últimas linhas de `telemetry`, da mais recente para a mais antiga (máximo 500) |
| `GET /health` | `{"ok": true}` |

As datas saem em ISO 8601 com fuso (`+00:00`).

**Permissões no Atlas (feitas em 27/11):** o usuário da ponte (`ponte`, descrição "Ponte serial para Mongo (TI0148)") tem `readWrite` em `gym_occupancy` e em `gym_occupancy_teste`, e só neles. Hoje o `server/.env` ainda aponta para `gym_occupancy_teste`; para valer o oficial, trocar `MONGODB_DB=gym_occupancy`.

**Alternativas descartadas:**
- **Gravar os dois formatos nos mesmos documentos** (`ocupacao` e `timestamp` além dos nossos): só ajudaria se já houvesse um leitor no formato do simulador. Como a página ainda não existe, seria campo duplicado sem uso. Se isso mudar, a alteração é pequena em `server/bridge_core.py`.
- **Adotar o formato do simulador** (`name`, `ocupacao`, `timestamp`): perde `seq` (descarte de repetidos), `online` (sem sinal) e a chave `node`, que o resto do sistema usa.
- **Gravar em `ocupacao_db.maquinas`:** é uma coleção única de teste manual; não separa estado atual de histórico.
- **Telemetria a cada leitura** (como o simulador faz): enche o banco de linhas iguais e esconde as mudanças, que são o que importa.

**Consequências:**
- **Ponte e API:** já seguem este contrato; sem mudança de código.
- **Simulador** (`server/criaMaquinas.py`, do João Lucas): precisa passar a gravar `node`, `state`, `seq`, `ts` (já combinado em 25/11), e idealmente deixar um nó parar de enviar para testar o `online`.
- **Dados antigos em `gym_occupancy`** (3 + 27 documentos do simulador, formato antigo): limpar antes de gravar os reais, combinando com o João Lucas. Nada foi apagado.
- **Índices (opcional, só se o histórico crescer):** `nodes.node` único e `telemetry` por `(node, ts)` decrescente.
- **Página:** lê pela API local, sem credencial nenhuma no navegador.

**Estado dos testes (27/11):** conexão e permissão de escrita **verificadas** no banco de teste (inserção, leitura, atualização e remoção de um documento marcado, depois removido). A gravação real com o gateway **ainda não foi feita**; está prevista para quando o N01 estiver plugado.

**Em aberto:**
1. Aceite do grupo (mensagem só no final de tudo).
2. Qual banco a apresentação usa (`gym_occupancy` é a proposta) e quando trocar o `.env`.
3. Limpar ou migrar os dados antigos do simulador.
4. **Acesso ao Atlas, a tratar depois da apresentação:** existe uma entrada `0.0.0.0/0` ("testeglobal") na lista de IPs, que libera qualquer endereço; remover quando terminarem os testes. A entrada do laboratório (LI3) é temporária e expira; estender se precisar. Três usuários do banco têm `atlasAdmin` em todos os recursos.

**Cards relacionados:** criar "Decisão: contrato de dados do Mongo" na Base de Conhecimento do Trello depois do aceite do grupo. Relacionada: `2026-11-25 - Arquitetura do servidor (ponte, Mongo e API de leitura).md`.
