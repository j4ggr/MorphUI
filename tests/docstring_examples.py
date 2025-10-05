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
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout

from morphui.app import MorphApp
from morphui.uix.behaviors import MorphBackgroundBehavior


class UserButton(MorphBackgroundBehavior, ButtonBehavior, Label):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)



class RootWidget(MorphBackgroundBehavior, BoxLayout):

    def __init__(self, **kwargs):
        # make sure we aren't overriding any important functionality
        super(RootWidget, self).__init__(**kwargs)

        # let's add a Widget to this layout
        self.add_widget(Widget())
        self.add_widget(
            UserButton(
                text="Hello World",
                size_hint=(None, .5),
                width=200,
                pos_hint={'center_x': .5, 'center_y': .5},
                background_color=(1, 0, 0, 0.5),  # semi-transparent red
                border_color=(0, 1, 0, 0.5),
                radius=[25, 5, 25, 5],# rounded corners
                border_width=2,))
        self.add_widget(Widget())


class MainApp(MorphApp):

    def build(self) -> RootWidget:
        self.root = root = RootWidget()
        root.background_color = (0, 0.5, 1, 0.8)  # Blue background
        root.border_color = (0.2, 0.8, 0.5, 0.2)  # Green border
        root.border_width = 0
        root.radius = [20, 20, 20, 20]  # Rounded corners
        return root



if __name__ == '__main__':
    MainApp().run()