import numpy as np

from intern.src.python.Core.constants import *
from intern.src.python.Data.image import Image


class Hydrology:
    """
    Calculates the available water at every point on the terrain. It uses the average rainfall and groundwater from
    the biom. The water absorption of the soil is also considered and the evaporation by the sun is calculated.
    """

    def __init__(self, controller):
        self.controller = controller

    def calculate_hydrology_map(self, map, edaphic_map, soil_ids_map, image_insolation_map, biom):
        """
        Calculates the available water at every point on the terrain. It uses the average rainfall and groundwater from
        the biom. The water absorption and depth of the soil is also considered and the evaporation by the sun is calculated.
        :param map: Object of the map class.
        :param edaphic_map: Object of the Edaphology class. Used to get the soil depth.
        :param soil_ids_map: Map of the soil ids. Used to get the water absorption of the soil.
        :param image_insolation_map: Result of the insolation calculation. Used for the calculation of the evaporation.
        :param biom: Object of the biom class. Used to get the groundwater and rainfall values.
        :return: hydrology_map: Result of water calculations.
        """
        hydrology_map = Image(size=edaphic_map.size, dtype=np.float)
        for y in range(edaphic_map.size):
            print("Calculating hydrology: Row: " + str(y))
            for x in range(edaphic_map.size):
                depth = edaphic_map.image[y][x]
                soil_id = soil_ids_map.image[y][x]
                soil = self.controller.search_soil(soil_id)
                if depth >= 100:
                    depth_coefficient = 1.0
                else:
                    depth_coefficient = depth / 100
                water_supply = (biom.groundwater + biom.avg_rainfall_per_day) * depth_coefficient * soil.water_absorption
                evaporated_water = (image_insolation_map.image[y][x] * K_CALORIES_NEEDED_TO_EVAPORATE_1_G_WATER) / 1000
                if evaporated_water > water_supply:
                    evaporated_water = water_supply
                water_supply -= evaporated_water
                hydrology_map.image[y][x] = water_supply  # * (map.pixel_size ** 2)
        return hydrology_map
