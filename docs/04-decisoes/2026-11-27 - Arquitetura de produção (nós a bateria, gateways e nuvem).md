---
Data: "2026-11-27"
Tipo: Decisão
Participantes: Marcos (cenário de produção e decisão de registrar); a confirmar com o grupo
---

# Decisão: arquitetura de produção (nós a bateria, gateways na tomada e servidor na nuvem)

**Status:** PROPOSTA para a fase da **bolsa**. **Não muda a entrega de 10/12**, que continua com 2 nós, um deles no notebook, servidor local e página simples (decisões de 13/11 e 25/11). Este documento diz para onde o projeto vai depois, e o que do que já existe se reaproveita.

**Contexto:** em 27/11, ao discutir o gateway, o Marcos observou que na prática **nenhum nó ficará ligado no notebook** (o notebook fica longe das máquinas) e informou o cenário de produção:

- os nós ficam **a bateria**;
- a academia **tem Wi-Fi cobrindo toda a área**;
- o servidor fica **na nuvem**.

O desenho do laboratório (um nó no notebook, os outros por ESP-NOW) só funciona com o notebook perto dos nós. Nos ensaios o ESP-NOW alcançou cerca de 10 m com paredes e deixou de chegar entre 10 e 12 m; metal e pessoas no caminho pioram. Além disso, o nó do notebook é um ponto único de falha, e um receptor só não atende 100 máquinas.

**Decisão proposta:**

```
nós (bateria) ──ESP-NOW──▶ gateways (tomada) ──Wi-Fi da academia──▶ API na nuvem ──▶ Mongo (Atlas)
  N01 ... N100                poucos, espalhados                       grava e serve a página
```

- **Nós (bateria):** acordam, medem, decidem, transmitem por **ESP-NOW** e voltam a dormir. Não ficam associados ao Wi-Fi.
- **Gateways (tomada):** recebem por ESP-NOW e repassam por **HTTPS** à API na nuvem. São poucos e ficam espalhados para cobrir a academia. Vários podem existir ao mesmo tempo; o servidor descarta duplicatas por `(nó, seq)`.
- **API na nuvem:** recebe os quadros (`POST /ingest`, com um token por gateway), mantém o estado e o offline, grava no Mongo e serve a página. A chave do Mongo fica **só na nuvem**.
- **Troca de gateway:** qualquer ESP na tomada assume o papel com um comando (`papel coletor`), sem regravar. Nó a bateria não deve ser gateway.

**Por que não Wi-Fi direto de cada nó:** a bateria decide. Associar ao roteador, obter IP e abrir uma conexão a cada envio custa, tipicamente, dezenas de vezes mais energia que um envio ESP-NOW de poucos milissegundos (estimativa: medir antes de prometer duração de bateria). Wi-Fi direto seria o melhor caminho se os nós fossem ligados na tomada, pois eliminaria o gateway. Fica registrado como alternativa para esse caso.

**O que se reaproveita do que existe:**

| Hoje (laboratório) | Na produção |
|---|---|
| Quadro `N<id>,<estado>,<seq>`, sinal de vida de 15 s | Mesmo quadro. Pode ganhar a tensão da bateria. |
| Papel "coletor" (aviso `BCN` a cada 5 s, sensores aprendem o MAC) | Vira o **gateway**. A saída muda de serial USB para HTTPS. |
| Papel automático pela USB, comandos `id`, `papel`, `info`, `limpar` | O automático vale para a demonstração. Na produção o gateway é configurado por comando (`papel coletor`, e as credenciais de Wi-Fi). |
| Ponte: descarta `seq` repetido, offline após 60 s, retoma o estado do banco | Vira a lógica da API na nuvem. |
| Contrato `nodes` e `telemetry` no Mongo | Mantém (ver `2026-11-27 - Contrato de dados do Mongo.md`). |
| API de leitura (`/machines`, `/history`) | Hospedada, servindo a página. |

O firmware do papel automático e dos comandos foi **testado nas duas placas em 27/11**: o nó com o notebook na USB vira coletor sozinho; um nó só na fonte vira sensor e entrega ao coletor; trocar o coletor por outro nó funciona sem regravar (o sensor percebe a falta em ~20 s e aprende o novo pelos avisos). Quando o envio direto ao coletor falha, o quadro é reenviado por broadcast. Ainda **sem commit** (27/11).

**Pontos de atenção:**
1. **Canal.** O ESP32 conectado ao Wi-Fi é obrigado a usar o canal do roteador, e o ESP-NOW dos nós precisa estar no mesmo. Com um roteador só, fixa-se o canal. Com vários pontos de acesso em canais diferentes, os nós precisam **descobrir o canal** pelo aviso do gateway. Decidir cedo: pode exigir um roteador dedicado aos gateways, em canal fixo.
2. **Sensor e energia.** O HC-SR04 usa 5 V e consome mesmo parado, o que é ruim para bateria. Avaliar um sensor de 3,3 V de baixo consumo (um ToF, por exemplo) e alimentar o sensor só durante a medida. O circuito soldado para a entrega **provavelmente muda** na bateria.
3. **Ciclo de acordar e offline.** Um nó que dorme não manda sinal de vida a cada 15 s. O tempo de "offline" (hoje 60 s) tem de acompanhar o intervalo em que o nó acorda.
4. **Gateway sem internet.** Precisa guardar os quadros e reenviar quando a rede voltar (hoje nada é guardado). Os nós a bateria não guardam nada.
5. **Segurança.** O ESP-NOW hoje vai sem criptografia e o quadro é texto puro: qualquer ESP próximo poderia forjar um quadro. Para produção, usar a criptografia do ESP-NOW ou autenticar o quadro. O gateway precisa de um token próprio para a API.
6. **Nuvem e Atlas.** Um servidor na nuvem costuma mudar de IP, então a lista de IPs do Atlas precisa de outra saída (IP fixo ou regra restrita por usuário). Mesmo problema de IP e firewall visto no laboratório (porta 27017 bloqueada).
7. **Escala.** Com 100 nós, medir a taxa de perda do ESP-NOW com muitos nós e o efeito do Wi-Fi da academia no canal.

