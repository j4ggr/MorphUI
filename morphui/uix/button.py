"""
Modern button component for MorphUI
"""

from kivy.uix.button import Button
from kivy.graphics import Color, RoundedRectangle
from kivy.animation import Animation
from kivy.properties import ListProperty, NumericProperty, StringProperty, BooleanProperty
from kivy.metrics import dp

from ..theme.styles import theme_manager
from ..utils.animations import create_color_animation


class MorphButton(Button):
    """
    A modern, customizable button widget that extends Kivy's Button
    
    Features:
    - Customizable colors and styling
    - Rounded corners with adjustable radius
    - Smooth animations on press/release
    - Multiple button styles (filled, outlined, text)
    - Integration with MorphUI theme system
    """
    
    # Custom properties
    background_color = ListProperty([0.2, 0.4, 0.8, 1.0])
    background_color_pressed = ListProperty([0.1, 0.2, 0.6, 1.0])
    background_color_disabled = ListProperty([0.8, 0.8, 0.8, 1.0])
    
    text_color = ListProperty([1.0, 1.0, 1.0, 1.0])
    text_color_disabled = ListProperty([0.5, 0.5, 0.5, 1.0])
    
    border_width = NumericProperty(0)
    border_color = ListProperty([0.0, 0.0, 0.0, 1.0])
    
    corner_radius = NumericProperty(dp(8))
    
    button_style = StringProperty("filled")  # filled, outlined, text
    
    elevation = NumericProperty(0)
    ripple_effect = BooleanProperty(True)
    
    def __init__(self, **kwargs):
        # Remove default background
        kwargs.setdefault('background_normal', '')
        kwargs.setdefault('background_down', '')
        kwargs.setdefault('background_disabled_normal', '')
        
        super().__init__(**kwargs)
        
        # Apply theme colors if not explicitly set
        self._apply_theme_colors()
        
        # Bind events
        self.bind(
            pos=self._update_graphics,
            size=self._update_graphics,
            state=self._on_state_change
        )
        
        # Initial graphics setup
        self._update_graphics()
    
    def _apply_theme_colors(self):
        """Apply colors from the current theme"""
        colors = theme_manager.colors
        
        if self.button_style == "filled":
            self.background_color = colors.PRIMARY
            self.background_color_pressed = colors.PRIMARY_DARK
            self.text_color = colors.WHITE
        elif self.button_style == "outlined":
            self.background_color = [0, 0, 0, 0]  # Transparent
            self.background_color_pressed = colors.PRIMARY + [0.1]  # Semi-transparent
            self.border_width = dp(1)
            self.border_color = colors.PRIMARY
            self.text_color = colors.PRIMARY
        elif self.button_style == "text":
            self.background_color = [0, 0, 0, 0]  # Transparent
            self.background_color_pressed = colors.PRIMARY + [0.1]  # Semi-transparent
            self.text_color = colors.PRIMARY
    
    def _update_graphics(self, *args):
        """Update the button's visual appearance"""
        self.canvas.before.clear()
        
        with self.canvas.before:
            # Background color
            if self.state == 'normal':
                Color(*self.background_color)
            elif self.state == 'down':
                Color(*self.background_color_pressed)
            else:  # disabled
                Color(*self.background_color_disabled)
            
            # Main background
            RoundedRectangle(
                pos=self.pos,
                size=self.size,
                radius=[self.corner_radius]
            )
            
            # Border (if enabled)
            if self.border_width > 0:
                Color(*self.border_color)
                # Would need custom drawing for borders in Kivy
                # This is a simplified version
    
    def _on_state_change(self, instance, state):
        """Handle state changes with animations"""
        if state == 'down':
            # Button press animation
            if self.ripple_effect:
                Animation(
                    background_color=self.background_color_pressed,
                    duration=0.1
                ).start(self)
        else:
            # Button release animation
            if self.ripple_effect:
                Animation(
                    background_color=self.background_color,
                    duration=0.2
                ).start(self)
        
        # Update graphics
        self._update_graphics()
    
    def set_style(self, style):
        """Change the button style"""
        self.button_style = style
        self._apply_theme_colors()
        self._update_graphics()
    
    def on_background_color(self, instance, value):
        """Update graphics when background color changes"""
        self._update_graphics()
    
    def on_corner_radius(self, instance, value):
        """Update graphics when corner radius changes"""
        self._update_graphics()