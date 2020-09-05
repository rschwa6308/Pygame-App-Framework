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
    
    def compute_dests(self):
        for row, flex_map_row in zip(self.layout, self.flex_map):
            for child, flex_map_child in zip(row, flex_map_row):
                child.dest = (
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
        background_color: Tuple[int, int, int] = default_background_color,
        **kwargs
    ):
        children = [child for row in layout for child in row]

        if not all(isinstance(child, Component) for child in children):
            raise ValueError(f"Invalid children argument: {children}; children must all be Components")

        super().__init__(x_flex, y_flex, background_color, children=children, **kwargs)
        
        self.layout = layout

        self.compute_flex_map()

        # calculate children's `dest`s based on flex_map
        self.compute_dests()


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
