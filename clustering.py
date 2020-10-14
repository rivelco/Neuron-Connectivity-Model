import math
import numpy as np

# Calculates the clustering coefficient just for one node
# Receives a node to calculate the coefficient, an adjacency list and a binary matrix of adjacency
# Returns the clustering coefficient for that node
def singleLocalClusteringCoef(node, adjList, matrix):
    k = len(adjList[node])          # Get the number of neighbours of that node
    if k == 0 or k == 1:            # If it doesn't have more than 2 neighbours
        return 0                        # return 0, by definition of the coefficient
    existent = 0                    # Counter for the number of existent clusters
    for i in range(k):              # Iterates over all the neighbours
        nodeA = adjList[node][i]        # Get the first neighbour
        for j in range(i+1, k):         # Iterates again over all the neighbours of initial node
            nodeB = adjList[node][j]        # Get a second neighbour, different to the first one
            if matrix[nodeA][nodeB] == 1:   # If the two neighbours are connected
                existent += 1                   # Count that as a cluster, complete connection
    C = (2*existent)/(k*(k-1))      # Calculate the coefficient, actual connections / possible ones
    return C                        # Returns the coefficient

# This function calculates the clustering coefficient for all the nodes in a list
# Receives a list of cells, and adjacency list and a binary matrix of connectivity
# Returns a numpy array with the clustering coefficient for every node
def localClusteringCoef(cells, adjList, matrix):
    clustCoefs = np.empty(len(cells))   # Creates an empty numpy array
    for i, cell in enumerate(cells):    # Iterates over all the cells in the list
        current = singleLocalClusteringCoef(cell, adjList, matrix)  # Get the single coefficient
        clustCoefs[i] = current             # Add that value to the array
    return clustCoefs                   # Returns the numpy array

# Calculates the global clustering coefficient as an average of locals
# Receives a numpy array with the local coefficient of each node
# Returns the average value
def globalClusteringCoef(clusteringCoefs):
    return np.average(clusteringCoefs)

# Calculates the transitivity coefficient for a single node
# Receives the node, an adjacency list and a binary adjacency matrix
# Returns 
def singleTransitivityCoef(nodeA, adjList, matrix):
    k = len(adjList[nodeA])
    length3 = 0
    length2 = 0
    for i in range(k):
        nodeB = adjList[nodeA][i]
        k2 = len(adjList[nodeB])
        for j in range(k2):
            nodeC = adjList[nodeB][j]
            if nodeA != nodeC and nodeB != nodeC:
                length2 += 1
                if matrix[nodeA][nodeC] == 1:
                    length3 += 1
    return length3, length2

def transitivityCoef(cells, adjList, matrix):
    length3 = 0
    length2 = 0
    for cell in cells:
        l3, l2 = singleTransitivityCoef(cell, adjList, matrix)
        length2 += l2
        length3 += l3

    if length2 == 0:
        return 0
    coef = length3 / length2
    return coef
