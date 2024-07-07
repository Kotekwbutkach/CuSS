import tkinter as tk
from user_interface.float_entry import FloatEntry


class NormalParamsFrame(tk.Frame):
    string_vars = list[list[int]]

    def __init__(self, master):
        super(NormalParamsFrame, self).__init__(master)
        self.string_vars = [[tk.StringVar(value=str(i)) for _ in range(4)] for i in range(2)]

        title_frame = tk.Frame(self, width=390, height=50, borderwidth=2, relief="raised", padx=2)
        x_top_frame = tk.Frame(self, width=140, height=30, borderwidth=2, relief="raised", padx=2)
        x_bottom_frame = tk.Frame(self, width=140, height=130, borderwidth=2, relief="raised", padx=2)
        y_top_frame = tk.Frame(self, width=140, height=30, borderwidth=2, relief="raised", padx=2)
        y_bottom_frame = tk.Frame(self, width=140, height=130, borderwidth=2, relief="raised", padx=2)
        mean_std_dev_frame = tk.Frame(self, width=100, height=100, borderwidth=2, relief="raised",
                                      padx=2)

        title_label = tk.Label(self, text="Normal distribution parameters", font="Arial 14")

        x_label = tk.Label(self, text="x", font="Arial 12")
        y_label = tk.Label(self, text="y", font="Arial 12")
        x1_label = tk.Label(self, text="x1", font="Arial 9")
        x2_label = tk.Label(self, text="x2", font="Arial 9")
        y1_label = tk.Label(self, text="y1", font="Arial 9")
        y2_label = tk.Label(self, text="y2", font="Arial 9")
        mean_label = tk.Label(self, text="Mean:")
        std_dev_label = tk.Label(self, text="Std dev:")
        mean_x1_entry = FloatEntry(self, textvariable=self.string_vars[0][0], width=8)
        mean_x2_entry = FloatEntry(self, textvariable=self.string_vars[0][1], width=8)
        mean_v1_entry = FloatEntry(self, textvariable=self.string_vars[0][2], width=8)
        mean_v2_entry = FloatEntry(self, textvariable=self.string_vars[0][3], width=8)
        std_dev_x1_entry = FloatEntry(self, textvariable=self.string_vars[1][0], width=8)
        std_dev_x2_entry = FloatEntry(self, textvariable=self.string_vars[1][1], width=8)
        std_dev_v1_entry = FloatEntry(self, textvariable=self.string_vars[1][2], width=8)
        std_dev_v2_entry = FloatEntry(self, textvariable=self.string_vars[1][3], width=8)

        title_frame.grid(row=0, column=0, columnspan=5, pady=2, sticky="N")
        x_top_frame.grid(row=1, column=1, columnspan=2, pady=2, sticky="S")
        x_bottom_frame.grid(row=2, column=1, columnspan=2, rowspan=3, pady=2, sticky="S")
        y_top_frame.grid(row=1, column=3, columnspan=2, pady=2, sticky="S")
        y_bottom_frame.grid(row=2, column=3, columnspan=2, rowspan=3, pady=2, sticky="S")

        mean_std_dev_frame.grid(row=3, column=0, rowspan=2, pady=2, sticky="S")
        title_label.grid(row=0, column=0, columnspan=5, pady=2)
        x_label.grid(row=1, column=1, columnspan=2, pady=2)
        y_label.grid(row=1, column=3, columnspan=2, pady=2)
        x1_label.grid(row=2, column=1, pady=2)
        x2_label.grid(row=2, column=2, pady=2)
        y1_label.grid(row=2, column=3, pady=2)
        y2_label.grid(row=2, column=4, pady=2)
        mean_label.grid(row=3, column=0, padx=10, pady=2)
        std_dev_label.grid(row=4, column=0, padx=10, pady=2)

        mean_x1_entry.grid(row=3, column=1, padx=10, pady=10)
        mean_x2_entry.grid(row=3, column=2, padx=10, pady=10)
        mean_v1_entry.grid(row=3, column=3, padx=10, pady=10)
        mean_v2_entry.grid(row=3, column=4, padx=10, pady=10)

        std_dev_x1_entry.grid(row=4, column=1, padx=10, pady=10)
        std_dev_x2_entry.grid(row=4, column=2, padx=10, pady=10)
        std_dev_v1_entry.grid(row=4, column=3, padx=10, pady=10)
        std_dev_v2_entry.grid(row=4, column=4, padx=10, pady=10)
