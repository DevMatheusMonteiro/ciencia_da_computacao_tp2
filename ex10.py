import time
import random

def insertion_sort(arr, left, right):
    for i in range(left + 1, right + 1):
        key = arr[i]
        j = i - 1
        while j >= left and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key

def quicksort(arr, low, high):
    if low < high:
        pivot_index = partition(arr, low, high)
        quicksort(arr, low, pivot_index - 1)
        quicksort(arr, pivot_index + 1, high)

def quicksort_hibrido(arr, left, right):
    if right - left + 1 < 10:
        insertion_sort(arr, left, right)
        return
    if left < right:
        pivot_index = partition(arr, left, right)
        quicksort_hibrido(arr, left, pivot_index - 1)
        quicksort_hibrido(arr, pivot_index + 1, right)

def partition(arr, low, high):
    pivot = arr[high]
    i = low - 1
    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1

tamanhos = [1000, 5000, 10000, 50000]

print(f"{'Tamanho':<10} {'QuickSort (s)':<18} {'Híbrido (s)':<18} {'Diferença'}")
print("-" * 60)

for n in tamanhos:
    dados = random.sample(range(n * 10), n)

    arr1 = dados.copy()
    inicio = time.perf_counter()
    quicksort(arr1, 0, len(arr1) - 1)
    tempo_qs = time.perf_counter() - inicio

    arr2 = dados.copy()
    inicio = time.perf_counter()
    quicksort_hibrido(arr2, 0, len(arr2) - 1)
    tempo_hib = time.perf_counter() - inicio

    diff = tempo_qs - tempo_hib
    resultado = f"+{diff:.6f}s mais rápido" if diff > 0 else f"{diff:.6f}s mais lento"

    print(f"{n:<10} {tempo_qs:<18.6f} {tempo_hib:<18.6f} {resultado}")


# Conclusão:
# O híbrido tende a ser mais rápido pois o Insertion Sort é eficiente
# em vetores pequenos, evitando o overhead de chamadas recursivas desnecessárias.
