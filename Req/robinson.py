"""
An implementation of Robinson's algorithm.

See 'ON THE HAMILTONIAN GAME (A Travelling Salesmen Problem)' by Robinson J.
"""

from itertools import permutations
from Req import Circuit, System


def system_builder(paths, map):
    """Build a system of circuits from a list of steps."""
    circuits = []
    n = len(paths)
    while sum(len(i) for i in circuits) < n:
        dummy = paths
        cycle = list(dummy.pop())
        d = 0

        while d != len(paths):
            d = len(paths)
            for i, j in dummy:
                if i in cycle and j in cycle:
                    paths.pop(paths.index((i, j)))
                elif i in cycle:
                    paths.pop(paths.index(i, j))
                    cycle.append(j)

        circuits.append(Circuit(cycle, map))
    return System(circuits)


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
        path = system.journeys
        ln = len(circ)
        for n, i in enumerate(circ):
            path[path.index((i, system.i_[i]))] = (circ.cycle[(n + 1) % ln],
                                                   system.i_[i])
        system = system_builder(path, system.map)

    return system
