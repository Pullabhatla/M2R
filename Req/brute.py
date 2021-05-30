"""Required objects for a brute force approach to the TSP."""


def brute_tour(map):
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
    ham_cycles = [i for i in map.alltours() if i.tour[0] == 0]

    return min(ham_cycles)
