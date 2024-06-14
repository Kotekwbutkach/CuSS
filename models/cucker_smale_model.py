from typing import Callable

import numpy as np

from data import ParticlesState
from models import OdeModel


class CuckerSmaleModel(OdeModel):
    phi: Callable[[np.ndarray], np.ndarray]

    def __init__(self, phi: Callable[[float], float] = lambda s: 100/(1 + s ** 1.5)):
        self.phi = np.vectorize(phi)

    def calculate_acceleration(self, delta_t: float, previous_particles_state: ParticlesState) -> ParticlesState:
        new_particles_state = previous_particles_state.get_particles()

        for _n, particle in enumerate(previous_particles_state.particles_range()):
            distance = np.std(
                (previous_particles_state.get_particles() - particle)[
                    :,
                    previous_particles_state.position_indices],
                axis=0)
            velocity_difference = (
                previous_particles_state.get_particles() - particle)[
                    :,
                    previous_particles_state.velocity_indices]
            acceleration = np.mean(np.multiply(velocity_difference, self.phi(distance)), axis=0)
            new_particles_state[_n, previous_particles_state.acceleration_indices] = acceleration

        return ParticlesState(
            previous_particles_state.number_of_particles,
            previous_particles_state.number_of_dimensions,
            new_particles_state)
