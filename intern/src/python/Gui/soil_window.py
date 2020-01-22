import tkinter as tk


class SoilWindow(tk.Frame):
    """
    Lists all previously created soils.
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
        tk.Label(self.frame, text="Soils:", font='Helvetica 18 bold').grid(row=row, column=column, pady=10)
        row += 1
        tk.Button(self.frame, text="Create new soil type >",
                  command=lambda: main_window.show_frame("NewSoilWindow")).grid(row=row, column=column, pady=10,
                                                                                padx=10)
        for soil in controller.soils.values():
            row += 1
            tk.Label(self.frame, text=soil.name, font='Helvetica 16').grid(row=row, column=column, pady=10, sticky='E')
            row += 1
            tk.Label(self.frame, text="ID:").grid(row=row, column=column + 1, pady=5, sticky='E')
            tk.Label(self.frame, text=soil.id).grid(row=row, column=column + 2, pady=5, sticky='W')
            row += 1
            tk.Label(self.frame, text="Albedo:").grid(row=row, column=column + 1, pady=5, sticky='E')
            tk.Label(self.frame, text=soil.albedo).grid(row=row, column=column + 2, pady=5, sticky='W')
            row += 1
            tk.Label(self.frame, text="Water absoption:").grid(row=row, column=column + 1, pady=5, sticky='E')
            tk.Label(self.frame, text=str(soil.water_absorption) + " l/m³").grid(row=row, column=column + 2, pady=5, sticky='W')

    def on_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox(tk.ALL))
