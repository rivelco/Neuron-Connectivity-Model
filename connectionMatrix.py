import probabilityFunctions as pf
import numpy as np
import math

# This function creates a squared matrix indicating the distances between each pair of cells
# Receives a list containing the cells objects
# Returns a numpy matrix where matrix[int(A)][int(B)] contains the distance between cell A and B
def distanceMatrix(cells):
    size = len(cells)                       # Get the number of cells
    matrix = np.empty((size, size))         # Create the matrix
    for i, cellA in enumerate(cells):       # Iterates over all the cells
        for j in range(i, size):                # Iterates with optimization
            cellB = cells[j]                            # Get the current cell
            distance = pf.getDistance(cellA, cellB)     # Calculates the distance
            matrix[cellA.name][cellB.name] = distance   # Get it into the matrix
            matrix[cellB.name][cellA.name] = distance   # Get it into the matrix
    return matrix                           # Return the matrix

# This function creates a squared probability matrix
# Receives a list of cells, a criteria (1 or 2) and a radius (float)
# Returns a numpy matrix where matrix[a][b] has the probability of connection between node 'a' and
# node 'b', given a criteria and a radius (equal for both nodes)
def probabilityMatrix(cells, criteria, radius):
    size = len(cells)                                       # Get the total number of nodes on dict
    matrix = np.empty((size, size))                         # Creates the numpy matrix
    for i, cellA in enumerate(cells):                       # Iterates over each node
        for j in range(i, size):
            cellB = cells[j]                        # Get the current second cell
            distance = pf.getDistance(cellA, cellB) # Get the distance between cellA and cellB
            mValue = 0                              # Auxiliary var for final probability
            if criteria == 1:                       # Checks if we're dealing with criteria 1
                mValue = pf.directUnion(distance, radius)# Gets corresponding value, either 1 or 0
            elif criteria == 2:                     # Checks if we're dealing with criteria 2
                mValue = pf.probability(distance, radius)# Gets corresponding value, from 0.0 to 1.0
            else:                                   # Gets inside here if it's a different criteria
                return None                              # Error value
            matrix[cellA.name][cellB.name] = mValue   # Set that probability value on the matrix
            matrix[cellB.name][cellA.name] = mValue   # Set that probability value on the matrix
    return matrix   # Returns the final table

# This function creates a squared probability matrix
# Receives a list of cells and a criteria (1 or 2)
# Returns a numpy matrix where matrix[a][b] has the probability of connection between node 'a' and
# node 'b', given a criteria and the random radius of each cell
def probabilityMatrix2Rad(cells, criteria):
    size = len(cells)       # Get the total number of nodes on cells
    matrix = np.empty((size, size))
    for i, cellA in enumerate(cells):                       # Iterates over each node
        for j in range(i, size):
            cellB = cells[j]
            distance = pf.getDistance(cellA, cellB)  # Get the distance between cellA and cellB
            mValue = 0                               # Auxiliary var for final probability
            if criteria == 1:                        # Checks if we're dealing with criteria 1
                # Gets corresponding value, either 1 or 0, using the random radius values
                mValue = pf.directUnion2Rad(distance, cellA.radius, cellB.radius)
            elif criteria == 2:                      # Checks if we're dealing with criteria 2
                # Gets corresponding value, from 0.0 to 1.0, using the random radius values
                mValue = pf.probability2Rad(distance, cellA.radius, cellB.radius)
            else:                                    # Gets inside here if it's a different criteria
                return None                              # Error value
            matrix[cellA.name][cellB.name] = mValue   # Set that probability value on the matrix
            matrix[cellB.name][cellA.name] = mValue   # Set that probability value on the matrix
    return matrix   # Returns the final table

# Create a binary matrix for a given probability matrix and criterion 0.0-1.0
# Receives a probability numpy matrix and a float value as a threshold, from 0.0 to 1.0
# Returns a numpy matrix and a adjacency list with the thresholded data, just 1's and 0's
def binaryMatrix(matrix, criterion):
    size = matrix.shape[0]              # Get the number of nodes
    binMatrix = np.empty((size, size))  # Creates a new numpy matrix
    adjList = {}                        # Dict for the adjacency list
    for i in range(size):               # Iterates over all the cells
        for j in range(i, size):            # Little optimization
            adjList[i] = adjList.get(i, []) # Get the current adj-list or creates a new one
            adjList[j] = adjList.get(j, []) # Same for node j
            if matrix[i][j] > criterion:    # If the threshold is reached
                binMatrix[i][j] = 1             # Mark with 1 the corresponding position in matrix
                binMatrix[j][i] = 1             # Mirroed matrix
                if i != j:                      # Avoid to put a node in it's own adj-list
                    adjList[i].append(j)            # Append the current node to the adj-list
                    adjList[j].append(i)            # Same for the other node
            else:                           # If the threshold is not reached
                binMatrix[i][j] = 0         # Mark with 0 the corresponding position
                binMatrix[j][i] = 0         # Mirroed. Nothing to do with adj-lists
    return binMatrix, adjList           # Returns the matrix and the adj-list

# This function converts a binary matrix to an adjacency list using a python dict
# Receives the binary numpy matrix
# Returns a python dict that contains lists corresponding to the adjacency list for each node
def binMatrixtoAdjList(matrix):
    size = matrix.shape[0]              # Get the number of nodes
    adjList = {}                        # Creates the python dict
    for i in range(0, size):            # Iterates over the whole matrix
        for j in range(0, size):            # No optimization applies here
            adjList[i] = adjList.get(i, [])     # Get the adjList for the node or creates it
            # IMPORTANT to keep this assignation here and not inside the if, because all the nodes
            # must be in the dict so we never get a key error, just empty lists
            if matrix[i][j] == 1 and i != j:    # If the connection exists and the node is valid
                adjList[i].append(j)                # Append the node to the corresponding list
    return adjList                      # Returns the adjacency list
