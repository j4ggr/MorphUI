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
from morphui.uix.label import MorphLabel
from morphui.uix.boxlayout import MorphBoxLayout
from morphui.uix.scrollview import MorphScrollView

class MyApp(MorphApp):

    def build(self) -> MorphScrollView:
        self.theme_manager.theme_mode = 'Dark'
        self.theme_manager.seed_color = 'morphui_teal'

        return MorphScrollView(
                MorphBoxLayout(
                    MorphLabel(text='Label 1', theme_style='primary'),
                    MorphLabel(text='Label 2', theme_style='secondary'),
                    MorphLabel(text='Label 3', theme_style='tertiary'),
                    size_hint=(1, None),
                    height=1000,
                    theme_style='surface',
                    orientation='vertical',
                    identity='scroll_content'),
                identity='scroll_view',)

if __name__ == "__main__":
    MyApp().run()