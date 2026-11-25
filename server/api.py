# API de leitura da ponte (só GET), para a página web consultar.
#
#   GET /health                           {"ok": true}
#   GET /machines                         lista com o estado atual de cada nó
#   GET /machines/<n>                     um nó
#   GET /machines/<n>/history?limit=50    últimas mudanças de estado (mais recente primeiro)
#
# Usa só a biblioteca padrão. Por padrão ouve só em 127.0.0.1 (a página abre no próprio
# notebook); use --api-host 0.0.0.0 para outro aparelho da mesma rede acessar.
# O estado atual vem da memória da ponte; o histórico vem do Mongo quando há (fonte_historico)
# e, senão, da memória.

import json
from datetime import datetime
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

LIMITE_PADRAO = 50
LIMITE_MAXIMO = 500


def _para_json(valor):
    if isinstance(valor, datetime):
        return valor.isoformat()
    raise TypeError(f"não serializável: {type(valor).__name__}")


def criar_servidor(rastreador, host="127.0.0.1", porta=8000, fonte_historico=None):
    # fonte_historico(node, limite) -> lista de documentos; padrão: a memória do rastreador.
    historico = fonte_historico or rastreador.historico

    class Handler(BaseHTTPRequestHandler):
        def _enviar(self, codigo, corpo):
            dados = json.dumps(corpo, default=_para_json, ensure_ascii=False).encode("utf-8")
            self.send_response(codigo)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(dados)))
            self.send_header("Access-Control-Allow-Origin", "*")  # a página pode vir de outra porta
            self.end_headers()
            self.wfile.write(dados)

        def do_OPTIONS(self):
            self.send_response(204)
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Access-Control-Allow-Methods", "GET, OPTIONS")
            self.send_header("Content-Length", "0")
            self.end_headers()

        def do_GET(self):
            url = urlparse(self.path)
            partes = [p for p in url.path.split("/") if p]

            if partes == ["health"]:
                return self._enviar(200, {"ok": True})
            if partes == ["machines"]:
                return self._enviar(200, rastreador.snapshot())

            if len(partes) in (2, 3) and partes[0] == "machines" and partes[1].isdigit():
                node = int(partes[1])
                if len(partes) == 2:
                    for doc in rastreador.snapshot():
                        if doc["node"] == node:
                            return self._enviar(200, doc)
                    return self._enviar(404, {"erro": "nó desconhecido"})
                if partes[2] == "history":
                    pedido = parse_qs(url.query).get("limit", [str(LIMITE_PADRAO)])[0]
                    if not pedido.isdigit() or int(pedido) < 1:
                        return self._enviar(400, {"erro": "limit deve ser um inteiro positivo"})
                    limite = min(int(pedido), LIMITE_MAXIMO)
                    try:
                        return self._enviar(200, historico(node, limite))
                    except Exception:
                        return self._enviar(503, {"erro": "histórico indisponível"})

            return self._enviar(404, {"erro": "rota não encontrada"})

        def log_message(self, formato, *args):
            pass  # sem uma linha de log por requisição (a página consulta toda hora)

    return ThreadingHTTPServer((host, porta), Handler)
