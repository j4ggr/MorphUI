from typing import Any
from typing import Dict

from kivy.uix.label import Label

from .behaviors import MorphThemeBehavior
from .behaviors import MorphAutoSizingBehavior
from .behaviors import MorphIdentificationBehavior
from .behaviors import MorphSurfaceLayerBehavior


__all__ = [
    'MorphLabel',]


class MorphLabel(
        MorphIdentificationBehavior,
        MorphThemeBehavior,
        MorphSurfaceLayerBehavior,
        MorphAutoSizingBehavior,
        Label):
    
    _default_settings: Dict[str, Any] = dict(
        halign='left',
        valign='middle',
        theme_color_bindings=dict(
            text_color='text_surface_color',
            surface_color='surface_color',),
        typography_role='Label',
        typography_size='medium',
        typography_weight='Regular',)
    """Default settings for MorphLabel instances."""

    def __init__(self, **kwargs) -> None:
        _kwargs = self._default_settings.copy()
        if 'theme_style' in kwargs:
            _kwargs.pop('theme_color_bindings')
        _kwargs = _kwargs | kwargs
        super().__init__(**_kwargs)
