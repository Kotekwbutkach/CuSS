from typing import Union

import numpy as np

from data import ParticlesState
from validation import Validate


class ParticlesSystem:
    number_of_particles: int
    number_of_dimensions: int
    step_limit: int
    current_step: int
    _particles: np.array

    def __init__(self,
                 number_of_particles: int,
                 number_of_dimensions: int,
                 step_limit: int,
                 particles: Union[None, np.array] = None):
        self.number_of_particles = number_of_particles
        self.number_of_dimensions = number_of_dimensions
        self.step_limit = step_limit
        self.current_step = 0
        if particles is None:
            self._particles = np.zeros((number_of_particles, step_limit, 3 * number_of_dimensions))
        else:
            Validate(particles).is_of_shape((number_of_particles, step_limit, 3 * number_of_dimensions))
            self._particles = particles

    def at_step(self, step: int):
        Validate(step).is_type(int)
        Validate(step).is_less_than(self.step_limit)
        Validate(step).is_greater_than_or_equal(0)

        return ParticlesState(self.number_of_particles, self.number_of_dimensions, self._particles[:, step, :])

    def steps(self):
        _s = 0

        while _s < self.step_limit:
            yield ParticlesState(self.number_of_particles, self.number_of_dimensions, self._particles[:, _s, :])
            _s += 1
