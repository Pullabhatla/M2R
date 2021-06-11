"""An implementation of Simulated Annealing."""

from Req.greedy import two_opt_swap
from Req.req import Hamiltonian
import numpy as np


def random_swap(tour):
    """Return tour after randomised swap."""
    n = len(tour)
    a = np.random.randint(n)
    b = np.random.randint(n)
    while b == a:
        b = np.random.randint(n)
    nodes = list(tour.cycle)
    swap_index = (a, b)
    swap_value = (nodes[a], nodes[b])
    for i in range(2):
        nodes[swap_index[i]] = swap_value[1-i]

    return Hamiltonian(tuple(nodes), tour.map)


def random_vertex_insert_mutation(tour):
    """Return tour after randomly inserting a node."""
    n = len(tour)
    a = np.random.randint(n-1)
    b = np.random.randint(a + 1, n)

    return tour[:a] + tour[b] + tour[a:b] + tour[b+1:]


def random_block_insert_mutation(tour):
    """Return tour after randomly swapping two blocks."""
    n = len(tour)
    a = np.random.randint(n - 2)
    b = np.random.randint(a + 1, n - 1)
    c = np.random.randint(b + 1, n)

    return tour[:a] + tour[b:c+1] + tour[c+1:]


def random_block_reverse_mutation(tour):
    """Return tour after randomised 2-opt swap."""
    n = len(tour)
    a = np.random.randint(n - 1)
    b = np.random.randint(a + 1, n)
    return two_opt_swap(a, b, tour)


def hybrid(tour):
    """Return tour after randomised hybrid swap."""
    n = np.random.random()

    if n < 0.89:
        return random_block_reverse_mutation(tour)
    elif n < 0.99:
        return random_vertex_insert_mutation(tour)
    else:
        return random_block_insert_mutation(tour)


def simulated_annealing(tour, t0=100, alpha=0.99, int_its=20, swap=random_swap):  # noqa E501
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
    return best_tour
