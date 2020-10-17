import math
import numpy as np

# Get total number of connected components. Disc: One connected component has more than one node
# Receives a binary matrix of adjacency
# Returns a dict of lists indicating the nodes that belong to each cc (cc[0] has isolated nodes)
# and a numpy array with the relation of each node belonging to witch cc
def connectedComponents(matrix):
    size = matrix.shape[0]     # Total amount of different nodes in matrix, given that is squared
    nodes = np.full(size, -1)  # List that indicates the [i] node belongs to the nodes[i] component
    queue = []                 # Queue for the nodes to process on the BFS
    compCounter = 0            # Counter for the total connected components
    components = {}            # Dict of lists, the int(key) holds the list of nodes of that key
    components[0] = []         # This component holds the isolated nodes, nodes of component 0
    # Implementation of a BFS to find all the connected components in the matrix
    for node in range(1, size):       # For each node on the matrix
        if nodes[node] == -1:           # If we have not visited the node previously
            queue.append(node)              # insert that new node on the queue
            compCounter += 1                # increase the components counter by one
            flag = False                    # Flag to check if the next node has more connections
            key = compCounter               # Make a key with current component number
            while len(queue) > 0:           # while exists more connected nodes
                current = queue.pop(0)          # Take one node to work with
                if nodes[current] == -1:        # Process the node if it hasn't been analyzed before
                    nodes[current] = compCounter# marks the connected component that node belongs to
                    components[key] = components.get(key, []) # Get or create that cc list
                    components[key].append(current) # add the current node to the list it belongs to
                    for comparedNode in range(1, size): # Iterates over all the other nodes
                        # If a connection exists and we have not visited that node before
                        if matrix[current][comparedNode] == 1 and nodes[comparedNode] == -1:
                            flag = True    # Flag true when a new connection with 'current' is found
                            queue.append(comparedNode)  # we add that node to the queue
            if not flag:            # False when no other connections have been found
                compCounter -= 1      # Take one out from the counter because we're correcting here
                del components[key]   # Delete the entry from the dict
                components[0].append(current) # Add that isolated node to the corresponding key [0]
                nodes[current] = 0    # Mark this cell as "alone" on the list
    # Return the dict of lists of connected components
    # and the relation of nodes and the component they belong to
    return components, nodes

# This function returns the number of nodes of every connected component
# Receives a dict of lists of connected components
# Returns a numpy array with the amount of nodes on every connected component
def nodesPerCC(components):
    size = len(components)
    nodespcc = np.empty(size)            # New list that holds the number of nodes per cc
    for i in range(size):                # Iterates over all the components on the dict
        nodespcc[i] = len(components[i])      # Add each number of elements per cc
    return nodespcc                      # Returns the list of number of nodes per cc

# Returns the number of nodes of every connected component without the isolated nodes
# Receives a dict of lists of connected components
# Returns a numpy array with the amount of nodes of every connected component w/o the isolated cells
def nodesPerCC_WOZ(components):
    size = len(components)
    nodespcc = np.empty(size - 1)           # New list that holds the number of nodes per cc
    for i in range(1, size):                # Iterates over all the components on the dict
        nodespcc[i-1] = len(components[i])      # Add each number of elements per cc
    return nodespcc                         # Returns the list of number of nodes per cc

# This functions returns the degree of each node given a binary matrix
# Receives a binary matrix of adjacency
# Returns a numpy array indicating that the node i has edgesPN[i] edges
def edgesPerNode(matrix):
    size = matrix.shape[0]                      # Get the size of the squared matrix
    edgesPN = np.zeros(size)                    # Fill with zeros
    for i in range(size):                       # Analyze the whole matrix
        for j in range(size):
            if not i == j:                      # Does not count the diagonal
                if matrix[i][j] == 1:           # If a connection is found
                    edgesPN[i] += 1                 # Count that edge in the node
    return edgesPN                              # Return that array
