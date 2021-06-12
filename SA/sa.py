"""An implementation of Simulated Annealing."""

from Req.greedy import two_opt_swap
from Req.req import Hamiltonian
import numpy as np


def random_swap(tour):
    """Randomly choose and swap two nodes in a cycle."""
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
    """Randomly remove a node and inject elsewhere in the cycle."""
    n = len(tour)
    a = np.random.randint(n-1)
    b = np.random.randint(a + 1, n)

    return Hamiltonian(tuple(list(tour.cycle[:a]) + [tour.cycle[b]]
                             + list(tour.cycle[a:b]) + list(tour.cycle[b+1:])),
                       tour.map)


def random_block_insert_mutation(tour):
    """Randomly remove consecutive nodes and inject elsewhere in the cycle."""
    n = len(tour)
    a = np.random.randint(n - 2)
    b = np.random.randint(a + 1, n - 1)
    c = np.random.randint(b + 1, n)

    return Hamiltonian(tuple(list(tour.cycle[:a]) + list(tour.cycle[b:c+1])
                             + list(tour.cycle[a:b]) + list(tour.cycle[c+1:])),
                       tour.map)


def random_block_reverse_mutation(tour):
    """Randomly apply a 2-opt swap to the tour."""
    n = len(tour)
    a = np.random.randint(n - 1)
    b = np.random.randint(a + 1, n)
    return two_opt_swap(a, b, tour)


def hybrid(tour, a=0.89, b=0.1):
    """Cocktail of tour mutations."""
    n = np.random.random()

    if n < a:
        return random_block_reverse_mutation(tour)
    elif n < a + b:
        return random_vertex_insert_mutation(tour)
    else:
        return random_block_insert_mutation(tour)


def simulated_annealing(tour, t0=100, alpha=0.99, int_its=20, swap=hybrid):  # noqa E501
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
