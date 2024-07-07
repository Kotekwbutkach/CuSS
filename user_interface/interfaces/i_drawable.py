from abc import abstractmethod

import pygame


class IDrawable:
    rect: pygame.Rect

    @abstractmethod
    def draw(self, surface: pygame.Surface):
        pass
