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
from shapely.geometry import Polygon, box as sbox

# ============================== PARÂMETROS ==============================
# As medidas do Marcos (28/11) foram tiradas com uma régua comum, lida em passos de 1 mm: incerteza de +-1 mm.
# Tudo que decide se uma peça CABE usa a medida + MARGEM; as aberturas que dependem de posição (USB, LED, furos do sensor) têm folga extra.
MARGEM = 1.0
# --- caixa
WALL = 2.0              # parede lateral
FLOOR = 2.0             # frente (por onde o sensor olha)
LID_T = 2.0             # tampa
INNER_D = 26.0          # profundidade interna (da frente até a tampa)  [CONFIRMAR com a placa montada]

# --- placa perfurada (15 x 12 furos), medida pelo Marcos
BOARD_L, BOARD_W, BOARD_T = 45.0 + MARGEM, 34.0 + MARGEM, 1.0    # medido 45 x 34 x 1 em 28/11; tamanho + margem (a espessura fica nominal: o erro vertical é absorvido pela abertura do USB)
BOARD_H_TOTAL = 20.0 + MARGEM    # da face de baixo da placa até o topo do C1 (medido em 28/11: 20 mm) + margem
STANDOFF = 3.0          # calço sob a placa (folga para as soldas e o corpo do R4)
PITCH = 2.54
M_COL_A = 7.0           # borda da placa (lado A) até o centro da coluna A; medido em 28/11 (7 mm: a placa tem uma fileira de pads na borda)
M_ROW_O = 3.0           # borda do lado do USB até o centro da linha O; medido em 28/11
# (USB_EDGE_GAP, a folga entre a placa perfurada e a parede do USB, é calculado nas cotas derivadas a partir do conector da ESP)

# --- ESP32-C6 SuperMini soldada direto
ESP_GAP = 3.0           # vão entre a placa perfurada e a placa da ESP; medido em 28/11: 3 mm
ESP_PCB_T = 1.2         # espessura da placa da ESP (foto de 28/11: 1,2 a 1,6 mm)
ESP_W, ESP_L = 18.0 + MARGEM, 26.0 + MARGEM     # medido em 28/11: 18 x 26 mm (a ficha diz 22,5 mm; a sua é mais longa), sem o conector, + margem
USBC_H, USBC_W = 3.0, 9.0   # conector USB-C da ESP (altura medida em 28/11: 3 mm; largura da ficha)
USBC_PROTRUDE = 2.0     # quanto o conector USB-C passa da borda da placa da ESP: medido em 28/11, 28 mm da ponta do conector ao fim da ESP - 26 mm da placa
USBC_LEN = 7.3          # comprimento do corpo do conector USB-C (da ponta para dentro)
ESP_EDGE_IN = 1.0       # a borda do USB da placa da ESP fica 1 mm para dentro da borda da placa perfurada: o conector passa 1 mm dela (medido em 28/11)

# --- C1 (eletrolítico em pé, K·O / K·R) e a posição dele na placa
C1_D = 10.0 + MARGEM     # medido 10 mm + margem
C1_COL_IDX = 10         # coluna K = 11ª coluna (índice 10)
C1_ROW_CENTER = 1.5     # centro entre as linhas O e R (1,5 passos a partir da linha O)

