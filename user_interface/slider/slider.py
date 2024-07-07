import pygame

from user_interface.interfaces import ILeftMouseClickable, IDrawable


class Slider(ILeftMouseClickable, IDrawable):
    rect: pygame.Rect
    _panel_color: pygame.Color
    _rail_color: pygame.Color
    _knob_color: pygame.Color
    _margin: int
    _rail_height: int
    _knob_width: int
    _rail_start: int
    _rail_end: int

    _min_value: int
    _max_value: int
    _value: int
    selected: bool

    def __init__(self,
                 value: int,
                 min_value: int,
                 max_value: int,
                 rect: pygame.Rect,
                 panel_color: pygame.Color,
                 rail_color: pygame.Color,
                 knob_color: pygame.Color,
                 margin: int = 20,
                 rail_height: int = 10,
                 knob_width: int = 20):
        self._min_value = min_value
        self._max_value = max_value
        self.set_value(value)

        self.rect = rect
        self._panel_color = panel_color
        self._rail_color = rail_color
        self._knob_color = knob_color
        self._margin = margin
        self._rail_height = rail_height
        self._knob_width = knob_width
        self._rail_start = self.rect.x + margin + knob_width/2
        self._rail_end = self.rect.x + self.rect.size[0] - margin - knob_width/2
        self._selected = False

    def get_value(self):
        return self._value

    def set_value(self, value):
        self._value = min(self._max_value, max(self._min_value, value))

    def _value_to_position(self, value: int):
        return (self._rail_start + (value - self._min_value) /
                (self._max_value - self._min_value) * (self._rail_end - self._rail_start))

    def _position_to_value(self, mouse_position: int):
        if mouse_position <= self._rail_start:
            return self._min_value
        if mouse_position >= self._rail_end:
            return self._max_value
        return round(self._min_value + (mouse_position - self._rail_start) /
                     (self._rail_end - self._rail_start) * (self._max_value - self._min_value))

    def draw(self, surface: pygame.Surface):
        pygame.draw.rect(surface, self._panel_color, self.rect)
        rail = pygame.Rect(0, 0, 0, 0)
        rail.width = self.rect.size[0] - 2 * self._margin
        rail.height = self._rail_height
        rail.center = self.rect.center
        pygame.draw.rect(surface, self._rail_color, rail)
        knob = pygame.Rect(0, 0, self._knob_width, self.rect.size[1] - 2 * self._margin)
        knob.center = self._value_to_position(self._value), self.rect.centery
        pygame.draw.rect(surface, self._knob_color, knob)

    def on_left_mouse_key_down(self):
        if self.rect.contains(pygame.Rect(*pygame.mouse.get_pos(), 0, 0)):
            self._selected = True

    def on_left_mouse_key_up(self):
        self._selected = False

    def on_mouse_move(self):
        if self._selected:
            self._value = self._position_to_value(pygame.mouse.get_pos()[0])
