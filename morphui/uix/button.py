from typing import Any
from typing import Dict
from warnings import warn

from kivy.metrics import dp
from kivy.uix.label import Label
from kivy.properties import BooleanProperty

from morphui.utils import clean_config
from morphui.uix.label import MorphIconLabel
from morphui.uix.label import MorphSimpleIconLabel
from morphui.uix.label import MorphButtonTextLabel
from morphui.uix.label import MorphButtonLeadingIconLabel
from morphui.uix.behaviors import MorphIconBehavior
from morphui.uix.behaviors import MorphScaleBehavior
from morphui.uix.behaviors import MorphHoverBehavior
from morphui.uix.behaviors import MorphThemeBehavior
from morphui.uix.behaviors import MorphButtonBehavior
from morphui.uix.behaviors import MorphRippleBehavior
from morphui.uix.behaviors import MorphTooltipBehavior
from morphui.uix.behaviors import MorphElevationBehavior
from morphui.uix.behaviors import MorphAutoSizingBehavior
from morphui.uix.behaviors import MorphRoundSidesBehavior
from morphui.uix.behaviors import MorphContentLayerBehavior
from morphui.uix.behaviors import MorphCompleteLayerBehavior
from morphui.uix.behaviors import MorphDelegatedThemeBehavior
from morphui.uix.behaviors import MorphIdentificationBehavior
from morphui.uix.behaviors import MorphInteractionLayerBehavior
from morphui.uix.container import MorphLeadingTextContainer


__all__ = [
    'MorphSimpleIconButton',
    'MorphButton',
    'MorphIconButton',
    'MorphTrailingIconButton',
    'MorphChipTrailingIconButton',
    'MorphTextFieldTrailingIconButton',]


class MorphSimpleIconButton(
        MorphIconBehavior,
        MorphAutoSizingBehavior,
        MorphThemeBehavior,
        MorphHoverBehavior,
        MorphRippleBehavior,
        MorphInteractionLayerBehavior,
        MorphContentLayerBehavior,
        MorphButtonBehavior,
        MorphTooltipBehavior,
        Label):
    """A simple icon button widget with ripple effect and MorphUI
    theming.

    This class is a lightweight button designed for displaying icons
    with ripple effects and theming support. It is useful for scenarios
    where a full-featured button is not required but icon interaction is
    needed (e.g., toolbar buttons, or within a chip).
    """

    default_config: Dict[str, Any] = dict(
        theme_color_bindings=dict(
            normal_surface_color='transparent_color',
            disabled_border_color='outline_variant_color',
            normal_content_color='content_surface_color',
            hovered_content_color='content_surface_variant_color'),
        typography_role=MorphIconLabel.default_config['typography_role'],
        typography_size=MorphIconLabel.default_config['typography_size'],
        font_name=MorphIconLabel.default_config['font_name'],
        halign='center',
        valign='center',
        ripple_enabled=True,
        ripple_color=None,
        ripple_layer='interaction',
        padding=dp(8),
        auto_size=True,)
    """Default configuration values for MorphSimpleIconButton.
    
    Provides standard icon button appearance and behavior settings:
    - Center alignment for icon visibility
    - Middle vertical alignment for centered appearance
    - Bounded colors for theme integration
    - Ripple effect for touch feedback
    - Auto-sizing to fit content
    These values can be overridden by subclasses or during 
    instantiation.
    """

    def __init__(self, **kwargs) -> None:
        config = clean_config(self.default_config, kwargs)
        super().__init__(**config)


class MorphButton(
        MorphTooltipBehavior,
        MorphRoundSidesBehavior,
        MorphIdentificationBehavior,
        MorphHoverBehavior,
        MorphThemeBehavior,
        MorphRippleBehavior,
        MorphCompleteLayerBehavior,
        MorphButtonBehavior,
        MorphAutoSizingBehavior,
        MorphElevationBehavior,
        Label):
    """A button widget with ripple effect and MorphUI theming.
    
    This class combines Kivy's TouchRippleButtonBehavior with MorphUI's
    MorphLabel to create a button that supports ripple effects and 
    theming.
    """
    default_config: Dict[str, Any] = dict(
        halign='center',
        valign='center',
        theme_color_bindings={
            'normal_surface_color': 'surface_container_color',
            'normal_border_color': 'outline_color',
            'disabled_border_color': 'outline_variant_color',
            'normal_content_color': 'content_surface_color',
            'hovered_content_color': 'content_surface_variant_color',},
        ripple_enabled=True,
        ripple_color=None,
        ripple_layer='interaction',
        padding=dp(8),
        auto_size=True,)
    """Default configuration values for MorphButton.

    Provides standard button appearance and behavior settings:
    - Center alignment for text readability
    - Middle vertical alignment for centered appearance
    - Bounded colors for theme integration
    - Ripple effect for touch feedback
    - Auto-sizing to fit content
    
    These values can be overridden by subclasses or during 
    instantiation."""

    def __init__(self, **kwargs) -> None:
        config = clean_config(self.default_config, kwargs)
        super().__init__(**config)


