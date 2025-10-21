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
from morphui.uix.label import MorphSimpleIconLabel
from morphui.uix.boxlayout import MorphBoxLayout

class MyApp(MorphApp):
    def build(self):
        return MorphBoxLayout(
            MorphSimpleIconLabel(
                icon='home',
                typography_size='large',),
            MorphSimpleIconLabel(
                icon='language-python',
                typography_size='large',),
            orientation='vertical',
            padding=50,
            spacing=15,)
    
if __name__ == '__main__':
    MyApp().run()