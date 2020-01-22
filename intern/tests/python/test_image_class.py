import unittest
from intern.src.python.Data.image import Image


class TestImageClass(unittest.TestCase):

    def test_ConstructorShouldInitializeCorrectly(self):
        # given
        fill_color = 10

        # when
        image = Image(size=2, fill_color=fill_color)

        # then
        self.assertEqual(fill_color, image.image[0][0])
        self.assertEqual(fill_color, image.image[0][1])
        self.assertEqual(fill_color, image.image[1][0])
        self.assertEqual(fill_color, image.image[1][1])


if __name__ == '__main__':
    unittest.main()
