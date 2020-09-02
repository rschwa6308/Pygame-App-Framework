from GridView import *
from Hoster import *
from App import *



# --- Menu Screen --- #
menu_title_style = {
    "font_kwargs": {
        "font_name": "Dotum",
        "font_size": 56,
        "underline": True
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
        [Text(2, 3, text="Arithma", **menu_title_style)],
        [Button(2, 2, text="Levels", **menu_button_style, on_click=lambda self, event: self.run_hook("NAVIGATE_TO", "level_select"))],
        [Button(2, 2, text="Settings", **menu_button_style, on_click=lambda self, event: self.run_hook("NAVIGATE_TO", "settings"))],
        [
            Button(1, 2, text="Credits", **menu_button_style, on_click=lambda self, event: self.run_hook("NAVIGATE_TO", "credits")),
            Button(1, 2, text="Quit", **menu_button_style, on_click=lambda self, event: self.run_hook("QUIT_APP"))
        ]
    ], parent_dest=(0.3, 0.0, 0.4, 0.9))]
)


# --- Level Select Screen --- #
# TODO


# --- Settings Screen --- #
# TODO


# --- Credits Screen --- #
# TODO


hoster = Hoster(
    {
        "menu": menu_screen,
        # "level_select": TODO,
        # "settings": TODO,
        # "credits": TODO
    },
    "menu"
)


app = App(hoster)
app.run()