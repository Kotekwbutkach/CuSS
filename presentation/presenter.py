import numpy as np
import pygame
from pygame import Surface

from data import ParticlesSystem
from validation import Validate


class Presenter:
    width: int
    height: int
    fps: int
    particles_system: ParticlesSystem
    surface: Surface = None

    def __init__(self,
                 particles_system: ParticlesSystem,
                 width: int = 800,
                 height: int = 600,
                 fps: int = 20):
        self.particles_system = particles_system
        self.width = width
        self.height = height
        self.fps = fps

    def _draw_particle(self, particle: np.ndarray):
        pygame.draw.circle(self.surface, pygame.Color("white"), (particle[0], particle[1]), 5)

    def _present_step(self, step: int):
        Validate(step).is_type(int)
        Validate(step).is_less_than_or_equal(self.particles_system.step_limit)
        Validate(self.particles_system.number_of_dimensions).is_equal_to(2)
        for particle in self.particles_system.at_step(step).particles_range():
            self._draw_particle(particle)

    def present(self):
        if self.surface is None:
            pygame.init()
            pygame.display.set_mode((800, 600))
            self.surface = pygame.display.get_surface()
            pygame.display.set_caption('CuSS')
            pygame_icon = pygame.image.load("cuss.png")
            pygame.display.set_icon(pygame_icon)

        clock = pygame.time.Clock()
        running = True

        step = 0
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            self.surface.fill(pygame.Color("black"))
            self._present_step(step)
            pygame.display.flip()
            if step < self.particles_system.step_limit - 1:
                step += 1
            clock.tick(self.fps)
