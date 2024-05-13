import numpy as np
import pygame

from calculation import ParticlesSystemCalculator
from data import ParticlesSystem
from models import ConstantAccelerationModel
from presentation import Presenter, VelocityPresenter

if __name__ == "__main__":
    number_of_particles = 5
    number_of_dimensions = 2
    step_limit = 200

    particles_system_args = {
        "number_of_particles": number_of_particles,
        "number_of_dimensions": number_of_dimensions,
        "step_limit": step_limit,
        "particles": np.array([[
            [x + 10 * y] * number_of_dimensions +
            [x + 2 * y] * number_of_dimensions +
            [0] * number_of_dimensions for x in range(step_limit)] for y in range(number_of_particles)])}

    particles_system = ParticlesSystem(**particles_system_args)

    def phi(s: float):
        return 1/(1 + s ** 2)

    arrphi = np.vectorize(phi)

    for _n, particle in enumerate(particles_system.at_step(0).particles_range()):
        distance = np.std(
            (particles_system.at_step(0).get_particles() - particle)[:, particles_system.at_step(0).position_indices])
        velocity_difference = (
                particles_system.at_step(0).get_particles() - particle)[:, particles_system.at_step(0).velocity_indices]
        acceleration = np.mean(np.multiply(velocity_difference, arrphi(distance)), axis=0)
        particle[particles_system.at_step(0).acceleration_indices] = acceleration

    # model = ConstantAccelerationModel()
    #
    # particles_system_calculator = ParticlesSystemCalculator(particles_system, model, 0.1)
    # particles_system_calculator.calculate()