**Atualização de firmware sem cabo (OTA):** requisito do Marcos em 27/11: os nós ficam dentro de caixas que **escondem o conector USB**, então atualizar o firmware tem de ser possível sem plugar cabo.

*Já verificado (27/11, núcleo 3.3.11 e a placa):* flash de 4 MB; a tabela de partições já tem **duas áreas de aplicativo** (`ota_0` e `ota_1`, 1280 KB cada) e `otadata`; o **rollback do bootloader está ligado** (`CONFIG_BOOTLOADER_APP_ROLLBACK_ENABLE=y`); o firmware atual ocupa cerca de 991 KB e cabe nas duas áreas. Falta o código. Secure boot e assinatura de imagem **não** estão ligados. As bibliotecas `Update`, `HTTPUpdate` e `ArduinoOTA` já vêm no núcleo.

*Caminhos:*
1. **Pelo gateway, por ESP-NOW (recomendado com bateria).** O gateway baixa a imagem da nuvem por HTTPS e a distribui em blocos aos nós (250 bytes por quadro; 1 MB são cerca de 4.000 quadros), com confirmação e retransmissão por bloco. O nó grava na partição inativa, confere o hash e reinicia. O nó só fica acordado numa janela de atualização, avisada na resposta ao quadro dele. O nó nunca se associa ao Wi-Fi. Custo: protocolo próprio (bloco, retransmissão, retomada).
2. **Wi-Fi puxado pelo nó.** No modo de atualização o nó se associa ao Wi-Fi e baixa a imagem por HTTPS. Mais simples (as bibliotecas existem), mas exige as credenciais do Wi-Fi em cada nó e gasta bateria (aceitável, pois é raro). O binário com TLS cresce; a área de 1280 KB pode apertar, e há 1408 KB de `spiffs` sem uso que podem virar área de aplicativo.
3. **Bluetooth, pelo celular.** Possível no ESP32-C6, mas é desenvolvimento novo. Só como plano C.
4. **Plano B físico:** um prolongador USB até a parede da caixa, ou pontos de teste (pogo pins) acessíveis sem abrir. É o que salva o nó se a atualização e o rollback falharem.

*Exigências:*
- **Imagem autenticada antes de gravar** (hash mais assinatura ou HMAC; no limite, secure boot v2, que é irreversível). O ESP-NOW é aberto: sem isso, qualquer ESP por perto poderia gravar um firmware malicioso.
- **Rollback com validação:** a versão nova precisa confirmar que funciona (por exemplo, entregar um quadro ao gateway) em alguns minutos; senão o bootloader volta à anterior.
- **O mecanismo de atualização tem de estar sempre na imagem nova.** Um firmware que quebra o OTA é o pior caso. Testar em um nó antes de distribuir, e atualizar por etapas.
- **Versão visível** (no log de boot e, de preferência, na telemetria) para saber o que cada nó está rodando.
- **O primeiro firmware com OTA precisa ser gravado por cabo.** Os nós das primeiras caixas devem sair de lá já com ele.

**Alternativas descartadas:**
- **Um nó ligado ao notebook (como no laboratório):** alcance de ~10 m, ponto único de falha e não escala. Continua valendo só para a demonstração.
- **Wi-Fi direto de cada nó:** gasto de bateria; ver acima. Valeria se os nós fossem ligados na tomada.
- **Nós gravando direto no Mongo:** a chave do banco ficaria nas placas.

**Consequências:**
- **Entrega de 10/12:** nenhuma. O laboratório segue com o nó no notebook, a ponte e a API locais.
- **Firmware:** na bolsa, trocar a saída do coletor (serial por Wi-Fi/HTTPS), suporte a canal do Wi-Fi, armazenamento no gateway, sono profundo e leitura intermitente nos nós, e **atualização sem cabo** com imagem autenticada e rollback.
- **Caixa:** prever um acesso de serviço ao conector (prolongador USB ou pogo pins), mesmo com OTA.
- **Servidor:** a ponte e a API passam a ser um serviço na nuvem com `POST /ingest`. Era a alternativa "API separada e hospedada" de 25/11, descartada para o laboratório e agora retomada para a produção.
- **Hardware:** definir o sensor e a alimentação por bateria antes de projetar a placa.

**Em aberto:**
1. Aceite do grupo.
2. Tipo de bateria e autonomia desejada (define sensor e intervalo de leitura).
3. Roteador dedicado aos gateways em canal fixo, ou descoberta de canal pelos nós.
4. Onde a API fica hospedada e como liberar o acesso ao Mongo.

**Cards relacionados:** criar "Decisão: arquitetura de produção" na Base de Conhecimento do Trello depois do aceite. Relacionadas: `2026-11-25 - Arquitetura do servidor (ponte, Mongo e API de leitura).md` e `2026-11-27 - Contrato de dados do Mongo.md`.
