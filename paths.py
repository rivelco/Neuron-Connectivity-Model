import heapq as hq
import math
import numpy as np

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
            if matrix[origin][neighbour] != None:       # Detect a valid connection for our problem
            #if matrix[origin][neighbour] == 1:
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
              
    matrix = np.array(mat1)
    dist, prev = shortestPath(matrix, 0)
    rec = reconstructPath(prev, 0, 4)
    print(dist)
    print(prev)
    print(rec)

if __name__ == '__main__':
    test()
