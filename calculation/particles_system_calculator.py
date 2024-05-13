from data import ParticlesSystem
from models import OdeModel
from validation import Validate


class ParticlesSystemCalculator:
    particles_system: ParticlesSystem
    model: OdeModel
    current_step: int
    delta_t: float

    def __init__(self, particles_system: ParticlesSystem, model: OdeModel, delta_t: float):
        Validate(particles_system).is_type(ParticlesSystem)
        Validate(model).is_type(OdeModel)
        Validate(delta_t).is_type(float)
        self.particles_system = particles_system
        self.model = model
        self.current_step = 0
        self.delta_t = delta_t

    def calculate_step(self):
        previous_particle_state = self.particles_system.at_step(self.current_step)
        new_particle_state = self.model.calculate_new_particles_state(self.delta_t, previous_particle_state)
        self.current_step += 1
        self.particles_system.set_step(self.current_step, new_particle_state)

    def calculate(self):
        while self.current_step < (self.particles_system.step_limit - 1):
            self.calculate_step()
