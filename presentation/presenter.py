import pygame
from pygame import Surface

from data import ParticlesSystem
from validation import Validate


class Presenter:
    width: int
    height: int
    fps: int
    particles_system: ParticlesSystem

    def __init__(self,
                 particles_system: ParticlesSystem,
                 width: int = 800,
                 height: int = 600,
                 fps: int = 20):
        self.particles_system = particles_system
        self.width = width
        self.height = height
        self.fps = fps

    def present_step(self, surface: Surface, step: int):
        Validate(step).is_type(int)
        Validate(step).is_less_than_or_equal(self.particles_system.step_limit)
        Validate(self.particles_system.number_of_dimensions).is_equal_to(2)
        for particle in self.particles_system.at_step(step).particles_range():
            particle_position = particle[0], particle[1]
            pygame.draw.circle(surface, pygame.Color("white"), particle_position, 5)

    def present(self):
        pygame.init()
        pygame.display.set_mode((800, 600))
        surface = pygame.display.get_surface()
        pygame.display.set_caption('CuSS')
        # TODO pygame.display.set_icon()

        clock = pygame.time.Clock()
        running = True

        step = 0
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            surface.fill(pygame.Color("black"))
            self.present_step(surface, step)
            pygame.display.flip()
            if step < self.particles_system.step_limit - 1:
                step += 1
            clock.tick(self.fps)
