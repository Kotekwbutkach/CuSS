import sys
import tkinter as tk

import numpy as np
import pygame

from models.ode_model_builder import OdeModelBuilder
from plotting import Plotter
from presentation import Presenter
from user_interface.int_entry import IntEntry
from user_interface.normal_params_frame import NormalParamsFrame

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

    print([[float(x.get()) for x in var] for var in normal_distribution_param_string_vars])

    if not should_start:
        sys.exit()

    if __name__ == "__main__":
        NUMBER_OF_DIMENSIONS = 2
        NUMBER_OF_PARTICLES = 5
        NUMBER_OF_STEPS = 10000

        initial_condition = np.zeros((2, NUMBER_OF_PARTICLES, NUMBER_OF_DIMENSIONS))
        initial_condition[0:] = (np.random.normal(100, 100, NUMBER_OF_DIMENSIONS * NUMBER_OF_PARTICLES)
                                 .reshape(NUMBER_OF_PARTICLES, NUMBER_OF_DIMENSIONS))
        initial_condition[1:] = (np.random.normal(5, 5, NUMBER_OF_DIMENSIONS * NUMBER_OF_PARTICLES)
                                 .reshape(NUMBER_OF_PARTICLES, NUMBER_OF_DIMENSIONS))

        BOUNDS = ((0, 0), (600, 600))

        standard_model = (
            OdeModelBuilder()
            .with_default_phi_function(1, 2)
            .with_default_distance_function()
            .with_standard_cucker_smale_model()
            .build_for_time_step(0.05))

        higher_order_interactions_model = (
            OdeModelBuilder()
            .with_default_phi_function(1, 2)
            .with_default_distance_function()
            .with_higher_order_cucker_smale_model(2)
            .build_for_time_step(0.05))

        standard_traj = standard_model.calculate_trajectory(
            initial_condition,
            NUMBER_OF_STEPS)
        higher_order_interactions_traj = higher_order_interactions_model.calculate_trajectory(
            initial_condition,
            NUMBER_OF_STEPS)

        trajectories = [
            (standard_traj, pygame.Color("green")),
            (higher_order_interactions_traj, pygame.Color("purple"))]

        presenter = Presenter(trajectories)
        presenter.present()

        plotter = Plotter(trajectories, ".\\plots\\simulation_1")
        plotter.plot()
