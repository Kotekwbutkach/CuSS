import numpy as np

from calculation import ParticlesSystemCalculator
from data import ParticlesSystem
from models import ConstantAccelerationModel, CuckerSmaleModel
from presentation import Presenter, VelocityPresenter

number_of_particles = 5
number_of_dimensions = 2
step_limit = 400

particles_system_args = {
    "number_of_particles": number_of_particles,
    "number_of_dimensions": number_of_dimensions,
    "step_limit": step_limit,
    "particles": np.zeros((number_of_particles, step_limit, 3 * number_of_dimensions))}

particles_system_args["particles"][:, 0, 0:2] = np.random.normal(scale=40, loc=200, size=10).reshape((5, 2))
particles_system_args["particles"][:, 0, 2:4] = np.random.normal(scale=20, loc=5, size=10).reshape((5, 2))

particles_system = ParticlesSystem(**particles_system_args)

model = CuckerSmaleModel()

particles_system_calculator = ParticlesSystemCalculator(particles_system, model, 0.1)
particles_system_calculator.calculate()

presenter = VelocityPresenter(particles_system, 600, 800, 20)
presenter.present()
