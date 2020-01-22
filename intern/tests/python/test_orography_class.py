import unittest
from intern.src.python.Logic.orography import Orography


class TestOrographyClass(unittest.TestCase):

    def test_CalculateNormal(self):
        # given
        vector1 = [0, 0, 0]
        vector2 = [4, 5, 0]
        vector3 = [3, 2, 0]
        expected = [0, 0, -7]

        # when
        normal = Orography.calculate_normal(vector1, vector2, vector3)

        # then
        self.assertEqual(normal, expected)

    def test_CalculateNormalMap(self):
        # given
        array = [[[0, 0, 5], [1, 0, 5]], [[0, 1, 5], [1, 1, 5]]]
        expected = [[[0.0, 0.0, 1.0], [0.0, 0.0, 1.0]], [[0.0, 0.0, 1.0], [0.0, 0.0, 1.0]]]

        # when
        normal_map = Orography.calculate_normal_map(array)

        # then
        self.assertEqual(expected, normal_map)

    def test_Normalize(self):
        # given
        vector = [3.0, 1.0, 2.0]
        expected = [0.802, 0.267, 0.535]

        # when
        result = Orography.normalize(vector)
        result = [round(value, 3) for value in result]

        # then
        self.assertEqual(expected, result)


if __name__ == '__main__':
    unittest.main()
