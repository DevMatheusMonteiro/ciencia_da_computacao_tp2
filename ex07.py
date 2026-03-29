from collections import deque
import random, statistics, sys
sys.setrecursionlimit(100000)

# ── Utilitários ────────────────────────────────────────────────────────────────

def identity_key(x):
    """Normaliza a chave de comparação: retorna x[1] se tupla, senão x.
    Funciona tanto para candidatos (idx, val) quanto para elementos brutos."""
    return x[1] if isinstance(x, tuple) else x

def middle_index(lst, size=None):
    """Retorna o índice do meio. Se size for None, usa len(lst); caso contrário
    usa size diretamente (ex.: middle_index(arr, left+right) → (left+right)//2)."""
    if size is None:
        size = len(lst)
    return size // 2

def median_of_3(candidates, key=None):
    min_a_b = min(candidates[0], candidates[1], key=key)
    min_b_c = min(candidates[1], candidates[2], key=key)
    min_a_c = min(candidates[0], candidates[2], key=key)
    return max(min_a_b, min_b_c, min_a_c, key=key)

# ── Contadores globais (resetados antes de cada chamada de benchmark) ─────────

comparacoes = 0
recursoes   = 0
trocas      = 0

# ── QuickSelect Naive ─────────────────────────────────────────────────────────

def partition_naive(arr, left, right):
    global comparacoes, trocas
    pivot_index = arr[right]
    i  = left - 1
    for j in range(left, right):
        comparacoes += 1
        if arr[j] <= pivot_index:
            i += 1
            if i != j:
                arr[i], arr[j] = arr[j], arr[i]
                trocas += 1
    if i + 1 != right:
        arr[i + 1], arr[right] = arr[right], arr[i + 1]
        trocas += 1
    return i + 1

def qs_naive(arr, left, right, k):
    global recursoes
    if left == right:
        return arr[left]
    pivot_index = partition_naive(arr, left, right)
    if k == pivot_index:
        return arr[pivot_index]
    if k < pivot_index:
        recursoes += 1
        return qs_naive(arr, left, pivot_index - 1, k)
    recursoes += 1
    return qs_naive(arr, pivot_index + 1, right, k)

# ── Partição hist ────────────────────────────────────────────────────

def partition_hist(arr, left, right, pivot, key=identity_key):
    """Particiona arr[left..right] usando pivot=(index, raw_value).
    key é aplicada aos elementos de arr para comparação."""
    global comparacoes, trocas
    pivot_index, pivot_value = pivot
    if pivot_index != right:
        arr[pivot_index], arr[right] = arr[right], arr[pivot_index]
        trocas += 1
    i = left - 1
    for j in range(left, right):
        comparacoes += 1
        if key(arr[j]) <= key(pivot_value):
            i += 1
            if i != j:
                arr[i], arr[j] = arr[j], arr[i]
                trocas += 1
    if i + 1 != right:
        arr[i + 1], arr[right] = arr[right], arr[i + 1]
        trocas += 1
    return i + 1

# ── QuickSelect com Histórico (pivô aleatório) ────────────────────────────────
#
# Histórico armazena o ÍNDICE do ponto médio do próximo subarray, calculado
# após a partição (com conhecimento de onde o pivô pousou):
#   k < pivot_index → armazena (left + pivot_index) // 2  (mid do subarray esquerdo)
#   k > pivot_index → armazena (pivot_index + right) // 2 (mid do subarray direito)
# Candidatos são filtrados por [left, right] a cada chamada.
# Se len(candidates) >= 3: sorteia aleatoriamente um candidato do histórico — O(1).
# Se len(candidates) < 3: fallback com índice aleatório em [left, right] — O(1).
# Complexidade: O(n) melhor/médio esperado, O(n²) pior teórico (improvável com
# aleatoriedade).

branch_counts = {"hist": 0, "else": 0}

