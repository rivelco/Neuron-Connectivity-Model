import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.collections import PatchCollection
import math
import random
import numpy as np

# This function puts on plt cache each valid edge on a given probability matrix
def drawEdges(matrix, cells, ax):
    size = int(math.sqrt(matrix.size))
    for i in range(size):                 # Iterates over each node
        for j in range(i, size):                 # Iterates again for each comparable node
            # Only iterate over one side of the symmetric matrix
            if matrix[i][j] == 1 and not i == j:      # If that probability is valid given the criterion
                xValues = [cells[i].x, cells[j].x]      # Extract the 'y' coordinates of every cell
                yValues = [cells[i].y, cells[j].y]      # And the 'x' coordinates too
                ax.plot(xValues, yValues, zorder=2, color='#FFFF00')     # Plot that edge

def drawNodes(cells, ax, tags):
    listXM = []      # List for 'x' coordinates
    listYM = []      # List for 'y' coordinates
    listXV = []      # List for 'x' coordinates
    listYV = []      # List for 'y' coordinates
    listXL = []      # List for 'x' coordinates
    listYL = []      # List for 'y' coordinates
    for cell in cells:     # Iterate over the dict items
        if cell.name == 0:
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
        ax.scatter(listXM, listYM, marker='.', c='#FF0000', alpha=1, edgecolor='none', label='Dorsal medial', zorder=3)  # Plots those coordinates
        if tags:
            for i, tag in enumerate(range(len(listXM))):
                ax.annotate(tag, (listXM[i], listYM[i]))
    if len(listXL) > 0:
        ax.scatter(listXL, listYL, marker='.', c='#0000FF', alpha=1, edgecolor='none', label='Dorsal lateral', zorder=3)  # Plots those coordinates
        if tags:
            for i, tag in enumerate(range(len(listXL))):
                ax.annotate(tag, (listXL[i], listYL[i]))
    if len(listXV) > 0:
        ax.scatter(listXV, listYV, marker='.', c='#00FF00', alpha=1, edgecolor='none', label='Ventral', zorder=3)  # Plots those coordinates
        if tags:
            for i, tag in enumerate(range(len(listXV))):
                ax.annotate(tag, (listXV[i], listYV[i]))

def markThisCells(toDraw, cells, color, ax):
    listX = []
    listY = []
    for cell in toDraw:
        temp = cells[cell]
        listX.append(temp.x)
        listY.append(temp.y)
    if len(listX) > 0:
        ax.scatter(listX, listY, marker='.', c=color, alpha=1, edgecolor='none', zorder=5, label='Isolated cell')

def drawConnectedComponents(ccomponents, matrix, cells, ax):
    size = int(math.sqrt(matrix.size))
    colors = []
    visited = np.zeros(size)
    queue = []

    sComp = len(ccomponents)
    for i in range(sComp):
        colors.append('#%06X' % random.randint(0, 0xFFFFFF))
    cit = 0

    for i in range(1, sComp):
        queue.append(ccomponents[i][0])
        while len(queue) > 0:
            now = queue.pop(0)
            if visited[now] == 0:
                visited[now] = 1
                currentCompSize = len(ccomponents[i])
                for j in range(0, currentCompSize):
                    node = ccomponents[i][j]
                    if matrix[now][node] == 1 and visited[node] == 0:
                        queue.append(node)
                        xValues = [cells[now].x, cells[node].x]      # Extract the 'y' coordinates of every cell
                        yValues = [cells[now].y, cells[node].y]      # And the 'x' coordinates too
                        ax.plot(xValues, yValues, zorder=2, color=colors[cit])     # Plot that edge
                #print(queue)
        cit += 1


# This function puts on plt cache the dendritic fields of a given dict of cells
# it diferentiates with color for each section or 'Slice'
def drawDendriticFields(cells, ax, radConst):
    colors = []     # List for the color of each node
    patches = []

    for cell in cells:     # Iterate over the dict items
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
        circle = mpl.patches.Circle(axes, radius=rad)   # Create a new circle form with given attributes
        patches.append(circle)              # Add that circle to the patches list

    p = PatchCollection(patches, alpha=0.3, color=colors, edgecolor='none', zorder=1) # Create collection
    ax.add_collection(p)    # Add that collection to the given axes
