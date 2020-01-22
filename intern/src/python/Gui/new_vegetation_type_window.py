import tkinter as tk

from intern.src.python.Data.vegetation import Vegetation
from intern.src.python.Gui.vegetation_window import VegetationWindow


class NewVegetationWindow(tk.Frame):
    """
    Window for creating new vegetation.
    """

    def __init__(self, parent, main_window, controller):
        tk.Frame.__init__(self, parent)
        self.main_window = main_window
        self.controller = controller
        row = 0
        column = 0

        tk.Button(self, text="< Back to vegetation types",
                  command=lambda: main_window.show_frame("VegetationWindow")).grid(row=row, column=column, pady=10)
        row += 1
        tk.Label(self, text="New vegetation type:", font='Helvetica 16 bold').grid(row=row, column=column, pady=10)
        height = 1
        width = 10
        column += 1
        row += 1
        tk.Label(self, text="Name:").grid(row=row, column=column, pady=10)
        self.new_vegetation_name = tk.Text(self, height=height, width=width)
        self.new_vegetation_name.grid(row=row, column=column + 1, pady=10)
        row += 1
        tk.Label(self, text="Energy demand (in kcal/day):").grid(row=row, column=column, pady=10)
        self.new_vegetation_energy_demand = tk.Text(self, height=height, width=width)
        self.new_vegetation_energy_demand.grid(row=row, column=column + 1, pady=10)
        row += 1
        tk.Label(self, text="Water demand (in l/cm²):").grid(row=row, column=column, pady=10)
        self.new_vegetation_water_demand = tk.Text(self, height=height, width=width)
        self.new_vegetation_water_demand.grid(row=row, column=column + 1, pady=10)
        row += 1
        tk.Label(self, text="Soil demand:").grid(row=row, column=column, pady=10)
        self.soil_demand = tk.ttk.Combobox(self, values=[soil.name for soil in self.controller.soils.values()])
        self.soil_demand.grid(row=row, column=column + 1, pady=10)
        row += 1
        tk.Label(self, text="Soil depth demand (in cm):").grid(row=row, column=column, pady=10)
        self.new_vegetation_soil_depth_demand = tk.Text(self, height=height, width=width)
        self.new_vegetation_soil_depth_demand.grid(row=row, column=column + 1, pady=10)
        row += 1
        tk.Button(self, text="Save vegetation",
                  command=lambda: self.save_vegetation()).grid(row=row, column=column, pady=10)

    def save_vegetation(self):
        name = self.new_vegetation_name.get("1.0", 'end-1c')
        energy_demand = self.new_vegetation_energy_demand.get("1.0", 'end-1c')
        water_demand = self.new_vegetation_water_demand.get("1.0", 'end-1c')
        soil_demand = self.soil_demand.get()
        soil_depth_demand = self.new_vegetation_soil_depth_demand.get("1.0", 'end-1c')
        new_vegetation = Vegetation(name, energy_demand, water_demand, soil_demand, soil_depth_demand)
        new_vegetation.save_vegetation()
        self.controller.load_vegetations()
        self.main_window.update_frame(VegetationWindow)
