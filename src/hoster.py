from typing import Dict
import pygame

from component import Component
from colors import *


class Hoster(Component):
    default_background_color = WHITE

    def __init__(
        self,
        component_id_map: Dict[str, Component],
        start_id: str,
        background_color=default_background_color
    ):
        super().__init__()

        self.component_id_map = component_id_map
        self.start_id = start_id
        self.background_color = background_color

        self.children = self.component_id_map.values()

        self.nav_stack = []
        self.initialized = False

        for component in component_id_map.values():
            component.bind_hook("NAVIGATE_TO", self.navigate_to, bind_to_children=True)
            component.bind_hook("NAVIGATE_BACK", self.navigate_back, bind_to_children=True)

        # get a handle to all descendants per component id
        self.descendants_id_map = {
            id: component.get_descendants()
            for id, component in self.component_id_map.items()
        }

        # get a handle to all stepped descendants per component id
        self.stepped_descendants_id_map = {
            id: [d for d in descendants if d.stepped]
            for id, descendants in self.descendants_id_map.items()
        }

    def current_component_id(self):
        return self.nav_stack[-1]
    
    def current_component(self):
        return self.component_id_map[self.current_component_id()]

    def set_caption(self):
        """calls a hook to set the window caption based on the current component;
        called whenever the current component changes
        """
        caption = self.nav_stack[-1]
        self.run_hook("SET_CAPTION", caption)
    
    def navigate_to(self, new_id):
        print(f"! navigating to \"{new_id}\" !")
        if self.nav_stack:
            self.current_component().on_unmount()
        self.nav_stack.append(new_id)
        self.current_component().on_mount()
        self.set_caption()
        self.run_hook("TRIGGER_RERENDER")
    
    def navigate_back(self):
        if len(self.nav_stack) <= 1:
            raise RuntimeError("Cannot navigate back because nav_stack is already at the root")
        print(f"! navigating back !")
        self.current_component().on_unmount()
        self.nav_stack.pop()
        self.current_component().on_mount()
        self.set_caption()
        self.run_hook("TRIGGER_RERENDER")

    def step(self):
        """called once at the beginning of each frame by the root app"""
        stepped_descendants = self.stepped_descendants_id_map[self.current_component_id()]
        for desc in stepped_descendants:
            desc.step()
    
    def process_event(self, event):
        self.current_component().process_event(event)
    
    def on_mount(self):
        self.navigate_to(self.start_id)

    def render_onto(self, surf: pygame.Surface, region: pygame.Rect = None):
        surf.fill(self.background_color)
        self.current_component().render_onto(surf, region)
