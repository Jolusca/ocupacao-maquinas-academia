# Gera o PDF do layout da placa perfurada de um nó (ESP32-C6 SuperMini + HC-SR04).
# Uso: python3 desenha_placa.py SAIDA.pdf   (as ligações vêm de layout_dados.py, que se confere sozinho)
import re
import sys
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.patches import Rectangle, Circle, FancyBboxPatch, Ellipse

import layout_dados as L

erros = L.verificar()
if erros:
    sys.exit("layout com erro, não desenhei:\n  " + "\n  ".join(erros))

NC, NR = len(L.COLS), L.NLIN
C0 = 2                       # as 2 primeiras colunas do desenho (A, B) não existem nas placas cortadas
NCV = NC - C0                # colunas de cada placa: 15
COL_P1 = "ABCDEFGHIJKLMNO"                      # Placa 1: A a O
COL_P2 = "QRSTUVWXYZABCDE"                   # Placa 2: Q a Z e depois A a E
LINHAS = "OPQRSTUVWXYZ"                      # linhas 1 a 12 = O a Z (linha 1, a O, fica do lado da USB)
COR = {"5V": "#d62728", "GND": "#222222", "TRIG": "#2e8b57", "ECHO": "#e0a100", "X": "#7b3fb5"}
COBRE, SOLDA = "#c98a3b", "#cfd2d6"
FONTE = "DejaVu Sans"
plt.rcParams.update({"font.family": FONTE, "pdf.fonttype": 42})


def hole(h):
    return L.COLS.index(h[0]), int(h[1:])


def _tokens():
    t = set()
    for _, (_, f) in L.COMPONENTES.items(): t |= set(f)
    for _, (_, f) in L.BARRAMENTOS.items(): t |= set(f)
    for _, (_, f, _) in L.FIOS.items(): t |= set(f)
    for f in L.PONTES.values(): t |= set(f)
    for _, (_, f) in L.SOBRE_ILHAS.items(): t |= set(f)
    t |= {L.pino_esq(i) for i in range(1, 11)} | {L.pino_dir(i) for i in range(1, 11)}
    return t - {"C1", "C2", "S1"}   # nomes de componentes que parecem furos


TOKENS = _tokens()


def vis(texto):
    """Troca os nomes de furo do desenho lógico (colunas A-Q) pelas letras da Placa 1 (A-O)."""
    def f(m):
        h = m.group(0)
        return (COL_P1[L.COLS.index(h[0]) - C0] + h[1:]) if h in TOKENS else h
    return re.sub(r"\b[A-Q][0-9]{1,2}\b", f, texto)


