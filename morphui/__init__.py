"""
MorphUI - A creative and flexible UI extension for Kivy

MorphUI provides modern and customizable UI components for Kivy applications,
offering greater design freedom compared to Material Design-bound libraries.
"""

__version__ = "0.1.0"
__author__ = "j4ggr"
__email__ = ""
__license__ = "MIT"

# Import core modules when available
try:
    from .uix import *
    from .theme import *
    from .utils import *
    UI_COMPONENTS_AVAILABLE = True
except ImportError:
    # Allow importing morphui even if Kivy dependencies aren't fully installed
    # Theme system should still work
    try:
        from .theme import *
        from .utils import clamp, lerp, is_dark_color, get_contrasting_color, blend_colors, adjust_color_brightness
        UI_COMPONENTS_AVAILABLE = False
    except ImportError:
        UI_COMPONENTS_AVAILABLE = False

__all__ = [
    "__version__",
    "__author__",
    "__email__",
    "__license__",
]