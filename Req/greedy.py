"""Implementation of greedy TSP algorithms."""

from Req import Hamiltonian


def nearest_neighbour(map, start=0):
    """
    Make the locally optimal choice at each step.

    Parameters
    ----------
    map : Map
        The map being investigated.
    start: int, optional
        Index of the starting node of the tour.
        Default is zero.

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
            elif map.D[x, i] < map.D[x, min_idx] or min_idx in tour:
                min_idx = i

        tour.append(min_idx)

    return Hamiltonian(tuple(tour), map)


def best_nn(map):
    """
    Implement nearest_neighbour repeatedly and return best greedy tour.

    Parameters
    ----------
    map : Map
        The map being investigated.
    Returns
    -------
    Hamiltonian
        A sub-optimal tour.
    """
    tours = []
    for i in range(len(map)):
        tours.append(nearest_neighbour(map, i))

    return min(tours)
