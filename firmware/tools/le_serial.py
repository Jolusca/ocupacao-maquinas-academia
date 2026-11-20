#!/usr/bin/env python3
"""Le a serial do gateway e confere o que chega.

- mostra os quadros N<id>,<estado>,<seq>; linhas que comecam com "# " sao log (use -v para ver);
- por no: conta quadros e procura lacunas no seq (quadros perdidos);
- abre a porta SEM mexer em DTR/RTS e avisa se a placa reiniciou ao abrir (o uptime do log
  "# up=" volta a zero ou aparece "# boot").

Uso: python3 tools/le_serial.py [PORTA] [-t SEGUNDOS] [-v]
"""
import argparse
import glob
import re
import sys
import time

import serial

FRAME = re.compile(r"^N(\d{2}),([01]),(\d{1,5})$")
UP = re.compile(r"\bup=(\d+)")


def porta_padrao():
    candidatas = sorted(glob.glob("/dev/serial/by-id/*")) + sorted(glob.glob("/dev/ttyACM*"))
    return candidatas[0] if candidatas else None


def abrir(porta):
    s = serial.Serial()
    s.port = porta
    s.baudrate = 115200
    s.timeout = 0.5
    s.dsrdtr = False
    s.rtscts = False
    s.dtr = False   # definidos antes do open(): a porta abre sem acionar o reset da placa
    s.rts = False
    s.open()
    return s


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("porta", nargs="?", help="ex.: /dev/ttyACM0 (padrao: a primeira encontrada)")
    ap.add_argument("-t", "--tempo", type=float, default=30, help="segundos de leitura (padrao 30)")
    ap.add_argument("-v", "--logs", action="store_true", help="mostrar tambem as linhas de log '# '")
    args = ap.parse_args()

    porta = args.porta or porta_padrao()
    if not porta:
        sys.exit("nenhuma porta serial encontrada (/dev/ttyACM*)")
    s = abrir(porta)
    print(f"lendo {porta} por {args.tempo:.0f} s ...")

    inicio = time.time()
    ultimo_up = None
    reinicio = False
    por_no = {}   # no -> {"n": quadros, "ultimo": seq, "lacunas": perdidos, "dup": repetidos}
    invalidas = 0

    while time.time() - inicio < args.tempo:
        linha = s.readline().decode("utf-8", "replace").strip()
        if not linha:
            continue
        if linha.startswith("#"):
            if "boot" in linha:
                reinicio = True
                print("   (a placa reiniciou: apareceu '# boot')")
            m = UP.search(linha)
            if m:
                up = int(m.group(1))
                if ultimo_up is not None and up < ultimo_up:
                    reinicio = True
                    print("   (a placa reiniciou: o uptime voltou a zero)")
                ultimo_up = up
            if args.logs:
                print(f"{time.time() - inicio:6.1f}s  {linha}")
            continue
        m = FRAME.match(linha)
        if not m:
            invalidas += 1
            print(f"{time.time() - inicio:6.1f}s  linha fora do contrato: {linha!r}")
            continue
        no, estado, seq = int(m.group(1)), int(m.group(2)), int(m.group(3))
        d = por_no.setdefault(no, {"n": 0, "ultimo": None, "lacunas": 0, "dup": 0})
        if d["ultimo"] is not None:
            salto = (seq - d["ultimo"]) % 65536
            if salto == 0:
                d["dup"] += 1
            elif salto > 1:
                d["lacunas"] += salto - 1
        d["ultimo"] = seq
        d["n"] += 1
        print(f"{time.time() - inicio:6.1f}s  N{no:02d}  {'OCUPADA' if estado else 'livre  '}  seq={seq}")

    print("\n--- resumo ---")
    for no, d in sorted(por_no.items()):
        print(f"N{no:02d}: {d['n']} quadros, {d['lacunas']} perdidos por lacuna de seq, {d['dup']} repetidos")
    if not por_no:
        print("nenhum quadro recebido")
    print(f"linhas fora do contrato: {invalidas}")
    print("reinicio ao abrir a porta: " + ("SIM (ajustar DTR/RTS)" if reinicio else "nao"))


if __name__ == "__main__":
    main()
