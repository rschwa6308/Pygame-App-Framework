from View import *
from Fonts import *

from typing import Callable, Any

class Button(View):
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
        on_click: Callable[[Component, pygame.event.EventType], Any] = lambda self, event: None
    ):
        super().__init__(x_flex, y_flex, background_color)
        
        self.text = text
        self.text_color = text_color

        self.on_click = on_click
    
    def process_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                self.on_click(self, event)
    
    def render_onto(self, surf: pygame.Surface, region: pygame.Rect = None):
        region = super().render_onto(surf, region)
        default_font.render_to(surf, region.topleft, self.text, self.text_color)
