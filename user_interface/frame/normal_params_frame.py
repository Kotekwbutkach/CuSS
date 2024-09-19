import tkinter as tk
from user_interface.float_entry import FloatEntry


class NormalParamsFrame(tk.Frame):
    string_vars = dict[str, tk.StringVar]

    def __init__(self, master):
        super(NormalParamsFrame, self).__init__(master)
        self.string_vars = {
            "mean_x1": tk.StringVar(value="0"),
            "mean_x2": tk.StringVar(value="0"),
            "mean_v1": tk.StringVar(value="0"),
            "mean_v2": tk.StringVar(value="0"),
            "std_dev_x1": tk.StringVar(value="1"),
            "std_dev_x2": tk.StringVar(value="1"),
            "std_dev_v1": tk.StringVar(value="1"),
            "std_dev_v2": tk.StringVar(value="1"),
        }

        title_frame = tk.Frame(self, width=150, height=50, borderwidth=2, relief="raised", padx=2)
        x1_frame = tk.Frame(self, width=50, height=30, borderwidth=2, padx=2)
        x2_frame = tk.Frame(self, width=50, height=30, borderwidth=2, padx=2)
        v1_frame = tk.Frame(self, width=50, height=30, borderwidth=2, padx=2)
        v2_frame = tk.Frame(self, width=50, height=30, borderwidth=2, padx=2)

        title_label = tk.Label(title_frame, text="Normal distribution parameters", font="Arial 14")

        x1_label = tk.Label(x1_frame, text="x1", font="Arial 9")
        x2_label = tk.Label(x2_frame, text="x2", font="Arial 9")
        v1_label = tk.Label(v1_frame, text="v1", font="Arial 9")
        v2_label = tk.Label(v2_frame, text="v2", font="Arial 9")
        mean_label = tk.Label(self, text="Mean:")
        std_dev_label = tk.Label(self, text="Std dev:")
        mean_x1_entry = FloatEntry(self, textvariable=self.string_vars["mean_x1"], width=6)
        mean_x2_entry = FloatEntry(self, textvariable=self.string_vars["mean_x2"], width=6)
        mean_v1_entry = FloatEntry(self, textvariable=self.string_vars["mean_v1"], width=6)
        mean_v2_entry = FloatEntry(self, textvariable=self.string_vars["mean_v2"], width=6)
        std_dev_x1_entry = FloatEntry(self, textvariable=self.string_vars["std_dev_x1"], width=6)
        std_dev_x2_entry = FloatEntry(self, textvariable=self.string_vars["std_dev_x2"], width=6)
        std_dev_v1_entry = FloatEntry(self, textvariable=self.string_vars["std_dev_v1"], width=6)
        std_dev_v2_entry = FloatEntry(self, textvariable=self.string_vars["std_dev_v2"], width=6)

        title_frame.grid(row=0, column=0, columnspan=5, pady=2, sticky="N")
        x1_frame.grid(row=1, column=1, pady=2, sticky="N")
        x2_frame.grid(row=1, column=2, pady=2, sticky="N")
        v1_frame.grid(row=1, column=3, pady=2, sticky="N")
        v2_frame.grid(row=1, column=4, pady=2, sticky="N")

        title_label.grid(row=0, column=0, columnspan=5, pady=2)
        x1_label.grid(row=0, column=0, pady=2)
        x2_label.grid(row=0, column=1, pady=2)
        v1_label.grid(row=0, column=0, pady=2)
        v2_label.grid(row=0, column=1, pady=2)
        mean_label.grid(row=2, column=0, padx=10, pady=2)
        std_dev_label.grid(row=3, column=0, padx=10, pady=2)

        mean_x1_entry.grid(row=2, column=1, padx=10, pady=10)
        mean_x2_entry.grid(row=2, column=2, padx=10, pady=10)
        mean_v1_entry.grid(row=2, column=3, padx=10, pady=10)
        mean_v2_entry.grid(row=2, column=4, padx=10, pady=10)

        std_dev_x1_entry.grid(row=3, column=1, padx=10, pady=10)
        std_dev_x2_entry.grid(row=3, column=2, padx=10, pady=10)
        std_dev_v1_entry.grid(row=3, column=3, padx=10, pady=10)
        std_dev_v2_entry.grid(row=3, column=4, padx=10, pady=10)
