# Ponte serial -> Mongo: lê os quadros do gateway (ESP ligada por USB), valida com o parser,
# ignora seq repetido, marca nó offline e grava no banco.
#
# Rode da raiz do repositório:
#   python3 -m server.bridge --dry-run                 # lê a serial e só mostra na tela
#   python3 -m server.bridge --dry-run --simular       # sem placa: gera nós falsos
#   python3 -m server.bridge                           # grava no Mongo (precisa do .env)
#
# Variáveis do .env (nunca vão para o git): MONGODB_URI, opcionalmente MONGODB_USERNAME,
# MONGODB_PASSWORD (preenchem <username>/<password> da URI) e MONGODB_DB (padrão gym_occupancy).

import argparse
import glob
import os
import random
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import quote_plus

from server.bridge_core import (
    OFFLINE_PADRAO_S,
    Atualizacao,
    RastreadorNos,
    linha_para_quadro,
)
from server.frame_parser import FrameFormatError, FrameRangeError

BAUD = 115200


def agora_utc():
    return datetime.now(timezone.utc)


def log(texto):
    print(texto, file=sys.stderr, flush=True)


# ---------------------------------------------------------------- destinos (sinks)

class TelaSink:
    # Só mostra na tela; serve para conferir a ponte sem banco.
    def aplicar(self, a: Atualizacao):
        n = a.no
        estado = "OCUPADA" if n["state"] else "livre"
        situacao = "online" if n["online"] else "OFFLINE"
        marca = " [+telemetry]" if a.telemetria else ""
        print(f"{agora_utc().astimezone():%H:%M:%S} N{n['node']:02d} {n['name']}: {estado}, "
              f"seq={n['seq']}, {situacao}{marca}", flush=True)


class MongoSink:
    def __init__(self, db):
        self._nos = db["nodes"]
        self._telemetria = db["telemetry"]

    @classmethod
    def do_ambiente(cls):
        try:
            from pymongo import MongoClient  # só aqui, para o resto rodar sem pymongo
        except ImportError:
            raise SystemExit("Falta o pymongo: pip install pymongo python-dotenv pyserial")

        try:
            from dotenv import load_dotenv
            aqui = Path(__file__).resolve().parent
            for pasta in (aqui, aqui.parent):
                if (pasta / ".env").exists():
                    load_dotenv(pasta / ".env")
                    break
        except ImportError:
            pass  # sem python-dotenv, vale o que já estiver no ambiente

        uri = os.getenv("MONGODB_URI")
        if not uri:
            raise SystemExit("Defina MONGODB_URI no .env (ou use --dry-run).")
        usuario = os.getenv("MONGODB_USERNAME")
        senha = os.getenv("MONGODB_PASSWORD")
        if usuario and "<username>" in uri:
            uri = uri.replace("<username>", quote_plus(usuario))
        if senha and "<password>" in uri:
            uri = uri.replace("<password>", quote_plus(senha))

        cliente = MongoClient(uri, serverSelectionTimeoutMS=5000)
        return cls(cliente[os.getenv("MONGODB_DB", "gym_occupancy")])

    def aplicar(self, a: Atualizacao):
        # Falha de rede não pode derrubar a ponte; só avisa (sem imprimir a URI nem a mensagem
        # completa do erro, que pode trazer endereço do cluster).
        try:
            self._nos.update_one({"node": a.no["node"]}, {"$set": a.no}, upsert=True)
            if a.telemetria:
                self._telemetria.insert_one(dict(a.telemetria))
        except Exception as erro:
            log(f"erro ao gravar N{a.no['node']:02d} no Mongo ({type(erro).__name__})")


# ---------------------------------------------------------------- fontes de linhas
# Cada fonte devolve linhas de texto; devolve None quando passou um tempo sem linha, para a
# ponte ainda poder checar quem ficou offline.

def porta_padrao():
    candidatas = sorted(glob.glob("/dev/serial/by-id/*")) + sorted(glob.glob("/dev/ttyACM*"))
    return candidatas[0] if candidatas else None


