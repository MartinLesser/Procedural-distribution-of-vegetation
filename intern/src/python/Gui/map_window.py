import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from intern.src.python.Data.image import Image


class MapWindow(tk.Frame):
    """
    Lists all previously created maps.
    """

    def __init__(self, parent, main_window, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
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

        tk.Button(self.frame, text="< Back to menu",
                           command=lambda: main_window.show_frame("MenuWindow")).grid(row=row, column=column, pady=10)
        row += 1
        tk.Label(self.frame, text="Maps:", font='Helvetica 18 bold').grid(row=row, column=column, pady=10)
        row += 1
        tk.Button(self.frame, text="Create new map >",
                  command=lambda: main_window.show_frame("NewMapWindow")).grid(row=row, column=column, pady=10, padx=10)
        column += 1
        for map in controller.maps.values():
            row += 1
            tk.Label(self.frame, text=map.name, font='Helvetica 16').grid(row=row, column=column, pady=(50, 0), columnspan=4, sticky='S')
            row += 1
            tk.Label(self.frame, text="Biom:").grid(row=row, column=column + 1, pady=5, sticky='E')
            tk.Label(self.frame, text=map.biom.name).grid(row=row, column=column + 2, pady=5, sticky='W')
            row += 1
            tk.Label(self.frame, text="Height conversion:").grid(row=row, column=column + 1, pady=5, sticky='E')
            tk.Label(self.frame, text=str(map.height_conversion) + " meter/unit").grid(row=row, column=column + 2, pady=5, sticky='W')
            row += 1
            tk.Label(self.frame, text="Maximum soil depth:").grid(row=row, column=column + 1, pady=5, sticky='E')
            tk.Label(self.frame, text=str(map.max_soil_depth) + " cm").grid(row=row, column=column + 2, pady=5, sticky='W')
            row += 1
            tk.Label(self.frame, text="Pixel size:").grid(row=row, column=column + 1, pady=5, sticky='E')
            tk.Label(self.frame, text=str(map.pixel_size) + " m").grid(row=row, column=column + 2, pady=5, sticky='W')
            row += 1
            figure_height_map = Figure(figsize=(3, 3))
            subplot_height_map = figure_height_map.add_subplot()
            subplot_height_map.title.set_text('Height map')
            canvas_height_map = FigureCanvasTkAgg(figure_height_map, master=self.frame)
            canvas_height_map.get_tk_widget().grid(row=row, column=column + 1)
            height_map = Image()
            height_map.load_image(map.height_map_path)
            subplot_height_map.imshow(height_map.image, cmap='gray')

            figure_texture_map = Figure(figsize=(3, 3))
            subplot_texture_map = figure_texture_map.add_subplot()
            subplot_texture_map.title.set_text('Soil-IDs map')
            canvas_texture_map = FigureCanvasTkAgg(figure_texture_map, master=self.frame)
            canvas_texture_map.get_tk_widget().grid(row=row, column=column + 2)
            texture_map = Image()
            texture_map.load_image(map.texture_map_path)
            subplot_texture_map.imshow(texture_map.image)

    def on_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox(tk.ALL))
