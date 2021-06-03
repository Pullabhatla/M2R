"""Required objects for a brute force approach to the TSP."""


def brute_tour(map):
    """
    Return an optimal solution in factorial time.

    Parameter
    ---------
    map: Map
        The map being investigated.
    Returns
    -------
    Hamiltonian
        A tour of minimum cost.
    """
    ham_cycles = [i for i in map.alltours()]

    return min(ham_cycles)
