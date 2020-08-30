import heapq as hq
import math
import numpy as np
from collections import deque

# Implementation of Dijkstra's algorithm uing a priority queue
# Receives two arguments, adjacency matrix and starting node
# Returns two numpy arrays, first indicates minimum path cost from 'start' to each node
# and the second array indicates the previous node to succesfully reconstruct the shortest path
def shortestPath(matrix, start):
    size = int(math.sqrt(matrix.size))                  # Get the size of the squared matrix
    dist = np.full(size, math.inf)                      # Array of distances, tarting with infinity
    prev = np.full(size, None)                          # Array of prev nodes, starts with none (usefull on reconstruction)
    queue = []                                          # Will be a priority queue
    dist[start] = 0                                     # "Going to start from start costs 0"
    hq.heappush(queue, (start, dist[start]))            # Create priority queue and insert the startng point
    # Previous line, second arguent reads as: "going to 'start' from start, costs 'dist[start]'"
    while len(queue) > 0:                       # While not empty queue
        origin, cost = hq.heappop(queue)            # Extract origin node and cost to get there
        for neighbour in range(size):               # Analyze each neighbour, may be iproved by adacency list
            #if matrix[origin][neighbour] != None:       # Detect a valid connection for our problem
            if matrix[origin][neighbour] == 1:
                now = cost + matrix[origin][neighbour]      # Calculates the new cost to get there
                if now < dist[neighbour]:                   # If that cost is better than the previosly known
                    dist[neighbour] = now                       # The new cot is that newly calculated
                    prev[neighbour] = origin                    # And the previous node to get there is 'origin'
                    hq.heappush(queue, (neighbour, dist[neighbour]))    # Insert that new data to queue
    return dist, prev       # Return the array with costs and the array for reconstruct the path

# This function reconstruct the shortest path to get to any other node
# Receives three arguments, the path from Dijkstra's algorithm, the origin node and the target node
# Returns a list with the nodes to visit in order to get the minimum cost
def reconstructPath(path, origin, target):
    rec = []                            # List with the nodes that reconstruct the shortest path
    if path[target] != None or target == origin:    # If path exists or the following node is the origin
        while target != None:                           # While the target cell exists
            rec.append(target)                              # Add that node to the result list
            target = path[target]                           # Check the previos node of that one
    rec.reverse()                       # Invert the list in order to give the correct sequence from origin to target
    return rec                          # return the result

# Implementation of Brande's algorithm for betweenes centrality
# Check https://ucilnica.fri.uni-lj.si/pluginfile.php/1212/course/section/1199/Brandes%20-%20A%20faster%20algorithm%20for%20betweenness%20centrality%2C%202001.pdf
def brandeAlgorithmMat(matrix):
    size = int(math.sqrt(matrix.size))
    V = range(size)
    C = np.zeros(size)
    for node in V:
        S = []
        P = np.empty(size, dtype=np.object)
        for i in range(P.shape[0]):
            P[i] = []
        sigma = np.zeros(size)
        sigma[node] = 1
        d = np.full(size, -1)
        d[node] = 0
        queue = deque([])
        queue.append(node)
        while queue:
            v = queue.popleft()
            S.append(v)
            for w in V:
                if matrix[v][w] == 1:
                    if d[w] < 0:
                        queue.append(w)
                        d[w] = d[v] + 1
                    if d[w] == d[v] + 1:
                        sigma[w] = sigma[w] + sigma[v]
                        P[w].append(v)
        delta = np.zeros(size)
        while S:
            w = S.pop()
            for v in P[w]:
                delta[v] = delta[v] + (sigma[v]/sigma[w])*(1+delta[w])
            if w != node:
                C[w] = C[w] + delta[w]
    return C

def brandeAlgorithm(adjList):
    #size = int(math.sqrt(matrix.size))
    size = len(adjList)
    V = range(size)
    C = np.zeros(size)
    for node in V:
        S = []
        P = np.empty(size, dtype=np.object)
        for i in range(P.shape[0]):
            P[i] = []
        sigma = np.zeros(size)
        sigma[node] = 1
        d = np.full(size, -1)
        d[node] = 0
        queue = deque([])
        queue.append(node)
        while queue:
            v = queue.popleft()
            S.append(v)
            for w in adjList[v]:
                #if matrix[v][w] == 1:
                if d[w] < 0:
                    queue.append(w)
                    d[w] = d[v] + 1
                if d[w] == d[v] + 1:
                    sigma[w] = sigma[w] + sigma[v]
                    P[w].append(v)
        delta = np.zeros(size)
        while S:
            w = S.pop()
            for v in P[w]:
                delta[v] = delta[v] + (sigma[v]/sigma[w])*(1+delta[w])
            if w != node:
                C[w] = C[w] + delta[w]
    return C

def test():
    mat0 = [[1, 1, 1, 1, 1],
            [1, 1, 1, 1, 0],
            [1, 1, 1, 0, 1],
            [1, 1, 0, 1, 0],
            [1, 0, 1, 0, 1]]
    mat1 = [[0, 6, None, 7, None],
              [None, 0, 5, 8, -4],
              [None, -2, 0, None, 7],
              [None, None, -3, 0, 9],
              [2, None, None, None, 0]]

    matrix = np.array(mat0)
    dist, prev = shortestPath(matrix, 2)
    rec = reconstructPath(prev, 2, 3)
    print(dist)
    print(prev)
    print(rec)

if __name__ == '__main__':
    test()
