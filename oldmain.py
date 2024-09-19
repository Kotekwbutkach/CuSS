import sys
import tkinter as tk

import numpy as np
import pygame

from models.ode_model_builder import OdeModelBuilder
from plotting import Plotter
from presentation import Presenter
from user_interface.int_entry import IntEntry
from user_interface.frame.normal_params_frame import NormalParamsFrame

if __name__ == "__main__":

    window = tk.Tk()
    should_start = False

    def start():
        global should_start
        should_start = True
        window.destroy()

    window.title("CoDyS - parameters")

    number_of_particles_str_var = tk.StringVar(value='5')

    number_of_particles_frame = tk.Frame(width=200, height=100)
    number_of_particles_entry = IntEntry(number_of_particles_frame, textvariable=number_of_particles_str_var, width=8)
    number_of_particles_label = tk.Label(number_of_particles_frame, text="Number of particles: ", font="Arial 9")

    number_of_particles_label.grid(row=0, column=0)
    number_of_particles_entry.grid(row=0, column=1)

    normal_params_frame = NormalParamsFrame(window)

    start_button = tk.Button(window, command=start, text="Start")
    normal_distribution_param_string_vars = normal_params_frame.string_vars

    number_of_particles_frame.grid(row=0, column=0)
    normal_params_frame.grid(row=1, column=0)
    start_button.grid(row=2, column=0)
    window.mainloop()

    normal_params = [[[float(index.get()) for index in var] for var in measure_type]
                     for measure_type in normal_distribution_param_string_vars]

    print(normal_params)

    if not should_start:
        sys.exit()

    NUMBER_OF_PARTICLES = int(number_of_particles_str_var.get())
    NUMBER_OF_STEPS = 1000

    initial_condition = np.zeros((2, NUMBER_OF_PARTICLES, 2))
    initial_condition[0, :, 0] = (np.random.normal(normal_params[0][0][0], normal_params[1][0][0], NUMBER_OF_PARTICLES))
    initial_condition[0, :, 1] = (np.random.normal(normal_params[0][0][1], normal_params[1][0][1], NUMBER_OF_PARTICLES))
    initial_condition[1, :, 0] = (np.random.normal(normal_params[0][1][0], normal_params[1][1][0], NUMBER_OF_PARTICLES))
    initial_condition[1, :, 1] = (np.random.normal(normal_params[0][1][1], normal_params[1][1][1], NUMBER_OF_PARTICLES))

    BOUNDS = ((0, 0), (600, 600))

    models = [
        OdeModelBuilder()
        .with_default_phi_function(5, 2)
        .with_default_distance_function()
        .with_higher_order_cucker_smale_model(k)
        .build_for_time_step(0.05)
        for k in range(1, 3)]

    trajectories = [model.calculate_trajectory(
        initial_condition,
        NUMBER_OF_STEPS) for model in models]

    colored_trajectories = list(zip(
        trajectories,
        [pygame.Color("red"),
         pygame.Color("green"),
         pygame.Color("blue"),
         pygame.Color("orange")]))

    presenter = Presenter(colored_trajectories)
    presenter.present()

    plotter = Plotter(colored_trajectories,
                      ["model standardowy", "model rzędu 2", "model rzędu 3", "model rzędu 4"],
                      ".\\plots\\simulation_1")
    plotter.plot()
