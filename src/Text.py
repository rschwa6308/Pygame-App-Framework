from View import *
from Fonts import *


class Text(View):
    default_background_color = WHITE
    default_text_color = BLACK

    def __init__(
        self,
        x_flex: int = 1,
        y_flex: int = 1,
        background_color: Tuple[int, int, int] = default_background_color,
        text: str = "",
        text_color: Tuple[int, int, int] = default_text_color,
        **kwargs
        # TODO: add font options here
    ):
        super().__init__(x_flex, y_flex, background_color, **kwargs)
        
        self.text = text
        self.text_color = text_color
    
    def render_onto(self, surf: pygame.Surface, region: pygame.Rect = None):
        region = super().render_onto(surf, region)
        render_text_to(surf, "CENTER", self.text, region=region, fgcolor=self.text_color)
