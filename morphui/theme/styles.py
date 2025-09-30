"""
Dynamic color management system for MorphUI

This module provides a dynamic color system that automatically updates
all widget colors when switching between light and dark themes.
"""

from kivy.event import EventDispatcher
from kivy.properties import ListProperty, StringProperty
from kivy.clock import Clock
from .colors import LightColorPalette, DarkColorPalette
from .typography import Typography


class DynamicColor(EventDispatcher):
    """
    A dynamic color that automatically updates when the theme changes.
    
    Usage:
        surface_color = DynamicColor("SURFACE")
        widget.background_color = surface_color.rgba
        
        # Color will automatically update when theme changes
    """
    
    rgba = ListProperty([1, 1, 1, 1])
    
    def __init__(self, color_name, **kwargs):
        super().__init__(**kwargs)
        self.color_name = color_name
        self._theme_manager = None
        self._update_color()
        
        # Register with theme manager when it becomes available
        Clock.schedule_once(self._register_with_theme_manager, 0)
    
    def _register_with_theme_manager(self, dt):
        """Register this color with the theme manager"""
        global theme_manager
        if theme_manager:
            self._theme_manager = theme_manager
            theme_manager.bind(on_theme_change=self._on_theme_change)
            self._update_color()
    
    def _on_theme_change(self, theme_manager, theme_name):
        """Called when theme changes"""
        self._update_color()
    
    def _update_color(self):
        """Update the color based on current theme"""
        if self._theme_manager:
            color = getattr(self._theme_manager.colors, self.color_name, [1, 1, 1, 1])
            self.rgba = color[:]
        else:
            # Default to light theme if no theme manager
            color = getattr(LightColorPalette, self.color_name, [1, 1, 1, 1])
            self.rgba = color[:]


class ThemeManager(EventDispatcher):
    """
    Central theme management system that handles dynamic color updates.
    
    Usage:
        theme_manager.current_theme = "dark"  # Switch to dark theme
        color = theme_manager.get_dynamic_color("SURFACE")
    """
    
    __events__ = ('on_theme_change',)
    
    current_theme = StringProperty("light")
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._themes = {
            "light": {
                "colors": LightColorPalette,
                "typography": Typography,
                "name": "Light Theme"
            },
            "dark": {
                "colors": DarkColorPalette,
                "typography": Typography,
                "name": "Dark Theme"
            }
        }
        self._dynamic_colors = {}
        self.bind(current_theme=self._on_current_theme_change)
    
    @property
    def colors(self):
        """Get current theme's color palette"""
        return self._themes[self.current_theme]["colors"]
    
    @property
    def typography(self):
        """Get current theme's typography"""
        return self._themes[self.current_theme]["typography"]
    
    def _on_current_theme_change(self, instance, theme_name):
        """Called when current_theme property changes"""
        self.dispatch('on_theme_change', theme_name)
    
    def on_theme_change(self, theme_name):
        """Event fired when theme changes"""
        pass
    
    def register_theme(self, name, color_palette_class, typography_class, display_name):
        """Register a new theme"""
        self._themes[name] = {
            "colors": color_palette_class,
            "typography": typography_class,
            "name": display_name
        }
    
    def get_dynamic_color(self, color_name):
        """
        Get a dynamic color that automatically updates with theme changes.
        
        Args:
            color_name: Name of the color from the palette (e.g., "SURFACE", "PRIMARY")
            
        Returns:
            DynamicColor instance
        """
        if color_name not in self._dynamic_colors:
            self._dynamic_colors[color_name] = DynamicColor(color_name)
        return self._dynamic_colors[color_name]
    
    def get_color(self, color_name):
        """
        Get a static color from the current theme.
        
        Args:
            color_name: Name of the color from the palette
            
        Returns:
            Color as [r, g, b, a] list
        """
        return getattr(self.colors, color_name, [1, 1, 1, 1])
    
    def get_available_themes(self):
        """Get list of available theme names"""
        return list(self._themes.keys())
    
    def get_theme_display_name(self, theme_name):
        """Get display name for a theme"""
        return self._themes.get(theme_name, {}).get("name", theme_name)


# Global theme manager instance
theme_manager = ThemeManager()


# Convenience functions for creating dynamic colors
def surface_color():
    """Get dynamic surface color"""
    return theme_manager.get_dynamic_color("SURFACE")

def primary_color():
    """Get dynamic primary color"""
    return theme_manager.get_dynamic_color("PRIMARY")

def secondary_color():
    """Get dynamic secondary color"""
    return theme_manager.get_dynamic_color("SECONDARY")

def background_color():
    """Get dynamic background color"""
    return theme_manager.get_dynamic_color("BACKGROUND")

def on_surface_color():
    """Get dynamic text color for surface"""
    return theme_manager.get_dynamic_color("ON_SURFACE")

def on_primary_color():
    """Get dynamic text color for primary"""
    return theme_manager.get_dynamic_color("ON_PRIMARY")

def on_secondary_color():
    """Get dynamic text color for secondary"""
    return theme_manager.get_dynamic_color("ON_SECONDARY")

def error_color():
    """Get dynamic error color"""
    return theme_manager.get_dynamic_color("ERROR")

def success_color():
    """Get dynamic success color"""
    return theme_manager.get_dynamic_color("SUCCESS")

def warning_color():
    """Get dynamic warning color"""
    return theme_manager.get_dynamic_color("WARNING")

def info_color():
    """Get dynamic info color"""
    return theme_manager.get_dynamic_color("INFO")