def qs_hist(arr, left, right, k, history, history_size=3, key=identity_key):
    global recursoes
    if left == right:
        return arr[left]

    candidates = [(i, arr[i]) for i in history if left <= i <= right]

    if len(candidates) >= 3:
        branch_counts["hist"] += 1
        pivot = random.choice(candidates)
    else:
        branch_counts["else"] += 1
        idx = random.randint(left, right)
        pivot = (idx, arr[idx])

    pivot_index = partition_hist(arr, left, right, pivot, key=key)

    if k == pivot_index:
        return arr[pivot_index]
    if k < pivot_index:
        history.append((left + pivot_index) // 2)
        if len(history) > history_size:
            history.popleft()
        recursoes += 1
        return qs_hist(arr, left, pivot_index - 1, k, history, history_size, key)
    history.append((pivot_index + right) // 2)
    if len(history) > history_size:
        history.popleft()
    recursoes += 1
    return qs_hist(arr, pivot_index + 1, right, k, history, history_size, key)

# ── QuickSelect Median-of-3 ───────────────────────────────────────────────────
#
# Pivô escolhido via median_of_3(left, mid, right) a cada chamada — O(1) garantido.
# Sem histórico: cada chamada escolhe o pivô olhando apenas o subarray atual.
# Elimina a degeneração O(n²) do naive em dados ordenados sem overhead de deque.
# Complexidade: O(n) melhor/médio, O(n²) pior teórico (sequências adversárias).

def qs_m3(arr, left, right, k, key=identity_key):
    global recursoes
    if left == right:
        return arr[left]
    mid   = middle_index(arr, left + right)
    three = [(left, arr[left]), (mid, arr[mid]), (right, arr[right])]
    pivot = median_of_3(three, key=key)
    pivot_index = partition_hist(arr, left, right, pivot, key=key)
    if k == pivot_index:
        return arr[pivot_index]
    if k < pivot_index:
        recursoes += 1
        return qs_m3(arr, left, pivot_index - 1, k, key)
    recursoes += 1
    return qs_m3(arr, pivot_index + 1, right, k, key)

def kth_smallest(arr, k, history_size=3):
    if k < 1 or k > len(arr):
        raise ValueError(f"k={k} fora do intervalo [1, {len(arr)}]")
    return qs_hist(arr[:], 0, len(arr) - 1, k - 1, deque(), history_size)


# ── Funções de benchmark ──────────────────────────────────────────────────────

def _reset(counts=None):
    global comparacoes, recursoes, trocas
    comparacoes = recursoes = trocas = 0
    if counts is not None:
        counts["hist"] = counts["else"] = 0

def bench_naive(arr, k):
    _reset()
    qs_naive(arr[:], 0, len(arr) - 1, k - 1)
    return comparacoes, recursoes, trocas

def bench_hist(arr, k):
    _reset(branch_counts)
    kth_smallest(arr, k)
    return comparacoes, recursoes, trocas, dict(branch_counts)

def bench_m3(arr, k):
    _reset()
    if k < 1 or k > len(arr):
        raise ValueError(f"k={k} fora do intervalo [1, {len(arr)}]")
    qs_m3(arr[:], 0, len(arr) - 1, k - 1)
    return comparacoes, recursoes, trocas

# ── Análise comparativa ───────────────────────────────────────────────────────
#
# Três variantes comparadas com as mesmas entradas:
#   Naive : pivô sempre arr[right]. Determinístico.
#           Complexidade: O(n) melhor/médio, O(n²) pior (arrays ordenados).
#
#   Hist  : histórico armazena midpoints do próximo subarray; pivô sorteado
#           aleatoriamente entre os candidatos (>= 3) ou índice aleatório em
#           [left, right] (fallback). Seleção O(1) — sem recursão interna.
#           Complexidade: O(n) esperado, O(n²) no pior caso com pivot aleatório ruim.
#           Em dados ordenados elimina a degeneração por aleatoriedade + histórico.
#
#   M3    : pivô via median_of_3(left, mid, right) a cada chamada — O(1).
#           Sem histórico; sem aleatoriedade.
#           Complexidade: O(n) médio, O(n²) pior teórico (sequências adversárias
#           específicas ao padrão de median-of-3 existem, mas são raras na prática).
#
# Métricas:
#   cmps  : comparações entre elementos (custo dominante)
#   rec   : chamadas recursivas (profundidade da pilha)
#   trocas: movimentações efetivas de elementos
#
# Branches (qs_hist):
#   hist : chamadas em que havia >= 3 candidatos válidos na range (pivô do histórico)
#   else : chamadas em que o histórico era insuficiente (pivô aleatório em [l,r])
#
# ── Hist vs Naive ─────────────────────────────────────────────────────────────
#   Arrays ordenados: Hist é muito MELHOR (~98-99.6% menos comparações e
#     ~94-99% menos recursões). O pivô aleatório, guiado pelo histórico de
#     midpoints, quebra a degeneração O(n²) do naive.
#   Arrays aleatórios/duplicatas: Hist é levemente PIOR (~1-3% mais comparações
#     e recursões). Pivô aleatório do histórico não supera arr[right] em média
#     para dados sem estrutura — ambos operam em O(n) esperado.
#
# ── M3 vs Naive ───────────────────────────────────────────────────────────────
#   Arrays ordenados: M3 é muito MELHOR (~97-99.7% menos comparações e recursões).
#   Arrays aleatórios/duplicatas: M3 é MELHOR (~14-17% menos comparações e
#     ~9-16% menos recursões). Pivô mediano de três posições fixas é
#     deterministicamente mais central que arr[right].
#
# ── M3 vs Hist ────────────────────────────────────────────────────────────────
#   Arrays ordenados: desempenho equivalente (~98-99.6% de redução em ambos).
#   Arrays aleatórios/duplicatas: M3 é claramente MELHOR (~14-18% menos
#     comparações). O pivô aleatório do Hist não traz vantagem sobre o pivô
#     mediano determinístico do M3 em dados sem estrutura — e ainda sofre
#     ligeiro aumento de comparações vs naive (~1-3%).

random.seed(42)

cenarios = [
    ("Aleatorio",         lambda n: random.sample(range(n * 3), n), 200, [500, 2000]),
    ("Crescente",         lambda n: list(range(n)),                   20, [500, 2000]),
    ("Decrescente",       lambda n: list(range(n, 0, -1)),            20, [500, 2000]),
    ("Quase ordenado",    lambda n: list(range(n - 5)) + list(range(n - 5, n))[::-1], 20, [500, 2000]),
    ("Muitas duplicatas", lambda n: [random.randint(0, n // 5) for _ in range(n)], 200, [500, 2000]),
]

# ── Tabela 1: comparações, recursões, trocas ─────────────────────────────────

W = 155
print("=" * W)
print("TABELA 1 — Comparacoes, Recursoes e Trocas (medias por chamada)")
print("=" * W)
cab = (
    f"{'Cenario':<22} {'N':>5} | "
    f"{'Naive':^30} | "
    f"{'Hist':^30} | "
    f"{'M3':^30} | "
    f"{'Red cmps':^16} | "
    f"{'Red rec':^14}"
)
sub = (
    f"{'':22} {'':5} | "
    f"{'cmps':>8} {'rec':>6} {'trocas':>8} {'cmps max':>8} | "
    f"{'cmps':>8} {'rec':>6} {'trocas':>8} {'cmps max':>8} | "
    f"{'cmps':>8} {'rec':>6} {'trocas':>8} {'cmps max':>8} | "
    f"{'Hist':>7} {'M3':>7} | "
    f"{'Hist':>6} {'M3':>6}"
)
print(cab)
print(sub)
print("-" * W)

resultados = {}

for label, gen, trials, sizes in cenarios:
    resultados[label] = {}
    for N in sizes:
        cn, rn, tn = [], [], []
        ch, rh, th, rb = [], [], [], {"hist": [], "else": []}
        cm, rm, tm     = [], [], []

        for _ in range(trials):
            arr = gen(N)
            k   = random.randint(1, N)

            c, r, t         = bench_naive(arr, k)
            cn.append(c); rn.append(r); tn.append(t)

            c, r, t, counts = bench_hist(arr, k)
            ch.append(c); rh.append(r); th.append(t)
            for b in rb:
                rb[b].append(counts[b])

            c, r, t         = bench_m3(arr, k)
            cm.append(c); rm.append(r); tm.append(t)

        mcn, mrn = statistics.mean(cn), statistics.mean(rn)
        mch, mrh = statistics.mean(ch), statistics.mean(rh)
        mcm, mrm = statistics.mean(cm), statistics.mean(rm)

        red_ch = (mcn - mch) / mcn * 100 if mcn > 0 else 0.0
        red_cm = (mcn - mcm) / mcn * 100 if mcn > 0 else 0.0
        red_rh = (mrn - mrh) / mrn * 100 if mrn > 0 else 0.0
        red_rm = (mrn - mrm) / mrn * 100 if mrn > 0 else 0.0

        resultados[label][N] = rb

        print(
            f"{label:<22} {N:>5} | "
            f"{mcn:>8.0f} {mrn:>6.1f} {statistics.mean(tn):>8.0f} {max(cn):>8} | "
            f"{mch:>8.0f} {mrh:>6.1f} {statistics.mean(th):>8.0f} {max(ch):>8} | "
            f"{mcm:>8.0f} {mrm:>6.1f} {statistics.mean(tm):>8.0f} {max(cm):>8} | "
            f"{red_ch:>6.1f}% {red_cm:>6.1f}% | "
            f"{red_rh:>5.1f}% {red_rm:>5.1f}%"
        )
    print()

# ── Tabela 2: branches do histórico (qs_hist) ────────────────────────────────

print("=" * 55)
print("TABELA 2 — Branches do historico por chamada (qs_hist)")
print("=" * 55)
print(f"{'Cenario':<22} {'N':>5} | {'hist':>8} {'else':>8}")
print("-" * 55)

for label, gen, trials, sizes in cenarios:
    for N in sizes:
        rb = resultados[label][N]
        print(
            f"{label:<22} {N:>5} | "
            f"{statistics.mean(rb['hist']):>8.1f} {statistics.mean(rb['else']):>8.1f}"
        )
    print()
