"""Rede bayesiana do farol de bicicleta a dínamo (IA - UFAM, 2º Trabalho).

Estrutura:  Str -> R <- Flw ;  R -> V ;  V -> Li <- B ;  K -> Li
Inferência por enumeração (sem bibliotecas externas).
"""
from itertools import product

TF = (True, False)
STR = ("dry", "wet", "snow_covered")

# ---------- CPTs ----------
P_Str = {"dry": 0.6, "wet": 0.3, "snow_covered": 0.1}
P_Flw = {True: 0.1, False: 0.9}
P_B = {True: 0.95, False: 0.05}
P_K = {True: 0.98, False: 0.02}
# P(R=t | Str, Flw)
P_R_t = {("dry", False): 0.01, ("dry", True): 0.30,
         ("wet", False): 0.10, ("wet", True): 0.60,
         ("snow_covered", False): 0.40, ("snow_covered", True): 0.90}
# P(V=t | R)
P_V_t = {True: 0.1, False: 0.9}
# P(Li=t | V, B, K)  (tabela do enunciado)
P_Li_t = {(True, True, True): 0.99, (True, True, False): 0.01,
          (True, False, True): 0.01, (True, False, False): 0.001,
          (False, True, True): 0.3, (False, True, False): 0.005,
          (False, False, True): 0.005, (False, False, False): 0.0}

def p_R(r, s, f):  return P_R_t[(s, f)] if r else 1 - P_R_t[(s, f)]
def p_V(v, r):     return P_V_t[r] if v else 1 - P_V_t[r]
def p_Li(l, v, b, k):
    p = P_Li_t[(v, b, k)]
    return p if l else 1 - p

def joint(s, f, r, v, b, k, l):
    return (P_Str[s] * P_Flw[f] * p_R(r, s, f) * p_V(v, r)
            * P_B[b] * P_K[k] * p_Li(l, v, b, k))

VARS = ("Str", "Flw", "R", "V", "B", "K", "Li")
DOM = {"Str": STR, "Flw": TF, "R": TF, "V": TF, "B": TF, "K": TF, "Li": TF}

def query(target, evidence=None):
    """P(target | evidence) por enumeração da distribuição conjunta."""
    evidence = evidence or {}
    dist = {}
    for val in DOM[target]:
        tot = 0.0
        for combo in product(*(DOM[v] for v in VARS)):
            a = dict(zip(VARS, combo))
            if a[target] != val or any(a[k] != x for k, x in evidence.items()):
                continue
            tot += joint(*combo)
        dist[val] = tot
    z = sum(dist.values())
    return {k: v / z for k, v in dist.items()}

if __name__ == "__main__":
    print("(e) P(V | Str=snow_covered) =", query("V", {"Str": "snow_covered"}))
    print("\n(d) P(Li=t | V, Str) deve ser igual para todo Str, dado V:")
    for v in TF:
        print(f"  V={v}:", {s: round(query('Li', {'V': v, 'Str': s})[True], 6) for s in STR})
    print("\n    Sem condicionar em V (dependência marginal, via Str->R->V->Li):")
    print("  ", {s: round(query('Li', {'Str': s})[True], 6) for s in STR})
    print("   P(Li=t) =", round(query('Li')[True], 6))
