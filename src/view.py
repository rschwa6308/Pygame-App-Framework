from typing import Tuple
import warnings
import pygame

from component import Component
from colors import *
from util import SCALE_MODES


class View(Component):
    default_bg_color = WHITE
    default_border_color = BLACK

    default_scale_mode = "STRETCH"

    def __init__(
        self,
        x_flex: int = 1,
        y_flex: int = 1,
        bg_color: pygame.Color = default_bg_color,
        border_color: pygame.Color = default_border_color,
        border_width: int = 0,
        border_radius: int = 1,
        margins: Tuple[int, int, int, int] = (0, 0, 0, 0),  # (N, E, S, W)
        # the region within this View's parent to resize to
        dest: Tuple[float, float, float, float] = (0, 0, 1, 1),            # (L, T, W, H) (floating point in [0, 1]),
        scale_mode: str = None,
        aspect_ratio: float = None,
        abs_size: Tuple[int, int] = None,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.x_flex = x_flex
        self.y_flex = y_flex
        self.bg_color = bg_color
        self.border_color = border_color
        self.border_width = border_width
        self.border_radius = border_radius
        self.margins = margins
        self.dest = dest

        # check for sizing argument conflicts
        if aspect_ratio is not None and abs_size is not None:
            warnings.warn(RuntimeWarning(
                "values for both aspect_ratio and abs_size were given; " +
                "aspect_ratio will be ignored"
            ))
            aspect_ratio = None

        # dynamically set scale mode based on given inputs
        if scale_mode is None:
            if aspect_ratio is not None:
                scale_mode = "CONTAIN"
            elif abs_size is not None:
                scale_mode = "ORIGINAL"
            else:
                scale_mode = self.default_scale_mode
        else:
            if scale_mode == "CONTAIN" and aspect_ratio is None:
                warnings.warn(RuntimeWarning(
                    "scale_mode was set to \"CONTAIN\" but no aspect ratio was given; " +
                    "\"STRETCH\" will be used instead"
                ))
                scale_mode = self.default_scale_mode
            elif scale_mode == "ORIGINAL" and abs_size is None:
                warnings.warn(RuntimeWarning(
                    "scale_mode was set to \"ORIGINAL\" but no absolute size was given; " +
                    "\"STRETCH\" will be used instead"
                ))
                scale_mode = self.default_scale_mode

        self.scale_mode = scale_mode
        self.aspect_ratio = aspect_ratio
        self.abs_size = abs_size

        self.child_regions_cache = []   # format (Component, Rect)
        self.hover_child = None
        self.press_child = None

        # TODO: maybe repalce this with a Rect representing collision area
        self.collision_offset = [0, 0]
    
    def render_children_onto(self, surf, region=None):
        if region is None:
            region = surf.get_rect()
        
        # render all children
        self.child_regions_cache = []                                   # clear cache
        for child in self.children:
            child_region = pygame.Rect(
                region.width * child.dest[0],
                region.height * child.dest[1],
                region.width * child.dest[2],
                region.height * child.dest[3]
            )
            child_region_abs = pygame.Rect(
                region.left + region.width * child.dest[0],
                region.top + region.height * child.dest[1],
                region.width * child.dest[2],
                region.height * child.dest[3]
            )

            self.child_regions_cache.append((child, child_region))      # save in cache
            child.render_onto(surf, child_region_abs)
    
    def render_border_onto(self, surf, region=None):
        if region is None:
            region = surf.get_rect()
        
        if self.border_width > 0:
            pygame.draw.rect(                                   # draw border
                surf, self.border_color, region,
                width=self.border_width, border_radius=self.border_radius
            )
    
    def render_onto(
        self,
        surf: pygame.Surface,
        region: pygame.Rect = None,
        render_children=True,
        render_border=True
    ):
        self.collision_offset = [0, 0]

        if region is None:
            region = surf.get_rect()
        
        # adjust region to account for margins
        draw_region = pygame.Rect(
            region.left + self.margins[0],
            region.top + self.margins[1],
            region.width - (self.margins[0] + self.margins[2]),
            region.height - (self.margins[1] + self.margins[3]),
        )

        # adjust region to account for scale_mode (i.e. enforce aspect ratio)
        if self.abs_size:
            src_size = self.abs_size
        else:
            src_size = (self.aspect_ratio, 1)
        target_size = SCALE_MODES[self.scale_mode](src_size, draw_region.size)
        draw_region = pygame.Rect(
            draw_region.left + round((draw_region.size[0] - target_size[0]) / 2),
            draw_region.top + round((draw_region.size[1] - target_size[1]) / 2),
            *target_size
        )

        self.collision_offset[0] += region.left - draw_region.left
        self.collision_offset[1] += region.top - draw_region.top

        if self.border_width > 0:
            pygame.draw.rect(                           # fill background
                surf, self.bg_color, draw_region,
                width=0, border_radius=self.border_radius
            )
        else:
            surf.fill(self.bg_color, draw_region)            # fill background
        
        # render all children (on top)
        if render_children:
            self.render_children_onto(surf, draw_region)
        
        # render border (on top)
        if render_border:
            self.render_border_onto(surf, draw_region)

        # return the affected region
        return draw_region
    
    def process_event(self, event):
        # Handle all mouse events (excluding scroll wheel - see https://github.com/pygame/pygame/issues/682)
        if event.type in (
            pygame.MOUSEMOTION,
            pygame.MOUSEBUTTONDOWN,
            pygame.MOUSEBUTTONUP,
        ):
            new_hover_child = None

            # find new hover child
            for child, region in self.child_regions_cache:
                adjusted_pos = (
                    event.pos[0] + self.collision_offset[0],
                    event.pos[1] + self.collision_offset[1]
                )
                if region.collidepoint(adjusted_pos):
                    new_hover_child = child
                    # convert `pos` to local coords and include original as `parent_pos` and process event
                    local_pos = (
                        adjusted_pos[0] - region.left,
                        adjusted_pos[1] - region.top
                    )
                    converted_event = event
                    converted_event.pos, converted_event.parent_pos = local_pos, adjusted_pos
                    break
            
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
                if event.button == 1:
                    self.set_ui_state("press", False)

        elif event.type == pygame.MOUSEWHEEL:
            # Pass mouse-wheel event only to the currently hovered child (if it exists)
            if self.hover_child is not None:
                self.hover_child.process_event(event)

        # Pass all other event types to all children
        else:
            for child in self.children:
                child.process_event(event)
