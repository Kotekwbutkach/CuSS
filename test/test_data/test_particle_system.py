import unittest

import numpy as np

from data import ParticlesSystem, ParticlesState

number_of_particles = 5
number_of_dimensions = 2
step_limit = 10

particles_system_args = {
    "number_of_particles": number_of_particles,
    "number_of_dimensions": number_of_dimensions,
    "step_limit": step_limit,
    "particles": np.array([[
        [x+10*y] * number_of_dimensions +
        [x+10*y] * number_of_dimensions +
        [0] * number_of_dimensions for x in range(step_limit)] for y in range(number_of_particles)])}

particles_state_args = {
    "number_of_particles": number_of_particles,
    "number_of_dimensions": number_of_dimensions,
    "particles": np.array([
        [x] * number_of_dimensions +
        [x] * number_of_dimensions +
        [0] * number_of_dimensions for x in range(number_of_particles)])}


class TestParticlesSystem(unittest.TestCase):
    particles_system: ParticlesSystem
    particles_state: ParticlesState

    @classmethod
    def setUpClass(cls):
        cls.particles_system = ParticlesSystem(**particles_system_args)
        cls.particles_state = ParticlesState(**particles_state_args)

    def test_at_time_returns_expected_data(self):
        state_0 = self.particles_system.at_step(0)
        np.testing.assert_array_equal(
            state_0.at_particle(0),
            particles_system_args["particles"][0][0])
        np.testing.assert_array_equal(
            state_0.at_particle(number_of_particles-1),
            particles_system_args["particles"][number_of_particles - 1][0])
        state_t = self.particles_system.at_step(step_limit-1)
        np.testing.assert_array_equal(
            state_t.at_particle(0),
            particles_system_args["particles"][0][step_limit - 1])
        np.testing.assert_array_equal(
            state_t.at_particle(number_of_particles-1),
            particles_system_args["particles"][number_of_particles - 1][step_limit - 1])

    def test_at_time_raises_expected_error(self):
        with self.assertRaises(TypeError):
            _ = self.particles_system.at_step("foo")
        with self.assertRaises(ValueError):
            _ = self.particles_system.at_step(step_limit)
        with self.assertRaises(ValueError):
            _ = self.particles_system.at_step(-1)

    def test_steps_returns_expected_data(self):
        state_0 = list(self.particles_system.steps_range())[0]
        np.testing.assert_array_equal(
            state_0.at_particle(0),
            particles_system_args["particles"][0][0])
        np.testing.assert_array_equal(
            state_0.at_particle(number_of_particles-1),
            particles_system_args["particles"][number_of_particles - 1][0])
        state_t = list(self.particles_system.steps_range())[step_limit - 1]
        np.testing.assert_array_equal(
            state_t.at_particle(0),
            particles_system_args["particles"][0][step_limit - 1])
        np.testing.assert_array_equal(
            state_t.at_particle(number_of_particles-1),
            particles_system_args["particles"][number_of_particles - 1][step_limit - 1])
        for _s, particles_state in enumerate(self.particles_system.steps_range()):
            for _n, particle in enumerate(particles_state.particles_range()):
                np.testing.assert_array_equal(particle, particles_system_args["particles"][_n][_s])

    def test_steps_raises_expected_error(self):
        with self.assertRaises(Exception):
            _ = list(self.particles_system.steps_range())["foo"]
        with self.assertRaises(Exception):
            _ = list(self.particles_system.steps_range())[step_limit]

    def test_set_step_provides_expected_data(self):
        for _s in range(self.particles_system.step_limit):
            self.particles_system.set_step(_s, self.particles_state)
            state = self.particles_system.at_step(_s)
            self.assertEqual(state, self.particles_state)

    def test_set_step_raises_expected_error(self):
        with self.assertRaises(TypeError):
            _ = self.particles_system.set_step("foo", self.particles_state)
        with self.assertRaises(TypeError):
            _ = self.particles_system.set_step(0, "foo")
        with self.assertRaises(ValueError):
            _ = self.particles_system.set_step(step_limit, self.particles_state)
        with self.assertRaises(ValueError):
            _ = self.particles_system.set_step(-1, self.particles_state)


if __name__ == '__main__':
    unittest.main()