class MorphIconButton(
        MorphIconBehavior,
        MorphButton):
    """A button widget designed for icon display with ripple effect 
    and MorphUI theming.
    
    This class is similar to MorphButton but is intended for use with
    icon fonts or images, providing a button that supports ripple 
    effects and theming.
    """

    default_config: Dict[str, Any] = dict(
        font_name=MorphIconLabel.default_config['font_name'],
        halign='center',
        valign='center',
        theme_color_bindings={
            'normal_surface_color': 'surface_container_color',
            'normal_content_color': 'content_surface_color',
            'hovered_content_color': 'content_surface_variant_color',
            'normal_border_color': 'outline_color',},
        typography_role=MorphIconLabel.default_config['typography_role'],
        typography_size=MorphIconLabel.default_config['typography_size'],
        ripple_enabled=True,
        ripple_color=None,
        ripple_layer='interaction',
        auto_size=True,
        padding=dp(8),
        radius=[5] * 4,
        )
    """Default configuration values for MorphIconButton.

    Provides standard icon button appearance and behavior settings:
    - Center alignment for icon visibility
    - Middle vertical alignment for centered appearance
    - Bounded colors for theme integration
    - Ripple effect for touch feedback
    - Auto-sizing to fit content
    - Rounded corners for a modern look

    These values can be overridden by subclasses or during 
    instantiation.
    """


class MorphTrailingIconButton(
        MorphScaleBehavior,
        MorphSimpleIconButton):
    """Trailing icon button for containers.
    
    This widget displays an interactive icon button on the right side
    of a container, with support for scale animations. Used primarily
    for chips where the trailing icon needs button behavior.
    """
    
    default_config: Dict[str, Any] = (
        MorphSimpleIconLabel.default_config.copy() | dict(
        padding=dp(0),
        pos_hint={'center_y': 0.5},))


