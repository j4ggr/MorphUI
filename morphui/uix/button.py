from typing import Any
from typing import Dict

from kivy.metrics import dp
from kivy.uix.label import Label

from morphui.uix.behaviors import MorphIconBehavior
from morphui.uix.behaviors import MorphScaleBehavior
from morphui.uix.behaviors import MorphHoverBehavior
from morphui.uix.behaviors import MorphThemeBehavior
from morphui.uix.behaviors import MorphButtonBehavior
from morphui.uix.behaviors import MorphRippleBehavior
from morphui.uix.behaviors import MorphElevationBehavior
from morphui.uix.behaviors import MorphAutoSizingBehavior
from morphui.uix.behaviors import MorphRoundSidesBehavior
from morphui.uix.behaviors import MorphCompleteLayerBehavior
from morphui.uix.behaviors import MorphIdentificationBehavior
from morphui.uix.behaviors import MorphInteractionLayerBehavior

from morphui.utils import clean_config

from morphui.uix.label import MorphIconLabel
from morphui.uix.label import MorphSimpleIconLabel

__all__ = [
    'MorphSimpleIconButton',
    'MorphButton',
    'MorphIconButton',
    'MorphTrailingIconButton',
    'MorphChipTrailingIconButton',]


class MorphSimpleIconButton(
        MorphIconBehavior,
        MorphAutoSizingBehavior,
        MorphThemeBehavior,
        MorphHoverBehavior,
        MorphRippleBehavior,
        MorphInteractionLayerBehavior,
        MorphButtonBehavior,
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
        padding=10,
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



class MorphChipTrailingIconButton(
        MorphTrailingIconButton):
    """Trailing icon button for chips.
    
    Inherits from :class:`~morphui.uix.button.MorphTrailingIconButton`.
    """
    pass
