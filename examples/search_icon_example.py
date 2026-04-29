
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parents[1].resolve()))

from morphui.app import MorphApp
from morphui.uix.floatlayout import MorphFloatLayout
from morphui.uix.dropdown import MorphListItemFlat
from morphui.uix.dropdown import MorphDropdownFilterField
from morphui.uix.dropdown import MorphDropdownFilterFieldFilled
from morphui.uix.dropdown import MorphDropdownFilterFieldOutlined
from morphui.uix.dropdown import MorphDropdownFilterFieldRounded

class MyApp(MorphApp):
    def build(self) -> MorphFloatLayout:
        self.theme_manager.theme_mode = 'Dark'
        self.theme_manager.seed_color = 'morphui_teal'
        icon_items = [
            {
                'label_text': icon_name,
                'normal_leading_icon': icon_name,}
            for icon_name in sorted(self.typography.icon_map.keys())]
        layout = MorphFloatLayout(
            MorphDropdownFilterFieldOutlined(
                identity='outlined_picker',
                items=icon_items,
                heading_text='Search icons...',
                leading_icon='magnify',
                pos_hint={'center_x': 0.5, 'center_y': 0.9},
                size_hint=(0.8, None),),
            MorphDropdownFilterFieldFilled(
                identity='filled_picker',
                items=icon_items,
                heading_text='Search icons...',
                leading_icon='magnify',
                pos_hint={'center_x': 0.5, 'center_y': 0.7},
                size_hint=(0.8, None),),
            MorphDropdownFilterFieldRounded(
                identity='rounded_picker',
                items=icon_items,
                heading_text='Search icons...',
                leading_icon='magnify',
                pos_hint={'center_x': 0.5, 'center_y': 0.5},
                size_hint=(0.8, None),))
        self.outlined_picker = layout.identities.outlined_picker
        self.outlined_picker.bind(on_item_release=self.icon_selected_callback)
        self.filled_picker = layout.identities.filled_picker
        self.filled_picker.bind(on_item_release=self.icon_selected_callback)
        self.rounded_picker = layout.identities.rounded_picker
        self.rounded_picker.bind(on_item_release=self.icon_selected_callback)
        return layout

    def icon_selected_callback(
            self,
            picker: MorphDropdownFilterField,
            item: MorphListItemFlat,
            index: int
            ):
        picker.leading_icon = item.label_text
        picker.text = item.label_text

if __name__ == '__main__':
    MyApp().run()