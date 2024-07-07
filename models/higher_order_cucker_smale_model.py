from typing import Callable

import numpy as np

from data import ParticlesState
from models import OdeModel
from validation import Validate


class HigherOrderCuckerSmaleModel(OdeModel):
    number_of_particles: int
    subset_size: int
    subsets: list[set[int, ...]]
    phi: Callable[[np.ndarray], np.ndarray]

    def __init__(self,
                 number_of_particles: int,
                 subset_size: int = 2,
                 phi: Callable[[float], float] = lambda s: 1/(1 + s ** 2)):
        self.number_of_particles = number_of_particles
        self.subset_size = subset_size
        self.phi = np.vectorize(phi)
        self.subsets = self._get_k_subsets(subset_size, number_of_particles)

    @classmethod
    def _get_k_subsets(cls, k, n):
        Validate(k).is_less_than_or_equal(n)
        if k == n:
            result = [{x for x in range(n)}]
        elif k == 1:
            result = [{x} for x in range(n)]
        else:
            result = cls._get_k_subsets(k, n-1) + [{*x, n-1} for x in cls._get_k_subsets(k-1, n-1)]

        return result

    def calculate_acceleration(self, delta_t: float, previous_particles_state: ParticlesState) -> ParticlesState:
        new_particles_state = previous_particles_state.get_particles()

        subset_central_values = np.array([previous_particles_state.get_average_of_particles(subset) for subset in self.subsets])

        for _n, particle in enumerate(previous_particles_state.particles_range()):
            distance = np.std(
                (subset_central_values - particle)[
                    :,
                    previous_particles_state.position_indices],
                axis=0)
            velocity_difference = (
                subset_central_values - particle)[
                    :,
                    previous_particles_state.velocity_indices]
            acceleration = np.mean(np.multiply(velocity_difference, self.phi(distance)), axis=0)
            new_particles_state[_n, previous_particles_state.acceleration_indices] = acceleration

        return ParticlesState(
            previous_particles_state.number_of_particles,
            previous_particles_state.number_of_dimensions,
            new_particles_state)
