# Padrão de código do firmware

Este documento define como escrevemos o código de `firmware/`. O objetivo é que
qualquer pessoa do grupo leia e altere o código de outra sem estranhar o estilo,
e que boa parte das conferências fique por conta de ferramentas, não de revisão
manual.

A base é o **BARR-C:2018 (Embedded C Coding Standard, de Michael Barr)**, a
bibliografia básica da matéria de C Avançado. A edição gratuita está em
<https://barrgroup.com/coding-standard>. Aqui ficam só um resumo com as nossas
palavras e as exceções que decidimos adotar. O texto do padrão tem direitos
autorais: **não copie o PDF nem trechos longos dele para este repositório**.

## Escopo

| Pasta | Situação |
|---|---|
| `hal/`, `app/`, `test/` | Seguem este padrão. `make format-check` confere o estilo. |
| `core/` | Entra no padrão e no formatador depois da junção das branches. Quem implementar o `core/` já pode seguir este documento. |
| `tools/` (shell e Python) | Fora do escopo do BARR-C (que é para C). Use bom senso e `shellcheck` no shell. |

## Como conferir e aplicar o estilo

```
make format         # aplica o estilo em hal/, app/ e test/
make format-check   # só confere; sai com erro se algo estiver fora do padrão
make test           # roda os testes (o -Werror já barra avisos do compilador)
```

- O estilo está em `.clang-format` (largura, chaves, indentação) e `.editorconfig`
  (UTF-8, LF, 4 espaços, linha final). Configure o seu editor para ler os dois.
- O `clang-format` precisa estar instalado: `pip install clang-format` ou o pacote
  `clang-format` da sua distribuição.
- Antes de abrir um pull request: `make format && make test`.

## Regras adotadas

### Formato
- **Chaves sempre**, mesmo em `if`, `else`, `for` e `while` de uma linha só. A
  chave de abertura fica **em linha própria** (estilo Allman). O `clang-format`
  faz isso por você.
- **Até 80 colunas** por linha, em código e em comentário.
- **Indentação de 4 espaços**, nunca tab. Fim de linha LF.
- Uma instrução por linha, e **uma variável por declaração** (sem
  `int a, b;`).
- **Parênteses** em volta de cada operando de `&&` e `||`:
  `if ((len <= 0) || (len > MAX))`. Não confie na precedência dos operadores.

### Comentários
- Escreva em **português, com acentos**, em frases completas. Comente o **porquê**
  e as suposições, não o que o código já diz.
- Todo módulo e toda função pública têm o contrato descrito **no `.h`**: unidades,
  valores de retorno, quem pode chamar o quê. As implementações explicam os
  mecanismos não óbvios (por que 3 tentativas, por que a interrupção é assim).
- **Todo cast leva um comentário** que diz por que ele é seguro (de preferência
  na linha de cima). Se o cast não for necessário, tire-o.
- Nunca deixe código comentado. Para desligar um trecho, use `#if 0`.
- Não escreva nome de pessoa nem data relativa ("na terça") em comentário. Use
  `TODO:` e registre o dono e o prazo no Trello.
- **Textos de log na serial ficam em ASCII**: quem lê a serial não sabe de acentos.

### Nomes
- Identificadores em **inglês**, em `snake_case`. Macros e constantes em
  `MAIÚSCULAS_COM_SUBLINHADO`.
- **Pelo menos 3 letras** em qualquer variável, inclusive contadores de laço
  (`step_idx`, não `i`).
- Funções públicas começam com o **nome do módulo**: `radio_send`, `occ_update`,
  `frame_decode`. Funções internas são `static`.
- Tipos: `typedef` com sufixo `_t` (`frame_t`, `occ_t`).
- Variáveis de arquivo (`static`) levam o prefixo **`s_`** (`s_peer`). O prefixo
  **`g_`** fica reservado a variáveis globais com ligação externa, que devem ser
  evitadas.
- Rotinas de interrupção terminam em **`_isr`** (`echo_isr`).
- Constantes numéricas têm **nome** (`ACK_TIMEOUT_MS`), não aparecem soltas no
  código. Em macros e expressões, valores sem sinal levam o sufixo `u` (`100u`).
- Cada `.c`/`.cpp` tem um `.h` de mesmo nome e inclui o **seu próprio `.h`**
  (`radio.cpp` inclui `radio.h`).

