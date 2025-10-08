from typing import Any
from typing import Dict

from kivy.uix.label import Label
from kivy.properties import StringProperty

from .behaviors import MorphThemeBehavior
from .behaviors import MorphTextLayerBehavior
from .behaviors import MorphAutoSizingBehavior
from .behaviors import MorphIdentificationBehavior


__all__ = [
    'MorphLabel',
    'MorphIconLabel',]


class MorphLabel(
        MorphIdentificationBehavior,
        MorphThemeBehavior,
        MorphTextLayerBehavior,
        MorphAutoSizingBehavior,
        Label,
        ):
    
    _default_settings: Dict[str, Any] = dict(
        halign='left',
        valign='middle',
        theme_color_bindings=dict(
            content_color='content_surface_color',
            surface_color='transparent_color',),
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


class MorphIconLabel(MorphLabel):
    """A label designed to display icons using icon fonts.

    This class extends `MorphLabel` to facilitate the use of icon fonts,
    allowing for easy integration of icons into your UI. It inherits all
    properties and behaviors from `MorphLabel`, including theming and
    auto-sizing capabilities.

    Examples
    --------
    ```python
    from morphui.app import MorphApp
    from morphui.uix.iconlabel import MorphIconLabel
    from morphui.uix.boxlayout import MorphBoxLayout

    class MyApp(MorphApp):
        def build(self):
            self.theme_manager.seed_color = 'Purple'
            return MorphBoxLayout(
                MorphIconLabel(
                    icon='home',
                    theme_style='primary',
                    typography_size='huge',),
                MorphIconLabel(
                    icon='user',
                    theme_style='secondary',
                    typography_size='huge',),
                orientation='vertical',
                padding=50,
                spacing=15,
                theme_style='surface',)
            )
    MyApp().run()
    ```
    """

    icon: str = StringProperty('')
    """The name of the icon to display, corresponding to the icon font 
    mapping."""

    _default_settings: Dict[str, Any] = dict(
        font_name='MaterialIcons',
        halign='center',
        valign='middle',
        theme_color_bindings=dict(
            content_color='primary_color',
            surface_color='transparent_color',),
        typography_role='Label',
        typography_size='medium',
        typography_weight='Regular',)
    """Default settings for MorphIconLabel instances."""

    def __init__(self, **kwargs) -> None:
        _kwargs = self._default_settings.copy()
        if 'theme_style' in kwargs:
            _kwargs.pop('theme_color_bindings')
        _kwargs = _kwargs | kwargs
        super().__init__(**_kwargs)
        self.bind(icon=self._apply_icon)
        self._apply_icon(self, self.icon)

    def _apply_icon(self, instance: Any, icon: str) -> None:
        """Update the label text when the icon property changes.
        
        This method looks up the icon name in the typography's icon map
        and sets the label's text to the corresponding character.
        """
        assert icon in self.typography.icon_map, (
            f"Icon '{icon}' not found in typography icon map.")
        self.text = self.typography.icon_map.get(icon, '')
        print(self.text)
