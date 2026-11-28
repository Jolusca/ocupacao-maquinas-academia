# Dados do layout da placa perfurada (um nó: ESP32-C6 SuperMini + HC-SR04).
# Furos: coluna (letra) + linha (número). A coluna D é a fileira esquerda do soquete e a J a direita
# (a SuperMini fica encaixada entre elas, USB para cima).
COLS = "ABCDEFGHIJKLMNOPQ"
NLIN = 12

# Pinos da SuperMini, de cima para baixo, USB para cima (conferido na placa do Marcos em 26/11).
PINOS_ESQ = ["TX(16)", "RX(17)", "GPIO0", "GPIO1", "GPIO2", "GPIO3", "GPIO4", "GPIO5", "GPIO6", "GPIO7"]
PINOS_DIR = ["5V", "GND", "3V3", "GPIO20", "GPIO19", "GPIO18", "GPIO15", "GPIO14", "GPIO9", "GPIO8"]

def pino_esq(i): return f"D{i}"   # i = 1..10
def pino_dir(i): return f"J{i}"

# Componentes: nome -> (rótulo, [furos])
COMPONENTES = {
    "S1": ("4 fios soldados (HC-SR04)", ["Q1", "Q3", "Q5", "Q7"]),   # VCC, TRIG, ECHO, GND
    "C1": ("Capacitor 470 µF (+ em M1, - em M4)", ["M1", "M4"]),
    "R1": ("1 kΩ", ["P6", "L6"]),
    "R2": ("2 kΩ", ["L7", "P7"]),
}
# Componente soldado POR BAIXO, direto entre duas ilhas já ocupadas (não usa furo próprio).
SOBRE_ILHAS = {
    "C2": ("100 nF", ["J1", "J2"]),   # entre o pino 5V e o pino GND da ESP
}
# Ligações condutoras (cada uma une os furos citados)
BARRAMENTOS = {   # fio nu de cobre estanhado, soldado ao longo da linha
    "B5V":  ("5V",  ["J1", "M1", "Q1"]),
    "BGND": ("GND", ["L4", "M4"]),
}
FIOS = {          # fio rígido encapado, pela face de baixo: (cor, furos, caminho)
    "W3": ("GND",  ["J2", "L4"],  [("J", 2), ("K", 2), ("K", 4), ("L", 4)]),
    "W4": ("GND",  ["P7", "M4"],  [("P", 7), ("P", 8), ("M", 8), ("M", 4)]),
    "W5": ("TRIG", ["Q3", "D3"],  [("Q", 3), ("D", 3)]),
    "W6": ("ECHO", ["Q5", "P6"],  [("Q", 5), ("P", 6)]),
    "W9": ("X",    ["L6", "D4"],  [("L", 6), ("E", 6), ("E", 4), ("D", 4)]),
}
# Resistor emendado NO MEIO de um fio (sem furo próprio): separa a rede do lado do sensor da do pino da ESP.
RESISTOR_NO_FIO = {"W5": ("R4", "1 kΩ")}

PONTES = {        # ponte de solda entre furos vizinhos
    "X": ["L6", "L7"],
    "G": ["P7", "Q7"],   # GND do sensor (Q7) ligado ao fim do R2 (P7), que já é GND
}

def rede_de(arestas, nos):
    pai = {n: n for n in nos}
    def raiz(a):
        while pai[a] != a:
            pai[a] = pai[pai[a]]; a = pai[a]
        return a
    for a, b in arestas:
        pai.setdefault(a, a); pai.setdefault(b, b)
        pai[raiz(a)] = raiz(b)
    return raiz

