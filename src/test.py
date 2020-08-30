from App import *
from Colors import *

from random import choice




NUM_LEVELS = 15
LEVELS_PER_ROW = 5


level_screens = [
    Text(1, 1, choice(ACCENTS), f"Level #{x + 1}", children=[
        Button(
            text="BACK",
            border_width=3,
            border_radius=10,
            font_kwargs={"bold": True, "italic": True},
            parent_dest=(0.1, 0.1, 0.1, 0.1),   # position within parent
            on_click=lambda self, event: self.run_hook("NAVIGATE_TO", "level_select"),
        )
    ])
    for x in range(NUM_LEVELS)
]


level_select_buttons = [
    Button(
        background_color=level.background_color,
        text=f"Level #{x + 1}",
        text_color=WHITE,
        font_kwargs={"bold": True},
        border_width=10,
        border_radius=20,
        on_click=lambda self, event: self.run_hook("NAVIGATE_TO", self.nav_target),
        margins=(5,)*4
    )
    for x, level in enumerate(level_screens)
]


# navigation targets must be bound manually because lambdas are lazy
for x, button in enumerate(level_select_buttons):
    button.nav_target = f"level_{x + 1}"


num_rows = NUM_LEVELS // LEVELS_PER_ROW
level_select_screen = GridView([
    [Text(5, 0.5, text="Level Select")]
] + [
    level_select_buttons[row * LEVELS_PER_ROW:(row + 1) * LEVELS_PER_ROW]
    for row in range(NUM_LEVELS // LEVELS_PER_ROW)
])



# class Image(View):
#     def __init__(self, image: pygame.Surface, **kwargs):
#         super().__init___(**kwargs)
#         self.image = image

#     def render_onto(self, surf, region=None):
#         # TODO: scale `self.image` to fill `region` here
#         self.image.blit(surf, (0, 0))
        






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