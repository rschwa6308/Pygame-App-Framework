import warnings
import pygame

from view import View


class GameView(View):
    """A View for implementing game elements;
    typical usage is to subclass GameView and override only setup, step, process_event, and render"""
    stepped = True

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        if "children" in kwargs and kwargs["children"]:
            warnings.warn(RuntimeWarning(
                "GameView children is not yet fully supported; " +
                "any events that you want to be processed by a child must be passed manually"
            ))

        self.setup()

    def get_window_size(self):
        return self.collision_rect.size

    def setup(self):
        """called once immediately after self.__init__()"""

    def step(self):
        """called once at the beginning of every frame by the hoster"""

    def process_event(self, event):
        pass

    def render(self) -> pygame.Surface:
        pass

    def render_onto(
        self,
        surf: pygame.Surface,
        region: pygame.Rect = None,
        render_children=True,
        render_border=True
    ):
        super().render_onto(surf, region, render_border=False)
        game_surf = self.render()
        dest = (
            region.left + (region.width - game_surf.get_width()) // 2,
            region.top + (region.height - game_surf.get_height()) // 2
        )
        surf.blit(game_surf, dest)

        if render_border:
            self.render_border_onto(surf, self.collision_rect)

        if render_children:
            self.render_children_onto(surf, self.collision_rect)
