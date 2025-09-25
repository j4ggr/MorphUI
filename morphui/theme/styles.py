"""
Theme management system for MorphUI
"""

from .colors import ColorPalette, DarkColorPalette
from .typography import Typography


class ThemeManager:
    """Manages themes for MorphUI components"""
    
    _instance = None
    _current_theme = "light"
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        self.themes = {
            "light": {
                "colors": ColorPalette,
                "typography": Typography,
                "name": "Light Theme"
            },
            "dark": {
                "colors": DarkColorPalette,
                "typography": Typography,
                "name": "Dark Theme"
            }
        }
    
    @property
    def current_theme(self):
        """Get the current theme name"""
        return self._current_theme
    
    @current_theme.setter
    def current_theme(self, theme_name):
        """Set the current theme"""
        if theme_name in self.themes:
            self._current_theme = theme_name
        else:
            raise ValueError(f"Theme '{theme_name}' not found. Available themes: {list(self.themes.keys())}")
    
    @property
    def colors(self):
        """Get the color palette for the current theme"""
        return self.themes[self._current_theme]["colors"]
    
    @property
    def typography(self):
        """Get the typography settings for the current theme"""
        return self.themes[self._current_theme]["typography"]
    
    def get_theme_info(self):
        """Get information about the current theme"""
        return self.themes[self._current_theme]
    
    def register_theme(self, name, colors, typography, display_name=None):
        """Register a new custom theme"""
        self.themes[name] = {
            "colors": colors,
            "typography": typography,
            "name": display_name or name.title()
        }
    
    def get_available_themes(self):
        """Get list of available theme names"""
        return list(self.themes.keys())


# Global theme manager instance
theme_manager = ThemeManager()