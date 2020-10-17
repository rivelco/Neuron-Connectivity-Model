import csv
import math
import random
#import numpy as np

# Cell class, contains the characteristics of each cell
class Cell:
    def __init__(self, x, y, name, slice, radius):  # Constructor, coords, name, slice and radius
        self.x = int(x)
        self.y = int(y)
        self.name = int(name)
        self.slice = int(slice)
        self.radius = int(radius)

# This function reads the data from csv file and save its contents
# Receives the location of the csv file and the anatomic region to read ('1', '2', '3' or 'all')
# CSV file must have columns containing X and Y coordinates, the 'slice' (region)
# Returns a python list containing all the cells
def extractCells(location, wichOnes):
    cells = []                          # Final list
    numOfCell = 0                       # Used to know the total amount of desired cells
    maxY = 0                            # Max value on y axis, because ImageJ get this inverted
    cells.append(Cell(0, 0, 0, 0, 0))   # Foo cell, at cells[0]
    with open(location) as file:        # Open the file at given location
        reader = csv.DictReader(file)   # Starts a reader on dict form for csv
        for row in reader:              # Reads out each row
            if row['Slice'] == wichOnes or wichOnes == 'all':   # Select the desired section
                numOfCell += 1                                  # Count that cell
                radius = random.randint(125, 150)               # Choose a random radius value
                cell = Cell(row['X'], row['Y'], numOfCell, row['Slice'], radius) # Creates a cell
                cells.append(cell)                              # Add that new cell to list
            if int(row['Y']) > maxY:                            # Select the max value for y
                maxY = int(row['Y'])
    for cell in cells:                  # Iterate over all cells
        cell.y = abs(cell.y - maxY)         # Invert the y axis
    return cells                        # Returns the final list
