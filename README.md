# Neuron Connectivity Model

Scripts for neuronal interaction modeling. The scripts consider the geometry of the neuron, the location and a criteria for connection.

## [cellsDistribution](cellsDistribution.py)

This file is intended to include the functions that will analyze the distribution of cells.

### distribution1D

This function generates the array to plot one dimension of an histogram for density of cells. Receives a range of cells, a list of cells objects and an ax, either 'y' or 'x'. Returns the numpy array with the values of an ax of every cell.

```
histogram = distribution1D(cells, cellsDic, axis)
```

## [clustering](clustering.py)

This file is intended to include the functions that analyzes different clustering indicators such as clustering coefficient and transitivity.

### singleLocalClusteringCoef

Calculates the clustering coefficient just for one node. Receives a node to calculate the coefficient, an adjacency list and a binary matrix of adjacency. Returns the clustering coefficient for that node.

```
C = singleLocalClusteringCoef(node, adjList, matrix)
```

### localClusteringCoef

This function calculates the clustering coefficient for all the nodes in a list. Receives a list of cells, and adjacency list and a binary matrix of connectivity. Returns a numpy array with the clustering coefficient for every node.

```
localClustering = localClusteringCoef(cells, adjList, matrix)
```

### globalClusteringCoef

Calculates the global clustering coefficient as an average of locals. Receives a numpy array with the local coefficient of each node. Returns the average value.

```
globalClustering = globalClusteringCoef(clusteringCoefs)
```

### singleTransitivityCoef

Calculates the transitivity coefficient for a single node. Receives the node, an adjacency list and a binary adjacency matrix. Returns the number of paths of length three and two respectively.

```
length3, length2 = singleTransitivityCoef(nodeA, adjList, matrix)
```

### transitivityCoef

Calculates the global coefficient of transitivity of a network. Receives a list of cells (may be a `range(1, n)`), an adjacency list and a binary adjacency matrix. Returns the transitivity coefficient, paths of length 3 over paths of length 2.

```
transitivity = transitivityCoef(cells, adjList, matrix)
```

## [connectedComponents](connectedComponents.py)

This file is intended to contain the functions used to find and describe some basic data about the connected components in the slice.

### connectedComponents

Get total number of connected components. Disc: One connected component has more than one node. Receives a binary matrix of adjacency. Returns a dictionary of lists indicating the nodes that belong to each connected components (`cc[0]` has isolated nodes) and a numpy array with the relation of each node belonging to witch connected components.

```
components, nodes = connectedComponents(matrix)
```

### nodesPerCC

This function returns the number of nodes of every connected component. Receives a dictionary of lists of connected components. Returns a numpy array with the amount of nodes on every connected component.

```
nodespcc = nodesPerCC(components)
```

### nodesPerCC_WOZ

Returns the number of nodes of every connected component without the isolated nodes. Receives a dictionary of lists of connected components. Returns a numpy array with the amount of nodes of every connected component without the isolated cells.

```
nodespcc = nodesPerCC_WOZ(components)
```

### edgesPerNode

This functions returns the degree of each node given a binary matrix. Receives a binary matrix of adjacency. Returns a numpy array indicating that the node `i` has `edgesPN[i]` edges.

```
edgesPN = edgesPerNode(matrix)
```

## [connectionMatrix](connectionMatrix.py)

This file contains the functions used to produce different kinds of matrices, like adjacency and distance matrix.

### distanceMatrix

This function creates a squared matrix indicating the distances between each pair of cells. Receives a list containing the cells objects. Returns a numpy matrix where `matrix[int(A)][int(B)]` contains the distance between cell `A` and `B`.

```
matrix = distanceMatrix(cells)
```

### probabilityMatrix

This function creates a squared probability matrix. Receives a list of cells, a criteria (`1` or `2`) and a radius (float). Returns a numpy matrix where `matrix[a][b]` has the probability of connection between node `a` and node `b`, given a criteria and a radius (equal for both nodes).

```
matrix = probabilityMatrix(cells, criteria, radius)
```

### probabilityMatrix2Rad

This function creates a squared probability matrix. Receives a list of cells and a criteria (`1` or `2`). Returns a numpy matrix where `matrix[a][b]` has the probability of connection between node `a` and node `b`, given a criteria and the random radius of each cell.

```
matrix = probabilityMatrix2Rad(cells, criteria)
```

### binaryMatrix

Create a binary matrix for a given probability matrix and criterion from `0.0` to `1.0`. Receives a probability numpy matrix and a float value as a threshold, from `0.0` to `1.0`. Returns a numpy matrix and a adjacency list with the thresholded data, just 1's and 0's.

```
binMatrix, adjList = binaryMatrix(matrix, criterion)
```

### binMatrixtoAdjList

This function converts a binary matrix to an adjacency list using a python dictionary. Receives the binary numpy matrix. Returns a python dictionary that contains lists corresponding to the adjacency list for each node.