class Vista:
    def __init__(self, ax, espelhar):
        self.ax, self.esp = ax, espelhar

    def X(self, c):
        c = c - C0
        return (NCV - 1 - c) if self.esp else c

    def P(self, h):
        c, r = hole(h) if isinstance(h, str) else (L.COLS.index(h[0]), h[1])
        return self.X(c), -(r - 1)

    def PL(self, c, r):
        return self.X(L.COLS.index(c)), -(r - 1)

    def placa(self, pads):
        ax = self.ax
        ax.add_patch(Rectangle((-0.9, -(NR - 1) - 0.9), NCV - 1 + 1.8, NR - 1 + 0.9 + 0.55,
                               fc="#ebe5cf" if not pads else "#e6dcc0", ec="#7a735a", lw=1.2, zorder=0))
        for c in range(C0, NC):
            for r in range(1, NR + 1):
                x, y = self.X(c), -(r - 1)
                if pads:
                    ax.add_patch(Circle((x, y), 0.30, fc=COBRE, ec="#8a5a1f", lw=0.4, zorder=1))
                    ax.add_patch(Circle((x, y), 0.11, fc="white", ec="#6d4a1a", lw=0.4, zorder=2))
                else:
                    ax.add_patch(Circle((x, y), 0.12, fc="#5d5842", ec="none", zorder=1))
        for c in range(C0, NC):
            ax.text(self.X(c), 1.55, COL_P1[c - C0], ha="center", va="center", fontsize=9, fontweight="bold", color="#333")
            ax.text(self.X(c), 1.95, COL_P2[c - C0], ha="center", va="center", fontsize=7.5, color="#8a6d3b")
        ax.text(-2.0 if not self.esp else NCV - 1 + 2.0, 1.55, "Placa 1", ha="center", va="center", fontsize=7, color="#333")
        ax.text(-2.0 if not self.esp else NCV - 1 + 2.0, 1.95, "Placa 2", ha="center", va="center", fontsize=7, color="#8a6d3b")
        for r in range(1, NR + 1):
            ax.text(-1.45 if not self.esp else NCV - 1 + 1.45, -(r - 1), f"{r} ({LINHAS[r-1]})", ha="center", va="center",
                    fontsize=8, fontweight="bold", color="#333")

    def modulo(self, fantasma=False):
        ax = self.ax
        x0, x1 = self.X(3) - 0.55, self.X(9) + 0.55
        if x0 > x1: x0, x1 = x1, x0
        top, bot = 0.5, -(9) - 0.5
        ax.add_patch(Rectangle((x0, bot), x1 - x0, top - bot, fc="#9ec9e8" if not fantasma else "none",
                               ec="#2b6a99", lw=1.3, ls="--", alpha=0.35 if not fantasma else 1, zorder=3))
        ux = (x0 + x1) / 2
        ax.add_patch(Rectangle((ux - 0.8, top), 1.6, 0.55, fc="#bfc5cc", ec="#555", lw=1, zorder=3))
        ax.text(ux, top + 0.27, "USB-C", ha="center", va="center", fontsize=6.5, color="#222", zorder=4)
        if not fantasma:
            ax.text(ux, -4.5, "ESP32-C6\nSuperMini\n(USB para cima)", ha="center", va="center", fontsize=8, color="#1f4e79",
                    zorder=4, alpha=0.9)
        else:
            ax.text(ux, -8.0, "ESP32-C6 (soldada\npor cima)", ha="center", va="center", fontsize=7, color="#5a7a95", zorder=4)

    def soquetes(self):
        ax = self.ax
        for col, nomes, lado in (("D", L.PINOS_ESQ, "esq"), ("J", L.PINOS_DIR, "dir")):
            x = self.PL(col, 1)[0]
            ax.add_patch(Rectangle((x - 0.42, -9.5), 0.84, 10.0, fc="#8f8f8f", ec="#444", lw=1, zorder=4))
            for i in range(1, 11):
                usado = (col == "D" and i in (3, 4)) or (col == "J" and i in (1, 2))
                ax.add_patch(Circle((x, -(i - 1)), 0.17, fc="#f5c542" if usado else "#8c8c8c", ec="black", lw=0.5, zorder=5))
                interno_esq = (lado == "esq") != self.esp   # rótulo para o lado de dentro do módulo
                dx = 0.62 if interno_esq else -0.62
                ha = "left" if interno_esq else "right"
                cor = "#b00020" if usado else "#35506b"
                ax.text(x + dx, -(i - 1), nomes[i - 1], ha=ha, va="center", fontsize=6.6 if not usado else 7.2,
                        fontweight="bold" if usado else "normal", color=cor, zorder=6,
                        bbox=dict(boxstyle="round,pad=0.08", fc="#eef5fb", ec="none", alpha=0.9))


