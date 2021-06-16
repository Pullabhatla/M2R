"""Extra."""
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import numpy.random as nrnd
from networkx.algorithms import tree


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

    def __init__(self, links, distances, directed=True, undirected_multi=False,
                 nc=None, pos=None):
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
        G = nx.MultiDiGraph()  # noqa N806
        self.val = True
        if not directed:
            G = nx.Graph()  # noqa N806
            self.val = False
        if undirected_multi:
            G = nx.MultiGraph()  # noqa N806
            self.val = True
        self.weighted_edge_list = [i + (j,)
                                   for i, j in zip(self.links, self.distance)]
        G.add_weighted_edges_from(self.weighted_edge_list)
        self.G = G
        self.pos = nx.spring_layout(self.G)
        if pos:
            self.pos = pos

    def draw(self, edge_weights=False, directed=True, multi_edges=False,
             pos=None):
        """Draw the graph."""
        if pos:
            self.pos = pos
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

    def adjacency(self, undirected=False):
        """Cost adjacency matrix of the graph."""
        A = np.zeros([self.v, self.v])  # noqa N806
        for u, d in zip(self.links, self.distance):
            A[u[0]-1, u[1]-1] = d
        if undirected:
            A = A + A.T  # noqa N806
        return A

    def neighbors(self, c):
        """Find neghbor cities of c."""
        return list(self.G.neighbors(c))

    def distance_neighbors(self, c):
        """Distance of neighbors of city c."""
        return[self.edgelabels[f'({c}, {i})'] for i in self.neighbors(c)]

    def radius(self, c, r):
        """Find cities at most a distance r from city c."""
        neighbors = self.neighbors(c)
        return [i for i in neighbors if self.edgelabels[f'({c}, {i})'] <= r]

    def speration(self, r):
        """List of nodes seperated by distance of atmost r."""
        truth_array = (np.array(self.distance) <= r)
        nodes = np.array(self.links)[truth_array]
        return list(nodes)

    def connected(self):
        """
        Determine graph is connected only.

        works when undirected(directed=False).
        """
        return nx.is_connected(self.G)

    def cyclic(self):
        """
        Test if graph is cyclic.

        only used on undirected graph.
        """
        return bool(len(nx.cycle_basis(self.G)))

    def add_edge(self, edge, weight):
        """Adding in an extra edge."""
        return Graph(self.links+[edge],
                     self.distance+[weight], directed=False)

    def spanning_tree(self):
        """Find the minimumspanning tree."""
        mst = tree.minimum_spanning_edges(self.G, algorithm="kruskal")
        edgelist = list(mst)
        links = [i[0:2] for i in edgelist]
        weights = [i[2]['weight'] for i in edgelist]
        return Graph(links, weights, directed=False)

    def degrees(self):
        """Return degree of each node."""
        return self.G.degree([i for i in range(1, self.v + 1)])

    def odd_nodes(self):
        """List of odd degree nodes."""
        v = dict(self.degrees()).items()
        return [i for i, d in v if d % 2 == 1]

    def sub_graph(self, nodes):
        """Graph object subgraph of given set of nodes."""
        H = self.G.subgraph(nodes)  # noqa N806
        if self.val:
            weights = [self.G.get_edge_data(*i)[0]['weight']
                       for i in H.edges()]
        else:
            weights = [self.G.get_edge_data(*i)['weight']
                       for i in H.edges()]
        return Graph(list(H.edges()), weights, directed=False, pos=self.pos)

    def min_matching(self):
        """Min_matching graph."""
        u1 = self.links
        w1 = self.distance
        neg_w1 = list(np.array(w1)*(-1))
        new_graph = Graph(u1, neg_w1, directed=False)
        set_matching = nx.max_weight_matching(new_graph.G, maxcardinality=True)
        if new_graph.val:
            weights = [-1 * new_graph.G.get_edge_data(*i)[0]['weight']
                       for i in set_matching]
        else:
            weights = [-1 * new_graph.G.get_edge_data(*i)['weight']
                       for i in set_matching]
        return Graph(list(set_matching), weights, directed=False)

    def union(self, other):
        """Union of 2 graphs that keeps repeat edges."""
        if not isinstance(other, Graph):
            raise TypeError
        total_link_list = self.links + other.links
        total_distance = self.distance + other.distance
        return Graph(total_link_list, total_distance, undirected_multi=True)

    def eulerian_tour(self):
        """Find eulerian tour of a graph."""
        graph = self.G
        edges_eulerian_tour = list(nx.eulerian_circuit(graph))
        if self.val:
            weights = [self.G.get_edge_data(*i)[0]['weight']
                       for i in edges_eulerian_tour]
        else:
            weights = [self.G.get_edge_data(*i)['weight']
                       for i in edges_eulerian_tour]
        return Graph(edges_eulerian_tour, weights)

    def shortcut(self):
        """Short cut the graph."""
        tour = [i[0] for i in self.links]
        visited_vertices = []
        for vertex in tour:
            if not(vertex in visited_vertices):
                visited_vertices.append(vertex)
        visited_vertices.append(tour[0])
        return [(i, j)
                for i, j in zip(visited_vertices[:-1], visited_vertices[1:])]


class GraphMatrix:
    """
    Class to convert cost adjacency matrix.

    into Graph will all its features.
    """

    def __init__(self, A, directed=True, undirected_multi=False):  # noqa N806
        """Convert into a Graph object."""
        self.A = A
        n = len(A)
        self.link_list = []
        self.dist_list = []
        [(self.link_list.append((i+1, j+1)), self.dist_list.append(A[i, j]))
         for i in range(n) for j in range(n) if A[i, j]]
        self.G = Graph(self.link_list, self.dist_list,
                       directed=directed, undirected_multi=undirected_multi)

    def graph(self):
        """Return Graph object."""
        return self.G


class RandomGraph:
    """Random graph generator."""

    def __init__(self, max_dist=100, number_of_cities=6):
        """
        Generate a random graph object.

        accessed by attribute graph.
        """
        A = nrnd.randint(1, max_dist, [number_of_cities, number_of_cities])  # noqa N806
        b = np.array(np.diag(A))
        M = A - np.diag(b)  # noqa N806
        self.matrix = M
        self.graph = GraphMatrix(M)  # generates a random graph object


class SymmetricRandomGraph:
    """Symmetric graph generator."""

    def __init__(self, max_dist=100, number_of_cities=6):
        """
        Generate a random graph object.

        accessed by attribute graph.
        """
        A = nrnd.randint(1, max_dist, [number_of_cities, number_of_cities])   # noqa N806
        S = A + A.transpose()  # noqa N806
        b = np.array(np.diag(S))
        M = S - np.diag(b)  # noqa N806
        self.matrix = M
        self.graph = GraphMatrix(M)  # generates a random graph object
