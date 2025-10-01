"""
This file is used to test the docstring examples in the code.py file.
Just copy the code examples from the docstrings and paste them here.
Then run this file to see if there are any errors.
You can also use this file to test code snippets that are not in the
docstrings.

leave the first three lines as they are. They are used to set up the
path so that the imports work correctly. We add the
parent directory to the path so that we can import the morphui module.
In case the lines are missing, here they are again:

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parents[1].resolve()))
"""
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parents[1].resolve()))


# from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout

from morphui.app import MorphApp
from morphui.uix.behaviors.hover import MorphHoverBehavior


class HoverButton(Button, MorphHoverBehavior):
    '''A button with hover effects.'''

    hovered_text: str = "Hovered widget"

    normal_text: str = "Hover over me"

    def on_enter(self) -> None:
        self.color = (0, 0.8, 0.5, 1)  # Change color on hover
        self.text = self.hovered_text

    def on_leave(self) -> None:
        self.color = (1, 1, 1, 1)  # Reset color when not hovering
        self.text = self.normal_text

    def on_enter_edge(self, edge: str) -> None:
        self.text = f"Hovered {edge} edge"

    def on_leave_edge(self, edge: str) -> None:
        self.text = self.hovered_text if self.hovered else self.normal_text

    def on_enter_corner(self, corner: str) -> None:
        self.text = f"Hovered {corner} corner"

    def on_leave_corner(self, corner: str) -> None:
        self.text = self.hovered_text if self.hovered else self.normal_text


class HoverApp(MorphApp):
    def build(self) -> BoxLayout:
        layout = BoxLayout(padding=100)
        btn = HoverButton(text="Hover over me")
        layout.add_widget(btn)
        return layout
        
if __name__ == "__main__":
    HoverApp().run()