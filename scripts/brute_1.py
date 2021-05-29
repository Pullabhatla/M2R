"""Solutions to an 7-node TSP across different distance functions."""

from scipy.spatial.distance import cityblock, chebyshev, canberra
from Req import Map, minimal_tour

points = [(0.5296956846985459, 0.8222832124398117),
          (0.3217612255807988, 0.4094554653671926),
          (0.7732969211715641, 0.26606592909472326),
          (0.8110924658585621, 0.026623706692775473),
          (0.039717188300034456, 0.38733952685578654),
          (0.975297275309528, 0.3399336100561293),
          (0.6392518139961628, 0.7589843132455842)]

map1 = Map(points, cityblock)
map2 = Map(points, canberra)
map3 = Map(points, chebyshev)
map4 = Map(points)

print("Taxicab Distance (L1 metric):")
minimal_tour(map1).show2d()

print("Canberra Distance (Weighted L1 metric):")
minimal_tour(map2).show2d()

print("Chebyshev Distance (L-infty metric):")
minimal_tour(map3).show2d()

print("Euclidean Distance (L2 metric):")
minimal_tour(map4).show2d()
