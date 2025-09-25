"""
Modern card component for MorphUI
"""

from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, RoundedRectangle
from kivy.properties import ListProperty, NumericProperty
from kivy.metrics import dp

from ..theme.styles import theme_manager


class MorphCard(BoxLayout):
    """
    A modern card widget that provides a container with styling
    
    Features:
    - Rounded corners with customizable radius
    - Elevation/shadow effect (simulated with darker background)
    - Customizable background color
    - Padding support
    - Integration with MorphUI theme system
    """
    
    # Custom properties
    background_color = ListProperty([1.0, 1.0, 1.0, 1.0])
    corner_radius = NumericProperty(dp(12))
    elevation = NumericProperty(2)
    card_padding = NumericProperty(dp(16))
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Apply theme colors
        self._apply_theme_colors()
        
        # Set default padding
        self.padding = [self.card_padding] * 4
        
        # Bind events
        self.bind(
            pos=self._update_graphics,
            size=self._update_graphics,
            background_color=self._update_graphics,
            corner_radius=self._update_graphics,
            elevation=self._update_graphics
        )
        
        # Initial graphics setup
        self._update_graphics()
    
    def _apply_theme_colors(self):
        """Apply colors from the current theme"""
        colors = theme_manager.colors
        self.background_color = colors.SURFACE
    
    def _update_graphics(self, *args):
        """Update the card's visual appearance"""
        self.canvas.before.clear()
        
        with self.canvas.before:
            # Shadow/elevation effect (simplified)
            if self.elevation > 0:
                shadow_offset = self.elevation
                shadow_color = [0, 0, 0, 0.1 + (self.elevation * 0.05)]
                
                Color(*shadow_color)
                RoundedRectangle(
                    pos=(self.x + shadow_offset, self.y - shadow_offset),
                    size=self.size,
                    radius=[self.corner_radius]
                )
            
            # Main card background
            Color(*self.background_color)
            RoundedRectangle(
                pos=self.pos,
                size=self.size,
                radius=[self.corner_radius]
            )
    
    def set_elevation(self, elevation):
        """Set the card's elevation"""
        self.elevation = elevation
    
    def on_card_padding(self, instance, value):
        """Update padding when card_padding changes"""
        self.padding = [value] * 4