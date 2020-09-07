import pygame

from view import View
from util import SCALE_MODES


class Image(View):
    def __init__(
        self,
        image: pygame.Surface,
        scale_mode: str = "CONTAIN",
        **kwargs
    ):
        super().__init__(**kwargs)
        self.image = image
        self.scale_mode = scale_mode

        self.image_size = image.get_size()
        self.scaled_image = None

    def render_onto(
        self,
        surf: pygame.Surface,
        region: pygame.Rect = None,
        render_children=True,
        render_border=True
    ):
        # scale `self.image` to fill the given `region`
        target_size = SCALE_MODES[self.scale_mode](self.image_size, region.size)
        if self.scaled_image is None or\
           self.scaled_image.get_size() != target_size:
            self.scaled_image = pygame.transform.scale(self.image, target_size)
        
        # center `self.scaled_image` within `region`
        # TODO: provide a prop for customizing this (i.e. a value in [0, 1]^2)? maybe not
        target_pos = (
            round((region.size[0] - target_size[0]) / 2),
            round((region.size[1] - target_size[1]) / 2),
        )

        surf.blit(self.scaled_image, target_pos)
