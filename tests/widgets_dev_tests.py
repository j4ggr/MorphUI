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

from kivy.clock import Clock
from morphui.app import MorphApp

from morphui.uix.label import MorphLabel
from morphui.uix.label import MorphIconLabel

from morphui.uix.button import MorphButton
from morphui.uix.button import MorphIconButton

from morphui.uix.selection import MorphSwitch
from morphui.uix.selection import MorphCheckbox
from morphui.uix.selection import MorphRadioButton

from morphui.uix.boxlayout import MorphBoxLayout

from morphui.uix.textfield import MorphTextInput
from morphui.uix.textfield import MorphTextFieldFilled
from morphui.uix.textfield import MorphTextFieldRounded
from morphui.uix.textfield import MorphTextFieldOutlined


class DisabledButton(MorphButton):

    def switch_state(self, *args) -> None:
        self.disabled = not self.disabled
        self.elevation = 0 if self.disabled else 3

    def on_disabled(self, instance, disabled) -> None:
        self.text = "Disabled" if disabled else "Enabled"

class AutoSizeIcon(MorphIconLabel):

    def switch_auto_size(self, *args) -> None:
        new_state = not self.auto_size[0]
        self.auto_size = new_state, new_state
        self.active = new_state

class MyApp(MorphApp):
    def build(self) -> MorphBoxLayout:
        self.theme_manager.seed_color = 'Purple'
        width = 350
        layout = MorphBoxLayout(
            DisabledButton(
                identity='disabled_button',
                text="Disabled",
                theme_style='secondary',
                disabled=True,),
            AutoSizeIcon(
                auto_size_once=False,
                size_hint=(1, 1),
                identity='icon_label',
                normal_icon='language-python',
                active_icon='language-java'),
            MorphLabel(
                text="Morph default\n Label",),
            MorphIconLabel(
                icon='language-python',),
            MorphButton(
                text="Morph Button",
                theme_style='primary',
                round_sides=True,
                elevation=1),
            MorphIconButton(
                icon='language-python',
                elevation=2,),
            MorphTextInput(
                identity='text_input',
                hint_text="Morph\nTextInput",
                radius=[2, 2, 2, 2],
                auto_height=True,
                theme_color_bindings={
                    'normal_surface_color': 'surface_container_color',
                    'normal_content_color': 'content_surface_color',
                    'normal_border_color': 'outline_color',
                    'focus_border_color': 'primary_color',
                    'hint_text_color': 'primary_color'},),
            MorphTextFieldRounded(
                identity='rounded_textfield',
                leading_icon='magnify',
                label_text='Search in Rounded TextField',
                pos_hint={'center_x': 0.5, 'top': 0.9},
                size_hint_x=None,
                width=width,),
            MorphTextFieldOutlined(
                identity='outlined_textfield',
                leading_icon='account',
                label_text='User in Outlined TextField',
                pos_hint={'center_x': 0.5, 'top': 0.8},
                supporting_error_texts={
                    'none': 'No errors.',
                    'required': 'This field is required.',
                    'max_text_length': 'Maximum length is 12 characters.',},
                size_hint_x=None,
                multiline=True,
                max_text_length=12,
                width=width,
                required=True,),
            MorphTextFieldFilled(
                identity='filled_textfield',
                leading_icon='lock',
                label_text='Password in Filled TextField',
                password=True,
                pos_hint={'center_x': 0.5, 'top': 0.7},
                size_hint_x=None,
                width=width,),
            MorphBoxLayout(
                MorphCheckbox(
                    identity='checkbox',),
                MorphRadioButton(
                    identity='radiobutton1',
                    group='test_group',),
                MorphRadioButton(
                    identity='radiobutton2',
                    group='test_group',),
                MorphRadioButton(
                    identity='radiobutton3',
                    group='test_group',),
                MorphSwitch(
                    identity='switch',),
                orientation='horizontal',
                spacing=20,),
            theme_style='surface',
            orientation='vertical',
            padding=50,
            spacing=15,)
        self.icon_label = layout.identities.icon_label
        self.disabled_button = layout.identities.disabled_button
        self.text_input = layout.identities.text_input
        self.rounded_textfield = layout.identities.rounded_textfield
        self.outlined_textfield = layout.identities.outlined_textfield
        self.filled_textfield = layout.identities.filled_textfield
        self.checkbox = layout.identities.checkbox
        self.switch = layout.identities.switch
        return layout

    def on_start(self) -> None:
        dt = 2
        Clock.schedule_interval(self.disabled_button.switch_state, dt)
        Clock.schedule_interval(self.icon_label.switch_auto_size, dt)
        Clock.schedule_interval(self.theme_manager.toggle_theme_mode, dt * 2)
        Clock.schedule_interval(self.checkbox.trigger_ripple, 1)

        return super().on_start()

if __name__ == '__main__':
    MyApp().run()