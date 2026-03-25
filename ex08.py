import random
import time


# ── QuickSort simples (pivô = último elemento) ──────────────────────────────

def partition_simple(arr, left, right):
    pivot = arr[right]
    i = left - 1
    for j in range(left, right):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i + 1], arr[right] = arr[right], arr[i + 1]
    return i + 1


def quicksort_simple(arr, left, right):
    if left < right:
        pi = partition_simple(arr, left, right)
        quicksort_simple(arr, left, pi - 1)
        quicksort_simple(arr, pi + 1, right)


# ── QuickSort com mediana de três ───────────────────────────────────────────

def median_of_three(arr, left, right):
    mid = (left + right) // 2
    # Ordena as três posições e retorna o índice do valor mediano
    if arr[left] > arr[mid]:
        arr[left], arr[mid] = arr[mid], arr[left]
    if arr[left] > arr[right]:
        arr[left], arr[right] = arr[right], arr[left]
    if arr[mid] > arr[right]:
        arr[mid], arr[right] = arr[right], arr[mid]
    # arr[mid] é a mediana; coloca no penúltimo para não atrapalhar a partição
    arr[mid], arr[right - 1] = arr[right - 1], arr[mid]
    return arr[right - 1]


def partition_median(arr, left, right):
    if right - left < 2:
        if arr[left] > arr[right]:
            arr[left], arr[right] = arr[right], arr[left]
        return left

    pivot = median_of_three(arr, left, right)
    i = left
    j = right - 1

    while True:
        i += 1
        while arr[i] < pivot:
            i += 1
        j -= 1
        while arr[j] > pivot:
            j -= 1
        if i >= j:
            break
        arr[i], arr[j] = arr[j], arr[i]

    arr[i], arr[right - 1] = arr[right - 1], arr[i]
    return i


def quicksort_median(arr, left, right):
    if right - left < 2:
        if left < right and arr[left] > arr[right]:
            arr[left], arr[right] = arr[right], arr[left]
        return
    pi = partition_median(arr, left, right)
    quicksort_median(arr, left, pi - 1)
    quicksort_median(arr, pi + 1, right)


# ── Utilitários ─────────────────────────────────────────────────────────────

def sort_and_time(sort_fn, arr):
    data = arr[:]
    start = time.perf_counter()
    sort_fn(data, 0, len(data) - 1)
    elapsed = time.perf_counter() - start
    assert data == sorted(arr), "Ordenação incorreta!"
    return elapsed


def benchmark(label, arr):
    print(f"\n{label} (n={len(arr)}):")
    t_simple = sort_and_time(quicksort_simple, arr)
    t_median = sort_and_time(quicksort_median, arr)
    print(f"  QuickSort simples        : {t_simple * 1000:.3f} ms")
    print(f"  QuickSort mediana-de-três: {t_median * 1000:.3f} ms")
    ganho = (t_simple - t_median) / t_simple * 100 if t_simple > 0 else 0
    if ganho > 0:
        print(f"  Mediana-de-três foi {ganho:.1f}% mais rapida")
    else:
        print(f"  Simples foi {-ganho:.1f}% mais rapido")


# ── Cenários de teste ────────────────────────────────────────────────────────

if __name__ == "__main__":
    import sys
    sys.setrecursionlimit(10000)

    N = 3000

    aleatorio      = random.sample(range(N * 10), N)
    ordenado       = list(range(N))
    invertido      = list(range(N, 0, -1))
    quase_ordenado = list(range(N))
    for _ in range(N // 20):        # 5 % das posições trocadas
        i, j = random.randrange(N), random.randrange(N)
        quase_ordenado[i], quase_ordenado[j] = quase_ordenado[j], quase_ordenado[i]

    benchmark("Vetor aleatório",       aleatorio)
    benchmark("Vetor ordenado",        ordenado)
    benchmark("Vetor invertido",       invertido)
    benchmark("Vetor quase ordenado",  quase_ordenado)

    print("""
=== Análise ===
Vetor aleatório:
  Ambas as versões têm desempenho similar (O(n log n) médio).
  A mediana-de-três adiciona overhead mínimo que pode deixá-la
  ligeiramente mais lenta em dados já aleatórios.

Vetores ordenados / invertidos (pior caso do QuickSort simples):
  O pivô = último elemento gera partições degeneradas (0 e n-1),
  resultando em O(n²) e risco de estouro de pilha.
  A mediana-de-três escolhe um pivô central, mantendo O(n log n).

Vetor quase ordenado:
  Situação frequente na prática. O QuickSort simples sofre
  degradação proporcional ao grau de ordenação; a mediana-de-três
  resiste bem por escolher pivôs mais balanceados.

Conclusão:
  A mediana-de-três praticamente elimina o pior caso em vetores
  com algum grau de ordenação, com custo extra desprezível (3
  comparações por chamada recursiva).
""")
