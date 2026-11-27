# Testa a lógica da ponte sem serial e sem banco.
# Rode na raiz do repositório (pasta ocupacao-maquinas-academia):
# python3 -m unittest server.test_bridge -v

import unittest
from datetime import datetime, timedelta, timezone

from server.bridge import MongoSink, executar, montar_uri
from server.bridge_core import RastreadorNos, linha_para_quadro
from server.frame_parser import Frame, FrameFormatError, FrameRangeError

T0 = datetime(2026, 11, 25, 12, 0, 0, tzinfo=timezone.utc)


def em(segundos):
    return T0 + timedelta(seconds=segundos)


class LinhaParaQuadroTests(unittest.TestCase):
    def test_quadro_valido(self):
        self.assertEqual(linha_para_quadro("N02,1,17\r\n"), Frame(node=2, state=1, seq=17))

    def test_log_e_linha_vazia_sao_ignorados(self):
        self.assertIsNone(linha_para_quadro("# up=1234 rssi=-72"))
        self.assertIsNone(linha_para_quadro("   \n"))

    def test_lixo_levanta_erro_do_parser(self):
        with self.assertRaises(FrameFormatError):
            linha_para_quadro("ola mundo")
        with self.assertRaises(FrameRangeError):
            linha_para_quadro("N02,2,1")


class RastreadorTests(unittest.TestCase):
    def setUp(self):
        self.r = RastreadorNos(offline_apos_s=60)

    def test_primeiro_quadro_cria_no_e_telemetria(self):
        a = self.r.receber(Frame(2, 0, 0), em(0))
        self.assertEqual(a.no["node"], 2)
        self.assertEqual(a.no["name"], "maquina_2")
        self.assertTrue(a.no["online"])
        self.assertEqual(a.telemetria, {"node": 2, "state": 0, "seq": 0, "ts": em(0)})

    def test_sinal_de_vida_so_atualiza_last_seen(self):
        self.r.receber(Frame(2, 1, 5), em(0))
        a = self.r.receber(Frame(2, 1, 6), em(15))
        self.assertIsNone(a.telemetria)
        self.assertEqual(a.no["last_seen"], em(15))
        self.assertEqual(a.no["seq"], 6)

    def test_mudanca_de_estado_gera_telemetria(self):
        self.r.receber(Frame(2, 0, 1), em(0))
        a = self.r.receber(Frame(2, 1, 2), em(3))
        self.assertEqual(a.telemetria["state"], 1)
        self.assertEqual(a.no["state"], 1)

    def test_seq_repetido_nao_gera_telemetria_nem_muda_estado(self):
        self.r.receber(Frame(2, 0, 1), em(0))
        self.r.receber(Frame(2, 1, 2), em(3))
        a = self.r.receber(Frame(2, 1, 2), em(4))  # retry do rádio
        self.assertIsNone(a.telemetria)
        self.assertEqual(a.no["last_seen"], em(4))

    def test_seq_que_da_a_volta_conta_como_novo(self):
        self.r.receber(Frame(2, 0, 65535), em(0))
        a = self.r.receber(Frame(2, 1, 0), em(1))
        self.assertIsNotNone(a.telemetria)

    def test_nos_sao_independentes(self):
        self.r.receber(Frame(2, 1, 7), em(0))
        a = self.r.receber(Frame(3, 1, 7), em(1))  # mesmo seq, outro nó: não é repetido
        self.assertIsNotNone(a.telemetria)

    def test_offline_depois_do_limite_e_uma_vez_so(self):
        self.r.receber(Frame(2, 1, 1), em(0))
        self.assertEqual(self.r.verificar_offline(em(60)), [])  # no limite ainda vale
        saidas = self.r.verificar_offline(em(61))
        self.assertEqual(len(saidas), 1)
        self.assertFalse(saidas[0].no["online"])
        self.assertEqual(saidas[0].no["state"], 1)  # guarda o último estado conhecido
        self.assertEqual(self.r.verificar_offline(em(120)), [])  # não repete o aviso

    def test_volta_a_ficar_online(self):
        self.r.receber(Frame(2, 1, 1), em(0))
        self.r.verificar_offline(em(100))
        a = self.r.receber(Frame(2, 1, 2), em(110))
        self.assertTrue(a.no["online"])

    def test_snapshot_ordenado_e_copia(self):
        self.r.receber(Frame(3, 1, 1), em(0))
        self.r.receber(Frame(2, 0, 1), em(0))
        lista = self.r.snapshot()
        self.assertEqual([d["node"] for d in lista], [2, 3])
        lista[0]["state"] = 99  # mexer na cópia não altera o rastreador
        self.assertEqual(self.r.snapshot()[0]["state"], 0)

    def test_historico_em_memoria_mais_recente_primeiro(self):
        self.r.receber(Frame(2, 0, 1), em(0))
        self.r.receber(Frame(2, 0, 2), em(15))  # sinal de vida: não entra no histórico
        self.r.receber(Frame(2, 1, 3), em(20))
        h = self.r.historico(2)
        self.assertEqual([d["state"] for d in h], [1, 0])
        self.assertEqual(len(self.r.historico(2, limite=1)), 1)
        self.assertEqual(self.r.historico(9), [])

    def test_nomes_personalizados(self):
        r = RastreadorNos(nomes={2: "supino"})
        self.assertEqual(r.receber(Frame(2, 0, 0), em(0)).no["name"], "supino")
        self.assertEqual(r.receber(Frame(3, 0, 0), em(0)).no["name"], "maquina_3")


class ColetorSink:
    def __init__(self):
        self.recebidas = []

    def aplicar(self, a):
        self.recebidas.append(a)


