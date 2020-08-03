from typing import Dict

from Component import *

class Hoster(Component):
    def __init__(self, component_id_map: Dict[str, Component], start_id):       
        self.component_id_map = component_id_map
        self.current_id = start_id
        self.trigger_update = lambda: NotImplementedError("A trigger_update function has not yet been bound to this Hoster")
    
    def navigate_to(component_id):
        old_component = self.component_id_map[self.current_id]
        self.component_id_map[component_id]
        old_component.on_unmount()
        self.trigger_update()

    def render_onto(self, surf: pygame.Surface, region: pygame.Rect = None):
        component = self.component_id_map[self.current_id]
        component.render_onto(surf, region)
