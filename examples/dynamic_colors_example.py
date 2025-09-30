"""
Example demonstrating dynamic colors in Kivy with MorphUI theme system.

This example shows how to create widgets that automatically update their colors
when switching between light and dark themes.
"""

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.scrollview import ScrollView
from kivy.graphics import Color, Rectangle
from kivy.metrics import dp

# Import MorphUI theme system
from morphui.theme.styles import theme_manager


class DynamicWidget(Widget):
    """
    A widget that demonstrates dynamic background colors.
    The background will automatically change when the theme switches.
    """
    
    def __init__(self, color_name="SURFACE", **kwargs):
        super().__init__(**kwargs)
        
        # Get dynamic color
        self.dynamic_color = theme_manager.get_dynamic_color(color_name)
        
        # Set up graphics
        with self.canvas.before:
            self.bg_color = Color(rgba=self.dynamic_color.rgba)
            self.bg_rect = Rectangle(pos=self.pos, size=self.size)
        
        # Bind to updates
        self.dynamic_color.bind(rgba=self._update_color)
        self.bind(pos=self._update_rect, size=self._update_rect)
    
    def _update_color(self, instance, rgba):
        """Update background color when dynamic color changes"""
        self.bg_color.rgba = rgba
    
    def _update_rect(self, *args):
        """Update rectangle position and size"""
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size


class DynamicButton(Button):
    """
    A button that uses dynamic colors for background and text.
    """
    
    def __init__(self, bg_color_name="PRIMARY", text_color_name="ON_PRIMARY", **kwargs):
        super().__init__(**kwargs)
        
        # Get dynamic colors
        self.bg_dynamic_color = theme_manager.get_dynamic_color(bg_color_name)
        self.text_dynamic_color = theme_manager.get_dynamic_color(text_color_name)
        
        # Set initial colors
        self.background_color = self.bg_dynamic_color.rgba
        self.color = self.text_dynamic_color.rgba
        
        # Bind to updates
        self.bg_dynamic_color.bind(rgba=self._update_bg_color)
        self.text_dynamic_color.bind(rgba=self._update_text_color)
    
    def _update_bg_color(self, instance, rgba):
        """Update background color"""
        self.background_color = rgba
    
    def _update_text_color(self, instance, rgba):
        """Update text color"""
        self.color = rgba


class DynamicLabel(Label):
    """
    A label that uses dynamic colors for text.
    """
    
    def __init__(self, text_color_name="ON_SURFACE", **kwargs):
        super().__init__(**kwargs)
        
        # Get dynamic color
        self.text_dynamic_color = theme_manager.get_dynamic_color(text_color_name)
        
        # Set initial color
        self.color = self.text_dynamic_color.rgba
        
        # Bind to updates
        self.text_dynamic_color.bind(rgba=self._update_color)
    
    def _update_color(self, instance, rgba):
        """Update text color"""
        self.color = rgba


