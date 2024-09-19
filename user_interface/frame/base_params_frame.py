import tkinter as tk

from tkinter.font import Font
from user_interface.float_entry import FloatEntry


class BaseParamsFrame(tk.Frame):
    string_vars = dict[str, tk.StringVar]

    def __init__(self, master):
        super(BaseParamsFrame, self).__init__(master)
        self.string_vars = {
            "particles": tk.StringVar(value="5"),
            "duration": tk.StringVar(value="1000"),
            "beta_coefficient": tk.StringVar(value="2"),
        }

        title_frame = tk.Frame(self, width=200, height=50, borderwidth=2, relief="raised", padx=2)
        param_names_frame = tk.Frame(self, width=100, height=100, borderwidth=2, padx=2)
        param_values_frame = tk.Frame(self, width=140, height=130, borderwidth=2, padx=2)

        title_label = tk.Label(self, text="Base parameters", font="Arial 14")

        particles_label = tk.Label(param_names_frame, text="Number of particles:", font="Arial 9")
        duration_label = tk.Label(param_names_frame, text="Duration:", font="Arial 9")
        beta_label = tk.Label(param_names_frame, text="Beta coefficient:", font="Arial 9")
        italic_font = Font(family="arial", size=9, slant="italic")
        phi_label = tk.Label(param_names_frame, text="Phi(s) = (1 + s^{Beta/2})^{-1}", font=italic_font)
        particles_entry = FloatEntry(param_values_frame, textvariable=self.string_vars["particles"], width=8)
        duration_entry = FloatEntry(param_values_frame, textvariable=self.string_vars["duration"], width=8)
        beta_entry = FloatEntry(param_values_frame, textvariable=self.string_vars["beta_coefficient"], width=8)

        title_frame.grid(row=0, column=0, columnspan=2, pady=2, sticky="N")
        param_names_frame.grid(row=1, column=0, columnspan=1, rowspan=4, pady=2, sticky="N")
        param_values_frame.grid(row=1, column=1, columnspan=1, rowspan=3, pady=2, sticky="W")

        title_label.grid(row=0, column=0, columnspan=5, pady=2)

        particles_label.grid(row=0, column=0, pady=2)
        duration_label.grid(row=1, column=0, pady=2)
        beta_label.grid(row=2, column=0, pady=2)
        phi_label.grid(row=3, column=0, pady=2)

        particles_entry.grid(row=0, column=0, pady=2)
        duration_entry.grid(row=1, column=0, pady=2)
        beta_entry.grid(row=2, column=0, pady=2)
