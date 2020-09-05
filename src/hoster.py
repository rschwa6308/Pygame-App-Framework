from typing import Dict
import pygame

from component import Component


class Hoster(Component):
    def __init__(self, component_id_map: Dict[str, Component], start_id: str):
        super().__init__()

        self.component_id_map = component_id_map
        self.start_id = start_id

        self.children = self.component_id_map.values()

        self.nav_stack = []
        self.initialized = False

        for component in component_id_map.values():
            component.bind_hook("NAVIGATE_TO", self.navigate_to, bind_to_children=True)
            component.bind_hook("NAVIGATE_BACK", self.navigate_back, bind_to_children=True)
    
    def current_component(self):
        return self.component_id_map[self.nav_stack[-1]]
    
    def navigate_to(self, new_id):
        print(f"! navigating to \"{new_id}\" !")
        if self.nav_stack: self.current_component().on_unmount()
        self.nav_stack.append(new_id)
        self.current_component().on_mount()
        self.run_hook("TRIGGER_RERENDER")
    
    def navigate_back(self):
        if len(self.nav_stack) <= 1:
            raise RuntimeError("Cannot navigate back because nav_stack is already at the root")
        print(f"! navigating back !")
        self.current_component().on_unmount()
        self.nav_stack.pop()
        self.current_component().on_mount()
        self.run_hook("TRIGGER_RERENDER")
    
    def process_event(self, event):
        self.current_component().process_event(event)
    
    def on_mount(self):
        self.navigate_to(self.start_id)

    def render_onto(self, surf: pygame.Surface, region: pygame.Rect = None):
        self.current_component().render_onto(surf, region)
