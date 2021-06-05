"""Christofides algorithm."""
from GraphTheory.read import Graph, GraphMatrix
from GraphTheory.mst import MST
import numpy as np


def christofides(matrix, over_ride=False, name='graph'):
    """Christofides algorithm."""
    # check if matrix is symmetric.
    # can override if you  know he matrix is almost symmetric.
    if not isinstance(matrix, np.ndarray):
        raise TypeError(f'Expected an array got {type(matrix).__name__}')
    if not over_ride:
        if not np.allclose(matrix, matrix.T):
            print('Matrix input is not symmetric.')
        else:
            print('Matrix input is symmetric.')
    # since matrix is symmetric
    matrix = np.triu(matrix)
    # convert matrix into a Graph object
    GM = GraphMatrix(matrix, directed=False)  # noqa N806
    GM_G = GM.G  # noqa N806
    # minimum spanning tree
    min_span_info = MST(GM.G).kruskal()
    min_span_tree = Graph(min_span_info[1], min_span_info[2], directed=False)
    # draw min span tree
    print(f'Minimum spanning tree for {name}.')
    min_span_tree.draw(directed=False, pos=GM_G.pos)
    # check if connected
    print(f'Minimum spanning tree is connected = {min_span_tree.connected()}')
    # get the odd degreee nodes
    odd_nodes = min_span_tree.odd_nodes()
    # subgraph of the main graph GM_G with the odd nodes
    sub_graph = GM_G.sub_graph(odd_nodes)
    # check subgraph connected
    print(f'Subgraph is connected = {sub_graph.connected()}')
    # finding the minimum weight perfect matching of the subgraph
    minG = sub_graph.min_matching()  # noqa N806
    # find the union of the minimum weight matching and the spanning tree
    union_graph = minG.union(min_span_tree)
    # find the eulerian tour
    euler_graph = union_graph.eulerian_tour()
    print(f'eulerian tour of the union of the minimum'
          f' weight matching and the spanning tree for {name}.')
    euler_graph.draw()
    # shortcut of the eulerian tour
    short = euler_graph.shortcut()
    weights = [GM_G.G.get_edge_data(*i)['weight'] for i in short]
    solution = Graph(short, weights)
    print(f'Solution of TSP for {name}.')
    solution.draw()
    return print(
        f'links: {solution.links}\n'
        f'distances: {solution.distance}\n'
        f'total distance={sum(weights)}'
            )
