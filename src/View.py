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
        children: Sequence[Component] = [],
        parent_dest: pygame.Rect = None     # a rect with all coords and dims in [0, 1]
    ):
        super().__init__(x_flex, y_flex)
        self.background_color = background_color
        self.border_color = border_color
        self.border_width = border_width
        self.border_radius = border_radius
        self.margins = margins
        self.children = children
        self.parent_dest = parent_dest
    
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
        # TODO: store child_regions_cache here vvv
        for child in self.children:
            child_region = pygame.Rect(
                region.left * self.parent_dest.left,
                region.top * self.parent_dest.top,
                region.width * self.parent_dest.width,
                region.height * self.parent_dest.height
            )
            child.render_onto(surf, child_region)

        # return the affected region
        return region
