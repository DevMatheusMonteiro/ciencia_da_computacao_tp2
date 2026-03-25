from collections import deque


def median_of(arr, indices):
    values = sorted(arr[i] for i in indices)
    return values[len(values) // 2]


def partition_with_pivot_value(arr, left, right, pivot_val):
    # Move o pivot para o final antes de particionar
    for i in range(left, right + 1):
        if arr[i] == pivot_val:
            arr[i], arr[right] = arr[right], arr[i]
            break

    pivot = arr[right]
    i = left - 1
    for j in range(left, right):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i + 1], arr[right] = arr[right], arr[i + 1]
    return i + 1


def quickselect_adaptive(arr, left, right, k, history, history_size):
    if left == right:
        return arr[left]

    # Candidatos: histórico de índices que ainda estão no subarray atual
    candidates = [i for i in history if left <= i <= right]

    if len(candidates) >= 2:
        # Usa a mediana dos pivôs históricos válidos
        pivot_val = median_of(arr, candidates)
    else:
        # Fallback: mediana entre primeiro, meio e último
        mid = (left + right) // 2
        trio = sorted([arr[left], arr[mid], arr[right]])
        pivot_val = trio[1]

    pivot_index = partition_with_pivot_value(arr, left, right, pivot_val)

    # Atualiza histórico com o índice do pivô recém-escolhido
    history.append(pivot_index)
    if len(history) > history_size:
        history.popleft()

    if k == pivot_index:
        return arr[pivot_index]
    elif k < pivot_index:
        return quickselect_adaptive(arr, left, pivot_index - 1, k, history, history_size)
    else:
        return quickselect_adaptive(arr, pivot_index + 1, right, k, history, history_size)


def kth_smallest(arr, k, history_size=3):
    if k < 1 or k > len(arr):
        raise ValueError(f"k={k} fora do intervalo [1, {len(arr)}]")
    history = deque()
    return quickselect_adaptive(arr[:], 0, len(arr) - 1, k - 1, history, history_size)


if __name__ == "__main__":
    vetor = [7, 2, 1, 6, 5, 3, 4, 8]
    print(f"Vetor: {vetor}")
    print()

    for k in [1, 3, 5, 8]:
        resultado = kth_smallest(vetor, k, history_size=3)
        print(f"{k}º menor elemento: {resultado}")

    print()
    print("=== Análise do impacto ===")
    print("""
Pivô padrão (QuickSelect original):
  - Sempre escolhe arr[right], o que pode gerar O(n²) no pior caso
    (ex.: vetor já ordenado).

Pivô com histórico das últimas k escolhas:
  - Acumula os índices dos k pivôs anteriores e usa a mediana
    dos que ainda pertencem ao subarray corrente.
  - Tende a escolher pivôs mais centrais conforme o histórico
    cresce, reduzindo a chance de partições desequilibradas.
  - Benefício maior em vetores com padrões repetidos ou ordenados.
  - Custo extra: O(k) por chamada para filtrar e calcular a mediana,
    mas k é pequeno (constante), portanto a complexidade média
    permanece O(n).
  - Não garante O(n) no pior caso (como Median-of-Medians faz),
    mas na prática reduz a probabilidade de degeneração.
""")
