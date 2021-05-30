import numpy as np


class Kruskal:
    """Kruskal algorithm."""

    def __init__(self, graph):
        """Take Graph object from read.py."""
        self.graph = graph
        self.distances = graph.distance
        self.links = graph.links
        self.ordered_distance = sorted(graph.distance)
        permutation = np.array([self.distances.index(a)
                                for a in self.ordered_distance])
        self.ordered_links = [self.links[i] for i in permutation]
