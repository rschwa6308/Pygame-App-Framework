import pygame.freetype


DEFAULT_FONT_NAME = "Arial"
DEFAULT_FONT_SIZE = 24


pygame.freetype.init()

font_cache = {}
def get_font(font_name=DEFAULT_FONT_NAME, font_size=DEFAULT_FONT_SIZE, bold=False, italic=False):
    """Get a `Font` object (cached)"""
    key = f"{font_name}-{font_size}"
    if bold: key += "-bold"
    if italic: key += "-italic"

    if key in font_cache:
        font = font_cache[key]
    else:
        font = pygame.freetype.SysFont(font_name, font_size, bold, italic)
        font_cache[key] = font

    return font


def render_text_to(
    surf, dest, text, region=None,
    font_name=DEFAULT_FONT_NAME, font_size=DEFAULT_FONT_SIZE, bold=False, italic=False, **kwargs
):
    """Render the given text onto the given surface.
    Argument `dest` can be either coordinates (local to region) or "CENTER"."""
    font = get_font(font_name, font_size, bold, italic)

    if region is None:
        region = surf.get_rect()

    if dest == "CENTER":
        text_rect = font.get_rect(text)
        real_dest = (
            region.left + round((region.width - text_rect.width) / 2),
            region.top + round((region.height - text_rect.height) / 2),
        )
    else:
        real_dest = (
            region.left + dest[0],
            region.top + dest[1]
        )

    font.render_to(surf, real_dest, text, **kwargs)
