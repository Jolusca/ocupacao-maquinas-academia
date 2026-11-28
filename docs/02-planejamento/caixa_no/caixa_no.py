#!/usr/bin/env python3
"""Caixa do nó de ocupação (placa perfurada + HC-SR04) - modelo paramétrico, v1 (rascunho de encaixe).

Gera base.stl e tampa.stl e confere se nenhum componente real encosta na caixa.
Uso: python3 caixa_no.py [PASTA_DE_SAIDA]        (precisa de: trimesh, manifold3d, numpy, matplotlib)

Eixos (mm), em coordenadas EXTERNAS da caixa:
  x = comprimento (a placa fica na ponta x=0, o sensor na outra)
  y = largura     (a parede y=0 é a do USB-C)
  z = profundidade, a partir da FRENTE (z=0 é a face de fora por onde o sensor olha; a tampa fica em cima)
A base é impressa com a frente (z=0) apoiada na mesa; a tampa, com a face de fora apoiada na mesa.

Tudo o que é medida está no bloco PARÂMETROS. Itens marcados [CONFIRMAR] são suposições a medir com paquímetro.
"""
import json
import sys
from pathlib import Path

import numpy as np
import trimesh
from matplotlib.font_manager import FontProperties
from matplotlib.textpath import TextPath
from shapely import affinity
from shapely.geometry import Polygon

# ============================== PARÂMETROS ==============================
# --- caixa
WALL = 2.0              # parede lateral
FLOOR = 2.0             # frente (por onde o sensor olha)
LID_T = 2.0             # tampa
INNER_D = 26.0          # profundidade interna (da frente até a tampa)  [CONFIRMAR com a placa montada]

# --- placa perfurada (15 x 12 furos), medida pelo Marcos
BOARD_L, BOARD_W, BOARD_T = 45.0, 33.0, 1.6
BOARD_H_TOTAL = 21.0    # da face de baixo da placa até o topo do C1 (altura medida: 2,1 cm)
STANDOFF = 3.0          # calço sob a placa (folga para as soldas e o corpo do R4)
PITCH = 2.54
M_COL_A = 4.7           # [CONFIRMAR] margem da borda da placa até o centro da coluna A (lado oposto ao sensor)
M_ROW_O = 2.5           # [CONFIRMAR] margem da borda do USB até o centro da linha O
USB_EDGE_GAP = 0.5      # folga entre a borda do USB da placa e a parede (para o plugue encaixar até o fundo)

# --- ESP32-C6 SuperMini soldada direto
ESP_GAP = 2.6           # vão entre a placa perfurada e a placa da ESP (Marcos: 2 mm; foto de 28/11: 2,2 a 3 mm)
ESP_PCB_T = 1.2         # espessura da placa da ESP (foto de 28/11: 1,2 a 1,6 mm)
ESP_W, ESP_L = 18.0, 22.5
USBC_H, USBC_W = 3.2, 9.0   # conector USB-C da ESP (altura, largura)
USBC_PROTRUDE = 0.7     # quanto o conector passa da borda da ESP

# --- C1 (eletrolítico em pé, K·O / K·R) e a posição dele na placa
C1_D = 10.0
C1_COL_IDX = 10         # coluna K = 11ª coluna (índice 10)
C1_ROW_CENTER = 1.5     # centro entre as linhas O e R (1,5 passos a partir da linha O)

# --- sensor HC-SR04 (datasheet)
S_L, S_W = 46.5, 21.0   # datasheet 45 x 20; na foto de 28/11 a placa mediu ~46,5 x 20,6 (+-1): usei o maior
S_PCB_T = 1.6
S_TOTAL_T = 15.0        # da frente dos cilindros até as costas da placa
TX_D = 16.0
TX_CC = 26.0            # [CONFIRMAR] distância entre os centros dos cilindros
HOLE_D = 16.8           # furo dos cilindros (folga de 0,4 mm de cada lado)
HOLE_SLOT = 1.2         # o furo é alongado em x por esse tanto: tolera +-0,6 mm no espaçamento dos cilindros (26 a 27 mm nas fotos)
HOLE_CHAMFER = 1.0      # chanfro por fora, para não cortar o cone de som
SENSOR_RECESS = 0.0     # quanto a frente dos cilindros fica atrás da face de fora
# conector Dupont do sensor: bloco único de 4 pinos, rígido, deitado no plano da placa e saindo pela borda LONGA (foto de 28/11)
CONN_W, CONN_OUT, CONN_T = 10.2, 12.0, 3.0   # largura (4 x 2,54), quanto passa da borda [CONFIRMAR com régua], espessura
CONN_LANE = 15.0        # faixa livre ao lado do sensor: CONN_OUT + ~3 mm para o fio sair do bloco e dobrar

