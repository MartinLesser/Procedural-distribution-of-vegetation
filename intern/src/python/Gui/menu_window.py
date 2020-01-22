import tkinter as tk


class MenuWindow(tk.Frame):
    """
    Menu for creating data (bioms, maps, soils or vegetation types) and calculating probabilities.
    """

    def __init__(self, parent, main_window, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        row = 0
        label = tk.Label(self, text="Main menu", font='Helvetica 18 bold')
        label.grid(row=row, column=0, pady=10)

        row += 1
        button_biom = tk.Button(self, text="Biom types >",
                                command=lambda: main_window.show_frame("BiomWindow"))
        button_biom.grid(row=row, column=0, pady=5, padx=5)
        row += 1
        button_soil = tk.Button(self, text="Soil types >",
                                command=lambda: main_window.show_frame("SoilWindow"))
        button_soil.grid(row=row, column=0, pady=5, padx=5)
        row += 1
        button_vegetation = tk.Button(self, text="Vegetation types >",
                                command=lambda: main_window.show_frame("VegetationWindow"))
        button_vegetation.grid(row=row, column=0, pady=5, padx=5)
        row += 1
        button_map = tk.Button(self, text="Maps >",
                               command=lambda: main_window.show_frame("MapWindow"))
        button_map.grid(row=row, column=0, pady=5, padx=5)
        row += 1
        button_map = tk.Button(self, text="Calculate probability cloud >",
                               command=lambda: main_window.show_frame("ProbabilityCloudWindow"))
        button_map.grid(row=row, column=0, pady=5, padx=5)