def vista_cima(ax):
    v = Vista(ax, False)
    v.placa(False)
    v.modulo()
    v.soquetes()
    # S1: 4 fios soldados nos furos P1, P3, Q2, P4 (cores do kit: vermelho, laranja, amarelo, marrom)
    xr = v.X(16) + 1.0
    cores = [("VCC", "vermelho", "#d62728"), ("TRIG", "laranja", "#ff7f0e"), ("ECHO", "amarelo", "#e0c000"), ("GND", "marrom", "#7b4a1e")]
    for h, (nome, cor_nome, cor) in zip(L.COMPONENTES["S1"][1], cores):
        px, py = v.P(h)
        ax.plot([px, xr], [py, py], color=cor, lw=3.2, solid_capstyle="round", zorder=5)
        ax.add_patch(Circle((px, py), 0.2, fc="#f5c542", ec="black", lw=0.6, zorder=6))
        ax.text(xr + 0.15, py, f"{nome} ({cor_nome})", ha="left", va="center", fontsize=7.6, fontweight="bold", zorder=7,
                bbox=dict(boxstyle="round,pad=0.08", fc="#fbf8ec", ec="none", alpha=0.9))
    ax.text(v.X(13.0), -10.7, "S1: 4 fios soldados (coluna O, linhas O Q S U)", ha="center", va="center", fontsize=8, fontweight="bold", color="#222")
    # C1 (em pé, 10 mm de diâmetro, pernas abertas a 3 furos: M1 e M4)
    cx, cy = v.P("M1")[0], -1.5
    ax.add_patch(Circle((cx, cy), 2.0, fc="#3a5f8a", ec="#1d2f45", lw=1.4, zorder=4))
    ax.text(cx, cy + 0.15, "C1", ha="center", va="center", fontsize=9, color="white", fontweight="bold", zorder=6)
    ax.text(cx, cy - 0.45, "470 µF\n10 × 16 mm", ha="center", va="center", fontsize=6.8, color="white", zorder=6)
    for h, sinal in (("M1", "+"), ("M4", "−")):
        px, py = v.P(h)
        ax.add_patch(Circle((px, py), 0.17, fc="#f5c542", ec="black", lw=0.5, zorder=7))
        ax.text(px - 0.5, py + (0.0), sinal, ha="center", va="center", fontsize=11, fontweight="bold", color="#b00020" if sinal == "+" else "#111", zorder=8)
    # resistores
    for nome, (valor, furos) in (("R1", L.COMPONENTES["R1"]), ("R2", L.COMPONENTES["R2"])):
        (xa, ya), (xb, yb) = v.P(furos[0]), v.P(furos[1])
        ax.plot([xa, xb], [ya, yb], color="#777", lw=2, zorder=3)
        xm = (xa + xb) / 2
        ax.add_patch(FancyBboxPatch((xm - 1.25, ya - 0.33), 2.5, 0.66, boxstyle="round,pad=0.02,rounding_size=0.25",
                                    fc="#d9b77a", ec="#7a5a22", lw=1, zorder=4))
        ax.text(xm, ya, f"{nome}  {valor}", ha="center", va="center", fontsize=7.2, fontweight="bold", color="#3a2a08", zorder=5)
        for h in furos:
            px, py = v.P(h)
            ax.add_patch(Circle((px, py), 0.14, fc="#f5c542", ec="black", lw=0.5, zorder=6))
    ax.text(v.X(13), -8.4, "Divisor de tensão do ECHO\n(5 V → 3,3 V)", ha="center", va="center", fontsize=8, color="#444", style="italic")
    cfg(ax, v)


def cfg(ax, v):
    ax.set_xlim(-2.6, NCV - 1 + 4.6)
    ax.set_ylim(-(NR - 1) - 1.3, 2.5)
    ax.set_aspect("equal")
    ax.axis("off")


