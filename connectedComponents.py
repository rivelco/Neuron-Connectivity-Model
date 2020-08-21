import math
import numpy as np

# This funtion find the connected components from a given binary matrix
# Returns a dict of lists where each list holds the nodes it contains, also a relation of nodes and components
def connectedComponents(matrix):
    size = int(math.sqrt(matrix.size))             # Total amount of nodes in matrix, given that is squared
    nodes = np.full(size, -1)                      # List that indicates the [i] node belongs to the nodes[i] coponent

    queue = []                      # Queue for the nodes to process on the BFS
    compCounter = 0                 # Counter for the total connectet components
    components = {}                 # Dict of lists, the key holds the list of nodes of that key. key is always a number
    components[0] = []              # This component holds the isolated nodes, nodes of component 0

    for node in range(1, size):       # For each node on the matrix
        if nodes[node] == -1:           # If we have not visited the node previously
            queue.append(node)              # insert that new node on the queue
            compCounter += 1                # increase the components counter by one
            flag = False                    # Flag to check if the next node has more connections
            key = compCounter               # Make a key with current component number
            while len(queue) > 0:           # while exists more connected nodes
                current = queue.pop(0)          # Take one node to work with
                if nodes[current] == -1:        # We only process the node if it has not been analyzed before
                    nodes[current] = compCounter    # marks the connected component that node belongs to
                    if not key in components:       # if that key does'nt exists on the components dict
                        components[key] = []            # we create a new list for that key
                    components[key].append(current)     # add the current node to the list it belongs to
                    for comparedNode in range(1, size): # Iterates over all the nodes that are connected to current
                        # If that connection exists and we have not visited that node before
                        if matrix[current][comparedNode] == 1 and nodes[comparedNode] == -1:
                            flag = True                 # Flag true when a new connection for 'current' is found
                            queue.append(comparedNode)  # we add that node to the queue
            if not flag:            # False when no connections has been found, it means a connected component of 1 node
                compCounter -= 1        # Take one out from the counter because we're correcting here
                del components[key]     # Delete the entry from the dict
                components[0].append(current) # Add that isolated node to the corresponding key
                nodes[current] = 0      # Mark this cell as "alone" on the list
    # Return the dict of lists of connected components the relation of nodes and the component they belong to
    return components, nodes

# Function that receives a dict of lists of connected components
# Returns a list of the amount of nodes of every connected component
def nodesPerCC(components):
    size = len(components)
    nodespcc = np.empty(size)            # New list that holds the number of nodes per cc
    for i in range(size):                # Iterates over all the components on the dict
        nodespcc[i] = len(components[i])      # Add each number of elements per cc
    return nodespcc                                 # Returns the list of number of nodes per cc

# Function that receives a dict of lists of connected components
# Returns a list of the amount of nodes of every connected component without the isolated cells
def nodesPerCC_WOZ(components):
    size = len(components)
    nodespcc = np.empty(size - 1)           # New list that holds the number of nodes per cc
    for i in range(1, size):                # Iterates over all the components on the dict
        nodespcc[i-1] = len(components[i])      # Add each number of elements per cc
    return nodespcc                         # Returns the list of number of nodes per cc

# Returns a numpy array indicating that the node i has edgesPN[i] edges
# Needs a binary matrix
def edgesPerNode(matrix):
    size = int(math.sqrt(matrix.size))          # Get the size of the squared matrix
    edgesPN = np.zeros(size)                    # Fill with zeros
    for i in range(size):                       # Analyze the whole matrix
        for j in range(size):
            if not i == j:                      # Does not count the diagonal
                if matrix[i][j] == 1:           # If a connection is found
                    edgesPN[i] += 1                 # Count that edge in the node
    return edgesPN                              # Return that array

# Returns the average number of nodes per cc given a dict of components
# Deprecated since this data is not normally distributed
def avgNodesPCC(components):
    nodespcc = nodesPerCC(components)   # Get the number on nodes per cc
    avg = 0                             # Initialize the result
    for cc in nodespcc:                 # Iterates over the list
        avg += cc                           # Sums up every element
    avg -= nodespcc[0]                  # Takes out the isolated nodes
    avg = avg / (len(components)-1)     # Calculate the average
    return avg                          # Returns that number

# Retrurns the average number of edges per node
# Deprecated since the distribution usually is not normal
def avgEdgesPN(matrix):
    edgesPN = edgesPerNode(matrix)
    avg = 0
    for edge in edgesPN:
        avg += edge
    avg -= edgesPN[0]
    avg = avg /(len(edgesPN)-1)
    return avg
