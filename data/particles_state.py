from typing import Union

import numpy as np

from validation import Validate


class ParticlesState:
    number_of_particles: int
    _particles: np.array

    def __init__(self,
                 number_of_particles: int,
                 particles: Union[None, np.array] = None):
        self.number_of_particles = number_of_particles
        if particles is None:
            self._particles = np.zeros((number_of_particles, 3))
        else:
            self._particles = particles

    def at_particle(self, n: int):
        Validate(n).is_type(int)
        Validate(n).is_less_than(self.number_of_particles)
        Validate(n).is_greater_than_or_equal(0)

        return self._particles[n, :]

    def particles(self):
        _n = 0

        while _n < self.number_of_particles:
            yield self._particles[_n, :]
            _n += 1
