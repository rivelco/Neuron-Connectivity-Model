import math
import random
from getData import Cell

# Function to validate if a point at coord x,y is inside of an ellipse
# with center at h,k and minor and major radius rx, ry
def validPoint(h, k, rx, ry, x, y):
    rx = rx/2
    ry = ry/2
    eq = ((x-h)**2)/(rx**2) + ((y-k)**2)/(ry**2)    # From the ellipse equation
    if eq <= 1:
        return True
    else:
        return False

# This function creates a list of Cells. total is the total amount of cells to creates
# It creates them inside of an ellipse with minor diameter of rx and mayor diameter of ry
# Also, creates the radius of each cell at random or at constant value
def generateCells(total, randRad, rx, ry):
    h = rx/2                                # Calculates the center of the ellipse, no negative coords
    k = ry/2                                # Calculates the center of the ellipse
    nullCells = []                          # List of null cells
    nullCells.append(Cell(0, 0, 0, 0, 0))   # Foo cell, at nullCells[0]
    for i in range(1, total):               # Iterates over the given range
        name = i                            # To get the name of each cell
        slice = 1                           # Number of slice
        if randRad:                         # True if we want random radius
            radius = random.randint(125, 150)   # Random radius
        else:
            radius = 125                        # Fixed value
        coordX = 0                          # Initial foo coords at x
        coordY = 0                          # Initial foo coords at y
        while not validPoint(h, k, rx, ry, coordX, coordY): # Find a valid coord
            coordX = random.randint(0, rx)                      # Generates at random the coords
            coordY = random.randint(0, ry)
        newCell = Cell(coordX, coordY, name, slice, radius) # When valid coord, the new cell is created
        nullCells.append(newCell)                           # Append that cell to the list
    return nullCells                        # Return the cells

def rMin(area, rMaxC):
    return area/(math.pi*rMaxC)

def rMax(area, rMinC):
    return area/(math.pi*rMinC)
