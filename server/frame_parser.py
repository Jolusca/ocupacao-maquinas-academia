# Parser dos quadros ASCII do firmware.

from dataclasses import dataclass
import re


@dataclass(frozen=True)
class Frame:
    node: int
    state: int
    seq: int


class FrameFormatError(ValueError):
    """A linha não segue o formato ASCII do quadro."""


class FrameRangeError(ValueError):
    """Um campo numérico está fora da faixa do protocolo."""


_FRAME_PATTERN = re.compile(r"N([0-9]{2}),([0-9]+),([0-9]+)(?:\r?\n)?")


def _parse_bounded_number(digits, maximum, field):
    # in: dígitos ASCII, limite como texto e nome do campo.
    # out: inteiro dentro do limite; FrameRangeError se exceder.
    # Compara como texto para evitar converter números enormes.
    normalized = digits.lstrip("0") or "0"
    if len(normalized) > len(maximum) or (
        len(normalized) == len(maximum) and normalized > maximum
    ):
        raise FrameRangeError(f"{field} excede {maximum}")
    return int(normalized)


def parse_frame(line):
    # in: texto como "N02,1,17", com LF/CRLF final opcional.
    # out: Frame(node=2, state=1, seq=17); exceção se inválido.
    match = _FRAME_PATTERN.fullmatch(line)
    if match is None:
        raise FrameFormatError("Esperado N<dois dígitos>,<dígitos>,<dígitos>")

    node_digits, state_digits, seq_digits = match.groups()
    node = int(node_digits)
    if node == 0:
        raise FrameRangeError("node deve estar entre 1 e 99")
    state = _parse_bounded_number(state_digits, "1", "state")
    seq = _parse_bounded_number(seq_digits, "65535", "seq")
    return Frame(node=node, state=state, seq=seq)