def abrir_serial(porta):
    import serial  # só aqui, para os testes rodarem sem pyserial

    s = serial.Serial()
    s.port = porta
    s.baudrate = BAUD
    s.timeout = 0.5
    s.dsrdtr = False
    s.rtscts = False
    # NÃO mexer em DTR/RTS: desligar reinicia a placa (ver firmware/tools/le_serial.py).
    s.open()
    s.reset_input_buffer()  # descarta o que ficou no buffer (pode vir uma linha cortada)
    return s


def linhas_serial(porta=None):
    import serial

    while True:
        escolhida = porta or porta_padrao()
        if not escolhida:
            log("nenhuma porta serial encontrada; tentando de novo em 2 s")
            time.sleep(2)
            yield None
            continue
        try:
            s = abrir_serial(escolhida)
            log(f"lendo {escolhida}")
            while True:
                bruto = s.readline()
                yield bruto.decode("utf-8", "replace") if bruto else None
        except (serial.SerialException, OSError) as erro:
            # Placa desplugada ou reiniciada: a porta some e pode voltar com outro nome.
            log(f"serial indisponível ({type(erro).__name__}); tentando de novo em 2 s")
            time.sleep(2)
            yield None


def linhas_simuladas(nos=(2, 3, 4), intervalo_s=1.0, vida_s=15.0, silencia_no=4, silencia_apos_s=30.0):
    # Gera o que o gateway imprimiria. O nó "silencia_no" para de enviar depois de
    # "silencia_apos_s" segundos, para ver o offline funcionando.
    estado = {n: 0 for n in nos}
    seq = {n: 0 for n in nos}
    ultimo = {n: None for n in nos}
    inicio = time.monotonic()
    while True:
        t = time.monotonic() - inicio
        for n in nos:
            if n == silencia_no and t > silencia_apos_s:
                continue
            mudou = random.random() < 0.15
            vencido = ultimo[n] is None or t - ultimo[n] >= vida_s
            if mudou or vencido:
                if mudou:
                    estado[n] ^= 1
                yield f"N{n:02d},{estado[n]},{seq[n]}"
                seq[n] = (seq[n] + 1) % 65536
                ultimo[n] = t
        time.sleep(intervalo_s)
        yield None


# ---------------------------------------------------------------- laço principal

def executar(linhas, rastreador, sink, relogio=agora_utc):
    for linha in linhas:
        agora = relogio()
        if linha is not None:
            try:
                quadro = linha_para_quadro(linha)
            except (FrameFormatError, FrameRangeError) as erro:
                log(f"quadro ignorado ({erro}): {linha.strip()[:40]!r}")
                quadro = None
            if quadro is not None:
                sink.aplicar(rastreador.receber(quadro, agora))
        for atualizacao in rastreador.verificar_offline(agora):
            sink.aplicar(atualizacao)


def ler_nomes(pares):
    nomes = {}
    for par in pares or []:
        numero, _, nome = par.partition("=")
        if not numero.isdigit() or not nome:
            raise SystemExit(f"--nome inválido: {par!r} (use N=NOME, ex.: 2=supino)")
        nomes[int(numero)] = nome
    return nomes


def main():
    ap = argparse.ArgumentParser(description="Ponte serial -> Mongo do gateway.")
    ap.add_argument("--porta", help="ex.: /dev/ttyACM0 (padrão: a primeira encontrada)")
    ap.add_argument("--dry-run", action="store_true", help="só mostra na tela, sem gravar no Mongo")
    ap.add_argument("--simular", action="store_true", help="sem placa: gera nós falsos")
    ap.add_argument("--offline-apos", type=float, default=OFFLINE_PADRAO_S,
                    help=f"segundos sem quadro para marcar offline (padrão {OFFLINE_PADRAO_S})")
    ap.add_argument("--nome", action="append", metavar="N=NOME",
                    help="nome da máquina de um nó, ex.: --nome 2=supino (padrão maquina_<n>)")
    args = ap.parse_args()

    sink = TelaSink() if args.dry_run else MongoSink.do_ambiente()
    rastreador = RastreadorNos(args.offline_apos, ler_nomes(args.nome))
    linhas = linhas_simuladas() if args.simular else linhas_serial(args.porta)
    try:
        executar(linhas, rastreador, sink)
    except KeyboardInterrupt:
        log("encerrado")


if __name__ == "__main__":
    main()
