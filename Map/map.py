"""Required objects for the TSP and related problems."""

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
        self.D = np.array([[self.dist(a, b, dist_func) for b in points]
                           for a in points])

    def dist(self, origin, destination, dist_func):
        """
        Return the distance between two nodes.

        Parameters
        ----------
        origin : tuple
            Cartesian coordinates of origin point.
        dest : tuple
            Cartesian coordinates of destination point.
        dist_func : function
            Function computing the distance between two points.

        Returns
        -------
        int or float
            Distance between the origin and destination points.
        """
        return dist_func(origin, destination)

    def __len__(self):
        """Return the number of points on the map."""
        return len(self.points)

    def show2d(self):
        """Return an indexed 2D visual representation of the map."""
        x = [i[0] for i in self.points]
        y = [j[1] for j in self.points]
        plt.scatter(x, y)
        plt.axis('off')
        for i in range(len(self.points)):
            plt.annotate(i, (x[i], y[i]))
        plt.show()
