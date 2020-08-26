from typing import Tuple, Sequence

from Component import *
from Colors import *


class View(Component):
    default_background_color = WHITE
    default_border_color = BLACK

    def __init__(
        self,
        x_flex: int = 1,
        y_flex: int = 1,
        background_color: Tuple[int, int, int] = default_background_color,
        border_color: Tuple[int, int, int] = default_border_color,
        border_width: int = 0,
        border_radius: int = 0,
        margins: Tuple[int, int, int, int] = (0, 0, 0, 0),  # (N, E, S, W)
        children: Sequence[Component] = []
    ):
        super().__init__(x_flex, y_flex)
        self.background_color = background_color
        self.border_color = border_color
        self.border_width = border_width
        self.border_radius = border_radius
        self.margins = margins
        self.children = children
    
    def render_onto(self, surf: pygame.Surface, region: pygame.Rect = None):
        if region is None:
            region = surf.get_rect()
        
        # adjust region to account for margins
        region = pygame.Rect(
            region.left + self.margins[0],
            region.top + self.margins[1],
            region.width - (self.margins[0] + self.margins[2]),
            region.height - (self.margins[1] + self.margins[3]),
        )

        if self.border_width > 0:
            pygame.draw.rect(                               # fill background
                surf, self.background_color, region,
                width=0, border_radius=self.border_radius
            )
            pygame.draw.rect(                               # draw border
                surf, self.border_color, region,
                width=self.border_width, border_radius=self.border_radius
            )
        else:
            surf.fill(self.background_color, region)        # fill background
        
        # render all children (on top)
        for child in self.children:
            pass
            # TODO!!! decide where parent position should be tracked / abs positioning?

        # return the affected region
        return region