# --- sensor HC-SR04 (datasheet)
S_L, S_W = 45.0 + MARGEM, 20.0 + MARGEM   # datasheet 45 x 20; medido pelo Marcos em 28/11: 45 x 20; + margem
S_PCB_T = 1.6
S_TOTAL_T = 13.0        # da frente dos cilindros até as costas da placa; medido em 28/11: 13 mm (o datasheet diz 15 com o conector)
TX_D = 16.0
TX_CC = 26.0            # [CONFIRMAR] distância entre os centros dos cilindros
HOLE_D = 17.2           # furo dos cilindros de 16 mm (folga de 0,6 mm de cada lado: cobre +-1 mm da régua no diâmetro)
HOLE_SLOT = 2.0         # o furo é alongado em x por esse tanto: tolera +-1 mm no espaçamento dos cilindros (medido 26 mm)
HOLE_CHAMFER = 1.0      # chanfro por fora, para não cortar o cone de som
SENSOR_RECESS = 0.5     # quanto a frente dos cilindros fica atrás da face de fora (se o sensor for 1 mm mais fundo, sobra no máximo 0,5 mm para fora)
# conector Dupont do sensor: bloco único de 4 pinos, rígido, deitado no plano da placa e saindo pela borda LONGA (foto de 28/11)
CONN_W, CONN_OUT, CONN_T = 10.0 + MARGEM, 12.0 + MARGEM, 3.0   # largura (4 x 2,54), quanto passa da borda (medido na foto de 28/11: 12 mm), espessura
CONN_LANE = 18.0        # faixa livre ao lado do sensor: CONN_OUT + ~5 mm para o fio sair do bloco e fazer a curva (raio ~4-5 mm)

# --- layout interno (x a partir da parede interna)
BOARD_X0 = 1.0
CABLE_GAP = 22.0        # espaço do cabo entre a placa e o sensor
END_CLEAR = 1.0
SIDE_CLEAR = 1.5        # folga na lateral oposta ao USB

# --- suportes, parafusos e abertura do USB
SENSOR_POST = 3.5       # lado do pilar sob cada canto do sensor
BOARD_POST = 4.5
SCREW_POST_D, INSERT_D, INSERT_DEPTH = 9.0, 4.2, 7.0   # inserto de rosca a quente M3; pilar de 9 mm deixa 2,4 mm de parede ao redor do furo (>= parede de 2 mm da caixa)
SCREW_HOLE_D, SCREW_CBORE_D, SCREW_CBORE_DEPTH = 3.4, 6.4, 1.2
PRESS = 4.5             # lado dos pilares que prendem as placas por cima (pino fino quebra: Hubs recomenda >= 5 mm; 4,5 é o que cabe sem encostar em componente)
PRESS_GAP = 1.0           # folga entre os pilares da tampa e as placas (absorve +-1 mm da régua; uma fita de espuma de 1 mm tira a folga)
LIP_T, LIP_H, LIP_CLEAR = 1.2, 1.5, 0.3                # aba de encaixe da tampa
USB_OPEN_W, USB_OPEN_H, USB_OPEN_R = 14.5, 11.0, 1.5   # abertura: plugue USB-C 12,35 x 6,5 mm + 1 mm de cada lado (regra da Hubs: 2 mm no total)
USB_PLUG_W, USB_PLUG_H, USB_PLUG_LEN = 12.35, 6.5, 25.0   # padrão USB-C; o plugue do Marcos mediu 10 x 6 mm (+-1), então este tamanho cobre o dele e cabos mais largos

# --- ímãs de fixação (na tampa, que é o fundo da caixa; ficam na ponta do SENSOR, longe da antena da ESP)
MAG_D, MAG_H = 10.0, 2.0            # [CONFIRMAR] ímã de neodímio em disco 10 x 2 mm
MAG_CLEAR_D, MAG_CLEAR_H = 0.2, 0.2  # folga do bolso (o ímã é colado)
MAG_BOSS_D = 14.0                    # reforço por dentro da tampa, ao redor do bolso (parede de 1,9 mm)
MAG_SKIN = 0.6                       # pele de plástico entre o ímã e a máquina; o bolso abre PARA DENTRO (sem ponte na impressão)
MAG_X_FROM_SENSOR_END = 12.0         # distância do centro do ímã até a ponta do sensor
ANTENNA_ZONE_LEN = 7.0               # comprimento da região da antena na ponta da ESP oposta ao USB
ANTENNA_MIN_DIST = 25.0              # distância mínima do ímã até essa região

# --- alívio de tração do cabo USB (aba externa com 2 fendas para abraçadeira de nylon)
TIE_TAB_HALF, TIE_TAB_LEN, TIE_TAB_H = 12.0, 14.0, 6.0
TIE_SLOT_DX = 8.6                    # as fendas ficam a 8,6 mm do eixo do plugue (que tem meia largura de 6,2)
TIE_SLOT_X, TIE_SLOT_Y = 2.0, 3.8    # espessura x largura da fita (abraçadeira de até 3,6 mm)
TIE_SLOT_AT = 9.0                    # distância da fenda até a parede