class MorphIconTextButton(
        MorphIconBehavior,
        MorphTooltipBehavior,
        MorphRoundSidesBehavior,
        MorphDelegatedThemeBehavior,
        MorphHoverBehavior,
        MorphThemeBehavior,
        MorphRippleBehavior,
        MorphCompleteLayerBehavior,
        MorphButtonBehavior,
        MorphElevationBehavior,
        MorphLeadingTextContainer,):
    """A button widget that combines icon and text display with ripple
    effect and MorphUI theming.

    This class extends MorphLeadingTextContainer to create a button
    that supports both icon and text content, along with ripple effects
    and theming.

    Examples
    --------
    Simple usage of MorphIconTextButton in a MorphApp:
    ```python
    from morphui.app import MorphApp
    from morphui.uix.button import MorphIconTextButton
    from morphui.uix.floatlayout import MorphFloatLayout

    class MyApp(MorphApp):
        def build(self) -> MorphFloatLayout:
            self.theme_manager.seed_color = 'morphui_teal'
            self.theme_manager.switch_to_dark()
            return MorphFloatLayout(
                MorphIconTextButton(
                    identity='icon_text_button',
                    normal_icon='language-python',
                    label_text='Icon Text Button',
                    pos_hint={'center_x': 0.5, 'center_y': 0.5},),)
    
    if __name__ == '__main__':
        MyApp().run()
    ```

    Toggle behavior with MorphToggleButtonBehavior:
    ```python
    from morphui.app import MorphApp
    from morphui.uix.button import MorphIconTextButton
    from morphui.uix.floatlayout import MorphFloatLayout
    from morphui.uix.behaviors import MorphToggleButtonBehavior

    class ToggleIconTextButton(
            MorphIconTextButton,
            MorphToggleButtonBehavior):
        pass

    class MyApp(MorphApp):
        def build(self) -> MorphFloatLayout:
            self.theme_manager.seed_color = 'morphui_teal'
            self.theme_manager.switch_to_dark()
            return MorphFloatLayout(
                ToggleIconTextButton(
                    identity='icon_text_button',
                    normal_icon='language-python',
                    active_icon='language-java',
                    label_text='Icon Text Button',
                    pos_hint={'center_x': 0.5, 'center_y': 0.5},),)
        
    if __name__ == '__main__':
        MyApp().run()
    """ 

    _default_child_widgets = {
        'leading_widget': MorphButtonLeadingIconLabel,
        'label_widget': MorphButtonTextLabel,}
    """Default child widgets for MorphIconTextButton.

    - `leading_widget`: An instance of :class:`~morphui.uix.label.
      MorphButtonLeadingIconLabel` for displaying the leading icon.
    - `label_widget`: An instance of :class:`~morphui.uix.label.
      MorphButtonTextLabel` for displaying the button text.
    """

    default_config: Dict[str, Any] = dict(
        theme_color_bindings={
            'normal_surface_color': 'surface_container_color',
            'normal_border_color': 'outline_color',
            'disabled_border_color': 'outline_variant_color',
            'normal_content_color': 'content_surface_color',
            'hovered_content_color': 'content_surface_variant_color',},
        orientation='horizontal',
        ripple_enabled=True,
        ripple_color=None,
        ripple_layer='interaction',
        padding=dp(8),
        spacing=dp(4),
        radius=dp(4),
        auto_size=True,
        delegate_content_color=True,)
    """Default configuration values for MorphIconTextButton.

    Provides standard button appearance and behavior settings:
    - Bounded colors for theme integration
    - Ripple effect for touch feedback
    - Auto-sizing to fit content
    - Delegation of content color theming to child widgets
    These values can be overridden by subclasses or during 
    instantiation.
    """

    def __init__(self, **kwargs) -> None:
        config = clean_config(self.default_config, kwargs)
        if 'leading_icon' in kwargs:
            warn(
                "`leading_icon` is not supported. Use `normal_icon` instead.",
                UserWarning,)
            config['normal_icon'] = kwargs.pop('leading_icon')

        super().__init__(**config)
        self.delegate_to_children = [
            self.leading_widget,
            self.label_widget,]

    
    def _update_icon(self, *args) -> None:
        """Update the leading icon based on the toggle state.

        This method switches the leading icon between `normal_icon` and
        `active_icon` depending on whether the chip is active or not.
        """
        self.leading_icon = self.icon


class MorphChipTrailingIconButton(
        MorphTrailingIconButton):
    """Trailing icon button for chips.
    
    Inherits from :class:`~morphui.uix.button.MorphTrailingIconButton`.
    """
    pass


class MorphTextFieldTrailingIconButton(MorphIconButton):
    """Trailing icon button for text fields.

    Used primarily in text fields where the trailing icon needs button
    behavior (e.g., clear text button).
    """

    disabled: bool = BooleanProperty(False)
    """Indicates whether the button is disabled.

    When True, the label is rendered in a disabled state, typically with
    a different color or style to indicate it is not interactive.

    :attr:`disabled` is a :class:`kivy.properties.BooleanProperty` and
    defaults to False.
    """

    focus: bool = BooleanProperty(False)
    """Indicates whether the button is focused.

    When set to True, the button is considered focused, which may
    affect its visual appearance and behavior.
    
    :attr:`focus` is a :class:`kivy.properties.BooleanProperty` and
    defaults to False."""

    error: bool = BooleanProperty(False)
    """Indicates whether the button is in an error state.

    When set to True, the button is considered to be in an error state,
    which may affect its visual appearance and behavior.

    :attr:`error` is a :class:`kivy.properties.BooleanProperty` and
    defaults to False.
    """

    default_config: Dict[str, Any] = dict(
        theme_color_bindings=dict(
            normal_content_color='primary_color',
            normal_surface_color='transparent_color',
            hovered_content_color='content_surface_variant_color',),
        font_name=MorphIconButton.default_config['font_name'],
        typography_role=MorphIconButton.default_config['typography_role'],
        typography_size=MorphIconButton.default_config['typography_size'],
        focus_state_opacity=0.0,
        halign='center',
        valign='center',
        round_sides=True,
        ripple_enabled=False,
        size_hint=(None, None),
        size=(dp(24), dp(24)),
        padding=dp(0),)
