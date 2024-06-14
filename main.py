import os

import numpy as np

from calculation import ParticlesSystemCalculator
from data import ParticlesSystem
from models import CuckerSmaleModel
from plotting.plotter import Plotter
from presentation import Presenter

number_of_particles = 5
number_of_dimensions = 2
step_limit = 400

particles_system_args = {
    "number_of_particles": number_of_particles,
    "number_of_dimensions": number_of_dimensions,
    "step_limit": step_limit,
    "particles": np.zeros((number_of_particles, step_limit + 1, 3 * number_of_dimensions))}

particles_system_args["particles"][:, 0, 0:2] = (
    np.random.normal(
        scale=40,
        loc=0,
        size=number_of_particles*number_of_dimensions)
    .reshape((number_of_particles, number_of_dimensions)))
particles_system_args["particles"][:, 0, 2:4] = (
    np.random.normal(
        scale=40,
        loc=0,
        size=number_of_particles * number_of_dimensions)
    .reshape((number_of_particles, number_of_dimensions)))

particles_system = ParticlesSystem(**particles_system_args)

model = CuckerSmaleModel()

particles_system_calculator = ParticlesSystemCalculator(particles_system, model, 0.1)
particles_system_calculator.calculate()

presenter = Presenter(
    particles_system,
    width=800,
    height=600,
    fps=20,
    should_draw_velocity=True)
presenter.present()

particles_system.get_bounds()

presenter.get_data_to_view_transform()(tuple(particles_system.at_step(0).at_particle(0)[0:2]))

plotter = Plotter(particles_system, os.path.join(os.getcwd(), 'plots', 'simulation_1'))
plotter.plot_values()
plotter.plot_std_dev()
