from kivy.app import App

from .theme.styles import ThemeManager


__all__ = [
    'MorphApp',]


class MorphApp(App):
    """Main application class."""

    theme_manager: ThemeManager = ThemeManager()
    """Theme manager instance for handling theming and styles."""


