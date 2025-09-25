"""
Modern text input component for MorphUI
"""

from kivy.uix.textinput import TextInput
from kivy.graphics import Color, RoundedRectangle, Line
from kivy.properties import ListProperty, NumericProperty, StringProperty, BooleanProperty
from kivy.metrics import dp, sp
from kivy.animation import Animation

from ..theme.styles import theme_manager


class MorphTextInput(TextInput):
    """
    A modern text input widget that extends Kivy's TextInput
    
    Features:
    - Modern styling with rounded corners
    - Focus states with color transitions
    - Floating label support
    - Error state indication
    - Integration with MorphUI theme system
    """
    
    # Custom properties
    background_color = ListProperty([1.0, 1.0, 1.0, 1.0])
    background_color_focus = ListProperty([1.0, 1.0, 1.0, 1.0])
    
    border_color = ListProperty([0.8, 0.8, 0.8, 1.0])
    border_color_focus = ListProperty([0.2, 0.4, 0.8, 1.0])
    border_color_error = ListProperty([0.9, 0.2, 0.2, 1.0])
    
    corner_radius = NumericProperty(dp(8))
    border_width = NumericProperty(dp(1))
    
    hint_text_color = ListProperty([0.6, 0.6, 0.6, 1.0])
    
    has_error = BooleanProperty(False)
    error_message = StringProperty("")
    
    floating_label = BooleanProperty(False)
    label_text = StringProperty("")
    
    def __init__(self, **kwargs):
        # Remove default background
        kwargs.setdefault('background_normal', '')
        kwargs.setdefault('background_active', '')
        
        super().__init__(**kwargs)
        
        # Apply theme colors
        self._apply_theme_colors()
        
        # Setup padding
        self.padding = [dp(12), dp(8)]
        
        # Bind events
        self.bind(
            pos=self._update_graphics,
            size=self._update_graphics,
            focus=self._on_focus_change,
            text=self._on_text_change
        )
        
        # Initial graphics setup
        self._update_graphics()
    
    def _apply_theme_colors(self):
        """Apply colors from the current theme"""
        colors = theme_manager.colors
        
        self.background_color = colors.SURFACE
        self.background_color_focus = colors.SURFACE
        self.border_color = colors.GRAY_300
        self.border_color_focus = colors.PRIMARY
        self.foreground_color = colors.GRAY_800
        self.hint_text_color = colors.GRAY_400
    
    def _update_graphics(self, *args):
        """Update the text input's visual appearance"""
        self.canvas.before.clear()
        
        with self.canvas.before:
            # Background
            if self.focus:
                Color(*self.background_color_focus)
            else:
                Color(*self.background_color)
            
            RoundedRectangle(
                pos=self.pos,
                size=self.size,
                radius=[self.corner_radius]
            )
            
            # Border
            if self.has_error:
                Color(*self.border_color_error)
            elif self.focus:
                Color(*self.border_color_focus)
            else:
                Color(*self.border_color)
            
            Line(
                rounded_rectangle=(
                    self.x, self.y, self.width, self.height,
                    self.corner_radius, self.corner_radius,
                    self.corner_radius, self.corner_radius
                ),
                width=self.border_width
            )
    
    def _on_focus_change(self, instance, focus):
        """Handle focus changes with animations"""
        if focus:
            # Focus animation
            Animation(
                border_color=self.border_color_focus,
                duration=0.2
            ).start(self)
        else:
            # Unfocus animation  
            if not self.has_error:
                Animation(
                    border_color=self.border_color,
                    duration=0.2
                ).start(self)
        
        self._update_graphics()
    
    def _on_text_change(self, instance, text):
        """Handle text changes"""
        # Clear error state when user starts typing
        if self.has_error and text:
            self.clear_error()
    
    def set_error(self, error_message=""):
        """Set the error state"""
        self.has_error = True
        self.error_message = error_message
        self._update_graphics()
    
    def clear_error(self):
        """Clear the error state"""
        self.has_error = False
        self.error_message = ""
        self._update_graphics()
    
    def on_background_color(self, instance, value):
        """Update graphics when background color changes"""
        self._update_graphics()
    
    def on_corner_radius(self, instance, value):
        """Update graphics when corner radius changes"""
        self._update_graphics()