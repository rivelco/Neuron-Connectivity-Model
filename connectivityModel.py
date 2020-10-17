import numpy as np
import csv
import matplotlib.pyplot as plt
import pathlib

import getData
import connectionMatrix
import networkPlots
import connectedComponents
import probabilityFunctions as pf
import paths
import clustering
import nullModel
import cellsDistribution

# Main function, performs the topological  analysis and generates the reports for every analysis
# Receives a python dictionary with the following keys and example values
# animal        : "Control 6 L1"    - Name of the animal to look for or to generate (if null animal)
# slice         : "2D"              - Number (1-4) and side (I, D) of the slide
# section       : "all"             - Name of the section, either '1', '2', '3' or 'all'
# fixedRadius   : True              - Boolean value to evaluate fixed or random radius values
# criteria      : 2                 - Criteria to evaluate, either 1 or 2
# criterion     : 0.4285            - Criterion or probability to consider, always float
# nullModeling  : False             - Boolean value, True if generating a null model
# noc           : 302               - Number of cells to consider when null-modeling
# nullArea      : 14.0756           - Area of the nuclei when null-modeling
# saveCSV       : True              - Boolean value, True if want to save the CSV report files
# saveFigs      : True              - Boolean value, True if want to save the figs, PNG files
# showFigs      : False             - Boolean value, True if want to display the figs
# When saving reports, the function creates a folder tree like this:
#   'savedData/[animal]/Criteria [criteria]/{criterion}/[slice]/[section]/
# Inside saves the report data that was indicated. If nothing is saved, the folder is not created
def main(inData):
    # Unzip the input data if given, either way it is loaded by defaults
    animal          = inData.get("animal", "Not specified")
    slice           = inData.get("slice", "2D")
    section         = inData.get("section", "all")
    fixedRadius     = inData.get("fixedRadius", True)
    criteria        = inData.get("criteria", 2)
    criterion       = inData.get("criterion", 0.4285)
    nullModeling    = inData.get("nullModeling", False)
    noc             = inData.get("noc", 300)
    nullArea        = inData.get("nullArea", 14.0756)
    saveCSV         = inData.get("saveCSV", False)
    saveFigs        = inData.get("saveFigs", False)
    showFigs        = inData.get("showFigs", True)

    # So we can know the current animal being analyzed
    print('\n>>         ' + animal + ' - ' + slice + '         <<')
    print(">> Section: " + section + " | Criteria: " + str(criteria) + " | Criterion: " + str(criterion))

    # Location of file to analyze
    fileLocation = 'Data/Processing/' + animal + '/' + slice + '.csv'

    # For display style
    aboutCrit = ''
    if criteria == 2:
        aboutCrit = 'Connectivity criterion ' + str(criterion)
    # For display style
    aboutRad = ''
    if not fixedRadius:
        aboutRad = 'Random radius values (100-150um)'
    else:
        aboutRad = 'Radius size fixed at 125um' #127.47548783981962

    if nullModeling:        # If null modeling was selected
        nullrMin = 1250     # Arbitrary size of one side
        nullrMax = int(nullModel.rMax(nullArea, nullrMin))  # Calculates the other radius
        cells = nullModel.generateCells(noc, True, 2*nullrMin, 2*nullrMax)  # Generates the cells
    else:
        cells = getData.extractCells(fileLocation, section) # Extract the experimental data

    nCells = len(cells) # number of cells to analyze

    matrix = np.empty((nCells, nCells))     # Matrix to work with
    if fixedRadius:                         # Choose a fixed or random setting
        matrix = connectionMatrix.probabilityMatrix(cells, criteria, 125)   # Creates the matrix
    else:
        matrix = connectionMatrix.probabilityMatrix2Rad(cells, criteria)    # Creates the matrix

    # Creates the data to generate the reports. See individual function documentation for more info
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

    # Summary to console
    print('- Total number of nodes analyzed  {}'.format(nCells-1))
    print('- Total number of components      {}'.format(len(ccomponents)-1))
    print('- Isolated nodes                  {}'.format(len(ccomponents[0])))
    print('- Global clustering coefficient   {}'.format(globalClustering))
    print('- Transitivity of the network     {}'.format(transitivity))

    # Generating texts
    fGeneralTable = {}
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

    # Creates the folder path
    folderCrit = ''
    if criteria == 1:
        folderCrit = 'Criteria 1/'
    else:
        folderCrit = 'Criteria 2/{:.4f}/'.format(criterion)
    dataFolder = 'savedData/' + animal + '/' + folderCrit + slice + '/' + section

    if saveCSV:
        pathlib.Path(dataFolder).mkdir(parents=True, exist_ok=True) # Creates all the folders
        # Summary report
        with open(dataFolder + '/' + animal + ' - GT.csv', mode='a') as csv_file:
            fieldnames = ['animal', 'slice', 'section', 'number of nodes', 'Fixed radius',
                          'criteria', 'criterion', 'connected components', 'isolated cells',
                          'global clustering coeff', 'transitivity']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerow(fGeneralTable)
        # Saves all the cells data
        with open(dataFolder + '/' + animal + ' - DC.csv', mode='a') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(['cell', 'x', 'y', 'slice', 'radius'])
            for cell in cells:
                writer.writerow([cell.name, cell.x, cell.y, cell.slice, cell.radius])
        # Saves data for every connected component, individually
        with open(dataFolder + '/' + animal + ' - CC.csv', mode='a') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(['comp', 'number of nodes', 'global clustering coefficient', 'transitivity'])
            for i in range(1, len(ccomponents)):
                ccnow = ccomponents[i]
                writer.writerow([i, len(ccnow), ccClustering[i-1], ccTransitivity[i-1]])
        # Saves the data of every node, individually
        with open(dataFolder + '/' + animal + ' - ND.csv', mode='a') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(['node', 'degree', 'centrality', 'clustering'])
            for cell in cells:
                i = cell.name
                writer.writerow([i, edgesPN[i], centrality[i], localClustering[i]])

    plt.rcParams.update({  # Setting style for the figures
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

    figNetwork, axNetwork = plt.subplots()  # Main fig of networks
    networkPlots.drawNodes(cells, axNetwork, False)
    networkPlots.drawConnectedComponents(ccomponents, binMatrix, cells, axNetwork)
    networkPlots.markThisCells(ccomponents[0], cells, '#FFFFFF', axNetwork)
    #networkPlots.drawDendriticFields(cells, axNetwork, fixedRadius)
    #networkPlots.drawEdges(binMatrix, cells, axNetwork)

    figNodes, axNodes = plt.subplots(1, 3)  # Figs for the histograms for individual nodes
    binsND = int(np.amax(edgesPN))
    if binsND <= 0:
        binsND = 10
    axNodes[0].hist(edgesPN, bins = binsND)
    axNodes[1].hist(centrality, bins=12)
    axNodes[2].hist(localClustering, bins=12)

    figCC, axCC = plt.subplots(1, 3)        # Figs for individual connected components
    axCC[0].hist(nodesPCC_WOZ, bins=10)
    axCC[1].hist(ccClustering, bins=10)
    axCC[2].hist(ccTransitivity, bins=12)

    figDist, axDist = plt.subplots()        # Figs for 2D histogram of distribution
    binsX = list(range(-500, 5500, 500))
    binsY = list(range(-500, 7000, 500))
    distCellsX = cellsDistribution.distribution1D(range(1, nCells), cells, 'x')
    distCellsY = cellsDistribution.distribution1D(range(1, nCells), cells, 'y')
    axDist.hist2d(distCellsX, distCellsY, bins=(binsX,binsY), cmap=plt.cm.jet)

    # Style and info for the network figure
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

    # Style and info for the 2D histogram
    figDist.set_size_inches((7.15,9.1))
    figDist.suptitle('Density of cells', fontsize=20)
    axDist.set_title( animal + ' - Section ' + slice + '\n', fontsize=12)
    axDist.spines['top'].set_visible(False)
    axDist.spines['right'].set_visible(False)
    axDist.set_xlabel('X coordinates (um)')
    axDist.set_ylabel('Y coordinates (um)')
    figDistName = animal + '-' + slice + '-' + section + ' - Hist2d.png'

    # Style and info for the histograms of individual nodes
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

    # Style and info for the histograms of individual connected components
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

    if saveFigs:    # Saves the figures if indicated
        figNetwork.savefig(dataFolder + '/ ' + figNetworkName, format='png')
        figDist.savefig(dataFolder + '/ ' + figDistName, format='png')
        figNodes.savefig(dataFolder + '/ ' + figNodesName, format='png')
        figCC.savefig(dataFolder + '/ ' + figCCName, format='png')

    if showFigs:    # Shows the figures if indicated
        plt.show()
    else:
        plt.close('all')

if __name__ == "__main__":
    # Example of input data
    inData = {}
    inData["animal"]        = "Control 6 L1"
    inData["slice"]         = "2D"
    inData["section"]       = "all"
    inData["fixedRadius"]   = True
    inData["criteria"]      = 2
    inData["criterion"]     = 0.4285
    inData["nullModeling"]  = False
    inData["noc"]           = 302
    inData["nullArea"]      = 14.0756
    inData["saveCSV"]       = True
    inData["saveFigs"]      = True
    inData["showFigs"]      = True
    main(inData)
