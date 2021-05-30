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
    points: list
        A list of n-tuple Cartesian coordinates of the points on the map.
    D: numpy.ndarray
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
        """Return an indexed 2D visual representation of the map."""
        x = [i[0] for i in self.points]
        y = [j[1] for j in self.points]
        plt.scatter(x, y, s=50)
        plt.axis('scaled')
        plt.axis('off')
        for i in range(len(self.points)):
            plt.annotate(i, (x[i], y[i]))
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


class Circuit:
    """
    Class implementing closed circuits of points in a map.

    Attributes
    ----------
    cycle : tuple
        Indices of all points in the circuit.
    globalmap : Map
        The map which the circuit belongs to.
    localmap : Map
        A miniature map containing all points of the circuit.
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
        """Return an indexed 2D visual representation of the circuit."""
        x = np.array([i[0] for i in self.points]
                     + [self.points[0][0]])
        y = np.array([j[1] for j in self.points]
                     + [self.points[0][1]])
        plt.plot(x[0], y[0], 'r*', markersize=12)
        plt.scatter(x, y, s=50)
        plt.quiver(x[:-1], y[:-1], x[1:]-x[:-1], y[1:]-y[:-1],
                   scale_units='xy', angles='xy', scale=1, width=0.01,
                   color='g')
        plt.axis('scaled')
        plt.axis('off')
        for i, j in enumerate(self.cycle):
            plt.annotate(j, (x[i], y[i]), fontsize=15)
        plt.show()

    def __iter__(self):
        """Return self on iterating."""
        self.num = 0
        return self

    def __next__(self):
        """Return a point and move to next."""
        if self.num < len(self):
            dummy = self.cycle[self.num]
            self.num += 1
            return dummy

        else:
            raise StopIteration


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
