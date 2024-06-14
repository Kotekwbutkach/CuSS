import numpy as np
import pygame
from pygame import Surface

from data import ParticlesSystem
from validation import Validate


class Presenter:
    width: int
    height: int
    fps: int
    step: 0
    particles_system: ParticlesSystem
    surface: Surface = None

    should_draw_velocity: bool

    def __init__(self,
                 particles_system: ParticlesSystem,
                 width: int = 800,
                 height: int = 600,
                 fps: int = 20,
                 should_draw_velocity: bool = True
                 ):
        self.particles_system = particles_system
        self.width = width
        self.height = height
        self.fps = fps
        self.step = 0
        self.should_draw_velocity = should_draw_velocity

    def _draw_particle(self, particle: np.ndarray):
        pygame.draw.circle(
            self.surface,
            pygame.Color("white"),
            (particle[0], particle[1]),
            5)

        if self.should_draw_velocity:
            pygame.draw.line(
                self.surface,
                pygame.Color("red"),
                (particle[0], particle[1]),
                (particle[0] + particle[2], particle[1] + particle[3]),
                width=3)

    def _draw_step(self, step: int):
        Validate(step).is_type(int).is_less_than_or_equal(self.particles_system.step_limit)
        Validate(self.particles_system.number_of_dimensions).is_equal_to(2)
        for particle in self.particles_system.at_step(step).particles_range():
            self._draw_particle(particle)

    def _draw_step_text(self, step: int, font: pygame.font):
        Validate(step).is_type(int).is_less_than_or_equal(self.particles_system.step_limit)
        step_text = font.render(f'Step {self.step} of {self.particles_system.step_limit}', False, pygame.Color("white"))
        self.surface.blit(step_text, (0, 0))

    def present(self):
        pygame.init()
        pygame.display.set_mode((800, 600))
        self.surface = pygame.display.get_surface()
        pygame.display.set_caption('CuSS')
        pygame_icon = pygame.image.load("cuss.png")
        pygame.display.set_icon(pygame_icon)

        pygame.font.init()
        font = pygame.font.SysFont('Arial', 20)

        self.surface.fill(pygame.Color("black"))
        self._draw_step(self.step)
        self._draw_step_text(self.step, font)
        pygame.display.flip()

        clock = pygame.time.Clock()
        running = True
        started = False

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        started = True
            if started:
                self.surface.fill(pygame.Color("black"))
                self._draw_step(self.step)
                self._draw_step_text(self.step, font)
                pygame.display.flip()
                if self.step < self.particles_system.step_limit:
                    self.step += 1
                clock.tick(self.fps)
