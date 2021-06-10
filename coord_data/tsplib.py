"""
Generate maps from real world data.

Data taken from:
http://www.math.uwaterloo.ca/tsp/world/countries.html
http://comopt.ifi.uni-heidelberg.de/software/TSPLIB95/tsp/
http://www.math.uwaterloo.ca/tsp/vlsi/index.html
"""

from Req import Map


def gen_data(file, dist_func=None):
    """Read TSP data from a text file and generate a map."""
    input = open(file)
    n = int(input.readline().strip().split()[1])

    points = []

    for i in range(n):
        entry = input.readline().strip().split()
        point = (float(entry[2]), float(entry[1]))
        points.append(point)
    if dist_func is None:
        return Map(points)
    else:
        return Map(points, dist_func)


a280 = gen_data("~/M2R/M2R/coord_data/a280.txt")
djibouti = gen_data("djibouti.txt")
vlsi = gen_data("vlsi.txt")
wsahara = gen_data("wsahara.txt")
