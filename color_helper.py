import pygame


class ColorHelper:
    @staticmethod
    def mix(color1: tuple[int, int, int] | pygame.Color,
            color2: tuple[int, int, int] | pygame.Color,
            a1: int = 1,
            a2: int = 2):
        return tuple((a1 * color1[i] + a2 * color2[i]) // (a1 + a2) for i in range(3))
