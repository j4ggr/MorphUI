from typing import Any
from typing import Dict

from kivy.uix.label import Label

from .behaviors import MorphThemeBehavior
from .behaviors import MorphBackgroundBehavior
from .behaviors import MorphAutoSizingBehavior
from .behaviors import MorphIdentificationBehavior


__all__ = [
    'MorphLabel'
]


class MorphLabel(
        MorphIdentificationBehavior,
        MorphThemeBehavior,
        MorphBackgroundBehavior,
        MorphAutoSizingBehavior,
        Label):
    
    _default_settings: Dict[str, Any] = dict(
        halign='left',
        valign='middle',
        theme_color_bindings=dict(
            color='text_surface_color',
            background_color='surface_color',),)
    """Default settings for MorphLabel instances."""

    def __init__(self, **kwargs) -> None:
        _kwargs = self._default_settings | kwargs
        super().__init__(**_kwargs)
