"""
Basic example demonstrating MorphUI components
"""

from kivy.app import App
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivy.metrics import dp

# Import MorphUI components
from morphui.uix.button import MorphButton
from morphui.uix.label import MorphLabel
from morphui.uix.card import MorphCard
from morphui.uix.textinput import MorphTextInput
from morphui.theme.styles import theme_manager


class MorphUIExampleApp(App):
    """Example app showcasing MorphUI components"""
    
    def build(self):
        # Create main scroll view
        scroll = ScrollView()
        
        # Main container
        main_layout = BoxLayout(
            orientation='vertical',
            spacing=dp(20),
            padding=[dp(20), dp(40)],
            size_hint_y=None
        )
        main_layout.bind(minimum_height=main_layout.setter('height'))
        
        # Title
        title = MorphLabel(
            text="MorphUI Components Demo",
            text_style="display",
            size_hint_y=None,
            height=dp(50)
        )
        main_layout.add_widget(title)
        
        # Subtitle
        subtitle = MorphLabel(
            text="A flexible Kivy UI extension",
            text_style="headline", 
            size_hint_y=None,
            height=dp(30)
        )
        main_layout.add_widget(subtitle)
        
        # Button examples card
        button_card = MorphCard(
            size_hint_y=None,
            height=dp(300)
        )
        
        button_layout = BoxLayout(
            orientation='vertical',
            spacing=dp(10)
        )
        
        button_layout.add_widget(MorphLabel(
            text="Buttons",
            text_style="title"
        ))
        
        # Different button styles
        filled_btn = MorphButton(
            text="Filled Button",
            button_style="filled",
            size_hint_y=None,
            height=dp(48)
        )
        button_layout.add_widget(filled_btn)
        
        outlined_btn = MorphButton(
            text="Outlined Button", 
            button_style="outlined",
            size_hint_y=None,
            height=dp(48)
        )
        button_layout.add_widget(outlined_btn)
        
        text_btn = MorphButton(
            text="Text Button",
            button_style="text", 
            size_hint_y=None,
            height=dp(48)
        )
        button_layout.add_widget(text_btn)
        
        button_card.add_widget(button_layout)
        main_layout.add_widget(button_card)
        
        # Text input examples card
        input_card = MorphCard(
            size_hint_y=None,
            height=dp(200)
        )
        
        input_layout = BoxLayout(
            orientation='vertical',
            spacing=dp(10)
        )
        
        input_layout.add_widget(MorphLabel(
            text="Text Inputs",
            text_style="title"
        ))
        
        text_input = MorphTextInput(
            hint_text="Enter your name",
            size_hint_y=None,
            height=dp(48),
            multiline=False
        )
        input_layout.add_widget(text_input)
        
        text_input_error = MorphTextInput(
            hint_text="This field has an error",
            size_hint_y=None,
            height=dp(48),
            multiline=False
        )
        text_input_error.set_error("This field is required")
        input_layout.add_widget(text_input_error)
        
        input_card.add_widget(input_layout)
        main_layout.add_widget(input_card)
        
        # Typography examples card
        typo_card = MorphCard(
            size_hint_y=None,
            height=dp(250)
        )
        
        typo_layout = BoxLayout(
            orientation='vertical',
            spacing=dp(5)
        )
        
        typo_layout.add_widget(MorphLabel(
            text="Typography Styles",
            text_style="title"
        ))
        
        # Different text styles
        for style in ["display", "headline", "title", "body", "label", "caption"]:
            typo_layout.add_widget(MorphLabel(
                text=f"This is {style} text",
                text_style=style,
                size_hint_y=None,
                height=dp(30) if style in ["body", "label", "caption"] else dp(40)
            ))
        
        typo_card.add_widget(typo_layout)
        main_layout.add_widget(typo_card)
        
        # Theme toggle card
        theme_card = MorphCard(
            size_hint_y=None,
            height=dp(120)
        )
        
        theme_layout = BoxLayout(
            orientation='vertical',
            spacing=dp(10)
        )
        
        theme_layout.add_widget(MorphLabel(
            text="Theme Toggle",
            text_style="title"
        ))
        
        theme_btn = MorphButton(
            text="Switch to Dark Theme",
            size_hint_y=None,
            height=dp(48)
        )
        theme_btn.bind(on_press=self.toggle_theme)
        theme_layout.add_widget(theme_btn)
        
        theme_card.add_widget(theme_layout)
        main_layout.add_widget(theme_card)
        
        scroll.add_widget(main_layout)
        return scroll
    
    def toggle_theme(self, instance):
        """Toggle between light and dark themes"""
        if theme_manager.current_theme == "light":
            theme_manager.current_theme = "dark"
            instance.text = "Switch to Light Theme"
        else:
            theme_manager.current_theme = "light"
            instance.text = "Switch to Dark Theme"


if __name__ == "__main__":
    MorphUIExampleApp().run()