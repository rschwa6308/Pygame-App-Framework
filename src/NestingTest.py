from GridView import *
from Hoster import *
from App import *

import random


DEPTH = 3


# TODO: fix hover issue here :)
curr = Button()


for _ in range(DEPTH):
    curr = View(
        children=[curr],
        dest=(0.1, 0.1, 0.8, 0.8),
        bg_color=random.choice(ACCENTS)
    )


home_screen = curr



hoster = Hoster(
    {
        "home": home_screen,
    },
    "home"
)


app = App(hoster)
app.run()