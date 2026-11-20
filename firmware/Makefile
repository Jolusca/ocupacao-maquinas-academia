# Testes da lógica do nó (C puro, no PC) e verificação de estilo.
#   make test           compila e roda os testes
#   make format         aplica o estilo (.clang-format) nos arquivos do hal/, app/ e test/
#   make format-check   só confere o estilo; sai com erro se algum arquivo estiver fora do padrão
CC      ?= gcc
CFLAGS  ?= -std=c11 -Wall -Wextra -Wpedantic -Werror -g -Icore -Ihal
SRC     := core/frame.c core/occupancy.c core/scheduler.c hal/dist_fake.c
TESTS   := test_frame test_occupancy test_scheduler test_cenarios
BIN     := $(addprefix build/,$(TESTS))
HDR     := core/frame.h core/occupancy.h core/scheduler.h hal/dist_fake.h test/minitest.h

# O core/ ainda não entra no formatador: é de quem o implementa e será incluído
# depois da junção das branches.
CLANG_FORMAT ?= clang-format
FORMAT_FILES := $(wildcard hal/*.h hal/*.c hal/*.cpp app/*.h test/*.h test/*.c)
FORMAT_INO   := app/app.ino

.PHONY: test clean format format-check

test: $(BIN)
	@fail=0; for t in $(BIN); do echo "=== $$t"; ./$$t || fail=1; done; \
	if [ $$fail -ne 0 ]; then echo; echo "ALGUM TESTE FALHOU"; exit 1; fi; echo; echo "TODOS OS TESTES PASSARAM"

build/%: test/%.c $(SRC) $(HDR)
	@mkdir -p build
	$(CC) $(CFLAGS) -o $@ $< $(SRC)

format:
	$(CLANG_FORMAT) -i $(FORMAT_FILES)
	$(CLANG_FORMAT) --assume-filename=app/app.cpp < $(FORMAT_INO) > $(FORMAT_INO).tmp && mv $(FORMAT_INO).tmp $(FORMAT_INO)

format-check:
	$(CLANG_FORMAT) --dry-run --Werror $(FORMAT_FILES)
	$(CLANG_FORMAT) --assume-filename=app/app.cpp < $(FORMAT_INO) | diff -u $(FORMAT_INO) - > /dev/null

clean:
	rm -rf build
