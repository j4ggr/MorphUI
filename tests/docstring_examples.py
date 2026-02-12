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
from morphui.uix.pickers import MorphDockedDatePickerField
from morphui.uix.floatlayout import MorphFloatLayout

class MyApp(MorphApp):

    def build(self) -> MorphFloatLayout:
        self.theme_manager.theme_mode = 'Dark'
        self.theme_manager.seed_color = 'morphui_teal'

        self.layout = MorphFloatLayout(
            MorphDockedDatePickerField(
                kind='range',
                identity='date_picker_field',
                pos_hint={'center_x': 0.5, 'center_y': 0.8},
                size_hint_x= 0.6,))

        return self.layout

if __name__ == "__main__":
    MyApp().run()