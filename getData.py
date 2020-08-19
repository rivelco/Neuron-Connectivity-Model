import csv
import math
import random
#import numpy as np

class Cell:                 # Cell object
    def __init__(self, x, y, name, slice, radius):  # Constructor, coords, name and slice
        self.x = int(x)
        self.y = int(y)
        self.name = int(name)
        self.slice = int(slice)
        self.radius = int(radius)

def extractCells(location, wichOnes): # Returns a dict with cells (Cell class)
    cells = []                          # Final dictionary
    numOfCell = 0
    maxY = 0
    cells.append(Cell(0, 0, 0, 0, 0)) # Foo cell, at cells[0]

    with open(location) as file:        # Open the file at given location
        reader = csv.DictReader(file)   # Starts a reader on dict form for csv
        for row in reader:              # Reads out each fow
            if row['Slice'] == wichOnes or wichOnes == 'all':
                numOfCell += 1
                radius = random.randint(125, 150)
                cell = Cell(row['X'], row['Y'], numOfCell, int(row['Slice']), radius)
                cells.append(cell)
                #cells[str(numOfCell)] = cell      # Adds that instance at dict with key 'N' NOTE that is a str
            if int(row['Y']) > maxY:
                maxY = int(row['Y'])
    for cell in cells:
        cell.y = abs(cell.y - maxY)
    return cells        # Returns the final dict
