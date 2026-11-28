#!/usr/bin/env python3
"""Gera previa.png: base com os componentes (iso, de cima, lateral do USB) e a tampa. Uso: python3 previa.py"""
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.colors as mc
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

import caixa_no as C

SAIDA = Path(__file__).parent
base, lid, comp, dados = C.main(SAIDA)
LUZ = np.array([0.35, -0.55, 0.75]); LUZ /= np.linalg.norm(LUZ)
CORES = {"placa_perfurada": "#2e8b57", "esp_pcb": "#243b6b", "usb_c_esp": "#9aa0a6", "c1": "#2f6fb5",
         "sensor_pcb": "#1d63c4", "cilindro_1": "#c8ccd0", "cilindro_2": "#c8ccd0", "plugue_usb": "#e8731a", "conector_sensor": "#8e44ad", "ima_1": "#b02a2a", "ima_2": "#b02a2a"}


def desenha(ax, mesh, cor, alpha=1.0):
    n = mesh.face_normals
    sombra = 0.50 + 0.50 * np.clip(n @ LUZ, 0, 1)
    rgb = np.array(mc.to_rgb(cor))
    fc = [(*(rgb * s), alpha) for s in sombra]
    ax.add_collection3d(Poly3DCollection(mesh.triangles, facecolors=fc, edgecolors="none"))


def cena(ax, itens, elev, azim, titulo):
    for mesh, cor, alpha in itens:
        desenha(ax, mesh, cor, alpha)
    ax.set_xlim(0, C.L_EXT); ax.set_ylim(-26, C.W_EXT); ax.set_zlim(0, C.H_EXT + 2)
    ext = np.array([C.L_EXT, C.W_EXT + 26, C.H_EXT + 2])
    ax.set_box_aspect(ext)
    ax.view_init(elev=elev, azim=azim)
    ax.set_title(titulo, fontsize=10, fontweight="bold")
    ax.set_xlabel("x (comprimento)"); ax.set_ylabel("y (largura)"); ax.set_zlabel("z (profundidade)")
    ax.tick_params(labelsize=6)


itens = [(base, "#d9d9d9", 0.35)] + [(m, CORES.get(k, "#8e44ad"), 0.55 if k == "plugue_usb" else 0.95) for k, m in comp.items()]
fig = plt.figure(figsize=(15, 10.5))
cena(fig.add_subplot(2, 2, 1, projection="3d"), itens, 28, -58, "Base com os componentes (vista isométrica)")
cena(fig.add_subplot(2, 2, 2, projection="3d"), itens, 90, -90, "De cima, sem a tampa")
cena(fig.add_subplot(2, 2, 3, projection="3d"), itens, 4, -90, "Lado do USB-C (abertura e plugue)")
ax = fig.add_subplot(2, 2, 4)
corte = lid.section(plane_origin=[0, 0, C.H_EXT - 0.3], plane_normal=[0, 0, 1])      # a 0,3 mm da face de fora: aparecem o texto e os bolsos
for linha in corte.discrete:
    ax.plot(linha[:, 0], linha[:, 1], color="#5a4630", lw=1.1)
ax.set_aspect("equal"); ax.grid(alpha=0.3)
ax.set_title("Tampa N01 vista de fora (corte a 0,3 mm da face): texto, bolsos dos ímãs e furos dos parafusos", fontsize=9, fontweight="bold")
ax.set_xlabel("x (mm)"); ax.set_ylabel("y (mm)")
e = dados["externa_mm"]
fig.suptitle(f"Caixa do nó (rascunho v2): {e[0]:.0f} × {e[1]:.0f} × {e[2]:.0f} mm externos  |  plugue USB-C em laranja, ímãs em vermelho, conector do sensor em roxo", fontsize=12)
fig.tight_layout()
fig.savefig(SAIDA / "previa.png", dpi=110)
print("previa.png gerada")
