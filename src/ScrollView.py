from View import *


class ScrollView(View):
    default_background_color = WHITE

    # portion of canvas to scroll with 1 scroll event
    scroll_speed_x = 0.10
    scroll_speed_y = 0.05

    scroll_bar_color = BLACK
    scroll_bar_opacity = 0.5
    scroll_bar_width = 8
    scroll_bar_padding = 5

    def __init__(
        self,
        x_flex: int = 1,
        y_flex: int = 1,
        background_color: Tuple[int, int, int] = default_background_color,
        canvas_size_factors: Tuple[float, float] = (1.0, 1.0),
        scroll_bar_x: bool = None,
        scroll_bar_y: bool = None,
        **kwargs
    ):
        super().__init__(x_flex, y_flex, background_color, **kwargs)

        self.canvas_size_factors = canvas_size_factors

        if scroll_bar_x is None:
            self.scroll_bar_x = canvas_size_factors[0] > 1.0
        else:
            self.scroll_bar_x = scroll_bar_x

        if scroll_bar_y is None:
            self.scroll_bar_y = canvas_size_factors[1] > 1.0
        else:
            self.scroll_bar_y = scroll_bar_y

        # internal coordinates (in [0, 1]^4) representing the area that is currently visible
        # (L, T, W, H)
        self.scroll_area = [
            0.0, 0.0,
            1 / canvas_size_factors[0],
            1 / canvas_size_factors[1]
        ]
        self.canvas_cache = None

        self.collision_offset = (0, 0)
    
    def process_event(self, event):
        if event.type == pygame.MOUSEWHEEL:
            # prevent double-scrolling of nested ScrollViews (only scroll the child)
            # TODO: default to scrolling the parent (i.e. self) when the child is maxed/mined out (?)
            if not isinstance(self.hover_child, ScrollView):
                old_scroll_area = list(self.scroll_area)    # copy
                d = (-event.x, event.y)
                for i in (0, 1):
                    self.scroll_area[i] -= d[i] * (self.scroll_speed_x, self.scroll_speed_y)[i]
                    if d[i] > 0:
                        self.scroll_area[i] = max(self.scroll_area[i], 0.0)
                    else:
                        self.scroll_area[i] = min(self.scroll_area[i], 1 - self.scroll_area[2+i])
                
                if self.scroll_area != old_scroll_area:
                    self.run_hook("TRIGGER_RERENDER")

        super().process_event(event)
    
    def render_onto(self, surf: pygame.Surface, region: pygame.Rect = None):
        region = super().render_onto(surf, region, render_children=False, render_border=False)
        
        # create canvas surface (cached)
        if self.canvas_cache is None or region.size != surf.get_size():
            canvas = pygame.Surface((
                region.width * self.canvas_size_factors[0],
                region.height * self.canvas_size_factors[1],
            ), pygame.SRCALPHA)
            canvas.fill((0, 0, 0, 0))
            self.canvas_cache = canvas
        else:
            canvas = self.canvas_cache

        super().render_children_onto(canvas)

        canvas_rect = canvas.get_rect()
        blit_area = pygame.Rect(
            canvas_rect.width * self.scroll_area[0],
            canvas_rect.height * self.scroll_area[1],
            canvas_rect.width * self.scroll_area[2],
            canvas_rect.height * self.scroll_area[3],
        )

        # update collision offset value
        self.collision_offset = blit_area.topleft

        surf.blit(canvas, region, area=blit_area)

        # draw scroll bars
        scroll_bar_rects = []
        if self.scroll_bar_x:
            scroll_bar_rects.append(pygame.Rect(
                self.scroll_bar_padding + region.width * self.scroll_area[0],
                region.height - (self.scroll_bar_width + self.scroll_bar_padding),
                region.width * self.scroll_area[2] - self.scroll_bar_padding * 2,
                self.scroll_bar_width
            ))

        if self.scroll_bar_y:
            scroll_bar_rects.append(pygame.Rect(
                region.width - (self.scroll_bar_width + self.scroll_bar_padding),
                self.scroll_bar_padding + region.height * self.scroll_area[1],
                self.scroll_bar_width,
                region.height * self.scroll_area[3] - self.scroll_bar_padding * 2
            ))
        
        for rect in scroll_bar_rects:
            temp_surf = pygame.Surface(region.size)
            temp_surf.fill(WHITE)
            temp_surf.set_colorkey(WHITE)
            temp_surf.set_alpha(255 * self.scroll_bar_opacity)
            pygame.draw.rect(
                temp_surf, self.scroll_bar_color, rect,
                border_radius=self.scroll_bar_width
            )
            surf.blit(temp_surf, region)

        super().render_border_onto(surf, region)
