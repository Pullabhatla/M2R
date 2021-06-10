"""Read data."""
import pandas as pd
import os
import numpy as np
from scipy.spatial.distance import euclidean


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

# adj matrix:
kn57 = read_data('kn57_dist.csv')
uk12 = read_data('uk12_dist.csv')
sgb128 = read_data('sgb128_dist.csv')
# the numpy array version
kn_57 = kn57.to_numpy()
uk_12 = uk12.to_numpy()
sgb_128 = sgb128.to_numpy()
# coord data:
djibouti = read_data('djibouti.csv')
wsahara = read_data('wsahara.csv')
vlsi = read_data('vlsi.csv')
a280 = read_data('a280.csv')
# can add more csv files in like this

d_array = djibouti.to_numpy()
ws_array = wsahara.to_numpy()
vlsi_array = vlsi.to_numpy()
a280_array = a280.to_numpy()
# need to input x and y coord the right way
# djabouti data file is arrange yx
djibouti_adjacencymatrix = coord_to_matrix(d_array[:, 1], d_array[:, 0])
# wsahara data dile is arranged yx
ws_adjacencymatrix = coord_to_matrix(ws_array[:, 1], ws_array[:, 0])
# vlsi data dile is arranged yx
vlsi_adjacencymatrix = coord_to_matrix(vlsi_array[:, 1], vlsi_array[:, 0])
# a280 data dile is arranged yx
a280_adjacencymatrix = coord_to_matrix(a280_array[:, 1], a280_array[:, 0])