```
adjList = binMatrixtoAdjList(matrix)
```

## [connectivityModel](connectivityModel.py)

### main

Main function, performs the topological  analysis and generates the reports for every analysis. Receives a python dictionary with the following keys and example values:

**animal**        : "Control 6 L1"    - Name of the animal to look for or to generate (if null animal) <br />
**slice**         : "2D"              - Number (1-4) and side (I, D) of the slide <br />
**section**       : "all"             - Name of the section, either '1', '2', '3' or 'all' <br />
**fixedRadius**   : True              - Boolean value to evaluate fixed or random radius values <br />
**criteria**      : 2                 - Criteria to evaluate, either 1 or 2 <br />
**criterion**     : 0.4285            - Criterion or probability to consider, always float <br />
**nullModeling**  : False             - Boolean value, True if generating a null model <br />
**noc**           : 302               - Number of cells to consider when null-modeling <br />
**nullArea**      : 14.0756           - Area of the nuclei when null-modeling <br />
**saveCSV**       : True              - Boolean value, True if want to save the CSV report files <br />
**saveFigs**      : True              - Boolean value, True if want to save the figs, PNG files <br />
**showFigs**      : False             - Boolean value, True if want to display the figs <br />

When saving reports, the function creates a folder tree like this:

```
savedData/[animal]/Criteria [criteria]/{criterion}/[slice]/[section]/
```

Inside saves the report data that was indicated. If nothing is saved, the folder is not created.

```
main(inData):
```

## [generatorScript](generatorScript.py)

This function generates the data for all the experimental and null animals. Disclaimer: may take a while to finish, couple of hours. Receives one argument from the console when the function is called, may be:

- `all` - To analyze experimental and null animals
- `exp` - To analyze only experimental, real animals
- `nul` - To analyze only null animals

The function by itself does not creates files, it only runs the [connectivityModel.py](connectivityModel.py) with all the possible configurations.

```
python generatorScript.py all
```

## [getData](getData.py)

### class Cell

`Cell` class, contains the characteristics of each cell. Coordinates, name, slice and radius.

```
cell = Cell(1024, 256, 8, 2, 128)
```

### extractCells

This function reads the data from `.csv` file and save its contents. Receives the location of the `.csv` file and the anatomic region to read (`1`, `2`, `3` or `all`). CSV file must have columns containing X and Y coordinates, the 'slice' (region). Returns a python list containing all the cells.

```
cells = extractCells(location, wichOnes)
```

## [networkPlots](networkPlots.py)

This file contains the functions that draws the different reconstructions of the nuclei. All of them loads in an matplotlib object the drawing, other function has to save it.

### drawEdges

This function puts on ax each valid edge in a given binary matrix. Receives a binary matrix, a list of cells and a matplotlib object ax. Does not return anything but draws all the edges in ax.

```
drawEdges(matrix, cells, ax)
```

### drawNodes

This function draws on ax each node. Receives a list of cells, a matplotlib ax object, and a boolean value to plot or not each name. Does not return anything but draws every node on the cells list as a scatter plot.

```
drawNodes(cells, ax, tags)
```

### markThisCells

This function marks a given list of nodes, here is marking the isolated cells with white on ax. Receives a list with the cells to draw, the main list of cells, color to use and matplotlib ax. Does not return anything but draws the given list of cells with the specified color.

```
markThisCells(toDraw, cells, color, ax)
```

### drawConnectedComponents

Draw with different colors each connected component. Receives a dictionary of connected components, a binary matrix, a list of cells and a matplotlib ax. Does not returns anything but prints every connected component with different colors.

```
drawConnectedComponents(ccomponents, matrix, cells, ax)
```

### drawDendriticFields

This function draws on ax the dendritic fields of a given list of cells. Receives a list of cells, a matplotlib ax object and boolean value to print a constant radius or not. Doesn't return anything but draws the dendritic field of each cell with different color per region.

```
drawDendriticFields(cells, ax, radConst)
```

## [nullModel](nullModel.py)

This file contains the functions to create a simulated set of cells inside of an ellipse that simulates the striatum.

### validPoint

Function to validate if a point at coordinate `x,y` is inside of an ellipse with center at `h,k` and minor and major diameters `rx`, `ry`. Receives coordinates `h`, `k`, the radius `rx` and `ry` and the coordinates `x`, `y`. Returns a boolean value, either is inside or not of the ellipse.

```
valid = validPoint(h, k, rx, ry, x, y)
```

### generateCells

This function creates a list of Cells. `total` is the total amount of cells to creates. It creates them inside of an ellipse with minor diameter of `rx` and mayor diameter of `ry`. Also, creates the radius of each cell at random or at constant value. Receives the number of cells to create, a boolean value to indicate random radius, and coordinates. Returns a list of null cells, just like the one we get when reading real values.

```
nullCells = generateCells(total, randRad, rx, ry)
```

### rMin