def vista_baixo(ax):
    v = Vista(ax, True)
    v.placa(True)
    v.modulo(fantasma=True)
    ax.add_patch(Circle((v.P("M1")[0], -1.5), 2.0, fc="none", ec="#999", lw=1, ls=":", zorder=3))
    ax.text(v.P("M1")[0], -1.5, "C1\n(em pé,\npor cima)", ha="center", va="center", fontsize=6.5, color="#777", zorder=3)
    ax.text(v.X(13.0), -10.7, "S1 (4 fios, coluna O)", ha="center", va="center", fontsize=8, fontweight="bold", color="#555")
    for nome in ("R1", "R2"):
        furos = L.COMPONENTES[nome][1]
        (xa, ya), (xb, yb) = v.P(furos[0]), v.P(furos[1])
        xm = (xa + xb) / 2
        ax.add_patch(FancyBboxPatch((xm - 1.25, ya - 0.33), 2.5, 0.66, boxstyle="round,pad=0.02,rounding_size=0.25",
                                    fc="none", ec="#999", lw=1, ls=":", zorder=3))
        ax.text(xm, ya, nome, ha="center", va="center", fontsize=7, color="#777", zorder=3)
    # barramentos (fio nu)
    for nome, (rede, furos) in L.BARRAMENTOS.items():
        pts = [v.P(f) for f in furos]
        ax.plot([pts[0][0], pts[-1][0]], [pts[0][1], pts[-1][1]], color=COBRE if rede == "5V" else COBRE,
                lw=5.5, solid_capstyle="round", zorder=6, alpha=0.95)
        ax.plot([pts[0][0], pts[-1][0]], [pts[0][1], pts[-1][1]], color=COR[rede], lw=1.6, zorder=7)
        ax.text(v.X(12.5), pts[0][1] - 0.62, f"barramento {rede} (fio nu)", ha="center", va="center",
                fontsize=7.2, fontweight="bold", color=COR[rede], zorder=9,
                bbox=dict(boxstyle="round,pad=0.15", fc="white", ec=COR[rede], lw=0.8))
    # fios encapados
    for nome, (rede, furos, cam) in L.FIOS.items():
        pts = [v.PL(c, r) for c, r in cam]
        ax.plot([p[0] for p in pts], [p[1] for p in pts], color="white", lw=4.2, zorder=8, solid_capstyle="round", solid_joinstyle="round")
        ax.plot([p[0] for p in pts], [p[1] for p in pts], color=COR[rede], lw=2.4, zorder=9, solid_capstyle="round", solid_joinstyle="round")
    # C2 (100 nF) soldado por baixo, direto entre as ilhas do 5V (J1) e do GND (J2) da ESP
    for nome, (valor, furos) in L.SOBRE_ILHAS.items():
        (xa, ya), (xb, yb) = v.P(furos[0]), v.P(furos[1])
        ax.add_patch(FancyBboxPatch((xa - 0.33, min(ya, yb) + 0.12), 0.66, abs(ya - yb) - 0.24, boxstyle="round,pad=0.02,rounding_size=0.2",
                                    fc="#d8b24a", ec="#6b4e10", lw=1.2, zorder=12))
        ax.text(xa + 0.95, (ya + yb) / 2, f"{nome} {valor}\n(por baixo)", ha="left",
                va="center", fontsize=6.8, fontweight="bold", color="#5a4108", zorder=13,
                bbox=dict(boxstyle="round,pad=0.12", fc="#fff6d6", ec="#6b4e10", lw=0.7))
    # R4 faz o papel do fio do TRIG: corpo por baixo, sob a ESP; perna curta nua no pino; perna longa ISOLADA até o fio
    for fio, (rnome, rvalor) in L.RESISTOR_NO_FIO.items():
        cam = L.FIOS[fio][2]
        (x1, y1), (x2, y2) = v.PL(*cam[-2]), v.PL(*cam[-1])
        xm = v.X(5.5)
        ax.plot([x2, xm], [y2, y2], color="#8c8c8c", lw=2.4, zorder=11, solid_capstyle="round")   # perna curta, nua
        ax.add_patch(FancyBboxPatch((xm - 0.9, y1 - 0.26), 1.8, 0.52, boxstyle="round,pad=0.02,rounding_size=0.22",
                                    fc="#d9b77a", ec="#7a5a22", lw=1.2, zorder=12))
        ax.text(xm, y1, f"{rnome} {rvalor}", ha="center", va="center", fontsize=7.2, fontweight="bold", color="#3a2a08", zorder=13)
        ax.text(xm, y1 - 0.75, "perna curta (nua)", ha="center", va="center", fontsize=6.2, color="#555", zorder=13)
    # pontes de solda
    for nome, furos in L.PONTES.items():
        (xa, ya), (xb, yb) = v.P(furos[0]), v.P(furos[1])
        ax.add_patch(Ellipse(((xa + xb) / 2, (ya + yb) / 2), abs(xb - xa) + 0.62, abs(yb - ya) + 0.62, fc=SOLDA, ec="#444", lw=1.2, zorder=10))
    # furos soldados
    usados = set()
    for _, (_, f) in L.COMPONENTES.items(): usados |= set(f)
    for _, (_, f, _) in L.FIOS.items(): usados |= set(f)
    for i in range(1, 11): usados |= {L.pino_esq(i), L.pino_dir(i)}
    for _, (_, f) in L.BARRAMENTOS.items(): usados |= set(f)
    # Pontas reais dos fios (e do R4): círculo prateado POR CIMA. As demais ilhas ficam por BAIXO dos fios, para
    # mostrar que um fio que só passa por elas não faz contato.
    pontas = set()
    for _, (_, f, _) in L.FIOS.items(): pontas |= set(f)
    for h in usados:
        x, y = v.P(h)
        ax.add_patch(Circle((x, y), 0.2, fc=SOLDA, ec="#555", lw=0.8, zorder=15 if h in pontas else 7))
    # rótulos dos fios (com fundo para ler)
    pos = {"W3": ("W3  GND", ("K", 5.0), (0, 0)), "W4": ("W4  GND", ("M", 6), (0.75, 0)),
           "W5": ("R4: perna longa ISOLADA", ("N", 3), (0, 0.55)), "W6": ("W6  ECHO", ("P", 4.6), (0.0, 0)),
           "W9": ("W9  → GPIO1", ("H", 6), (0, -0.38))}
    for nome, (txt, (c, r), (dx, dy)) in pos.items():
        rede = L.FIOS[nome][0]
        x, y = v.PL(c, r)
        ax.text(x + dx, y + dy, txt, ha="center", va="center", fontsize=7.4, fontweight="bold", color=COR[rede],
                bbox=dict(boxstyle="round,pad=0.15", fc="white", ec=COR[rede], lw=0.8), zorder=12)
    for nome, (rx, ry, dx) in {"ponte X": ("L", 6.5, 0.9), "ponte G": ("P", 7.9, 0.0)}.items():
        x, y = v.PL(rx, ry)
        ax.text(x + dx, y, nome, ha="center", va="center", fontsize=7,
                color="#333", bbox=dict(boxstyle="round,pad=0.12", fc="#f2f2f2", ec="#555", lw=0.7), zorder=12)
    cfg(ax, v)


