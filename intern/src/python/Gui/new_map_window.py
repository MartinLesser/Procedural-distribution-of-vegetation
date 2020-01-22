import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkfilebrowser import askopenfilenames

from intern.src.python.Data.image import Image
from intern.src.python.Data.map import Map
from intern.src.python.Gui.map_window import MapWindow
from intern.src.python.Gui.probability_cloud_window import ProbabilityCloudWindow


class NewMapWindow(tk.Frame):
    """
    Window for creating new map.
    """

    def __init__(self, parent, main_window, controller):
        tk.Frame.__init__(self, parent)
        self.main_window = main_window
        self.controller = controller

        # height map
        self.subplot_height_map = None
        self.canvas_height_map = None
        self.height_map_path = ""
        # texture map
        self.subplot_texture_map = None
        self.canvas_texture_map = None
        self.texture_map_path = ""

        row = 0
        column = 0

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

        tk.Button(self.frame, text="< Back to maps",
                  command=lambda: main_window.show_frame("MapWindow")).grid(row=row, column=column, pady=10)
        row += 1
        tk.Label(self.frame, text="New map:", font='Helvetica 16 bold').grid(row=row, column=column, pady=10)
        height = 1
        width = 10
        column += 1

        row += 1
        tk.Label(self.frame, text="Name:").grid(row=row, column=column, pady=10)
        self.new_map_name = tk.Text(self.frame, height=height, width=width)
        self.new_map_name.grid(row=row, column=column + 1, pady=10)

        row += 1
        tk.Label(self.frame, text="Biom:").grid(row=row, column=column, pady=10)
        self.biom = tk.ttk.Combobox(self.frame, values=[soil.name for soil in self.controller.bioms.values()])
        self.biom.grid(row=row, column=column + 1, pady=10)

        row += 1
        tk.Label(self.frame, text="Height conversion (one unit is how many meter?):").grid(row=row, column=column, pady=10)
        self.new_map_height_conversion = tk.Text(self.frame, height=height, width=width)
        self.new_map_height_conversion.grid(row=row, column=column + 1, pady=10)

        row += 1
        tk.Label(self.frame, text="Maximum soil depth (in cm):").grid(row=row, column=column, pady=10)
        self.new_map_max_soil_depth = tk.Text(self.frame, height=height, width=width)
        self.new_map_max_soil_depth.grid(row=row, column=column + 1, pady=10)

        row += 1
        tk.Label(self.frame, text="Pixel size (in m):").grid(row=row, column=column, pady=10)
        self.new_map_pixel_size = tk.Text(self.frame, height=height, width=width)
        self.new_map_pixel_size.grid(row=row, column=column + 1, pady=10)

        row += 1
        # height map
        figure_height_map = Figure(figsize=(3, 3))
        self.subplot_height_map = figure_height_map.add_subplot()
        self.subplot_height_map.title.set_text('Height map')
        self.canvas_height_map = FigureCanvasTkAgg(figure_height_map, master=self.frame)
        self.canvas_height_map.get_tk_widget().grid(row=row, column=column)
        tk.Button(self.frame, text="Load height-map", command=self.load_height_map).grid(row=row + 1, column=column)

        # soil id map
        figure_texture_map = Figure(figsize=(3, 3))
        self.subplot_texture_map = figure_texture_map.add_subplot()
        self.subplot_texture_map.title.set_text('Soil-IDs map')
        self.canvas_texture_map = FigureCanvasTkAgg(figure_texture_map, master=self.frame)
        self.canvas_texture_map.get_tk_widget().grid(row=row, column=column + 1)
        tk.Button(self.frame, text="Load soil-id-map", command=self.load_texture_map).grid(row=row + 1, column=column + 1)

        row += 2
        tk.Button(self.frame, text="Save map",
                  command=lambda: self.save_map()).grid(row=row, column=column, pady=10, columnspan=2)

    def save_map(self):
        name = self.new_map_name.get("1.0", 'end-1c')
        biom = self.biom.get()
        height_conversion = float(self.new_map_height_conversion.get("1.0", 'end-1c'))
        max_soil_depth = float(self.new_map_max_soil_depth.get("1.0", 'end-1c'))
        pixel_distance = float(self.new_map_pixel_size.get("1.0", 'end-1c'))
        new_map = Map(name, biom, self.height_map_path, self.texture_map_path, height_conversion, max_soil_depth,
                      pixel_distance)
        new_map.save_map()
        self.controller.load_maps()
        self.main_window.update_frame(ProbabilityCloudWindow)
        self.main_window.update_frame(MapWindow)

    def load_height_map(self):
        rep = askopenfilenames(parent=self, initialdir='/', initialfile='tmp',
                               filetypes=[("Pictures", "*.png")])
        if len(rep) > 0:
            self.height_map_path = rep[0]
            image_height_map = Image()
            image_height_map.load_image(self.height_map_path)
            self.subplot_height_map.imshow(image_height_map.image, cmap='gray')
            self.canvas_height_map.draw()

    def load_texture_map(self):
        rep = askopenfilenames(parent=self, initialdir='/', initialfile='tmp',
                               filetypes=[("Pictures", "*.png")])
        if len(rep) > 0:
            self.texture_map_path = rep[0]
            soil_ids_map = Image()
            soil_ids_map.load_image(self.texture_map_path)
            self.subplot_texture_map.imshow(soil_ids_map.image)
            self.canvas_texture_map.draw()

    def on_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox(tk.ALL))
