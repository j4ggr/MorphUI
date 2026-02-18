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
                pos_hint={'center_x': 0.5, 'center_y': 0.6},
                theme_color_bindings=dict(
                    normal_content_color='primary_color',
                    normal_surface_color='transparent_color',
                    normal_border_color='outline_variant_color',),),
            MorphFilterChip(
                identity='filter',
                label_text='Filter Chip',
                pos_hint={'center_x': 0.5, 'center_y': 0.5}),
            MorphInputChip(
                identity='input_chip',
                label_text='Input Chip',
                pos_hint={'center_x': 0.5, 'center_y': 0.4},),
            theme_color_bindings={
                'normal_surface_color': 'surface_container_low_color',})
        self.input_chip = self.layout.identities.input_chip
        self.input_chip.bind(on_trailing_widget_release=self.re_add_chip)
        return self.layout
        
    def re_add_chip(self, dt: float) -> None:
        def _re_add(dt):
            if not self.input_chip.parent:
                self.layout.add_widget(self.input_chip)
        Clock.schedule_once(_re_add, 2)

if __name__ == '__main__':
    MyApp().run()