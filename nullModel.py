import math
import random
from getData import Cell

def validPoint(h, k, rx, ry, x, y):
    rx = rx/2
    ry = ry/2
    eq = ((x-h)**2)/(rx**2) + ((y-k)**2)/(ry**2)
    if eq <= 1:
        return True
    else:
        return False

def rMin(area, rMaxC):
    return area/(math.pi*rMaxC)

def rMax(area, rMinC):
    return area/(math.pi*rMinC)

def generateCells(total, h, k, rx, ry):
    nullCells = []
    nullCells.append(Cell(0, 0, 0, 0, 0))   # Foo cell, at cells[0]
    print('Generando celulas...')
    for i in range(1, total):
        name = i
        slice = 1
        radius = random.randint(125, 150)
        coordX = 0
        coordY = 0
        while validPoint(h, k, rx, ry, coordX, coordY) == False:
            coordX = random.randint(0, 4500)
            coordY = random.randint(0, 5000)
        newCell = Cell(coordX, coordY, name, slice, radius)
        nullCells.append(newCell)
    return nullCells
