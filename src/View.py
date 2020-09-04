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
        border_radius: int = 1,
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
        self.ui_state = {
            "hover": False,
            "press": False
        }
        self.hover_child = None
        self.press_child = None
    
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
        self.child_regions_cache = []                                   # clear cache
        for child in self.children:
            child_region = pygame.Rect(
                region.width * child.parent_dest[0],
                region.height * child.parent_dest[1],
                region.width * child.parent_dest[2],
                region.height * child.parent_dest[3]
            )
            child_region_abs = pygame.Rect(
                region.left + region.width * child.parent_dest[0],
                region.top + region.height * child.parent_dest[1],
                region.width * child.parent_dest[2],
                region.height * child.parent_dest[3]
            )

            self.child_regions_cache.append((child, child_region))      # save in cache
            child.render_onto(surf, child_region_abs)

        # return the affected region
        return region
    
    def process_event(self, event):
        # print(f"{self}.process_event({event})")
        # Handle all mouse events
        if event.type in (pygame.MOUSEMOTION, pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP):
            new_hover_child = None

            # find new hover child
            for child, region in self.child_regions_cache:
                if region.collidepoint(event.pos):
                    new_hover_child = child
                    # convert `pos` to local coords and include original as `parent_pos` and process event
                    local_pos = (event.pos[0] - region.left, event.pos[1] - region.top)
                    converted_event = event
                    converted_event.pos, converted_event.parent_pos = local_pos, event.pos
                    break
            
            # print(f"{self}'s NEW HOVER CHILD: {new_hover_child}")

            # Pass mouse-motion events only to the affected child and handle hover changes
            if event.type == pygame.MOUSEMOTION:
                if new_hover_child is not None:
                    new_hover_child.process_event(converted_event)
                # handle hover changes
                if self.hover_child is None and new_hover_child is None:
                    pass
                elif self.hover_child is None:
                    new_hover_child.set_ui_state("hover", True)
                elif new_hover_child is None:
                    self.hover_child.set_ui_state("hover", False)
                elif self.hover_child is not new_hover_child:
                    self.hover_child.set_ui_state("hover", False)
                    new_hover_child.set_ui_state("hover", True)
                self.hover_child = new_hover_child

            # Pass mouse-button-down event only to the affected child and handle press changes
            if event.type == pygame.MOUSEBUTTONDOWN:
                if new_hover_child is not None:
                    new_hover_child.process_event(converted_event)
                # handle press changes
                if event.button == 1 and new_hover_child is not None:
                    new_hover_child.set_ui_state("press", True)
                    self.press_child = new_hover_child
        
            # Pass mouse-button-up events only to the currently pressed child (if it exists) and handle press changes
            elif event.type == pygame.MOUSEBUTTONUP:
                if self.press_child is not None:
                    self.press_child.process_event(event)   # TODO: pass converted_event (if necessary)
                # handle press changes
                if event.button == 1 and self.press_child is not None:
                    new_hover_child.set_ui_state("press", False)
                    self.press_child = None

        # Pass all other event types to all children
        else:
            for child in self.children:
                child.process_event(event)
