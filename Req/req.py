"""Required objects for the TSP and related problems."""

from itertools import permutations
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial.distance import euclidean


class Map:
    """
    Class implementing the map of points being used.

    Attributes
    ----------
    points : list
        A list of n-tuple Cartesian coordinates of the points on the map.
    D : numpy.ndarray
        An array with d_ij as the distance between points i and j.
    """

    def __init__(self, points, dist_func=euclidean):
        """
        Initialise self with points and distance matrix.

        Parameters
        ----------
        points : list
            A list of n-tuple Cartesian coordinates.
        dist_func : function, optional
            Function computing the distance between two points.
            Default is the Euclidean metric.
        """
        self.points = points
        self.dist_func = dist_func
        self.D = np.array([[self.dist_func(a, b) for b in points]
                           for a in points])

    def dist(self, origin_idx, destination_idx):
        """
        Return the distance between two nodes.

        Parameters
        ----------
        origin_idx : int
            Index of the origin point.
        destination_idx : int
            Index of the destination point.

        Returns
        -------
        int or float
            Distance between the origin and destination points.
        """
        return self.D[origin_idx, destination_idx]

    def __len__(self):
        """Return the number of points on the map."""
        return len(self.points)

    def show2d(self):
        """Return an indexed 2D visualisation of the map."""
        x = [i[0] for i in self.points]
        y = [j[1] for j in self.points]
        plt.scatter(x, y, s=50)
        plt.axis('scaled')
        plt.axis('off')
        for i in range(len(self.points)):
            plt.annotate(" " + str(i), (x[i], y[i]), fontsize=15)
        plt.show()

    def __iter__(self):
        """Return self on iterating."""
        self.num = 0
        return self

    def __next__(self):
        """Return a point and move to next."""
        if self.num < len(self):
            dummy = self.points[self.num]
            self.num += 1
            return dummy

        else:
            raise StopIteration

    def alltours(self, start=0):
        """Return list of all unique Hamiltonian cycles."""
        n = len(self)
        perms = permutations([i for i in range(n) if i != start])
        return [Hamiltonian((start,) + i, self) for i in perms]

    def __eq__(self, other):
        """Return true if maps are equal."""
        return [self.points, self.dist_func] == [other.points, other.dist_func]

    def __hash__(self):
        """Return hash of tuple of points when hashed."""
        return hash(tuple(self.points))


class Circuit:
    """
    Class implementing closed circuits of points in a map.

    Attributes
    ----------
    cycle : tuple
        Indices of all points in the circuit.
    map : Map
        The map which the circuit belongs to.
    journey : list
        A list of all steps taken in completing the circuit.
        List elements are 2-tuples.
    """

    def __init__(self, cycle, map):
        """
        Intitialise self with local circuit map and cycle.

        Parameters
        ----------
        cycle : tuple
            Indices of all map points to be visited in order.
        map : Map
            Map in which the circuit resides.
        """
        self.cycle = cycle
        self.map = map
        self.points = [map.points[i] for i in cycle]
        self.journey = ([(cycle[i], cycle[i+1]) for i in range(len(cycle)-1)]
                        + [(cycle[-1], cycle[0])])

    def cost(self):
        """Return the travelled distance of the circuit journey."""
        dist = self.map.dist
        return sum([dist(a, b) for a, b in self.journey])

    def __lt__(self, other):
        """Implement an ordering of Circuits."""
        return self.cost() < other.cost()

    def __len__(self):
        """Return the number of points in the circuit."""
        return len(self.cycle)

    def show2d(self):
        """Return an indexed 2D visualisation of the circuit."""
        x = np.array([i[0] for i in self.points]
                     + [self.points[0][0]])
        y = np.array([j[1] for j in self.points]
                     + [self.points[0][1]])
        plt.plot(x[0], y[0], 'r*', markersize=12)
        plt.scatter(x, y, s=50)
        plt.quiver(x[:-1], y[:-1], x[1:]-x[:-1], y[1:]-y[:-1],
                   scale_units='xy', angles='xy', scale=1, width=0.008,
                   color='green')
        plt.axis('scaled')
        plt.axis('off')
        for i, j in enumerate(self.cycle):
            plt.annotate(" " + str(j), (x[i], y[i]), fontsize=15)
        plt.show()

    def __iter__(self):
        """Return self as iterator."""
        self.num = 0
        return self

    def __next__(self):
        """Return a point index and move to next."""
        if self.num < len(self):
            dummy = self.cycle[self.num]
            self.num += 1
            return dummy

        else:
            raise StopIteration

    def __repr__(self):
        """Printable representation of a circuit."""
        return str(tuple(self.cycle))


