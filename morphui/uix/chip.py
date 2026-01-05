from typing import Any
from typing import Dict

from kivy.metrics import dp

from morphui.uix.behaviors import MorphIconBehavior
from morphui.uix.behaviors import MorphHoverBehavior
from morphui.uix.behaviors import MorphRippleBehavior
from morphui.uix.behaviors import MorphButtonBehavior
from morphui.uix.behaviors import MorphElevationBehavior
from morphui.uix.behaviors import MorphRoundSidesBehavior
from morphui.uix.behaviors import MorphColorThemeBehavior
from morphui.uix.behaviors import MorphSurfaceLayerBehavior
from morphui.uix.behaviors import MorphToggleButtonBehavior
from morphui.uix.behaviors import MorphContentLayerBehavior
from morphui.uix.behaviors import MorphInteractionLayerBehavior

from morphui.uix.container import LeadingTextTrailingContainer

from morphui.uix.label import MorphChipTextLabel
from morphui.uix.label import MorphChipLeadingIconLabel

from morphui.uix.button import MorphChipTrailingIconButton


__all__ = [
    'MorphChip',
    'MorphFilterChip',
    'MorphInputChip',]


class MorphChip(
        MorphHoverBehavior,
        MorphRippleBehavior,
        MorphButtonBehavior,
        MorphColorThemeBehavior,
        MorphRoundSidesBehavior,
        MorphContentLayerBehavior,
        MorphInteractionLayerBehavior,
        MorphSurfaceLayerBehavior,
        MorphElevationBehavior,
        LeadingTextTrailingContainer,):
    """Morph Chip component.

    A chip is a compact element that represents an input, attribute, 
    or action. Chips can contain a leading icon, text, and a trailing 
    icon. They are typically used for filtering, assisting, input and
    suggestions.

    Use the `leading_icon` and `trailing_icon` properties to add
    icons to the chip. The `label_text` property is used to set the text
    of the chip.
    
    Inherits from :class:`~morphui.uix.container.LeadingTextTrailingContainer`
    which provides the base layout structure and child widget management.

    Example
    -------
    ````python
    from kivy.clock import Clock
    from morphui.app import MorphApp
    from morphui.uix.chip import MorphChip
    from morphui.uix.chip import MorphInputChip
    from morphui.uix.chip import MorphFilterChip
    from morphui.uix.floatlayout import MorphFloatLayout

    class MyApp(MorphApp):
        def build(self) -> MorphFloatLayout:
            self.theme_manager.seed_color = 'morphui_teal'
            self.theme_manager.switch_to_dark()
            self.layout = MorphFloatLayout(
                MorphChip(
                    identity='chip',
                    leading_icon='language-python',
                    trailing_icon='close',
                    label_text='Python Chip',
                    pos_hint={'center_x': 0.5, 'center_y': 0.6},),
                MorphFilterChip(
                    identity='filter',
                    label_text='Filter Chip',
                    pos_hint={'center_x': 0.5, 'center_y': 0.5}),
                MorphInputChip(
                    identity='input_chip',
                    label_text='Input Chip',
                    pos_hint={'center_x': 0.5, 'center_y': 0.4},),
                normal_surface_color=self.theme_manager.surface_color,)
            self.input_chip = self.layout.identities.input_chip
            return self.layout
        
        def on_start(self) -> None:
            Clock.schedule_interval(self.re_add_chip, 2)

        def re_add_chip(self, dt: float) -> None:
            if not self.input_chip.parent:
                self.layout.add_widget(self.input_chip)

    if __name__ == '__main__':
        MyApp().run()
    """

    _default_child_widgets = {
        'leading_widget': MorphChipLeadingIconLabel,
        'label_widget': MorphChipTextLabel,
        'trailing_widget': MorphChipTrailingIconButton,}
    """Default child widgets for the chip.

    This dictionary maps widget identities to their default classes.
    """

    default_config: Dict[str, Any] = dict(
        theme_color_bindings=dict(
            normal_surface_color='transparent_color',
            normal_border_color='outline_variant_color',),
        orientation='horizontal',
        auto_size=True,
        padding=dp(8),
        spacing=dp(8),
        radius=dp(8),
        round_sides=False,)
    """Default configuration for the :class:`MorphChip` component."""
    
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        
        self.bind(
            pos=self._update_layout,
            size=self._update_layout,
            spacing=self._update_layout,
            padding=self._update_layout,
            radius=self._update_layout,)
        self._update_layout()
    
    def _update_layout(self, *args) -> None:
        """Update the layout of the chip and its child widgets.
        
        This method recalculates and updates the layout of the chip
        and its child widgets based on the current properties such as
        size, padding, spacing, and radius.
        """
        if self.trailing_widget.icon:
            trailing_radius = [0, *self.clamped_radius[1:3], 0]
            expansion = [self.spacing / 2, *self.padding[1:]]
        else:
            trailing_radius = [0, 0, 0, 0]
            expansion = [0, 0, 0, 0]
        self.trailing_widget.radius = trailing_radius
        self.trailing_widget.interaction_layer_expansion = expansion


