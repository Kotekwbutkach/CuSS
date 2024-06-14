import math
from typing import Callable

import numpy as np
import pygame
from pygame import Surface

from data import ParticlesSystem
from validation import Validate


class Presenter:
    ADJUST_BOUNDS_MARGIN = 10
    GRID_GRANULARITY = 100

    width: int
    height: int
    fps: int
    step: 0
    particles_system: ParticlesSystem
    surface: Surface = None

    bounds: [tuple[np.float64, ...]]

    grid_lines: list[tuple[tuple[int, int], tuple[int, int]]]

    _should_draw_velocity: bool
    _should_draw_grid: bool

    data_to_view_transform: Callable[[tuple[np.float64, ...]], tuple[float, ...]]

    def __init__(self,
                 particles_system: ParticlesSystem,
                 width: int = 600,
                 height: int = 600,
                 fps: int = 20,
                 should_draw_velocity: bool = True,
                 should_draw_grid: bool = True,
                 should_adjust_bounds: bool = True
                 ):
        self.particles_system = particles_system
        self.width = width
        self.height = height
        self.fps = fps
        self.step = 0

        self._should_draw_velocity = should_draw_velocity
        self._should_draw_grid = should_draw_grid

        if not should_adjust_bounds:
            self.bounds = np.array([[0, self.width], [0, self.height]])
            self.data_to_view_transform = lambda x: x
        else:
            self.bounds = self.particles_system.get_bounds()
            self.data_to_view_transform = self.get_data_to_view_transform()
        if should_draw_grid:
            gridpoints_x = np.arange(
                math.ceil(self.bounds[0][0]/self.GRID_GRANULARITY) * self.GRID_GRANULARITY,
                self.bounds[0][1],
                self.GRID_GRANULARITY)
            gridpoints_y = np.arange(
                math.ceil(self.bounds[1][0] / self.GRID_GRANULARITY) * self.GRID_GRANULARITY,
                self.bounds[1][1],
                self.GRID_GRANULARITY)
            self.grid_lines = ([(self.data_to_view_transform((x, self.bounds[1][0])),
                                 self.data_to_view_transform((x, self.bounds[1][1]))) for x in gridpoints_x] +
                               [(self.data_to_view_transform((self.bounds[0][0], y)),
                                 self.data_to_view_transform((self.bounds[0][1], y))) for y in gridpoints_y])

    def get_data_to_view_transform(self) -> Callable[[tuple[np.float64, ...]], tuple[float, ...]]:

        def _transform(x: tuple[np.float64, ...]) -> tuple[float, ...]:
            result = [np.interp(
                x[i],
                self.bounds[i, :],
                (self.ADJUST_BOUNDS_MARGIN, (
                    self.width - self.ADJUST_BOUNDS_MARGIN,
                    self.height - self.ADJUST_BOUNDS_MARGIN)[i]))
                for i in range(2)]
            return result
        return _transform

    def _draw_centerpoint(self):
        centerpoint = self.data_to_view_transform((0, 0))

        pygame.draw.line(
            self.surface,
            pygame.Color("gray40"),
            (centerpoint[0] - 10, centerpoint[1]),
            (centerpoint[0] + 10, centerpoint[1]),
            5
        )
        pygame.draw.line(
            self.surface,
            pygame.Color("gray40"),
            (centerpoint[0], centerpoint[1] - 10),
            (centerpoint[0], centerpoint[1] + 10),
            5
        )

    def _draw_particle(self, particle: np.ndarray):
        pygame.draw.circle(
            self.surface,
            pygame.Color("white"),
            self.data_to_view_transform((particle[0], particle[1])),
            5)

        if self._should_draw_velocity:
            pygame.draw.line(
                self.surface,
                pygame.Color("red"),
                self.data_to_view_transform((particle[0], particle[1])),
                self.data_to_view_transform((particle[0] + particle[2], particle[1] + particle[3])),
                width=3)

    def _draw_grid(self):
        for grid_line in self.grid_lines:
            pygame.draw.line(self.surface, pygame.Color("gray20"), *grid_line)

    def _draw_step(self, step: int):
        Validate(step).is_type(int).is_less_than_or_equal(self.particles_system.step_limit)
        Validate(self.particles_system.number_of_dimensions).is_equal_to(2)
        if self._should_draw_grid:
            self._draw_grid()
        self._draw_centerpoint()
        for particle in self.particles_system.at_step(step).particles_range():
            self._draw_particle(particle)

    def _draw_step_text(self, step: int, font: pygame.font):
        Validate(step).is_type(int).is_less_than_or_equal(self.particles_system.step_limit)
        step_text = font.render(f'Step {self.step} of {self.particles_system.step_limit}', False, pygame.Color("white"))
        self.surface.blit(step_text, (0, 0))

    def present(self):
        pygame.init()
        pygame.display.set_mode((self.width, self.height))
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
