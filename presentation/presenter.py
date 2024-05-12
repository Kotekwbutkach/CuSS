import pygame
from pygame import Surface

from data import ParticlesSystem
from validation import Validate


class Presenter:
    def __init__(self,
                 particles_system: ParticlesSystem):
        self.particles_system = particles_system

    def present_step(self, surface: Surface, step: int):
        Validate(step).is_type(int)
        Validate(step).is_less_than_or_equal(self.particles_system.step_limit)
        Validate(self.particles_system.number_of_dimensions).is_equal_to(2)
        for particle in self.particles_system.at_step(step).particles():
            particle_position = particle[0], particle[1]
            pygame.draw.circle(surface, pygame.Color("white"), particle_position, 5)