def verificar():
    # Monta as redes só com o que é condutor (barramentos, fios, pontes) e compara com o esquemático.
    arestas = []
    for _, (_, furos) in BARRAMENTOS.items():
        arestas += list(zip(furos, furos[1:]))
    for nome, (_, furos, _) in FIOS.items():
        if nome in RESISTOR_NO_FIO:
            continue  # o resistor no meio do fio impede que as duas pontas sejam a mesma rede
        arestas.append(tuple(furos))
    for furos in PONTES.values():
        arestas.append(tuple(furos))
    todos = {f for a in arestas for f in a}
    for _, (_, furos) in COMPONENTES.items():
        todos |= set(furos)
    todos |= {pino_esq(i) for i in range(1, 11)} | {pino_dir(i) for i in range(1, 11)}
    r = rede_de(arestas, todos)
    rede = lambda f: r(f)
    erros = []
    def igual(*furos):
        if len({rede(f) for f in furos}) != 1: erros.append(f"deveriam estar na mesma rede: {furos}")
    def diferente(a, b, nome):
        if rede(a) == rede(b): erros.append(f"curto: {nome}")
    # redes esperadas
    V5, GND = "J1", "J2"; TRIG, TRIGE, ECHO = "Q3", "D3", "Q5"; X = "L6"
    igual("J1", "M1", "Q1")                      # 5V: pino 5V, C1+, VCC do sensor
    igual("J2", "L4", "M4", "P7", "Q7")          # GND: pino GND, C1- (M4), fim do divisor (R2), GND do sensor (pela ponte G)
    igual("Q5", "P6")                            # ECHO -> R1
    igual("L6", "L7", "D4")                      # nó do divisor -> GPIO1
    redes = {"5V": V5, "GND": GND, "TRIG": TRIG, "TRIGE": TRIGE, "ECHO": ECHO, "X": X}
    nomes = list(redes)
    for i in range(len(nomes)):
        for j in range(i + 1, len(nomes)):
            diferente(redes[nomes[i]], redes[nomes[j]], f"{nomes[i]} x {nomes[j]}")
    # pinos que não podem ser tocados
    for i in range(3, 11):
        if pino_dir(i) in todos and rede(pino_dir(i)) in {rede(v) for v in redes.values()}:
            erros.append(f"pino {PINOS_DIR[i-1]} (J{i}) ligado a uma rede do circuito")
    for i in (1, 2, 5, 6, 7, 8, 9, 10):
        if rede(pino_esq(i)) in {rede(v) for v in redes.values()}:
            erros.append(f"pino {PINOS_ESQ[i-1]} (D{i}) ligado a uma rede do circuito")
    # componentes entre as redes certas
    esperado = {"R1": ("ECHO", "X"), "R2": ("X", "GND"), "C1": ("5V", "GND")}
    inv = {rede(v): k for k, v in redes.items()}
    for comp, (a, b) in esperado.items():
        furos = COMPONENTES[comp][1]
        ra = inv.get(rede(furos[0])); rb = inv.get(rede(furos[1]))
        # C1: + em L1 (5V), - em L4 (GND); R1: a=P6 (ECHO), b=L6 (X); R2: a=L7 (X), b=P7 (GND)
        if (ra, rb) != (a, b): erros.append(f"{comp} ligado a {ra}/{rb}, esperado {a}/{b}")
    for comp, (_, furos) in SOBRE_ILHAS.items():
        ra = inv.get(rede(furos[0])); rb = inv.get(rede(furos[1]))
        if (ra, rb) != ("5V", "GND"): erros.append(f"{comp} ligado a {ra}/{rb}, esperado 5V/GND")
    # S1: VCC, TRIG, ECHO, GND
    s1 = [inv.get(rede(f)) for f in COMPONENTES["S1"][1]]
    if s1 != ["5V", "TRIG", "ECHO", "GND"]: erros.append(f"S1 ligado a {s1}")
    # furos com mais de 2 itens inseridos (terminais de componentes + pontas de fios + pinos do soquete)
    uso = {}
    for _, (_, f) in COMPONENTES.items():
        for h in f: uso[h] = uso.get(h, 0) + 1
    for _, (_, f, _) in FIOS.items():
        for h in f: uso[h] = uso.get(h, 0) + 1
    for i in range(1, 11):
        for h in (pino_esq(i), pino_dir(i)): uso[h] = uso.get(h, 0) + 1
    for h, n in uso.items():
        if n > 2: erros.append(f"furo {h} com {n} itens")
    # caminhos dos fios: começam e terminam nos furos declarados
    for nome, (_, f, cam) in FIOS.items():
        ini, fim = f"{cam[0][0]}{cam[0][1]}", f"{cam[-1][0]}{cam[-1][1]}"
        if (ini, fim) != tuple(f): erros.append(f"{nome}: caminho {ini}->{fim} difere de {f}")
    return erros

if __name__ == "__main__":
    e = verificar()
    print("REDES CONFERIDAS: OK (sem erros)" if not e else "ERROS:\n  " + "\n  ".join(e))
