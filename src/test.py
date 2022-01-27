import os
from random import choice
import pygame

# used in `TestGame`
from collections import deque
from random import uniform
from itertools import combinations

from view import View
from gridview import GridView
from scrollview import ScrollView
from button import Button
from text import Text
from image import Image
from gameview import GameView
from hoster import Hoster
from app import App
from colors import *


# --- Define the game --- #

class TestGame(GameView):
    num_balls = 5

    gravity = 0.0005
    elasticity = 0.9

    class Ball:
        default_mass = 1.0
        default_radius = 0.075
        default_color = BLACK

        def __init__(self, pos, vel, mass=default_mass, radius=default_radius, color=default_color):
            self.pos = list(pos)
            self.vel = list(vel)

            self.mass = mass
            self.radius = radius
            self.color = color

            self.pos_history = deque(maxlen=10)      # store the position of the ball over the last 10 frames

        def save_pos(self):
            self.pos_history.append(tuple(self.pos))

        def get_pos_px(self, window_size):
            return (
                self.pos[0] * window_size[0],
                (1.0 - self.pos[1]) * window_size[1]    # y coordinate flipped
            )

        def get_radius_px(self, window_size):
            return self.radius * window_size[0]         # window guaranteed to be square by `aspect_ratio=1`

        def render_onto(self, window):
            window_size = window.get_size()
            pos_px = self.get_pos_px(window_size)
            radius_ps = self.get_radius_px(window_size)
            pygame.draw.circle(window, self.color, pos_px, radius_ps)

    def setup(self):
        self.balls = [
            self.Ball(
                (uniform(0, 1), uniform(0, 1)),
                (uniform(-0.01, 0.01), uniform(-0.01, 0.01)),
                color=choice(ACCENTS)
            )
            for _ in range(self.num_balls)
        ]

        self.ball_held = None

    def step(self):
        for ball in self.balls:
            ball.vel[1] -= self.gravity

            if ball is self.ball_held:
                ball.vel = [0, 0]

            ball.pos[0] += ball.vel[0]
            ball.pos[1] += ball.vel[1]

            # ball-wall collision
            # TODO: more robust potential/kinetic energy transformation
            x, y = ball.pos
            if x < ball.radius:
                ball.vel[0] *= -self.elasticity
                ball.pos[0] = ball.radius
            elif x > 1.0 - ball.radius:
                ball.vel[0] *= -self.elasticity
                ball.pos[0] = 1 - ball.radius

            if y < ball.radius:
                ball.vel[1] *= -self.elasticity
                ball.pos[1] = ball.radius
            elif y > 1.0 - ball.radius:
                ball.vel[1] *= -self.elasticity
                ball.pos[1] = 1 - ball.radius

            # ball-ball collision
            for a, b in combinations(self.balls, 2):
                dist_sqrd = (a.pos[0] - b.pos[0]) ** 2 + (a.pos[1] - b.pos[1]) ** 2
                if dist_sqrd <= (a.radius + b.radius) ** 2:
                    pass    # TODO: robust bounce physics here

            ball.save_pos()

        self.run_hook("TRIGGER_RERENDER")

    def convert_cursor_pos(self, cursor_pos_px):
        w, h = self.get_window_size()
        return [
            cursor_pos_px[0] / w,
            1.0 - cursor_pos_px[1] / h              # y coordinate flipped
        ]

    def process_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                window_size = self.get_window_size()
                for ball in self.balls:
                    x, y = ball.get_pos_px(window_size)
                    dist_sqrd_to_ball = (event.pos[0] - x) ** 2 +\
                                        (event.pos[1] - y) ** 2
                    if dist_sqrd_to_ball <= ball.get_radius_px(window_size) ** 2:
                        self.ball_held = ball
                        ball.pos = self.convert_cursor_pos(event.pos)
                        break

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                if self.ball_held:
                    # drop ball with some included velocity
                    pos_history = self.ball_held.pos_history
                    recent_displacement = (
                        pos_history[-1][0] - pos_history[0][0],
                        pos_history[-1][1] - pos_history[0][1]
                    )
                    self.ball_held.vel = [
                        recent_displacement[0] / len(pos_history),
                        recent_displacement[1] / len(pos_history)
                    ]
                    self.ball_held = None

        elif event.type == pygame.MOUSEMOTION:
            if self.ball_held:
                self.ball_held.pos = self.convert_cursor_pos(event.pos)
                self.ball_held.save_pos()

    def render(self):
        window = pygame.Surface(self.get_window_size())
        window.fill(WHITE)
        for ball in self.balls:
            ball.render_onto(window)

        return window


# --- Define the menu layout --- #

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
            dest=(0.6, 0.1, 0.35, 0.4),
            canvas_size_factors=(1.0, 3.0),
            border_width=3,
            aspect_ratio=1,
            children=[
                View(bg_color=GREEN, dest=(0.1, 0.0, 0.2, 1.0), margins=(0, 10, 0, 10)),
                Button(bg_color=RED, dest=(0.4, 0.1, 0.2, 0.2), text="!", on_click=lambda s, e: print("HI")),
                View(bg_color=BLUE, dest=(0.4, 0.4, 0.2, 0.2)),
                View(bg_color=MAGENTA, dest=(0.8, 0.6, 0.2, 0.2)),
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
        ),
        TestGame(
            dest=(0.6, 0.6, 0.3, 0.3),
            aspect_ratio=1,
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
        aspect_ratio=1,
        # abs_size=(200, 100),
        # scale_mode="CONTAIN"
    )
    for x, level in enumerate(level_screens)
]


# navigation targets must be bound manually because lambdas are lazy
for x, button in enumerate(level_select_buttons):
    button.nav_target = f"level_{x + 1}"


num_rows = NUM_LEVELS // LEVELS_PER_ROW
level_select_screen = GridView([
    [View(5, 1, children=[
        Button(
            text="Quit",
            dest=(0.05, 0.05, 0.1, 0.4),
            aspect_ratio=2,
            border_width=5,
            border_radius=10,
            on_click=lambda self, event: self.run_hook("QUIT_APP")
        ),
        Text(
            text="Level Select",
            font_kwargs={
                "font_size": 40,
                "bold": True,
            },
            dest=(0.3, 0.1, 0.4, 0.8)
        )
    ])]
] + [
    level_select_buttons[row * LEVELS_PER_ROW:(row + 1) * LEVELS_PER_ROW]   
    for row in range(NUM_LEVELS // LEVELS_PER_ROW)
], margins=(10,)*4)


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


app = App(hoster, fullscreen=True, borderless=False, quit_keys=[pygame.K_ESCAPE])
app.run()


# TODO:
#   [✓] View fixed aspect ratio
#   [✓] View exact width/height
#   [ ] View min/max width/height
#   [ ] View padding
#   [ ] ListView? (maybe not necessary since list comprehension works so well)
#   [ ] better support of TRANSPARENT backgrounds
#   [ ] optionally different ScrollView behavior where children size matches parent's siblings (aunts/uncles ?)
#       (sort of breaks the whole paradigm so maybe not)
#   [ ] click+drag scroll bars (might be hard since currently no support for click+drag anywhere)
#   [✓] better support for nested ScrollViews
#   [✓] fullscreen support
