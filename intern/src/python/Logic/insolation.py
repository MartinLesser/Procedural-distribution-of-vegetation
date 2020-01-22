import math
import numpy as np

from intern.src.python.Core.constants import *
from intern.src.python.Data.image import Image
from intern.src.python.Data.sun import Sun


class Insolation:
    """
    The insolation class is used for calculating the amount of energy that each point on the terrain receives by
    sunlight during one day. First it is calculated which points receive light. Then the actual energy will be
    calculated at every point. This depends on the number of daylight hours a point receives light, the solar constant,
    atmospheric absorption, cloud reflection, atmospheric diffusion and ground reflection (albedo).
    At last the reflection of surrounding pixels will be added to the energy of a pixel.
    """

    def __init__(self, controller):
        self.controller = controller
        self.insolation_image = Image(size=self.controller.image_height_map.size)

    def calculate_raw_insolation(self, sun, x, y, map_size, pixel_size, heightmap_max_height, height_conversion):
        """
        Calculates if a given point on the terrain receives light at a given daylight hour. Atmospheric absorption etc.
        is not considered during this calculation.
        :param sun: Object of the sun class. Used for calculating from which direction the sun shines.
        :param x, y: Integer of the x and y position of the point on the terrain.
        :param map_size: Integer of the size of the terrain.
        :param pixel_size: Float. The size a pixel represents of the real terrain.
        :param heightmap_max_height: Integer. Maximal height of the terrain.
        :param height_conversion: Float. Conversion value of the height of the heightmap to calculate the real height.
        """
        uvw = sun.convert_to_uv_coordinates()  # transforms the polar coordinates of the sun to cartesian coordinates
        x_step = uvw[0]
        y_step = uvw[1]
        z_step = uvw[2]
        x_start_world_pos = x * pixel_size
        y_start_world_pos = y * pixel_size
        z_start_world_pos = self.controller.image_height_map.image[y][x] * height_conversion
        x_real_world_pos = x_start_world_pos  # current x position for walking along the direction vector
        y_real_world_pos = y_start_world_pos  # current y position for walking along the direction vector
        z_real_world_pos = z_start_world_pos  # current z position for walking along the direction vector
        t = 0  # used for the vector equation
        sun_beam_reaches_pixel = True
        map_x_y_boundary = map_size * pixel_size  # boundary of the map

        while 0 <= x_real_world_pos < map_x_y_boundary and 0 <= y_real_world_pos < map_x_y_boundary \
                and z_real_world_pos < heightmap_max_height:

            # this if statement decides how far the sun direction vector will be followed until a new
            # pixel in the pixel space will be reached. Only then a new height can be compared. This accelerates the
            # algorithm.
            if x_step != 0.0 or y_step != 0.0:
                if x_real_world_pos % pixel_size >= y_real_world_pos % pixel_size and x_step != 0:
                    t_step = (pixel_size - (x_real_world_pos % pixel_size)) / x_step
                else:
                    t_step = (pixel_size - (y_real_world_pos % pixel_size)) / y_step
            else:
                break  # sun stands in zenith so every pixel will receive light

            t_step = abs(t_step)
            t += t_step
            x_real_world_pos = x_start_world_pos + t * x_step
            y_real_world_pos = y_start_world_pos + t * y_step
            z_real_world_pos = z_start_world_pos + t * z_step
            x_pixel_pos = int(x_real_world_pos / pixel_size)
            y_pixel_pos = int(y_real_world_pos / pixel_size)

            if x_pixel_pos < 0 or y_pixel_pos < 0 or x_pixel_pos > map_size - 1 or y_pixel_pos > map_size - 1:
                break  # sun beam leaves the map boundary

            terrain_height = self.controller.image_height_map.image[y_pixel_pos][x_pixel_pos] * height_conversion
            line_height = z_real_world_pos
            if terrain_height > line_height:
                sun_beam_reaches_pixel = False
                break  # something blocks the light from the sun for that pixel
        if sun_beam_reaches_pixel:
            self.insolation_image.image[y][x] += SOLAR_CONSTANT_K_CALORIES_PER_HOUR  # * (map.pixel_size ** 2)

    def add_reflection_insolation(self, reflection_coefficient):
        """
        Adds the energy of the neighbours of a pixel and calculates the average. A fraction of this number will
        be added to the currently observed pixel.
        :param reflection_coefficient: Float. Fraction of the average energy of the neighbourspixels that the pixel
            will receive.
        """
        padded_insolation_image = np.pad(self.insolation_image.image, 1, 'edge')
        for y in range(1, self.controller.image_height_map.size + 1):
            print("Reflection: Row: " + str(y))
            for x in range(1, self.controller.image_height_map.size + 1):
                neighbor_insolation_sum = 0
                neighbor_insolation_sum += padded_insolation_image[y][x + 1]
                neighbor_insolation_sum += padded_insolation_image[y + 1][x + 1]
                neighbor_insolation_sum += padded_insolation_image[y + 1][x]
                neighbor_insolation_sum += padded_insolation_image[y + 1][x - 1]
                neighbor_insolation_sum += padded_insolation_image[y][x - 1]
                neighbor_insolation_sum += padded_insolation_image[y - 1][x - 1]
                neighbor_insolation_sum += padded_insolation_image[y - 1][x]
                neighbor_insolation_sum += padded_insolation_image[y - 1][x + 1]
                added_reflection_insolation = neighbor_insolation_sum / 8 * reflection_coefficient
                self.insolation_image.image[y - 1][x - 1] += added_reflection_insolation

    def calculate_actual_insolation(self, map, daylight_hours, sun_start_elevation, sun_start_azimuth,
                                    sun_max_elevation, reflection_coefficient):
        """
        Calculates the actual energy of each pixel based on the previously calculated raw energy. The atmosphere and
        reflection reduce the raw energy.
        :param map_name: String of the current map name.
        :param daylight_hours: Integer of the number of daylight hours.
        :param sun_start_elevation: Float of the start elevation of the sun.
        :param sun_start_azimuth: Float of the start azimuth of the sun.
        :param sun_max_elevation: Float of the maximal sun elevation (noon).
        :param reflection_coefficient: Float of the reflection coeficient. It states how much light of the neighbour
                pixel will be reflected.
        :return: insolation_image: Image of the calculated actual energy of each pixel.
        """
        self.calculate_insolation_for_daylight_hours(map, daylight_hours, sun_start_elevation, sun_start_azimuth,
                                                     sun_max_elevation)
        for y in range(self.controller.image_height_map.size):
            for x in range(self.controller.image_height_map.size):
                pixel_raw_insolation = self.insolation_image.image[y][x]
                cloud_reflection_loss = pixel_raw_insolation * map.biom.cloud_reflection / 100
                atmospheric_absorption_loss = pixel_raw_insolation * map.biom.atmospheric_absorption / 100
                atmospheric_diffusion_loss = pixel_raw_insolation * map.biom.atmospheric_diffusion / 100
                soil_id = self.controller.soil_ids_map.image[y][x]
                soil = self.controller.search_soil(soil_id)
                albedo = soil.albedo
                self.insolation_image.image[y][x] = (pixel_raw_insolation - cloud_reflection_loss -
                                                     atmospheric_absorption_loss -
                                                     atmospheric_diffusion_loss) * (1.0 - albedo)
        self.add_reflection_insolation(reflection_coefficient)
        return self.insolation_image

    def calculate_insolation_for_daylight_hours(self, map, daylight_hours, sun_start_elevation, sun_start_azimuth,
                                                sun_max_elevation):
        """
        Calculates the sun position for every day light hours. At each hour the raw energy for each pixel wil be
        calculated.
        :param map_name: String of the current map name.
        :param daylight_hours: Integer of the number of daylight hours.
        :param sun_start_elevation: Float of the start elevation of the sun.
        :param sun_start_azimuth: Float of the start azimuth of the sun.
        :param sun_max_elevation: Float of the maximal sun elevation (noon).
        """
        assert daylight_hours > 0, "Daylight hours must be at least one!"

        # elevation
        if daylight_hours == 1:
            elevation_per_hour = 0
        elif daylight_hours == 2:
            elevation_per_hour = sun_max_elevation - sun_start_elevation
        else:
            if daylight_hours % 2 == 1:
                elevation_per_hour = ((sun_max_elevation - sun_start_elevation) / math.ceil(
                    (daylight_hours - 2) / 2))  # the sun shall rise to 90 (or less) degrees till noon and then fall again
            else:
                elevation_per_hour = (sun_max_elevation - sun_start_elevation) / (daylight_hours / 2)

        # azimuth
        if daylight_hours == 1:
            azimuth_per_hour = 0
        elif daylight_hours == 2:
            azimuth_per_hour = 180 - 2 * sun_start_azimuth
        else:
            azimuth_per_hour = 180 / (daylight_hours - 1)  # the sun shall wander 180 degrees

        sun = Sun(elevation=sun_start_elevation, azimuth=sun_start_azimuth)

        for hour in range(daylight_hours):
            print("############ Hour: " + str(hour + 1) + " ############")
            print("Sun polar coordinates: Azimuth: " + str(round(sun.azimuth, 1)) + "° Elevation: " + str(
                round(sun.elevation, 1)) + "°")
            max_height = np.amax(self.controller.image_height_map.image) * map.height_conversion
            for y in range(self.controller.image_height_map.size):
                print("Raw Insolation: Row:" + str(y))
                for x in range(self.controller.image_height_map.size):
                    self.calculate_raw_insolation(sun, x, y, self.controller.image_height_map.size, map.pixel_size,
                                                  max_height, map.height_conversion)

            if daylight_hours % 2 == 1:
                if hour < int((daylight_hours / 2)):
                    sun.elevation += elevation_per_hour
                else:
                    sun.elevation -= elevation_per_hour
            else:
                if hour != daylight_hours / 2 - 1:
                    if hour < int((daylight_hours / 2)):
                        sun.elevation += elevation_per_hour
                    else:
                        sun.elevation -= elevation_per_hour
            sun.azimuth += azimuth_per_hour
