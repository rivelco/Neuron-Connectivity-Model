import math

# Corresponding to the first criteria
# Receives two parameters, distance between cells and the radius (same for both)
# Binary function, returns either 1 or 0
def directUnion(distance, radius):
    # Checks if the dendritic fields may touch each other
    isTouching = distance < 2*radius
    if isTouching:
        return 1    # If they are, the function returns 1
    else:
        return 0    # If not, the function returns 0

# Corresponding to the first criteria but with different radius
# Receives two parameters, distance between cells and the radius of each one
# Binary function, returns either 1 or 0
def directUnion2Rad(distance, radiusA, radiusB):
    # Checks if the dendritic fields may touch each other
    isTouching = distance < radiusA + radiusB
    if isTouching:
        return 1    # If they are, the function returns 1
    else:
        return 0    # If not, the function returns 0

# This function calculates the distance between two cells using Pythagoras theorem
# Receives two cell objects
# Returns the euclidean distance between the given cells
def getDistance(cellA, cellB):
    dx = abs(cellA.x - cellB.x)                 # Distance on x
    dy = abs(cellA.y - cellB.y)                 # Distance on y
    distance = math.sqrt((dx**2) + (dy**2))     # Calculates final distance using Pythagoras theorem
    return distance                             # Returns that

# This function calculates the overlap area of two circles with same radius
# Receives a distance between the cells and a radius
# Returns the area of overlap between the two circles
def overlapArea(distance, radius):
    distance = abs(distance)    # Use only the absolute value of distance
    radius = abs(radius)        # Only positive radius sizes
    if radius*2 < distance:     # If they does not even touch
        return 0                    # returns 0
    arg1 = 2*radius*radius*math.acos(distance/(2*radius))
    arg2 = distance/2 * math.sqrt((4*radius*radius) - (distance*distance))
    return  arg1 - arg2         # Calculates the area in pieces just for style reasons

# This function calculates the overlap area of two circles with different radius
# Receives a distance between the cells and the radius for each cell
# Returns the area of overlap between the two circles
def overlapArea2Rad(d, r, R):
    d = abs(d)              # Only working with positive values
    r = abs(r)              # Only working with positive values
    R = abs(R)              # Only working with positive values
    temp = max(r, R)        # Re-order the values to have the minor value on r
    temp2 = min(r, R)
    r = temp2
    R = temp
    if r+R <= d:            # If they doesn't even touch then return 0
        return 0
    if d <= R - r:          # If the distance allows one circle to be totally inside the other
        return math.pi*r*r      # Then return the area of the smallest circle
    arg1 = r**2*math.acos((d**2+r**2-R**2)/(2*d*r)) + R**2*math.acos((d**2+R**2-r**2)/(2*d*R))
    arg2 = (1/2)*math.sqrt((-d+r+R)*(d+r-R)*(d-r+R)*(d+r+R))
    return arg1 - arg2      # Calculates the area in pieces just for style reasons

# Calculates the proportion of overlap when considering same radius
# Receives the distance and radius of the cells
# Returns the proportion of overlap over the maximum possible overlap
def proportion(distance, radius):
    return overlapArea(distance, radius)/overlapArea(0, radius)

# Calculates the proportion of overlap when considering two different radius
# Receives the distance and radius of each cell
# Returns the proportion of overlap over the maximum possible overlap
def proportion2Rad(distance, r, R):
    return overlapArea2Rad(distance, r, R)/overlapArea2Rad(0, r, R)

# Sigmoid function, not in use but keeping it here just in case...
def sigmoid(x):
    return 1/(1+math.exp(-x))

# The initial proposal probability of connection between two cells at distance d and same radius
# DISCLAIMER: deprecated but keeping it here just for historical reasons
def probability_deprec(distance, radius):
    if distance > 2*radius:     # If their dendritic fields would never touch
        return 0                    # arbitrary probability of 0
    if distance <= radius:      # If they touch beyond somas
        return 1                    # arbitrary probability of 1
    # On every other case, we return an adjusted probability
    return sigmoid(proportion(distance, radius)) + (1 - sigmoid(proportion(radius, radius)))

# The actual probability of connection between two cells of same radius
# Receives the distance between the two cells and the radius (same for both)
# Returns the probability of connection
def probability(distance, radius):
    distance = abs(distance)        # Working only with positive values
    radius = abs(radius)            # Working only with positive values
    if radius == 0:                 # If the radius is 0 then we return 0
        return 0
    return proportion(distance, radius)     # The probability is the proportion

# The actual probability of connection between two cells of different radius
# Receives the distance between the two cells and the radius of each one
# Returns the probability of connection
# DISCLAIMER: Deprecated but keeping it here for historical reasons
def probability2Rad_deprec(distance, r, R):
    minRad = min(abs(r), abs(R))      # Orders the input values
    maxRad = max(abs(r), abs(R))      # So r has the smallest value
    if distance > minRad + maxRad:    # If the cells does not even touch
        return 0                            # The probability of connection is 0
    if distance <= maxRad:            # If one cell is contained inside the other
        return 1                            # The probability of connection is total
    return sigmoid(proportion2Rad(distance, r, R)) + (1 - sigmoid(proportion2Rad(max(r,R), r, R)))

# The actual probability of connection between two cells of different radius
# Receives the distance between the two cells and the radius of each one
# Returns the probability of connection
def probability2Rad(distance, r, R):
    distance = abs(distance)        # Working only with positive values
    r = abs(r)                      # Working only with positive values
    R = abs(R)                      # Working only with positive values
    if r == 0 or R == 0:            # If the radius is 0 then we return 0
        return 0
    return proportion2Rad(distance, r, R)   # The probability is the proportion
