#!/usr/bin/env python3
"""Test script for MorphResizeBehavior.

This script demonstrates the resize behavior functionality by creating
a simple resizable widget that can be dragged at edges and corners.
"""

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle

# Import the resize behavior
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from morphui.uix.behaviors.resize import MorphResizeBehavior


class ResizableTestWidget(MorphResizeBehavior, Widget):
    """A test widget that demonstrates resize functionality."""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Set initial properties
        self.size = (200, 150)
        self.pos = (100, 100)
        
        # Customize resize behavior
        self.min_size = [80, 60]
        self.max_size = [400, 300]
        self.resize_edge_color = [0, 0.8, 0.2, 0.6]  # Green highlight
        
        # Create visual background
        with self.canvas.before:
            Color(0.3, 0.3, 0.8, 1)  # Blue background
            self.bg_rect = Rectangle(pos=self.pos, size=self.size)
        
        # Bind to update background when size/pos changes
        self.bind(pos=self.update_graphics, size=self.update_graphics)
        
        # Add a label to show current size
        self.label = Label(
            text=f'Size: {int(self.width)}x{int(self.height)}',
            pos=self.pos,
            size=self.size,
            color=(1, 1, 1, 1)
        )
        self.add_widget(self.label)
    
    def update_graphics(self, *args):
        """Update the background rectangle and label."""
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size
        self.label.pos = self.pos
        self.label.size = self.size
        self.label.text = f'Size: {int(self.width)}x{int(self.height)}\\nPos: {int(self.x)}, {int(self.y)}'
    
    def on_resize_start(self, edge_or_corner):
        """Handle resize start."""
        print(f"Started resizing from {edge_or_corner}")
        # Make widget semi-transparent during resize
        with self.canvas.before:
            Color(0.3, 0.3, 0.8, 0.7)
    
    def on_resize_end(self, edge_or_corner):
        """Handle resize end."""
        print(f"Finished resizing from {edge_or_corner}")
        print(f"Final size: {self.width}x{self.height}")
        # Restore full opacity
        with self.canvas.before:
            Color(0.3, 0.3, 0.8, 1)


class ResizeTestApp(App):
    """Simple test app for resize behavior."""
    
    def build(self):
        # Create root widget
        root = Widget()
        
        # Create resizable test widget
        resizable = ResizableTestWidget()
        root.add_widget(resizable)
        
        # Create a second resizable widget with aspect ratio preservation
        resizable2 = ResizableTestWidget()
        resizable2.pos = (350, 200)
        resizable2.preserve_aspect_ratio = True
        resizable2.resize_edge_color = [0.8, 0.2, 0, 0.6]  # Red highlight
        with resizable2.canvas.before:
            Color(0.8, 0.3, 0.3, 1)  # Red background
            resizable2.bg_rect = Rectangle(pos=resizable2.pos, size=resizable2.size)
        root.add_widget(resizable2)
        
        return root


if __name__ == '__main__':
    ResizeTestApp().run()