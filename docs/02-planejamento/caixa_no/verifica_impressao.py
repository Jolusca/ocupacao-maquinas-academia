#!/usr/bin/env python3
"""Verificador de impressão FDM: fatia cada peça na posição de impressão e procura pontes e overhangs.

Regra usada (Hubs/Protolabs/Prusa): overhang até ~45 graus sem suporte, ponte (vão sem apoio) de até ~5 mm.
Em cada camada (0,2 mm) calcula a parte que NÃO tem apoio na camada de baixo (já descontado o 45 graus, que é 0,2 mm por camada) e,
para cada região sem apoio, o "alcance": a maior distância dela até a camada de baixo. Ponte de 5 mm => alcance de 2,5 mm.

Uso: python3 verifica_impressao.py     (precisa de: trimesh, shapely, numpy, scipy, networkx, manifold3d, matplotlib)
"""
import sys
import tempfile
from pathlib import Path

import numpy as np
from shapely.geometry import MultiPoint, Point
from shapely.ops import unary_union

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).parent))
import caixa_no as C   # noqa: E402

H = 0.2                 # altura de camada
ALCANCE_MAX = 2.5       # mm: ponte de 5 mm
AREA_MIN = 0.6          # mm²: ignora ruído


def camadas(mesh):
    zs = np.arange(H / 2, mesh.bounds[1][2], H)
    out = []
    for p in mesh.section_multiplane([0, 0, 0], [0, 0, 1], zs):
        out.append(unary_union(p.polygons_full) if p is not None else Point(0, 0).buffer(0))
    return zs, out


def alcance(regiao, apoio):
    """Maior distância de um ponto da região até o apoio (amostra o contorno e uma grade interna)."""
    pts = [Point(c) for c in regiao.exterior.coords]
    x0, y0, x1, y1 = regiao.bounds
    for x in np.arange(x0, x1, 0.5):
        for y in np.arange(y0, y1, 0.5):
            if regiao.contains(Point(x, y)):
                pts.append(Point(x, y))
    return max((apoio.distance(p) for p in pts), default=0.0)


def analisa(nome, mesh):
    zs, cam = camadas(mesh)
    eventos = []
    for i in range(1, len(cam)):
        if cam[i].is_empty:
            continue
        sem_apoio = cam[i].difference(cam[i - 1].buffer(H))      # 45 graus: 1 camada de overhang
        geoms = list(sem_apoio.geoms) if hasattr(sem_apoio, "geoms") else [sem_apoio]
        for g in geoms:
            if g.area < AREA_MIN or g.geom_type != "Polygon":
                continue
            eventos.append((float(zs[i]), g.centroid.x, g.centroid.y, alcance(g, cam[i - 1].buffer(H)), g.area))
    # junta camadas seguidas na mesma região e guarda o pior alcance
    grupos = []
    for z, x, y, a, ar in eventos:
        for g in grupos:
            if abs(g["x"] - x) < 6 and abs(g["y"] - y) < 6:
                g["a"], g["z"] = max(g["a"], a), g["z"] if a < g["a"] else z
                break
        else:
            grupos.append({"x": x, "y": y, "a": a, "z": z})
    ruins = sorted([g for g in grupos if g["a"] > ALCANCE_MAX], key=lambda g: -g["a"])
    return ruins, len(cam)


if __name__ == "__main__":
    out = Path(tempfile.mkdtemp())
    base, lid, comp, dados = C.main(out)
    from trimesh import load
    pecas = {"base": base, "tampa_N01": load(out / "tampa_N01.stl"), "teste_inserto": load(out / "teste_inserto.stl")}
    pior = 0.0
    for nome, m in pecas.items():
        ruins, n = analisa(nome, m)
        print(f"== {nome}: {n} camadas de {H} mm; regiões com ponte/overhang acima de {2 * ALCANCE_MAX:g} mm: {len(ruins)}")
        for g in ruins:
            pior = max(pior, g["a"])
            print(f"   x={g['x']:.1f} y={g['y']:.1f} z={g['z']:.1f} mm  vão sem apoio de ~{2 * g['a']:.1f} mm")
    sys.exit(0)
