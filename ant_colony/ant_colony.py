"""Implementation of Ant colony optimisation for TSP."""

import numpy as np
from Req import Hamiltonian


def ant_colony(map, alpha=3, beta=3, m=10, rho=0.2, q=1, its_max=10):
    """
    Perform ant colony optimisation on a map.

    Parameters
    ----------
    map : Map
        The map being investigated.
    alpha : float
        how likely ant choose their way depend on pheromone
    beta : float
        dependence of path distance on ants' route
    m : int
        The number of ants in the colony.
    rho : float
        Rate of evaporation of pheromone.
    q : float
        Amount of pheromone an ant secretes.
    its_max : int
        The number of iterations to run through.

    Returns
    -------
    Hamiltonian
        A tour of optimal or sub-optimal length.
    """
    n = len(map)
    tau = np.ones((n, n))
    eta = 1/map.D
    for i in range(n):
        eta[i, i] = 0
    paths_array = np.zeros((m, n), int)
    its = 0
    path_best = np.zeros((its_max, n), int)
    distance_best = np.zeros(its_max)

    while its < its_max:
        paths_length = np.zeros(m)
        for i in range(m):
            source = np.random.randint(n)
            visited = []
            unvisited = list(range(n))
            node_now = source
            node_next = -1
            paths_array[i, 0] = source

            for j in range(1, n):
                visited.append(node_now)
                unvisited.remove(node_now)
                prob_roulette = [0]*n
                for k in unvisited:
                    prob_roulette[k] = (pow(tau[node_now, k], alpha)
                                        * pow(eta[node_now, k], beta))
                prob_roulette = prob_roulette/sum(prob_roulette)
                cum_roulette = prob_roulette.cumsum()
                cum_roulette -= np.random.uniform(0, 1)
                node_next = list(cum_roulette > 0).index(True)
                paths_array[i, j] = node_next
                paths_length[i] += map.D[node_now, node_next]
                node_now = node_next
            paths_length[i] += map.D[node_now, source]

        if its == 0:
            distance_best[its] = paths_length.min()
            path_best[its] = paths_array[paths_length.argmin()].copy()
        else:
            if distance_best[its-1] < paths_length.min():
                distance_best[its] = distance_best[its-1]
                path_best[its] = path_best[its-1].copy()
            else:
                distance_best[its] = paths_length.min()
                path_best[its] = paths_array[paths_length.argmin()].copy()

        add_tau = np.zeros((n, n))

        for i in range(m):
            for j in range(n):
                row = paths_array[i, j]
                col = paths_array[i, (j+1) % n]
                add_tau[row][col] += q/paths_length[i]

        tau = (1 - rho)*tau + add_tau

        its += 1

    return Hamiltonian(path_best[-1], map)
