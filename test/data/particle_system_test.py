import unittest

import numpy as np

from data import ParticlesSystem

number_of_particles = 5
step_limit = 10

particle_system_args = {
    "number_of_particles": number_of_particles,
    "step_limit": step_limit,
    "particles": np.array([[[x+10*y, x+10*y, 0] for x in range(step_limit)] for y in range(number_of_particles)])}


class ParticlesSystemTest(unittest.TestCase):
    particles_system: ParticlesSystem

    @classmethod
    def setUpClass(cls):
        cls.particles_system = ParticlesSystem(**particle_system_args)

    def test_at_time_returns_expected_data(self):
        state_0 = self.particles_system.at_step(0)
        np.testing.assert_array_equal(
            state_0.at_particle(0),
            particle_system_args["particles"][0][0])
        np.testing.assert_array_equal(
            state_0.at_particle(number_of_particles-1),
            particle_system_args["particles"][number_of_particles-1][0])
        state_t = self.particles_system.at_step(step_limit-1)
        np.testing.assert_array_equal(
            state_t.at_particle(0),
            particle_system_args["particles"][0][step_limit-1])
        np.testing.assert_array_equal(
            state_t.at_particle(number_of_particles-1),
            particle_system_args["particles"][number_of_particles-1][step_limit-1])

    def test_at_time_raises_expected_error(self):
        with self.assertRaises(TypeError):
            particle = self.particles_system.at_step("foo")
        with self.assertRaises(ValueError):
            particle = self.particles_system.at_step(step_limit)
        with self.assertRaises(ValueError):
            particle = self.particles_system.at_step(-1)

    def test_steps_returns_expected_data(self):
        state_0 = list(self.particles_system.steps())[0]
        np.testing.assert_array_equal(
            state_0.at_particle(0),
            particle_system_args["particles"][0][0])
        np.testing.assert_array_equal(
            state_0.at_particle(number_of_particles-1),
            particle_system_args["particles"][number_of_particles-1][0])
        state_t = list(self.particles_system.steps())[step_limit-1]
        np.testing.assert_array_equal(
            state_t.at_particle(0),
            particle_system_args["particles"][0][step_limit-1])
        np.testing.assert_array_equal(
            state_t.at_particle(number_of_particles-1),
            particle_system_args["particles"][number_of_particles-1][step_limit-1])
        for _s, particles_state in enumerate(self.particles_system.steps()):
            for _n, particle in enumerate(particles_state.particles()):
                np.testing.assert_array_equal(particle, particle_system_args["particles"][_n][_s])

    def test_steps_raises_expected_error(self):
        with self.assertRaises(Exception):
            particle = list(self.particles_system.steps())["foo"]
        with self.assertRaises(Exception):
            particle = list(self.particles_system.steps())[step_limit]


if __name__ == '__main__':
    unittest.main()
