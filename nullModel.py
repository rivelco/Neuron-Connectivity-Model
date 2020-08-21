import math
import random

def validPoint(h, k, rx, ry, x, y):
    eq = ((x-h)**2)/(rx**2) + ((y-k)**2)/(ry**2)
    if eq <= 1:
        return True
    else:
        return False

def rMin(area, rMaxC):
    return area/(math.pi*rMaxC)

def rMax(area, rMinC):
    return area/(math.pi*rMinC)
