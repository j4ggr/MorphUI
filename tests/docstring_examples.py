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

from morphui.app import MorphApp
from morphui.uix.label import MorphIconLabel
from morphui.uix.behaviors import MorphToggleButtonBehavior
from morphui.uix.floatlayout import MorphFloatLayout

class MyWidget(
        MorphToggleButtonBehavior,
        MorphIconLabel,):

    default_config = (
        MorphIconLabel.default_config.copy() | dict(
        theme_color_bindings=dict(
            surface_color='transparent_color',
            content_color='content_surface_variant_color',
            border_color='outline_color',
            active_surface_color='primary_color',
            active_content_color='content_primary_color',),
        round_sides=True,
        active_radius_enabled=True,))

class MyApp(MorphApp):
    def build(self) -> MorphFloatLayout:
        self.theme_manager.switch_to_dark()
        return MorphFloatLayout(
            MyWidget(
                identity='my_widget',
                icon='language-python',
                pos_hint={'center_x': 0.5, 'center_y': 0.5},),
            surface_color=self.theme_manager.surface_color,)

if __name__ == '__main__':
    MyApp().run()