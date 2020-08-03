from typing import Sequence

from View import *

class GridView(View):
    default_background_color = (255, 255, 255)

    @staticmethod
    def compute_flex_map(layout):
        total_x_flex = max(sum(child.x_flex for child in row) for row in layout) if layout else 1
        total_y_flex = sum(max(child.y_flex for child in row) for row in layout) if layout else 1
        
        flex_map = []
        y = 0
        for row in layout:
            flex_map_row = []
            x = 0
            for child in row:
                flex_map_row.append((x, y, child.x_flex, child.y_flex))
                x += child.x_flex
            flex_map.append(flex_map_row)
            y += max(child.y_flex for child in row)

        return (flex_map, total_x_flex, total_y_flex)
    
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

        super().__init__(x_flex, y_flex, background_color)
        
        self.layout = layout
        self.children = children

        self.flex_map, self.total_x_flex, self.total_y_flex = self.compute_flex_map(layout)
        
    # renders self onto the given surface
    # TODO: min_spacing around children
    def render_onto(self, surf: pygame.Surface, region: pygame.Rect = None):
        if region is None:
            region = surf.get_rect()
        elif not surf.get_rect().contains(region):
            raise ValueError(f"Invalid region: {region}; region must be contained within surf")

        surf.fill(self.background_color, rect=region)

        x_flex_px = region.width / self.total_x_flex
        y_flex_px = region.height / self.total_y_flex
        
        for row, flex_map_row in zip(self.layout, self.flex_map):
            for child, flex_map_child in zip(row, flex_map_row):
                child_region = pygame.Rect(
                    round(flex_map_child[0] * x_flex_px), round(flex_map_child[1] * y_flex_px),
                    round(flex_map_child[2] * x_flex_px), round(flex_map_child[3] * y_flex_px)
                )
                child.render_onto(surf, region=child_region)        


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
