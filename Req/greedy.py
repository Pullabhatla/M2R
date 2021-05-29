"""An implementation of a greedy TSP algorithm."""


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

    while len(tour) < n:
        pass
