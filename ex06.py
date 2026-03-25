def partition(arr, left, right):
    pivot = arr[right]
    i = left - 1

    for j in range(left, right):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]

    arr[i + 1], arr[right] = arr[right], arr[i + 1]
    return i + 1

def quickselect(arr, left, right, k):
    if left == right:
        return arr[left]

    pivot_index = partition(arr, left, right)

    if k == pivot_index:
        return arr[pivot_index]
    elif k < pivot_index:
        return quickselect(arr, left, pivot_index - 1, k)
    else:
        return quickselect(arr, pivot_index + 1, right, k)

def kth_smallest(arr, k):
    if k < 1 or k > len(arr):
        raise ValueError(f"k={k} fora do intervalo [1, {len(arr)}]")
    return quickselect(arr[:], 0, len(arr) - 1, k - 1)

vetor = [7, 2, 1, 6, 5, 3, 4, 8]
print(f"Vetor: {vetor}")

for k in [1, 3, 5, 8]:
    resultado = kth_smallest(vetor, k)
    print(f"{k}º menor elemento: {resultado}")