Auxiliary function to calculate the minor radius of an ellipse when knowing everything else. Receives the desired area of the resulting ellipse and the major radius. Returns the minor radius value.

```
minRadius = rMin(area, rMaxC)
```

### rMax

Auxiliary function to calculate the major radius of an ellipse when knowing everything else. Receives the desired area of the resulting ellipse and the minor radius. Returns the major radius value.

```
maxRadius = rMax(area, rMinC)
```

## [paths](paths.py)

### shortestPath

Implementation of Dijkstra's algorithm using a priority queue. Receives two arguments, adjacency binary `matrix` and starting node. Returns two numpy arrays, first indicates minimum path cost from `start` to each other node and the second array indicates the previous node to successfully reconstruct the shortest path.

```
dist, prev = shortestPath(matrix, start)
```

### reconstructPath

This function reconstruct the shortest path to get to any other node. Receives three arguments, the `path` from Dijkstra's algorithm, the `origin` node and the `target` node. Returns a list with the nodes to visit in order to get the minimum cost.

```
rec = reconstructPath(path, origin, target)
```

### brandeAlgorithmMat

Implementation of Brande's algorithm for betweenness centrality using a binary adjacency `matrix`. Check the paper [A Faster Algorithm for Betweenness Centrality, Ulrik Brandes](https://ucilnica.fri.uni-lj.si/pluginfile.php/1212/course/section/1199/Brandes%20-%20A%20faster%20algorithm%20for%20betweenness%20centrality%2C%202001.pdf)

```
C = brandeAlgorithmMat(matrix)
```

### brandeAlgorithm

Implementation of Brande's algorithm for betweenness centrality using an `adjacency` list. Check the paper [A Faster Algorithm for Betweenness Centrality, Ulrik Brandes](https://ucilnica.fri.uni-lj.si/pluginfile.php/1212/course/section/1199/Brandes%20-%20A%20faster%20algorithm%20for%20betweenness%20centrality%2C%202001.pdf)

```
C = brandeAlgorithm(adjList)
```

## [probabilityFunctions](probabilityFunctions.py)

### directUnion

Corresponding to the first criteria. Receives two parameters, `distance` between cells and the `radius` (same for both). Binary function, returns either `1` or `0`.

```
isTouching = directUnion(distance, radius)
```

### directUnion2Rad

Corresponding to the first criteria but with different radius. Receives two parameters, distance between cells and the radius of each one. Binary function, returns either `1` or `0`.

```
isTouching =  directUnion2Rad(distance, radiusA, radiusB)
```

### getDistance

This function calculates the distance between two cells using Pythagoras theorem. Receives two cell objects. Returns the euclidean distance between the given cells.

```
distance = getDistance(cellA, cellB)
```

### overlapArea

This function calculates the overlap area of two circles with same radius. Receives a `distance` between the cells and a `radius`. Returns the area of overlap between the two circles.

```
overlap = overlapArea(distance, radius)
```

### overlapArea2Rad

This function calculates the overlap area of two circles with different radius. Receives a distance between the cells and the radius for each cell. Returns the area of overlap between the two circles.

```
overlap = overlapArea2Rad(d, r, R)
```

### proportion

Calculates the proportion of overlap when considering same radius. Receives the `distance` and `radius` of the cells. Returns the proportion of overlap over the maximum possible overlap.

```
proportion = proportion(distance, radius):
```

### proportion2Rad

Calculates the proportion of overlap when considering two different radius. Receives the distance and radius of each cell. Returns the proportion of overlap over the maximum possible overlap.

```
proportion = proportion2Rad(distance, r, R)
```

### probability

The actual probability of connection between two cells of same radius. Receives the `distance` between the two cells and the `radius` (same for both). Returns the probability of connection.

```
probability = probability(distance, radius)
```

### probability2Rad

The actual probability of connection between two cells of different radius. Receives the distance between the two cells and the radius of each one. Returns the probability of connection.

```
probability = probability2Rad(distance, r, R)
```

## [summaryPlots](summaryPlots.py)

### makeGrpahics

This function creates the actual plot with error bars and saves the data plotted. Receive a matplotlib `ax`, `control` and `AVP` data (dictionary of lists), the `marker` and `name` for `.csv` file. Creates the plot on ax and saves 4 csv files with plotted data.

```
makeGrpahics(ax, control, avp, mark, csvName)
```

## darkPlot

This function sets the plots styles, dark mode as usual.

```
darkPlot()
```

### generatePlot

Function that makes the plots. Receives the data for the animal. Generates a plot, also 4 csv files with the numeric data plotted.

```
generatePlot(animals, sliceNum, sliceSide, section, fRad, criteria, criterions, nullM)
```

### main

Main function, generates the graphics and the `.csv` files with plotted data. Receives one argument by the console, either `nullModel` or `justExp` indicating if the null model must be plotted too. The function saves the plots and the `.csv` files with the numeric data.

```
python summaryPlots.py justExp
```