def titulo(fig, texto, sub=None):
    fig.text(0.04, 0.955, texto, fontsize=16, fontweight="bold", color="#14304f", va="center")
    if sub:
        fig.text(0.04, 0.923, sub, fontsize=9.5, color="#444", va="center")
    fig.text(0.04, 0.018, "Projeto Ocupação de Máquinas de Academia · TI0148 Sistemas Embarcados · UFC", fontsize=7.5, color="#777")


def legenda(fig, caixa, linhas, titulo_txt="Como ler"):
    ax = fig.add_axes(caixa)
    ax.axis("off")
    ax.add_patch(Rectangle((0, 0), 1, 1, fc="#f6f8fb", ec="#c8d2de", lw=1, transform=ax.transAxes))
    ax.text(0.05, 0.97, titulo_txt, fontsize=10.5, fontweight="bold", color="#14304f", va="top", transform=ax.transAxes)
    y = 0.915
    for t in linhas:
        if isinstance(t, tuple):
            cor, txt = t
            ax.add_patch(Rectangle((0.05, y - 0.012), 0.10, 0.018, fc=cor, ec="none", transform=ax.transAxes))
            ax.text(0.19, y - 0.003, vis(txt), fontsize=8, va="center", transform=ax.transAxes)
            y -= 0.04
        else:
            n = t.count("\n") + 1
            ax.text(0.05, y, vis(t), fontsize=8, va="top", transform=ax.transAxes, linespacing=1.35)
            y -= 0.034 * n + 0.012
    return ax


def pagina_cima(pdf):
    fig = plt.figure(figsize=(11.69, 8.27))
    titulo(fig, "Placa perfurada, 1 nó: VISTA DE CIMA (lado dos componentes)",
           "ESP32-C6 SuperMini + HC-SR04 com divisor de tensão. Duas placas iguais: Placa 1 (colunas A–O) e Placa 2 (Q–Z e A–E), linhas O–Z.")
    ax = fig.add_axes([0.03, 0.045, 0.66, 0.85])
    vista_cima(ax)
    legenda(fig, [0.71, 0.045, 0.27, 0.85], [
        "Placa de 15 × 12 furos: colunas A–O e\nlinhas 1–12 (1=O ... 12=Z). A linha 1 fica\ndo lado da USB. Em marrom, as colunas\nda Placa 2 (Q–Z e A–E).",
        "A ESP32-C6 é soldada direto nas colunas\nB e H, linhas 1 a 10, com a USB para CIMA\n(linha 1), rente à borda da placa.",
        "Pinos usados (em amarelo):\nD3 = GPIO0 (TRIG)\nD4 = GPIO1 (ECHO, já em 3,3 V)\nJ1 = 5V      J2 = GND",
        "Componentes:\nS1  4 fios soldados em Q1, Q3, Q5, Q7:\n      VCC vermelho, TRIG laranja,\n      ECHO amarelo, GND marrom\nC1  470 µF (10 × 16 mm), + em M1 e − em M4,\n      em pé, pernas abertas a 3 furos\nR1 P6–L6 (1 kΩ) · R2 L7–P7 (2 kΩ),\n      deitados",
        "As ligações ficam por BAIXO da placa\n(página 2). Aqui só entram os componentes.",
    ])
    pdf.savefig(fig); plt.close(fig)


