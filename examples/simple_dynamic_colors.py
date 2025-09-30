"""
Simple example demonstrating dynamic colors in Kivy with MorphUI theme system.

This example shows the basic concept of creating widgets that automatically 
update their colors when switching between light and dark themes.
"""

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.metrics import dp

# Import MorphUI theme system
from morphui.theme.styles import theme_manager


class SimpleButton(Button):
    """A button that demonstrates dynamic colors"""
    
    def __init__(self, bg_color_name="PRIMARY", text_color_name="ON_PRIMARY", **kwargs):
        super().__init__(**kwargs)
        
        # Get dynamic colors
        self.bg_dynamic_color = theme_manager.get_dynamic_color(bg_color_name)
        self.text_dynamic_color = theme_manager.get_dynamic_color(text_color_name)
        
        # Set initial colors
        self.background_color = self.bg_dynamic_color.rgba
        self.color = self.text_dynamic_color.rgba
        
        # Update colors when theme changes
        self.bg_dynamic_color.bind(rgba=self._update_bg_color)
        self.text_dynamic_color.bind(rgba=self._update_text_color)
    
    def _update_bg_color(self, instance, rgba):
        self.background_color = rgba
    
    def _update_text_color(self, instance, rgba):
        self.color = rgba


class SimpleLabel(Label):
    """A label that demonstrates dynamic text colors"""
    
    def __init__(self, text_color_name="ON_SURFACE", **kwargs):
        super().__init__(**kwargs)
        
        # Get dynamic color
        self.text_dynamic_color = theme_manager.get_dynamic_color(text_color_name)
        
        # Set initial color
        self.color = self.text_dynamic_color.rgba
        
        # Update color when theme changes
        self.text_dynamic_color.bind(rgba=self._update_color)
    
    def _update_color(self, instance, rgba):
        self.color = rgba


class DynamicColorApp(App):
    """
    Simple app demonstrating dynamic colors.
    """
    
    def build(self):
        # Main layout
        main_layout = BoxLayout(
            orientation='vertical', 
            padding=dp(20), 
            spacing=dp(20)
        )
        
        # Title
        title = SimpleLabel(
            text="Dynamic Colors Demo",
            font_size=dp(24),
            text_color_name="ON_BACKGROUND",
            size_hint_y=None,
            height=dp(40)
        )
        main_layout.add_widget(title)
        
        # Instructions
        instructions = SimpleLabel(
            text="Click 'Toggle Theme' to see colors change automatically!",
            text_color_name="ON_BACKGROUND",
            size_hint_y=None,
            height=dp(30)
        )
        main_layout.add_widget(instructions)
        
        # Button examples
        buttons_layout = BoxLayout(
            orientation='vertical',
            spacing=dp(10),
            size_hint_y=None,
            height=dp(200)
        )
        
        # Primary button
        primary_btn = SimpleButton(
            text="Primary Button",
            bg_color_name="PRIMARY",
            text_color_name="ON_PRIMARY",
            size_hint_y=None,
            height=dp(50)
        )
        buttons_layout.add_widget(primary_btn)
        
        # Secondary button
        secondary_btn = SimpleButton(
            text="Secondary Button",
            bg_color_name="SECONDARY", 
            text_color_name="ON_SECONDARY",
            size_hint_y=None,
            height=dp(50)
        )
        buttons_layout.add_widget(secondary_btn)
        
        # Error button
        error_btn = SimpleButton(
            text="Error Button",
            bg_color_name="ERROR",
            text_color_name="ON_ERROR",
            size_hint_y=None,
            height=dp(50)
        )
        buttons_layout.add_widget(error_btn)
        
        # Theme toggle button
        self.theme_btn = SimpleButton(
            text=f"Switch to {'Dark' if theme_manager.current_theme == 'light' else 'Light'} Theme",
            bg_color_name="SURFACE_VARIANT",
            text_color_name="ON_SURFACE",
            size_hint_y=None,
            height=dp(50)
        )
        self.theme_btn.bind(on_press=self.toggle_theme)
        buttons_layout.add_widget(self.theme_btn)
        
        main_layout.add_widget(buttons_layout)
        
        return main_layout
    
    def toggle_theme(self, instance):
        """Toggle between light and dark themes"""
        if theme_manager.current_theme == "light":
            theme_manager.current_theme = "dark"
            instance.text = "Switch to Light Theme"
        else:
            theme_manager.current_theme = "light"
            instance.text = "Switch to Dark Theme"


if __name__ == "__main__":
    DynamicColorApp().run()