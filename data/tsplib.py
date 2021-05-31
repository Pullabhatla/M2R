"""Data taken from http://www.math.uwaterloo.ca/tsp/world/countries.html."""

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
    if dist_func:
        return Map(points)
    else:
        return Map(points, dist_func)


djibouti = gen_data("djibouti.txt")
wsahara = gen_data("Wsahara.txt")
