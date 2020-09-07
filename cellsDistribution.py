import numpy as np

def distribution1D(cells, cellsDic, axis):
    histogram = np.empty(len(cells))
    for i, cell in enumerate(cells):
        if axis == 'x':
            histogram[i] = cellsDic[cell].x
        elif acis == 'y':
            histogram[i] = cellsDic[cell].y
    return histogram