class Hamiltonian(Circuit):
    """Circuit subclass implementing a complete tour of a map."""

    def __init__(self, cycle, map):
        """
        Verify tour is Hamiltonian then initialise self.

        Parameters
        ----------
        cycle : tuple
            Points visited in the tour in order.
        map : Map
            The map which the tour belongs to.
        """
        if set(cycle) != set([i for i in range(len(map))]):
            raise ValueError(f"{cycle} is not Hamiltonian.")

        super().__init__(cycle, map)


class Segment:
    """
    Class implementing an open segment of points in a map.

    Attributes
    ----------
    nodes : list
        List containing nodes to be visited in order.
    map : Map
        The map the segment belongs to.
    """

    def __init__(self, nodes, map):
        """
        Initialise self with nodes and map.

        Parameters
        ----------
        nodes : list
            List containing nodes to be visited in order.
        map : Map
            The map the segment belongs to.
        """
        self.nodes = nodes
        self.map = map

    def __len__(self):
        """Return the number of points in the segment."""
        return len(self.nodes)

    def cost(self):
        """Return the cost of traversing the segment."""
        return sum(self.map.dist(self.nodes[i], self.nodes[i + 1])
                   for i in range(len(self) - 1))

    def __lt__(self, other):
        """Implement an ordering of segments."""
        return self.cost() < other.cost()

    def __iter__(self):
        """Return self as iterator."""
        self.num = 0
        return self

    def __next__(self):
        """Return a node and move to next."""
        if self.num < len(self):
            dummy = self.nodes[self.num]
            self.num += 1
            return dummy

        else:
            raise StopIteration


class System:
    """
    A system containing disjoint circuits.

    As described in Julia Robinson's 'On the Hamiltonian game'.

    Attributes
    ----------
    circuits : list
        A list of the circuits present.
    map: Map
        The map the system belongs to.
    journeys : list
        A list of all steps taken in the system.
    S : numpy.ndarray
        The auxiliary matrix of the system.
    """

    def __init__(self, circuits):
        """Initialise self with circuits and auxiliary matrix.."""
        self.circuits = circuits
        self.map = circuits[0].map
        self.journeys = sum([i.journey for i in circuits], [])

        i_ = []
        n = len(self)
        for i in range(n):
            for j, k in self.journeys:
                if i == j:
                    i_.append(k)
                    break

        d = self.map.D
        s = np.array([[d[j][i_[i]] - d[i][i_[i]] for j in range(n)]
                     for i in range(n)], float)

        for i in range(n):
            s[i][i_[i]] = np.inf

        self.S = s
        self.i_ = i_

    def cost(self):
        """Return total travelled distance across all circuits."""
        return sum([i.cost() for i in self.circuits])

    def __len__(self):
        """Return number of points in the system."""
        return sum([len(i) for i in self.circuits])

    def s_length(self, circuit):
        """Return the s-length of a closed circuit."""
        return sum([self.S[a, b] for a, b in circuit.journey])

    def show2d(self):
        """Return an indexed 2D visualisation of the system."""
        for c in self.circuits:
            x = np.array([i[0] for i in c.points]
                         + [c.points[0][0]])
            y = np.array([j[1] for j in c.points]
                         + [c.points[0][1]])
            plt.plot(x[0], y[0], 'r*', markersize=12)
            plt.scatter(x, y, s=50)
            plt.quiver(x[:-1], y[:-1], x[1:]-x[:-1], y[1:]-y[:-1],
                       scale_units='xy', angles='xy', scale=1, width=0.008,
                       color='green')

            for i, j in enumerate(c.cycle):
                plt.annotate(" " + str(j), (x[i], y[i]), fontsize=15)

        plt.axis('scaled')
        plt.axis('off')
        plt.show()

    def __repr__(self):
        return str(self.circuits)
