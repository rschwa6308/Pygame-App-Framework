from view import View
from gridview import GridView
from scrollview import ScrollView
from button import Button
from text import Text
from hoster import Hoster
from app import App


NUM_LEVELS = 48
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
        [Button(
            2, 2, text="Levels",
            on_click=lambda self, event: self.run_hook("NAVIGATE_TO", "level_select"),
            **menu_button_style
        )],
        [Button(
            2, 2, text="Settings",
            on_click=lambda self, event: self.run_hook("NAVIGATE_TO", "settings"),
            **menu_button_style
        )],
        [
            Button(
                1, 2, text="Credits",
                on_click=lambda self, event: self.run_hook("NAVIGATE_TO", "credits"),
                **menu_button_style
            ),
            Button(
                1, 2, text="Quit",
                on_click=lambda self, event: self.run_hook("QUIT_APP"),
                **menu_button_style
            )
        ]
    ], dest=(0.3, 0.0, 0.4, 0.9))]
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
    level_select_buttons[row * LEVELS_PER_ROW:(row + 1) * LEVELS_PER_ROW]
    for row in range(NUM_LEVELS // LEVELS_PER_ROW)
]

level_select_screen = View(children=[
    Text(
        LEVELS_PER_ROW, 0.5,
        text="Levels",
        dest=(0.25, 0.0, 0.5, 0.1),
        **menu_h2_style
    ),
    # TODO: some sort of border or bg-color change to differentiate this region
    ScrollView(
        children=[GridView(level_select_layout, margins=(12, 0)*2)],
        canvas_size_factors = (1.0, 2.0),
        dest=(0.1, 0.1, 0.8, 0.7),
    ),
    Button(
        text="Back",
        dest=(0.4, 0.85, 0.2, 0.1),
        on_click=lambda self, event: self.run_hook("NAVIGATE_BACK"),
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