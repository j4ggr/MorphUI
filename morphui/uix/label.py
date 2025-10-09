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
    
    default_config: Dict[str, Any] = dict(
        halign='left',
        valign='middle',
        theme_color_bindings=dict(
            content_color='content_surface_color',
            surface_color='transparent_color',),
        typography_role='Title',
        typography_size='medium',
        typography_weight='Regular',)
    """Default configuration values for MorphLabel instances.
    
    Provides standard label appearance and behavior settings:
    - Left alignment for text readability
    - Middle vertical alignment for centered appearance
    - Surface content colors for theme integration
    - Label typography role with medium sizing
    
    These values can be overridden by subclasses or during 
    instantiation.
    
    Notes
    -----
    - The `theme_color_bindings` are automatically removed when 
      `theme_style` is specified.
    - Typography properties are applied if the typography behavior is
    """

    def __init__(self, **kwargs) -> None:
        config = self.default_config.copy()
        if 'theme_style' in kwargs:
            config.pop('theme_color_bindings')
        config.update(kwargs)
        super().__init__(**config)
        for option in self.typography.available_style_properties:
            if option in kwargs and hasattr(self, option):
                setattr(self, option, kwargs[option])


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

    default_config: Dict[str, Any] = dict(
        font_name='MaterialIcons',
        halign='center',
        valign='middle',
        theme_color_bindings=dict(
            content_color='primary_color',
            surface_color='transparent_color',),
        font_size='36sp',
        auto_size=True,)
    """Default configuration values for MorphIconLabel instances.
    
    Provides icon-specific display and behavior settings:
    - MaterialIcons font for icon character rendering
    - Center alignment for optimal icon positioning
    - Primary color theme for icon prominence
    - Label typography role with medium sizing
    
    Inherits from MorphLabel but overrides key settings for icon 
    display. The `theme_color_bindings` are automatically removed when 
    `theme_style` is specified.
    """

    def __init__(self, **kwargs) -> None:
        config = self.default_config.copy()
        if 'theme_style' in kwargs:
            config.pop('theme_color_bindings')
        config.update(kwargs)
        super().__init__(**config)
        self.bind(icon=self._apply_icon)
        self._apply_icon(self, self.icon)

    def _apply_icon(self, instance: Any, icon: str) -> None:
        """Update the label text when the icon property changes.
        
        This method looks up the icon name in the typography's icon map
        and sets the label's text to the corresponding character.
        """
        self.text = self.typography.get_icon_character(icon)
