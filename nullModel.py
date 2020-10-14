import math
import random
from getData import Cell

# Function to validate if a point at coord x,y is inside of an ellipse
# with center at h,k and minor and major diameters rx, ry
# Receives coordinates h, k, the radius rx and ry and the coordinates x, y
# Returns a boolean value, either is inside or not of the ellipse
def validPoint(h, k, rx, ry, x, y):
    rx = rx/2           # Calculates the minor radius
    ry = ry/2           # Calculates the major radius
    eq = ((x-h)**2)/(rx**2) + ((y-k)**2)/(ry**2)    # From the ellipse equation
    if eq <= 1:
        return True     # Inside the ellipse
    else:
        return False    # Out of the ellipse

# This function creates a list of Cells. total is the total amount of cells to creates
# It creates them inside of an ellipse with minor diameter of rx and mayor diameter of ry
# Also, creates the radius of each cell at random or at constant value
# Receives the number of cells to create, a boolean value to indicate random radius, and coordinates
# Returns a list of null cells, just like the one we get when reading real values
def generateCells(total, randRad, rx, ry):
    h = rx/2                                # Calculates the center of the ellipse, no negative
    k = ry/2                                # Calculates the center of the ellipse
    nullCells = []                          # List of null cells
    nullCells.append(Cell(0, 0, 0, 0, 0))   # Foo cell, at nullCells[0]
    for i in range(1, total):               # Iterates over the given range
        name = i                            # To get the name of each cell
        slice = 1                           # Number of slice, default is 1, will improve this later
        if randRad:                         # True if we want random radius
            radius = random.randint(125, 150)   # Random radius
        else:
            radius = 125                        # Fixed value
        coordX = 0                          # Initial foo coords at x
        coordY = 0                          # Initial foo coords at y
        while not validPoint(h, k, rx, ry, coordX, coordY): # Find a valid coord
            coordX = random.randint(0, rx)                      # Generates at random the coords
            coordY = random.randint(0, ry)
        newCell = Cell(coordX, coordY, name, slice, radius) # When valid coord, creates a new cell
        nullCells.append(newCell)                           # Append that cell to the list
    return nullCells                        # Return the cells

# Auxiliary function to calculate the minor radius of an ellipse when knowing everything else
# Receives the desired area of the resulting ellipse and the major radius
# Returns the minor radius value
def rMin(area, rMaxC):
    return area*1000000/(math.pi*rMaxC)

# Auxiliary function to calculate the major radius of an ellipse when knowing everything else
# Receives the desired area of the resulting ellipse and the minor radius
# Returns the major radius value
def rMax(area, rMinC):
    return area*1000000/(math.pi*rMinC)
