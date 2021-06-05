import numpy as np
from queue import PriorityQueue


class Node:

	def __init__(self, path, matrix_reduced, cost, vertex, level):
		self.path = path
		self.matrix = matrix_reduced
		self.cost = cost
		self.vertex = vertex
		self.level = level


def newnode(matrix_parent, level, i, j):
	
	newnode = Node
	newnode.path.append(j)
	newnode.matrix = matrix_parent

	for k in range(len(matrix_parent - 1)):
		if level != 0:
			newnode.matrix[i][k] = float('inf')
			newnode.matrix[k][j] = float('inf')
		
	newnode.matrix[j][0] = float('inf')
	newnode.level = level
	newnode.vertex = j
	newnode.cost = calculatecost(newnode.matrix)
	return newnode
			

def rowreduction(matrix):

	rowmin = np.min(matrix, axis=1)
	for i in range(len(matrix) - 1):
		for j in range(len(matrix) - 1):
			if rowmin[i] != float('inf'):
				matrix[i][j] = matrix[i][j] - rowmin[i]


def columnreduction(matrix):

	columnmin = np.min(matrix, axis=0)

	for j in range(len(matrix) - 1):
		for i in range(len(matrix) - 1):
			if columnmin[i] != float('inf'):
				matrix[i][j] = matrix[i][j] - columnmin[i]


def reducedmatrix(matrix):
	matrix = rowreduction(matrix)
	matrix = columnreduction(matrix)
	return matrix
	

def calculatecost(matrix):

	cost = 0
	rowmin = np.min(matrix, axis=1)
	columnmin = np.min(matrix, axis=0)

	for i in range(len(matrix)-1):
		for num in rowmin:
			if num != float('inf'):
				cost += num

		for num in columnmin:
			if num != float('inf'):
				cost += num

	return cost



def tsp(matrix):
	optimal_cost = 0
	optimal_tour = []
	N = len(matrix) - 1
	pq = PriorityQueue()

	root = newnode(matrix, 0, -1, 0)
	root.matrix = reducedmatrix(root.matrix)
	optimal_cost += root.cost

	pq.put((root.cost, root))

	while not pq.empty():
		minnode = pq.get()
		pq.get()
		optimal_tour.append(minnode[1].vertex)

		if minnode[1].level == N - 1:
			optimal_tour.append(0)

			return optimal_tour, minnode[1].cost

		for j in range(1, N):
			if reducedmatrix(minnode[1].matrix)[minnode[1].vertex][j] != float('inf'):
				child = newnode(minnode[1].matrix, minnode[1].level + 1, minnode[1].vertex, j)
				child.cost = minnode[1].cost + minnode[1].matrix[minnode[1].vertex][j] + calculatecost(child.matrix)
				child.matrix = reducedmatrix(child.matrix)
				pq.put((child.cost, child))
