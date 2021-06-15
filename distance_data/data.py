"""Read data."""
import pandas as pd
import os
import numpy as np
from scipy.spatial.distance import euclidean
"""
http://www.math.uwaterloo.ca/tsp/world/countries.html
https://people.sc.fsu.edu/~jburkardt/datasets/cities/cities.html
"""


def read_data(filename):
    """Read in CSV files from the data folder."""
    return pd.read_csv(os.path.join(
        os.path.dirname(__file__), "..", "distance_data", filename))


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


grid04 = read_data('grid04_dist.csv')
ha30 = read_data('ha30_dist.csv')
kn57 = read_data('kn57_dist.csv')
uk12 = read_data('uk12_dist.csv')
wg22 = read_data('wg22_dist.csv')
sgb128 = read_data('sgb128_dist.csv')
wg59 = read_data('wg59_dist_NEW.csv')


djibouti = read_data('djibouti.csv')
usa = read_data('usa.csv')
wsahara = read_data('wsahara.csv')
# can add more csv files in like this

# heavy ones :)
egypt_coord = read_data('eg7146.csv')
finland_coord = read_data('fi10639.csv')
honduras_coord = read_data('ho14473.csv')
burma_coord = read_data('bm33708.csv')
oman_coord = read_data('mu1979.csv')
nicaragua_coord = read_data('nu3496.csv')

e_array = egypt_coord.to_numpy()
f_array = finland_coord.to_numpy()
h_array = honduras_coord.to_numpy()
# b_array = burma_coord.to_numpy()  # too many nodes
o_array = oman_coord.to_numpy()
n_array = nicaragua_coord.to_numpy()

d_array = djibouti.to_numpy()
u_array = usa.to_numpy()
ws_array = wsahara.to_numpy()
# need to input x and y coord the right way
# djabouti data file is arrange yx
djibouti_adjacencymatrix = coord_to_matrix(d_array[:, 1], d_array[:, 0])
# usa data file is arranged xy
usa_adjacencymatrix = coord_to_matrix(u_array[:, 0], u_array[:, 1])
# wsahara data dile is arranged yx
ws_adjacencymatrix = coord_to_matrix(ws_array[:, 1], ws_array[:, 0])
