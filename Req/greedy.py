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


def two_opt_swap(i, j, tour):
    """
    Perform a 2-opt swap with i<j.

    Parameters
    ----------
    i : int
        Smaller index of node to be swapped.
    j : int
        Greater index of node to be swapped with.
    tour : Hamiltonian
        The Hamiltonian cycle being investigated.

    Returns
    -------
    Hamiltonian
        The tour after performing the swap.
    """
    new_cycle = tour.cycle[:i] + tour.cycle[i:j+1][::-1] + tour.cycle[j+1:]

    return Hamiltonian(new_cycle, tour.map)


def repeated_2_opt(tour):
    """
    Repeatedly apply 2-opt swaps to a tour.

    Parameter
    ---------
    tour : Hamiltonian
        The Hamiltonian cycle being investigated.

    Returns
    -------
    Hamiltonian
        The tour after performing the swaps.
    """
    pre_iter = None
    post_iter = tour

    while pre_iter == None or post_iter.cost() < pre_iter.cost():
        pre_iter = post_iter
        opt_tour = post_iter
        for i in range(len(tour) - 1):
            break_out_flag = False
            for j in range(i+1, len(tour)):
                swap_tour = two_opt_swap(i, j, tour)
                if swap_tour.cost() < opt_tour.cost():
                    opt_tour = swap_tour
                    break_out_flag = True
                    break
            if break_out_flag:
                break
        post_iter = opt_tour

    return opt_tour
