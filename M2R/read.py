"""Extra."""
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import numpy.random as nrnd


def read_in_csv(filepath):
    """
    Return data frame, data frame shape the column titles and data types.

    filepath - can be url
    """
    import pandas as pd
    df = pd.read_csv(f"{filepath}")
    return df, df.shape, df.dtypes


class Graph:
    """
    class to store and create graph with cities and distances.

    -----
    parameters:
    links - list of tuples of length 2 to show
    intercity connections which cities are connected
    distances - distance from each city
    nc - number of cities default none
    """

    def __init__(self, links, distances, nc=None):
        """Initialize graph."""
        self.links = links
        self.distance = distances
        dict1 = dict()
        for j in range(len(links)):
            dict1[f'{links[j]}'] = distances[j]
        self.edgelabels = dict1
        if not nc:
            set_nodes = set([i for j in range(len(links)) for i in links[j]])
            self.v = len(set_nodes)
        else:
            self.v = nc
        G = nx.MultiDiGraph()
        self.weighted_edge_list = [i + (j,)
                                   for i, j in zip(self.links, self.distance)]
        G.add_weighted_edges_from(self.weighted_edge_list)
        self.G = G
        self.pos = nx.spring_layout(self.G)

    def draw(self, edge_weights=False, directed=True, multi_edges=False):
        """Draw the graph."""
        if multi_edges:
            nx.draw(self.G, self.pos, arrows=True, with_labels=True,
                    connectionstyle='arc3, rad = 0.2')
            if edge_weights:
                nx.draw_networkx_edge_labels(self.G, self.pos)
                plt.show()
        else:
            if edge_weights:
                nx.draw_networkx_edge_labels(self.G, self.pos)
            nx.draw(self.G, self.pos, arrows=directed, with_labels=True)
            plt.show()

    def nodes(self):
        """List od nodes."""
        return self.G.nodes

    def number_nodes(self):
        """No of nodes."""
        return self.v

    def edges(self):
        """All the edges."""
        return self.links

    def distances(self):
        """Intercity distances."""
        return self.distance

    def weighted_edges(self):
        """Edges and their corresponding weights."""
        return self.weighted_edge_list

    def edge_dictionary(self):
        """Edges and distances as a dictiionary."""
        return self.edgelabels

    def adjacency(self):
        """Cost adjacency matrix of the graph."""
        A = np.zeros([self.v, self.v])
        for u, d in zip(self.links, self.distance):
            A[u[0]-1, u[1]-1] = d
        return A


class GraphMatrix:
    """
    Class to convert cost adjacency matrix.

    into Graph will all its features.
    """

    def __init__(self, A):
        """Convert into a Graph object."""
        self.A = A
        n = len(A)
        self.link_list = []
        self.dist_list = []
        [(self.link_list.append((i+1, j+1)), self.dist_list.append(A[i, j]))
         for i in range(n) for j in range(n) if A[i, j]]
        self.G = Graph(self.link_list, self.dist_list)

    def graph(self):
        """Return Graph object."""
        return self.G


class RandomGraph:

    def __init__(self, max_dist=100, number_of_cities=6):
        """
        Generate a random graph object.

        accessed by attribute graph.
        """
        A = nrnd.randint(1, max_dist, [number_of_cities, number_of_cities])
        b = np.array(np.diag(A))
        M = A - np.diag(b)
        self.matrix = M
        self.graph = GraphMatrix(M)  # generates a random graph object
