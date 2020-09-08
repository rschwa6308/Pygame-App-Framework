import pygame


# Functions take `src_size` and `region_size` and return `target_size`
SCALE_MODES = {
    # maintain original size TODO: crop to fit region
    "ORIGINAL": lambda src, reg:
        src,    # (min(src[0], reg[0]), min(src[1], reg[1])),
    # stretch to fill region
    "STRETCH": lambda src, reg:
        reg,
    # stretch to fill smallest dimension of region (maintains aspect ratio)
    "CONTAIN": lambda src, reg:
        (round(src[0] * (r := min(reg[0] / src[0], reg[1] / src[1]))), round(src[1] * r)),
    # stretch to fill largest dimension of region (maintains aspect ratio)
    "COVER": lambda src, reg:
        (round(src[0] * (r := max(reg[0] / src[0], reg[1] / src[1]))), round(src[1] * r)),
}


MOUSE_POS_EVENT_TYPES = (
    pygame.MOUSEMOTION,
    pygame.MOUSEBUTTONDOWN,
    pygame.MOUSEBUTTONUP,
)