"""
An implementation of Robinson's algorithm.

See 'ON THE HAMILTONIAN GAME (A Travelling Salesmen Problem)' by Robinson J.
"""

from itertools import permutations
from Req import Circuit, System


def circuit_finder(system):
    """
    Find a circuit of negative s-length.

    Parameters
    ----------
    system : System
        The system of circuits under study.

    Returns
    -------
    Circuit or None
        A circuit with negative s-length if found or None type object.
    """
    n = len(system)
    nodes = [i for i in range(n)]
    map = system.map
    for i in range(2, n):
        for test in permutations(nodes, i):
            if system.s_length(Circuit(test, map)) < 0:
                return Circuit(test, map)

    return None


def robinson_solver(system):
    """
    Find a system which admits no circuits of negative s-length.

    Parameters
    ----------
    system : System
        The system of circuits under study.

    Returns
    -------
    System
        A system of minimal cost.
    """
    while circuit_finder(system) is not None:
        circ = circuit_finder(system)
        paths = system.journeys
        for i in circ:
            idx = paths.index((i, system.i_[i]))
