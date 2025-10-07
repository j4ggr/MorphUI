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
from kivy.uix.behaviors.touchripple import TouchRippleBehavior

class RippleLabel(TouchRippleBehavior, MorphLabel):

    def __init__(self, **kwargs):
        super(RippleLabel, self).__init__(**kwargs)

    def on_touch_down(self, touch):
        collide_point = self.collide_point(touch.x, touch.y)
        if collide_point:
            touch.grab(self)
            self.ripple_show(touch)
            return True
        return False

    def on_touch_up(self, touch):
        if touch.grab_current is self:
            touch.ungrab(self)
            self.ripple_fade()
            return True
        return False
    
class MyApp(MorphApp):
    def build(self) -> MorphBoxLayout:
        self.theme_manager.seed_color = 'Purple'
        return MorphBoxLayout(
            RippleLabel(
                text="Label 1",
                theme_style='primary',
                auto_size=True,),
            MorphLabel(
                text="Label 2",
                theme_style='secondary',
                auto_size=True,),
            theme_style='surface',
            auto_size=False,)

if __name__ == '__main__':
    MyApp().run()