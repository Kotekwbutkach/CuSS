from abc import abstractmethod

import numpy as np

from data import ParticlesState


class OdeModel:
    def calculate_new_particles_state(self, delta_t: float, previous_particles_state: ParticlesState) -> ParticlesState:
        particles_state = self.calculate_acceleration(delta_t, previous_particles_state)
        particles_state = self.calculate_velocity(delta_t, particles_state)
        particles_state = self.calculate_position(delta_t, particles_state)
        return particles_state

    @abstractmethod
    def calculate_acceleration(self, delta_t: float, particles_state: ParticlesState) -> ParticlesState:
        pass

    def calculate_velocity(self, delta_t: float, particles_state: ParticlesState) -> ParticlesState:
        for particle in particles_state.particles_range():
            particle[particles_state.velocity_indices] = (
                particle[particles_state.velocity_indices] +
                particle[particles_state.acceleration_indices] * delta_t)
        return particles_state

    def calculate_position(self, delta_t: float, particles_state: ParticlesState) -> ParticlesState:
        for particle in particles_state.particles_range():
            particle[particles_state.position_indices] = (
                particle[particles_state.position_indices] +
                particle[particles_state.velocity_indices] * delta_t +
                particle[particles_state.acceleration_indices] * ((delta_t ** 2)/2))
        return particles_state
