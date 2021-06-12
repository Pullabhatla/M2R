"""
Read data.

Optimal Tours
-------------
uk12 : 1733
wi29 : 27603
dj38 : 6656
kn57 : 
sgb128 :
xqf131 : 564
a280 : 2579
uy734 : 79114
zi929 : 95345
"""
import pandas as pd
import numpy as np
from scipy.spatial.distance import euclidean


def read_data(filename):
    """Read in CSV files from the data folder."""
    return pd.read_csv(filename)


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
dj38 = read_data('dj38.csv')
wi29 = read_data('wi29.csv')
xqf131 = read_data('xqf131.csv')
a280 = read_data('a280.csv')
# can add more csv files in like this

dj_38 = dj38.to_numpy()
wi_29 = wi29.to_numpy()
xqf_131 = xqf131.to_numpy()
a_280 = a280.to_numpy()
# need to input x and y coord the right way
# djabouti data file is arrange yx
djibouti_adjacencymatrix = coord_to_matrix(dj_38[:, 1], dj_38[:, 0])
# wsahara data dile is arranged yx
ws_adjacencymatrix = coord_to_matrix(wi_29[:, 1], wi_29[:, 0])
# vlsi data dile is arranged yx
vlsi_adjacencymatrix = coord_to_matrix(xqf_131[:, 1], xqf_131[:, 0])
# a280 data dile is arranged yx
a280_adjacencymatrix = coord_to_matrix(a_280[:, 1], a_280[:, 0])
