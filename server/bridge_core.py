# Lógica da ponte serial -> Mongo, sem serial e sem banco (testável no PC).
#
# Recebe quadros já validados e decide o que gravar:
#   - nodes: um documento por nó, com o estado atual e se está online;
#   - telemetry: um documento por MUDANÇA de estado (e o primeiro quadro de cada nó).
#     O sinal de vida (a cada 15 s) só atualiza last_seen em nodes, para o histórico
#     não encher de linhas repetidas.

from dataclasses import dataclass
from datetime import datetime, timedelta

from server.frame_parser import Frame, parse_frame

OFFLINE_PADRAO_S = 60  # 4 sinais de vida (15 s) sem chegar; medido em 20/11: 1,5% de perda a 10 m


@dataclass(frozen=True)
class Atualizacao:
    # no: documento para a coleção nodes (upsert por "node").
    # telemetria: documento para a coleção telemetry, ou None se não houve mudança.
    no: dict
    telemetria: dict | None


def linha_para_quadro(linha):
    # in: uma linha da serial do gateway.
    # out: Frame; None se a linha é vazia ou de log ("# ..."); exceção do parser se for lixo.
    texto = linha.strip()
    if not texto or texto.startswith("#"):
        return None
    return parse_frame(texto)


class RastreadorNos:
    def __init__(self, offline_apos_s=OFFLINE_PADRAO_S, nomes=None):
        # nomes: {numero_do_no: "nome da máquina"}; sem entrada vira "maquina_<n>".
        self._limite = timedelta(seconds=offline_apos_s)
        self._nomes = dict(nomes or {})
        self._nos = {}  # node -> {"state", "seq", "last_seen", "online"}

    def nome(self, node):
        return self._nomes.get(node, f"maquina_{node}")

    def _doc_no(self, node):
        e = self._nos[node]
        return {
            "node": node,
            "name": self.nome(node),
            "state": e["state"],
            "seq": e["seq"],
            "last_seen": e["last_seen"],
            "online": e["online"],
        }

    def receber(self, quadro: Frame, agora: datetime):
        # in: quadro válido e o instante de chegada (datetime com fuso).
        # out: Atualizacao com o que gravar.
        anterior = self._nos.get(quadro.node)

        if anterior is not None and anterior["seq"] == quadro.seq:
            # Repetido (o rádio reenviou porque perdeu o ACK): só prova que o nó está vivo.
            anterior["last_seen"] = agora
            anterior["online"] = True
            return Atualizacao(self._doc_no(quadro.node), None)

        mudou = anterior is None or anterior["state"] != quadro.state
        self._nos[quadro.node] = {
            "state": quadro.state,
            "seq": quadro.seq,
            "last_seen": agora,
            "online": True,
        }
        telemetria = None
        if mudou:
            telemetria = {
                "node": quadro.node,
                "state": quadro.state,
                "seq": quadro.seq,
                "ts": agora,
            }
        return Atualizacao(self._doc_no(quadro.node), telemetria)

    def verificar_offline(self, agora: datetime):
        # out: lista de Atualizacao dos nós que passaram do limite sem quadro agora.
        # Cada nó é avisado uma vez; quando voltar a enviar, receber() o marca online de novo.
        saidas = []
        for node, e in self._nos.items():
            if e["online"] and agora - e["last_seen"] > self._limite:
                e["online"] = False
                saidas.append(Atualizacao(self._doc_no(node), None))
        return saidas
