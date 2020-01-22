import unittest

from intern.src.python.Data.sun import Sun


class TestSunClass(unittest.TestCase):

    def test_ConversionToUVCoordinates1(self):
        # given
        sun = Sun(elevation=0, azimuth=0)
        expected = (1, 0)

        # when
        coord = sun.convert_to_uv_coordinates()

        # then
        self.assertEqual(expected[0], round(coord[0], 2))
        self.assertEqual(expected[1], round(coord[1], 2))

    def test_ConversionToUVCoordinates2(self):
        # given
        sun = Sun(elevation=0, azimuth=90)
        expected = (0, 1)

        # when
        coord = sun.convert_to_uv_coordinates()

        # then
        self.assertEqual(expected[0], round(coord[0], 2))
        self.assertEqual(expected[1], round(coord[1], 2))

    def test_ConversionToUVCoordinates3(self):
        # given
        sun = Sun(elevation=45, azimuth=45)
        expected = (0.5, 0.5)

        # when
        coord = sun.convert_to_uv_coordinates()

        # then
        self.assertEqual(expected[0], round(coord[0], 2))
        self.assertEqual(expected[1], round(coord[1], 2))

    def test_ConversionToUVCoordinates4(self):
        # given
        sun = Sun(elevation=90, azimuth=225)
        expected = (0, 0)

        # when
        coord = sun.convert_to_uv_coordinates()

        # then
        self.assertEqual(expected[0], round(coord[0], 2))
        self.assertEqual(expected[1], round(coord[1], 2))

    def test_ConversionToMapCoordinates1(self):
        # given
        sun = Sun(elevation=45, azimuth=45)
        map_size = 10
        expected = (6, 2, 9)

        # when
        coord = sun.convert_to_map_coordinates(map_size)

        # then
        self.assertEqual(expected[0], coord[0])
        self.assertEqual(expected[1], coord[1])
        self.assertEqual(expected[2], coord[2])

    def test_ConversionToMapCoordinates2(self):
        # given
        sun = Sun(elevation=0, azimuth=0)
        map_size = 10
        expected = (9, 4, 0)

        # when
        coord = sun.convert_to_map_coordinates(map_size)

        # then
        self.assertEqual(expected[0], coord[0])
        self.assertEqual(expected[1], coord[1])
        self.assertEqual(expected[2], coord[2])

    def test_ConversionToMapCoordinates3(self):
        # given
        sun = Sun(elevation=89, azimuth=0)
        map_size = 10
        expected = (4, 4, 572)

        # when
        coord = sun.convert_to_map_coordinates(map_size)

        # then
        self.assertEqual(expected[0], coord[0])
        self.assertEqual(expected[1], coord[1])


if __name__ == '__main__':
    unittest.main()
