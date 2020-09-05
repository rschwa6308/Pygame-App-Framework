from typing import Any, Tuple, Dict
import pygame

from view import View
from fonts import render_text_to
from colors import *


class Text(View):
    default_bg_color = WHITE
    default_text_color = BLACK

    def __init__(
        self,
        x_flex: int = 1,
        y_flex: int = 1,
        bg_color: Tuple[int, int, int] = default_bg_color,
        text: str = "",
        text_color: Tuple[int, int, int] = default_text_color,
        font_kwargs=None,
        **kwargs
        # TODO: add font options here
    ):
        super().__init__(x_flex, y_flex, bg_color, **kwargs)

        if font_kwargs is None:
            font_kwargs = {}

        self.text = text
        self.text_color = text_color
        self.font_kwargs = font_kwargs

    def render_onto(
        self,
        surf: pygame.Surface,
        region: pygame.Rect = None,
        render_children=True,
        render_border=True
    ):
        region = super().render_onto(surf, region)
        render_text_to(surf, "CENTER", self.text, region=region, fgcolor=self.text_color, **self.font_kwargs)
        return region