# --- número do nó gravado no lado de fora da tampa
TEXT_H, TEXT_DEPTH = 8.0, 0.6
NODE_LABELS = ("N01", "N02")

# --- fixação provisória por velcro: 4 cantos em L gravados (0,4 mm) na face de fora para alinhar a tira
VELCRO = True
VELCRO_X0, VELCRO_L, VELCRO_W = 42.0, 30.0, 18.0     # início em x (a partir da parede interna), comprimento e largura da tira
VELCRO_ARM, VELCRO_LINE, VELCRO_DEPTH = 5.0, 0.8, 0.4

# --- janela do LED RGB (WS2812, GPIO8) da ESP: o LED forte, à esquerda do CI central com o USB-C para cima (Marcos, 28/11).
# Posição pela foto da placa dele: ~1,5 mm da borda longa do lado dos pinos GPIO0-7 e ~10 mm da borda do USB. [CONFIRMAR]
# A tampa fica contra a máquina, então a janela é um furo na parede da ponta da caixa (lado da placa), mirando o LED.
LED_JANELA = True
LED_DX, LED_FROM_TIP, LED_H = 3.0, 17.0, 1.0        # LED a 3 mm da borda longa (lado GPIO0-7; medido em 28/11); centro a 17 mm da PONTA do conector (16 mm até o início do LED de ~2 mm)
LED_HOLE_D = 4.5                                     # furo horizontal de 4,5 mm (ponte < 5 mm); maior que o necessário porque a posição do LED tem +-1,5 mm

# --- boas práticas de FDM (Hubs, Protolabs, Prusa, Stratasys; ver nota de pesquisa)
BASE_CHAMFER = 0.6      # chanfro de 45 graus nas arestas que tocam a mesa (compensa o "elephant foot")
CORNER_R = 3.0          # raio dos cantos externos; o interno é CORNER_R - WALL (raio externo = interno + parede)
MIN_GAP = 0.5           # folga mínima ao redor de componentes internos (Hubs)

# --- lateralidade da placa (foto de 28/11): vista pelo lado dos componentes, a placa real tem o USB-C à ESQUERDA quando os fios do
# sensor ficam em cima. O modelo foi montado com a lateralidade oposta; ESPELHAR_Y reflete a caixa inteira no plano do meio (y).
ESPELHAR_Y = True

SECTIONS = 64
# =======================================================================

# ---- cotas derivadas
# folga entre a placa perfurada e a parede do USB: a ponta do conector USB-C passa da borda da placa perfurada (USBC_PROTRUDE - ESP_EDGE_IN)
# e fica a 0,5 mm da parede por dentro, para o plugue encaixar até o fundo
USB_EDGE_GAP = max(0.5, USBC_PROTRUDE - ESP_EDGE_IN + 0.5 + MARGEM)      # ponta do conector a 1,5 mm da parede
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
Z_SENSOR_FRONT = SENSOR_RECESS + S_TOTAL_T - S_PCB_T      # face da frente da placa do sensor (a ponta dos cilindros fica em z = SENSOR_RECESS)
Z_SENSOR_BACK = Z_SENSOR_FRONT + S_PCB_T
MAG_BOSS_H = Z_TOP_BASE - (H_EXT - MAG_SKIN - MAG_H - MAG_CLEAR_H)    # quanto o reforço do ímã desce abaixo da tampa


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


def rrect(x0, x1, y0, y1, r, n=12):
    """Retângulo de cantos arredondados (polígono shapely)."""
    return sbox(x0 + r, y0 + r, x1 - r, y1 - r).buffer(r, quad_segs=n)


