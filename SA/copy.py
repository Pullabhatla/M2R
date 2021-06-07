"""An implementation of Simulated Annealing."""

from Req.greedy import two_opt_swap
from Req.req import Hamiltonian
import numpy as np


def simple_swap(tour):
    """
    Swap a random node with immediate neighbour and return tour.

    Parameters
    ----------
    tour : Hamiltonian
        The tour to be manipulated.
    Returns
    -------
    Hamiltonian
        The tour after manipulation.
    """
    n = len(tour)
    a = np.random.randint(n)
    nodes = list(tour.cycle)
    chosen = (nodes[a], nodes[a-1])
    for i in range(2):
        nodes[a - i] = chosen[1 - i]
    return Hamiltonian(tuple(nodes), tour.map)


def random_swap(tour):
    """Return tour after randomised swap."""
    n = len(tour)
    a = np.random.randint(n)
    b = np.random.randint(n)
    while b==a:
        b = np.random.randint(n)
    nodes = list(tour.cycle)
    swap_index = (a, b)
    swap_value = (nodes[a], nodes[b])
    for i in range(2):
        nodes[swap_index[i]] = swap_value[1-i]

    return Hamiltonian(tuple(nodes), tour.map)


def simulated_annealing(tour, t0=100, alpha=0.9, int_its=1000, swap=two_opt_swap):
    """
    Return tour after applying simulated annealing.

    Parameters
    ----------
    tour : Hamiltonian
        The tour being optimised.
    t0 : int
        The starting temperature of the system.
    alpha : float
        The geometric cooling coefficient.
    int_its : ints
        The number of iterations at each temperature level.
    swap : function
        The function manipulating the Hamiltonian tour.

    Returns
    -------
    Hamiltonian
        The tour after applying simulated annealing.
    """
    best_tour = tour
    t = t0

    while t > 10**(-5):
        for n in range(int_its):
            new_tour = swap(best_tour)
            rand = np.random.random()
            delta = new_tour.cost() - best_tour.cost()

            if delta < 0 or rand < np.exp(-(delta/t)):
                best_tour = new_tour

        t = alpha * t
