import yaml


class Map:
    def __init__(self, name, biom, height_map_path, texture_map_path, height_conversion, max_soil_depth, pixel_size):
        self.name = name
        self.biom = biom
        self.height_map_path = height_map_path
        self.texture_map_path = texture_map_path
        self.height_conversion = height_conversion  # The factor to convert a height value of the height-map to the actual height
        self.max_soil_depth = max_soil_depth  # in cm, states the maximal depth the ground can have when it has no tilt
        self.pixel_size = pixel_size  # the size that a pixel covers of the real map in m

    def save_map(self):
        data = {self.name: {
            'biom': self.biom,
            'height_map_path': self.height_map_path,
            'texture_map_path': self.texture_map_path,
            'height_conversion': self.height_conversion,
            'max_soil_depth': self.max_soil_depth,
            'pixel_size': self.pixel_size,
            }
        }

        with open('resources/data/maps.yml', 'a') as outfile:
            yaml.dump(data, outfile, default_flow_style=False)
