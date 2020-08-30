from __future__ import annotations
from typing import Tuple, Sequence

import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"   # bruh

import pygame


class Component:
    """The base class for all UI elements"""
    def __init__(
        self,
        children: Sequence[Component] = []
    ):
        self.children = children

        # Hooks are functions belonging to objects higher up in the tree (e.g. navigation actions)
        self.hooks = {}

    def render_onto(self, surf: pygame.Surface):
        """Render the contents of self to the given surface"""
        raise NotImplementedError("Component subclass must implement the render_onto() method")

    def on_mount(self):
        """Called immediately before component is mounted to a Hoster"""

    def on_unmount(self):
        """Called immediately after component is unmounted from a Hoster"""

    def process_event(self, event: pygame.event.EventType):
        """Process the given pygame event object"""

    def bind_hook(self, name: str, func, bind_to_children=False):
        """Bind a hook function (with a given name) to this component.
        If bind_to_children is True, the hook will also be bound to all children recursively
        """
        self.hooks[name] = func
        if bind_to_children:
            for child in self.children:
                child.bind_hook(name, func, bind_to_children=True)

    def run_hook(self, name: str, *args, **kwargs):
        """Run a previously bound hook (with a given name)"""
        if name not in self.hooks:
            raise ValueError(f"A \"{name}\" hook has not yet been bound to this component")
        
        self.hooks[name](*args, **kwargs)
