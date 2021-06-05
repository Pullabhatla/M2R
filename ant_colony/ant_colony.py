"""Implementation of Ant colony optimization for TSP."""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import math
import random
from Req import Map


def Ant_colony(map, alpha, beta, m, rho, Q, its_max):
    """set up fpr parameters
    n: number of cities
    Tau： matrix of pheromone
    Eta： heuristic function， should be 1/distance
    Pathlist: matrix of the routes by every ant
    Pathlength: distance ant moved
    path_best: shortest path
    distance_best: shortest distance
    alpha: how likely ant choose their way depend on pheromone
    beta: dependence of path distance on ants' route
    m: ants number
    rho: vaporation of pheromone
    q: pheromone ants takes
    """
    n = len(map.points)  
    pointsList = [o for o in range(n)]
    Tau = np.ones((n,n))
    Eta = 1/map.D
    for i in range(n):
        Eta[i, i] = 0
    pathsList = np.zeros((m, n))
    its = 0
    path_best = np.zeros((its_max, n))
    distance_best = np.zeros(its_max)
    
    while its < its_max:
        pathsLength = np.zeros(m)
        for i in range(m):
            sourceNode = np.random.randint(n)
            visited = []
            unvisited = list(range(n))
            nodeNow = sourceNode
            nodeNext = -1
            pathsList[i, 0] = sourceNode
            
            for j in range(1, n):
                visited.append(nodeNow)
                unvisited.remove(nodeNow)
                probRoulette = [0]*n
                for k in unvisited:
                    probRoulette[k] = pow(Tau[nodeNow, k], alpha)*pow(Eta[nodeNow, k], beta)
                probRoulette = probRoulette/sum(probRoulette)
                cumRoulette = probRoulette.cumsum()
                cumRoulette -= np.random.uniform(0,1)
                nodeNext = list(cumRoulette > 0).index(True)
                pathsList[i, j] = nodeNext
                pathsLength[i] += map.D[nodeNow, nodeNext]
                nodeNow = nodeNext
            pathsLength[i] += map.D[nodeNow, sourceNode]
            
        if its == 0:
            distance_best[its] = pathsLength.min()
            path_best[its] = pathsList[pathsLength.argmin()].copy()
        else:
            if distance_best[its-1] < pathsLength.min():
                distance_best[its] = distance_best[its-1]
                path_best[its] = path_best[its-1].copy()
            else:
                distance_best[its] = pathsLength.min()
                path_best[its] = pathsList[pathsLength.argmin()].copy()
                
        """updatingg pheromone"""
        addTau = np.zeros((n,n))
        for i in range(m):
            for j in range(n-1):
                addTau[int(pathsList[i, j])][int(pathsList[i, j+1])] += Q/pathsLength[i]
            addTau[int(pathsList[i, n-1]), int(pathsList[i, 0])] += Q/pathsLength[i]
        Tau = (1 - rho)*Tau + addTau
        
        
        
        its += 1

    print(,path_best[-1]+1)
    print("iterating", its_max,"times","""optimized solution""",distance_best[-1])
    
    return path_best, distance_best

