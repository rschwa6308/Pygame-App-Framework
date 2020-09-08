import os
import pygame

from view import View
from gridview import GridView
from button import Button
from text import Text
from image import Image
from hoster import Hoster
from colors import *
from util import MOUSE_POS_EVENT_TYPES


class App:
    default_target_fps = 60

    def __init__(self, hoster: Hoster):
        self.hoster = hoster
        self.hoster.bind_hook("TRIGGER_RERENDER", self.trigger_rerender, bind_to_children=True)
        self.hoster.bind_hook("QUIT_APP", self.quit, bind_to_children=True)
        self.alive = False
        self.rerender_on_next_frame = True      # initial render

    def trigger_rerender(self):
        self.rerender_on_next_frame = True

    def update_screen(self):
        # print("RERENDER")
        self.hoster.render_onto(self.screen)
        pygame.display.update()

    def quit(self):
        self.alive = False

    def run(self, screen_dims=(800, 600), target_fps=default_target_fps):
        self.alive = True
        self.screen = pygame.display.set_mode(screen_dims, pygame.RESIZABLE)

        # Mount the hoster and render to the screen
        self.hoster.on_mount()

        clock = pygame.time.Clock()

        while self.alive:
            clock.tick(target_fps)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.alive = False
                elif event.type == pygame.VIDEORESIZE:
                    pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                    self.update_screen()
                else:
                    # pass all other events down to the hoster
                    if event.type in MOUSE_POS_EVENT_TYPES:
                        event.abs_pos = event.pos
                    self.hoster.process_event(event)

            if self.rerender_on_next_frame:
                self.update_screen()
                self.rerender_on_next_frame = False


if __name__ == "__main__":
    test_button = Button(
        1, 1, RED,
        text="Navigate to Other!",
        on_click=lambda self, event: self.run_hook("NAVIGATE_TO", "other")
    )

    test_component_1 = GridView([
        [View(5, 1, RED), View(2, 1, GREEN)],
        [View(6, 1, BLUE), test_button]
    ])

    test_component_2a = GridView([
        [View(1, 1, GREEN), View(1, 1, RED)],
        [Button(1, 1, RED, text="HIT", on_click=lambda self, event: print("HIT")), View(1, 1, GREEN)]
    ], x_flex=1, y_flex=1)

    test_assets_dir = os.path.join(os.path.dirname(__file__), "test_assets")
    test_image_source = pygame.image.load(os.path.join(test_assets_dir, "smile.png"))

    test_component_2 = GridView([
        [Image(image=test_image_source), test_component_2a],
        [Text(2, 1, BLUE, "Hello, World!")]
    ])

    test_hoster = Hoster(
        {
            "home": test_component_1,
            "other": test_component_2
        },
        "home"
    )

    test_app = App(test_hoster)
    test_app.run()
