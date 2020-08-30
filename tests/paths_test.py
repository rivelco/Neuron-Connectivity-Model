from Neuron_Connectivity_Model.paths import brandeAlgorithmMat
from Neuron_Connectivity_Model.paths import brandeAlgorithm
import numpy as np

class TestbrandesAlgorithmMatrix():
    def test_brandesTest0(self):
        matrix = [[1, 1, 1, 1, 1],
                    [1, 0, 0, 0, 0],
                    [1, 0, 1, 0, 0],
                    [1, 0, 0, 1, 0],
                    [1, 0, 0, 0, 1]]
        testcase = np.array(matrix)
        expected = [12,  0,  0,  0,  0]
        assert brandeAlgorithmMat(testcase).tolist() == expected
    def test_brandesTest1(self):
        matrix = [[1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 0],
                    [1, 1, 1, 0, 1],
                    [1, 1, 0, 1, 0],
                    [1, 0, 1, 0, 1]]
        testcase = np.array(matrix)
        expected = [4, 1, 1, 0, 0]
        assert brandeAlgorithmMat(testcase).tolist() == expected
    def test_brandesTest2(self):
        matrix = [[1, 1, 1, 0, 1, 0],
                    [0, 1, 0, 1, 0, 0],
                    [0, 0, 1, 0, 0, 0],
                    [0, 0, 0, 1, 0, 0],
                    [0, 0, 0, 0, 1, 0],
                    [1, 0, 0, 0, 0, 1]]
        testcase = np.array(matrix)
        expected = [4, 2, 0, 0, 0, 0]
        assert brandeAlgorithmMat(testcase).tolist() == expected
    def test_brandesTest3(self):
        matrix = [[1, 1, 1, 0, 1, 1],
                    [1, 1, 0, 1, 0, 0],
                    [1, 0, 1, 0, 0, 0],
                    [0, 1, 0, 1, 0, 0],
                    [1, 0, 0, 0, 1, 0],
                    [1, 0, 0, 0, 0, 1]]
        testcase = np.array(matrix)
        expected = [18,  8,  0,  0,  0,  0]
        assert brandeAlgorithmMat(testcase).tolist() == expected
    def test_brandesTest4(self):
        matrix = [[1, 0, 1, 0, 0, 0, 0],
                    [0, 1, 1, 0, 0, 0, 0],
                    [0, 0, 1, 1, 1, 0, 0],
                    [0, 0, 0, 1, 0, 1, 0],
                    [0, 0, 0, 0, 1, 1, 0],
                    [0, 0, 0, 0, 0, 1, 1],
                    [0, 0, 0, 0, 0, 0, 1]]
        testcase = np.array(matrix)
        expected = [0, 0, 8, 3, 3, 5, 0]
        assert brandeAlgorithmMat(testcase).tolist() == expected

class TestbrandesAlgorithm():
    def test_brandesAdj0(self):
        testcase = {0: [1, 2, 3, 4], 1: [0], 2: [0], 3: [0], 4: [0]}
        expected = [12,  0,  0,  0,  0]
        assert brandeAlgorithm(testcase).tolist() == expected
    def test_brandesAdj1(self):
        testcase = {0: [1, 2, 3, 4], 1: [0, 2, 3], 2: [0, 1, 4], 3: [0, 1], 4: [0, 2]}
        expected = [4, 1, 1, 0, 0]
        assert brandeAlgorithm(testcase).tolist() == expected
    def test_brandesAdj2(self):
        testcase = {0: [1, 2, 4], 1: [3], 2: [], 3: [], 4: [], 5: [0]}
        expected = [4, 2, 0, 0, 0, 0]
        assert brandeAlgorithm(testcase).tolist() == expected
    def test_brandesAdj3(self):
        testcase = {0: [1, 2, 4, 5], 1: [0, 3], 2: [0], 3: [1], 4: [0], 5: [0]}
        expected = [18,  8,  0,  0,  0,  0]
        assert brandeAlgorithm(testcase).tolist() == expected
    def test_brandesAdj4(self):
        testcase = {0: [2], 1: [2], 2: [3, 4], 3: [5], 4: [5], 5: [6], 6: []}
        expected = [0, 0, 8, 3, 3, 5, 0]
        assert brandeAlgorithm(testcase).tolist() == expected
