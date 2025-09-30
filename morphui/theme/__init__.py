"""
MorphUI Theme System

This module provides comprehensive theming support including:
- Dynamic colors that automatically update when switching themes
- Light and dark theme palettes
- Typography system
- Theme management

Usage:
    from morphui.theme.styles import theme_manager, surface_color
    
    # Use dynamic colors in widgets
    widget.background_color = surface_color().rgba
    
    # Switch themes
    theme_manager.current_theme = "dark"
"""

from .colors import ColorPalette, LightColorPalette, DarkColorPalette
from .typography import Typography
from .styles import (
    ThemeManager, DynamicColor, theme_manager,
    surface_color, primary_color, secondary_color, background_color,
    on_surface_color, on_primary_color, on_secondary_color,
    error_color, success_color, warning_color, info_color
)

__all__ = [
    # Color palettes
    'ColorPalette', 'LightColorPalette', 'DarkColorPalette',
    
    # Typography
    'Typography',
    
    # Theme management
    'ThemeManager', 'DynamicColor', 'theme_manager',
    
    # Convenience functions for dynamic colors
    'surface_color', 'primary_color', 'secondary_color', 'background_color',
    'on_surface_color', 'on_primary_color', 'on_secondary_color',
    'error_color', 'success_color', 'warning_color', 'info_color'
]