# Testa a API de leitura com um servidor de verdade numa porta livre.
# Rode na raiz do repositório (pasta ocupacao-maquinas-academia):
# python3 -m unittest server.test_api -v

import json
import threading
import unittest
import urllib.error
import urllib.request
from datetime import datetime, timedelta, timezone

from server.api import criar_servidor
from server.bridge import MongoSink
from server.bridge_core import RastreadorNos
from server.frame_parser import Frame

T0 = datetime(2026, 11, 25, 12, 0, 0, tzinfo=timezone.utc)


def em(segundos):
    return T0 + timedelta(seconds=segundos)


def pedir(url):
    try:
        with urllib.request.urlopen(url, timeout=5) as r:
            return r.status, json.loads(r.read()), r.headers
    except urllib.error.HTTPError as e:
        with e:  # fecha a resposta de erro
            return e.code, json.loads(e.read()), e.headers


class ApiTests(unittest.TestCase):
    def setUp(self):
        self.r = RastreadorNos(nomes={2: "supino"})
        self.r.receber(Frame(2, 0, 1), em(0))
        self.r.receber(Frame(2, 1, 2), em(5))
        self.r.receber(Frame(3, 0, 9), em(6))
        self.servidor = criar_servidor(self.r, "127.0.0.1", 0)  # porta 0 = qualquer livre
        self.base = f"http://127.0.0.1:{self.servidor.server_address[1]}"
        threading.Thread(target=self.servidor.serve_forever, daemon=True).start()

    def tearDown(self):
        self.servidor.shutdown()
        self.servidor.server_close()

    def test_health(self):
        codigo, corpo, _ = pedir(f"{self.base}/health")
        self.assertEqual((codigo, corpo), (200, {"ok": True}))

    def test_lista_de_maquinas(self):
        codigo, corpo, cab = pedir(f"{self.base}/machines")
        self.assertEqual(codigo, 200)
        self.assertEqual([m["node"] for m in corpo], [2, 3])
        self.assertEqual(corpo[0]["name"], "supino")
        self.assertEqual(corpo[0]["state"], 1)
        self.assertTrue(corpo[0]["online"])
        self.assertEqual(corpo[0]["last_seen"], em(5).isoformat())
        self.assertEqual(cab["Access-Control-Allow-Origin"], "*")

    def test_uma_maquina_e_desconhecida(self):
        self.assertEqual(pedir(f"{self.base}/machines/3")[1]["name"], "maquina_3")
        codigo, corpo, _ = pedir(f"{self.base}/machines/9")
        self.assertEqual(codigo, 404)

    def test_historico_mais_recente_primeiro(self):
        codigo, corpo, _ = pedir(f"{self.base}/machines/2/history")
        self.assertEqual(codigo, 200)
        self.assertEqual([h["state"] for h in corpo], [1, 0])
        self.assertEqual(corpo[0]["ts"], em(5).isoformat())

    def test_historico_respeita_limit(self):
        _, corpo, _ = pedir(f"{self.base}/machines/2/history?limit=1")
        self.assertEqual(len(corpo), 1)
        self.assertEqual(pedir(f"{self.base}/machines/2/history?limit=0")[0], 400)
        self.assertEqual(pedir(f"{self.base}/machines/2/history?limit=abc")[0], 400)

    def test_historico_de_no_sem_dados_e_lista_vazia(self):
        codigo, corpo, _ = pedir(f"{self.base}/machines/7/history")
        self.assertEqual((codigo, corpo), (200, []))

    def test_rota_inexistente_e_404_em_json(self):
        codigo, corpo, _ = pedir(f"{self.base}/nada")
        self.assertEqual(codigo, 404)
        self.assertIn("erro", corpo)

    def test_so_leitura(self):
        req = urllib.request.Request(f"{self.base}/machines", data=b"{}", method="POST")
        with self.assertRaises(urllib.error.HTTPError) as erro:
            urllib.request.urlopen(req, timeout=5)
        self.assertEqual(erro.exception.code, 501)  # POST não é suportado

    def test_falha_da_fonte_de_historico_vira_503(self):
        def quebrada(node, limite):
            raise RuntimeError("banco fora do ar")

        servidor = criar_servidor(self.r, "127.0.0.1", 0, fonte_historico=quebrada)
        threading.Thread(target=servidor.serve_forever, daemon=True).start()
        try:
            base = f"http://127.0.0.1:{servidor.server_address[1]}"
            self.assertEqual(pedir(f"{base}/machines/2/history")[0], 503)
            self.assertEqual(pedir(f"{base}/machines")[0], 200)  # o resto continua no ar
        finally:
            servidor.shutdown()
            servidor.server_close()


class CursorFalso:
    def __init__(self, docs):
        self.docs = list(docs)
        self.ordem = None
        self.max = None

    def sort(self, campo, sentido):
        self.ordem = (campo, sentido)
        self.docs.sort(key=lambda d: d[campo], reverse=(sentido == -1))
        return self

    def limit(self, n):
        self.max = n
        self.docs = self.docs[:n]
        return self

    def __iter__(self):
        return iter(self.docs)


class ColecaoComFind:
    def __init__(self, docs):
        self.docs = docs
        self.consulta = None

    def find(self, filtro, projecao):
        self.consulta = (filtro, projecao)
        return CursorFalso(d for d in self.docs if d["node"] == filtro["node"])


class HistoricoMongoTests(unittest.TestCase):
    def test_historico_do_mongo_filtra_ordena_e_limita(self):
        docs = [{"node": 2, "state": s, "ts": em(i)} for i, s in enumerate([0, 1, 0, 1])]
        docs.append({"node": 3, "state": 1, "ts": em(9)})
        tel = ColecaoComFind(docs)
        sink = MongoSink({"nodes": None, "telemetry": tel})
        resultado = sink.historico(2, 2)
        self.assertEqual([d["ts"] for d in resultado], [em(3), em(2)])
        self.assertEqual(tel.consulta, ({"node": 2}, {"_id": 0}))  # sem o ObjectId


if __name__ == "__main__":
    unittest.main()
