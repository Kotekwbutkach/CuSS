import tkinter as tk


class FloatEntry(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master)
        vcmd = (self.register(self.callback))
        w = tk.Entry(self, *args, **kwargs, validate='all', validatecommand=(vcmd, '%P'))
        w.pack()

    def callback(self, p):
        try:
            float(p)
            return True
        except ValueError:
            return p == '' or p == "-"
