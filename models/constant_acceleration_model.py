import numpy as np

from data import ParticlesState
from models import OdeModel


class ConstantAccelerationModel(OdeModel):

    def calculate_acceleration(self, delta_t: float, previous_particles_state: ParticlesState) -> ParticlesState:
        new_particles_state = previous_particles_state.get_particles()
        new_particles_state[:, previous_particles_state.acceleration_indices] = [1, 0]
        return ParticlesState(
            previous_particles_state.number_of_particles,
            previous_particles_state.number_of_dimensions,
            new_particles_state)


