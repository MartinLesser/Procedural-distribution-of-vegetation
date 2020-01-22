import tkinter as tk

from intern.src.python.Data.soil import Soil
from intern.src.python.Gui.soil_window import SoilWindow
from intern.src.python.Gui.new_vegetation_type_window import NewVegetationWindow


class NewSoilWindow(tk.Frame):
    """
    Window for creating new soil.
    """

    def __init__(self, parent, main_window, controller):
        tk.Frame.__init__(self, parent)
        self.main_window = main_window
        self.controller = controller
        row = 0
        column = 0

        tk.Button(self, text="< Back to soil types",
                  command=lambda: main_window.show_frame("SoilWindow")).grid(row=row, column=column, pady=10)
        row += 1
        tk.Label(self, text="New soil type:", font='Helvetica 16 bold').grid(row=row, column=column, pady=10)
        height = 1
        width = 10
        column += 1
        row += 1
        tk.Label(self, text="Name:").grid(row=row, column=column, pady=10)
        self.new_soil_name = tk.Text(self, height=height, width=width)
        self.new_soil_name.grid(row=row, column=column + 1, pady=10)
        row += 1
        tk.Label(self, text="ID:").grid(row=row, column=column, pady=10)
        self.new_soil_id = tk.Text(self, height=height, width=width)
        self.new_soil_id.grid(row=row, column=column + 1, pady=10)
        row += 1
        tk.Label(self, text="Albedo:").grid(row=row, column=column, pady=10)
        self.new_soil_albedo = tk.Text(self, height=height, width=width)
        self.new_soil_albedo.grid(row=row, column=column + 1, pady=10)
        row += 1
        tk.Label(self, text="Water absoption (in l/m³):").grid(row=row, column=column, pady=10)
        self.new_soil_water_absoption = tk.Text(self, height=height, width=width)
        self.new_soil_water_absoption.grid(row=row, column=column + 1, pady=10)
        row += 1
        tk.Button(self, text="Save soil",
                  command=lambda: self.save_soil()).grid(row=row, column=column, pady=10)

    def save_soil(self):
        name = self.new_soil_name.get("1.0", 'end-1c')
        id = self.new_soil_id.get("1.0", 'end-1c')
        albedo = self.new_soil_albedo.get("1.0", 'end-1c')
        water_absoption = self.new_soil_water_absoption.get("1.0", 'end-1c')
        new_soil = Soil(id, name, albedo, water_absoption)
        new_soil.save_soil()
        self.controller.load_soils()
        self.main_window.update_frame(NewVegetationWindow)
        self.main_window.update_frame(SoilWindow)
