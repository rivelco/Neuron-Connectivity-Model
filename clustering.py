import math
import numpy as np

def singleLocalClusteringCoef(node, adjList, matrix):
    k = len(adjList[node])
    if k == 0 or k == 1:
        return 0
    existent = 0
    for i in range(k):
        nodeA = adjList[node][i]
        for j in range(i+1, k):
            nodeB = adjList[node][j]
            if matrix[nodeA][nodeB] == 1:
                existent += 1
    C = (2*existent)/(k*(k-1))
    return C

def localClusteringCoef(cells, adjList, matrix):
    clustCoefs = np.empty(len(cells))
    for cell in cells:
        current = singleLocalClusteringCoef(cell.name, adjList, matrix)
        clustCoefs[cell.name] = current
    return clustCoefs

def globalClusteringCoef(clusteringCoefs):
    return np.average(clusteringCoefs)

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
        l3, l2 = singleTransitivityCoef(cell.name, adjList, matrix)
        length2 += l2
        length3 += l3

    if length2 == 0:
        return 0
    coef = length3 / length2
    return coef