def prisma(x0, x1, y0, y1, z0, z1, r, ch_z0=0.0, ch_z1=0.0):
    """Prisma de seção retangular com cantos de raio r e chanfro de 45 graus opcional na base (z0) e/ou no topo (z1)."""
    def camada(z, inset):
        pts = np.array(rrect(x0 + inset, x1 - inset, y0 + inset, y1 - inset, max(r - inset, 0.0)).exterior.coords)[:-1]
        return np.column_stack([pts, np.full(len(pts), z)])
    cam = ([camada(z0, ch_z0), camada(z0 + ch_z0, 0.0)] if ch_z0 > 0 else [camada(z0, 0.0)])
    cam += ([camada(z1 - ch_z1, 0.0), camada(z1, ch_z1)] if ch_z1 > 0 else [camada(z1, 0.0)])
    return trimesh.convex.convex_hull(np.vstack(cam))


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
esp_y0 = board_y0 + ESP_EDGE_IN                                    # borda do USB da placa da ESP
esp_x0 = usb_x - ESP_W / 2
led_x = usb_x - (ESP_W - MARGEM) / 2 + LED_DX            # LED a LED_DX da borda REAL (sem a margem) de x menor da ESP (lado dos pinos GPIO0-7)
led_y = esp_y0 - USBC_PROTRUDE + LED_FROM_TIP            # medido a partir da ponta do conector USB-C
led_z = Z_ESP_PCB0 + ESP_PCB_T + LED_H / 2               # centro do LED, em cima da placa da ESP
mag_cx = [X(SENSOR_X0 + MAG_X_FROM_SENSOR_END), X(SENSOR_X0 + S_L - MAG_X_FROM_SENSOR_END)]
mag_cy = Y(W_IN / 2)


def texto_forma(label):
    """Contorno 2D do texto (shapely), já centrado sobre a região da placa e invertido em y se a caixa será espelhada."""
    tp = TextPath((0, 0), label, size=10, prop=FontProperties(family="DejaVu Sans", weight="bold"))
    shape = Polygon()
    for ring in tp.to_polygons(closed_only=True):
        shape = shape.symmetric_difference(Polygon(ring).buffer(0))     # preenchimento par-ímpar: o miolo do 0 fica vazado
    x0, y0, x1, y1 = shape.bounds
    k = TEXT_H / (y1 - y0)
    shape = affinity.scale(shape, k, k, origin=(x0, y0))
    x0, y0, x1, y1 = shape.bounds
    shape = affinity.translate(shape, X(BOARD_X0 + BOARD_L / 2) - (x0 + x1) / 2, W_EXT / 2 - (y0 + y1) / 2)
    if ESPELHAR_Y:      # a caixa toda será refletida em y no fim; o texto já sai invertido para voltar a ler certo por fora
        shape = affinity.scale(shape, 1, -1, origin=(0, W_EXT / 2))
    return shape


def text_mesh(label):
    """Texto em relevo negativo (para gravar na face de fora da tampa)."""
    shape = texto_forma(label)
    parts = []
    for g in (shape.geoms if hasattr(shape, "geoms") else [shape]):
        m = trimesh.creation.extrude_polygon(g, TEXT_DEPTH + 1.0)
        m.apply_translation([0, 0, H_EXT - TEXT_DEPTH])
        parts.append(m)
    return U(*parts)


def espelha_y(m):
    """Reflete a peça no plano y = W_EXT/2 (x e z não mudam) e mantém as faces voltadas para fora."""
    r = m.copy()
    M = np.eye(4)
    M[1, 1], M[1, 3] = -1.0, W_EXT
    r.apply_transform(M)
    if r.volume < 0:
        r.invert()
    assert r.is_watertight and r.volume > 0, "espelhamento quebrou a malha"
    return r


def em_posicao_de_impressao(lid):
    """Vira a tampa para a face de fora ficar na mesa (z=0) e a aba e os pilares apontarem para cima."""
    m = lid.copy()
    m.apply_transform(trimesh.transformations.rotation_matrix(np.pi, [1, 0, 0]))
    m.apply_translation([0, W_EXT, H_EXT])
    assert abs(m.bounds[0][2]) < 1e-6 and abs(m.bounds[0][1]) < 1e-6, "tampa fora da mesa"
    return m


