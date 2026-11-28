#!/usr/bin/env python3
"""Desenha as opções de curva do cabo do sensor (vista de cima e de lado) -> curvas_cabo.png"""
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle, Circle

SAIDA = Path(__file__).parent
S_L, S_W = 46.5, 21.0
CAN_D, CAN_CC = 16.0, 26.5
CONN_W, CONN_OUT = 10.2, 12.0
cx = S_L / 2
COR_PLACA, COR_CONN, COR_FIO, COR_PAREDE = "#2f6fb5", "#6b3fa0", "#e8731a", "#9aa0a6"


def arco(c, r, a0, a1, n=30):
    t = np.radians(np.linspace(a0, a1, n))
    return c[0] + r * np.cos(t), c[1] + r * np.sin(t)


def vista_de_cima(ax, titulo, lane, r, com_bloco, largura_externa, nota, cor_titulo):
    ax.set_title(titulo, fontsize=11, fontweight="bold", color=cor_titulo)
    # paredes
    ax.add_patch(Rectangle((-18, -lane - 2.5), 74, 2.5, color=COR_PAREDE))          # parede do USB (embaixo)
    ax.add_patch(Rectangle((-18, S_W + 0.5), 74, 2.5, color=COR_PAREDE))            # parede de cima
    ax.add_patch(Rectangle((S_L + 1.0, -lane - 2.5), 2.5, S_W + lane + 5.5, color=COR_PAREDE))   # parede do fim
    # sensor
    ax.add_patch(Rectangle((0, 0), S_L, S_W, color=COR_PLACA, zorder=2))
    for x in (cx - CAN_CC / 2, cx + CAN_CC / 2):
        ax.add_patch(Circle((x, S_W / 2), CAN_D / 2, color="#d5d8dc", ec="#7f8c8d", zorder=3))
    ax.text(cx, S_W / 2, "sensor\n(cilindros p/ cima)", ha="center", va="center", fontsize=8, color="#34495e", zorder=4)
    # conector e fio
    y_fim = -CONN_OUT if com_bloco else -0.5
    if com_bloco:
        ax.add_patch(Rectangle((cx - CONN_W / 2, -CONN_OUT), CONN_W, CONN_OUT + 2.0, color=COR_CONN, zorder=5))
        ax.text(cx, -CONN_OUT / 2, "bloco\nDupont\n12 mm", ha="center", va="center", fontsize=8, color="white", zorder=6)
    reta = 1.0
    xs0, ys0 = [cx, cx], [y_fim, y_fim - reta]
    ax_, ay_ = arco((cx - r, y_fim - reta), r, 0, -90)
    y_fio = y_fim - reta - r
    xs = list(xs0) + list(ax_) + [-18]
    ys = list(ys0) + list(ay_) + [y_fio]
    ax.plot(xs, ys, color=COR_FIO, lw=4, solid_capstyle="round", zorder=6)
    ax.annotate("segue para a\nplaca perfurada", xy=(-17.5, y_fio), xytext=(-17, y_fio + 7), fontsize=8, color=COR_FIO,
                arrowprops=dict(arrowstyle="->", color=COR_FIO))
    # cotas
    xc = cx + 9.5
    ax.annotate("", xy=(xc, -lane), xytext=(xc, 0), arrowprops=dict(arrowstyle="<->", color="black"))
    ax.text(xc + 1.2, -lane / 2, f"faixa\n{lane:g} mm", ha="left", va="center", fontsize=9, fontweight="bold")
    ax.text(cx, S_W + 5.5 + 1.5, f"caixa de {largura_externa} mm de largura", ha="center", fontsize=10, fontweight="bold")
    ax.text(cx, -lane - 4.5, nota, ha="center", va="top", fontsize=8.5)
    ax.set_xlim(-18, 56); ax.set_ylim(-lane - 11, S_W + 9); ax.set_aspect("equal"); ax.axis("off")
    ax.text(51, -lane - 1.2, "parede do USB", ha="right", va="top", fontsize=7, color="#5d6d7e")


