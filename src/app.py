from typing import Tuple, Sequence
import warnings
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

    default_initial_caption = "Pygame App Framework :)"

    default_initial_screen_size = (800, 600)
    default_min_screen_size = (300, 225)

    default_resizable_state = True
    default_fullscreen_state = False
    default_borderless_state = False

    default_quit_keys = []

    def __init__(
            self,
            hoster: Hoster,
            caption: str = default_initial_caption,
            target_fps: int = default_target_fps,
            screen_size: Tuple[int, int] = None,
            min_screen_size: Tuple[int, int] = None,
            resizable: bool = None,
            fullscreen: bool = None,
            borderless: bool = None,
            quit_keys: Sequence[int] = None
    ):
        if fullscreen:
            if resizable:
                warnings.warn(RuntimeWarning(
                    "App cannot be both resizable and fullscreen; " +
                    "resizable flag will be ignored"
                ))
            resizable = False
            if screen_size is None:
                screen_size = (0, 0)    # automatically fills desktop
            else:
                warnings.warn(RuntimeWarning(
                    "App was set to have both a defined screen size and be fullscreen; " +
                    "content will be automatically scaled (UNSTABLE)"
                ))

        if screen_size is None:
            screen_size = self.default_initial_screen_size

        if min_screen_size is None:
            min_screen_size = self.default_min_screen_size

        if resizable is None:
            resizable = self.default_resizable_state

        if fullscreen is None:
            fullscreen = self.default_fullscreen_state

        if borderless is None:
            borderless = self.default_borderless_state

        if quit_keys is None:
            quit_keys = self.default_quit_keys

        self.hoster = hoster

        self.initial_caption = caption
        self.initial_screen_size = screen_size
        self.min_screen_size = min_screen_size
        self.target_fps = target_fps

        self.resizable = resizable
        self.fullscreen = fullscreen
        self.borderless = borderless

        self.quit_keys = quit_keys

        # bind all hooks
        for hook in [
            ("TRIGGER_RERENDER", self.trigger_rerender),
            ("QUIT_APP", self.quit),
            ("SET_CAPTION", pygame.display.set_caption),
            ("SET_ICON", pygame.display.set_icon),
            ("SET_FULLSCREEN", self.set_fullscreen),
            ("TOGGLE_FULLSCREEN", self.toggle_fullscreen)
        ]:
            self.hoster.bind_hook(*hook, bind_to_children=True)

        self.alive = False
        self.rerender_on_next_frame = True  # initial render
        self.screen = None

    def get_display_flags(self):
        display_flags = 0
        for prop, flag in [
            (self.resizable, pygame.RESIZABLE),
            (self.fullscreen, pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF),
            (self.borderless, pygame.NOFRAME)
        ]:
            if prop:
                display_flags |= flag

        return display_flags

    # TODO: test this behavior more fully on a *stable* pygame 2.0 branch
    def set_fullscreen(self, val):
        self.fullscreen = val
        new_screen_size = (0, 0) if val else self.initial_screen_size
        # post a video-resize event to trigger a display-reload
        pygame.event.post(pygame.event.Event(
            pygame.VIDEORESIZE,
            w=new_screen_size[0],
            h=new_screen_size[1]
        ))

    def toggle_fullscreen(self):
        self.set_fullscreen(not self.fullscreen)

    def trigger_rerender(self):
        self.rerender_on_next_frame = True

    def update_screen(self):
        # print("RERENDER")
        self.hoster.render_onto(self.screen)
        pygame.display.update()

    def quit(self):
        self.alive = False

    def run(self, screen_size=None, target_fps=None):
        if screen_size is None:
            screen_size = self.initial_screen_size

        if target_fps is None:
            target_fps = self.target_fps

        self.alive = True

        display_flags = self.get_display_flags()
        self.screen = pygame.display.set_mode(screen_size, display_flags)

        pygame.display.set_caption(self.initial_caption)

        # Mount the hoster and render to the screen
        self.hoster.on_mount()

        clock = pygame.time.Clock()

        while self.alive:
            clock.tick(target_fps)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.alive = False
                elif event.type == pygame.VIDEORESIZE:
                    new_screen_size = (
                        max(event.w, self.min_screen_size[0]),
                        max(event.h, self.min_screen_size[1]),
                    ) if (event.w, event.h) != (0, 0) else (0, 0)
                    print(new_screen_size)
                    pygame.display.set_mode(new_screen_size, self.get_display_flags())
                    self.update_screen()
                elif event.type == pygame.KEYDOWN and event.key in self.quit_keys:
                    self.quit()
                else:
                    # pass all other events down to the hoster
                    if event.type in MOUSE_POS_EVENT_TYPES:
                        event.abs_pos = event.pos
                    self.hoster.process_event(event)

            if self.rerender_on_next_frame:
                self.update_screen()
                self.rerender_on_next_frame = False

        pygame.display.quit()


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
