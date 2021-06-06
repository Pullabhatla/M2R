import numpy as np
from queue import PriorityQueue


class Node:

    def __init__(self, path, matrix_reduced, cost, vertex, level):
        self.path = path
        self.path = []
        self.matrix = matrix_reduced
        self.cost = cost
        self.vertex = vertex
        self.level = level


def newnode(matrix_parent, level, i, j):

    node = Node([], matrix_parent, calculatecost(matrix_parent), j, level)
    node.path.append(j)

    for k in range(len(matrix_parent) - 1):
        if level != 0:
            node.matrix[i][k] = float('inf')
            node.matrix[k][j] = float('inf')

    node.matrix[j][0] = float('inf')
    return node


def rowreduction(matrix):

    rowmin = np.min(matrix, axis=1)
    for i in range(len(matrix)):
        for j in range(len(matrix)):
            if rowmin[i] != float('inf'):
                matrix[i][j] = matrix[i][j] - rowmin[i]
    return matrix


def columnreduction(matrix):

    columnmin = np.min(matrix, axis=0)

    for j in range(len(matrix)):
        for i in range(len(matrix)):
            if columnmin[i] != float('inf'):
                matrix[i][j] = matrix[i][j] - columnmin[i]
    return matrix


def reducedmatrix(matrix):
    matrix = rowreduction(matrix)
    matrix = columnreduction(matrix)
    return matrix


def calculatecost(matrix):
    cost = 0
    rowmin = np.min(matrix, axis=1)
    matrix = rowreduction(matrix)
    columnmin = np.min(matrix, axis=0)

    for num in rowmin:
        if num != float('inf'):
            cost += num

    for num in columnmin:
        if num != float('inf'):
            cost += num

    return cost


def tsp(matrix):
    optimal_cost = 0
    pq = PriorityQueue()
    for i in range(len(matrix)):
        matrix[i][i] = float('inf')

    root = newnode(matrix, 0, -1, 0)
    root.matrix = reducedmatrix(root.matrix)
    optimal_cost += root.cost

    pq.put((root.cost, root))

    while not pq.empty():
        minnode = pq.get()
        pq.get()

        if minnode[1].level == len(matrix) - 1:
            return minnode[1].path, minnode[1].cost

        for j in range(1, len(matrix)):
            if reducedmatrix(minnode[1].matrix)[minnode[1].vertex][j] != float('inf'):
                child = newnode(minnode[1].matrix, minnode[1].level + 1, minnode[1].vertex, j)
                child.cost = minnode[1].cost + minnode[1].matrix[minnode[1].vertex][j] + calculatecost(child.matrix)
                child.matrix = reducedmatrix(child.matrix)
                pq.put((child.cost, child))
