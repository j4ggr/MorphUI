"""Example application demonstrating MorphLinearProgress and
MorphCircularProgress in both determinate and indeterminate modes.

Run this file directly to launch the demo:

    python examples/progress_example.py

Controls
--------
- Slider      : change the determinate value (0–100)
- Toggle btn  : switch between Light and Dark theme
"""
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parents[1].resolve()))

from kivy.metrics import dp

from morphui.app import MorphApp
from morphui.uix.label import MorphSimpleLabel
from morphui.uix.button import MorphButton
from morphui.uix.boxlayout import MorphBoxLayout
from morphui.uix.floatlayout import MorphFloatLayout
from morphui.uix.progress import MorphLinearProgress
from morphui.uix.progress import MorphCircularProgress


class ProgressExampleApp(MorphApp):

    def build(self) -> MorphFloatLayout:
        self.theme_manager.seed_color = 'morphui_teal'
        self.theme_manager.theme_mode = 'Light'

        # --- determinate indicators ---
        self.linear_det = MorphLinearProgress(
            value=0.4,
            size_hint_x=1,)

        self.circular_det = MorphCircularProgress(
            value=0.4,
            size=(dp(64), dp(64)),)

        # --- indeterminate indicators ---
        self.linear_ind = MorphLinearProgress(
            indeterminate=True,
            size_hint_x=1,)

        self.circular_ind = MorphCircularProgress(
            indeterminate=True,
            size=(dp(64), dp(64)),
            thickness=dp(4),)

        # --- value label ---
        self.value_label = MorphSimpleLabel(
            text='Value: 40%',
            auto_size=True,)

        # --- slider (simulated with two buttons) ---
        btn_minus = MorphButton(
            text='−10 %',
            size_hint=(None, None),
            size=(dp(80), dp(40)),
            on_press=self._decrement,)

        btn_plus = MorphButton(
            text='+10 %',
            size_hint=(None, None),
            size=(dp(80), dp(40)),
            on_press=self._increment,)

        btn_theme = MorphButton(
            text='Toggle Dark / Light',
            size_hint=(None, None),
            size=(dp(180), dp(40)),
            on_press=self._toggle_theme,)

        control_row = MorphBoxLayout(
            btn_minus,
            self.value_label,
            btn_plus,
            btn_theme,
            orientation='horizontal',
            spacing=dp(12),
            size_hint_y=None,
            height=dp(48),)

        # --- section labels ---
        def section(text):
            return MorphSimpleLabel(
                text=text,
                auto_size=True,)

        circular_row = MorphBoxLayout(
            MorphBoxLayout(
                section('Determinate'),
                self.circular_det,
                orientation='vertical',
                spacing=dp(8),
                size_hint=(None, None),
                size=(dp(120), dp(120)),),
            MorphBoxLayout(
                section('Indeterminate'),
                self.circular_ind,
                orientation='vertical',
                spacing=dp(8),
                size_hint=(None, None),
                size=(dp(120), dp(120)),),
            orientation='horizontal',
            spacing=dp(24),
            size_hint_y=None,
            height=dp(120),)

        content = MorphBoxLayout(
            section('Linear — Determinate'),
            self.linear_det,
            section('Linear — Indeterminate'),
            self.linear_ind,
            section('Circular'),
            circular_row,
            control_row,
            orientation='vertical',
            spacing=dp(16),
            padding=dp(40),
            size_hint=(0.9, None),)

        content.bind(minimum_height=content.setter('height'))

        root = MorphFloatLayout(
            content,
            theme_color_bindings={
                'normal_surface_color': 'surface_color',},)

        content.pos_hint = {'center_x': 0.5, 'center_y': 0.5}
        return root

    # ------------------------------------------------------------------
    # Callbacks
    # ------------------------------------------------------------------

    def _increment(self, *args) -> None:
        new_val = min(1.0, self.linear_det.value + 0.1)
        self.linear_det.value = new_val
        self.circular_det.value = new_val
        self.value_label.text = f'Value: {new_val:.0%}'

    def _decrement(self, *args) -> None:
        new_val = max(0, self.linear_det.value - 0.1)
        self.linear_det.value = new_val
        self.circular_det.value = new_val
        self.value_label.text = f'Value: {new_val:.0%}'

    def _toggle_theme(self, *args) -> None:
        current = self.theme_manager.theme_mode
        self.theme_manager.theme_mode = (
            'Dark' if current == 'Light' else 'Light')


if __name__ == '__main__':
    ProgressExampleApp().run()
