import numpy as np
from pathlib import Path
import pickle
import os
import yaml

from intern.src.python.Data.biom import Biom
from intern.src.python.Data.image import Image
from intern.src.python.Data.map import Map
from intern.src.python.Data.soil import Soil
from intern.src.python.Data.vegetation import Vegetation
from intern.src.python.Gui.main_window import MainWindow
from intern.src.python.Logic.edaphology import Edaphology
from intern.src.python.Logic.hydrology import Hydrology
from intern.src.python.Logic.insolation import Insolation
from intern.src.python.Logic.probabilities import Probabilities
from intern.src.python.Logic.orography import Orography


class Controller:
    """
    The Controller class controls the flow of the application. It starts the UI, loads all data and controlls
    the calculation of the maps (insolation, orography, edaphology and hydrology) by starting the other logic
    classes. It also starts the calculation of the probability map. All results will be saved and can be loaded
    later on.
    """

    def __init__(self):
        self.image_height_map = None
        self.soil_ids_map = None
        self.image_insolation_map = None
        self.image_orographic_map = None
        self.image_edaphic_map = None
        self.image_water_map = None
        self.image_probabilities = None
        self.bioms = {}
        self.load_bioms()
        self.soils = {}
        self.load_soils()
        self.vegetations = {}
        self.load_vegetations()
        self.maps = {}
        self.load_maps()
        self.main_window = MainWindow(self)

    def load_height_and_soil_map(self, map_name):
        """
        It creates two images and loads the height- and soil- map into it.
        :param map_name: String of the map name. It is used to find the images on disk.
        """
        map = self.maps[map_name]
        self.image_height_map = Image()
        self.image_height_map.load_image(map.height_map_path)
        self.soil_ids_map = Image()
        self.soil_ids_map.load_image(map.texture_map_path)
        # self.transform_and_save_soil_id_map(map.texture_map_path)
        # self.save_image_as_csv(self.image_height_map.image)

    def transform_and_save_soil_id_map(self, path):
        """
        This function is used to transform all occuring IDs in a soil map to wanted IDs (usually the IDs of the
        created soils). To transform the IDs you have to change the transformation list. This function is used
        as a workaround if you can't find a valid soil-map.
        :param path: String of the path to the map that shall be transformed.
        """
        self.soil_ids_map.filter_unique_numbers_from_2d_array()
        transformation_list = {0: 40, 9362: 80, 18724: 120, 28086: 160, 37449: 200, 46811: 240}
        self.soil_ids_map.transform_image_to_valid_soils(transformation_list)
        self.soil_ids_map.filter_unique_numbers_from_2d_array()  # check if the transformation was successfull
        self.soil_ids_map.save_image(path)

    def prepare_insolation_calculation(self, map_name, daylight_hours, sun_start_elevation, sun_start_azimuth,
                                       sun_max_elevation, reflection_coefficient):
        """
        It finds the correct map obect and creates an image and an object of insolation class. Then the heightmap
        gets loaded and the calculation of the insolation gets started. The results will be shown in the UI and saved.
        :param map_name: String of the current map name
        :param daylight_hours: Integer of the number of daylight hours
        :param sun_start_elevation: Float of the start elevation of the sun
        :param sun_start_azimuth: Float of the start azimuth of the sun
        :param sun_max_elevation: Float of the maximal sun elevation (noon)
        :param reflection_coefficient: Float of the reflection coeficient. It states how much light of the neighbour
                pixel will be reflected.
        """
        map = self.maps[map_name]
        self.image_insolation_map = Image(size=self.image_height_map.size)
        insolation = Insolation(self)
        self.image_height_map.load_image(map.height_map_path)
        self.image_insolation_map = insolation.calculate_actual_insolation(map, daylight_hours, sun_start_elevation,
                                                                           sun_start_azimuth, sun_max_elevation,
                                                                           reflection_coefficient)
        self.main_window.frames['ProbabilityCloudWindow'].draw_insolation_image(self.image_insolation_map)
        save_path = "resources/results/" + map_name + "/" + map_name + "_" + str(daylight_hours) + "daylight_hours_insolation_image.png"
        self.image_insolation_map.save_image(save_path)

    def prepare_orographic_calculation(self, map_name):
        """
        It loads the correct map object, starts the orograhic calculation, displays the result in the UI and
        saves it as an image.
        :param map_name: name of the current map
        """
        map = self.maps[map_name]
        self.image_orographic_map = Orography.calculate_normal_map(map, self.image_height_map)
        self.main_window.frames['ProbabilityCloudWindow'].draw_orographic_image(self.image_orographic_map)
        self.save_3d_list(self.image_orographic_map, "resources/results/" + map_name + "/" + map_name + "_orographic_normals")

    def prepare_edaphic_calculation(self, map_name):
        """
        It loads the correct map object, calculates all angles on the map (between the normal vector and the z-vector),
        starts the edaphic calculation, displays the result in the UI and saves it as an image.
        :param map_name: name of the current map
        """
        map = self.maps[map_name]
        angles = Edaphology.calculate_angles(self.image_orographic_map)
        self.image_edaphic_map = Edaphology.calculate_soil_depth(map, self.image_height_map.size, angles)
        self.main_window.frames['ProbabilityCloudWindow'].draw_edaphic_image(self.image_edaphic_map)
        self.image_edaphic_map.save_image("resources/results/" + map_name + "/" + map_name + "_edaphic_image.png")

    def prepare_water_calculation(self, map_name):
        """
        It loads the correct map and biom object, starts the hydrologic calculation, displays the result in the UI and
        saves it as an image.
        :param map_name: name of the current map
        """
        map = self.maps[map_name]
        biom = map.biom
        hydrology = Hydrology(self)
        self.image_water_map = hydrology.calculate_hydrology_map(map, self.image_edaphic_map, self.soil_ids_map,
                                                                 self.image_insolation_map, biom)
        self.main_window.frames['ProbabilityCloudWindow'].draw_hydrology_image(self.image_water_map)
        self.image_water_map.save_image("resources/results/" + map_name + "/" + map_name + "_water_image.png")

    def calculate_all(self, map_name, daylight_hours, sun_start_elevation, sun_start_azimuth, sun_max_elevation,
                      reflection_coefficient):
        """
        Starts all calculation. This function is used for very large maps. So the user does not have to check the
        state of the application all the time. You can start all calculations and come back a few hours later.
        :param map_name: String of the current map name.
        :param daylight_hours: Integer of the number of daylight hours.
        :param sun_start_elevation: Float of the start elevation of the sun.
        :param sun_start_azimuth: Float of the start azimuth of the sun.
        :param sun_max_elevation: Float of the maximal sun elevation (noon).
        :param reflection_coefficient: Float of the reflection coeficient. It states how much light of the neighbour
                pixel will be reflected.
        """
        self.prepare_insolation_calculation(map_name, daylight_hours, sun_start_elevation, sun_start_azimuth,
                                            sun_max_elevation, reflection_coefficient)
        self.prepare_orographic_calculation(map_name)
        self.prepare_edaphic_calculation(map_name)
        self.prepare_water_calculation(map_name)

    def prepare_probabilites_calculation(self, vegetation_name, map_name):
        """
        It creates a probability object, starts the calculation of the probabilites and displays the result in the UI.
        :param vegetation_name: String. Name of the vegetation for which the probabilites will be calculated.
        :param map_name: String. Name of the current map.
        """
        probability_calculator = Probabilities(self, vegetation_name, map_name)
        self.image_probabilities = probability_calculator.calculate_probabilities()
        self.main_window.frames['ProbabilityCloudWindow'].draw_probability_image(self.image_probabilities)

    def search_soil(self, soil_id):
        """
        Searches for the soil object in the soil list with the help of the soil ID.
        :param soil_id: ID of the soil for which the object from the list shall be found.
        :return: soil_value: Soil object from the soil list.
        """
        for soil_name, soil_value in self.soils.items():
            if soil_value.id == soil_id:
                return soil_value
        print('Soil id (' + str(soil_id) + ') could not be found!')
        return self.soils['NotFound']  # raise Exception('Soil id could not be found!')

    def load_bioms(self):
        """
        Loads all bioms from the bioms.yml into a list.
        """
        bioms = {}
        bioms_file = Path("resources/data/bioms.yml")
        if bioms_file.is_file():
            with open(bioms_file, 'r') as stream:
                try:
                    bioms_dict = yaml.safe_load(stream)
                    if bioms_dict is not None:
                        for biom_name, biom_values in bioms_dict.items():
                            bioms[biom_name] = Biom(biom_name,
                                                    float(biom_values['atmospheric_diffusion']),
                                                    float(biom_values['atmospheric_absorption']),
                                                    float(biom_values['cloud_reflection']),
                                                    float(biom_values['avg_rainfall_per_day']),
                                                    float(biom_values['groundwater']))
                except yaml.YAMLError as exc:
                    print(exc)
        self.bioms = bioms

    def load_soils(self):
        """
        Loads all soils from the soils.yml into a list.
        """
        soils = {}
        soils_file = Path("resources/data/soil_types.yml")
        if soils_file.is_file():
            with open(soils_file, 'r') as stream:
                try:
                    soils_dict = yaml.safe_load(stream)
                    if soils_dict is not None:
                        for soil_name, soil_values in soils_dict.items():
                            soils[soil_name] = Soil(int(soil_values['id']), soil_name, float(soil_values['albedo']),
                                                    float(soil_values['water_absorption']))
                except yaml.YAMLError as exc:
                    print(exc)
        self.soils = soils

    def load_vegetations(self):
        """
        Loads all vegetations from the vegetation_types.yml into a list.
        """
        vegetations = {}
        vegetations_file = Path("resources/data/vegetation_types.yml")
        if vegetations_file.is_file():
            with open(vegetations_file, 'r') as stream:
                try:
                    vegetations_dict = yaml.safe_load(stream)
                    if vegetations_dict is not None:
                        for vegetation_name, vegetation_values in vegetations_dict.items():
                            vegetations[vegetation_name] = Vegetation(vegetation_name,
                                                                      float(vegetation_values['energy_demand']),
                                                                      float(vegetation_values['water_demand']),
                                                                      self.soils[vegetation_values['soil_demand']],
                                                                      float(vegetation_values['soil_depth_demand']))
                except yaml.YAMLError as exc:
                    print(exc)
        self.vegetations = vegetations

    def load_maps(self):
        """
        Loads all maps from the maps.yml into a list.
        """
        maps = {}
        maps_file = Path("resources/data/maps.yml")
        if maps_file.is_file():
            with open(maps_file, 'r') as stream:
                try:
                    maps_dict = yaml.safe_load(stream)
                    if maps_dict is not None:
                        for map_name, map_values in maps_dict.items():
                            maps[map_name] = Map(map_name, self.bioms[map_values['biom']],
                                                 map_values['height_map_path'],
                                                 map_values['texture_map_path'],
                                                 map_values['height_conversion'],
                                                 map_values['max_soil_depth'],
                                                 map_values['pixel_size'])
                except yaml.YAMLError as exc:
                    print(exc)
        self.maps = maps

    @staticmethod
    def save_3d_list(list, path):
        """
        It saves the result of the orographic class (normal map) as a file.
        :param list: List of the normal vectors of the current map.
        :param path: String of the path where the file should be saved.
        """
        if not os.path.exists(os.path.dirname(path)):
            os.makedirs(os.path.dirname(path))
        output = open(path, 'wb')
        pickle.dump(list, output)
        output.close()

    @staticmethod
    def load_3d_list(path):
        """
        Loads the normal vectors from a file.
        :param path: String of the path of the file that will be loaded.
        :return: list: List of the loaded normal vectors (normal map).
        """
        pkl_file = open(path, 'rb')
        list = pickle.load(pkl_file)
        pkl_file.close()
        return list

    @staticmethod
    def save_image_as_csv(image):
        np.savetxt("resources/height_map.csv", image, delimiter=',', fmt='%s')


if __name__ == "__main__":
    Controller().main_window.mainloop()
