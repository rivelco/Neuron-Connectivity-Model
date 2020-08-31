import math

# Corresponding to the first criteria
# Binary function, returns either 1 or 0
# Receives two parameters, distance between cells and the radious of each one
def directUnion(distance, radius):
    # Checks if the dendritic fields may touch each other
    isTouching = distance < 2*radius
    if isTouching:
        return 1    # If they are, the function returns 1
    else:
        return 0    # If not, the function returns 0

def directUnion2Rad(distance, radiusA, radiusB):
    # Checks if the dendritic fields may touch each other
    isTouching = distance < radiusA + radiusB
    if isTouching:
        return 1    # If they are, the function returns 1
    else:
        return 0    # If not, the function returns 0

# This function calculates the distance between two cells using Pythagoras theorem
def getDistance(cellA, cellB):
    dx = abs(cellA.x - cellB.x)         # Distance on x
    dy = abs(cellA.y - cellB.y)         # Distance on y
    distance = math.sqrt((dx**2) + (dy**2)) # Calculates final distance
    return distance # Returns that

# This function calculates the overlap area of two circles or radius 'radius'
def overlapArea(distance, radius):
    distance = abs(distance)
    radius = abs(radius)
    if radius*2 < distance:
        return 0
    return 2*radius*radius*math.acos(distance/(2*radius)) - distance/2 * math.sqrt((4*radius*radius) - (distance*distance))

def overlapArea2Rad(d, r, R):
    d = abs(d)
    r = abs(r)
    R = abs(R)
    temp = max(r, R)
    temp2 = min(r, R)
    r = temp2
    R = temp
    if r+R <= d:
        return 0
    if d <= R - r:
        return math.pi*r*r
    arg1 = r**2*math.acos((d**2+r**2-R**2)/(2*d*r)) + R**2*math.acos((d**2+R**2-r**2)/(2*d*R))
    arg2 = (1/2)*math.sqrt((-d+r+R)*(d+r-R)*(d-r+R)*(d+r+R))
    return arg1 - arg2

# This function calculates the ptoportion between what is overlapped and the maximum
def proportion_deprec(distance, radius):
    return overlapArea(distance, radius)/overlapArea(radius, radius)

def proportion(distance, radius):
    return overlapArea(distance, radius)/overlapArea(0, radius)

def proportion2Rad_deprec(distance, r, R):
    return overlapArea2Rad(distance, r, R)/overlapArea2Rad(max(r,R), r, R)

def proportion2Rad(distance, r, R):
    return overlapArea2Rad(distance, r, R)/overlapArea2Rad(0, r, R)

# Sigmoid function
def sigmoid(x):
    return 1/(1+math.exp(-x))

# The proposal probability of connection between two cells at distance d and same radius
def probability_deprec(distance, radius):
    if distance > 2*radius:     # If their dendritic fields would never touch
        return 0                    # arbitrary probability of 0
    if distance <= radius:      # If they touch beyond somas
        return 1                    # arbitrary probability of 1
    # On every other case, whe return an adjusted probability
    return sigmoid(proportion(distance, radius)) + (1 - sigmoid(proportion(radius, radius)))

def probability(distance, radius):
    distance = abs(distance)
    radius = abs(radius)
    if radius == 0:
        return 0
    return proportion(distance, radius)

def probability2Rad_deprec(distance, r, R):
    minRad = min(r, R)
    maxRad = max(r, R)
    if distance > minRad + maxRad:
        return 0
    if distance <= maxRad:
        return 1
    return sigmoid(proportion2Rad(distance, r, R)) + (1 - sigmoid(proportion2Rad(max(r,R), r, R)))

def probability2Rad(distance, r, R):
    distance = abs(distance)
    r = abs(r)
    R = abs(R)
    if r == 0 or R == 0:
        return 0
    return proportion2Rad(distance, r, R)

# Same as 'probability' but without adjust
def probWOAdjust(distance, radius):
    if distance > 2*radius:
        return 0
    if distance <= radius:
        return 1
    return sigmoid(proportion(distance, radius))

if __name__ == "__main__":
    res = overlapArea2Rad(0, 150, 200)
    #print(math.acos(-0.98))
    print(res)
    #print(math.pi*300*300)
