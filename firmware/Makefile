# Testes da logica do no (C puro, no PC). Uso: make test
CC      ?= gcc
CFLAGS  ?= -std=c11 -Wall -Wextra -Wpedantic -Werror -g -Icore
CORE    := core/frame.c core/occupancy.c core/scheduler.c
TESTS   := test_frame test_occupancy test_scheduler
BIN     := $(addprefix build/,$(TESTS))

.PHONY: test clean

test: $(BIN)
	@fail=0; for t in $(BIN); do echo "=== $$t"; ./$$t || fail=1; done; \
	if [ $$fail -ne 0 ]; then echo; echo "ALGUM TESTE FALHOU"; exit 1; fi; echo; echo "TODOS OS TESTES PASSARAM"

build/%: test/%.c $(CORE) core/frame.h core/occupancy.h core/scheduler.h test/minitest.h
	@mkdir -p build
	$(CC) $(CFLAGS) -o $@ $< $(CORE)

clean:
	rm -rf build