def abertura_usb():
    """Abertura do plugue na parede: retângulo de USB_OPEN_W x USB_OPEN_H com um 'telhado' a 45 graus no topo. Com o teto reto, o vão de
    14,5 mm seria uma ponte no ar (Hubs: ponte < 5 mm); o telhado reduz o trecho plano a 5 mm e o resto é overhang de 45 graus.
    O telhado começa acima do plugue com 1 mm de folga, então a abertura continua livre para o corpo do plugue (12,35 x 6,5)."""
    hw = USB_OPEN_W / 2
    ys = USB_PLUG_H / 2 + 1.0                       # onde o telhado começa (já acima do plugue + folga)
    topo = ys + (hw - 2.5)                          # sobe a 45 graus até sobrar um trecho plano de 5 mm
    pol = Polygon([(-hw, -USB_OPEN_H / 2), (hw, -USB_OPEN_H / 2), (hw, ys), (2.5, topo), (-2.5, topo), (-hw, ys)])
    pol = pol.buffer(-USB_OPEN_R).buffer(USB_OPEN_R, quad_segs=8)       # cantos arredondados (tensão e impressão)
    m = trimesh.creation.extrude_polygon(pol, WALL + 1.0)
    m.apply_transform(trimesh.transformations.rotation_matrix(np.pi / 2, [1, 0, 0]))      # (x, y, z) -> (x, -z, y)
    m.apply_translation([usb_x, WALL + 0.5, Z_USBC_C])
    return m


def build_base():
    shell = D(prisma(0, L_EXT, 0, W_EXT, 0, Z_TOP_BASE, CORNER_R, ch_z0=BASE_CHAMFER),
              prisma(WALL, L_EXT - WALL, WALL, W_EXT - WALL, Z_FLOOR, Z_TOP_BASE + 1, max(CORNER_R - WALL, 0.0)))
    adds = []
    # pilares sob os 4 cantos do sensor (a placa do sensor apoia aqui, com os cilindros nos furos).
    # Os que ficam junto das paredes vão até a parede: um pino de 3,5 mm sozinho é fraco (Hubs: pinos < 5 mm); preso à parede vira nervura.
    for sx in (sensor_x0, sensor_x1 - SENSOR_POST):
        for sy in (sensor_y0, sensor_y1 - SENSOR_POST):
            x1 = L_EXT - WALL + 0.2 if sx > sensor_x0 else sx + SENSOR_POST
            y1 = W_EXT - WALL + 0.2 if sy > sensor_y0 else sy + SENSOR_POST
            adds.append(box(sx, x1, sy, y1, Z_FLOOR, Z_SENSOR_FRONT))
    # calços sob os 4 cantos da placa perfurada
    for bx in (board_x0, board_x1 - BOARD_POST):
        for by in (board_y0, board_y1 - BOARD_POST):
            adds.append(box(bx, bx + BOARD_POST, by, by + BOARD_POST, Z_FLOOR, Z_BOARD))
    # pilares dos parafusos da tampa (com furo para inserto M3)
    for (px, py) in screw_pts:
        adds.append(cyl(px, py, Z_FLOOR, Z_TOP_BASE, SCREW_POST_D / 2))
    # aba externa para o alívio de tração do cabo USB (apoiada na mesa na impressão, sem suporte)
    adds.append(prisma(usb_x - TIE_TAB_HALF, usb_x + TIE_TAB_HALF, -TIE_TAB_LEN, 1.0, 0, TIE_TAB_H, 0.0, ch_z0=BASE_CHAMFER))
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
    cuts.append(abertura_usb())
    if LED_JANELA:     # furo horizontal (eixo x) na parede da ponta, na altura e na posição do LED RGB
        c = trimesh.creation.cylinder(radius=LED_HOLE_D / 2, height=WALL + 1.0, sections=32)
        c.apply_transform(trimesh.transformations.rotation_matrix(np.pi / 2, [0, 1, 0]))     # eixo z -> eixo x
        c.apply_translation([WALL / 2, led_y, led_z])
        cuts.append(c)
    return D(body, *cuts)


def velcro_ret():
    """Retângulo da tira de velcro na face de fora da tampa: (x0, x1, y0, y1)."""
    cx = X(VELCRO_X0 + VELCRO_L / 2)
    return cx - VELCRO_L / 2, cx + VELCRO_L / 2, W_EXT / 2 - VELCRO_W / 2, W_EXT / 2 + VELCRO_W / 2


