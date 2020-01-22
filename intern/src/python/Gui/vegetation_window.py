import tkinter as tk


class VegetationWindow(tk.Frame):
    """
    Lists all previously created vegetation types.
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
        tk.Label(self.frame, text="Vegetation types:", font='Helvetica 18 bold').grid(row=row, column=column, pady=10)
        row += 1
        tk.Button(self.frame, text="Create new vegetation type >",
                  command=lambda: main_window.show_frame("NewVegetationWindow")).grid(row=row, column=column, pady=10,
                                                                                padx=10)
        for vegetation in controller.vegetations.values():
            row += 1
            tk.Label(self.frame, text=vegetation.name, font='Helvetica 16').grid(row=row, column=column, pady=10, sticky='E')
            row += 1
            tk.Label(self.frame, text="Energy demand:").grid(row=row, column=column + 1, pady=5, sticky='E')
            tk.Label(self.frame, text=str(vegetation.energy_demand) + " kcal/day").grid(row=row, column=column + 2, pady=5, sticky='W')
            row += 1
            tk.Label(self.frame, text="Water demand:").grid(row=row, column=column + 1, pady=5, sticky='E')
            tk.Label(self.frame, text=str(vegetation.water_demand) + " l/day").grid(row=row, column=column + 2, pady=5, sticky='W')
            row += 1
            tk.Label(self.frame, text="Soil demand:").grid(row=row, column=column + 1, pady=5, sticky='E')
            tk.Label(self.frame, text=vegetation.soil_demand.name).grid(row=row, column=column + 2, pady=5, sticky='W')
            row += 1
            tk.Label(self.frame, text="Soil depth demand:").grid(row=row, column=column + 1, pady=5, sticky='E')
            tk.Label(self.frame, text=str(vegetation.soil_depth_demand) + " cm").grid(row=row, column=column + 2, pady=5, sticky='W')

    def on_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox(tk.ALL))