class DynamicColorExampleApp(App):
    """
    Example app demonstrating dynamic colors in action.
    """
    
    def build(self):
        # Main layout with dynamic background
        main_layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(10))
        
        # Add background widget
        with main_layout.canvas.before:
            bg_color = Color(rgba=theme_manager.get_dynamic_color("BACKGROUND").rgba)
            bg_rect = Rectangle(pos=main_layout.pos, size=main_layout.size)
        
        # Update background when theme changes
        def update_bg_color(instance, rgba):
            bg_color.rgba = rgba
        
        def update_bg_rect(instance, value):
            bg_rect.pos = main_layout.pos
            bg_rect.size = main_layout.size
            
        theme_manager.get_dynamic_color("BACKGROUND").bind(rgba=update_bg_color)
        main_layout.bind(pos=update_bg_rect, size=update_bg_rect)
        
        # Title
        title = DynamicLabel(
            text="Dynamic Colors Example",
            font_size=dp(24),
            text_color_name="ON_BACKGROUND",
            size_hint_y=None,
            height=dp(40)
        )
        main_layout.add_widget(title)
        
        # Instruction label
        instruction = DynamicLabel(
            text="Click the theme toggle button to see colors change automatically!",
            text_color_name="ON_BACKGROUND",
            size_hint_y=None,
            height=dp(30)
        )
        main_layout.add_widget(instruction)
        
        # Create scroll view for content
        scroll = ScrollView()
        content = BoxLayout(orientation='vertical', spacing=dp(10), size_hint_y=None)
        content.bind(minimum_height=content.setter('height'))
        
        # Surface card
        surface_card = DynamicWidget(
            color_name="SURFACE",
            size_hint_y=None,
            height=dp(120)
        )
        
        card_layout = BoxLayout(orientation='vertical', padding=dp(15), spacing=dp(5))
        
        card_title = DynamicLabel(
            text="Surface Card",
            font_size=dp(18),
            text_color_name="ON_SURFACE",
            size_hint_y=None,
            height=dp(25)
        )
        card_layout.add_widget(card_title)
        
        card_text = DynamicLabel(
            text="This card uses surface colors that adapt to the theme.",
            text_color_name="ON_SURFACE",
            size_hint_y=None,
            height=dp(40)
        )
        card_layout.add_widget(card_text)
        
        surface_card.add_widget(card_layout)
        content.add_widget(surface_card)
        
        # Button examples
        button_layout = BoxLayout(orientation='horizontal', spacing=dp(10), size_hint_y=None, height=dp(50))
        
        primary_btn = DynamicButton(
            text="Primary",
            bg_color_name="PRIMARY",
            text_color_name="ON_PRIMARY"
        )
        button_layout.add_widget(primary_btn)
        
        secondary_btn = DynamicButton(
            text="Secondary", 
            bg_color_name="SECONDARY",
            text_color_name="ON_SECONDARY"
        )
        button_layout.add_widget(secondary_btn)
        
        error_btn = DynamicButton(
            text="Error",
            bg_color_name="ERROR",
            text_color_name="ON_ERROR"
        )
        button_layout.add_widget(error_btn)
        
        content.add_widget(button_layout)
        
        # Color showcase
        showcase_layout = BoxLayout(orientation='horizontal', spacing=dp(5), size_hint_y=None, height=dp(100))
        
        color_names = ["PRIMARY", "SECONDARY", "SUCCESS", "WARNING", "ERROR", "INFO"]
        for color_name in color_names:
            color_widget = DynamicWidget(
                color_name=color_name,
                size_hint_x=1.0/len(color_names)
            )
            
            color_label = DynamicLabel(
                text=color_name,
                font_size=dp(10),
                text_color_name=f"ON_{color_name}" if hasattr(theme_manager.colors, f"ON_{color_name}") else "ON_SURFACE",
                halign="center",
                valign="middle"
            )
            color_label.bind(size=color_label.setter('text_size'))
            
            color_widget.add_widget(color_label)
            showcase_layout.add_widget(color_widget)
        
        content.add_widget(showcase_layout)
        
        # Theme toggle button
        theme_btn = DynamicButton(
            text=f"Switch to {'Dark' if theme_manager.current_theme == 'light' else 'Light'} Theme",
            bg_color_name="SURFACE_VARIANT",
            text_color_name="ON_SURFACE",
            size_hint_y=None,
            height=dp(50)
        )
        
        def toggle_theme(instance):
            if theme_manager.current_theme == "light":
                theme_manager.current_theme = "dark"
                instance.text = "Switch to Light Theme"
            else:
                theme_manager.current_theme = "light"  
                instance.text = "Switch to Dark Theme"
        
        theme_btn.bind(on_press=toggle_theme)
        content.add_widget(theme_btn)
        
        scroll.add_widget(content)
        main_layout.add_widget(scroll)
        
        return main_layout


if __name__ == "__main__":
    DynamicColorExampleApp().run()