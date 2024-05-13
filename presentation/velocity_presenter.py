import numpy as np
import pygame

from presentation import Presenter


class VelocityPresenter(Presenter):
    def _draw_particle(self, particle: np.ndarray):
        pygame.draw.circle(self.surface,
                           pygame.Color("white"),
                           (particle[0], particle[1]),
                           5)
        pygame.draw.line(self.surface,
                         pygame.Color("red"),
                         (particle[0], particle[1]),
                         (particle[0] + particle[2], particle[1] + particle[3]))
