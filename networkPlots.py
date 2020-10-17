import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.collections import PatchCollection
import math
import random
import numpy as np

# This function puts on ax each valid edge in a given binary matrix
# Receives a binary matrix, a list of cells and a matplotlib object ax
# Does not return anything but draws all the edges in ax
def drawEdges(matrix, cells, ax):
    size = matrix.shape[0]              # Calculates the number of nodes
    for i in range(size):               # Iterates over each node
        for j in range(i, size):            # Only iterate over one side of the symmetric matrix
            if matrix[i][j] == 1 and not i == j:      # If that connection exists not with itself
                xValues = [cells[i].x, cells[j].x]    # Extract the 'y' coordinates of every cell
                yValues = [cells[i].y, cells[j].y]    # And the 'x' coordinates too
                ax.plot(xValues, yValues, zorder=2, color='#FFFF00')     # Plot that edge

# This function draws on ax each node
# Receives a list of cells, a matplotlib ax object, and a boolean value to plot or not each name
# Does not return anything but draws every node on the cells list as a scatter plot
def drawNodes(cells, ax, tags):
    listXM = []      # List for 'x' coordinates, for dorsal medial region
    listYM = []      # List for 'y' coordinates, for dorsal medial region
    listXV = []      # List for 'x' coordinates, for ventral region
    listYV = []      # List for 'y' coordinates, for ventral region
    listXL = []      # List for 'x' coordinates, for dorsal lateral region
    listYL = []      # List for 'y' coordinates, for dorsal lateral region
    for cell in cells:                  # Iterate over the dict items
        if cell.name == 0:                  # Ignores the foo cell at [0]
            continue
        if cell.slice == 1:                 # Identify the dorsal medial section
            listXM.append(cell.x)                # Adds each coordinate to respective list
            listYM.append(cell.y)
        elif cell.slice == 2:               # Identify the ventral region
            listXV.append(cell.x)                # Adds each coordinate to respective list
            listYV.append(cell.y)
        elif cell.slice == 3:               # Identify the dorsal lateral section
            listXL.append(cell.x)                # Adds each coordinate to respective list
            listYL.append(cell.y)
    if len(listXM) > 0:
        # Plots those coordinates with given color and label
        ax.scatter(listXM, listYM, marker='.', c='#FF0000', alpha=1, edgecolor='none', label='Dorsal medial', zorder=3)
        if tags:    # If true then plot each node name, recommended only for small references
            for i, tag in enumerate(range(len(listXM))):
                ax.annotate(tag, (listXM[i], listYM[i]))
    if len(listXL) > 0:
        # Plots those coordinates with given color and label
        ax.scatter(listXL, listYL, marker='.', c='#0000FF', alpha=1, edgecolor='none', label='Dorsal lateral', zorder=3)
        if tags:    # If true then plot each node name, recommended only for small references
            for i, tag in enumerate(range(len(listXL))):
                ax.annotate(tag, (listXL[i], listYL[i]))
    if len(listXV) > 0:
        # Plots those coordinates with given color and label
        ax.scatter(listXV, listYV, marker='.', c='#00FF00', alpha=1, edgecolor='none', label='Ventral', zorder=3)
        if tags:    # If true then plot each node name, recommended only for small references
            for i, tag in enumerate(range(len(listXV))):
                ax.annotate(tag, (listXV[i], listYV[i]))

# This function marks a given list of nodes, here is marking the isolated cells with white on ax
# Receives a list with the cells to draw, the main list of cells, color to use and matplotlib ax
# Does not return anything but draws the given list of cells with the specified color
def markThisCells(toDraw, cells, color, ax):
    listX = []                  # List of X coordinates
    listY = []                  # List of Y coordinates
    for cell in toDraw:         # Iterates over the given list of cells
        temp = cells[cell]          # Get the info of the current cell from the main cells list
        listX.append(temp.x)        # Add it's coordinates to the corresponding list
        listY.append(temp.y)
    if len(listX) > 0:          # If we added some cells then plot those with label
        ax.scatter(listX, listY, marker='.', c=color, alpha=1, edgecolor='none', zorder=5, label='Isolated cell')

# Draw with different colors each connected component
# Receives a dict of connected components, a binary matrix, a list of cells and a matplotlib ax
# Does not returns anything but prints every connected component with different colors
def drawConnectedComponents(ccomponents, matrix, cells, ax):
    size = matrix.shape[0]      # Get the number of cells
    colors = []                 # List for the different colors
    visited = np.zeros(size)    # Numpy array for visited nodes on the BFS
    queue = []                  # List to use as a queue on the BFS

    sComp = len(ccomponents)    # Get the number of connected components
    for i in range(sComp):      # For each connected component we generate a new color
        colors.append('#%06X' % random.randint(0, 0xFFFFFF))    # Add each color to colors list
    cit = 0                     # Iterator for the colors list
    # Implementation of a BFS to find all the different connected components
    for i in range(1, sComp):           # Iterates over each connected component
        queue.append(ccomponents[i][0])     # Add the first node of the current connected component
        while len(queue) > 0:               # While we haven't finished reaching every node
            now = queue.pop(0)                  # Get a node from the queue
            if visited[now] == 0:               # If we haven't visited that node
                visited[now] = 1                    # Mark as visited
                currentCompSize = len(ccomponents[i])   # Get the number of neighbours of that node
                for j in range(0, currentCompSize):         # Iterates over every node
                    node = ccomponents[i][j]                    # Get a neighbour
                    if matrix[now][node] == 1 and visited[node] == 0:   # If is valid
                        queue.append(node)                      # Add it to the queue
                        xValues = [cells[now].x, cells[node].x] # Extract the 'y' coordinates
                        yValues = [cells[now].y, cells[node].y] # And the 'x' coordinates too
                        ax.plot(xValues, yValues, zorder=2, color=colors[cit])  # Plot that edge
        cit += 1 # At this point we have finished with the cc i-1, so move on to the next color


# This function draws on ax the dendritic fields of a given list of cells
# Receives a list of cells, a matplotlib ax object and boolean value to print a constant rad or not
# Doesn't return anything but draws the dendritic field of each cell with different color per region
def drawDendriticFields(cells, ax, radConst):
    colors = []     # List for the colors for each node
    patches = []    # List of patches cause we're drawing circles
    for cell in cells:     # Iterate over the cells
        if cell.name == 0:                  # Skip the foo cell
            continue
        if cell.slice == 1:                 # Identify the dorsal medial section
            colors.append('#FF0000')            # with red color
        elif cell.slice == 2:               # Identify the ventral region
            colors.append('#00FF00')            # with green color
        elif cell.slice == 3:               # Identify the dorsal lateral section
            colors.append('#0000FF')            # with blue color
        axes = (cell.x, cell.y)             # Get tuple of axes
        rad = 125                           # Set default radius
        if not radConst:                    # If we don't want constant radius
            rad = cell.radius                   # Get the random radius from the model
        circle = mpl.patches.Circle(axes, radius=rad)   # Create a new circle with given attributes
        patches.append(circle)              # Add that circle to the patches list
    # Create collection of circles, put all together
    p = PatchCollection(patches, alpha=0.3, color=colors, edgecolor='none', zorder=1)
    ax.add_collection(p)    # Draw that collection in the given ax object