def marcas_velcro():
    """Quatro cantos em L gravados na face de fora, FORA da tira, para alinhar o velcro. Um rebaixo da tira inteira exigiria uma ponte
    de 30 x 20 mm na primeira camada (a face de fora fica na mesa), por isso só se grava o contorno dos cantos."""
    x0, x1, y0, y1 = velcro_ret()
    a, w, z0 = VELCRO_ARM, VELCRO_LINE, H_EXT - VELCRO_DEPTH
    barras = []
    for (px, sx) in ((x0, -1), (x1, 1)):
        for (py, sy) in ((y0, -1), (y1, 1)):
            xa, xb = sorted((px + sx * w, px - sx * a))
            ya, yb = sorted((py + sy * w, py))
            barras.append(box(xa, xb, ya, yb, z0, H_EXT + 1))                       # barra paralela a x
            xa, xb = sorted((px + sx * w, px))
            ya, yb = sorted((py + sy * w, py - sy * a))
            barras.append(box(xa, xb, ya, yb, z0, H_EXT + 1))                       # barra paralela a y
    return U(*barras)


def build_lid(label):
    plate = prisma(0, L_EXT, 0, W_EXT, Z_TOP_BASE, H_EXT, CORNER_R, ch_z1=BASE_CHAMFER)
    # aba que entra na caixa
    ix0, ix1 = WALL + LIP_CLEAR, L_EXT - WALL - LIP_CLEAR
    iy0, iy1 = WALL + LIP_CLEAR, W_EXT - WALL - LIP_CLEAR
    r_lip = max(CORNER_R - WALL - LIP_CLEAR, 0.0)
    lip = D(prisma(ix0, ix1, iy0, iy1, Z_TOP_BASE - LIP_H, Z_TOP_BASE, r_lip),
            prisma(ix0 + LIP_T, ix1 - LIP_T, iy0 + LIP_T, iy1 - LIP_T, Z_TOP_BASE - LIP_H - 1, Z_TOP_BASE + 1, max(r_lip - LIP_T, 0.0)))
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
    # bolsos dos ímãs abertos para DENTRO da caixa, com uma pele de MAG_SKIN entre o ímã e a máquina. Na impressão (face de fora na mesa)
    # o bolso fica virado para cima, sem ponte; um bolso aberto para fora exigiria uma ponte de 10 mm na primeira camada (Hubs: < 5 mm).
    for mx in mag_cx:
        cuts.append(cyl(mx, mag_cy, Z_TOP_BASE - MAG_BOSS_H - 1, H_EXT - MAG_SKIN, (MAG_D + MAG_CLEAR_D) / 2))
    cuts.append(text_mesh(label))
    if VELCRO:
        cuts.append(marcas_velcro())
    return D(body, *cuts)


