import numpy as np

# This function generates the array to plot one dimension of an histogram for density of cells
# Receives a range of cells, a list of cells objects and an axe, either 'y' or 'x'
# Returns the numpy array with the values of an axe of every cell
def distribution1D(cells, cellsDic, axis):
    histogram = np.empty(len(cells))        # Creates a numpy array
    for i, cell in enumerate(cells):        # Iterates over all the cells
        if axis == 'x':                     # Choose an axe to work with
            histogram[i] = cellsDic[cell].x     # Extract the value of each cell for that axe
        elif axis == 'y':
            histogram[i] = cellsDic[cell].y
    return histogram                        # Returns the numpy array
