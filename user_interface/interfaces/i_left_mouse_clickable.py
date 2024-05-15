from abc import abstractmethod


class ILeftMouseClickable:
    @abstractmethod
    def on_left_mouse_key_down(self):
        pass

    @abstractmethod
    def on_left_mouse_key_up(self):
        pass

    @abstractmethod
    def on_mouse_move(self):
        pass
