"""
Enhanced label component for MorphUI
"""

from kivy.uix.label import Label
from kivy.properties import ListProperty, StringProperty, NumericProperty
from kivy.metrics import sp

from ..theme.styles import theme_manager


class MorphLabel(Label):
    """
    An enhanced label widget that extends Kivy's Label
    
    Features:
    - Integration with MorphUI theme system
    - Predefined text styles (display, headline, title, body, etc.)
    - Customizable colors
    - Better typography control
    """
    
    # Custom properties
    text_color = ListProperty([0.0, 0.0, 0.0, 1.0])
    text_style = StringProperty("body")  # display, headline, title, body, label, caption
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Apply theme and style
        self._apply_theme_style()
        
        # Bind properties
        self.bind(text_style=self._on_text_style_change)
    
    def _apply_theme_style(self):
        """Apply typography and color from theme"""
        typography = theme_manager.typography
        colors = theme_manager.colors
        
        # Get style configuration
        style_config = typography.get_text_style(self.text_style)
        
        # Apply font size
        self.font_size = sp(style_config.get('font_size', 16))
        
        # Apply colors (use theme's text color if not explicitly set)
        if not hasattr(self, '_custom_color_set'):
            self.text_color = colors.GRAY_800
            self.color = self.text_color
    
    def _on_text_style_change(self, instance, style):
        """Handle text style changes"""
        self._apply_theme_style()
    
    def on_text_color(self, instance, value):
        """Update label color when text_color changes"""
        self.color = value
        self._custom_color_set = True
    
    def set_style(self, style_name):
        """Change the text style"""
        self.text_style = style_name
    
    def make_bold(self):
        """Make text bold (requires custom font support)"""
        # Note: Kivy's default font doesn't support bold
        # This would work with custom fonts that have bold variants
        self.bold = True
    
    def make_italic(self):
        """Make text italic (requires custom font support)"""
        # Note: Kivy's default font doesn't support italic
        # This would work with custom fonts that have italic variants  
        self.italic = True