import Neuron_Connectivity_Model.connectionMatrix as cm
from Neuron_Connectivity_Model import Cell
import math
import numpy as np

class TestBinMatrixToAdjList:
    def test_directNot(self):
        mat = [[1, 1, 1, 1, 1],
               [1, 0, 0, 0, 0],
               [1, 0, 1, 0, 0],
               [1, 0, 0, 1, 0],
               [1, 0, 0, 0, 1]]
        testcase = np.array(mat)
        expected = {0: [1, 2, 3, 4], 1: [0], 2: [0], 3: [0], 4: [0]}
        assert cm.binMatrixtoAdjList(testcase) == expected
    def test_directYes(self):
        mat = [[1, 1, 1, 1, 1],
               [1, 1, 1, 1, 0],
               [1, 1, 1, 0, 1],
               [1, 1, 0, 1, 0],
               [1, 0, 1, 0, 1]]
        testcase = np.array(mat)
        expected = {0: [1, 2, 3, 4], 1: [0, 2, 3], 2: [0, 1, 4], 3: [0, 1], 4: [0, 2]}
        assert cm.binMatrixtoAdjList(testcase) == expected
    def test_directJust(self):
        mat = [[1, 1, 1, 0, 1, 0],
               [0, 1, 0, 1, 0, 0],
               [0, 0, 1, 0, 0, 0],
               [0, 0, 0, 1, 0, 0],
               [0, 0, 0, 0, 1, 0],
               [1, 0, 0, 0, 0, 1]]
        testcase = np.array(mat)
        expected = {0: [1, 2, 4], 1: [3], 2: [], 3: [], 4: [], 5: [0]}
        assert cm.binMatrixtoAdjList(testcase) == expected
    def test_direct2RNot(self):
        mat = [[1, 1, 1, 0, 1, 1],
               [1, 1, 0, 1, 0, 0],
               [1, 0, 1, 0, 0, 0],
               [0, 1, 0, 1, 0, 0],
               [1, 0, 0, 0, 1, 0],
               [1, 0, 0, 0, 0, 1]]
        testcase = np.array(mat)
        expected = {0: [1, 2, 4, 5], 1: [0, 3], 2: [0], 3: [1], 4: [0], 5: [0]}
        assert cm.binMatrixtoAdjList(testcase) == expected
    def test_direct2RYes(self):
        mat = [[1, 0, 1, 0, 0, 0, 0],
               [0, 1, 1, 0, 0, 0, 0],
               [0, 0, 1, 1, 1, 0, 0],
               [0, 0, 0, 1, 0, 1, 0],
               [0, 0, 0, 0, 1, 1, 0],
               [0, 0, 0, 0, 0, 1, 1],
               [0, 0, 0, 0, 0, 0, 1]]
        testcase = np.array(mat)
        expected = {0: [2], 1: [2], 2: [3, 4], 3: [5], 4: [5], 5: [6], 6: []}
        assert cm.binMatrixtoAdjList(testcase) == expected
