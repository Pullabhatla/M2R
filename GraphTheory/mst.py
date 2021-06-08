"""
Kruskal and prims min span tree.

good for undirected.
prims is from  - "https://www.programiz.com/dsa/prim-algorithm"
"""
import numpy as np
from GraphTheory.read import Graph


class MST:
    """Kruskal and prims algorithm."""

    def __init__(self, graph):
        """Take Graph object from read.py."""
        self.graph = graph
        self.distances = graph.distance
        self.links = graph.links
        self.weighted_edge_list = graph.weighted_edge_list
        self.G = graph.G
        self.sort = sorted(self.weighted_edge_list, key=lambda x: x[2])
        self.ordered_distance = [i[2] for i in self.sort]
        self.ordered_links = [i[0:2] for i in self.sort]
        self.nodes = graph.nodes()
        self.number_nodes = graph.number_nodes()
        self.matrix = graph.adjacency()

    def kruskal(self):
        """Find minimum spanning tree using kruskals algorithm."""
        val = True
        travelled_distance = self.ordered_distance[0]
        travelled_distance_list = [self.ordered_distance[0]]
        travelled_edges = [self.ordered_links[0]]
        travelled_nodes = [self.ordered_links[0][0], self.ordered_links[0][1]]
        for i, j in zip(self.ordered_links[1:], self.ordered_distance[1:]):
            G = (Graph(travelled_edges, travelled_distance_list,  # noqa N806
                       directed=False))
            if len(set(i).intersection(set(travelled_nodes))) < 2 and val:
                travelled_nodes.append(i[0])
                travelled_nodes.append(i[1])
                travelled_edges.append(i)
                travelled_distance_list.append(j)
                travelled_distance += j
            if (not any(val,
                        i in travelled_edges,
                        tuple(reversed(i)) in travelled_edges,
                        G.add_edge(i, j).cyclic())):
                travelled_nodes.append(i[0])
                travelled_nodes.append(i[1])
                travelled_edges.append(i)
                travelled_distance_list.append(j)
                travelled_distance += j
            if len(set(travelled_nodes)) == self.number_nodes:
                val = False

            if (G.connected() and
                    len(set(travelled_nodes)) == self.number_nodes):
                return (set(travelled_nodes), travelled_edges,
                        travelled_distance_list, travelled_distance)

    def prims(self, start_node, matrix=None):
        """Prims algorithm."""
        if isinstance(matrix, np.ndarray):
            self.matrix = matrix
        selected = [0]*self.number_nodes
        set_visited_nodes = {start_node}
        visited_edges = []
        weights = []

        selected[start_node] = True
        while (len(set_visited_nodes) < self.number_nodes):
            m = 10000000
            x = 0
            y = 0
            for i in range(self.number_nodes):
                if selected[i]:
                    for j in range(self.number_nodes):
                        if ((not selected[j]) and self.matrix[i][j]):
                            if m > self.matrix[i][j]:
                                m = self.matrix[i][j]
                                x = i
                                y = j
            set_visited_nodes.add(x+1)
            set_visited_nodes.add(y+1)
            visited_edges.append(tuple([x+1, y+1]))
            weights.append((self.matrix[x][y]))
            selected[y] = True

        return [set_visited_nodes, visited_edges, weights]
