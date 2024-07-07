import sys
import tkinter as tk

import numpy as np

from calculation import ParticlesSystemCalculator
from data import ParticlesSystem
from models import CuckerSmaleModel, HigherOrderCuckerSmaleModel
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

    if not should_start:
        sys.exit()

    STEP_LIMIT = 400

    normal_distribution_params = np.array([
        [float(var.get()) if var.get() != '' else i
         for var in row]
        for i, row in enumerate(normal_distribution_param_string_vars)])
    number_of_particles = int(number_of_particles_str_var.get())
    step_limit = STEP_LIMIT

    particles_system_args = {
        "number_of_particles": number_of_particles,
        "number_of_dimensions": 2,
        "step_limit": step_limit,
        "particles": np.zeros((number_of_particles, step_limit + 1, 6))}

    particles_system_args["particles"][:, 0, 0] = (
        np.random.normal(
            loc=normal_distribution_params[0][0],
            scale=normal_distribution_params[1][0],
            size=number_of_particles))
    particles_system_args["particles"][:, 0, 1] = (
        np.random.normal(
            loc=normal_distribution_params[0][1],
            scale=normal_distribution_params[1][1],
            size=number_of_particles))

    particles_system_args["particles"][:, 0, 2] = (
        np.random.normal(
            loc=normal_distribution_params[0][2],
            scale=normal_distribution_params[1][2],
            size=number_of_particles))

    particles_system_args["particles"][:, 0, 3] = (
        np.random.normal(
            loc=normal_distribution_params[0][3],
            scale=normal_distribution_params[1][3],
            size=number_of_particles))

    particles_system1 = ParticlesSystem(**particles_system_args)
    model1 = CuckerSmaleModel()

    particles_system_calculator1 = ParticlesSystemCalculator(particles_system1, model1, 0.1)
    particles_system_calculator1.calculate()

    presenter1 = Presenter(
        particles_system1,
        width=800,
        height=600,
        fps=30,
        should_draw_velocity=True,
        trajectory_shadow=100)
    presenter1.present()

    particles_system2 = ParticlesSystem(**particles_system_args)
    model2 = HigherOrderCuckerSmaleModel(number_of_particles, 4)

    particles_system_calculator2 = ParticlesSystemCalculator(particles_system2, model2, 0.1)
    particles_system_calculator2.calculate()

    presenter2 = Presenter(
        particles_system2,
        width=800,
        height=600,
        fps=30,
        should_draw_velocity=True,
        trajectory_shadow=100)
    presenter2.present()
