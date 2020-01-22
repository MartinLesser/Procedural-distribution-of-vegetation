import tkinter as tk


class BiomWindow(tk.Frame):
    """
    Lists all previously created bioms.
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
        tk.Label(self.frame, text="Bioms:", font='Helvetica 18 bold').grid(row=row, column=column, pady=10)
        row += 1
        tk.Button(self.frame, text="Create new Biom >",
                  command=lambda: main_window.show_frame("NewBiomWindow")).grid(row=row, column=column, pady=10, padx=10)
        for biom in controller.bioms.values():
            row += 1
            tk.Label(self.frame, text=biom.name, font='Helvetica 16').grid(row=row, column=column, pady=10, sticky='E')
            row += 1
            tk.Label(self.frame, text="Atmospheric absorption:").grid(row=row, column=column + 1, pady=5, sticky='E')
            tk.Label(self.frame, text=str(biom.atmospheric_absorption) + "%").grid(row=row, column=column + 2, pady=5, sticky='W')
            row += 1
            tk.Label(self.frame, text="Atmospheric diffusion:").grid(row=row, column=column + 1, pady=5, sticky='E')
            tk.Label(self.frame, text=str(biom.atmospheric_diffusion) + "%").grid(row=row, column=column + 2, pady=5, sticky='W')
            row += 1
            tk.Label(self.frame, text="Cloud reflection:").grid(row=row, column=column + 1, pady=5, sticky='E')
            tk.Label(self.frame, text=str(biom.cloud_reflection) + "%").grid(row=row, column=column + 2, pady=5, sticky='W')
            row += 1
            tk.Label(self.frame, text="Average rainfall per day:").grid(row=row, column=column + 1, pady=5, sticky='E')
            tk.Label(self.frame, text=str(biom.avg_rainfall_per_day) + " l/m²").grid(row=row, column=column + 2, pady=5, sticky='W')
            row += 1
            tk.Label(self.frame, text="Groundwater:").grid(row=row, column=column + 1, pady=5, sticky='E')
            tk.Label(self.frame, text=str(biom.groundwater) + " l/m³").grid(row=row, column=column + 2, pady=5, sticky='W')

    def on_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox(tk.ALL))
