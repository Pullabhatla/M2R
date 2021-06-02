import numpy as np
from queue import PriorityQueue


class Node:

	def __init__(self, path, matrix_reduced, cost, vertex, level):
		self.path = path
		self.matrix = matrix_reduced
		self.cost = cost
		self.vertex = vertex
		self.level = level

	def newnode(self, matrix_parent, level, i, j):

		newnode = Node
		
		newnode.path = self.path.append(j)
		
		newnode.matrix = matrix_parent

		for k in range(len(matrix_parent - 1)):
			if level != 0:
				newnode.matrix[i][k] = float('inf')
				newnode.matrix[k][j] = float('inf')
		
		newnode.matrix[j][0] = float('inf')

		newnode.level = level
		newnode.vertex = j

		self = newnode

		return self
			

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
	matrix = rowReduction(matrix)
	matrix = columnReduction(matrix)
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

	pq = PriorityQueue()

	root = Node.newnode(matrix, 0, -1, 0)

	rootcost = calculateCost(root.matrix)

	pq.push(rootcost)

	for j in range(len(matrix)-1):
		child = Node.newnode()

	