# --- layout interno (x a partir da parede interna)
BOARD_X0 = 1.0
CABLE_GAP = 22.0        # espaço do cabo entre a placa e o sensor
END_CLEAR = 1.0
SIDE_CLEAR = 1.5        # folga na lateral oposta ao USB

# --- suportes, parafusos e abertura do USB
SENSOR_POST = 3.5       # lado do pilar sob cada canto do sensor
BOARD_POST = 4.5
SCREW_POST_D, INSERT_D, INSERT_DEPTH = 7.0, 4.2, 7.0   # inserto de rosca a quente M3
SCREW_HOLE_D, SCREW_CBORE_D, SCREW_CBORE_DEPTH = 3.4, 6.4, 1.2
PRESS = 3.0             # lado dos pilares que prendem as placas por cima
PRESS_GAP = 0.2
LIP_T, LIP_H, LIP_CLEAR = 1.2, 1.5, 0.3                # aba de encaixe da tampa
USB_OPEN_W, USB_OPEN_H, USB_OPEN_R = 14.0, 10.0, 1.5   # abertura: plugue do padrão USB-C é 12,35 x 6,5 mm; folga vertical de +-1,75 mm
USB_PLUG_W, USB_PLUG_H, USB_PLUG_LEN = 12.35, 6.5, 25.0

# --- ímãs de fixação (na tampa, que é o fundo da caixa; ficam na ponta do SENSOR, longe da antena da ESP)
MAG_D, MAG_H = 10.0, 2.0            # [CONFIRMAR] ímã de neodímio em disco 10 x 2 mm
MAG_CLEAR_D, MAG_CLEAR_H = 0.2, 0.2  # folga do bolso (o ímã é colado)
MAG_BOSS_D, MAG_BOSS_H = 14.0, 2.0   # reforço por dentro da tampa, para sobrar parede atrás do ímã
MAG_X_FROM_SENSOR_END = 12.0         # distância do centro do ímã até a ponta do sensor
ANTENNA_ZONE_LEN = 7.0               # comprimento da região da antena na ponta da ESP oposta ao USB
ANTENNA_MIN_DIST = 25.0              # distância mínima do ímã até essa região

# --- alívio de tração do cabo USB (aba externa com 2 fendas para abraçadeira de nylon)
TIE_TAB_HALF, TIE_TAB_LEN, TIE_TAB_H = 12.0, 14.0, 6.5
TIE_SLOT_DX = 8.6                    # as fendas ficam a 8,6 mm do eixo do plugue (que tem meia largura de 6,2)
TIE_SLOT_X, TIE_SLOT_Y = 2.0, 3.8    # espessura x largura da fita (abraçadeira de até 3,6 mm)
TIE_SLOT_AT = 9.0                    # distância da fenda até a parede

# --- número do nó gravado no lado de fora da tampa
TEXT_H, TEXT_DEPTH = 8.0, 0.6
NODE_LABELS = ("N01", "N02")

SECTIONS = 64
# =======================================================================

