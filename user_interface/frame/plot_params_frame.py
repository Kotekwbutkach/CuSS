import tkinter as tk

from tkinter.font import Font

from user_interface.int_entry import IntEntry
from user_interface.float_entry import FloatEntry


class PlotParamsFrame(tk.Frame):
    string_vars = dict[str, tk.StringVar]
    boolean_vars = dict[str, tk.StringVar]

    def __init__(self, master):
        super(PlotParamsFrame, self).__init__(master)
        self.string_vars = {
            "iterations": tk.StringVar(value="1"),
            "folder filepath": tk.StringVar(value="results"),
            "position min filename": tk.StringVar(value="Min distance"),
            "position mean filename": tk.StringVar(value="Mean distance"),
            "position max filename": tk.StringVar(value="Max distance"),
            "velocity min filename": tk.StringVar(value="Min velocity difference"),
            "velocity mean filename": tk.StringVar(value="Mean velocity difference"),
            "velocity max filename": tk.StringVar(value="Max velocity difference"),
        }
        self.boolean_vars = {
            "position min": tk.BooleanVar(value=True),
            "position mean": tk.BooleanVar(value=True),
            "position max": tk.BooleanVar(value=True),
            "velocity min": tk.BooleanVar(value=True),
            "velocity mean": tk.BooleanVar(value=True),
            "velocity max": tk.BooleanVar(value=True),
        }

        title_frame = tk.Frame(self, width=200, height=50, borderwidth=2, relief="raised", padx=2)
        info_frame = tk.Frame(self, width=200, height=50, borderwidth=2, padx=2)
        general_frame = tk.Frame(self, width=200, height=50, borderwidth=2, padx=2)

        title_label = tk.Label(title_frame, text="Plotting parameters", font="Arial 14")
        italic_font = Font(family="arial", size=9, slant="italic")
        info_label = tk.Label(
            info_frame,
            text="Generate plots for the following with the input filename:",
            font=italic_font)

        folder_filepath_label = tk.Label(general_frame, text="Folder relative filepath:", font="Arial 9")
        folder_filepath_entry = tk.Entry(general_frame, textvariable=self.string_vars["folder filepath"], width=30)
        iterations_label = tk.Label(general_frame, text="Number of iterations:", font="Arial 9")
        iterations_entry = IntEntry(general_frame, textvariable=self.string_vars["iterations"], width=8)

        pos_min_label = tk.Label(self, text="Minimum distance:", font="Arial 9")
        pos_mean_label = tk.Label(self, text="Mean distance:", font="Arial 9")
        pos_max_label = tk.Label(self, text="Maximum distance:", font="Arial 9")
        vel_min_label = tk.Label(self, text="Minimum velocity difference:", font="Arial 9")
        vel_mean_label = tk.Label(self, text="Mean velocity difference:", font="Arial 9")
        vel_max_label = tk.Label(self, text="Maximum velocity difference:", font="Arial 9")

        pos_min_box = tk.Checkbutton(self, variable=self.boolean_vars["position min"], font="Arial 9")
        pos_mean_box = tk.Checkbutton(self, variable=self.boolean_vars["position mean"], font="Arial 9")
        pos_max_box = tk.Checkbutton(self, variable=self.boolean_vars["position max"], font="Arial 9")
        vel_min_box = tk.Checkbutton(self, variable=self.boolean_vars["velocity min"], font="Arial 9")
        vel_mean_box = tk.Checkbutton(self, variable=self.boolean_vars["velocity mean"], font="Arial 9")
        vel_max_box = tk.Checkbutton(self, variable=self.boolean_vars["velocity max"], font="Arial 9")

        pos_min_entry = tk.Entry(self, textvariable=self.string_vars["position min filename"], font="Arial 9")
        pos_mean_entry = tk.Entry(self, textvariable=self.string_vars["position mean filename"], font="Arial 9")
        pos_max_entry = tk.Entry(self, textvariable=self.string_vars["position max filename"], font="Arial 9")
        vel_min_entry = tk.Entry(self, textvariable=self.string_vars["velocity min filename"], font="Arial 9")
        vel_mean_entry = tk.Entry(self, textvariable=self.string_vars["velocity mean filename"], font="Arial 9")
        vel_max_entry = tk.Entry(self, textvariable=self.string_vars["velocity max filename"], font="Arial 9")

        pos_min_suffix = tk.Label(self, text=".csv", font="Arial 9")
        pos_mean_suffix = tk.Label(self, text=".csv", font="Arial 9")
        pos_max_suffix = tk.Label(self, text=".csv", font="Arial 9")
        vel_min_suffix = tk.Label(self, text=".csv", font="Arial 9")
        vel_mean_suffix = tk.Label(self, text=".csv", font="Arial 9")
        vel_max_suffix = tk.Label(self, text=".csv", font="Arial 9")

        title_frame.grid(row=0, column=0, columnspan=4, pady=2, sticky="N")
        general_frame.grid(row=1, column=0, columnspan=4, pady=2, sticky="N")
        info_frame.grid(row=2, column=0, columnspan=4, pady=2, sticky="N")

        title_label.grid(row=0, column=0, pady=2)
        info_label.grid(row=0, column=0, pady=2)

        folder_filepath_label.grid(row=0, column=0, pady=2)
        folder_filepath_entry.grid(row=0, column=1, pady=2)
        iterations_label.grid(row=1, column=0, pady=2)
        iterations_entry.grid(row=1, column=1, pady=2, sticky="W")

        pos_min_label.grid(row=3, column=0, pady=2, sticky="E")
        pos_mean_label.grid(row=4, column=0, pady=2, sticky="E")
        pos_max_label.grid(row=5, column=0, pady=2, sticky="E")
        vel_min_label.grid(row=6, column=0, pady=2, sticky="E")
        vel_mean_label.grid(row=7, column=0, pady=2, sticky="E")
        vel_max_label.grid(row=8, column=0, pady=2, sticky="E")

        pos_min_box.grid(row=3, column=1, pady=2)
        pos_mean_box.grid(row=4, column=1, pady=2)
        pos_max_box.grid(row=5, column=1, pady=2)
        vel_min_box.grid(row=6, column=1, pady=2)
        vel_mean_box.grid(row=7, column=1, pady=2)
        vel_max_box.grid(row=8, column=1, pady=2)

        pos_min_entry.grid(row=3, column=2, pady=2)
        pos_mean_entry.grid(row=4, column=2, pady=2)
        pos_max_entry.grid(row=5, column=2, pady=2)
        vel_min_entry.grid(row=6, column=2, pady=2)
        vel_mean_entry.grid(row=7, column=2, pady=2)
        vel_max_entry.grid(row=8, column=2, pady=2)

        pos_min_suffix.grid(row=3, column=3, pady=2)
        pos_mean_suffix.grid(row=4, column=3, pady=2)
        pos_max_suffix.grid(row=5, column=3, pady=2)
        vel_min_suffix.grid(row=6, column=3, pady=2)
        vel_mean_suffix.grid(row=7, column=3, pady=2)
        vel_max_suffix.grid(row=8, column=3, pady=2)

