"""
Utility modules for MorphUI
"""

try:
    from .animations import *
    from .helpers import *
    __all__ = ["create_fade_animation", "create_slide_animation", "dp", "sp", "get_window_size"]
except ImportError:
    # Kivy not available - import only non-Kivy utilities
    from .helpers import clamp, lerp, is_dark_color, get_contrasting_color, blend_colors, adjust_color_brightness
    __all__ = ["clamp", "lerp", "is_dark_color", "get_contrasting_color", "blend_colors", "adjust_color_brightness"]