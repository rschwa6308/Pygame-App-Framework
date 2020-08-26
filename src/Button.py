from Text import *
from Fonts import *

from typing import Callable, Any

class Button(Text):
    default_background_color = WHITE
    default_text_color = BLACK

    def __init__(
        self,
        x_flex: int = 1,
        y_flex: int = 1,
        background_color: Tuple[int, int, int] = default_background_color,
        text: str = "",
        text_color: Tuple[int, int, int] = default_text_color,
        # must be a function of the form (self, event) -> any
        on_click: Callable[[View, pygame.event.EventType], Any] = lambda self, event: None,
        **kwargs
    ):
        super().__init__(x_flex, y_flex, background_color, text, text_color, **kwargs)
        self.on_click = on_click
    
    def process_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                print(self)
                self.on_click(self, event)
    
    def render_onto(self, surf: pygame.Surface, region: pygame.Rect = None):
        region = super().render_onto(surf, region)
        # render_text_to(surf, "CENTER", self.text, region=region, fgcolor=self.text_color)
