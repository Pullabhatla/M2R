"""
Data from:
https://people.sc.fsu.edu/~jburkardt/datasets/cities/cities.html - a8, uk12
http://www.math.uwaterloo.ca/tsp/world/countries.html - wi29, dj38, qa194, uy734, zi929 # noqa
http://www.math.uwaterloo.ca/tsp/vlsi/index.html - xqf131, bcl380, xql662
http://comopt.ifi.uni-heidelberg.de/software/TSPLIB95/ - a279

Optimal Tours
-------------
g4 : 12
a5 : 28
a8 : 88
uk12 : 1733
p15 : 291
wi29 : 27603
dj38 : 6656
xqf131 : 564
qa194 : 9352
a279 : 2579
bcl380 : 1621
xql662 : 2513
uy734 : 79114
zi929 : 95345
"""
import pandas as pd
import numpy as np
import os
from scipy.spatial.distance import euclidean
from Req import Map


def tsp_norm(a, b):
    """Euclidean norm rounded to the nearest integer."""
    return int(round(euclidean(a, b),0))


def read_data(filename):
    """Read in CSV files from the data folder."""
    return pd.read_csv(os.path.join(
        os.path.dirname(__file__), "..", "benchmark_data", filename))


def coord_to_matrix(x, y, dist_function=None):
    """Convert coordinate data into matrix form."""
    coordlist = [(i, j) for i, j in zip(x, y)]
    dist_function = tsp_norm
    if dist_function:
        dist_function = dist_function
    n = len(x)
    adj = np.zeros([n, n])
    for i in range(n):
        adj[i][i:] = [dist_function(j, coordlist[i]) for j in coordlist[i:]]
    adj += adj.T
    return adj


def gen_data(filename, dist_func=tsp_norm):
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

a279 = read_data('a279.csv').to_numpy()
a279 = coord_to_matrix(a279[:, 0], a279[:, 1])

uy734 = gen_data('uy734.txt')

zi929 = gen_data('zi929.txt')

qa194 = gen_data('qa194.txt')

bcl380 = gen_data('bcl380.txt')

xql662 = gen_data('xql662.txt')

# manually entered numpy.ndarrays
a8 = np.array([[0, 12, 3, 23, 1, 5, 32, 56],
               [12, 0, 9, 18, 3, 41, 45, 5],
               [3, 9, 0, 89, 56, 21, 12, 49],
               [23, 18, 89, 0, 87, 46, 75, 17],
               [1, 3, 56, 87, 0, 55, 22, 86],
               [5, 41, 21, 46, 55, 0, 21, 76],
               [32, 45, 12, 75, 22, 21, 0, 11],
               [56, 5, 49, 17, 86, 76, 11, 0]])

a5 = np.array([[0, 20, 30, 10, 11],
               [15, 0, 16, 4, 2],
               [3, 5, 0, 2, 4],
               [19, 6, 18, 0, 3],
               [16, 4, 7, 16, 0]])

g4 = np.array([[0, 5, 4, 3],
              [3, 0, 8, 2],
              [5, 3, 0, 9],
              [6, 4, 3, 0]])

p15 = np.array([[0, 29, 82, 46, 68, 52, 72, 42, 51, 55, 29, 74, 23, 72, 46],
                [29,  0, 55, 46, 42, 43, 43, 23, 23, 31, 41, 51, 11, 52, 21],
                [82, 55,  0, 68, 46, 55, 23, 43, 41, 29, 79, 21, 64, 31, 51],
                [46, 46, 68,  0, 82, 15, 72, 31, 62, 42, 21, 51, 51, 43, 64],
                [68, 42, 46, 82,  0, 74, 23, 52, 21, 46, 82, 58, 46, 65, 23],
                [52, 43, 55, 15, 74,  0, 61, 23, 55, 31, 33, 37, 51, 29, 59],
                [72, 43, 23, 72, 23, 61,  0, 42, 23, 31, 77, 37, 51, 46, 33],
                [42, 23, 43, 31, 52, 23, 42,  0, 33, 15, 37, 33, 33, 31, 37],
                [51, 23, 41, 62, 21, 55, 23, 33,  0, 29, 62, 46, 29, 51, 11],
                [55, 31, 29, 42, 46, 31, 31, 15, 29,  0, 51, 21, 41, 23, 37],
                [29, 41, 79, 21, 82, 33, 77, 37, 62, 51,  0, 65, 42, 59, 61],
                [74, 51, 21, 51, 58, 37, 37, 33, 46, 21, 65,  0, 61, 11, 55],
                [23, 11, 64, 51, 46, 51, 51, 33, 29, 41, 42, 61,  0, 62, 23],
                [72, 52, 31, 43, 65, 29, 46, 31, 51, 23, 59, 11, 62,  0, 59],
                [46, 21, 51, 64, 23, 59, 33, 37, 11, 37, 61, 55, 23, 59,  0]])

mat_list = [g4, a5, a8, uk12, p15, wi29, dj38, xqf131, qa194, a279,
            bcl380, xql662, uy734, zi929]

opt_tour_lengths = [12, 28, 88, 1733, 291, 27603, 6656, 564, 9352, 2579,
                    1621, 2513, 79114, 95345]
