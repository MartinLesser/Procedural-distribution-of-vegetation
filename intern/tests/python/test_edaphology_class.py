import unittest

from intern.src.python.Core.constants import *
from intern.src.python.Logic.edaphology import Edaphology


class TestEdaphologyClass(unittest.TestCase):

    def test_CalculateAngles(self):
        # given
        normal_map = [[[0, 0, -1], [1, 0, 0]], [[0, 1, 0], [0, 0, 1]]]
        expected = [[180, 90], [90, 0]]

        # when
        angles = Edaphology.calculate_angles(normal_map)

        # then
        self.assertEqual(expected, angles)

    def test_CalculateSoilDepth(self):
        # given
        angles = [[90, 0], [45, 60.0]]
        expected = [[0, SOIL_DEPTH_MAX], [SOIL_DEPTH_MAX/2, SOIL_DEPTH_MAX/3]]

        # when
        soil_depths = Edaphology.calculate_soil_depth(angles)

        # then
        self.assertEqual(expected, soil_depths)


if __name__ == '__main__':
    unittest.main()
