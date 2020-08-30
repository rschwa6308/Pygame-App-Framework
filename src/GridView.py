from typing import Sequence

from View import *
from Colors import *

class GridView(View):
    default_background_color = WHITE

    def compute_flex_map(self):
        total_x_flex = max(sum(child.x_flex for child in row) for row in self.layout) if self.layout else 1
        total_y_flex = sum(max(child.y_flex for child in row) for row in self.layout) if self.layout else 1
        
        flex_map = []
        y = 0
        for row in self.layout:
            flex_map_row = []
            x = 0
            for child in row:
                flex_map_row.append((x, y, child.x_flex, child.y_flex))
                x += child.x_flex
            flex_map.append(flex_map_row)
            y += max(child.y_flex for child in row)

        self.flex_map, self.total_x_flex, self.total_y_flex = flex_map, total_x_flex, total_y_flex
    
    def compute_parent_dests(self):
        for row, flex_map_row in zip(self.layout, self.flex_map):
            for child, flex_map_child in zip(row, flex_map_row):
                child.parent_dest = (
                    flex_map_child[0] / self.total_x_flex,
                    flex_map_child[1] / self.total_y_flex,
                    flex_map_child[2] / self.total_x_flex,
                    flex_map_child[3] / self.total_y_flex
                )

    def __init__(
        self,
        layout: Sequence[Sequence[Component]] = [],
        x_flex: int = 1,
        y_flex: int = 1,
        background_color: Tuple[int, int, int] = default_background_color
    ):
        children = [child for row in layout for child in row]

        if not all(isinstance(child, Component) for child in children):
            raise ValueError(f"Invalid children argument: {children}; children must all be Components")

        super().__init__(x_flex, y_flex, background_color, children=children)
        
        self.layout = layout

        self.compute_flex_map()
        # self.child_regions_cache = []   # format (Component, Rect) TODO: remove in favor of implementation in `View`

        # calculate children's `parent_dest`s based on flex_map
        self.compute_parent_dests()

        

        
    # # renders self onto the given surface
    # # TODO: min_spacing around children
    # # TODO: use children positioning from parent class (do not call child.render_onto(...) here)
    # def render_onto(self, surf: pygame.Surface, region: pygame.Rect = None):
    #     region = super().render_onto(surf, region)

    #     x_flex_px = region.width / self.total_x_flex
    #     y_flex_px = region.height / self.total_y_flex
        
    #     self.child_regions_cache = []
    #     for row, flex_map_row in zip(self.layout, self.flex_map):
    #         for child, flex_map_child in zip(row, flex_map_row):
    #             child_region = pygame.Rect(
    #                 region.left + round(flex_map_child[0] * x_flex_px),
    #                 region.top + round(flex_map_child[1] * y_flex_px),
    #                 round(flex_map_child[2] * x_flex_px),
    #                 round(flex_map_child[3] * y_flex_px)
    #             )
    #             self.child_regions_cache.append((child, child_region))
    #             child.render_onto(surf, region=child_region)


if __name__ == "__main__":
    test_view = GridView(layout=[
        [View(5, 1, RED), View(1, 1, GREEN)],
        [View(6, 1, BLUE)]
    ])

    screen = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
    test_view.render_onto(screen)
    pygame.display.update()

    alive = True
    while alive:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                alive = False
            elif event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                test_view.render_onto(screen)
                pygame.display.update()
