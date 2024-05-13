import numpy as np

from calculation import ParticlesSystemCalculator
from data import ParticlesSystem
from models import ConstantAccelerationModel
from presentation import Presenter, VelocityPresenter

number_of_particles = 5
number_of_dimensions = 2
step_limit = 400

particles_system_args = {
    "number_of_particles": number_of_particles,
    "number_of_dimensions": number_of_dimensions,
    "step_limit": step_limit,
    "particles": np.array([[
        [x + 10 * y] * number_of_dimensions +
        [x + 2 * y] * number_of_dimensions +
        [0] * number_of_dimensions for x in range(step_limit)] for y in range(number_of_particles)])}

particles_system = ParticlesSystem(**particles_system_args)
model = ConstantAccelerationModel()

particles_system_calculator = ParticlesSystemCalculator(particles_system, model, 0.1)
particles_system_calculator.calculate()

presenter = VelocityPresenter(particles_system, 600, 800, 20)
presenter.present()
