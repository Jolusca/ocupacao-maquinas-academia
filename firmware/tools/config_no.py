#!/usr/bin/env python3
"""Envia um comando de configuracao a um no e mostra a resposta.

Comandos (veja core/command.h):
  id N                          numero do no (1..99); fica gravado na flash
  papel auto|coletor|sensor     papel do no; fica gravado na flash
  info                          mostra a configuracao atual
  limpar                        apaga o que foi gravado (volta ao padrao)

Uso: python3 tools/config_no.py [-p PORTA] COMANDO...
  ex.: python3 tools/config_no.py id 3
       python3 tools/config_no.py -p /dev/ttyACM1 papel sensor

Abre a porta sem desligar DTR/RTS (isso reiniciaria a placa). So mostra as linhas de log "# ";
os quadros que o coletor escreve na serial sao ignorados aqui.
"""
import argparse
import glob
import sys
import time

import serial


def porta_padrao():
    candidatas = sorted(glob.glob("/dev/serial/by-id/*")) + sorted(glob.glob("/dev/ttyACM*"))
    return candidatas[0] if candidatas else None


def main():
    ap = argparse.ArgumentParser(description="Configura um no pela serial.")
    ap.add_argument("-p", "--porta", help="ex.: /dev/ttyACM0 (padrao: a primeira encontrada)")
    ap.add_argument("-t", "--tempo", type=float, default=2.5, help="segundos esperando a resposta (padrao 2,5)")
    ap.add_argument("comando", nargs="+", help="o comando e seus argumentos")
    args = ap.parse_args()

    porta = args.porta or porta_padrao()
    if not porta:
        sys.exit("nenhuma porta serial encontrada")
    s = serial.Serial()
    s.port, s.baudrate, s.timeout = porta, 115200, 0.3
    s.dsrdtr = False
    s.rtscts = False
    s.open()
    s.reset_input_buffer()
    s.write((" ".join(args.comando) + "\n").encode("ascii"))
    s.flush()
    fim = time.time() + args.tempo
    respondeu = False
    while time.time() < fim:
        linha = s.readline().decode("utf-8", "replace").strip()
        # Mostra so as respostas do comando; o log de acompanhamento "up=" polui.
        if linha.startswith("# ") and "up=" not in linha:
            print(linha)
            respondeu = True
    if not respondeu:
        print("sem resposta (a placa esta plugada e rodando o firmware novo?)")
        sys.exit(1)


if __name__ == "__main__":
    main()
