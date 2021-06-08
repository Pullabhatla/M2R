"""Christofides algorithm."""
from GraphTheory.read import Graph, GraphMatrix
from GraphTheory.mst import MST
import numpy as np


def christofides1(matrix, over_ride=False, name='graph', own_kruskals=False):
    """Christofides algorithm."""
    if not isinstance(matrix, np.ndarray):
        raise TypeError(f'Expected an array got {type(matrix).__name__}')
    if not over_ride:
        if not np.allclose(matrix, matrix.T):
            print('Matrix input is not symmetric.')
        else:
            print('Matrix input is symmetric.')
    matrix_copy = matrix.copy()
    matrix = np.triu(matrix)
    GM = GraphMatrix(matrix, directed=False)  # noqa N806
    GM_G = GM.G  # noqa N806
    if own_kruskals:
        min_span_info = MST(GM.G).kruskal()
        min_span_tree = Graph(min_span_info[1], min_span_info[2],
                              directed=False)
    else:
        min_span_tree = GM.G.spanning_tree()
    odd_nodes = min_span_tree.odd_nodes()
    sub_graph = GM_G.sub_graph(odd_nodes)
    minG = sub_graph.min_matching()  # noqa N806
    union_graph = minG.union(min_span_tree)
    euler_graph = union_graph.eulerian_tour()
    short = euler_graph.shortcut()
    weights = [matrix_copy[i[0]-1][i[1]-1] for i in short]
    solution = Graph(short, weights)
    return print(
        f'links: {solution.links}\n'
        f'distances: {solution.distance}\n'
        f'total distance={sum(weights)}'
            )
