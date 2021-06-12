import numpy as np
from queue import PriorityQueue


class Node:

    def __init__(self, path, matrix_reduced, cost, vertex, level):
        self.path = path  # order of vertices
        self.matrix = matrix_reduced
        self.cost = cost
        self.vertex = vertex
        self.level = level
        
    def __lt__(self,other):
        if isinstance(other, Node):
            return self.cost < other.cost
        else: 
            raise TypeError
    
    def __le__(self, other):
        if isinstance(other, Node):
            return self.cost <= other.cost
        else: 
            raise TypeError


def newnode( matrix_parent, level, i, j, prev_node=None):  # prev_node node class object of i 
    if prev_node:
        path = prev_node.path+[j]
    else:
        path = [0]
 
    node = Node(path, matrix_parent, calculatecost(matrix_parent), j, level)
    
    for k in range(len(matrix_parent)):
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
    node_queue = []
    matrix = matrix + np.diag([float('inf')]*len(matrix)) # mat change

    root = newnode(matrix, 0, -1, 0)
    root.matrix = reducedmatrix(root.matrix)

    pq.put((root.cost, root))
    minnode = pq.queue[0]
    while not pq.empty():



        q = PriorityQueue()

        if minnode[1].level == (len(matrix) - 1):
            node_queue = sorted(node_queue)
            # print(node_queue)
            return(minnode[1].path+[0], minnode[1].cost, node_queue)
          

        for j in range(1, len(matrix)):

            if minnode[1].matrix[minnode[1].vertex][j] != float('inf'):


                #child.cost = cost of travel + costcurrentreduction + cost of previuos reduction
                #child.matrix = reducedmatrix(changerowcolumn to inf matrix)
                minmatrix_copy = minnode[1].matrix.copy()

                new_level = minnode[1].level + 1
                i = minnode[1].vertex

                child = newnode(minnode[1].matrix, new_level, i, j, prev_node=minnode[1])
                #after newnode matrix is goin to have the infs
                # minnodematrix has changed
                cost = minmatrix_copy[minnode[1].vertex][j] + minnode[1].cost + calculatecost(child.matrix)
                # during calculate cost child.matrix already gets row reduced
                child.matrix = columnreduction(child.matrix)
                child.cost = cost
                # reset minnode matrix back what it was
                minnode[1].matrix = minmatrix_copy

                q.put((child.cost, child)) # add to q
            
        minnode = q.queue[0]
        [node_queue.append(i) for i in q.queue[1:]] # collects any children not explored


def children(node, n):
#puts every unvisited child of a node in a list, matrix length is n
    
    q = PriorityQueue()
    for j in range(1, n):
        if node[1].matrix[node[1].vertex][j] != float('inf'):
            # child.cost = cost of travel + costcurrentreduction + cost of previous reduction
            # child.matrix = reducedmatrix(changerowcolumn to inf matrix)
            minmatrix_copy = node[1].matrix.copy()

            new_level = node[1].level + 1
            i = node[1].vertex

            child = newnode(node[1].matrix, new_level, i, j,
                            prev_node=node[1])
            # after newnode matrix is goin to have the infs
            # minnodematrix has changed
            cost = (minmatrix_copy[node[1].vertex][j] + node[1].cost
                    + calculatecost(child.matrix))
            # during calculate cost child.matrix already gets row reduced
            child.matrix = columnreduction(child.matrix)
            child.cost = cost
            # reset minnode matrix back what it was
            node[1].matrix = minmatrix_copy
            q.put((child.cost, child))  # add to q
    return q

    


def tspfull(matrix):

    lowerbound = tsp(matrix)[1]  #first lowerbound
    matrix_copy = matrix.copy()
    n = len(matrix)
    matrix = matrix + np.diag([float('inf')]*len(matrix))  # mat change

    root = newnode(matrix, 0, -1, 0)
    root.matrix = reducedmatrix(root.matrix)
    
    #create list with root
    q = []
    q.append((root.cost, root))

    #go through each level
    for i in range(1, n):
        w = [] #this will be a list of all the unvisited children nodes of each node in q
        while q:
            currentnode = q.pop(0)
            for childnode in children(currentnode, n):
                if childnode[0] < lowerbound: #if that childnode is below the lowerbound, that branch is explored
                    w.append(childnode)
            q = w #q is now a list of the next level of children with costs below lowerbound

    if len(q) == 0:
    #if q becomes empty, then there is no other path with a cost less than the lowerbound, so return original path
        return tsp(matrix_copy)
    else:
    #otherwise, find the least costing path out of the level4 children and make that the path
        minnode = min(q)
        return minnode[1].path+[0], minnode[1].cost

def tspfull2(matrix):
    tsp_output = tsp(matrix) 
    lowerbound = tsp_output[1]  #first lowerbound
    matrix_copy = matrix.copy()
    n = len(matrix)
    matrix = matrix + np.diag([float('inf')]*len(matrix))  # mat change
    
    less_lb = [i for i in tsp_output[2] if i[0]<lowerbound]
    # empty list check 
    less_lb
    less_lb_level = sorted(less_lb, key=lambda x: -1*x[1].level)
    furthestless_lb_lev # take smallest 

    root = newnode(matrix, 0, -1, 0)
    root.matrix = reducedmatrix(root.matrix)
    
    
    