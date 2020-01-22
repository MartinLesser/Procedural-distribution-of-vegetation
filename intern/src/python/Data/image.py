import imageio
import numpy as np
import os


class Image:
    """
    The image class is used as a container of the loaded and calculated maps. The image can be loaded and saved.
    """

    def __init__(self, size=None, fill_color=None, dtype=None):
        if size is None:
            size = 1
        self.size = size
        if fill_color is None:
            fill_color = 0
        self.fill_color = fill_color
        if dtype is None:
            dtype = np.uint16
        self.dtype = dtype
        self.image = np.full(shape=(size, size), fill_value=fill_color, dtype=self.dtype)
        self.is_image_loaded = False

    def __eq__(self, other):
        assert self.size == other.size, "The sizes of the images are not equal!"
        return (self.image == other.image).all()

    def load_image(self, path):
        self.image = imageio.imread(path)
        self.size = self.image.shape[0]
        # float values need special care. they were stored as integers and will be transformed back to float values.
        if self.dtype == np.float:
            new_image = np.full(shape=(self.size, self.size), fill_value=0.0, dtype=np.float)
            for y in range(self.size):
                for x in range(self.size):
                    new_image[x][y] = self.image[x][y] / 1000.0
            self.image = new_image
        self.is_image_loaded = True

    def save_image(self, path):
        if not os.path.exists(os.path.dirname(path)):
            os.makedirs(os.path.dirname(path))
        # float values need special care. they will be transformed to integers.
        if self.dtype == np.float:
            image = np.zeros(shape=(self.size, self.size), dtype=np.uint16)
            for y in range(self.size):
                for x in range(self.size):
                    image[x][y] = self.image[x][y] * 1000
            imageio.imwrite(path, image)
        else:
            imageio.imwrite(path, self.image)

    def filter_unique_numbers_from_2d_array(self):
        list_of_unique_numbers = []
        for row in self.image:
            for number in row:
                if number not in list_of_unique_numbers:
                    list_of_unique_numbers.append(number)
        print(list_of_unique_numbers)

    def transform_image_to_valid_soils(self, transformation_list):
        for y in range(self.size):
            for x in range(self.size):
                self.image[x][y] = transformation_list[self.image[x][y]]