### Tipos e instruções
- Use **inteiros de largura fixa** (`uint8_t`, `int16_t`, `uint32_t`...). Não use
  `short` nem `long`. Para imprimir `uint32_t`, use `PRIu32` de `<inttypes.h>`.
  `int` só onde a API do Arduino ou do ESP-IDF o exige.
- Booleanos são `bool`. Não misture inteiro com sinal e sem sinal na mesma
  expressão.
- Laço infinito é `for (;;)`. Todo `if ... else if` termina com `else`. Sem
  `goto`, sem atribuição dentro de condição.
- Use `static` em tudo que é privado, `const` sempre que o valor não muda e
  `volatile` em variável compartilhada com interrupção ou outra tarefa.
- Cada arquivo `.h` tem guarda contra inclusão múltipla. **Nunca inclua um `.c` em
  outro `.c`.** Variáveis globais devem ser evitadas.
- Macros com argumentos só quando uma função não resolve, e sempre com
  parênteses em volta dos argumentos e do corpo.

## Exceções ao BARR-C (decididas e documentadas)

| Regra do padrão | O que fazemos |
|---|---|
| Constante à esquerda do `==` | **Não exigimos.** Os compiladores já avisam atribuição dentro de `if`. |
| Comentário de fim de arquivo | **Não exigimos.** O `.editorconfig` garante a linha final. |
| Uma única saída (`return`) por função | **Preferência**, não obrigação. Use `return` antecipado quando deixar o código mais claro. |
| Prefixos `p_` (ponteiro) e `b_` (booleano) | **Não adotamos.** Preferimos nomes descritivos. |
| Linguagem C | `hal/` e `app/` são C++ onde a API do Arduino e do ESP32 exige; o resto é C. Nos `.cpp` seguimos as mesmas regras. |
| `setup()` e `loop()` | Mantêm o nome exigido pelo Arduino. |
| Função pública com o nome do módulo | `dist_hcsr04_read` fica com esse nome para formar o par com `dist_fake_read` (mesma assinatura, o programa escolhe uma). |

Para mudar uma regra ou uma exceção, abra um pull request alterando este
documento, para o grupo discutir antes.

## Como trabalhamos o código

- **Testes antes do código (TDD).** O ciclo é: escrever um teste que falha,
  fazer só o necessário para ele passar, depois limpar o código (*refatorar*).
  Passos pequenos, rodando `make test` a cada um.
- **Lógica no PC, hardware na placa.** Tudo que decide fica em `core/` (C puro,
  sem incluir nada de hardware e sem ler relógio nem pino: o tempo entra como
  argumento). O que toca no hardware fica em `hal/`. Assim os testes rodam no PC
  sem placa.
- **Dublês de teste no lugar do hardware.** O `hal/dist_fake.c` faz o papel do
  sensor, e o relógio é injetado. Para testar outra parte que depende de
  hardware, crie um dublê com a mesma interface em vez de depender da placa.
- **Dono por pasta.** Cada pessoa mexe só na sua pasta, e as juntas são feitas por
  pull request. Um commit por módulo, com mensagem no formato
  `firmware: o que mudou`.
- **Sem dado de placa no repositório.** MACs, pinos e opções de cada placa ficam em
  `app/config.h` e são conferidos em revisão.

## Checklist de revisão de código

Antes de aprovar um pull request, confira:

- [ ] `make format-check` e `make test` passam.
- [ ] Sem `if`/`for`/`while` sem chaves, sem linha acima de 80 colunas.
- [ ] Nenhum número solto: tudo que aparece mais de uma vez ou tem significado
      tem nome.
- [ ] Cada cast tem comentário (ou foi removido).
- [ ] Funções públicas têm o contrato no `.h`; o "porquê" está nos comentários.
- [ ] Nada de nome de pessoa, data relativa ou código comentado.
- [ ] Interrupção curta, sem `Serial`; dado compartilhado é `volatile`.
- [ ] O `core/` não incluiu nada de hardware.

## Referências

- Michael Barr, *Embedded C Coding Standard* (BARR-C:2018),
  <https://barrgroup.com/coding-standard>.
- James Grenning, *Test-Driven Development for Embedded C* (2011).
- Material da matéria TI00163, C Avançado (aulas de funções, vários arquivos e
  macros).
