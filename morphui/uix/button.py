from typing import Any
from typing import Dict

from kivy.uix.label import Label

from .behaviors import MorphIconBehavior
from .behaviors import MorphHoverBehavior
from .behaviors import MorphThemeBehavior
from .behaviors import MorphButtonBehavior
from .behaviors import MorphRippleBehavior
from .behaviors import MorphElevationBehavior
from .behaviors import MorphAutoSizingBehavior
from .behaviors import MorphRoundSidesBehavior
from .behaviors import MorphCompleteLayerBehavior
from .behaviors import MorphIdentificationBehavior

from ..utils import clean_default_config

from .label import MorphIconLabel

__all__ = [
    'MorphButton',
    'MorphIconButton']


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
        valign='middle',
        theme_color_bindings={
            'surface_color': 'surface_container_color',
            'content_color': 'content_surface_color',
            'hovered_content_color': 'content_surface_variant_color',
            'border_color': 'outline_color',},
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
        config = clean_default_config(self.default_config) | kwargs
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
        valign='middle',
        theme_color_bindings={
            'surface_color': 'surface_container_color',
            'content_color': 'content_surface_color',
            'hovered_content_color': 'content_surface_variant_color',
            'border_color': 'outline_color',},
        typography_role=MorphIconLabel.default_config['typography_role'],
        typography_size=MorphIconLabel.default_config['typography_size'],
        ripple_enabled=True,
        ripple_color=None,
        ripple_layer='interaction',
        auto_size=True,
        padding=10,
        radius= [5] * 4,
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