import os
from random import choice
import pygame

from view import View
from gridview import GridView
from scrollview import ScrollView
from button import Button
from text import Text
from image import Image
from hoster import Hoster
from app import App
from colors import *


NUM_LEVELS = 15
LEVELS_PER_ROW = 5


# Load test images
test_assets_dir = os.path.join(os.path.dirname(__file__), "test_assets")
test_image_source = pygame.image.load(os.path.join(test_assets_dir, "smile.png"))


level_screens = [
    Text(1, 1, choice(ACCENTS), f"Level #{x + 1}", children=[
        Button(
            text="BACK",
            border_width=3,
            border_radius=10,
            font_kwargs={"bold": True, "italic": True},
            dest=(0.1, 0.1, 0.1, 0.1),   # position within parent
            on_click=lambda self, event: self.run_hook("NAVIGATE_TO", "level_select"),
        ),
        ScrollView(
            dest=(0.6, 0.3, 0.35, 0.5),
            canvas_size_factors=(1.0, 3.0),
            border_width=3,
            aspect_ratio=1,
            children=[
                View(bg_color=GREEN, dest=(0.1, 0.0, 0.2, 1.0), margins=(0, 10, 0, 10)),
                Button(bg_color=RED, dest=(0.4, 0.1, 0.2, 0.2), text="!", on_click=lambda s, e: print("HI")),
                View(bg_color=BLUE, dest=(0.4, 0.4, 0.2, 0.2)),
                View(bg_color=MAGENTA, dest=(0.8, 0.6, 0.2, 0.2)),
                # TODO: currently testing deeply nested scrollview event behavior
                ScrollView(
                    border_width=1,
                    dest=(0.4, 0.7, 0.3, 0.2),
                    canvas_size_factors=(2.0, 2.0),
                    children=[
                        Image(image=test_image_source)
                    ]
                )
            ]
        ),
        ScrollView(
            dest=(0.1, 0.7, 0.4, 0.2),
            canvas_size_factors=(2.0, 1.0),
            border_width=3,
            children=[
                Text(
                    text=" Hello, World! ABCDEFGHIJKLMNOPQRSTUVWXYZ 0123456789 ",
                    font_kwargs={"underline": True}
                )
            ]
        )
    ])
    for x in range(NUM_LEVELS)
]


level_select_buttons = [
    Button(
        bg_color=level.bg_color,
        text=f"Level #{x + 1}",
        text_color=WHITE,
        font_kwargs={"bold": True},
        border_width=10,
        border_radius=20,
        on_click=lambda self, event: self.run_hook("NAVIGATE_TO", self.nav_target),
        margins=(5,)*4,
        # aspect_ratio=1,
        abs_size=(200, 100),
        # scale_mode="CONTAIN"
    )
    for x, level in enumerate(level_screens)
]


# navigation targets must be bound manually because lambdas are lazy
for x, button in enumerate(level_select_buttons):
    button.nav_target = f"level_{x + 1}"


num_rows = NUM_LEVELS // LEVELS_PER_ROW
level_select_screen = GridView([
    [Text(5, 1, text="Level Select")]
] + [
    level_select_buttons[row * LEVELS_PER_ROW:(row + 1) * LEVELS_PER_ROW]   
    for row in range(NUM_LEVELS // LEVELS_PER_ROW)
])


hoster = Hoster(
    {
        "level_select": level_select_screen,
        **{
            f"level_{x+1}": level
            for x, level in enumerate(level_screens)
        }
    },
    "level_select"
)


app = App(hoster)
app.run()


# TODO:
#   - view fixed aspect ratio
#   - view min/max width/height
#   - view padding
#   - ListView? (maybe not necessary since list comprehension works so well)
#   - better support of TRANSPARENT backgrounds
#   - optionally different ScrollView behavior where children size matches parent's siblings (aunts/uncles ?)
#     (sort of breaks the whole paradigm so maybe not)
#   - click+drag scroll bars (might be hard since currently no support for click+drag anywhere)
