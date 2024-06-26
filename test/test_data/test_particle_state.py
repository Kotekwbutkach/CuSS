import unittest

import numpy as np

from data import ParticlesState

number_of_particles = 5
number_of_dimensions = 2

particles_state_args = {
    "number_of_particles": number_of_particles,
    "number_of_dimensions": number_of_dimensions,
    "particles": np.array([
        [x] * number_of_dimensions +
        [x] * number_of_dimensions +
        [0] * number_of_dimensions for x in range(number_of_particles)])}


class TestParticlesState(unittest.TestCase):
    particles_state: ParticlesState

    @classmethod
    def setUpClass(cls):
        cls.particles_state = ParticlesState(**particles_state_args)

    def test_at_particle_returns_expected_data(self):
        particle_0 = self.particles_state.at_particle(0)
        np.testing.assert_array_equal(particle_0, particles_state_args["particles"][0])
        particle_n = self.particles_state.at_particle(number_of_particles-1)
        np.testing.assert_array_equal(particle_n, particles_state_args["particles"][number_of_particles - 1])

    def test_at_particle_raises_expected_error(self):
        with self.assertRaises(TypeError):
            _ = self.particles_state.at_particle("foo")
        with self.assertRaises(ValueError):
            _ = self.particles_state.at_particle(number_of_particles)
        with self.assertRaises(ValueError):
            _ = self.particles_state.at_particle(-1)

    def test_particles_returns_expected_data(self):
        particle_0 = list(self.particles_state.particles_range())[0]
        np.testing.assert_array_equal(particle_0, particles_state_args["particles"][0])
        particle_n = list(self.particles_state.particles_range())[number_of_particles - 1]
        np.testing.assert_array_equal(particle_n, particles_state_args["particles"][number_of_particles - 1])
        for _n, particle in enumerate(self.particles_state.particles_range()):
            np.testing.assert_array_equal(particle, particles_state_args["particles"][_n])

    def test_particles_raises_expected_error(self):
        with self.assertRaises(Exception):
            _ = list(self.particles_state.particles_range())["foo"]
        with self.assertRaises(Exception):
            _ = list(self.particles_state.particles_range())[number_of_particles]


if __name__ == '__main__':
    unittest.main()
