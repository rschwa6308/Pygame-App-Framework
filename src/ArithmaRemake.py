from GridView import *
from Hoster import *
from App import *


NUM_LEVELS = 24
LEVELS_PER_ROW = 6


# --- Menu Screen --- #
menu_h1_style = {
    "font_kwargs": {
        "font_name": "Dotum",
        "font_size": 56,
        "underline": True
    }
}

menu_h2_style = {
    "font_kwargs": {
        "font_name": "Dotum",
        "font_size": 40,
    }
}

menu_button_style = {
    "font_kwargs": {
        "font_name": "verdana",
        "font_size": 26
    },
    "border_width": 2,
    "margins": (5,)*4
}

menu_screen = View(
    children=[GridView([
        [Text(2, 3, text="Arithma", **menu_h1_style)],
        [Button(2, 2, text="Levels", **menu_button_style, on_click=lambda self, event: self.run_hook("NAVIGATE_TO", "level_select"))],
        [Button(2, 2, text="Settings", **menu_button_style, on_click=lambda self, event: self.run_hook("NAVIGATE_TO", "settings"))],
        [
            Button(1, 2, text="Credits", **menu_button_style, on_click=lambda self, event: self.run_hook("NAVIGATE_TO", "credits")),
            Button(1, 2, text="Quit", **menu_button_style, on_click=lambda self, event: self.run_hook("QUIT_APP"))
        ]
    ], parent_dest=(0.3, 0.0, 0.4, 0.9))]
)


# --- Level Select Screen --- #
level_screens = [View() for _ in range(NUM_LEVELS)]

level_select_buttons = [
    Button(
        text=f"{x + 1}",
        on_click=lambda self, event: print(f"TODO: navigate to level_{self.nav_target}"),
        **menu_button_style
    )
    for x, level in enumerate(level_screens)
]

# navigation targets must be bound manually because lambdas are lazy
for x, button in enumerate(level_select_buttons):
    button.nav_target = f"level_{x + 1}"

# TODO: move "Levels" text to `level_select_screen.children`
num_rows = NUM_LEVELS // LEVELS_PER_ROW
level_select_layout = [
    [Text(LEVELS_PER_ROW, 0.5, text="Levels", **menu_h2_style)]
] + [
    level_select_buttons[row * LEVELS_PER_ROW:(row + 1) * LEVELS_PER_ROW]
    for row in range(NUM_LEVELS // LEVELS_PER_ROW)
]

level_select_screen = View(children=[
    GridView(
        level_select_layout,
        parent_dest=(0.1, 0.0, 0.75, 0.8)
    ),
    Button(
        text="Back",
        parent_dest=(0.4, 0.85, 0.2, 0.1),
        **menu_button_style
    )
])


# --- Settings Screen --- #
# TODO


# --- Credits Screen --- #
# TODO


hoster = Hoster(
    {
        "menu": menu_screen,
        "level_select": level_select_screen,
        # "settings": TODO,
        # "credits": TODO
    },
    "menu"
)


app = App(hoster)
app.run()