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
from morphui.uix.button import MorphButton
from morphui.uix.boxlayout import MorphBoxLayout
from morphui.uix.screenmanager import MorphScreen
from morphui.uix.screenmanager import MorphScreenManager

class MyApp(MorphApp):
    def build(self) -> MorphBoxLayout:
        self.theme_manager.seed_color = 'morphui_teal'

        self.main_layout = MorphBoxLayout(
            MorphScreenManager(
                MorphScreen(
                    MorphButton(
                        text="Go to Screen 2",
                        on_release=lambda x: self.change_screen('screen2'),),
                    name='screen1',),
                MorphScreen(
                    MorphButton(
                        text="Go to Screen 1",
                        on_release=lambda x: self.change_screen('screen1'),),
                    name='screen2',),
                identity='screen_manager',),
            identity='main_layout',
            orientation='vertical',)
        return self.main_layout

    def change_screen(self, name: str) -> None:
        sm = self.main_layout.identities.screen_manager
        sm.current = name

if __name__ == '__main__':
    MyApp().run()