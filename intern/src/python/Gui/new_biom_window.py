import tkinter as tk

from intern.src.python.Data.biom import Biom
from intern.src.python.Gui.biom_window import BiomWindow
from intern.src.python.Gui.new_map_window import NewMapWindow


class NewBiomWindow(tk.Frame):
    """
    Window for creating new biom.
    """

    def __init__(self, parent, main_window, controller):
        tk.Frame.__init__(self, parent)
        self.main_window = main_window
        self.controller = controller
        row = 0
        column = 0

        tk.Button(self, text="< Back to bioms",
                  command=lambda: main_window.show_frame("BiomWindow")).grid(row=row, column=column, pady=10)
        row += 1
        tk.Label(self, text="New Biom:", font='Helvetica 16 bold').grid(row=row, column=column, pady=10)
        height = 1
        width = 10
        column += 1
        row += 1
        tk.Label(self, text="Name:").grid(row=row, column=column, pady=10)
        self.new_biom_name = tk.Text(self, height=height, width=width)
        self.new_biom_name.grid(row=row, column=column + 1, pady=10)
        row += 1
        tk.Label(self, text="Atmospheric diffusion (in %):").grid(row=row, column=column, pady=10)
        self.new_biom_diffusion = tk.Text(self, height=height, width=width)
        self.new_biom_diffusion.grid(row=row, column=column + 1, pady=10)
        row += 1
        tk.Label(self, text="Atmospheric absorption (in %):").grid(row=row, column=column, pady=10)
        self.new_biom_absorption = tk.Text(self, height=height, width=width)
        self.new_biom_absorption.grid(row=row, column=column + 1, pady=10)
        row += 1
        tk.Label(self, text="Cloud reflection (in %):").grid(row=row, column=column, pady=10)
        self.new_biom_reflection = tk.Text(self, height=height, width=width)
        self.new_biom_reflection.grid(row=row, column=column + 1, pady=10)
        row += 1
        tk.Label(self, text="Average rainfall per day (in l/m²):").grid(row=row, column=column, pady=10)
        self.new_biom_rainfall = tk.Text(self, height=height, width=width)
        self.new_biom_rainfall.grid(row=row, column=column + 1, pady=10)
        row += 1
        tk.Label(self, text="Groundwater (in l/m³):").grid(row=row, column=column, pady=10)
        self.new_biom_groundwater = tk.Text(self, height=height, width=width)
        self.new_biom_groundwater.grid(row=row, column=column + 1, pady=10)
        row += 1
        tk.Button(self, text="Save biom",
                  command=lambda: self.save_biom()).grid(row=row, column=column, pady=10)

    def save_biom(self):
        name = self.new_biom_name.get("1.0", 'end-1c')
        diffusion = self.new_biom_diffusion.get("1.0", 'end-1c')
        absorption = self.new_biom_absorption.get("1.0", 'end-1c')
        reflection = self.new_biom_reflection.get("1.0", 'end-1c')
        rainfall = self.new_biom_rainfall.get("1.0", 'end-1c')
        groundwater = self.new_biom_groundwater.get("1.0", 'end-1c')
        new_biom = Biom(name, diffusion, absorption, reflection, rainfall, groundwater)
        new_biom.save_biom()
        self.controller.load_bioms()
        self.main_window.update_frame(NewMapWindow)
        self.main_window.update_frame(BiomWindow)