class ExecutarTests(unittest.TestCase):
    def test_fluxo_completo_com_lixo_no_meio(self):
        horas = iter([em(0), em(1), em(2), em(3), em(4), em(100)])
        sink = ColetorSink()
        linhas = ["# boot", "N02,0,0", "lixo", "N02,0,0", "N02,1,1", None]
        executar(iter(linhas), RastreadorNos(60), sink, relogio=lambda: next(horas))
        # 1) quadro novo, 2) repetido (só vida), 3) mudança, 4) offline ao passar de 60 s
        resumo = [(a.no["state"], a.no["online"], a.telemetria is not None) for a in sink.recebidas]
        self.assertEqual(resumo, [(0, True, True), (0, True, False), (1, True, True), (1, False, False)])


class ColecaoFalsa:
    def __init__(self):
        self.upserts = []
        self.insercoes = []

    def update_one(self, filtro, mudanca, upsert=False):
        self.upserts.append((filtro, mudanca, upsert))

    def insert_one(self, doc):
        self.insercoes.append(doc)


class CursorFalso:
    # Imita find().sort().limit() do pymongo, que devolve datas SEM fuso (naive, em UTC).
    def __init__(self, docs):
        self._docs = docs

    def sort(self, *a, **k):
        return self

    def limit(self, n):
        self._docs = self._docs[:n]
        return self

    def __iter__(self):
        return iter(self._docs)


class ColecaoComHistorico(ColecaoFalsa):
    def __init__(self, docs):
        super().__init__()
        self._docs = docs

    def find(self, *a, **k):
        return CursorFalso([dict(d) for d in self._docs])


class MongoSinkTests(unittest.TestCase):
    def setUp(self):
        self.nos, self.tel = ColecaoFalsa(), ColecaoFalsa()
        self.sink = MongoSink({"nodes": self.nos, "telemetry": self.tel})

    def test_historico_devolve_ts_em_utc_com_fuso(self):
        # O Mongo guarda em UTC mas o pymongo devolve a data sem fuso; a página leria como hora local.
        naive = datetime(2026, 11, 27, 14, 15, 12, 779000)
        sink = MongoSink({"nodes": self.nos, "telemetry": ColecaoComHistorico([
            {"node": 2, "state": 1, "seq": 3, "ts": naive}])})
        ts = sink.historico(2)[0]["ts"]
        self.assertEqual(ts.tzinfo, timezone.utc)
        self.assertEqual(ts.isoformat(), "2026-11-27T14:15:12.779000+00:00")

    def test_historico_mantem_ts_que_ja_tem_fuso(self):
        com_fuso = datetime(2026, 11, 27, 14, 0, 0, tzinfo=timezone.utc)
        sink = MongoSink({"nodes": self.nos, "telemetry": ColecaoComHistorico([
            {"node": 2, "state": 0, "seq": 1, "ts": com_fuso}])})
        self.assertEqual(sink.historico(2)[0]["ts"], com_fuso)

    def test_grava_no_por_upsert_e_telemetria(self):
        a = RastreadorNos().receber(Frame(2, 1, 4), em(0))
        self.sink.aplicar(a)
        self.assertEqual(self.nos.upserts[0][0], {"node": 2})
        self.assertTrue(self.nos.upserts[0][2])
        self.assertEqual(self.tel.insercoes[0]["state"], 1)

    def test_sem_mudanca_nao_insere_telemetria(self):
        r = RastreadorNos()
        r.receber(Frame(2, 1, 4), em(0))
        self.sink.aplicar(r.receber(Frame(2, 1, 5), em(15)))
        self.assertEqual(self.tel.insercoes, [])

    def test_erro_do_banco_nao_derruba_a_ponte(self):
        class Quebrada(ColecaoFalsa):
            def update_one(self, *a, **k):
                raise RuntimeError("banco fora do ar")

        sink = MongoSink({"nodes": Quebrada(), "telemetry": self.tel})
        sink.aplicar(RastreadorNos().receber(Frame(2, 1, 4), em(0)))  # não levanta


class MontarUriTests(unittest.TestCase):
    def test_marcadores_do_atlas(self):
        env = {"MONGODB_URI": "mongodb+srv://<db_username>:<db_password>@cluster.exemplo.net/?x=1",
               "MONGODB_USERNAME": "ponte", "MONGODB_PASSWORD": "p@ss/w:rd"}
        self.assertEqual(montar_uri(env), "mongodb+srv://ponte:p%40ss%2Fw%3Ard@cluster.exemplo.net/?x=1")

    def test_marcadores_antigos(self):
        env = {"MONGODB_URI": "mongodb+srv://<username>:<password>@c.net/",
               "MONGODB_USERNAME": "u", "MONGODB_PASSWORD": "s"}
        self.assertEqual(montar_uri(env), "mongodb+srv://u:s@c.net/")

    def test_uri_completa_nao_e_alterada(self):
        env = {"MONGODB_URI": "mongodb+srv://u:s@c.net/"}
        self.assertEqual(montar_uri(env), "mongodb+srv://u:s@c.net/")

    def test_monta_com_usuario_e_senha_no_host_padrao(self):
        uri = montar_uri({"MONGODB_USERNAME": "u", "MONGODB_PASSWORD": "s"})
        self.assertEqual(uri, "mongodb+srv://u:s@ocupacaomaquinas.wsoskab.mongodb.net/")

    def test_sem_credenciais_pede_o_env(self):
        with self.assertRaises(SystemExit):
            montar_uri({})


if __name__ == "__main__":
    unittest.main()
