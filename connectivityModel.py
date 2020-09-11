import math
import numpy as np
import csv
import matplotlib.pyplot as plt
import numpy as np
import random
from statsmodels.graphics.gofplots import qqplot
from scipy.stats import normaltest
import sys

import getData
import connectionMatrix
import networkPlots
import connectedComponents
import probabilityFunctions as pf
import paths
import clustering
import nullModel
import cellsDistribution

def main(animal, slice, section, fixedRadius, criteria, criterion):
    # animal = sys.argv[1]
    # slice = sys.argv[2]
    # section = sys.argv[3]
    # fixedRadius = sys.argv[4]
    # criteria = sys.argv[5]
    # criterion = sys.argv[6]

    fGeneralTable = {}
    fDirectCells = []
    fConnectComps = []
    fNodesInfo = []

    nullModeling = False
    noc = 350

    #animal = 'Control 6 L1'                 # Animal
    #slice = '1D'                            # Slice and side, number may be 1-4, side may be D or I
    #section = 'all'                         # Section inside nuclei, may be 1-3, or all
    #fixedRadius = False                     # Indicating if the program must work with fixed or random radius values
    # Location of file to analyze
    fileLocation = 'Data/For processing/' + animal + '/' + slice + '.csv'

    #criteria = 1                            # Connectivity criteria, may be 1 or 2
    #criterion = 3/7                         # Criterion used for connections -> 1 - (3/7)

    aboutCrit = ''
    if criteria == 2:
        aboutCrit = 'Connectivity criterion ' + str(criterion)

    aboutRad = ''
    if not fixedRadius:
        aboutRad = 'Random radius values (100-150um)'
    else:
        aboutRad = 'Radius size fixed at 125um' #127.47548783981962

    if nullModeling:
        cells = nullModel.generateCells(noc, True, 4000, 5000)
        animal = 'Null model - {} cells'.format(noc)
    else:
        cells = getData.extractCells(fileLocation, section)

    nCells = len(cells)

    matrix = np.empty((nCells, nCells))
    if fixedRadius:         # Choose a fixed or random setting
        matrix = connectionMatrix.probabilityMatrix(cells, criteria, 125)
    else:
        matrix = connectionMatrix.probabilityMatrix2Rad(cells, criteria)

    binMatrix, adjList      = connectionMatrix.binaryMatrix(matrix, criterion)
    ccomponents, nodesICC   = connectedComponents.connectedComponents(binMatrix)
    nodesPCC                = connectedComponents.nodesPerCC(ccomponents)
    nodesPCC_WOZ            = connectedComponents.nodesPerCC_WOZ(ccomponents)
    edgesPN                 = connectedComponents.edgesPerNode(binMatrix)
    centrality              = paths.brandeAlgorithm(adjList)
    localClustering         = clustering.localClusteringCoef(range(0, nCells), adjList, binMatrix)
    globalClustering        = clustering.globalClusteringCoef(localClustering)
    transitivity            = clustering.transitivityCoef(range(1, nCells), adjList, binMatrix)

    ccClustering = np.empty(len(ccomponents)-1)
    for i in range(0, len(ccomponents)-1):
        ccClusteringTemp    = clustering.localClusteringCoef(ccomponents[i+1], adjList, binMatrix)
        ccClustering[i]     = clustering.globalClusteringCoef(ccClusteringTemp)
    ccTransitivity = np.empty(len(ccomponents)-1)
    for i in range(0, len(ccomponents)-1):
        ccTransitivity[i]   = clustering.transitivityCoef(ccomponents[i+1], adjList, binMatrix)

    print('\n#### ' + animal + ' - ' + slice + ' ####')
    print(animal, slice, section, fixedRadius, criteria, criterion)
    print('Total number of nodes analyzed: {}'.format(nCells-1))
    print("Total number of components: {}".format(len(ccomponents)-1))
    print('Isolated nodes: {}'.format(len(ccomponents[0]))) # ccomponents[0] contains the isolated nodes
    print('Global clustering coefficient:', globalClustering)
    print('Transitivity of the network:', transitivity)

    # Generating texts
    fGeneralTable['animal'] = animal
    fGeneralTable['slice'] = slice
    fGeneralTable['section'] = section
    fGeneralTable['number of nodes'] = nCells-1
    fGeneralTable['Fixed radius'] = fixedRadius
    fGeneralTable['criteria'] = criteria
    fGeneralTable['criterion'] = criterion
    fGeneralTable['connected components'] = len(ccomponents) - 1
    fGeneralTable['isolated cells'] = len(ccomponents[0]) - 1
    fGeneralTable['global clustering coeff'] = globalClustering
    fGeneralTable['transitivity'] = transitivity

    folderCrit = ''
    if criteria == 1:
        folderCrit = 'Criteria 1/'
    else:
        folderCrit = 'Criteria 2/{:.4f}/'.format(criterion)
    dataFolder = 'savedData/' + animal + '/' + folderCrit + slice + '/' + section + '/'

    with open(dataFolder + animal + ' - GT.csv', mode='a') as csv_file:
        fieldnames = ['animal', 'slice', 'section', 'number of nodes', 'Fixed radius', 'criteria', 'criterion', 'connected components', 'isolated cells', 'global clustering coeff', 'transitivity']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow(fGeneralTable)

    with open(dataFolder + animal + ' - DC.csv', mode='a') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['cell', 'x', 'y', 'slice', 'radius'])
        for cell in cells:
            writer.writerow([cell.name, cell.x, cell.y, cell.slice, cell.radius])

    with open(dataFolder + animal + ' - CC.csv', mode='a') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['comp', 'bumber of nodes', 'global clustering coefficient', 'transitivity'])
        for i in range(1, len(ccomponents)):
            ccnow = ccomponents[i]
            writer.writerow([i, len(ccnow), ccClustering[i-1], ccTransitivity[i-1]])

    with open(dataFolder + animal + ' - ND.csv', mode='a') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['node', 'degree', 'centrality', 'clustering'])
        for cell in cells:
            i = cell.name
            writer.writerow([i, edgesPN[i], centrality[i], localClustering[i]])

    # Generates the figures
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

    figNetwork, axNetwork = plt.subplots()
    networkPlots.drawNodes(cells, axNetwork, False)
    networkPlots.drawConnectedComponents(ccomponents, binMatrix, cells, axNetwork)
    networkPlots.markThisCells(ccomponents[0], cells, '#FFFFFF', axNetwork)
    #networkPlots.drawDendriticFields(cells, axNetwork, fixedRadius)
    #networkPlots.drawEdges(binMatrix, cells, axNetwork)

    figNodes, axNodes = plt.subplots(1, 3)
    binsND = int(np.amax(edgesPN))
    if binsND <= 0:
        binsND = 10
    axNodes[0].hist(edgesPN, bins = binsND)
    axNodes[1].hist(centrality, bins=12)
    axNodes[2].hist(localClustering, bins=12)

    figCC, axCC = plt.subplots(1, 3)
    axCC[0].hist(nodesPCC_WOZ, bins=10)
    axCC[1].hist(ccClustering, bins=10)
    axCC[2].hist(ccTransitivity, bins=12)

    figDist, axDist = plt.subplots()
    binsX = list(range(-500, 5500, 500))
    binsY = list(range(-500, 7000, 500))
    distCellsX = cellsDistribution.distribution1D(range(1, nCells), cells, 'x')
    distCellsY = cellsDistribution.distribution1D(range(1, nCells), cells, 'y')
    axDist.hist2d(distCellsX, distCellsY, bins=(binsX,binsY), cmap=plt.cm.jet)

    # Style and info for the network plots figure
    figNetwork.set_size_inches((7.15,9.1))
    figNetwork.suptitle('Connectivity model - Criteria ' + str(criteria), fontsize=20)
    axNetwork.set_title( animal + ' - Section ' + slice + '\n' + aboutCrit + '  ' + aboutRad, fontsize=12)
    axNetwork.spines['top'].set_visible(False)
    axNetwork.spines['right'].set_visible(False)
    axNetwork.set_xlabel('X coordinates (um)')
    axNetwork.set_ylabel('Y coordinates (um)')
    axNetwork.grid(color='grey', linestyle='-', linewidth=0.25, alpha=0.5)
    axNetwork.legend()
    axNetwork.set_xlim(-500, 5000)
    axNetwork.set_ylim(-500, 6500)
    figNetworkName = animal + '-' + slice + '-' + section + '.png'
    figNetwork.savefig(dataFolder + figNetworkName, format='png')

    figDist.set_size_inches((7.15,9.1))
    figDist.suptitle('Density of cells', fontsize=20)
    axDist.set_title( animal + ' - Section ' + slice + '\n', fontsize=12)
    axDist.spines['top'].set_visible(False)
    axDist.spines['right'].set_visible(False)
    axDist.set_xlabel('X coordinates (um)')
    axDist.set_ylabel('Y coordinates (um)')
    figDistName = animal + '-' + slice + '-' + section + ' - Hist2d.png'
    figDist.savefig(dataFolder + figDistName, format='png')

    # Style and info for the histograms
    figNodes.set_size_inches((12, 5))
    figNodes.suptitle('Histograms per node', fontsize=16)
    axNodes[0].set_title('Node degree', fontsize=10)
    axNodes[0].spines['top'].set_visible(False)
    axNodes[0].spines['right'].set_visible(False)
    axNodes[0].set_xlabel('Degree')
    axNodes[0].set_ylabel('Amount of nodes')
    axNodes[0].grid(color='grey', linestyle='-', linewidth=0.25, alpha=0.5)
    axNodes[1].set_title('Centrality of each node', fontsize=10)
    axNodes[1].spines['top'].set_visible(False)
    axNodes[1].spines['right'].set_visible(False)
    axNodes[1].set_xlabel('Centrality')
    axNodes[1].set_ylabel('Amount of nodes')
    axNodes[1].grid(color='grey', linestyle='-', linewidth=0.25, alpha=0.5)
    axNodes[2].set_title('Clustering coefficient per node', fontsize=10)
    axNodes[2].spines['top'].set_visible(False)
    axNodes[2].spines['right'].set_visible(False)
    axNodes[2].set_xlabel('Clustering coefficient')
    axNodes[2].set_ylabel('Amount of nodes')
    axNodes[2].grid(color='grey', linestyle='-', linewidth=0.25, alpha=0.5)
    figNodesName = animal + '-' + slice + '-' + section + ' - Hist per nodes.png'
    figNodes.savefig(dataFolder + figNodesName, format='png')

    figCC.set_size_inches((12, 5))
    figCC.suptitle('Histograms per connected component (cc)', fontsize=16)
    axCC[0].set_title('Amount of nodes per cc', fontsize=10)
    axCC[0].spines['top'].set_visible(False)
    axCC[0].spines['right'].set_visible(False)
    axCC[0].set_xlabel('Quantity')
    axCC[0].set_ylabel('Amount of cc')
    axCC[0].grid(color='grey', linestyle='-', linewidth=0.25, alpha=0.5)
    axCC[1].set_title('Global clustering coefficient per cc', fontsize=10)
    axCC[1].spines['top'].set_visible(False)
    axCC[1].spines['right'].set_visible(False)
    axCC[1].set_xlabel('Global clustering coefficient')
    axCC[1].set_ylabel('Amount of cc')
    axCC[1].grid(color='grey', linestyle='-', linewidth=0.25, alpha=0.5)
    axCC[2].set_title('Transitivity per cc', fontsize=10)
    axCC[2].spines['top'].set_visible(False)
    axCC[2].spines['right'].set_visible(False)
    axCC[2].set_xlabel('Transitivity coefficient')
    axCC[2].set_ylabel('Amount of cc')
    axCC[2].grid(color='grey', linestyle='-', linewidth=0.25, alpha=0.5)
    figCCName = animal + '-' + slice + '-' + section + ' - Hist per cc.png'
    figCC.savefig(dataFolder + figCCName, format='png')

    plt.close('all')

    #plt.show()

    print('\n')


if __name__ == "__main__":
    main()
