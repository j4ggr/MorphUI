"""Example application demonstrating the sizing behaviors in
morphui.uix.behaviors.sizing:

- MorphSizeBoundsBehavior : lower/upper size constraints (inherited by
  MorphResizeBehavior, shown via the "Bounded resize" box below).
- MorphResizeBehavior     : drag-to-resize edges/corners, aspect ratio
  locking, and collapse/expand snapping.
- MorphAutoSizingBehavior : auto width/height/size based on content.

Run this file directly to launch the demo:

    python examples/sizing_example.py

Controls
--------
- Drag the edges/corners of the three boxes to resize them (hover to
  see the resizable edges highlighted).
- The left box is clamped between a minimum and maximum size.
- The middle box keeps its original width-to-height ratio while resized.
- The right box ("Sidebar") only resizes from its left edge; drag it
  small enough and it collapses shut, drag the thin strip back out to
  reopen it.
- Use the buttons at the bottom to grow/shrink the auto-sizing label
  and toggle which dimensions auto-size.
"""
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parents[1].resolve()))

from kivy.metrics import dp
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout

from morphui.app import MorphApp
from morphui.uix.label import MorphSimpleLabel
from morphui.uix.button import MorphButton
from morphui.uix.floatlayout import MorphFloatLayout
from morphui.uix.behaviors import MorphResizeBehavior
from morphui.uix.behaviors import MorphColorThemeBehavior
from morphui.uix.behaviors import MorphSurfaceLayerBehavior


def centered_label(**kwargs) -> MorphSimpleLabel:
    """Create a MorphSimpleLabel whose text stays centered as it resizes."""
    label = MorphSimpleLabel(halign='center', valign='middle', **kwargs)
    label.bind(size=label.setter('text_size'))
    return label


class ResizableBox(
        MorphResizeBehavior,
        MorphColorThemeBehavior,
        MorphSurfaceLayerBehavior,
        BoxLayout):
    """A themed box that can be resized by dragging its edges/corners.

    Combines :class:`MorphResizeBehavior` (drag-resize, size bounds,
    aspect ratio, collapse/expand) with surface theming so the box is
    visible and its resizable edges are highlighted on hover/drag.
    """

    def __init__(self, **kwargs) -> None:
        config = dict(
            orientation='vertical',
            padding=dp(10),
            size_hint=(None, None),) | kwargs
        super().__init__(**config)
        self.theme_color_bindings = {
            'normal_surface_color': 'surface_container_color',
            'normal_border_color': 'outline_variant_color',}
        self.border_width = dp(1)
        self.radius = [dp(10)]
        # Static highlight colors for the resize edge overlay.
        self.normal_overlay_edge_color = [0, 0, 0, 0.3]
        self.resizing_overlay_edge_color = [0.20, 0.47, 0.85, 1]
        self.overlay_edge_width = dp(2)


