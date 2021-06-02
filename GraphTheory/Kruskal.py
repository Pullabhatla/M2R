"""Kruskal min span tree."""


class Kruskal:
    """Kruskal algorithm."""

    def __init__(self, graph):
        """Take Graph object from read.py."""
        self.graph = graph
        self.distances = graph.distance
        self.links = graph.links
        self.weighted_edge_list = graph.weighted_edge_list
        self.G = graph.G
        self.sort = sorted(self.weighted_edge_list, key=lambda x: x[2])
        self.ordered_distance = sorted(graph.distance)
        self.ordered_links = [i[0:2] for i in self.sort]
        self.nodes = graph.nodes()

    def kruskal(self):
        """Find minimum spannig tree using kruskals algorithm."""
        travelled_edges = [self.ordered_links[0]]
        travelled_nodes = [self.ordered_links[0][0], self.ordered_links[0][1]]
        for i, j in zip(self.ordered_links[1:], self.ordered_distance[1:]):
            if not (i[0] and i[1] in travelled_nodes):
                travelled_nodes.append(i[0])
                travelled_nodes.append(i[1])
                travelled_edges.append(i)
                if sorted(set(travelled_nodes)) == set(self.nodes):
                    break
        return set(travelled_nodes), travelled_edges
