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
from morphui.uix.behaviors import MorphHoverBehavior
from morphui.uix.behaviors import MorphStateLayerBehavior

class TestWidget(MorphHoverBehavior, MorphStateLayerBehavior, MorphLabel):
    pass

class MyApp(MorphApp):
    def build(self) -> MorphBoxLayout:
        layout = MorphBoxLayout(
            TestWidget(text="Hover Me", theme_style='primary'),
            TestWidget(
                text="Or Hover Me Too",
                theme_style='primary',
                disabled=True,),
            orientation='vertical',
            padding=100,
            spacing=10,
            theme_style='surface',)
        
        return layout


if __name__ == '__main__':
    MyApp().run()