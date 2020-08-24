import math
import numpy

def localClusteringCoef(node, matrix):
    size = int(math.sqrt(matrix.size))
    neighbours = []
    total = 0
    for i in range(size):
        if matrix[node][i] == 1 and i != node:
            neighbours.append(i)
            total += 1

    actualConnctions = 0
    for nodeA in range(0, len(neighbours)):
        for nodeB in range(nodeA+1, len(neighbours)):
            if matrix[nodeA][nodeB] == 1:
                actualConnections += 1


    if matrix[node][node] == 1:
        total -= 1
