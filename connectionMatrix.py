import probabilityFunctions as pf

# This function creates a squared probability matrix
# For matrix[a][b] we get the probability of connection between node 'a' and node 'b'
# this probability is based on certain criteria, it may be 1 or 2
def probabilityMatrix(cells, criteria, radius):
    size = len(cells)       # Get the total number of nodes on dict

    matrix = [[0 for x in range(size+1)] for y in range(size+1)]    # Declare a squared matrix

    for keyA, cellA in cells.items():               # Iterates over each node
        for keyB, cellB in cells.items():               # For each node, we iterate again for each node (max)
            distance = pf.getDistance(cellA, cellB)         # Get the distance between cellA and cellB
            mValue = 0                                      # Auxiliary var for final probability
            if criteria == 1:                               # Checks if we're dealing with criteria 1
                mValue = pf.directUnion(distance, radius)          # Gets corresponding value, either 1 or 0
            elif criteria == 2:                             # Checks if we're dealing with criteria 2
                mValue = pf.probability(distance, radius)          # Gets corresponding value, from 0.0 to 1.0
            else:                                           # Gets inside here if it's a different criteria
                return None                                     # Error value

            matrix[int(cellA.name)][int(cellB.name)] = mValue   # Set that probability value on the matrix
            matrix[int(cellB.name)][int(cellA.name)] = mValue   # even on the reflex

    return matrix   # Returns the final table

def binaryMatrix(matrix, criterion):
    size = len(matrix[0])
    binMatrix = [[0 for x in range(size+1)] for y in range(size+1)]    # Declare a squared matrix
    for i in range(size):
        for j in range(size):
            if matrix[i][j] >= criterion:
                binMatrix[i][j] = 1
            else:
                binMatrix[i][j] = 0
    return binMatrix


def probabilityMatrix2Rad(cells, criteria):
    size = len(cells)       # Get the total number of nodes on dict

    matrix = [[0 for x in range(size+1)] for y in range(size+1)]    # Declare a squared matrix

    for keyA, cellA in cells.items():               # Iterates over each node
        for keyB, cellB in cells.items():               # For each node, we iterate again for each node (max)
            distance = pf.getDistance(cellA, cellB)         # Get the distance between cellA and cellB
            mValue = 0                                      # Auxiliary var for final probability
            if criteria == 1:                               # Checks if we're dealing with criteria 1
                mValue = pf.directUnion2Rad(distance, cellA.radius, cellB.radius)          # Gets corresponding value, either 1 or 0
            elif criteria == 2:                             # Checks if we're dealing with criteria 2
                mValue = pf.probability2Rad(distance, cellA.radius, cellB.radius)          # Gets corresponding value, from 0.0 to 1.0
            else:                                           # Gets inside here if it's a different criteria
                return None                                     # Error value

            matrix[int(cellA.name)][int(cellB.name)] = mValue   # Set that probability value on the matrix
            matrix[int(cellB.name)][int(cellA.name)] = mValue   # even on the reflex

    return matrix   # Returns the final table