def vista_de_lado(ax):
    ax.set_title("Por que \"subir\" o cabo NÃO economiza largura\n(corte no meio do sensor, olhando de lado)", fontsize=11, fontweight="bold", color="#c0392b")
    lane, r = 16.0, 4.0
    ax.add_patch(Rectangle((-lane - 2.5, -16), 2.5, 32, color=COR_PAREDE))               # parede do USB (esquerda)
    ax.add_patch(Rectangle((-lane - 2.5, 13), lane + 2.5 + S_W + 3, 2.5, color=COR_PAREDE))  # tampa
    ax.text(-lane + 1, 14.2, "tampa", fontsize=8, va="center")
    ax.add_patch(Rectangle((0, -1.6), S_W, 1.6, color=COR_PLACA, zorder=3))               # placa do sensor
    ax.text(S_W / 2, -3.2, "placa do sensor (vista de lado)", ha="center", fontsize=8, va="top")
    ax.add_patch(Rectangle((-CONN_OUT, 0), CONN_OUT + 2, 3, color=COR_CONN, zorder=4))     # bloco
    ax.text(-CONN_OUT / 2 + 1, 1.5, "bloco", ha="center", va="center", fontsize=8, color="white", zorder=5)
    y0, z0 = -CONN_OUT, 1.5
    tt = np.radians(np.linspace(0, 90, 30))
    xs = list(y0 - r * np.sin(tt)); zs = list(z0 + r - r * np.cos(tt))
    xs += [xs[-1]]; zs += [zs[-1] + 2.0]
    ax.plot([y0 + 0.5] + xs, [z0] + zs, color=COR_FIO, lw=4, solid_capstyle="round", zorder=6)
    ax.plot(xs[-1], zs[-1] + 0.6, marker="o", ms=11, mfc="white", mec=COR_FIO, mew=2, zorder=7)
    ax.plot(xs[-1], zs[-1] + 0.6, marker="x", ms=7, color=COR_FIO, mew=2, zorder=8)
    ax.text(xs[-1] + 1.6, zs[-1] + 0.6, "segue para a placa\n(entra na página)", fontsize=8, color=COR_FIO, va="center")
    ax.annotate("", xy=(y0, -5.6), xytext=(y0 - r, -5.6), arrowprops=dict(arrowstyle="<->", color="#c0392b", lw=1.6))
    ax.text(y0 - r / 2, -7.2, f"a curva\ngasta {r:g} mm\npara o lado", ha="center", va="top", fontsize=8.5, color="#c0392b", fontweight="bold")
    ax.set_xlim(-lane - 3, S_W + 2); ax.set_ylim(-14, 17); ax.set_aspect("equal"); ax.axis("off")


fig, axs = plt.subplots(2, 2, figsize=(15, 10.5))
vista_de_cima(axs[0, 0], "1) HOJE no modelo: curva no plano, raio ~3,5 mm", 17.0, 3.5, True, 42.5,
              "o cabo sai do bloco e dobra para a placa;\nsobram 5 mm até a parede", "#2c3e50")
vista_de_cima(axs[0, 1], "2) MESMA curva, mais apertada (a testar)", 16.0, 3.0, True, 41.5,
              "só vale se o cabo aguentar raio de 3 mm\nsem soltar o bloco dos pinos (ganho: 1 mm)", "#2c3e50")
vista_de_cima(axs[1, 0], "3) SEM o bloco: fios soldados direto no sensor", 5.0, 3.0, False, 39.0,
              "a largura passa a ser a da placa perfurada (35 mm internos);\nperde o encaixe e desencaixe do conector (ganho: 3,5 mm)", "#1e8449")
vista_de_lado(axs[1, 1])
fig.suptitle("Como o cabo do sensor sai e quanta largura a caixa precisa (vista de cima: roxo = bloco do conector, laranja = fios)", fontsize=12)
fig.tight_layout()
fig.savefig(SAIDA / "curvas_cabo.png", dpi=105)
print("curvas_cabo.png gerada")
