#!/usr/bin/env python3
"""Test script for MorphResizeBehavior.

This script demonstrates the resize behavior functionality by creating
a simple resizable widget that can be dragged at edges and corners.
"""

from typing import Any
from typing import Dict

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle

# Import the resize behavior
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from morphui.uix.boxlayout import MorphBoxLayout
from morphui.uix.behaviors.resize import MorphResizeBehavior


class ResizableBox(MorphBoxLayout, MorphResizeBehavior):
    """A simple resizable box layout."""

    default_options: Dict[str, Any] = dict(
        min_size=(100, 100),
        max_size=(800, 600),
        size=(300, 200),
        resizing_overlay_edge_color=(0.7, 0.7, 0.7, 1),)

    def __init__(self, **kwargs) -> None:
        options = self.default_options.copy() | kwargs
        super().__init__(**options)
        self.label = Label(text=self.label_text, size_hint=(1, 0.2))
        self.add_widget(self.label)
        self.bind(size=self.update_text, pos=self.update_text)

    @property
    def label_text(self) -> str:
        return f'ResizableBox\nSize: {self.size}, Pos: {self.pos}'
    
    def update_text(self, *args) -> None:
        self.label.text = self.label_text


class ResizeTestApp(App):
    """Simple test app for resize behavior."""
    
    def build(self):
        # Create root widget
        root = MorphBoxLayout()
        
        # Create resizable test widget
        resizable = MorphBoxLayout(
            surface_color=[0.2, 0.6, 0.8, 1],)
        root.add_widget(resizable)
        
        resizable2 = ResizableBox(
            surface_color=[0.8, 0.3, 0.3, 1],)
        root.add_widget(resizable2)
        
        return root


if __name__ == '__main__':
    ResizeTestApp().run()