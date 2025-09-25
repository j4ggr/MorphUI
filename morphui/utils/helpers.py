"""
Helper utilities for MorphUI components
"""

try:
    from kivy.metrics import dp as kivy_dp, sp as kivy_sp
    from kivy.core.window import Window
    KIVY_AVAILABLE = True
except ImportError:
    KIVY_AVAILABLE = False


def dp(value):
    """Convert density-independent pixels"""
    if KIVY_AVAILABLE:
        return kivy_dp(value)
    return value  # Fallback when Kivy not available


def sp(value):
    """Convert scale-independent pixels"""  
    if KIVY_AVAILABLE:
        return kivy_sp(value)
    return value  # Fallback when Kivy not available


def get_window_size():
    """Get current window dimensions"""
    if KIVY_AVAILABLE:
        return Window.size
    return (800, 600)  # Default fallback size


def get_window_width():
    """Get current window width"""
    if KIVY_AVAILABLE:
        return Window.width
    return 800  # Default fallback


def get_window_height():
    """Get current window height"""
    if KIVY_AVAILABLE:
        return Window.height
    return 600  # Default fallback


def clamp(value, min_value, max_value):
    """Clamp a value between min and max"""
    return max(min_value, min(value, max_value))


def lerp(start, end, factor):
    """Linear interpolation between two values"""
    return start + (end - start) * factor


def calculate_text_size(text, font_size=16, font_name=None):
    """Calculate the size needed to render text"""
    if not KIVY_AVAILABLE:
        # Approximate text size calculation when Kivy is not available
        char_width = font_size * 0.6  # Rough approximation
        char_height = font_size * 1.2
        return (len(text) * char_width, char_height)
    
    from kivy.core.text import Label as CoreLabel
    
    label = CoreLabel(text=text, font_size=font_size)
    if font_name:
        label.options['font_name'] = font_name
    
    label.refresh()
    return label.content_size


def is_dark_color(color):
    """Check if a color is considered 'dark' based on luminance"""
    if len(color) >= 3:
        # Calculate relative luminance
        r, g, b = color[0], color[1], color[2]
        luminance = 0.299 * r + 0.587 * g + 0.114 * b
        return luminance < 0.5
    return False


def get_contrasting_color(color):
    """Get a contrasting color (black or white) for the given color"""
    if is_dark_color(color):
        return [1.0, 1.0, 1.0, 1.0]  # White
    else:
        return [0.0, 0.0, 0.0, 1.0]  # Black


def blend_colors(color1, color2, factor=0.5):
    """Blend two colors together"""
    if len(color1) >= 3 and len(color2) >= 3:
        r = lerp(color1[0], color2[0], factor)
        g = lerp(color1[1], color2[1], factor)
        b = lerp(color1[2], color2[2], factor)
        a = lerp(color1[3] if len(color1) > 3 else 1.0, 
                color2[3] if len(color2) > 3 else 1.0, factor)
        return [r, g, b, a]
    return color1


def adjust_color_brightness(color, factor=1.2):
    """Adjust the brightness of a color"""
    if len(color) >= 3:
        r = clamp(color[0] * factor, 0.0, 1.0)
        g = clamp(color[1] * factor, 0.0, 1.0)
        b = clamp(color[2] * factor, 0.0, 1.0)
        a = color[3] if len(color) > 3 else 1.0
        return [r, g, b, a]
    return color