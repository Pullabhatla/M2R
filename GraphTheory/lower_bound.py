"""Lower bound using minimal spanning tree and removal of nodes."""
from GraphTheory.read import Graph, GraphMatrix
import numpy as np


def lower_bound(matrix):
    """Lower bound."""
    # assume symmetric matrix
    n = len(matrix)
    matrix_copy = [matrix.copy() for i in range(n)]
    zero = np.zeros(n)
    list_of_paths = []
    list_of_distances = []
    list_of_total_distance = []
    for i in range(n):
        matrix = matrix_copy[i]
        row_i = matrix[i, :]
        index_row_i = sorted([(val1, m)
                              for m, val1 in enumerate(row_i) if val1])
        min_2_edges = [k[1]+1 for k in index_row_i[0:2]]
        edges_add_back = [(i+1, v) for v in min_2_edges]
        weights_add_back = [matrix[e[0]-1, e[1]-1] for e in edges_add_back]
        matrix[:, i] = zero
        matrix[i, :] = zero
        graph1 = GraphMatrix(matrix, directed=False).G
        graph = graph1.spanning_tree()
        graph = graph.add_edge(edges_add_back[0], weights_add_back[0])
        graph = graph.add_edge(edges_add_back[1], weights_add_back[1])
        list_of_paths.append(graph.links)
        list_of_distances.append(graph.distance)
        list_of_total_distance.append(sum(graph.distance))
    neg_dist = list(np.array(list_of_total_distance)*-1)
    max_dist = min(neg_dist)
    index_max = neg_dist.index(max_dist)
    return (Graph(list_of_paths[index_max], list_of_distances[index_max]),
            -1*max_dist)
