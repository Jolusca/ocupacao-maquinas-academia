# Testes da logica do no (C puro, no PC). Uso: make test
CC      ?= gcc
CFLAGS  ?= -std=c11 -Wall -Wextra -Wpedantic -Werror -g -Icore -Ihal
SRC     := core/frame.c core/occupancy.c core/scheduler.c hal/dist_fake.c
TESTS   := test_frame test_occupancy test_scheduler test_cenarios
BIN     := $(addprefix build/,$(TESTS))
HDR     := core/frame.h core/occupancy.h core/scheduler.h hal/dist_source.h test/minitest.h

.PHONY: test clean

test: $(BIN)
	@fail=0; for t in $(BIN); do echo "=== $$t"; ./$$t || fail=1; done; \
	if [ $$fail -ne 0 ]; then echo; echo "ALGUM TESTE FALHOU"; exit 1; fi; echo; echo "TODOS OS TESTES PASSARAM"

build/%: test/%.c $(SRC) $(HDR)
	@mkdir -p build
	$(CC) $(CFLAGS) -o $@ $< $(SRC)

clean:
	rm -rf build
