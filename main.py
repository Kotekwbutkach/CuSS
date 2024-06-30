import tkinter as tk

import numpy as np

from calculation import ParticlesSystemCalculator
from data import ParticlesSystem
from models import CuckerSmaleModel, HigherOrderCuckerSmaleModel
from presentation import Presenter
from user_interface.float_entry import FloatEntry

window = tk.Tk()
window.title("CoDyS - parameters")

normal_params_frame = tk.Frame()

normal_distribution_string_vars = [[tk.StringVar() for _ in range(4)] for i in range(2)]
for i, row in enumerate(normal_distribution_string_vars):
    for str_var in row:
        str_var.set(str(i))

title_frame = tk.Frame(normal_params_frame, width=390, height=50, borderwidth=2, relief="raised", padx=2)
x_top_frame = tk.Frame(normal_params_frame, width=140, height=30, borderwidth=2, relief="raised", padx=2)
x_bottom_frame = tk.Frame(normal_params_frame, width=140, height=130, borderwidth=2, relief="raised", padx=2)
y_top_frame = tk.Frame(normal_params_frame, width=140, height=30, borderwidth=2, relief="raised", padx=2)
y_bottom_frame = tk.Frame(normal_params_frame, width=140, height=130, borderwidth=2, relief="raised", padx=2)
mean_std_dev_frame = tk.Frame(normal_params_frame, width=100, height=100, borderwidth=2, relief="raised", padx=2)

title_label = tk.Label(normal_params_frame, text="Normal distribution parameters", font="Arial 14")

x_label = tk.Label(normal_params_frame, text="x", font="Arial 12")
y_label = tk.Label(normal_params_frame, text="y", font="Arial 12")
x1_label = tk.Label(normal_params_frame, text="x1", font="Arial 9")
x2_label = tk.Label(normal_params_frame, text="x2", font="Arial 9")
y1_label = tk.Label(normal_params_frame, text="y1", font="Arial 9")
y2_label = tk.Label(normal_params_frame, text="y2", font="Arial 9")
mean_label = tk.Label(normal_params_frame, text="Mean:")
std_dev_label = tk.Label(normal_params_frame, text="Std dev:")
mean_x1_entry = FloatEntry(normal_params_frame, textvariable=normal_distribution_string_vars[0][0], width=8)
mean_x2_entry = FloatEntry(normal_params_frame, textvariable=normal_distribution_string_vars[0][1], width=8)
mean_v1_entry = FloatEntry(normal_params_frame, textvariable=normal_distribution_string_vars[0][2], width=8)
mean_v2_entry = FloatEntry(normal_params_frame, textvariable=normal_distribution_string_vars[0][3], width=8)
std_dev_x1_entry = FloatEntry(normal_params_frame, textvariable=normal_distribution_string_vars[1][0], width=8)
std_dev_x2_entry = FloatEntry(normal_params_frame, textvariable=normal_distribution_string_vars[1][1], width=8)
std_dev_v1_entry = FloatEntry(normal_params_frame, textvariable=normal_distribution_string_vars[1][2], width=8)
std_dev_v2_entry = FloatEntry(normal_params_frame, textvariable=normal_distribution_string_vars[1][3], width=8)
start_button = tk.Button(normal_params_frame, command=window.destroy, text="Start")


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
start_button.grid(row=5, column=0, columnspan=5)

normal_params_frame.pack()
window.mainloop()

NUMBER_OF_PARTICLES = 5
STEP_LIMIT = 400

normal_distribution_params = np.array([
    [float(var.get()) if var.get() != '' else i
     for var in row]
    for i, row in enumerate(normal_distribution_string_vars)])
number_of_particles = NUMBER_OF_PARTICLES
step_limit = STEP_LIMIT

print(normal_distribution_params)

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
