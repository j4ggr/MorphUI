from typing import Self
from kivy.app import App

from .theme.styles import ThemeManager
from .theme.typography import Typography

    

__all__ = [
    'MorphApp',]


class MorphApp(App):
    """Main application class."""

    theme_manager: ThemeManager
    """Theme manager instance for handling theming and styles. The
    :attr:`theme_manager` attribute provides access to theme registration
    and style management functionalities. This is automatically
    initialized when a new :class:`MorphApp` instance is created before
    the :meth:`__init__` method is called."""

    typography: Typography
    """Typography system instance for managing text styles. The
    :attr:`typography` attribute provides access to font registration
    and text style management functionalities. This is automatically
    initialized when a new :class:`MorphApp` instance is created before
    the :meth:`__init__` method is called. The font registration defined
    in :attr:`Typography.fonts_to_autoregister` is processed during this
    instance creation."""

    def __new__(cls, **kwargs) -> Self:
        instance = super().__new__(cls)
        instance.theme_manager = ThemeManager()
        instance.typography = Typography()
        for font_dict in instance.typography.fonts_to_autoregister:
            instance.typography.register_font(**font_dict)
        return instance

