import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.collections import PatchCollection

# This function puts on plt cache each valid edge on a given probability matrix
def drawEdges(matrix, cells, criterion, ax):
    for i in range(len(matrix[0])):                 # Iterates over each node
        for j in range(len(matrix[0])):                 # Iterates again for each comparable node
            if not i == j:                                  # Only iterate over one side of the symmetric matrix
                if matrix[i][j] >= criterion:                   # If that probability is valid given the criterion
                    xValues = [cells[str(i)].x, cells[str(j)].x]    # Extract the 'y' coordinates of every cell
                    yValues = [cells[str(i)].y, cells[str(j)].y]    # And the 'x' coordinates too
                    ax.plot(xValues, yValues, zorder=2)                      # Plot that edge
            else:
                break                                       # Breaks when iterating on the other side

def drawNodes(cells, ax):
    listXM = []      # List for 'x' coordinates
    listYM = []      # List for 'y' coordinates
    listXV = []      # List for 'x' coordinates
    listYV = []      # List for 'y' coordinates
    listXL = []      # List for 'x' coordinates
    listYL = []      # List for 'y' coordinates
    for key, cell in cells.items():     # Iterate over the dict items
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
    if len(listXL) > 0:
        ax.scatter(listXL, listYL, marker='.', c='#0000FF', alpha=1, edgecolor='none', label='Dorsal lateral', zorder=3)  # Plots those coordinates
    if len(listXV) > 0:
        ax.scatter(listXV, listYV, marker='.', c='#00FF00', alpha=1, edgecolor='none', label='Ventral', zorder=3)  # Plots those coordinates

def markThisCells(toDraw, cells, color, ax):
    listX = []
    listY = []
    for cell in toDraw:
        temp = cells[str(cell)]
        listX.append(temp.x)
        listY.append(temp.y)
    if len(listX) > 0:
        ax.scatter(listX, listY, marker='o', c=color, alpha=1, edgecolor='none', zorder=5, label='Isolated cell')

# This function puts on plt cache the dendritic fields of a given dict of cells
# it diferentiates with color for each section or 'Slice'
def drawDendriticFields(cells, ax, radConst):
    listX = []      # List for 'x' coordinates
    listY = []      # List for 'y' coordinates
    colors = []     # List for the color of each node
    patches = []
    color = ''

    for key, cell in cells.items():     # Iterate over the dict items
        if cell.slice == 1:                 # Identify the dorsal medial section
            colors.append('#FF0000')            # with red color
            color = '#FF0000'
        elif cell.slice == 2:               # Identify the ventral region
            colors.append('#00FF00')            # with green color
            color = '#00FF00'
        elif cell.slice == 3:               # Identify the dorsal lateral section
            colors.append('#0000FF')            # with blue color
            color = '#0000FF'
        axes = (cell.x, cell.y)
        rad = 125
        if not radConst:
            rad = cell.radius
        circle = mpl.patches.Circle(axes, radius=rad, color=color)
        patches.append(circle)
        listX.append(cell.x)                # Adds each coordinate to respective list
        listY.append(cell.y)

    p = PatchCollection(patches, alpha=0.5, color=colors, edgecolor='none', zorder=1)
    ax.add_collection(p)
    # .- area = 350     # Set the size of the dendritic field, just for graphical purposes
    #plt.scatter(listX, listY, s=area, c=colors, alpha=0.5, edgecolor='none')  # Plots those coordinates
    # .- plt.xlabel("Coords X")  # Label for x
    # .- plt.ylabel("Coords Y")  # Label for y
    return p

def drawConnectedComponents(components, cells):
    cc = {}
    for i in range(1, len(components)):
        key = str(components[i])
        if not key in cc:
            cc[key] = []
        cc[key].append(i)

    listX = []
    listY = []
    for ccn, items in cc.items():
        if not str(ccn) == '0':
            for item in items:
                listX.append(cells[str(item)].x)
                listY.append(cells[str(item)].y)
            plt.plot(listX, listY)
            listX.clear()
            listY.clear()
    print(cc)
