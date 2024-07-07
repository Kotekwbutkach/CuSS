import tkinter as tk


class MainMenu:
    number_of_particles: int
    step_limit: int

    mean: tuple[float, float]
    std_dev: tuple[float, float]

    def __init__(
            self,
            number_of_particles: int,
            step_limit: int,
            mean: tuple[float, float],
            std_dev: tuple[float, float]):
        self.number_of_particles = number_of_particles
        self.step_limit = step_limit

        self.mean = mean
        self.std_dev = std_dev

    def run(self):
        window = tk.Tk()

        self._pack_title(window)

        main_frame = tk.Frame(
            relief=tk.RIDGE,
            padx=5,
            pady=5,
            borderwidth=5
        )

        particles_string_var = self._pack_input_field(main_frame, "Number of particles: ", 5)
        particles_string_var.set(str(self.number_of_particles))

        random_params_frame = tk.Frame(
            main_frame,
            relief=tk.RIDGE,
            padx=5,
            pady=5,
            borderwidth=5
        )

        random_params_label = tk.Label(
            random_params_frame,
            text="Normal distribution parameters",
            font="Arial"
        )
        random_params_label.pack()

        random_params_frame = tk.Frame(
            main_frame,
            relief=tk.RIDGE,
            padx=5,
            pady=5,
            borderwidth=5
        )

        mean_x_string_var, mean_y_string_var = self._pack_input_field(random_params_frame, "Mean (x, y): ", 10)
        std_dev_x_string_var, std_dev_y_string_var = self._pack_input_field(random_params_frame, "Std dev (x, y): ", 10)

        mean_x_string_var.set(str(self.mean[0]))
        mean_y_string_var.set(str(self.mean[1]))
        std_dev_x_string_var.set(str(self.std_dev[0]))
        std_dev_y_string_var.set(str(self.std_dev[1]))

        random_params_frame.pack(side=tk.LEFT)

        start_frame = tk.Frame(
            main_frame,
            relief=tk.RIDGE,
            padx=5,
            pady=5,
            borderwidth=5
        )

        start_button = tk.Button(
            start_frame,
            bd=4,
            text="Start",
            font="Arial",
            width="10",
            height="1",
            background="blue",
            activebackground="darkblue"
        )

        start_button.pack()
        start_frame.pack(side=tk.RIGHT)
        main_frame.columnconfigure((0, 1), weight=10, pad=50)
        main_frame.pack()

        window.mainloop()

        self.number_of_particles = int(particles_string_var.get())
        self.mean = float(mean_x_string_var.get()), float(mean_y_string_var.get())
        self.std_dev = float(std_dev_x_string_var.get()), float(std_dev_y_string_var.get())

    @staticmethod
    def _pack_title(parent: tk.Tk | tk.Frame):
        frame = tk.Frame(
            parent,
            relief=tk.RIDGE,
            padx=5,
            pady=5,
            borderwidth=5
        )

        label = tk.Label(
            frame,
            text="Welcome to CoDyS - Collective Dynamics Simulator",
            font="Arial"
        )

        label.pack()
        frame.pack()

    @staticmethod
    def _pack_normal_random_params(
            parent: tk.Tk | tk.Frame,
            label_text: str,
            entry_width: int
    ):
        frame = tk.Frame(
            parent,
            borderwidth=5
        )

        label = tk.Label(
            frame,
            text=label_text,
            font="Arial",
        )
        label.pack(side=tk.LEFT)

        entry_value = tk.StringVar()
        entry = tk.Entry(
            frame,
            bd=2,
            width=entry_width,
            textvariable=entry_value
        )
        entry.pack(side=tk.RIGHT)

        frame.pack()
        return entry_value

    @staticmethod
    def _pack_input_field(
            parent: tk.Tk | tk.Frame,
            label_text: str,
            entry_width: int
    ):
        frame = tk.Frame(
            parent,
            borderwidth=5
        )

        label = tk.Label(
            frame,
            text=label_text,
            font="Arial",
        )
        label.pack(side=tk.LEFT)

        entry_value = tk.StringVar()
        entry = tk.Entry(
            frame,
            bd=2,
            width=entry_width,
            textvariable=entry_value
        )
        entry.pack(side=tk.RIGHT)

        frame.pack()
        return entry_value
