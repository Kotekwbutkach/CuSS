from typing import Union

import numpy as np

from validation import Validate


class ParticlesState:
    number_of_particles: int
    number_of_dimensions: int
    _particles: np.array

    def __init__(self,
                 number_of_particles: int,
                 number_of_dimensions: int,
                 particles: Union[None, np.array] = None):
        Validate(number_of_particles).is_type(int).is_greater_than_or_equal(1)
        Validate(number_of_dimensions).is_type(int).is_greater_than_or_equal(1)

        self.number_of_particles = number_of_particles
        self.number_of_dimensions = number_of_dimensions
        if particles is None:
            self._particles = np.zeros((number_of_particles, 3 * number_of_dimensions))
        else:
            (Validate(particles)
             .is_type(np.ndarray)
             .is_of_shape((number_of_particles, 3 * number_of_dimensions)))
            self._particles = particles

    def at_particle(self, n: int):
        (Validate(n)
         .is_type(int)
         .is_less_than(self.number_of_particles)
         .is_greater_than_or_equal(0))

        return np.array(self._particles[n, :])

    def particles(self):
        _n = 0

        while _n < self.number_of_particles:
            yield np.array(self._particles[_n, :])
            _n += 1