def pagina_baixo(pdf):
    fig = plt.figure(figsize=(11.69, 8.27))
    titulo(fig, "Placa perfurada, 1 nó: VISTA DE BAIXO (lado da solda, espelhada)",
           "Vire a placa como uma página de livro: as colunas ficam invertidas (A à direita). Aqui entram os fios.")
    ax = fig.add_axes([0.03, 0.045, 0.66, 0.85])
    vista_baixo(ax)
    legenda(fig, [0.71, 0.045, 0.27, 0.85], [
        (COR["5V"], "5V (barramento de fio nu)"),
        (COR["GND"], "GND (barramento nu e fios W3, W4)"),
        (COR["TRIG"], "TRIG (R4 como fio)"),
        (COR["ECHO"], "ECHO (W6)"),
        (COR["X"], "nó do divisor ao GPIO1 (W9)"),
        (SOLDA, "ponto de solda / ponte de solda"),
        "Fio nu (cobre estanhado): deitado sobre a\nlinha de furos, soldado em cada furo marcado.",
        "Fios W3, W4, W6, W9: rígido ENCAPADO\n(wire-wrap, AWG 26 a 30). Eles se cruzam\n(W3 e a perna do R4), mas têm capa.",
        "Solde na ilha de cobre; nos pinos da ESP,\nna própria ilha do pino.",
        "Fio desenhado POR CIMA de uma ilha, sem\ncírculo prateado sobre ele, só PASSA por\nbaixo dela: isolado, sem solda e sem contato.",
        "Pontes X e G: gota de solda unindo dois\nfuros vizinhos (ou um pedaço de fio).",
        "R4 (1 kΩ) é o fio do TRIG: corpo por baixo,\nsob a ESP, perna curta nua em D3; a perna\nlonga, ISOLADA, vai até Q3 (a ilha do fio laranja).",
        "C2 (100 nF): soldado POR BAIXO, direto\nentre as ilhas do 5V (J1) e do GND (J2),\nperto dos pinos da ESP. Terminais curtos.",
    ], "Legenda")
    pdf.savefig(fig); plt.close(fig)


def tabela(ax, dados, cabecalho, larguras, topo, fonte=8, linha=0.037):
    altura = linha * (len(dados) + 1)
    dados = [[vis(c) for c in lin] for lin in dados]
    t = ax.table(cellText=dados, colLabels=cabecalho, colWidths=larguras, bbox=[0, topo - altura, sum(larguras), altura],
                 cellLoc="left")
    t.auto_set_font_size(False)
    t.set_fontsize(fonte)
    for (r, c), cell in t.get_celld().items():
        cell.set_edgecolor("#c8d2de")
        if r == 0:
            cell.set_facecolor("#14304f"); cell.set_text_props(color="white", fontweight="bold")
        else:
            cell.set_facecolor("#ffffff" if r % 2 else "#f2f5f9")
    return t


