import numpy as np
from queue import PriorityQueue


class Node:

    def __init__(self, path, matrix_reduced, cost, vertex, level):
        self.path = path  # order of vertices
        self.matrix = matrix_reduced
        self.cost = cost
        self.vertex = vertex
        self.level = level


def newnode( matrix_parent, level, i, j, prev_node=None):  # prev_node node class object of i 
    if prev_node:
        path = prev_node.path.append(j)
    else:
        path = [0]
 
    node = Node(path, matrix_parent, calculatecost(matrix_parent), j, level)
    
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
    print(columnmin)

    for j in range(len(matrix)):
        for i in range(len(matrix)):
            if columnmin[j] != float('inf'): #i to j 
                matrix[i][j] = matrix[i][j] - columnmin[j] # i to j
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
    for num1, num2 in zip(rowmin, columnmin):
        if num1 != float('inf'):
            cost += num1
        if num2 != float('inf'):
            cost += num2

    return cost


def tsp(matrix):
    pq = PriorityQueue()
    matrix = matrix + np.diag([float('inf')]*len(matrix)) # mat change
 
    root = newnode(matrix, 0, -1, 0)
    root.matrix = reducedmatrix(root.matrix)

    pq.put((root.cost, root))

    while not pq.empty():

        if len(pq.queue) != 1:
            pq.get()
        minnode = pq.queue[0]
        q = PriorityQueue()
        q.put(minnode) # q kept

        if minnode[1].level == len(matrix) - 1:
            return minnode[1].path.append(0), minnode[1].cost

        for j in range(1, len(matrix)):
            if minnode[1].matrix[minnode[1].vertex][j] != float('inf'):
                child = newnode(minnode[1].matrix, minnode[1].level + 1, minnode[1].vertex, j)
                child.cost = minnode[1].cost + minnode[1].matrix[minnode[1].vertex][j] + calculatecost(child.matrix)
                child.matrix = reducedmatrix(child.matrix)
                q.put((child.cost, child)) # add to q
