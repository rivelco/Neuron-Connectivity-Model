import Neuron_Connectivity_Model.probabilityFunctions as pf
from Neuron_Connectivity_Model import Cell
import math

class TestDirectUnion:
    def test_directNot(self):
        testcase = [500, 200]
        expected = False
        assert pf.directUnion(testcase[0], testcase[1]) == expected
    def test_directYes(self):
        testcase = [500, 260]
        expected = True
        assert pf.directUnion(testcase[0], testcase[1]) == expected
    def test_directJust(self):
        testcase = [500, 250]
        expected = True
        assert pf.directUnion(testcase[0], testcase[1]) == expected
    def test_direct2RNot(self):
        testcase = [500, 250, 200]
        expected = False
        assert pf.directUnion2Rad(testcase[0], testcase[1], testcase[2]) == expected
    def test_direct2RYes(self):
        testcase = [500, 250, 300]
        expected = True
        assert pf.directUnion2Rad(testcase[0], testcase[1], testcase[2]) == expected
    def test_direct2RJust(self):
        testcase = [500, 200, 300]
        expected = False
        assert pf.directUnion2Rad(testcase[0], testcase[1], testcase[2]) == expected

class TestDistance:
    def test_distanceSameX(self):
        cellA = Cell(0, 0, 0, 1, 200)
        cellB = Cell(0, 200, 1, 1, 100)
        testcase = [cellA, cellB]
        expected = 200
        assert pf.getDistance(testcase[0], testcase[1]) == expected
    def test_distanceSameY(self):
        cellA = Cell(100, 0, 0, 1, 200)
        cellB = Cell(200, 0, 1, 1, 100)
        testcase = [cellA, cellB]
        expected = 100
        assert pf.getDistance(testcase[0], testcase[1]) == expected
    def test_distanceDiffAll(self):
        cellA = Cell(100, 500, 0, 1, 200)
        cellB = Cell(400, 200, 1, 1, 100)
        testcase = [cellA, cellB]
        expected = math.sqrt(300**2 + 300**2)
        assert pf.getDistance(testcase[0], testcase[1]) == expected

class TestOverlap:
    def test_overlapSameRad0(self):
        testcase = [300, 200]
        expected = 18132.470159104392
        assert pf.overlapArea(testcase[0], testcase[1]) == expected
    def test_overlapSameRad1(self):
        testcase = [500, 300]
        expected = 22507.778063402147
        assert pf.overlapArea(testcase[0], testcase[1]) == expected
    def test_overlapSameRadBarely(self):
        testcase = [400, 201]
        expected = 53.426582300692644
        assert pf.overlapArea(testcase[0], testcase[1]) == expected
    def test_overlapSameRadNegative(self):
        testcase = [-400, -100]
        expected = 53.426582300692644
        assert pf.overlapArea(testcase[0], testcase[1]) == expected
    def test_overlapSameRadJust(self):
        testcase = [400, 200]
        expected = 0
        assert pf.overlapArea(testcase[0], testcase[1]) == expected
    def test_overlapSameRadNone(self):
        testcase = [400, 100]
        expected = None
        assert pf.overlapArea(testcase[0], testcase[1]) == expected
    def test_overlapSameRadTotal(self):
        testcase = [0, 300]
        expected = math.pi*300*300
        assert pf.overlapArea(testcase[0], testcase[1]) == expected
    def test_overlap2Rad0(self):
        testcase = [400, 258, 280]
        expected = 34014.054181254396
        assert pf.overlapArea2Rad(testcase[0], testcase[1], testcase[2]) == expected
    def test_overlap2Rad1(self):
        testcase = [550, 300, 402]
        expected = 44618.536008852316
        assert pf.overlapArea2Rad(testcase[0], testcase[1], testcase[2]) == expected