def pagina_ligacoes(pdf):
    fig = plt.figure(figsize=(11.69, 8.27))
    titulo(fig, "Lista de ligações, materiais e ordem de montagem")
    ax = fig.add_axes([0.04, 0.05, 0.92, 0.84]); ax.axis("off")
    ax.text(0, 1.0, "Ligações (conferidas contra o esquemático)", fontsize=11, fontweight="bold", color="#14304f", va="top")
    dados = [
        ["B5V", "fio nu (barramento)", "J1 · M1 · Q1", "5V da ESP, C1 (+) e VCC do sensor"],
        ["BGND", "fio nu (barramento)", "L4 · M4", "C1 (−), W3 e W4: o GND da placa"],
        ["W3", "encapado, preto", "J2  →  L4", "GND da ESP ao barramento de GND"],
        ["W4", "encapado, preto", "P7  →  M4", "fim do divisor (R2) ao GND"],
        ["R4", "resistor 1 kΩ, perna longa isolada", "Q3  →  D3", "TRIG do sensor ao GPIO0: o resistor é o fio (corpo sob a ESP, perna curta em D3)"],
        ["W6", "encapado, amarelo", "Q5  →  P6", "ECHO do sensor ao início de R1"],
        ["W9", "encapado, roxo", "L6  →  D4", "nó do divisor (3,3 V) ao GPIO1"],
        ["ponte X", "gota de solda", "L6 – L7", "une o fim de R1 ao início de R2 (nó do divisor)"],
        ["ponte G", "gota de solda", "P7 – Q7", "liga o GND do sensor ao fim do R2 (que já é GND)"],
        ["C2", "100 nF (104), por baixo", "J1 – J2", "filtro de ruído entre o pino 5V e o pino GND da ESP"],
        ["S1", "4 fios do cabo do sensor", "Q1 · Q3 · Q5 · Q7", "VCC vermelho, TRIG laranja, ECHO amarelo, GND marrom"],
    ]
    tabela(ax, dados, ["ID", "Tipo", "De → Para", "Função"], [0.09, 0.20, 0.17, 0.46], 0.955, fonte=8.0, linha=0.0305)
    ax.text(0, 0.575, "Materiais (por placa)", fontsize=11, fontweight="bold", color="#14304f", va="top")
    mat = [
        "2  placas perfuradas de 15 × 12 furos (180), passo 2,54 mm, ilhas individuais: as duas metades que você cortou",
        "4  jumpers (marrom, vermelho, laranja, amarelo) para o cabo do sensor: corte a ponta do lado da placa e deixe a fêmea para o sensor",
        "    (a SuperMini precisa estar com pinos soldados)",
        "2  resistores de 1 kΩ (R1 e R4) e 1 resistor de 2 kΩ (R2), 1/4 W; o R4 com as pernas compridas (não corte antes de medir)",
        "1  capacitor cerâmico 104 = 100 nF (C2), de disco: dobre as pernas e solde por baixo nas ilhas J1 e J2",
        "    termo-retrátil fino para a perna longa do R4, e uma abraçadeira ou cola quente para o alívio de tração do cabo",
        "1  capacitor eletrolítico 470 µF, 10 V ou mais (C1). Serve de 100 a 470 µF; é proteção contra queda de tensão",
        "    fio de cobre nu estanhado (AWG 22 a 24), uns 10 cm;   fio de WIRE-WRAP (Kynar) AWG 26 a 30, uns 40 cm",
        "    ferro de solda, solda, alicate de corte, multímetro",
    ]
    ax.text(0, 0.548, vis("\n".join(mat)), fontsize=7.8, va="top", linespacing=1.38)
    ax.text(0, 0.285, "Ordem de montagem", fontsize=11, fontweight="bold", color="#14304f", va="top")
    passos = [
        "1.  Soldar a ESP32-C6 direto na placa (colunas B e H, linhas 1 a 10, USB na linha 1) e cortar as pontas dos pinos por baixo, rente à solda.",
        "2.  Soldar os resistores R1 e R2, fazer as pontes X e G e soldar os 4 fios do sensor em Q1, Q3, Q5 e Q7 (cores abaixo).",
        "3.  Soldar o capacitor C1 (+ em M1, − em M4), em pé, com as pernas abertas a 3 furos. Antes, solde os 4 fios do sensor: o corpo cobre as colunas I a M.",
        "4.  Soldar os barramentos de fio nu (B5V e BGND) e o C2 entre as ilhas J1 e J2, por baixo.",
        "5.  Soldar os fios encapados W3, W4, W6 e W9 e o R4 (de Q3 a D3). Prender o cabo do sensor (abraçadeira ou cola) perto da placa.",
        "6.  Testar com a placa DESLIGADA (página seguinte). Só depois plugar a USB.",
    ]
    ax.text(0, 0.258, vis("\n".join(passos)), fontsize=7.8, va="top", linespacing=1.4)
    pdf.savefig(fig); plt.close(fig)