class MorphFilterChip(
        MorphIconBehavior,
        MorphToggleButtonBehavior,
        MorphChip):
    """Morph Filter Chip component.

    A filter chip represents a filter option that can be toggled on
    or off. It is used to apply filters to content or data sets.

    Example
    -------
    ````python
    from morphui.app import MorphApp
    from morphui.uix.chip import MorphFilterChip
    from morphui.uix.floatlayout import MorphFloatLayout

    class MyApp(MorphApp):
        def build(self) -> MorphFloatLayout:
            self.theme_manager.switch_to_dark()
            return MorphFloatLayout(
                MorphFilterChip(
                    identity='my_widget',
                    leading_icon='filter',),
                normal_surface_color=self.theme_manager.surface_color,)
    
    if __name__ == '__main__':
        MyApp().run()
    """

    default_config: Dict[str, Any] = (
        MorphChip.default_config.copy() | dict(
        theme_color_bindings=dict(
            normal_surface_color='transparent_color',
            normal_content_color='content_surface_color',
            normal_border_color='outline_variant_color',
            active_surface_color='secondary_container_color',
            active_content_color='content_secondary_container_color',
            active_border_color='transparent_color',
            disabled_surface_color='transparent_color',
            disabled_content_color='outline_color',),
        normal_icon='',
        active_icon='check',))
    """Default configuration for the :class:`MorphFilterChip` component."""

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
    
    def _update_icon(self, *args) -> None:
        """Update the leading icon based on the toggle state.

        This method switches the leading icon between `normal_icon` and
        `active_icon` depending on whether the chip is active or not.
        """
        print(self.active, self.icon)
        self.leading_icon = self.icon


class MorphInputChip(MorphChip):
    """Morph Input Chip component.

    An input chip represents a user input or selection that can be
    removed. It typically includes   a trailing icon button for removal.

    Example
    -------
    ````python
    from morphui.app import MorphApp
    from morphui.uix.chip import MorphInputChip
    from morphui.uix.floatlayout import MorphFloatLayout

    class MyApp(MorphApp):
        def build(self) -> MorphFloatLayout:
            self.theme_manager.switch_to_dark()
            return MorphFloatLayout(
                MorphInputChip(
                    identity='my_widget',
                    label_text='Input Chip',
                    trailing_icon='close',),
                normal_surface_color=self.theme_manager.surface_color,)
    if __name__ == '__main__':
        MyApp().run()
    """
    default_config: Dict[str, Any] = (
        MorphChip.default_config.copy() | dict(
            trailing_icon='close',))
    """Default configuration for the :class:`MorphInputChip` component."""

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.trailing_widget.bind(
            on_press=self.on_trailing_widget_release,
            on_release=self.on_trailing_widget_release)
    
    def on_trailing_widget_press(self, *args) -> None:
        """Handle the press event of the trailing icon button.

        This method is called when the trailing icon button is
        pressed. It can be used to provide visual feedback or
        initiate actions before the chip is removed.
        """
        pass

    def on_trailing_widget_release(self, *args) -> None:
        """Handle the release event of the trailing icon button.

        This method is called when the trailing icon button is
        released. It removes the chip from its parent layout.
        """
        if self.parent:
            self.parent.remove_widget(self)
