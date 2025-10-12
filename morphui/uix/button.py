from typing import Any
from typing import Dict

from kivy.uix.label import Label
from kivy.properties import StringProperty

from .behaviors import MorphThemeBehavior
from .behaviors import MorphButtonBehavior
from .behaviors import MorphRippleBehavior
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
        MorphThemeBehavior,
        MorphRippleBehavior,
        MorphCompleteLayerBehavior,
        MorphButtonBehavior,
        MorphAutoSizingBehavior,
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
        MorphRoundSidesBehavior,
        MorphIdentificationBehavior,
        MorphThemeBehavior,
        MorphRippleBehavior,
        MorphCompleteLayerBehavior,
        MorphButtonBehavior,
        MorphAutoSizingBehavior,
        Label):
    """A button widget designed for icon display with ripple effect 
    and MorphUI theming.
    
    This class is similar to MorphButton but is intended for use with
    icon fonts or images, providing a button that supports ripple 
    effects and theming.
    """

    icon: str = StringProperty('')
    """The name of the icon to display, corresponding to the icon font 
    mapping.
    
    This property should match a key in the typography's icon map.
    Changing this property will update the button's label to show the
    corresponding icon character.
    
    :attr:`icon` is a :class:`~kivy.properties.StringProperty`
    and defaults to ''.
    """

    default_config: Dict[str, Any] = dict(
        font_name=MorphIconLabel.default_config['font_name'],
        halign='center',
        valign='middle',
        theme_color_bindings={
            'surface_color': 'surface_container_color',
            'content_color': 'content_surface_color',
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

    def __init__(self, **kwargs) -> None:
        config = clean_default_config(self.default_config) | kwargs
        super().__init__(**config)
        self.bind(icon=self._apply_icon)
        self._apply_icon(self, self.icon)

    def _apply_icon(self, instance: Any, icon: str) -> None:
        """Update the label text when the icon property changes.
        
        This method looks up the icon name in the typography's icon map
        and sets the label's text to the corresponding character.
        """
        self.text = self.typography.get_icon_character(icon)
