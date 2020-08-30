import probabilityFunctions as pf
import numpy as np
import math

# This function creates a squared probability matrix
# For matrix[a][b] we get the probability of connection between node 'a' and node 'b'
# this probability is based on certain criteria, it may be 1 or 2
def probabilityMatrix(cells, criteria, radius):
    size = len(cells)       # Get the total number of nodes on dict
    matrix = np.empty((size, size))
    for i, cellA in enumerate(cells):               # Iterates over each node
        for j in range(i, size):
            cellB = cells[j]
            distance = pf.getDistance(cellA, cellB)         # Get the distance between cellA and cellB
            mValue = 0                                      # Auxiliary var for final probability
            if criteria == 1:                               # Checks if we're dealing with criteria 1
                mValue = pf.directUnion(distance, radius)          # Gets corresponding value, either 1 or 0
            elif criteria == 2:                             # Checks if we're dealing with criteria 2
                mValue = pf.probability(distance, radius)          # Gets corresponding value, from 0.0 to 1.0
            else:                                           # Gets inside here if it's a different criteria
                return None                                     # Error value
            matrix[cellA.name][cellB.name] = mValue   # Set that probability value on the matrix
            matrix[cellB.name][cellA.name] = mValue   # Set that probability value on the matrix

    return matrix   # Returns the final table

def probabilityMatrix2Rad(cells, criteria):
    size = len(cells)       # Get the total number of nodes on cells
    matrix = np.empty((size, size))

    for i, cellA in enumerate(cells):               # Iterates over each node
        for j in range(i, size):
            cellB = cells[j]
            distance = pf.getDistance(cellA, cellB)         # Get the distance between cellA and cellB
            mValue = 0                                      # Auxiliary var for final probability
            if criteria == 1:                               # Checks if we're dealing with criteria 1
                mValue = pf.directUnion2Rad(distance, cellA.radius, cellB.radius)          # Gets corresponding value, either 1 or 0
            elif criteria == 2:                             # Checks if we're dealing with criteria 2
                mValue = pf.probability2Rad(distance, cellA.radius, cellB.radius)          # Gets corresponding value, from 0.0 to 1.0
            else:                                           # Gets inside here if it's a different criteria
                return None                                     # Error value
            matrix[cellA.name][cellB.name] = mValue   # Set that probability value on the matrix
            matrix[cellB.name][cellA.name] = mValue   # Set that probability value on the matrix

    return matrix   # Returns the final table

def binaryMatrix(matrix, criterion):
    size = int(math.sqrt(matrix.size))
    binMatrix = np.empty((size, size))
    adjList = {}
    for i in range(size):
        for j in range(i, size):
            adjList[i] = adjList.get(i, [])
            adjList[j] = adjList.get(j, [])
            if matrix[i][j] >= criterion:
                binMatrix[i][j] = 1
                binMatrix[j][i] = 1
                if i != j:
                    adjList[i].append(j)
                    adjList[j].append(i)
            else:
                binMatrix[i][j] = 0
                binMatrix[j][i] = 0
    return binMatrix, adjList

def binMatrixtoAdjList(matrix):
    size = int(math.sqrt(matrix.size))
    adjList = {}
    for i in range(0, size):
        for j in range(0, size):
            adjList[i] = adjList.get(i, [])
            if matrix[i][j] == 1 and i != j:
                adjList[i].append(j)
    return adjList

if __name__ == '__main__':
    mat0 = [[1, 1, 1, 1, 1],
            [1, 0, 0, 0, 0],
            [1, 0, 1, 0, 0],
            [1, 0, 0, 1, 0],
            [1, 0, 0, 0, 1]]
    mat1 = [[1, 1, 1, 1, 1],
            [1, 1, 1, 1, 0],
            [1, 1, 1, 0, 1],
            [1, 1, 0, 1, 0],
            [1, 0, 1, 0, 1]]
    mat2 = [[1, 1, 1, 0, 1, 0],
            [0, 1, 0, 1, 0, 0],
            [0, 0, 1, 0, 0, 0],
            [0, 0, 0, 1, 0, 0],
            [0, 0, 0, 0, 1, 0],
            [1, 0, 0, 0, 0, 1]]
    mat3 = [[1, 1, 1, 0, 1, 1],
            [1, 1, 0, 1, 0, 0],
            [1, 0, 1, 0, 0, 0],
            [0, 1, 0, 1, 0, 0],
            [1, 0, 0, 0, 1, 0],
            [1, 0, 0, 0, 0, 1]]
    mat4 = [[1, 0, 1, 0, 0, 0, 0],
            [0, 1, 1, 0, 0, 0, 0],
            [0, 0, 1, 1, 1, 0, 0],
            [0, 0, 0, 1, 0, 1, 0],
            [0, 0, 0, 0, 1, 1, 0],
            [0, 0, 0, 0, 0, 1, 1],
            [0, 0, 0, 0, 0, 0, 1]]
    matrix = np.array(mat0)
    C = binMatrixtoAdjList(matrix)
    print(C)
    print(type(C))
    matrix = np.array(mat1)
    C = binMatrixtoAdjList(matrix)
    print(C)
    matrix = np.array(mat2)
    C = binMatrixtoAdjList(matrix)
    print(C)
    matrix = np.array(mat3)
    C = binMatrixtoAdjList(matrix)
    print(C)
    matrix = np.array(mat4)
    C = binMatrixtoAdjList(matrix)
    print(C)
