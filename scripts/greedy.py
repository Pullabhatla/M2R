"""Failure of the greedy near neighbour algorithm with outliers."""

from Req import Map, brute_tour, nearest_neighbour, best_nn
import matplotlib.pyplot as plt

points = [(1, 1), (1, 2), (1, 3), (2, 1), (2, 3),
          (3, 1), (3, 2), (3, 3), (6, 6), (-4, 1)]

map = Map(points)
plt.title("Map")
map.show2d()

tour1 = nearest_neighbour(map)
tour2 = best_nn(map)
tour3 = brute_tour(map)

plt.title(f"Near Neighbour\nd = {tour1.cost()}")
tour1.show2d()

plt.title(f"Best Near Neighbour\nd = {tour2.cost()}")
tour2.show2d()

plt.title(f"Optimal Solution\nd = {tour3.cost()}")
tour3.show2d()
