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
        parent_dest: Tuple[float, float, float, float] = (0, 0, 1, 1),            # (L, T, W, H) (floating point in [0, 1]),
        **kwargs
    ):
        super().__init__(**kwargs)
        self.x_flex = x_flex
        self.y_flex = y_flex
        self.background_color = background_color
        self.border_color = border_color
        self.border_width = border_width
        self.border_radius = border_radius
        self.margins = margins
        self.parent_dest = parent_dest

        self.child_regions_cache = []   # format (Component, Rect)
    
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
            pygame.draw.rect(                                   # fill background
                surf, self.background_color, region,
                width=0, border_radius=self.border_radius
            )
            pygame.draw.rect(                                   # draw border
                surf, self.border_color, region,
                width=self.border_width, border_radius=self.border_radius
            )
        else:
            surf.fill(self.background_color, region)            # fill background
        
        # render all children (on top)
        self.child_regions_cache = []                               # clear cache
        for child in self.children:
            child_region = pygame.Rect(
                region.left + region.width * child.parent_dest[0],
                region.top + region.height * child.parent_dest[1],
                region.width * child.parent_dest[2],
                region.height * child.parent_dest[3]
            )
            self.child_regions_cache.append((child, child_region))  # save in cache
            child.render_onto(surf, child_region)

        # return the affected region
        return region
    
    def process_event(self, event):
        # Pass mouse events only to the affected child (with `pos` converted to child's local coordinates)
        if event.type in (pygame.MOUSEMOTION, pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP):
            for child, region in self.child_regions_cache:
                if region.collidepoint(event.pos):
                    # convert `pos` to local coords and include original as `parent_pos`
                    local_pos = (event.pos[0] - region.left, event.pos[1] - region.top)
                    event.pos, event.parent_pos = local_pos, event.pos
                    child.process_event(event)
                    break
