import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"   # grrr

import pygame

class Component:
    def __init__(self, x_flex: int = 1, y_flex: int = 1):
        self.x_flex = x_flex
        self.y_flex = y_flex

    def render_onto(self, surf: pygame.Surface):
        """Render the contents of self to the given surface"""
        raise NotImplementedError("Component subclass must implement the render_onto() method")

    def on_mount(self):
        """Called immediately before component is mounted to a Hoster"""
        pass

    def on_unmount(self):
        """Called immediately after component is unmounted from a Hoster"""
        pass
