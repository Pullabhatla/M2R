import numpy as np
def simple_swap(list_before_swap):
    n = len(list_before_swap)
    a = np.random.randint(n)
    b = np.random.randint(n)
    while b==a:
        b = np.random.randint(n)
    swap_index = [a, b]
    swap_value = [list_before_swap[a], list_before_swap[b]]
    for i in range(2):
        list_before_swap[swap_index[i]] = swap_value[1-i]

    return list_before_swap
