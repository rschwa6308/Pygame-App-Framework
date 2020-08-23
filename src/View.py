from typing import Tuple

from Component import *
from Colors import *


class View(Component):
    default_background_color = WHITE

    def __init__(
        self,
        x_flex: int = 1,
        y_flex: int = 1,
        background_color: Tuple[int, int, int] = default_background_color
    ):
        super().__init__(x_flex, y_flex)
        self.background_color = background_color
    
    def render_onto(self, surf: pygame.Surface, region: pygame.Rect = None):
        if region is None:
            region = surf.get_rect()

        surf.fill(self.background_color, region)

        # return the affected region
        return region