def pagina_testes(pdf):
    fig = plt.figure(figsize=(11.69, 8.27))
    titulo(fig, "Testes antes de ligar e cuidados")
    ax = fig.add_axes([0.04, 0.05, 0.92, 0.84]); ax.axis("off")
    ax.text(0, 1.0, "1) Placa DESLIGADA (multímetro em continuidade; a ESP está soldada na placa)", fontsize=11, fontweight="bold", color="#14304f", va="top")
    dados = [
        ["DEVE apitar", "J1 (5V) ↔ Q1 (VCC do S1)", "5V chega ao sensor"],
        ["DEVE apitar", "J2 (GND) ↔ Q7 (GND do S1)", "GND comum"],
        ["DEVE apitar", "L6 (nó do divisor) ↔ D4 (GPIO1)", "eco já reduzido chega ao GPIO1"],
        ["NÃO pode apitar", "J1 (5V) ↔ J2 (GND)", "curto na alimentação (um apito breve que some é o capacitor carregando)"],
        ["NÃO pode apitar", "J3 (3V3) ↔ J2 (GND)", "curto no 3,3 V (confira também as ilhas vizinhas do C2)"],
        ["NÃO pode apitar", "Q3 (TRIG) ↔ Q5 (ECHO)", "sinais em curto"],
        ["NÃO pode apitar", "Q5 (ECHO) ↔ D4 (GPIO1)", "ECHO direto no pino, sem o R1: pode queimar a ESP"],
    ]
    tabela(ax, dados, ["Resultado", "Entre os pontos", "Para quê"], [0.16, 0.34, 0.46], 0.955, fonte=8.2, linha=0.036)
    ax.text(0, 0.628, "2) Medir resistência (multímetro em ohms, escala de 20 kΩ ou automática)", fontsize=11, fontweight="bold", color="#14304f", va="top")
    dados2 = [
        ["Q5 (ECHO) ↔ L6 (nó)", "≈ 1 kΩ", "R1"],
        ["L6 (nó) ↔ J2 (GND)", "≈ 2 kΩ", "R2"],
        ["Q5 (ECHO) ↔ J2 (GND)", "≈ 3 kΩ", "o divisor inteiro"],
        ["Q3 (TRIG), ponta fêmea do fio ↔ D3 (GPIO0)", "≈ 1 kΩ", "R4 (não pode apitar; se der aberto, uma solda não pegou)"],
    ]
    tabela(ax, dados2, ["Entre os pontos", "Esperado", "Corresponde a"], [0.34, 0.12, 0.50], 0.592, fonte=8.2, linha=0.036)
    ax.text(0, 0.395, "3) Com a USB plugada, sem o sensor", fontsize=11, fontweight="bold", color="#14304f", va="top")
    ax.text(0, 0.368, vis("VCC do S1 (Q1) contra GND (Q7): cerca de 5 V.   Depois ligue o sensor e leia a serial: com um alvo parado a 30 cm\n"
                      "a leitura deve ficar perto de 30 cm, como na protoboard. Use o mesmo firmware, sem mudar nada."),
            fontsize=8.4, va="top", linespacing=1.45)
    ax.text(0, 0.283, "Cuidados e o que conferir", fontsize=11, fontweight="bold", color="#14304f", va="top")
    cuid = [
        "•  O sentido do divisor importa: 1 kΩ entre o ECHO e o nó, 2 kΩ entre o nó e o GND. Invertido, o GPIO1 recebe só 1,7 V.",
        "•  O C1 (10 × 16 mm) cobre as colunas I a M e as linhas O a R: nada mais pode ficar ali por cima, e ele sobe 16 mm acima da placa.",
        "•  Cores do sensor: VCC vermelho, TRIG laranja, ECHO amarelo, GND marrom. Sem conector polarizado, não encaixe a fêmea invertida (VCC↔GND queima o sensor): marque o pino VCC.",
        "•  O R4 (1 kΩ no TRIG) limita a corrente no GPIO0 se TRIG e ECHO forem trocados por engano. Foi testado: não muda a leitura. A perna longa vai ISOLADA; o corpo fica por baixo, sob a ESP.",
        "•  Se o N01 soldado funcionar, faça o N02 igual. Solde e teste UMA placa por vez.",
        "•  Posicione a ESP com a ponta da USB do lado da linha 1 (O), rente à borda. As linhas 11 e 12 (Y e Z) ficam abaixo da antena: deixe livres.",
        "•  W9 e a perna longa do R4 passam por baixo de ilhas soldadas e se cruzam com o W3: use fio de WIRE-WRAP (Kynar) ou esmaltado, e isole bem as pernas. Fio nu só nos barramentos.",
        "•  Antena da ESP: fica na ponta oposta à USB (linhas 9 e 10). Mantenha fios e metal longe dela e compare o RSSI com o da protoboard.",
        "•  Não use GPIO4, 5, 8, 9, 12, 13 e 15 (pinos de boot e da USB do chip). O desenho só usa GPIO0, GPIO1, 5V e GND.",
    ]
    ax.text(0, 0.254, vis("\n".join(cuid)), fontsize=8.0, va="top", linespacing=1.4)
    pdf.savefig(fig); plt.close(fig)


if __name__ == "__main__":
    saida = sys.argv[1]
    with PdfPages(saida) as pdf:
        pagina_cima(pdf)
        pagina_baixo(pdf)
        pagina_ligacoes(pdf)
        pagina_testes(pdf)
    print("gerado:", saida)
