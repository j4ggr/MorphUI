"""
Color palette definitions for MorphUI themes
"""

class ColorPalette:
    """Base color palette class"""
    
    # Primary colors
    PRIMARY = [0.259, 0.522, 0.957, 1.0]  # Blue
    PRIMARY_VARIANT = [0.200, 0.408, 0.851, 1.0]  # Darker blue
    
    # Secondary colors
    SECONDARY = [0.020, 0.675, 0.455, 1.0]  # Teal
    SECONDARY_VARIANT = [0.016, 0.565, 0.380, 1.0]  # Darker teal
    
    # Surface colors
    SURFACE = [1.0, 1.0, 1.0, 1.0]  # White
    SURFACE_VARIANT = [0.949, 0.949, 0.949, 1.0]  # Light gray
    
    # Background colors
    BACKGROUND = [0.980, 0.980, 0.980, 1.0]  # Very light gray
    
    # Error colors
    ERROR = [0.722, 0.106, 0.106, 1.0]  # Red
    
    # Text colors
    ON_PRIMARY = [1.0, 1.0, 1.0, 1.0]  # White text on primary
    ON_SECONDARY = [1.0, 1.0, 1.0, 1.0]  # White text on secondary
    ON_SURFACE = [0.062, 0.062, 0.062, 1.0]  # Dark text on surface
    ON_BACKGROUND = [0.062, 0.062, 0.062, 1.0]  # Dark text on background
    ON_ERROR = [1.0, 1.0, 1.0, 1.0]  # White text on error
    
    # Additional semantic colors
    SUCCESS = [0.298, 0.686, 0.314, 1.0]  # Green
    WARNING = [1.0, 0.596, 0.0, 1.0]  # Orange
    INFO = [0.129, 0.588, 0.953, 1.0]  # Light blue
    
    # Text colors for semantic colors
    ON_SUCCESS = [1.0, 1.0, 1.0, 1.0]
    ON_WARNING = [0.0, 0.0, 0.0, 1.0]
    ON_INFO = [1.0, 1.0, 1.0, 1.0]


class LightColorPalette(ColorPalette):
    """Light theme color palette"""
    pass  # Uses base colors which are already light theme


class DarkColorPalette(ColorPalette):
    """Dark theme color palette"""
    
    # Primary colors (slightly adjusted for dark theme)
    PRIMARY = [0.386, 0.611, 0.973, 1.0]  # Lighter blue
    PRIMARY_VARIANT = [0.259, 0.522, 0.957, 1.0]  # Original blue
    
    # Secondary colors (slightly adjusted)
    SECONDARY = [0.263, 0.784, 0.616, 1.0]  # Lighter teal
    SECONDARY_VARIANT = [0.020, 0.675, 0.455, 1.0]  # Original teal
    
    # Surface colors
    SURFACE = [0.078, 0.078, 0.078, 1.0]  # Dark gray
    SURFACE_VARIANT = [0.141, 0.141, 0.141, 1.0]  # Lighter dark gray
    
    # Background colors
    BACKGROUND = [0.051, 0.051, 0.051, 1.0]  # Very dark gray
    
    # Error colors (slightly lighter for dark theme)
    ERROR = [0.937, 0.384, 0.384, 1.0]  # Lighter red
    
    # Text colors
    ON_PRIMARY = [0.0, 0.0, 0.0, 1.0]  # Black text on light primary
    ON_SECONDARY = [0.0, 0.0, 0.0, 1.0]  # Black text on light secondary
    ON_SURFACE = [0.875, 0.875, 0.875, 1.0]  # Light text on dark surface
    ON_BACKGROUND = [0.875, 0.875, 0.875, 1.0]  # Light text on dark background
    ON_ERROR = [0.0, 0.0, 0.0, 1.0]  # Black text on light error
    
    # Additional semantic colors (adjusted for dark theme)
    SUCCESS = [0.451, 0.824, 0.475, 1.0]  # Lighter green
    WARNING = [1.0, 0.714, 0.278, 1.0]  # Lighter orange
    INFO = [0.384, 0.702, 0.973, 1.0]  # Lighter blue
    
    # Text colors for semantic colors
    ON_SUCCESS = [0.0, 0.0, 0.0, 1.0]
    ON_WARNING = [0.0, 0.0, 0.0, 1.0]
    ON_INFO = [0.0, 0.0, 0.0, 1.0]