class SizingExampleApp(MorphApp):

    def build(self) -> MorphFloatLayout:
        self.theme_manager.seed_color = 'morphui_teal'
        self.theme_manager.theme_mode = 'Light'
        Window.size = (1000, 650)

        # --- box 1: lower/upper size bounds ---
        self.bounded_box = ResizableBox(
            pos=(dp(40), dp(260)),
            size=(dp(220), dp(160)),
            size_lower_bound=[dp(120), dp(90)],
            size_upper_bound=[dp(320), dp(260)],)
        self.bounded_readout = MorphSimpleLabel(
            text='',
            auto_size=True,
            size_hint=(1, None),)
        self.bounded_readout.bind(
            size=self.bounded_readout.setter('text_size'))
        self.bounded_box.add_widget(centered_label(
            text='Bounded resize\n100-320 x 90-260',
            size_hint=(1, None),))
        self.bounded_box.add_widget(self.bounded_readout)
        self.bounded_box.bind(size=self._update_bounded_readout)
        self._update_bounded_readout()

        # --- box 2: aspect ratio preservation ---
        self.aspect_box = ResizableBox(
            pos=(dp(320), dp(295)),
            size=(dp(220), dp(110)),  # 2:1 ratio, kept while resizing
            preserve_aspect_ratio=True,)
        self.aspect_box.add_widget(centered_label(
            text='Aspect ratio locked\n(2:1)',
            size_hint=(1, 1),))

        # --- box 3: collapsible sidebar ---
        self.sidebar = ResizableBox(
            pos=(dp(600), dp(180)),
            size=(dp(220), dp(240)),
            resizable_edges=['left'],
            size_lower_bound=[dp(160), -1],
            collapsible=True,
            collapse_threshold=0.4,
            expand_threshold=0.6,)
        self.sidebar_label = centered_label(
            text='Collapsible sidebar\n(drag left edge)',
            size_hint=(1, 1),)
        self.sidebar.add_widget(self.sidebar_label)
        self.sidebar.bind(on_collapse=self._on_sidebar_collapse)
        self.sidebar.bind(on_expand=self._on_sidebar_expand)

        self.status_label = centered_label(
            text='Status: expanded',
            pos=(dp(600), dp(140)),
            size=(dp(220), dp(24)),
            size_hint=(None, None),)

        # --- auto-sizing demo ---
        self.auto_label = MorphSimpleLabel(
            text='Auto-sizing label',
            pos=(dp(40), dp(60)),
            auto_size=True,)

        add_text_btn = MorphButton(
            text='Add text',
            pos=(dp(40), dp(20)),
            size_hint=(None, None),
            size=(dp(100), dp(36)),
            on_press=self._grow_auto_label,)
        reset_text_btn = MorphButton(
            text='Reset text',
            pos=(dp(150), dp(20)),
            size_hint=(None, None),
            size=(dp(100), dp(36)),
            on_press=self._reset_auto_label,)
        toggle_width_btn = MorphButton(
            text='Toggle auto_width',
            pos=(dp(260), dp(20)),
            size_hint=(None, None),
            size=(dp(160), dp(36)),
            on_press=self._toggle_auto_width,)
        toggle_height_btn = MorphButton(
            text='Toggle auto_height',
            pos=(dp(430), dp(20)),
            size_hint=(None, None),
            size=(dp(160), dp(36)),
            on_press=self._toggle_auto_height,)

        title = centered_label(
            text='MorphUI sizing behaviors demo',
            pos=(dp(40), dp(600)),
            size=(dp(920), dp(30)),
            size_hint=(None, None),)

        return MorphFloatLayout(
            title,
            self.bounded_box,
            self.aspect_box,
            self.sidebar,
            self.status_label,
            self.auto_label,
            add_text_btn,
            reset_text_btn,
            toggle_width_btn,
            toggle_height_btn,
            theme_color_bindings={
                'normal_surface_color': 'background_color',},)

    def _update_bounded_readout(self, *args) -> None:
        """Keep the live size readout for the bounded box in sync."""
        self.bounded_readout.text = (
            f'Size: {int(self.bounded_box.width)} '
            f'x {int(self.bounded_box.height)}')

    def _on_sidebar_collapse(self, instance, axis) -> None:
        """Update the status label when the sidebar collapses shut."""
        self.status_label.text = f'Status: collapsed ({axis})'

    def _on_sidebar_expand(self, instance, axis) -> None:
        """Update the status label when the sidebar pops back open."""
        self.status_label.text = f'Status: expanded ({axis})'

    def _grow_auto_label(self, *args) -> None:
        """Append more text so the auto-sizing label grows."""
        self.auto_label.text += ' + more content'

    def _reset_auto_label(self, *args) -> None:
        """Reset the auto-sizing label back to its initial text."""
        self.auto_label.text = 'Auto-sizing label'

    def _toggle_auto_width(self, *args) -> None:
        """Toggle MorphAutoSizingBehavior.auto_width on the label."""
        self.auto_label.auto_width = not self.auto_label.auto_width

    def _toggle_auto_height(self, *args) -> None:
        """Toggle MorphAutoSizingBehavior.auto_height on the label."""
        self.auto_label.auto_height = not self.auto_label.auto_height


if __name__ == '__main__':
    SizingExampleApp().run()
