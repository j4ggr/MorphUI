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
from morphui.uix.gridlayout import MorphGridLayout

class MyApp(MorphApp):
    def build(self) -> MorphGridLayout:
        # self.typography.font_name = 'DMSans' # Uncomment to test custom font
        labels = []
        for role, variants in self.typography.text_styles.items():
            for size, style in variants.items():
                for weight in ('Thin', 'Regular', 'Heavy'):
                    label = MorphLabel(
                        text=(
                            f'{role}: {size}, {weight}, '
                            f'{style["font_size"]}, {style["line_height"]}'),
                        typography_role=role,
                        typography_size=size,
                        typography_weight=weight,
                        auto_height=True,)
                    labels.append(label)
        
        self.root = MorphGridLayout(
            *labels,
            theme_style='surface',
            cols=3,
            padding=50,
            spacing=15,)
        return self.root

if __name__ == '__main__':
    MyApp().run()