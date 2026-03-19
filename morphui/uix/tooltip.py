from typing import Any
from typing import Dict

from kivy.metrics import dp
from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout

from morphui.uix.behaviors import MorphElevationBehavior
from morphui.uix.behaviors import MorphAutoSizingBehavior
from morphui.uix.behaviors import MorphMenuMotionBehavior
from morphui.uix.behaviors import MorphColorThemeBehavior
from morphui.uix.behaviors import MorphDeclarativeBehavior
from morphui.uix.behaviors import MorphSurfaceLayerBehavior

from morphui.uix.label import MorphTooltipLabel
from morphui.uix.label import MorphTooltipHeadingLabel


__all__ = [
    'MorphTooltip',
    'MorphSimpleTooltip',
    'MorphRichTooltip',]


class MorphTooltip(
        MorphDeclarativeBehavior,
        MorphMenuMotionBehavior,
        MorphColorThemeBehavior,
        MorphSurfaceLayerBehavior,
        MorphElevationBehavior,
        MorphAutoSizingBehavior,
        BoxLayout):
    """A tooltip widget that provides brief information about a UI element
    when hovered over.

    This widget combines the motion behavior for menu-like positioning
    with elevation styling to create a visually distinct tooltip.
    
    Example
    -------
    ```python
    from morphui.app import MorphApp
    from morphui.uix.label import MorphSimpleLabel
    from morphui.uix.button import MorphIconButton
    from morphui.uix.tooltip import MorphTooltip
    from morphui.uix.floatlayout import MorphFloatLayout

    class MyApp(MorphApp):

        def build(self) -> MorphFloatLayout:
            self.theme_manager.theme_mode = 'Dark'
            self.theme_manager.seed_color = 'morphui_teal'
            
            layout = MorphFloatLayout(
                MorphIconButton(
                    tooltip=MorphTooltip(
                        MorphSimpleLabel(
                            text="This is helpful information!",
                            auto_size=True),),
                    icon='information',
                    pos_hint={'center_x': 0.5, 'center_y': 0.5}),
                theme_color_bindings={
                    'normal_surface_color': 'surface_color',},)
            return layout

    if __name__ == '__main__':
        MyApp().run()
    ```
    """

    default_config: Dict[str, Any] = dict(
        theme_color_bindings=dict(
            normal_surface_color='surface_container_highest_color',),
        menu_caller_spacing=dp(8),
        orientation='vertical',
        padding=[dp(8), dp(4)],
        radius=dp(4),
        spacing=dp(5),
        elevation=2,
        scale_enabled=False,
        auto_size=(True, True),)
    """Default configuration for MorphTooltip."""
    
    def __init__(self, *widgets, **kwargs: Any) -> None:
        config = self.default_config.copy() | kwargs
        super().__init__(*widgets, **config)

    def _update_caller_bindings(self, *args) -> None:
        """Update bindings to the caller button's position and size.

        This method binds to the caller button's `pos` and `size`
        properties to adjust the tooltip position whenever the caller
        changes. If there is no caller set, it does nothing.
        """
        if self.caller is None:
            return
        
        super()._update_caller_bindings()
        self.caller.bind(
            on_enter=self.open,
            on_leave=self.dismiss,)

    def update_tooltip_text(self, text: str) -> None:
        """Update the primary text of the tooltip.

        Override in subclasses to map ``text`` to the appropriate child
        label. The default implementation is a no-op so that plain
        :class:`MorphTooltip` instances (with arbitrary child widgets)
        are unaffected.

        Parameters
        ----------
        text:
            The new text to display.
        """
        pass


class MorphSimpleTooltip(MorphTooltip):
    """A tooltip that displays a single line of text.

    This is the simplest tooltip variant: it wraps a
    :class:`~morphui.uix.label.MorphSimpleLabel` inside a
    :class:`MorphTooltip`.  Use it when you only need a short text hint.
    For richer content (icons, multi-line, etc.) subclass
    :class:`MorphTooltip` directly.

    Parameters
    ----------
    tooltip_text:
        The text to display inside the tooltip.
    **kwargs:
        Additional keyword arguments forwarded to :class:`MorphTooltip`.

    Example
    -------
    ```python
    from morphui.uix.button import MorphIconButton
    from morphui.uix.tooltip import MorphSimpleTooltip

    btn = MorphIconButton(
        tooltip=MorphSimpleTooltip(
            'This is helpful information!',
            menu_anchor_position='right'),
        icon='information')
    ```
    """

    def __init__(
            self,
            tooltip_text: str,
            **kwargs: Any) -> None:
        self._label = MorphTooltipLabel(text=tooltip_text)
        super().__init__(self._label, **kwargs)

    def update_tooltip_text(self, text: str) -> None:
        """Update the label text."""
        self._label.text = text


class MorphRichTooltip(MorphTooltip):
    """A tooltip with a bold heading and an optional supporting line.

    Composes a :class:`MorphTooltipHeadingLabel` and, when
    ``supporting`` is provided, a :class:`MorphTooltipLabel` below it.
    Both texts are exposed as :class:`~kivy.properties.StringProperty`
    so they can be updated after construction.

    Parameters
    ----------
    heading:
        The bold heading text displayed at the top of the tooltip.
    supporting:
        Optional secondary text displayed below the heading.
        Pass an empty string (default) to show only the heading.
    **kwargs:
        Additional keyword arguments forwarded to :class:`MorphTooltip`.

    Example
    -------
    ```python
    from morphui.uix.button import MorphIconButton
    from morphui.uix.tooltip import MorphRichTooltip

    btn = MorphIconButton(
        tooltip=MorphRichTooltip(
            heading='Unsaved changes',
            supporting='Your edits will be lost.',
            menu_anchor_position='right'),
        icon='warning')
    ```
    """

    heading: str = StringProperty('')
    """The bold heading text displayed at the top of the tooltip."""

    supporting: str = StringProperty('')
    """Optional secondary text displayed below the heading."""

    def __init__(
            self,
            heading: str = '',
            supporting: str = '',
            **kwargs: Any) -> None:
        self._heading_label = MorphTooltipHeadingLabel(text=heading)
        self._supporting_label = MorphTooltipLabel(text=supporting)

        widgets = [self._heading_label]
        if supporting:
            widgets.append(self._supporting_label)

        super().__init__(*widgets, **kwargs)
        self.heading = heading
        self.supporting = supporting

        self.bind(
            heading=lambda _, v: setattr(self._heading_label, 'text', v),
            supporting=self._on_supporting,)

    def update_tooltip_text(self, text: str) -> None:
        """Update the supporting text.

        Maps ``text`` to :attr:`supporting`, which is the contextual
        detail line below the fixed heading.
        """
        self.supporting = text

    def _on_supporting(self, _instance: Any, supporting: str) -> None:
        """Add or remove the supporting label when the text changes."""
        self._supporting_label.text = supporting
        if supporting and self._supporting_label not in self.children:
            self.add_widget(self._supporting_label)
        elif not supporting and self._supporting_label in self.children:
            self.remove_widget(self._supporting_label)
        