from View import *
from Colors import *


# Functions take `image_size` and `region_size` and return `target_size`
SCALE_MODES = {
    # maintain original size TODO: crop to fit region
    "ORIGINAL": lambda img, reg:
        img, # (min(img[0], reg[0]), min(img[1], reg[1])),
    # stretch to fill region
    "STRETCH": lambda img, reg:
        reg,
    # stretch to fill smallest dimension of region (maintains aspect ratio)
    "CONTAIN": lambda img, reg:
        (round(img[0] * (r := reg[(d := reg[0] > reg[1])] / img[d])), round(img[1] * r)),
    # stretch to fill largest dimension of region (maintains aspect ratio)
    "COVER":   lambda img, reg:
        (round(img[0] * (r := reg[(d := reg[0] < reg[1])] / img[d])), round(img[1] * r)),
}


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

    def render_onto(self, surf, region=None):
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
