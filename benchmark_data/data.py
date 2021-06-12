"""
Read data.

Optimal Tours
-------------
uk12 : 1733
wi29 : 27603
dj38 : 6656
xqf131 : 564
qa194 : 9352
a280 : 2579
uy734 : 79114
zi929 : 95345
"""
import pandas as pd
import numpy as np
import os
from scipy.spatial.distance import euclidean
from Req import Map


def read_data(filename):
    """Read in CSV files from the data folder."""
    return pd.read_csv(os.path.join(
        os.path.dirname(__file__), "..", "benchmark_data", filename))


def coord_to_matrix(x, y, dist_function=None):
    """Convert coordinate data into matricx form."""
    coordlist = [(i, j) for i, j in zip(x, y)]
    dist_function = euclidean
    if dist_function:
        dist_function = dist_function
    n = len(x)
    adj = np.zeros([n, n])
    for i in range(n):
        adj[i][i:] = [dist_function(j, coordlist[i]) for j in coordlist[i:]]
    adj += adj.T
    return adj


def gen_data(filename, dist_func=None):
    """Read TSP data from a text file and generate an adjacency matrix."""
    input = open(os.path.join(
        os.path.dirname(__file__), "..", "benchmark_data", filename))
    n = int(input.readline().strip().split()[1])

    points = []

    for i in range(n):
        entry = input.readline().strip().split()
        point = (float(entry[2]), float(entry[1]))
        points.append(point)
    if dist_func is None:
        return Map(points).D
    else:
        return Map(points, dist_func).D


# matrix data to adj:
uk12 = read_data('uk12_dist.csv').to_numpy()

# coord data to adj:
dj38 = read_data('dj38.csv').to_numpy()
dj38 = coord_to_matrix(dj38[:, 0], dj38[:, 1])

wi29 = read_data('wi29.csv').to_numpy()
wi29 = coord_to_matrix(wi29[:, 0], wi29[:, 1])

xqf131 = read_data('xqf131.csv').to_numpy()
xqf131 = coord_to_matrix(xqf131[:, 0], xqf131[:, 1])

a280 = read_data('a280.csv').to_numpy()
a280 = coord_to_matrix(a280[:, 0], a280[:, 1])

uy734 = gen_data('uy734.txt')

zi929 = gen_data('zi929.txt')

qa194 = gen_data('qa194.txt')
