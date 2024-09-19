import tkinter as tk

from tkinter.font import Font
from user_interface.float_entry import FloatEntry


class ModelParamsFrame(tk.Frame):
    string_vars = dict[str, tk.StringVar]

    def __init__(self, master):
        super(ModelParamsFrame, self).__init__(master)
        self.string_vars = {
            "model 1": tk.StringVar(value="1"),
            "model 2": tk.StringVar(value=""),
            "model 3": tk.StringVar(value=""),
            "model 4": tk.StringVar(value=""),
        }

        title_frame = tk.Frame(self, width=200, height=50, borderwidth=2, relief="raised", padx=2)
        info_frame = tk.Frame(self, width=200, height=50, borderwidth=2, padx=2)
        model_names_frame = tk.Frame(self, width=100, height=100, borderwidth=2, padx=2)
        model_values_frame = tk.Frame(self, width=140, height=130, borderwidth=2, padx=2)
        model_colors_frame = tk.Frame(self, width=140, height=130, borderwidth=2, padx=2)

        title_label = tk.Label(title_frame, text="Model parameters", font="Arial 14")
        italic_font = Font(family="arial", size=9, slant="italic")
        info_label = tk.Label(
            info_frame,
            text="Fill in the blank values to compare multiple models simultaneously",
            font=italic_font)

        model1_label = tk.Label(model_names_frame, text="Model 1 order:", font="Arial 9")
        model2_label = tk.Label(model_names_frame, text="Model 2 order:", font="Arial 9")
        model3_label = tk.Label(model_names_frame, text="Model 3 order:", font="Arial 9")
        model4_label = tk.Label(model_names_frame, text="Model 4 order:", font="Arial 9")

        model1_entry = FloatEntry(model_values_frame, textvariable=self.string_vars["model 1"], width=8)
        model2_entry = FloatEntry(model_values_frame, textvariable=self.string_vars["model 2"], width=8)
        model3_entry = FloatEntry(model_values_frame, textvariable=self.string_vars["model 3"], width=8)
        model4_entry = FloatEntry(model_values_frame, textvariable=self.string_vars["model 4"], width=8)

        model1_color_frame = tk.Frame(model_colors_frame, width=20, height=20, bg="red")
        model2_color_frame = tk.Frame(model_colors_frame, width=20, height=20, bg="green")
        model3_color_frame = tk.Frame(model_colors_frame, width=20, height=20, bg="blue")
        model4_color_frame = tk.Frame(model_colors_frame, width=20, height=20, bg="orange")

        title_frame.grid(row=0, column=0, columnspan=3, pady=2, sticky="N")
        info_frame.grid(row=1, column=0, columnspan=3, pady=2, sticky="N")
        model_names_frame.grid(row=2, column=0, rowspan=4, pady=2, sticky="N")
        model_values_frame.grid(row=2, column=1, rowspan=4, pady=2, sticky="W")
        model_colors_frame.grid(row=2, column=2, rowspan=4, pady=2, sticky="W")

        title_label.grid(row=0, column=0, columnspan=5, pady=2)
        info_label.grid(row=0, column=0, columnspan=5, pady=2)

        model1_label.grid(row=0, column=0, pady=2)
        model2_label.grid(row=1, column=0, pady=2)
        model3_label.grid(row=2, column=0, pady=2)
        model4_label.grid(row=3, column=0, pady=2)

        model1_entry.grid(row=0, column=0, pady=2)
        model2_entry.grid(row=1, column=0, pady=2)
        model3_entry.grid(row=2, column=0, pady=2)
        model4_entry.grid(row=3, column=0, pady=2)

        model1_color_frame.grid(row=0, column=0, pady=2)
        model2_color_frame.grid(row=1, column=0, pady=2)
        model3_color_frame.grid(row=2, column=0, pady=2)
        model4_color_frame.grid(row=3, column=0, pady=2)