# ---- cotas derivadas
W_IN = max(USB_EDGE_GAP + BOARD_W + SIDE_CLEAR, CONN_LANE + S_W + 0.5)
SENSOR_X0 = BOARD_X0 + BOARD_L + CABLE_GAP
L_IN = SENSOR_X0 + S_L + END_CLEAR
L_EXT, W_EXT = L_IN + 2 * WALL, W_IN + 2 * WALL
Z_FLOOR = FLOOR
Z_TOP_BASE = FLOOR + INNER_D
H_EXT = Z_TOP_BASE + LID_T
Z_BOARD = Z_FLOOR + STANDOFF                      # face de baixo da placa
Z_BOARD_TOP = Z_BOARD + BOARD_T
Z_ESP_PCB0 = Z_BOARD_TOP + ESP_GAP
Z_USBC_C = Z_ESP_PCB0 + ESP_PCB_T + USBC_H / 2    # centro do USB-C
Z_C1_TOP = Z_BOARD + BOARD_H_TOTAL
Z_SENSOR_FRONT = S_TOTAL_T - S_PCB_T - SENSOR_RECESS    # face da frente da placa do sensor
Z_SENSOR_BACK = Z_SENSOR_FRONT + S_PCB_T


def X(x_in): return WALL + x_in
def Y(y_in): return WALL + y_in


