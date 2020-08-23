from typing import Dict

from Component import *

class Hoster(Component):
    def __init__(self, component_id_map: Dict[str, Component], start_id):
        super().__init__()

        self.component_id_map = component_id_map
        self.children = self.component_id_map.values()
        self.current_id = start_id

        for component in component_id_map.values():
            component.bind_hook("NAVIGATE_TO", self.navigate_to, bind_to_children=True)
    
    def current_component(self):
        return self.component_id_map[self.current_id]
    
    def navigate_to(self, new_id):
        print(f"! navigating to \"{new_id}\" !")
        self.current_component().on_unmount()
        self.component_id_map[new_id].on_mount()
        self.current_id = new_id
        self.run_hook("TRIGGER_UPDATE")
    
    def process_event(self, event):
        self.current_component().process_event(event)

    def render_onto(self, surf: pygame.Surface, region: pygame.Rect = None):
        self.current_component().render_onto(surf, region)
