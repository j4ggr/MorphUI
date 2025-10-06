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
from kivy.clock import Clock
from morphui.app import MorphApp
from morphui.uix.boxlayout import MorphBoxLayout
from morphui.uix.label import MorphLabel

class MyApp(MorphApp):
    def build(self) -> MorphBoxLayout:
        self.root = MorphBoxLayout(
            MorphLabel(
                identity="label1",
                text="Label 1",),
            MorphLabel(
                identity="label2",
                text="Label 2",
                theme_style='secondary',
                radius=[25, 5, 25, 5],),
            theme_style='surface',
            orientation='vertical',
            padding=10,
            spacing=10,)
        return self.root
    
    def on_start(self) -> None:
        Clock.schedule_interval(self.theme_manager.toggle_theme_mode, 2)


if __name__ == '__main__':
    MyApp().run()