def box(x0, x1, y0, y1, z0, z1):
    m = trimesh.creation.box(extents=[x1 - x0, y1 - y0, z1 - z0])
    m.apply_translation([(x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2])
    return m


def cyl(cx, cy, z0, z1, r, sections=SECTIONS):
    m = trimesh.creation.cylinder(radius=r, height=z1 - z0, sections=sections)
    m.apply_translation([cx, cy, (z0 + z1) / 2])
    return m


def cone(cx, cy, z0, radius, height, sections=SECTIONS):
    """Cone com a base (raio `radius`) em z=z0 e a ponta em z=z0+height."""
    m = trimesh.creation.cone(radius=radius, height=height, sections=sections)
    assert abs(m.bounds[0][2]) < 1e-6 and abs(m.bounds[1][2] - height) < 1e-6, "cone do trimesh mudou de convenção"
    m.apply_translation([cx, cy, z0])
    return m


def rounded_box_yz(x0, x1, ycent, zc, w, h, r, thick_y):
    """Prisma no eixo y com seção arredondada (largura w em x, altura h em z)."""
    parts = [box(x0, x1, ycent - thick_y / 2, ycent + thick_y / 2, zc - h / 2 + r, zc + h / 2 - r),
             box(x0 + r, x1 - r, ycent - thick_y / 2, ycent + thick_y / 2, zc - h / 2, zc + h / 2)]
    for cx in (x0 + r, x1 - r):
        for cz in (zc - h / 2 + r, zc + h / 2 - r):
            c = trimesh.creation.cylinder(radius=r, height=thick_y, sections=24)
            c.apply_transform(trimesh.transformations.rotation_matrix(np.pi / 2, [1, 0, 0]))
            c.apply_translation([cx, ycent, cz])
            parts.append(c)
    return trimesh.boolean.union(parts, engine="manifold")


def U(*meshes): return trimesh.boolean.union(list(meshes), engine="manifold")
def D(a, *bs): return trimesh.boolean.difference([a, *bs], engine="manifold")


def overlap(a, b):
    try:
        m = trimesh.boolean.intersection([a, b], engine="manifold")
        return 0.0 if m.is_empty else float(m.volume)
    except Exception:
        return 0.0


# ---- posições
sensor_cx, sensor_cy = X(SENSOR_X0 + S_L / 2), Y(CONN_LANE + S_W / 2)     # sensor encostado na parede de cima; a faixa do conector fica do lado do USB
hole_xs = [sensor_cx - TX_CC / 2, sensor_cx + TX_CC / 2]
usb_x = X(BOARD_X0 + M_COL_A + 4 * PITCH)         # o USB-C fica no centro da ESP (coluna E)
# 3 parafusos: o 4o canto (fim do sensor, lado de cima) é ocupado pela placa do sensor, que agora encosta ali
screw_pts = [(X(58.0), Y(3.5)), (X(58.0), Y(W_IN - 3.5)), (X(L_IN - 3.5), Y(3.5))]
board_x0, board_x1 = X(BOARD_X0), X(BOARD_X0 + BOARD_L)
board_y0, board_y1 = Y(USB_EDGE_GAP), Y(USB_EDGE_GAP + BOARD_W)
sensor_x0, sensor_x1 = X(SENSOR_X0), X(SENSOR_X0 + S_L)
sensor_y0, sensor_y1 = sensor_cy - S_W / 2, sensor_cy + S_W / 2
esp_y0 = board_y0 + M_ROW_O - (ESP_L - 9 * PITCH) / 2 - 0.2       # a ESP começa um pouco antes da linha O
esp_x0 = usb_x - ESP_W / 2
mag_cx = [X(SENSOR_X0 + MAG_X_FROM_SENSOR_END), X(SENSOR_X0 + S_L - MAG_X_FROM_SENSOR_END)]
mag_cy = Y(W_IN / 2)


def text_mesh(label):
    """Texto em relevo negativo (para gravar na face de fora da tampa), centrado sobre a região da placa."""
    tp = TextPath((0, 0), label, size=10, prop=FontProperties(family="DejaVu Sans", weight="bold"))
    shape = Polygon()
    for ring in tp.to_polygons(closed_only=True):
        shape = shape.symmetric_difference(Polygon(ring).buffer(0))     # preenchimento par-ímpar: o miolo do 0 fica vazado
    x0, y0, x1, y1 = shape.bounds
    k = TEXT_H / (y1 - y0)
    shape = affinity.scale(shape, k, k, origin=(x0, y0))
    x0, y0, x1, y1 = shape.bounds
    shape = affinity.translate(shape, X(BOARD_X0 + BOARD_L / 2) - (x0 + x1) / 2, W_EXT / 2 - (y0 + y1) / 2)
    parts = []
    for g in (shape.geoms if hasattr(shape, "geoms") else [shape]):
        m = trimesh.creation.extrude_polygon(g, TEXT_DEPTH + 1.0)
        m.apply_translation([0, 0, H_EXT - TEXT_DEPTH])
        parts.append(m)
    return U(*parts)


def em_posicao_de_impressao(lid):
    """Vira a tampa para a face de fora ficar na mesa (z=0) e a aba e os pilares apontarem para cima."""
    m = lid.copy()
    m.apply_transform(trimesh.transformations.rotation_matrix(np.pi, [1, 0, 0]))
    m.apply_translation([0, W_EXT, H_EXT])
    assert abs(m.bounds[0][2]) < 1e-6 and abs(m.bounds[0][1]) < 1e-6, "tampa fora da mesa"
    return m


def build_base():
    shell = D(box(0, L_EXT, 0, W_EXT, 0, Z_TOP_BASE),
              box(WALL, L_EXT - WALL, WALL, W_EXT - WALL, Z_FLOOR, Z_TOP_BASE + 1))
    adds = []
    # pilares sob os 4 cantos do sensor (a placa do sensor apoia aqui, com os cilindros nos furos)
    for sx in (sensor_x0, sensor_x1 - SENSOR_POST):
        for sy in (sensor_y0, sensor_y1 - SENSOR_POST):
            adds.append(box(sx, sx + SENSOR_POST, sy, sy + SENSOR_POST, Z_FLOOR, Z_SENSOR_FRONT))
    # calços sob os 4 cantos da placa perfurada
    for bx in (board_x0, board_x1 - BOARD_POST):
        for by in (board_y0, board_y1 - BOARD_POST):
            adds.append(box(bx, bx + BOARD_POST, by, by + BOARD_POST, Z_FLOOR, Z_BOARD))
    # pilares dos parafusos da tampa (com furo para inserto M3)
    for (px, py) in screw_pts:
        adds.append(cyl(px, py, Z_FLOOR, Z_TOP_BASE, SCREW_POST_D / 2))
    # aba externa para o alívio de tração do cabo USB (apoiada na mesa na impressão, sem suporte)
    adds.append(box(usb_x - TIE_TAB_HALF, usb_x + TIE_TAB_HALF, -TIE_TAB_LEN, 1.0, 0, TIE_TAB_H))
    body = U(shell, *adds)
    cuts = []
    for sgn in (-1, 1):
        cuts.append(box(usb_x + sgn * TIE_SLOT_DX - TIE_SLOT_X / 2, usb_x + sgn * TIE_SLOT_DX + TIE_SLOT_X / 2,
                        -TIE_SLOT_AT - TIE_SLOT_Y / 2, -TIE_SLOT_AT + TIE_SLOT_Y / 2, -1, TIE_TAB_H + 1))
    for (px, py) in screw_pts:
        cuts.append(cyl(px, py, Z_TOP_BASE - INSERT_DEPTH, Z_TOP_BASE + 1, INSERT_D / 2, 32))
    # furos do sensor (com chanfro por fora)
    for hx in hole_xs:
        cuts.append(box(hx - HOLE_SLOT / 2, hx + HOLE_SLOT / 2, sensor_cy - HOLE_D / 2, sensor_cy + HOLE_D / 2, -1, Z_FLOOR + 1))
        for dx in (-HOLE_SLOT / 2, HOLE_SLOT / 2):
            cuts.append(cyl(hx + dx, sensor_cy, -1, Z_FLOOR + 1, HOLE_D / 2))
            # chanfro de 45 graus: raio HOLE_D/2 + HOLE_CHAMFER na face de fora (z=0), caindo até HOLE_D/2 em z=HOLE_CHAMFER
            r_ch = HOLE_D / 2 + HOLE_CHAMFER
            cuts.append(cone(hx + dx, sensor_cy, 0.0, r_ch, r_ch))
    # abertura do USB-C na parede y=0
    cuts.append(rounded_box_yz(usb_x - USB_OPEN_W / 2, usb_x + USB_OPEN_W / 2, WALL / 2, Z_USBC_C, USB_OPEN_W, USB_OPEN_H, USB_OPEN_R, WALL + 1))
    return D(body, *cuts)


def build_lid(label):
    plate = box(0, L_EXT, 0, W_EXT, Z_TOP_BASE, H_EXT)
    # aba que entra na caixa
    ix0, ix1 = WALL + LIP_CLEAR, L_EXT - WALL - LIP_CLEAR
    iy0, iy1 = WALL + LIP_CLEAR, W_EXT - WALL - LIP_CLEAR
    lip = D(box(ix0, ix1, iy0, iy1, Z_TOP_BASE - LIP_H, Z_TOP_BASE),
            box(ix0 + LIP_T, ix1 - LIP_T, iy0 + LIP_T, iy1 - LIP_T, Z_TOP_BASE - LIP_H - 1, Z_TOP_BASE + 1))
    adds = [lip]
    # pilares que seguram a placa perfurada e o sensor por cima (nos cantos, onde não há componente)
    zb = Z_BOARD_TOP + PRESS_GAP
    for (px, py) in [(X(2.5), Y(2.0 + USB_EDGE_GAP)), (X(2.5), Y(USB_EDGE_GAP + BOARD_W - 2.0)), (X(BOARD_X0 + BOARD_L - 1.5), Y(USB_EDGE_GAP + BOARD_W - 2.0))]:
        adds.append(box(px - PRESS / 2, px + PRESS / 2, py - PRESS / 2, py + PRESS / 2, zb, Z_TOP_BASE))
    zs = Z_SENSOR_BACK + PRESS_GAP
    for px in (sensor_x0 + SENSOR_POST / 2, sensor_x1 - SENSOR_POST / 2):
        for py in (sensor_y0 + SENSOR_POST / 2, sensor_y1 - SENSOR_POST / 2):
            adds.append(box(px - PRESS / 2, px + PRESS / 2, py - PRESS / 2, py + PRESS / 2, zs, Z_TOP_BASE))
    # reforço por dentro, atrás de cada ímã
    for mx in mag_cx:
        adds.append(cyl(mx, mag_cy, Z_TOP_BASE - MAG_BOSS_H, Z_TOP_BASE + 0.5, MAG_BOSS_D / 2))
    body = U(plate, *adds)
    cuts = []
    for (px, py) in screw_pts:
        cuts.append(cyl(px, py, Z_TOP_BASE - 1, H_EXT + 1, SCREW_HOLE_D / 2, 32))
        cuts.append(cyl(px, py, H_EXT - SCREW_CBORE_DEPTH, H_EXT + 1, SCREW_CBORE_D / 2, 32))
    # bolsos dos ímãs, abertos para o lado de fora (o ímã encosta direto na máquina)
    for mx in mag_cx:
        cuts.append(cyl(mx, mag_cy, H_EXT - MAG_H - MAG_CLEAR_H, H_EXT + 1, (MAG_D + MAG_CLEAR_D) / 2))
    cuts.append(text_mesh(label))
    return D(body, *cuts)


def components():
    """Os componentes reais, só para conferir colisão (não são impressos)."""
    c = {}
    c["placa_perfurada"] = box(board_x0, board_x1, board_y0, board_y1, Z_BOARD, Z_BOARD_TOP)
    c["esp_pcb"] = box(esp_x0, esp_x0 + ESP_W, esp_y0, esp_y0 + ESP_L, Z_ESP_PCB0, Z_ESP_PCB0 + ESP_PCB_T)
    c["usb_c_esp"] = box(usb_x - USBC_W / 2, usb_x + USBC_W / 2, esp_y0 - USBC_PROTRUDE, esp_y0 + 6.5,
                         Z_ESP_PCB0 + ESP_PCB_T, Z_ESP_PCB0 + ESP_PCB_T + USBC_H)
    c1x = X(BOARD_X0 + M_COL_A + C1_COL_IDX * PITCH)
    c1y = board_y0 + M_ROW_O + C1_ROW_CENTER * PITCH
    c["c1"] = cyl(c1x, c1y, Z_BOARD_TOP, Z_C1_TOP, C1_D / 2)
    c["sensor_pcb"] = box(sensor_x0, sensor_x1, sensor_y0, sensor_y1, Z_SENSOR_FRONT, Z_SENSOR_BACK)
    for i, hx in enumerate(hole_xs):
        c[f"cilindro_{i+1}"] = cyl(hx, sensor_cy, SENSOR_RECESS, Z_SENSOR_FRONT, TX_D / 2)
    # plugue USB-C (do padrão) entrando pela abertura, vindo de fora (y negativo)
    c["conector_sensor"] = box(sensor_cx - CONN_W / 2, sensor_cx + CONN_W / 2, sensor_y0 - CONN_OUT, sensor_y0 + 2.0,
                               Z_SENSOR_BACK, Z_SENSOR_BACK + CONN_T)
    c["plugue_usb"] = box(usb_x - USB_PLUG_W / 2, usb_x + USB_PLUG_W / 2, -USB_PLUG_LEN, esp_y0 - USBC_PROTRUDE + 5.0,
                          Z_USBC_C - USB_PLUG_H / 2, Z_USBC_C + USB_PLUG_H / 2)
    for i, mx in enumerate(mag_cx):
        c[f"ima_{i+1}"] = cyl(mx, mag_cy, H_EXT - MAG_H, H_EXT, MAG_D / 2)
    return c


def distancia_xy(a, b):
    """Menor distância (mm) entre duas caixas alinhadas aos eixos, vistas de cima: (x0,x1,y0,y1)."""
    dx = max(a[0] - b[1], b[0] - a[1], 0.0)
    dy = max(a[2] - b[3], b[2] - a[3], 0.0)
    return float(np.hypot(dx, dy))


def main(out):
    out.mkdir(parents=True, exist_ok=True)
    base = build_base()
    lids = {rot: build_lid(rot) for rot in NODE_LABELS}
    lid = lids[NODE_LABELS[0]]
    saidas = {"base": base}
    saidas.update({f"tampa_{rot}": em_posicao_de_impressao(m) for rot, m in lids.items()})
    # peças de teste de encaixe: só as fatias que importam, imprimem em minutos antes da caixa inteira
    saidas["teste_sensor"] = trimesh.boolean.intersection(
        [base, box(sensor_x0 - 6, L_EXT, 0, W_EXT, 0, Z_SENSOR_FRONT + 1.5)], engine="manifold")
    saidas["teste_usb"] = trimesh.boolean.intersection(
        [base, box(0, usb_x + 20, -TIE_TAB_LEN - 1, 9, 0, Z_USBC_C + 9)], engine="manifold")
    for nome, m in saidas.items():
        assert m.is_watertight and m.volume > 0, f"{nome} inválida"
        m.export(out / f"{nome}.stl")
    comp = components()

    # ---- conferências de colisão
    relatorio, erros = {}, []
    for nome, m in comp.items():
        ob, ot = overlap(m, base), max(overlap(m, l) for l in lids.values())
        relatorio[nome] = {"na_base_mm3": round(ob, 2), "na_tampa_mm3": round(ot, 2)}
        if ob > 0.5 or ot > 0.5:
            erros.append(f"{nome} colide (base {ob:.1f} mm³, tampa {ot:.1f} mm³)")
    # a ESP e o C1 também não podem se tocar
    for a, b in (("esp_pcb", "c1"), ("usb_c_esp", "c1")):
        o = overlap(comp[a], comp[b])
        if o > 0.5:
            erros.append(f"{a} colide com {b} ({o:.1f} mm³)")
    # o conector USB-C da ESP tem que ficar alinhado com a abertura e a menos de 2,5 mm da face de dentro da parede
    esp_y_face = comp["usb_c_esp"].bounds[0][1]
    dist_parede = esp_y_face - WALL
    if not (0 <= dist_parede <= 2.5):
        erros.append(f"conector USB-C a {dist_parede:.2f} mm da parede (esperado 0 a 2,5)")
    # a faixa do conector: bloco + saída do fio precisam caber entre a borda do sensor e a parede
    folga_faixa = (sensor_y0 - WALL) - CONN_OUT
    if folga_faixa < 2.5:
        erros.append(f"faixa do conector com só {folga_faixa:.1f} mm de sobra para o fio dobrar (mínimo 2,5)")
    # os cilindros têm que estar a 26 mm um do outro e centrados no furo
    cc = abs(hole_xs[1] - hole_xs[0])
    # chanfro do furo do sensor: tem de ser vazio dentro do cone (raio HOLE_D/2 + 0,5 a 0,2 mm da face) e sólido fora dele
    sy = sensor_cy + HOLE_D / 2 + HOLE_CHAMFER * 0.5
    sonda_x = hole_xs[0] - HOLE_SLOT / 2
    sonda = lambda z: overlap(base, box(sonda_x - 0.1, sonda_x + 0.1, sy - 0.1, sy + 0.1, z - 0.1, z + 0.1))
    if sonda(0.15) > 0.001:
        erros.append("sem chanfro no furo do sensor (há material a 0,15 mm da face, dentro do cone)")
    if sonda(1.6) < 0.007:
        erros.append("furo do sensor largo demais além do chanfro (falta material a 1,6 mm da face)")
    # ímãs longe da antena (ponta da ESP oposta ao USB)
    antena = (esp_x0, esp_x0 + ESP_W, esp_y0 + ESP_L - ANTENNA_ZONE_LEN, esp_y0 + ESP_L)
    dist_ima = min(distancia_xy((mx - MAG_D / 2, mx + MAG_D / 2, mag_cy - MAG_D / 2, mag_cy + MAG_D / 2), antena) for mx in mag_cx)
    if dist_ima < ANTENNA_MIN_DIST:
        erros.append(f"ímã a {dist_ima:.1f} mm da antena (mínimo {ANTENNA_MIN_DIST})")
    # fendas da abraçadeira têm que ficar fora do corpo do plugue
    folga_fenda = TIE_SLOT_DX - TIE_SLOT_X / 2 - USB_PLUG_W / 2
    if folga_fenda <= 0.5:
        erros.append(f"fenda da abraçadeira a {folga_fenda:.2f} mm do plugue (mínimo 0,5)")
    # a aba não pode encostar no plugue
    folga_aba = (Z_USBC_C - USB_PLUG_H / 2) - TIE_TAB_H
    if folga_aba < 0.5:
        erros.append(f"aba a {folga_aba:.2f} mm do plugue (mínimo 0,5)")
    # texto: dentro da tampa, longe dos reforços dos ímãs e gravado de verdade (cada nó gera uma tampa diferente)
    tb = text_mesh(NODE_LABELS[0]).bounds
    if not (WALL + 1 <= tb[0][0] and tb[1][0] <= mag_cx[0] - MAG_BOSS_D / 2 - 1 and WALL + 1 <= tb[0][1] and tb[1][1] <= W_EXT - WALL - 1):
        erros.append(f"texto fora da área livre da tampa: {np.round(tb, 1).tolist()}")
    placa_tampa = box(0, L_EXT, 0, W_EXT, Z_TOP_BASE, H_EXT)
    texto_mm3 = {}
    for rot, l in lids.items():
        vt = text_mesh(rot)
        dentro, sobra = overlap(vt, placa_tampa), overlap(vt, l)     # o texto tem de ter volume na placa e a região dele tem de estar vazia
        texto_mm3[rot] = round(dentro, 1)
        if dentro < 20.0 or sobra > 0.5:
            erros.append(f"texto {rot} não foi gravado (volume na placa {dentro:.1f} mm³, material restante {sobra:.1f} mm³)")
    # a tampa não pode ficar com menos de 1 mm de parede atrás do texto
    if LID_T - TEXT_DEPTH < 1.0:
        erros.append("texto profundo demais para a tampa")

    dados = {
        "externa_mm": [round(L_EXT, 1), round(W_EXT, 1), round(H_EXT, 1)],
        "interna_mm": [round(L_IN, 1), round(W_IN, 1), INNER_D],
        "furos_sensor": {"diametro": HOLE_D, "distancia_centros": cc, "centro_x": round(sensor_cx, 2), "centro_y": round(sensor_cy, 2)},
        "abertura_usb": {"centro_x": round(usb_x, 2), "centro_z": round(Z_USBC_C, 2), "largura": USB_OPEN_W, "altura": USB_OPEN_H},
        "distancia_conector_usb_a_parede_mm": round(dist_parede, 2),
        "folga_c1_ate_tampa_mm": round(Z_TOP_BASE - Z_C1_TOP, 2),
        "imas": {"disco_mm": f"{MAG_D:g} x {MAG_H:g}", "centros_x": [round(v, 1) for v in mag_cx], "centro_y": round(mag_cy, 1),
                 "distancia_da_antena_mm": round(dist_ima, 1), "parede_atras_do_ima_mm": round(LID_T + MAG_BOSS_H - MAG_H - MAG_CLEAR_H, 2)},
        "faixa_do_conector_mm": {"conector_sai": CONN_OUT, "sobra_para_o_fio": round(folga_faixa, 1)},
        "abracadeira": {"folga_fenda_ao_plugue_mm": round(folga_fenda, 2), "folga_aba_ao_plugue_mm": round(folga_aba, 2)},
        "texto": {"rotulos": list(NODE_LABELS), "altura_mm": TEXT_H, "profundidade_mm": TEXT_DEPTH, "volume_gravado_mm3": texto_mm3, "limites_mm": np.round(tb, 1).tolist()},
        "pecas_stl": {k: round(v.volume / 1000, 2) for k, v in saidas.items()},
        "volume_base_cm3": round(base.volume / 1000, 2), "volume_tampa_cm3": round(lid.volume / 1000, 2),
        "colisoes": relatorio, "erros": erros,
    }
    (out / "conferencia.json").write_text(json.dumps(dados, ensure_ascii=False, indent=2), encoding="utf-8")
    return base, lid, comp, dados


if __name__ == "__main__":
    saida = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).parent
    base, lid, comp, dados = main(saida)
    print(json.dumps({k: v for k, v in dados.items() if k != "colisoes"}, ensure_ascii=False, indent=2))
    print("colisões (mm³):", {k: (v["na_base_mm3"], v["na_tampa_mm3"]) for k, v in dados["colisoes"].items()})
    sys.exit(1 if dados["erros"] else 0)
