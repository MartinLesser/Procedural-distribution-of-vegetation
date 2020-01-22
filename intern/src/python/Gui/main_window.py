import tkinter as tk

from intern.src.python.Gui.biom_window import BiomWindow
from intern.src.python.Gui.new_biom_window import NewBiomWindow
from intern.src.python.Gui.map_window import MapWindow
from intern.src.python.Gui.new_map_window import NewMapWindow
from intern.src.python.Gui.menu_window import MenuWindow
from intern.src.python.Gui.soil_window import SoilWindow
from intern.src.python.Gui.new_soil_type_window import NewSoilWindow
from intern.src.python.Gui.vegetation_window import VegetationWindow
from intern.src.python.Gui.new_vegetation_type_window import NewVegetationWindow
from intern.src.python.Gui.probability_cloud_window import ProbabilityCloudWindow


class MainWindow(tk.Tk):
    """
    Main window, which creates all other windows and stores them in a list. The show_frame function raises the
     selected window to the foreground.
    """

    def __init__(self, controller):
        tk.Tk.__init__(self)
        self.controller = controller
        self.title("Prozedurale Verteilung von Vegetation")
        self.window_width = 1300
        self.window_height = 800
        self.geometry(str(self.window_width) + "x" + str(self.window_height))
        self.resizable(0, 0)

        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (
            MenuWindow, MapWindow, NewMapWindow, SoilWindow, NewSoilWindow, BiomWindow, NewBiomWindow, VegetationWindow,
                NewVegetationWindow, ProbabilityCloudWindow):
            page_name = F.__name__
            frame = F(self.container, self, self.controller)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("MenuWindow")

    def show_frame(self, page_name):
        """
        Show a frame for the given page name
        """
        frame = self.frames[page_name]
        frame.tkraise()

    def update_frame(self, page_name):
        frame = page_name(self.container, self, self.controller)
        self.frames[page_name.__name__] = frame
        frame.grid(row=0, column=0, sticky="nsew")
