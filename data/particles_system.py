from typing import Iterable

import numpy as np

from data import ParticlesState
from validation import Validate


class ParticlesSystem:
    number_of_particles: int
    number_of_dimensions: int
    step_limit: int
    shape: tuple[int, int, int]
    _particles: np.array

    def __init__(self,
                 number_of_particles: int,
                 number_of_dimensions: int,
                 step_limit: int,
                 particles: np.ndarray | None = None):
        Validate(number_of_particles).is_type(int).is_greater_than_or_equal(1)
        Validate(number_of_dimensions).is_type(int).is_greater_than_or_equal(1)
        Validate(step_limit).is_type(int).is_greater_than_or_equal(1)

        self.number_of_particles = number_of_particles
        self.number_of_dimensions = number_of_dimensions
        self.step_limit = step_limit
        self.shape = number_of_particles, step_limit + 1, 3 * number_of_dimensions
        if particles is None:
            self._particles = np.zeros(self.shape)
        else:
            (Validate(particles)
             .is_type(np.ndarray)
             .is_of_shape(self.shape))
            self._particles = np.array(particles, dtype=float)

    def set_step(self, step: int, particles_state: ParticlesState):
        (Validate(step)
         .is_type(int)
         .is_greater_than_or_equal(0)
         .is_less_than_or_equal(self.step_limit))
        Validate(particles_state).is_type(ParticlesState)
        Validate(particles_state.shape).is_equal_to((self.shape[0], self.shape[2]))

        self._particles[:, step, :] = particles_state.get_particles()

    def at_step(self, step: int) -> ParticlesState:
        (Validate(step)
         .is_type(int)
         .is_less_than_or_equal(self.step_limit)
         .is_greater_than_or_equal(0))

        return ParticlesState(self.number_of_particles, self.number_of_dimensions, self._particles[:, step, :])

    def steps_range(self) -> Iterable[ParticlesState]:
        _s = 0

        while _s <= self.step_limit:
            yield ParticlesState(self.number_of_particles, self.number_of_dimensions, self._particles[:, _s, :])
            _s += 1

    def particle_data(self) -> np.ndarray:
        return self._particles.copy()
