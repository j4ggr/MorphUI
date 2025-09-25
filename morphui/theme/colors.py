"""
Color palette definitions for MorphUI themes
"""

class ColorPalette:
    """Base color palette for MorphUI themes"""
    
    # Primary colors
    PRIMARY = [0.2, 0.4, 0.8, 1.0]  # Blue
    PRIMARY_LIGHT = [0.4, 0.6, 0.9, 1.0]
    PRIMARY_DARK = [0.1, 0.2, 0.6, 1.0]
    
    # Secondary colors
    SECONDARY = [0.8, 0.4, 0.2, 1.0]  # Orange
    SECONDARY_LIGHT = [0.9, 0.6, 0.4, 1.0]
    SECONDARY_DARK = [0.6, 0.2, 0.1, 1.0]
    
    # Neutral colors
    WHITE = [1.0, 1.0, 1.0, 1.0]
    BLACK = [0.0, 0.0, 0.0, 1.0]
    GRAY_100 = [0.96, 0.96, 0.96, 1.0]
    GRAY_200 = [0.9, 0.9, 0.9, 1.0]
    GRAY_300 = [0.8, 0.8, 0.8, 1.0]
    GRAY_400 = [0.6, 0.6, 0.6, 1.0]
    GRAY_500 = [0.5, 0.5, 0.5, 1.0]
    GRAY_600 = [0.4, 0.4, 0.4, 1.0]
    GRAY_700 = [0.3, 0.3, 0.3, 1.0]
    GRAY_800 = [0.2, 0.2, 0.2, 1.0]
    GRAY_900 = [0.1, 0.1, 0.1, 1.0]
    
    # Status colors
    SUCCESS = [0.2, 0.8, 0.4, 1.0]  # Green
    WARNING = [1.0, 0.8, 0.0, 1.0]  # Yellow
    ERROR = [0.9, 0.2, 0.2, 1.0]    # Red
    INFO = [0.3, 0.7, 1.0, 1.0]     # Light blue
    
    # Background colors
    BACKGROUND = [0.98, 0.98, 0.98, 1.0]
    SURFACE = [1.0, 1.0, 1.0, 1.0]
    SURFACE_VARIANT = [0.95, 0.95, 0.95, 1.0]
    
    @classmethod
    def get_rgba(cls, color_name):
        """Get RGBA values for a color name"""
        return getattr(cls, color_name.upper(), cls.PRIMARY)
    
    @classmethod
    def hex_to_rgba(cls, hex_color, alpha=1.0):
        """Convert hex color to RGBA format"""
        if hex_color.startswith('#'):
            hex_color = hex_color[1:]
        
        if len(hex_color) == 3:
            hex_color = ''.join([c*2 for c in hex_color])
        
        r = int(hex_color[0:2], 16) / 255.0
        g = int(hex_color[2:4], 16) / 255.0
        b = int(hex_color[4:6], 16) / 255.0
        
        return [r, g, b, alpha]


class DarkColorPalette(ColorPalette):
    """Dark theme color palette"""
    
    # Override background colors for dark theme
    BACKGROUND = [0.1, 0.1, 0.1, 1.0]
    SURFACE = [0.15, 0.15, 0.15, 1.0]
    SURFACE_VARIANT = [0.2, 0.2, 0.2, 1.0]
    
    # Adjust primary colors for better contrast
    PRIMARY = [0.4, 0.6, 1.0, 1.0]  # Lighter blue
    SECONDARY = [1.0, 0.6, 0.4, 1.0]  # Lighter orange