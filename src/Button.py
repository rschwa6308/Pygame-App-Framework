from Text import *
from Fonts import *

from typing import Callable, Any

class Button(Text):
    default_bg_color = WHITE
    default_text_color = BLACK

    hover_opacity = 0.75
    press_opacity = 0.5

    rerender_ui_triggers = {
        "hover": True,
        "press": True
    }

    def __init__(
        self,
        x_flex: int = 1,
        y_flex: int = 1,
        bg_color: Tuple[int, int, int] = default_bg_color,
        text: str = "",
        text_color: Tuple[int, int, int] = default_text_color,
        # must be a function of the form (self, event) -> any
        on_click: Callable[[View, pygame.event.EventType], Any] = lambda self, event: None,
        **kwargs
    ):
        super().__init__(x_flex, y_flex, bg_color, text, text_color, **kwargs)
        self.on_click = on_click
    
    def process_event(self, event):
        super().process_event(event)

        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            # We can trust that the parent will only pass valid events
            self.on_click(self, event)
    
    def render_onto(self, surf: pygame.Surface, region: pygame.Rect = None):
        # print(f"{self.text}: {self.ui_state['hover']}")

        temp = self.bg_color

        if self.ui_state["press"]:
            self.bg_color = tuple(x * self.press_opacity for x in temp)
        elif self.ui_state["hover"]:
            self.bg_color = tuple(x * self.hover_opacity for x in temp)

        
        region = super().render_onto(surf, region)
        self.bg_color = temp

