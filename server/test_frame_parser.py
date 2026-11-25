# Testa o parser com os vetores compartilhados com o firmware.
# Rode na raiz do repositório (pasta ocupacao-maquinas-academia):
# python3 -m unittest server.test_frame_parser -v

from pathlib import Path
import unittest

from server.frame_parser import FrameFormatError, FrameRangeError, parse_frame


VECTORS = Path(__file__).resolve().parents[1] / "firmware" / "test" / "frames.txt"


def frame_cases():
    with VECTORS.open(encoding="utf-8") as vectors:
        for number, row in enumerate(vectors, start=1):
            row = row.rstrip("\r\n")
            if not row or row.startswith("#"):
                continue

            kind, encoded, node, state, seq = row.split("|")
            line = encoded.replace(r"\r", "\r").replace(r"\n", "\n")
            expected = (int(node), int(state), int(seq)) if kind == "OK" else kind
            yield f"vetor {number}: {line!r}", line, expected

    # Dígitos Unicode são inválidos no protocolo ASCII.
    yield "dígito Unicode", "N02,１,17", "FMT"

    # Sequência enorme deve gerar erro de faixa, sem erro de conversão.
    yield "sequência de 5.000 dígitos", "N02,1," + "9" * 5000, "RANGE"


class FrameParserTests(unittest.TestCase):
    def test_real_parser_contract(self):
        errors = {"FMT": FrameFormatError, "RANGE": FrameRangeError}
        for label, line, expected in frame_cases():
            with self.subTest(frame=label, expected=expected):
                if isinstance(expected, tuple):
                    frame = parse_frame(line)
                    self.assertEqual((frame.node, frame.state, frame.seq), expected)
                else:
                    with self.assertRaises(errors[expected]):
                        parse_frame(line)
