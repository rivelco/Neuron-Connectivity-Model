import math
import numpy as np
import csv
import matplotlib.pyplot as plt
import numpy as np

import getData
import connectionMatrix
import networkPlots
import connectedComponents
import probabilityFunctions as pf
import paths

def main():
    animal = 'Control 6 L1'                 # Animal
    slice = '1D'                            # Slice and side, number may be 1-4, side may be D or I
    anathomicSc = 'all'                     # Section inside nuclei, may be 1-3, or all
    fixedRadius = True                      # Indicating if the program must work with fixed or random radius values
    # Location of file to analyze
    fileLocation = 'Data/For processing/' + animal + '/' + slice + '.csv'
    #fileLocation = 'Data/Test/1D.csv'

    criteria = 1                            # Connectivity criteria, may be 1 or 2
    criterion = 3/7                         # Criterion used for connections

    aboutCrit = ''
    if criteria == 2:
        aboutCrit = 'Connectivity criterion ' + str(criterion)
    aboutRad = ''
    if not fixedRadius:
        aboutRad = 'Random radius values (125-150um)'
    else:
        aboutRad = 'Radius size fixed at 125um'

    print('\n#### ' + animal + ' - ' + slice + ' ####')

    # Numpy array with converted data extracted from csv file
    # Receives two parameters, a string with file location, and a string indicating the slice, 'all' for all
    cells = getData.extractCells(fileLocation, anathomicSc)
    print('Total number of nodes analyzed: {}'.format(len(cells)))

    # Probability table using numpy, for table[a][b] says the probability of connection between node 'a' and 'b'
    # Receives three parameters, an array with cells properties, and a number indicating the criteria
    # Matrix alone generates a matrix with a fixed radius on the third argument
    # Matrix2Rad generates random radius, generated inside the function, just 2 parameters needed
    matrixFix = connectionMatrix.probabilityMatrix(cells, criteria, 125)
    matrixAlt = connectionMatrix.probabilityMatrix2Rad(cells, criteria)

    matrix = np.empty((len(cells), len(cells)))
    if fixedRadius:         # Choose a fixed or random setting
        matrix = matrixFix
    else:
        matrix = matrixAlt

    plt.rcParams.update({                   # Plot style configuration
        "lines.color": "white",
        "patch.edgecolor": "white",
        "text.color": "white",
        "axes.facecolor": "black",
        "axes.edgecolor": "lightgray",
        "axes.labelcolor": "white",
        "xtick.color": "white",
        "ytick.color": "white",
        "grid.color": "lightgray",
        "figure.facecolor": "black",
        "figure.edgecolor": "black",
        "savefig.facecolor": "black",
        "savefig.edgecolor": "black"})

    fig, ax = plt.subplots()                # Plot for network plots

    # Puts on ax the plot for each node
    # Receives two parameters, the cells array for coords and the ax for drawing
    networkPlots.drawNodes(cells, ax)

    # Puts on ax the plot for the dendritic fields of each cell
    # Receives three parameter, the array with cells info, the ax and a bool indicating if it has to plot fixed radius
    networkPlots.drawDendriticFields(cells, ax, fixedRadius)

    # Puts on ax the draw of all edges on a given binary matrix
    #networkPlots.drawEdges(binMatrix, cells, ax)

    # Create a binary matrix for a given probability matrix and criterion 0.0-1.0
    binMatrix = connectionMatrix.binaryMatrix(matrix, criterion)

    # Get total number of connected components. Disc: One connected component has more than one node
    # Returns two objects, a dict of lists indicating the nodes that belong to each cc (cc[0] has isolated nodes)
    # and a numpy array with the ralation of each node belonging to each cc
    # Receives one parameter, a binary matrix
    ccomponents, nodesICC = connectedComponents.connectedComponents(binMatrix)
    print("Total number of components: {}".format(len(ccomponents)-1))
    # Draw with different colors each connected component
    # Uses a relation of cc, a binary matrix, the cells info and the ax where the figure will be draw
    networkPlots.drawConnectedComponents(ccomponents, binMatrix, cells, ax)

    # ccomponents[0] contains the isolated nodes
    print('Isolated nodes: {}'.format(len(ccomponents[0])))
    # This function marks a given list of nodes, here is marking the isolated cells in white on ax
    networkPlots.markThisCells(ccomponents[0], cells, '#FFFFFF', ax)

    # This function returns the amount of nodes per connected component on a dict of lists
    nodesPCC = connectedComponents.nodesPerCC(ccomponents)
    nodesPCC_WOZ = connectedComponents.nodesPerCC_WOZ(ccomponents)
    print('Median of nodes per cc: {}'.format(np.median(nodesPCC_WOZ)))

    # Returns a numpy array indicating the degree (number of edges) of each node
    edgesPN = connectedComponents.edgesPerNode(binMatrix)
    print('Median of edges per node: {}'.format(np.median(edgesPN)))
    #edgVals, edgCounts = np.unique(edgesPN, return_counts=True)
    #edgHist = dict(zip(edgVals, edgCounts))

    # Creates a figure for the histogram of node degree and nodes per connected components
    fig2, ax2 = plt.subplots(1, 2)
    # Creates the graph of each node degree
    ax2[0].hist(edgesPN, bins = int(np.amax(edgesPN)))
    ax2[1].hist(nodesPCC_WOZ, bins = len(nodesPCC_WOZ))

    mat0 = [[1, 1, 1, 1, 1],
            [1, 1, 1, 1, 0],
            [1, 1, 1, 0, 1],
            [1, 1, 0, 1, 0],
            [1, 0, 1, 0, 1]]
    mat1 = np.array(mat0)
    counts = np.zeros(5)
    for i in range(0, 5):
        dis, prev = paths.shortestPath(mat1, i)
        for j in range(0, 5):
            rec = paths.reconstructPath(prev, i, j)
            for node in range(1, len(rec)-1):
                counts[node] += 1

    print('Los conteos son: ')
    print(counts)


    figFolder = 'Figures/Saved/'
    # Style and info for the network plots figure
    fig.set_size_inches((7.15,9.1))
    fig.suptitle('Connectivity model - Criteria ' + str(criteria), fontsize=20)
    ax.set_title( animal + ' - Section ' + slice + '\n' + aboutCrit + '  ' + aboutRad, fontsize=12)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.set_xlabel('X coordinates (um)')
    ax.set_ylabel('Y coordinates (um)')
    ax.grid(color='grey', linestyle='-', linewidth=0.25, alpha=0.5)
    ax.legend()
    ax.set_xlim(-500, 5000)
    ax.set_ylim(-500, 6500)
    figName = animal + '-' + slice + '.png'
    fig.savefig(figFolder + figName, format='png')

    # Style and info for the histograms
    fig2.set_size_inches((9, 5))
    fig2.suptitle('Histograms of frequency', fontsize=16)

    ax2[0].set_title('Number of edges per node', fontsize=10)
    ax2[0].spines['top'].set_visible(False)
    ax2[0].spines['right'].set_visible(False)
    ax2[0].set_xlabel('Degree (edges per node)')
    ax2[0].set_ylabel('Nodes with that degree')
    ax2[0].grid(color='grey', linestyle='-', linewidth=0.25, alpha=0.5)
    ax2[1].set_title('Number of cells per connected component', fontsize=10)
    ax2[1].spines['top'].set_visible(False)
    ax2[1].spines['right'].set_visible(False)
    ax2[1].set_xlabel('Number of cells')
    ax2[1].set_ylabel('Number of connected components')
    ax2[1].grid(color='grey', linestyle='-', linewidth=0.25, alpha=0.5)
    fig2Name = animal + '-' + slice + ' - Hist' + '.png'
    fig2.savefig(figFolder + fig2Name, format='png')

    plt.show()

    print('\n')


if __name__ == "__main__":
    main()
