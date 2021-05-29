"""An implementation of a greedy TSP algorithm."""

from .req import Hamiltonian


def greedy(map, start):
    """
    Make the locally optimal choice at each step.

    Parameters
    ----------
    map : Map
        The map being investigated.
    start: int
        Index of the starting node of the tour.

    Returns
    -------
    Hamiltonian
        A sub-optimal tour.
    """
    tour = [start]
    n = len(map)
    min_idx = start

    while len(tour) < n:
        x = tour[-1]

        for i in range(n):
            if i in tour:
                continue
            elif map.dist(x, i) < map.dist(x, min_idx) or min_idx in tour:
                min_idx = i

        tour.append(min_idx)

    return Hamiltonian(tuple(tour), map)
