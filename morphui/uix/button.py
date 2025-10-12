from typing import Any
from typing import Dict

from kivy.uix.label import Label

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
        ripple_color=None,
        ripple_layer='interaction',
        auto_size=True,)
    def __init__(self, **kwargs) -> None:
        config = clean_default_config(self.default_config) | kwargs
        super().__init__(**config)
        print(self.available_states)


class MorphIconButton(
        MorphRippleBehavior,
        MorphButtonBehavior,
        MorphIconLabel):
    """A button widget designed for icon display with ripple effect 
    and MorphUI theming.
    
    This class is similar to MorphButton but is intended for use with
    icon fonts or images, providing a button that supports ripple 
    effects and theming.
    """
    pass