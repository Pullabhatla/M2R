"""Required objects for a brute force approach to the TSP."""


def minimal_tour(map):
    """
    Return a possibly non-unique minimal solution to the TSP by brute-force.

    Parameter
    ---------
    map: Map
        The map being investigated.
    Returns
    -------
    Hamiltonian
        A tour of minimum cost.
    """
    ham_cycles = map.alltours()

    return min(ham_cycles)
