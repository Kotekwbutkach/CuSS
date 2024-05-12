import unittest

import numpy as np

from data import ParticlesState

number_of_particles = 5

particle_state_args = {
    "number_of_particles": number_of_particles,
    "particles": np.array([[x, x, 0] for x in range(number_of_particles)])}


class ParticlesStateTest(unittest.TestCase):
    particles_state: ParticlesState

    @classmethod
    def setUpClass(cls):
        cls.particles_state = ParticlesState(**particle_state_args)

    def test_at_particle_returns_expected_data(self):
        particle_0 = self.particles_state.at_particle(0)
        np.testing.assert_array_equal(particle_0, particle_state_args["particles"][0])
        particle_n = self.particles_state.at_particle(number_of_particles-1)
        np.testing.assert_array_equal(particle_n, particle_state_args["particles"][number_of_particles-1])

    def test_at_particle_raises_expected_error(self):
        with self.assertRaises(TypeError):
            particle = self.particles_state.at_particle("foo")
        with self.assertRaises(ValueError):
            particle = self.particles_state.at_particle(number_of_particles)
        with self.assertRaises(ValueError):
            particle = self.particles_state.at_particle(-1)

    def test_particles_returns_expected_data(self):
        particle_0 = list(self.particles_state.particles())[0]
        np.testing.assert_array_equal(particle_0, particle_state_args["particles"][0])
        particle_n = list(self.particles_state.particles())[number_of_particles-1]
        np.testing.assert_array_equal(particle_n, particle_state_args["particles"][number_of_particles-1])
        for _n, particle in enumerate(self.particles_state.particles()):
            np.testing.assert_array_equal(particle, particle_state_args["particles"][_n])

    def test_particles_raises_expected_error(self):
        with self.assertRaises(Exception):
            particle = list(self.particles_state.particles())["foo"]
        with self.assertRaises(Exception):
            particle = list(self.particles_state.particles())[number_of_particles]


if __name__ == '__main__':
    unittest.main()
