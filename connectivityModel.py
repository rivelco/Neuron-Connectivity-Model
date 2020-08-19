import math
import numpy as np
import csv
import matplotlib.pyplot as plt

import getData
import connectionMatrix
import networkPlots
import connectedComponents
import probabilityFunctions as pf

def main():
    animal = 'Control 6 L1'
    slice = '1D'
    anathomicSc = 'all'
    # Location of file to analyze
    fileLocation = 'Datos para el modelo/Datos para procesar/' + animal + '/' + slice + '.csv'
    #fileLocation = 'Datos para el modelo/Test/1D.csv'

    criteria = 2
    # Criterion used for connections
    criterion = 0.1

    # Dict with converted data extracted from csv file
    # Receives two parameters, a string with file location, and a string indicating the slice, 'all' for all
    cells = getData.extractCells(fileLocation, anathomicSc)
    print('Total number of nodes analyzed: {}'.format(len(cells)))

    # Probability table, for table[a][b] says the probability of connection between node 'a' and 'b'
    # Receives two parameters, a dict with cells properties, and a number indicating the criteria

    matrixAlt = connectionMatrix.probabilityMatrix2Rad(cells, criteria)
    matrix = connectionMatrix.probabilityMatrix(cells, criteria, 125)

    fig, ax = plt.subplots()

    # Puts on plt cache the plot for the dendritic fields of each cell
    # Receives one parameter, the dict with cells info
    networkPlots.drawDendriticFields(cells, ax, True)

    # Puts on plt cache the plot for each edge given a table and certain criterion
    # Receives three parameters, the adjacency matrix, the cells dict for coords, and a 0.0-1 criterion
    networkPlots.drawNodes(cells, ax)
    networkPlots.drawEdges(matrix, cells, criterion, ax)

    # Get total number of connected components. Disc: One connected component has more than one node
    # Returns two objects, a list with the realation of each node and the CC it gelongs to, and the total number
    # Receives two parameters, an adjacency matrix and a criterion for each union
    ccomponents, nodesICC = connectedComponents.connectedComponents(matrix, criterion)
    print("Total number of components: {}".format(len(ccomponents)-1))

    averageNodesPCC = connectedComponents.avgNodesPCC(ccomponents)
    print('Average number of nodes per cc: {}'.format(averageNodesPCC))

    print('Isolated nodes: {}'.format(len(ccomponents['0'])))
    print('Ratio of isolated nodes: {}%'.format(len(ccomponents['0'])/len(cells)*100))

    networkPlots.markThisCells(ccomponents['0'], cells, '#000000', ax)

    averageEdgesPN = connectedComponents.avgEdgesPN(matrix, criterion)
    print('Average number of edges per node: {}'.format(averageEdgesPN))
    #networkPlots.drawConnectedComponents(nodesICC, cells)

    #plt.figure(figsize=(7.15,9.1))
    fig.set_size_inches((7.15,9.1))
    fig.suptitle('Connectivity model - Criteria ' + str(criteria), fontsize=20)
    ax.set_title( animal + ' - Section ' + slice, fontsize=18)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.set_xlabel('X coordinates (um)')
    ax.set_ylabel('Y coordinates (um)')
    ax.grid(color='grey', linestyle='-', linewidth=0.25, alpha=0.5)
    ax.legend()

    plt.xlim(-500, 5000)
    plt.ylim(-500, 6500)
    plt.show()

if __name__ == "__main__":
    main()
