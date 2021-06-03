"""An implementation of the Bellman-Held-Karp algorithm."""

from functools import lru_cache
from Req import Segment, Hamiltonian


@lru_cache(None)
def shortest_segment(to_visit, dest_idx, map):
    """
    Return the shortest segment.

    Return the shortest segment starting at 0, passing through all nodes in
    subset, and ending at dest_idx.

    Parameters
    ----------
    to_vist : tuple
        The tuple of nodes to traverse through.
    dest_idx : int
        The index of the destination node.
    map : Map
        The map being investigated.

    Returns
    -------
    Segment
        Segment of nodes to be visited.
    """
    if not to_visit:
        return Segment([0, dest_idx], map)

    else:
        return min(Segment(shortest_segment(tuple(i for i in to_visit if i != c),
                                            c, map).nodes
                           + [dest_idx], map) for c in to_visit)


def held_karp(map):
    """
    Return the optimal tour in exponential time.

    Parameters
    ----------
    map : Map
        The map being investigated.

    Returns
    -------
    Hamiltonian
        The optimal tour.
    """
    nodes = [i for i in range(1, len(map))]

    dummy = min(Hamiltonian(shortest_segment(tuple(i for i in nodes if i != d),
                                             d, map).nodes, map)
                for d in nodes if d != 0)

    shortest_segment.cache_clear()  # clear cache for unbiased testing

    return dummy