def components():
    """Os componentes reais, só para conferir colisão (não são impressos)."""
    c = {}
    c["placa_perfurada"] = box(board_x0, board_x1, board_y0, board_y1, Z_BOARD, Z_BOARD_TOP)
    c["esp_pcb"] = box(esp_x0, esp_x0 + ESP_W, esp_y0, esp_y0 + ESP_L, Z_ESP_PCB0, Z_ESP_PCB0 + ESP_PCB_T)
    c["usb_c_esp"] = box(usb_x - USBC_W / 2, usb_x + USBC_W / 2, esp_y0 - USBC_PROTRUDE, esp_y0 - USBC_PROTRUDE + USBC_LEN,
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
    c["led_rgb"] = box(led_x - 1.0, led_x + 1.0, led_y - 1.0, led_y + 1.0, Z_ESP_PCB0 + ESP_PCB_T, Z_ESP_PCB0 + ESP_PCB_T + LED_H)
    for i, mx in enumerate(mag_cx):
        c[f"ima_{i+1}"] = cyl(mx, mag_cy, H_EXT - MAG_SKIN - MAG_H, H_EXT - MAG_SKIN, MAG_D / 2)
    return c


def distancia_xy(a, b):
    """Menor distância (mm) entre duas caixas alinhadas aos eixos, vistas de cima: (x0,x1,y0,y1)."""
    dx = max(a[0] - b[1], b[0] - a[1], 0.0)
    dy = max(a[2] - b[3], b[2] - a[3], 0.0)
    return float(np.hypot(dx, dy))


def teste_inserto():
    """Bloco com 5 furos cegos de 4,0 a 4,4 mm (passo 0,1, em ordem crescente da esquerda para a direita) para achar o diâmetro certo do
    inserto M3 na sua impressora (a CNC Kitchen recomenda imprimir peças de teste: o furo impresso sai menor que o do CAD)."""
    n, passo = 5, 11.0
    bloco = box(0, n * passo + 2, 0, 12, 0, INSERT_DEPTH + 2.0)
    furos = [cyl(1 + passo / 2 + i * passo, 6.0, 2.0, INSERT_DEPTH + 3.0, (4.0 + 0.1 * i) / 2, 48) for i in range(n)]
    return D(bloco, *furos)


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
    saidas["teste_inserto"] = teste_inserto()
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
    if folga_faixa < 4.0:
        erros.append(f"faixa do conector com só {folga_faixa:.1f} mm de sobra para o fio curvar (mínimo 4,0)")
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
    # traço do texto >= 2 larguras de bico (0,8 mm): a "abertura" (erodir e dilatar 0,4 mm) só remove o que é mais fino que 0,8 mm
    forma = texto_forma(NODE_LABELS[0])
    perda_texto = (forma.area - forma.buffer(-0.4).buffer(0.4).area) / forma.area
    if perda_texto > 0.02:
        erros.append(f"traço do texto fino demais para o bico de 0,4 mm ({perda_texto:.1%} da área é mais fina que 0,8 mm)")

    # ---- boas práticas de FDM e de montagem (ver a nota de pesquisa)
    # (1) folga mínima de 0,5 mm ao redor de todos os componentes internos (Hubs), nos lados e em cima
    folgas = {}
    for nome, m in comp.items():
        if nome == "plugue_usb" or nome.startswith("ima_"):
            continue
        b = m.bounds
        g = min(b[0][0] - WALL, (L_EXT - WALL) - b[1][0], b[0][1] - WALL, (W_EXT - WALL) - b[1][1], Z_TOP_BASE - b[1][2])
        folgas[nome] = round(g, 2)
        if g < MIN_GAP - 1e-6:
            erros.append(f"{nome} a {g:.2f} mm da parede ou da tampa (mínimo {MIN_GAP})")
    # (1b) linha de visada do LED até o furo da parede: nada pode atravessar o caminho (cilindro de 2 mm de diâmetro, do LED até a parede)
    if LED_JANELA:
        visada = trimesh.creation.cylinder(radius=1.0, height=led_x - WALL, sections=24)
        visada.apply_transform(trimesh.transformations.rotation_matrix(np.pi / 2, [0, 1, 0]))
        visada.apply_translation([(led_x + WALL) / 2, led_y, led_z])
        obst = overlap(visada, base) + sum(overlap(visada, m) for k, m in comp.items() if k not in ("led_rgb", "esp_pcb", "usb_c_esp"))
        if obst > 0.05:
            erros.append(f"algo atravessa a linha de visada do LED até o furo ({obst:.2f} mm³)")
        if not (led_x - WALL) < 14.0:
            erros.append("LED longe demais da parede para o furo de 3,5 mm (> 14 mm)")
    # (2) pele do ímã: 0,4 a 0,8 mm (abaixo disso não imprime direito; acima, o ímã perde força)
    if not (0.4 <= MAG_SKIN <= 0.8):
        erros.append(f"pele do ímã de {MAG_SKIN} mm fora de 0,4 a 0,8")
    # (3) o bolso do ímã não pode abrir para fora (ponte de 10 mm na primeira camada)
    if overlap(lids[NODE_LABELS[0]], box(mag_cx[0] - 1, mag_cx[0] + 1, mag_cy - 1, mag_cy + 1, H_EXT - 0.3, H_EXT - 0.1)) < 0.5:
        erros.append("bolso do ímã aberto na face de fora (precisa de pele)")
    # (4) velcro: a tira não pode encostar no texto, nos rebaixos dos parafusos nem passar da tampa
    if VELCRO:
        vx0, vx1, vy0, vy1 = velcro_ret()
        m_ = VELCRO_LINE + 0.5
        if vx0 - m_ < tb[1][0] + 1.0:
            erros.append("tira de velcro colada no texto do nó")
        for (px, py) in screw_pts:
            if distancia_xy((vx0 - m_, vx1 + m_, vy0 - m_, vy1 + m_), (px - SCREW_CBORE_D / 2, px + SCREW_CBORE_D / 2, py - SCREW_CBORE_D / 2, py + SCREW_CBORE_D / 2)) < 1.0:
                erros.append("tira de velcro encosta no rebaixo de um parafuso")
        if vx1 + m_ > L_EXT - WALL or vy0 - m_ < WALL or vy1 + m_ > W_EXT - WALL:
            erros.append("tira de velcro passa da área plana da tampa")

    # as conferências acima foram feitas no sistema de eixos original; agora reflete tudo e grava
    cy_sensor = (W_EXT - sensor_cy) if ESPELHAR_Y else sensor_cy
    if ESPELHAR_Y:
        base = espelha_y(base)
        lids = {k: espelha_y(v) for k, v in lids.items()}
        lid = lids[NODE_LABELS[0]]
        comp = {k: espelha_y(v) for k, v in comp.items()}
        saidas = {k: espelha_y(v) for k, v in saidas.items()}
    for nome, m in saidas.items():
        assert m.is_watertight and m.volume > 0, f"{nome} inválida"
        m.export(out / f"{nome}.stl")

    dados = {
        "espelhada_em_y": ESPELHAR_Y,
        "externa_mm": [round(L_EXT, 1), round(W_EXT, 1), round(H_EXT, 1)],
        "interna_mm": [round(L_IN, 1), round(W_IN, 1), INNER_D],
        "furos_sensor": {"diametro": HOLE_D, "distancia_centros": cc, "centro_x": round(sensor_cx, 2), "centro_y": round(cy_sensor, 2)},
        "abertura_usb": {"centro_x": round(usb_x, 2), "centro_z": round(Z_USBC_C, 2), "largura": USB_OPEN_W, "altura_do_retangulo": USB_OPEN_H, "altura_total_com_telhado": round(USB_OPEN_H / 2 + USB_PLUG_H / 2 + 1.0 + USB_OPEN_W / 2 - 2.5, 2)},
        "distancia_conector_usb_a_parede_mm": round(dist_parede, 2),
        "folga_c1_ate_tampa_mm": round(Z_TOP_BASE - Z_C1_TOP, 2),
        "imas": {"disco_mm": f"{MAG_D:g} x {MAG_H:g}", "centros_x": [round(v, 1) for v in mag_cx], "centro_y": round(mag_cy, 1),
                 "distancia_da_antena_mm": round(dist_ima, 1), "pele_entre_ima_e_maquina_mm": MAG_SKIN, "bolso_abre_para": "dentro"},
        "boas_praticas": {"folga_minima_mm": min(folgas.values()), "folgas_por_componente_mm": folgas,
                          "chanfro_na_mesa_mm": BASE_CHAMFER, "raio_dos_cantos_mm": CORNER_R, "pilar_inserto_parede_mm": round((SCREW_POST_D - INSERT_D) / 2, 2),
                          "area_do_texto_mais_fina_que_0,8mm": f"{perda_texto:.1%}", "velcro": ({"retangulo_mm": [round(v, 1) for v in velcro_ret()]} if VELCRO else None)},
        "janela_do_led": ({"furo_mm": LED_HOLE_D, "led_x": round(led_x, 1), "led_y_no_eixo_original": round(led_y, 1), "led_z": round(led_z, 1),
                           "distancia_do_led_a_parede_mm": round(led_x - WALL, 1)} if LED_JANELA else None),
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
