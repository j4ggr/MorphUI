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
from morphui.uix.floatlayout import MorphFloatLayout
from morphui.uix.dropdown import MorphDropdownFilterField

class MyApp(MorphApp):
    def build(self) -> MorphFloatLayout:
        self.theme_manager.theme_mode = 'Dark'
        self.theme_manager.seed_color = 'morphui_teal'
        icon_items = [
            {
                'label_text': icon_name,
                'leading_icon': icon_name,}
            for icon_name in sorted(self.typography.icon_map.keys())]
        layout = MorphFloatLayout(
            MorphDropdownFilterField(
                identity='icon_picker',
                items=icon_items,
                item_release_callback=self.icon_selected_callback,
                heading_text='Search icons...',
                leading_icon='magnify',
                pos_hint={'center_x': 0.5, 'center_y': 0.9},
                size_hint=(0.8, None),))
        self.icon_picker = layout.identities.icon_picker
        return layout

    def icon_selected_callback(self, item, index):
        self.icon_picker.text = item.label_text
        self.icon_picker.leading_icon = item.label_text

if __name__ == '__main__':
    MyApp().run()