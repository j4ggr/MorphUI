"""
Practical example of creating a themed card widget with dynamic colors.

This demonstrates how to create reusable widgets that automatically adapt
to theme changes in MorphUI.
"""

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.graphics import Color, RoundedRectangle
from kivy.metrics import dp

from morphui.theme.styles import theme_manager


class ThemedCard(Widget):
    """
    A card widget that automatically adapts to theme changes.
    Demonstrates dynamic colors with canvas instructions.
    """
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Get dynamic colors
        self.surface_color = theme_manager.get_dynamic_color("SURFACE")
        
        # Create card background
        with self.canvas.before:
            self.bg_color = Color(rgba=self.surface_color.rgba)
            self.bg_rect = RoundedRectangle(
                pos=self.pos, 
                size=self.size,
                radius=[dp(8), dp(8), dp(8), dp(8)]
            )
        
        # Bind to updates
        self.surface_color.bind(rgba=self._update_color)
        self.bind(pos=self._update_graphics, size=self._update_graphics)
    
    def _update_color(self, instance, rgba):
        """Update card background color"""
        self.bg_color.rgba = rgba
    
    def _update_graphics(self, *args):
        """Update card position and size"""
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size


class ThemedLabel(Label):
    """
    A label that automatically uses appropriate text colors for the theme.
    """
    
    def __init__(self, color_name="ON_SURFACE", **kwargs):
        super().__init__(**kwargs)
        
        # Get dynamic text color
        self.text_color = theme_manager.get_dynamic_color(color_name)
        
        # Set initial color
        self.color = self.text_color.rgba
        
        # Bind to updates
        self.text_color.bind(rgba=self._update_color)
    
    def _update_color(self, instance, rgba):
        """Update text color"""
        self.color = rgba


class ThemedButton(Button):
    """
    A button that automatically uses theme colors.
    """
    
    def __init__(self, button_type="primary", **kwargs):
        super().__init__(**kwargs)
        
        # Choose colors based on button type
        if button_type == "primary":
            bg_color_name = "PRIMARY"
            text_color_name = "ON_PRIMARY"
        elif button_type == "secondary":
            bg_color_name = "SECONDARY"
            text_color_name = "ON_SECONDARY"
        elif button_type == "surface":
            bg_color_name = "SURFACE_VARIANT"
            text_color_name = "ON_SURFACE"
        else:
            bg_color_name = "PRIMARY"
            text_color_name = "ON_PRIMARY"
        
        # Get dynamic colors
        self.bg_color = theme_manager.get_dynamic_color(bg_color_name)
        self.text_color = theme_manager.get_dynamic_color(text_color_name)
        
        # Set initial colors
        self.background_color = self.bg_color.rgba
        self.color = self.text_color.rgba
        
        # Bind to updates
        self.bg_color.bind(rgba=self._update_bg_color)
        self.text_color.bind(rgba=self._update_text_color)
    
    def _update_bg_color(self, instance, rgba):
        """Update background color"""
        self.background_color = rgba
    
    def _update_text_color(self, instance, rgba):
        """Update text color"""
        self.color = rgba


class ThemedCardApp(App):
    """
    App demonstrating themed widgets in practice.
    """
    
    def build(self):
        # Main container with themed background
        root = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(15))
        
        # Set background color that updates with theme
        self.bg_color = theme_manager.get_dynamic_color("BACKGROUND")
        with root.canvas.before:
            self.bg_color_instruction = Color(rgba=self.bg_color.rgba)
            self.bg_rect = RoundedRectangle(pos=root.pos, size=root.size)
        
        # Update background when theme or layout changes
        self.bg_color.bind(rgba=self._update_bg_color)
        root.bind(pos=self._update_bg_rect, size=self._update_bg_rect)
        
        # Title
        title = ThemedLabel(
            text="Themed Widgets Demo",
            font_size=dp(28),
            color_name="ON_BACKGROUND",
            size_hint_y=None,
            height=dp(40)
        )
        root.add_widget(title)
        
        # Card 1: User Profile
        profile_card = ThemedCard(size_hint_y=None, height=dp(120))
        profile_layout = BoxLayout(orientation='vertical', padding=dp(15), spacing=dp(5))
        
        profile_title = ThemedLabel(
            text="User Profile",
            font_size=dp(18),
            color_name="ON_SURFACE",
            size_hint_y=None,
            height=dp(25)
        )
        profile_layout.add_widget(profile_title)
        
        profile_text = ThemedLabel(
            text="John Doe\\nSoftware Developer",
            color_name="ON_SURFACE",
            size_hint_y=None,
            height=dp(40)
        )
        profile_layout.add_widget(profile_text)
        
        # Buttons in profile card
        button_layout = BoxLayout(orientation='horizontal', spacing=dp(10), size_hint_y=None, height=dp(35))
        
        edit_btn = ThemedButton(
            text="Edit",
            button_type="primary",
            size_hint_x=0.5
        )
        button_layout.add_widget(edit_btn)
        
        delete_btn = ThemedButton(
            text="Delete", 
            button_type="surface",
            size_hint_x=0.5
        )
        button_layout.add_widget(delete_btn)
        
        profile_layout.add_widget(button_layout)
        profile_card.add_widget(profile_layout)
        root.add_widget(profile_card)
        
        # Card 2: Settings
        settings_card = ThemedCard(size_hint_y=None, height=dp(100))
        settings_layout = BoxLayout(orientation='vertical', padding=dp(15), spacing=dp(5))
        
        settings_title = ThemedLabel(
            text="Settings",
            font_size=dp(18),
            color_name="ON_SURFACE",
            size_hint_y=None,
            height=dp(25)
        )
        settings_layout.add_widget(settings_title)
        
        settings_text = ThemedLabel(
            text="Configure your preferences and display options.",
            color_name="ON_SURFACE",
            size_hint_y=None,
            height=dp(40)
        )
        settings_layout.add_widget(settings_text)
        
        settings_card.add_widget(settings_layout)
        root.add_widget(settings_card)
        
        # Theme toggle section
        theme_card = ThemedCard(size_hint_y=None, height=dp(80))
        theme_layout = BoxLayout(orientation='horizontal', padding=dp(15), spacing=dp(10))
        
        theme_label = ThemedLabel(
            text="Current Theme:",
            color_name="ON_SURFACE"
        )
        theme_layout.add_widget(theme_label)
        
        self.theme_button = ThemedButton(
            text=f"{theme_manager.current_theme.title()} Theme",
            button_type="secondary",
            size_hint_x=None,
            width=dp(150)
        )
        self.theme_button.bind(on_press=self.toggle_theme)
        theme_layout.add_widget(self.theme_button)
        
        theme_card.add_widget(theme_layout)
        root.add_widget(theme_card)
        
        return root
    
    def _update_bg_color(self, instance, rgba):
        """Update background color when theme changes"""
        self.bg_color_instruction.rgba = rgba
    
    def _update_bg_rect(self, instance, value):
        """Update background rectangle"""
        self.bg_rect.pos = instance.pos
        self.bg_rect.size = instance.size
    
    def toggle_theme(self, instance):
        """Toggle between light and dark themes"""
        if theme_manager.current_theme == "light":
            theme_manager.current_theme = "dark"
        else:
            theme_manager.current_theme = "light"
        
        # Update button text
        instance.text = f"{theme_manager.current_theme.title()} Theme"


if __name__ == "__main__":
    ThemedCardApp().run()