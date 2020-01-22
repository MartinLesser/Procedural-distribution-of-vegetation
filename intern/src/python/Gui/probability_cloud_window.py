from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np
from pathlib import Path
import tkinter as tk

from intern.src.python.Data.image import Image


class ProbabilityCloudWindow(tk.Frame):
    """
    This window allows the loading of a previously created map. Then the necessary information maps (insolation,
    normals, soil depth and water) can be calculated. With all necessary information the probability for the growth
    of a vegetation at each pixel can be calculated. The results will be displayed and can be saved.
    """

    def __init__(self, parent, main_window, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.parent = parent
        self.canvas_size = 3

        row = 0
        column = 0
        height = 1
        width = 10

        self.canvas = tk.Canvas(self, width=main_window.window_width-20, height=main_window.window_height)
        self.canvas.grid(row=0, column=0, sticky="nsew")

        scrollbar = tk.Scrollbar(self, command=self.canvas.yview)
        scrollbar.grid(row=0, column=1, sticky='ns')

        self.canvas.configure(yscrollcommand=scrollbar.set)

        # update scrollregion after starting 'mainloop'
        # when all widgets are in canvas
        self.canvas.bind('<Configure>', self.on_configure)

        self.frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.frame, anchor='nw')

        button = tk.Button(self.frame, text="< Back to menu",
                           command=lambda: main_window.show_frame("MenuWindow"))
        button.grid(row=row, column=column, pady=10)
        row += 1
        label = tk.Label(self.frame, text="Calculate probability cloud:", font='Helvetica 16 bold')
        label.grid(row=row, column=column, pady=10, columnspan='2')

        row += 1
        # dropdown box
        tk.Label(self.frame, text="Map:").grid(row=row, column=column, pady=10, sticky='E')
        self.maps = tk.ttk.Combobox(self.frame, values=[map.name for map in self.controller.maps.values()])
        self.maps.grid(row=row, column=column + 1, pady=10, sticky='W')
        # daylight hours
        row += 1
        tk.Label(self.frame, text="Daylight hours:").grid(row=row, column=column, pady=10, sticky='E')
        self.daylight_hours = tk.Text(self.frame, height=height, width=width)
        self.daylight_hours.insert(tk.END, "13")
        self.daylight_hours.grid(row=row, column=column + 1, pady=10, sticky='W')
        # load button
        row += 1
        self.button_load_map = tk.Button(self.frame, text="Load map",
                                         command=lambda: self.draw_height_and_soil_map(self.maps.get()))
        self.button_load_map.grid(row=row, column=column + 1, sticky='W', pady=10)
        # start sun elevation in degrees when calculating insolation
        row += 1
        tk.Label(self.frame, text="Sun start elevation (0-90°):").grid(row=row, column=column, pady=10, sticky='E')
        self.sun_start_elevation = tk.Text(self.frame, height=height, width=width)
        self.sun_start_elevation.insert(tk.END, "0")
        self.sun_start_elevation.grid(row=row, column=column + 1, pady=10, sticky='W')
        # start sun azimuth in degrees when calculating insolation. Where the sun rises.
        row += 1
        tk.Label(self.frame, text="Sun start azimuth (0-360°):").grid(row=row, column=column, pady=10, sticky='E')
        self.sun_start_azimuth = tk.Text(self.frame, height=height, width=width)
        self.sun_start_azimuth.insert(tk.END, "0")
        self.sun_start_azimuth.grid(row=row, column=column + 1, pady=10, sticky='W')
        # maximum sun elevation in degrees when calculating insolation
        row += 1
        tk.Label(self.frame, text="Sun max elevation (0-90°):").grid(row=row, column=column, pady=10, sticky='E')
        self.sun_max_elevation = tk.Text(self.frame, height=height, width=width)
        self.sun_max_elevation.insert(tk.END, "80")
        self.sun_max_elevation.grid(row=row, column=column + 1, pady=10, sticky='W')
        # how much insolation is reflected to nearby pixels
        row += 1
        tk.Label(self.frame, text="Reflection (0.0 - 1.0):").grid(row=row, column=column, pady=10, sticky='E')
        self.reflection_coefficient = tk.Text(self.frame, height=height, width=width)
        self.reflection_coefficient.insert(tk.END, "0.1")
        self.reflection_coefficient.grid(row=row, column=column + 1, pady=10, sticky='W')

        row += 1
        self.figure_height_map = Figure(figsize=(self.canvas_size, self.canvas_size))
        self.subplot_height_map = self.figure_height_map.add_subplot()
        self.height_map_colorbar = None
        # disable axis legends
        self.subplot_height_map.set_yticklabels([])
        self.subplot_height_map.set_xticklabels([])
        self.subplot_height_map.set_xticks([])
        self.subplot_height_map.set_yticks([])

        self.subplot_height_map.title.set_text('Height map')
        self.canvas_height_map = FigureCanvasTkAgg(self.figure_height_map, master=self.frame)
        self.canvas_height_map.get_tk_widget().grid(row=row, column=column + 1, sticky='E', pady=10)

        self.figure_texture_map = Figure(figsize=(self.canvas_size, self.canvas_size))
        self.subplot_texture_map = self.figure_texture_map.add_subplot()
        # disable axis legends
        self.subplot_texture_map.set_yticklabels([])
        self.subplot_texture_map.set_xticklabels([])
        self.subplot_texture_map.set_xticks([])
        self.subplot_texture_map.set_yticks([])
        self.subplot_texture_map.title.set_text('Soil-IDs map')
        self.canvas_texture_map = FigureCanvasTkAgg(self.figure_texture_map, master=self.frame)
        self.canvas_texture_map.get_tk_widget().grid(row=row, column=column + 2, sticky='W')

        # insolation
        self.figure_insolation = None
        self.subplot_insolation = None
        self.canvas_insolation = None
        self.button_insolation = None
        self.button_save_insolation = None
        self.insolation_colorbar = None
        # normal/orographic map
        self.figure_orographic = None
        self.subplot_orographic = None
        self.canvas_orographic = None
        self.button_orographic = None
        self.button_save_orographic = None
        # edaphic map
        self.figure_edaphic = None
        self.subplot_edaphic = None
        self.canvas_edaphic = None
        self.button_edaphic = None
        self.button_save_edaphic = None
        self.edaphic_colorbar = None
        # water map
        self.figure_water = None
        self.subplot_water = None
        self.canvas_water = None
        self.button_water = None
        self.button_save_water = None
        self.water_colorbar = None
        # probability map
        self.figure_probability = None
        self.subplot_probability = None
        self.canvas_probability = None
        self.button_probability = None
        self.button_save_probability = None
        self.probability_colorbar = None

        self.button_calc_all = None
        self.load_all_canvases(row, column)

    def on_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox(tk.ALL))

    def load_all_canvases(self, row, column):
        self.load_insolation_map_canvas(row=row + 1, column=column)
        self.load_orographic_map_canvas(row=row + 1, column=column + 1)
        self.load_edaphic_map_canvas(row=row + 1, column=column + 2)
        self.load_water_map_canvas(row=row + 1, column=column + 3)
        self.load_all_maps_button(row=row + 2, column=column)
        self.load_probability_menu(row=row + 4, column=column)

    def draw_height_and_soil_map(self, maps):
        self.controller.load_height_and_soil_map(maps)
        self.subplot_height_map.imshow(self.controller.image_height_map.image, cmap='gray')
        if self.height_map_colorbar:
            self.height_map_colorbar.remove()
        plot = self.subplot_height_map.pcolor(self.controller.image_height_map.image, cmap='gray')
        self.height_map_colorbar = self.figure_height_map.colorbar(plot)

        self.subplot_texture_map.imshow(self.controller.soil_ids_map.image)
        self.canvas_height_map.draw()
        self.canvas_texture_map.draw()
        map_name = self.maps.get()
        map = self.controller.maps[map_name]
        insolation_map_file = Path("resources/results/" + map_name + "/" + map_name + "_" +
                                   self.daylight_hours.get("1.0", 'end-1c') + "daylight_hours_insolation_image.png")

        self.controller.image_insolation_map = Image(size=3, fill_color=0xFF)
        if insolation_map_file.is_file():
            self.controller.image_insolation_map.load_image(insolation_map_file)
        self.draw_insolation_image(self.controller.image_insolation_map)

        orographic_file = Path("resources/results/" + map_name + "/" + map_name + "_orographic_normals")
        self.controller.image_orographic_map = [[[0.0, 0.0, 0.0], [0.0, 0.0, 0.0]], [[0.0, 0.0, 0.0], [0.0, 0.0, 0.0]]]
        if orographic_file.is_file():
            self.controller.image_orographic_map = self.controller.load_3d_list(orographic_file)
        self.draw_orographic_image(self.controller.image_orographic_map)

        edaphic_map_file = Path("resources/results/" + map_name + "/" + map_name + "_edaphic_image.png")
        self.controller.image_edaphic_map = Image(size=3, fill_color=0xFF)
        if edaphic_map_file.is_file():
            self.controller.image_edaphic_map.load_image(edaphic_map_file)
        self.draw_edaphic_image(self.controller.image_edaphic_map)

        water_map_file = Path("resources/results/" + map_name + "/" + map_name + "_water_image.png")
        self.controller.image_water_map = Image(dtype=np.float, size=3, fill_color=0xFF)
        if water_map_file.is_file():
            self.controller.image_water_map.load_image(water_map_file)
        self.draw_hydrology_image(self.controller.image_water_map)

        self.controller.image_probabilities = Image(dtype=np.float, size=3, fill_color=0xFF)
        self.draw_probability_image(self.controller.image_probabilities)

    def load_insolation_map_canvas(self, row, column):
        self.figure_insolation = Figure(figsize=(self.canvas_size, self.canvas_size))
        self.subplot_insolation = self.figure_insolation.add_subplot()
        self.subplot_insolation.title.set_text('Insolation map (kcal)')
        # disable axis legends
        self.subplot_insolation.set_yticklabels([])
        self.subplot_insolation.set_xticklabels([])
        self.subplot_insolation.set_xticks([])
        self.subplot_insolation.set_yticks([])

        self.canvas_insolation = FigureCanvasTkAgg(self.figure_insolation, master=self.frame)
        self.canvas_insolation.get_tk_widget().grid(row=row, column=column)
        self.button_insolation = tk.Button(self.frame, text="Calculate insolation map",
                                           command=lambda: self.controller.prepare_insolation_calculation(
                                               self.maps.get(), int(self.daylight_hours.get("1.0", 'end-1c')),
                                               float(self.sun_start_elevation.get("1.0", 'end-1c')),
                                               float(self.sun_start_azimuth.get("1.0", 'end-1c')),
                                               float(self.sun_max_elevation.get("1.0", 'end-1c')),
                                               float(self.reflection_coefficient.get("1.0", 'end-1c'))))
        self.button_insolation.grid(row=row + 1, column=column)
        # self.button_save_insolation = tk.Button(self.frame, text="Save insolation map",
        #                                         command=lambda: self.controller.image_insolation_map.save_image(
        #                                             "resources/results/" + map_name + "/" + self.maps.get() + "_" + self.daylight_hours.get(
        #                                                 "1.0", 'end-1c') + "daylight_hours_insolation_image.png"))
        # self.button_save_insolation.grid(row=row + 2, column=column)

    def load_orographic_map_canvas(self, row, column):
        self.figure_orographic = Figure(figsize=(self.canvas_size, self.canvas_size))
        self.subplot_orographic = self.figure_orographic.add_subplot()
        self.subplot_orographic.title.set_text('Orographic map')
        # disable axis legends
        self.subplot_orographic.set_yticklabels([])
        self.subplot_orographic.set_xticklabels([])
        self.subplot_orographic.set_xticks([])
        self.subplot_orographic.set_yticks([])

        self.canvas_orographic = FigureCanvasTkAgg(self.figure_orographic, master=self.frame)
        self.canvas_orographic.get_tk_widget().grid(row=row, column=column)
        self.button_orographic = tk.Button(self.frame, text="Calculate orographic map",
                                           command=lambda: self.controller.prepare_orographic_calculation(
                                               self.maps.get()))
        self.button_orographic.grid(row=row + 1, column=column)
        # self.button_save_orographic = tk.Button(self.frame, text="Save orographic map",
        #                                         command=lambda: self.controller.save_3d_list(
        #                                             self.controller.image_orographic_map,
        #                                             "resources/results/" + map_name + "/" + self.maps.get() + "_orographic_normals"))
        # self.button_save_orographic.grid(row=row + 2, column=column)

    def load_edaphic_map_canvas(self, row, column):
        self.figure_edaphic = Figure(figsize=(self.canvas_size, self.canvas_size))
        self.subplot_edaphic = self.figure_edaphic.add_subplot()
        self.subplot_edaphic.title.set_text('Edaphic map (cm)')
        # disable axis legends
        self.subplot_edaphic.set_yticklabels([])
        self.subplot_edaphic.set_xticklabels([])
        self.subplot_edaphic.set_xticks([])
        self.subplot_edaphic.set_yticks([])

        self.canvas_edaphic = FigureCanvasTkAgg(self.figure_edaphic, master=self.frame)
        self.canvas_edaphic.get_tk_widget().grid(row=row, column=column)
        self.button_edaphic = tk.Button(self.frame, text="Calculate edaphic map",
                                        command=lambda: self.controller.prepare_edaphic_calculation(self.maps.get()))
        self.button_edaphic.grid(row=row + 1, column=column)
        # self.button_save_edaphic = tk.Button(self.frame, text="Save edaphic map",
        #                                      command=lambda: self.controller.image_edaphic_map.save_image(
        #                                          "resources/results/" + map_name + "/" + self.maps.get() + "_edaphic_image.png"))
        # self.button_save_edaphic.grid(row=row + 2, column=column)

    def load_water_map_canvas(self, row, column):
        self.figure_water = Figure(figsize=(self.canvas_size, self.canvas_size))
        self.subplot_water = self.figure_water.add_subplot()
        self.subplot_water.title.set_text('Hydrology map (l)')
        # disable axis legends
        self.subplot_water.set_yticklabels([])
        self.subplot_water.set_xticklabels([])
        self.subplot_water.set_xticks([])
        self.subplot_water.set_yticks([])

        self.canvas_water = FigureCanvasTkAgg(self.figure_water, master=self.frame)
        self.canvas_water.get_tk_widget().grid(row=row, column=column)
        self.button_water = tk.Button(self.frame, text="Calculate hydrology map",
                                      command=lambda: self.controller.prepare_water_calculation(self.maps.get()))
        self.button_water.grid(row=row + 1, column=column)
        # self.button_save_water = tk.Button(self.frame, text="Save water map",
        #                                    command=lambda: self.controller.image_water_map.save_image(
        #                                        "resources/results/" + map_name + "/" + self.maps.get() + "_water_image.png"))
        # self.button_save_water.grid(row=row + 2, column=column)

    def load_probability_menu(self, row, column):
        tk.Label(self.frame, text="Vegetation type:").grid(row=row, column=column, pady=10, sticky='E', columnspan='2')
        vegetation_dropwdown = tk.ttk.Combobox(self.frame, values=[vegetation.name for vegetation in
                                                                   self.controller.vegetations.values()])
        vegetation_dropwdown.grid(row=row, column=column + 2, sticky='W', columnspan='2')

        self.figure_probability = Figure(figsize=(self.canvas_size, self.canvas_size))
        self.subplot_probability = self.figure_probability.add_subplot()
        self.subplot_probability.title.set_text('Probability map (%)')
        # disable axis legends
        self.subplot_probability.set_yticklabels([])
        self.subplot_probability.set_xticklabels([])
        self.subplot_probability.set_xticks([])
        self.subplot_probability.set_yticks([])

        row += 1
        self.canvas_probability = FigureCanvasTkAgg(self.figure_probability, master=self.frame)
        self.canvas_probability.get_tk_widget().grid(row=row, column=column, columnspan='4')
        self.button_probability = tk.Button(self.frame, text="Calculate probabilities",
                                            command=lambda: self.controller.prepare_probabilites_calculation(
                                                vegetation_dropwdown.get(), self.maps.get()))
        row += 1
        self.button_probability.grid(row=row, column=column, columnspan='2', sticky='E')
        self.button_save_probability = tk.Button(self.frame, text="Save probability map",
                                                 command=lambda: self.controller.image_probabilities.save_image(
                                                     "resources/results/" + self.maps.get() + "/" + self.maps.get() + "_"
                                                     + vegetation_dropwdown.get() + "_" + self.daylight_hours.get(
                                                     "1.0", 'end-1c') + "daylight_hours_probability_image.png"))
        self.button_save_probability.grid(row=row, column=column + 2, columnspan='2', sticky='W')

    def load_all_maps_button(self, row, column):
        self.button_calc_all = tk.Button(self.frame, text="Calculate and save all maps",
                                         command=lambda: self.controller.calculate_all(self.maps.get(),
                                                                                       int(self.daylight_hours.get(
                                                                                           "1.0", 'end-1c')),
                                                                                       float(
                                                                                           self.sun_start_elevation.get(
                                                                                               "1.0", 'end-1c')),
                                                                                       float(self.sun_start_azimuth.get(
                                                                                           "1.0", 'end-1c')),
                                                                                       float(self.sun_max_elevation.get(
                                                                                           "1.0", 'end-1c')),
                                                                                       float(
                                                                                           self.reflection_coefficient.get(
                                                                                               "1.0", 'end-1c'))
                                                                                       ))
        self.button_calc_all.grid(row=row + 1, column=column, columnspan=5, pady=10)

    def draw_insolation_image(self, insolation_image):
        if self.insolation_colorbar:
            self.insolation_colorbar.remove()
        self.subplot_insolation.imshow(insolation_image.image, cmap='afmhot')
        plot = self.subplot_insolation.pcolor(insolation_image.image, cmap='afmhot')
        self.insolation_colorbar = self.figure_insolation.colorbar(plot)
        self.canvas_insolation.draw()

    def draw_orographic_image(self, orographic_image):
        new_array = []
        for y in orographic_image:
            row = []
            for x in y:
                normal = x
                positive = [(normal[0] + 1) / 2, (normal[1] + 1) / 2, (normal[2] + 1) / 2]
                row.append(positive)
            new_array.append(row)
        self.subplot_orographic.imshow(new_array, cmap='cool')
        self.canvas_orographic.draw()

    def draw_edaphic_image(self, edaphic_image):
        if self.edaphic_colorbar:
            self.edaphic_colorbar.remove()
        self.subplot_edaphic.imshow(edaphic_image.image, cmap='YlOrBr')
        plot = self.subplot_edaphic.pcolor(edaphic_image.image, cmap='YlOrBr')
        self.edaphic_colorbar = self.figure_edaphic.colorbar(plot)
        self.canvas_edaphic.draw()

    def draw_hydrology_image(self, hydrology_image):
        if self.water_colorbar:
            self.water_colorbar.remove()
        self.subplot_water.imshow(hydrology_image.image, cmap='PuBu')
        plot = self.subplot_water.pcolor(hydrology_image.image, cmap='PuBu')
        self.water_colorbar = self.figure_water.colorbar(plot)
        self.canvas_water.draw()

    def draw_probability_image(self, probability_image):
        if self.probability_colorbar:
            self.probability_colorbar.remove()
        self.subplot_probability.imshow(probability_image.image, cmap='bone')
        plot = self.subplot_probability.pcolor(probability_image.image, cmap='bone')
        self.probability_colorbar = self.figure_probability.colorbar(plot)
        self.canvas_probability.draw()
