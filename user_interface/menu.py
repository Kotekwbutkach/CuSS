import pygame

from user_interface import Slider
from user_interface.interfaces import ILeftMouseClickable, IDrawable


class Menu(ILeftMouseClickable, IDrawable):
    _rect: pygame.Rect
    _left_mouse_clickables: list[ILeftMouseClickable]
    _drawables: list[IDrawable]
    _background_color: pygame.Color
    _accent_color_1: pygame.Color
    _accent_color_2: pygame.Color
    _accent_color_3: pygame.Color

    def __init__(self,
                 rect: pygame.Rect,
                 background_color: pygame.Color,
                 accent_color_1: pygame.Color,
                 accent_color_2: pygame.Color,
                 accent_color_3: pygame.Color
                 ):
        self._rect = rect
        self._background_color = background_color
        self._accent_color_1 = accent_color_1
        self._accent_color_2 = accent_color_2
        self._accent_color_3 = accent_color_3

        self._left_mouse_clickables = list()
        self._drawables = list()

    def add_slider(self,
                   value: int,
                   min_value: int,
                   max_value: int,
                   rect: pygame.Rect):
        relative_rect = pygame.Rect(
            self._rect.x + rect.x,
            self._rect.y + rect.y,
            rect.size[0],
            rect.size[1]
        )
        slider = Slider(
            value,
            min_value,
            max_value,
            relative_rect,
            self._accent_color_1,
            self._accent_color_2,
            self._accent_color_3)

        self._left_mouse_clickables.append(slider)
        self._drawables.append(slider)
        return self

    def draw(self, surface):
        pygame.draw.rect(surface, self._background_color, self._rect)
        for _d in self._drawables:
            _d.draw(surface)

    def on_left_mouse_key_down(self):
        for _lmc in self._left_mouse_clickables:
            _lmc.on_left_mouse_key_down()

    def on_left_mouse_key_up(self):
        for _lmc in self._left_mouse_clickables:
            _lmc.on_left_mouse_key_up()

    def on_mouse_move(self):
        for _lmc in self._left_mouse_clickables:
            _lmc.on_mouse_move()
