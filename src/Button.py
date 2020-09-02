from Text import *
from Fonts import *

from typing import Callable, Any

class Button(Text):
    default_background_color = WHITE
    default_text_color = BLACK

    hover_opacity = 0.75
    press_opacity = 0.5
    # opacity_color = (*BLACK, 127)

    rerender_on_hover = True
    rerender_on_press = True

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
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.ui_state["press"]:
                self.on_click(self, event)
    
    def render_onto(self, surf: pygame.Surface, region: pygame.Rect = None):
        temp = self.background_color

        if self.ui_state["press"]:
            self.background_color = tuple(x * self.press_opacity for x in temp)
        elif self.ui_state["hover"]:
            self.background_color = tuple(x * self.hover_opacity for x in temp)

        
        region = super().render_onto(surf, region)
        self.background_color = temp

