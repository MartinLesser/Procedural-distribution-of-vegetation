import unittest

from intern.src.python.Core.constants import *
from intern.src.python.Data.image import Image
from intern.src.python.Logic.insolation import Insolation


class TestImageClass(unittest.TestCase):
    # Test data was created with the help of https://www.geogebra.org/3d?lang=de
    def test_CalculateLineHeightTest1(self):
        # given
        point1 = [0.0, 0.0, 0.0]
        point2 = [5.0, 5.0, 3.0]
        x = 3.0
        y = 3.0
        expected_height = 1.8

        # when
        actual_height = Insolation.calculate_line_height(point1, point2, x, y)
        actual_height = round(actual_height, 2)

        # then
        self.assertEqual(expected_height, actual_height)

    def test_CalculateLineHeightTest2(self):
        # given
        point1 = [-4.15845, -2.84944, -1.26391]
        point2 = [7.20618, 2.30449, 2.61415]
        x = 1.1
        y = -0.47
        expected_height = 0.53

        # when
        actual_height = Insolation.calculate_line_height(point1, point2, x, y)
        actual_height = round(actual_height, 2)

        # then
        self.assertEqual(expected_height, actual_height)

    def test_CalculateLineHeightTest3(self):
        # given
        point1 = [4.58584, -4.76206, -2.19952]
        point2 = [-6.50204, 5.6101, 1.0]
        x = -8.75
        y = 7.71
        expected_height = 1.65

        # when
        actual_height = Insolation.calculate_line_height(point1, point2, x, y)
        actual_height = round(actual_height, 2)

        # then
        self.assertEqual(expected_height, actual_height)

    # This tests what happens when two points have the same x value
    def test_CalculateLineHeightSameX(self):
        # given
        point1 = [5., 5., 5.]
        point2 = [5., 2., 3.]
        x = 5.
        y = 3.5
        expected_height = 4.

        # when
        actual_height = Insolation.calculate_line_height(point1, point2, x, y)
        actual_height = round(actual_height, 2)

        # then
        self.assertEqual(expected_height, actual_height)

    # This tests what happens when two points have the same y value
    def test_CalculateLineHeightSameY(self):
        # given
        point1 = [5., 5., 5.]
        point2 = [1., 5., 3.]
        x = 3.
        y = 5.
        expected_height = 4.

        # when
        actual_height = Insolation.calculate_line_height(point1, point2, x, y)
        actual_height = round(actual_height, 2)

        # then
        self.assertEqual(expected_height, actual_height)

    # This tests what happens when two points have the same x and y values
    def test_CalculateLineHeightSameXandY(self):
        # given
        point1 = [5., 5., 5.]
        point2 = [5., 5., 3.]
        x = 5.
        y = 5.
        expected_height = 5.

        # when
        actual_height = Insolation.calculate_line_height(point1, point2, x, y)
        actual_height = round(actual_height, 2)

        # then
        self.assertEqual(expected_height, actual_height)

    # This test should result in a completely dark image because the heights of the height-map are all higher than
    # the height of the sun position. This test depends on the conversion of the height-map-value to the actual height.
    def test_CalculateInsolationDarkImage(self):
        # given
        image_size = 4
        input_image = Image(size=image_size, fill_color=100)
        insolation = Insolation(input_image)
        expected_image = Image(size=image_size, fill_color=0)  # completely dark
        sun_position = [2, 2, 10]

        # when
        insolation.calculate_insolation_cpu(sun_position)

        # then
        self.assertEqual(expected_image, insolation.insolation_image)

    # This test should result in uniformly bright image because the heights of the height-map are all lower than
    # the height of the sun position. Thus every pixel will receive sunlight/calories.
    # This test depends on the conversion of the height-map-value to the actual height.
    def test_CalculateInsolationWhiteImage(self):
        # given
        image_size = 4
        input_image = Image(size=image_size, fill_color=100)
        insolation = Insolation(input_image)
        expected_image = Image(size=image_size, fill_color=CAL_PER_HOUR_PER_PIXEL)  # every pixel receives calories
        sun_position = [2, 2, 200]

        # when
        insolation.calculate_insolation_cpu(sun_position)

        # then
        self.assertEqual(expected_image, insolation.insolation_image)

    def test_CalculateInsolationForDaylightHours(self):
        # given
        image_size = 10
        input_image = Image(size=image_size, fill_color=0)
        insolation = Insolation(input_image)
        daylight_hours = 7
        # every pixel receives calories per hour
        expected_image = Image(size=image_size, fill_color=CAL_PER_HOUR_PER_PIXEL*daylight_hours)

        # when
        insolation.calculate_insolation_for_daylight_hours(daylight_hours)

        # then
        self.assertEqual(expected_image, insolation.insolation_image)

