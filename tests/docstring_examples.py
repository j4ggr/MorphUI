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

from kivy.clock import Clock
from morphui.app import MorphApp
from morphui.uix.chip import MorphChip
from morphui.uix.chip import MorphInputChip
from morphui.uix.chip import MorphFilterChip
from morphui.uix.floatlayout import MorphFloatLayout

class MyApp(MorphApp):
    def build(self) -> MorphFloatLayout:
        self.theme_manager.seed_color = 'morphui_teal'
        self.theme_manager.switch_to_dark()
        self.layout = MorphFloatLayout(
            MorphChip(
                identity='chip',
                leading_icon='language-python',
                trailing_icon='close',
                label_text='Python Chip',
                pos_hint={'center_x': 0.5, 'center_y': 0.6},),
            MorphFilterChip(
                identity='filter',
                label_text='Filter Chip',
                pos_hint={'center_x': 0.5, 'center_y': 0.5}),
            MorphInputChip(
                identity='input_chip',
                label_text='Input Chip',
                pos_hint={'center_x': 0.5, 'center_y': 0.4},),
            normal_surface_color=self.theme_manager.surface_color,)
        self.input_chip = self.layout.identities.input_chip
        return self.layout
    
    def on_start(self) -> None:
        Clock.schedule_interval(self.re_add_chip, 2)

    def re_add_chip(self, dt: float) -> None:
        if not self.input_chip.parent:
            self.layout.add_widget(self.input_chip)

if __name__ == '__main__':
    MyApp().run()
