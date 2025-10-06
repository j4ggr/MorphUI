from typing import Self
from kivy.app import App

from .theme.manager import ThemeManager
from .theme.typography import Typography

    

__all__ = [
    'MorphApp',]


class MorphApp(App):
    """Main application class."""

    _theme_manager: ThemeManager = ThemeManager()
    """Theme manager instance for handling theming and styles."""

    _typography: Typography = Typography()
    """Typography instance for managing fonts and text styles."""

    def __new__(cls, **kwargs) -> Self:
        """Override __new__ to register fonts before instance creation."""
        instance = super().__new__(cls)
        for font_dict in instance._typography.fonts_to_autoregister:
            instance._typography.register_font(**font_dict)
        return instance

    @property
    def theme_manager(self) -> ThemeManager:
        """Access the theme manager for theming and style management.
        (read-only).

        The :attr:`theme_manager` attribute provides access to the
        :class:`ThemeManager` instance, which handles theming and style
        management. This instance is automatically initialized as a
        class attribute.
        """
        return self._theme_manager

    @property
    def typography(self) -> Typography:
        """Access the typography system for text style management.
        (read-only).

        The :attr:`typography` attribute provides access to the
        :class:`Typography` instance, which handles font registration
        and text style management. This instance is automatically
        initialized as a class attribute.
        """
        return self._typography
