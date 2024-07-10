import os

import numpy as np

from calculation import ParticlesSystemCalculator
from data import ParticlesSystem
from models import CuckerSmaleModel
from models.old_models.higher_order_cucker_smale_model import HigherOrderCuckerSmaleModel
from plotting.plotter import Plotter
from presentation import Presenter

number_of_particles = 20
number_of_dimensions = 2
step_limit = 400

particles_system_args = {
    "number_of_particles": number_of_particles,
    "number_of_dimensions": number_of_dimensions,
    "step_limit": step_limit,
    "particles": np.zeros((number_of_particles, step_limit + 1, 3 * number_of_dimensions))}

particles_system_args["particles"][:, 0, 0:2] = (
    np.random.normal(
        scale=10,
        loc=0,
        size=number_of_particles*number_of_dimensions)
    .reshape((number_of_particles, number_of_dimensions)))
particles_system_args["particles"][:, 0, 2:4] = (
    np.random.normal(
        scale=1,
        loc=0,
        size=number_of_particles * number_of_dimensions)
    .reshape((number_of_particles, number_of_dimensions)))

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

plotter = Plotter(particles_system1, os.path.join(os.getcwd(), 'plots', 'simulation_1'))
plotter.plot_values()
plotter.plot_std_dev()

plotter = Plotter(particles_system2, os.path.join(os.getcwd(), 'plots', 'simulation_2'))
plotter.plot_values()
plotter.plot_std_dev()
