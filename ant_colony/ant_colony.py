"""Implementation of Ant colony optimization for TSP."""

import numpy as np
from Req import Map
import matplotlib.pyplot as plt
import matplotlib
import math
import random

def Ant_colony(map, alpha, beta, m, rho, Q, its_max):
    pointsList = map.points
    n = len(pointsList)
    P = np.zeros(n, n)
    Tau = np.ones(n, n)
    Eta = 1/map.D
    PathsList = np.zeros(m, n)
    its = 0
    pathLength = np.zeros(m)
    path_best = np.zeros((its_max, n))
    distance_best = np.zeros(its_max)

    while its < its_max:
        for i in range(m):
            sourceNode = pointsList[np.random.randint(0,n)]
            has_visited = [sourceNode]
            nodeNow = sourceNode
            unvisit = [i for i in range(n)]
            PathsList[i, 0] = nodeNow
            for j in range(1, n):

                unvisit = [i for i in range(n)]
                unvisit.remove(has_visited)
                for k in range(len(unvisit)):
                    ProbList[k] = Tau[nodeNow][k]**alpha*Eta[nodeNow][k]**beta
                for h in has_visited:
                    ProbList[h] = 0
                cumsumProbList = (ProbList/sum(ProbList)).cumsum()
                cumsumProbList -= np.rand()
                nodeNext = ProbList[list(cumsumProbList > 0).index(True)]
                PathsList[i, j] = nodeNext
                has_visited.append(nodeNext)
                pathLength += map.D[nodeNow, nodeNext]
                nodeNow = nodeNext
            pathLength += map.D[nodeNow, sourceNode]

        if its == 0:
            distance_best[its] = pathLength.min()
            path_best[its] = PathsList[pathLength.argmin()].copy()
        else:
            if pathLength.min() > distance_best[its - 1]
            path_best[its] = PathsList[pathLength.argmin()].copy()



        changeTau = np.zeros((n, n))
        for i in range(m):
            for j in range(n - 1):
                changeTau[PathsList[i, j]][PathsList[i, j + 1]] += Q/pathLength[i]
            changeTau[PathsList[i, j + 1]][PathsList[i, 0]] += Q/pathLength[i]

        Tau = (1- rho) * Tau + changeTau
        its += 1


return [path_best + 1, distance_best]