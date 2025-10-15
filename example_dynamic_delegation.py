"""
Example showing the dynamic delegation approach for MorphTextField.
This is much cleaner and more flexible than the previous static approach.
"""

from kivy.uix.textinput import TextInput
from morphui.uix.textfield import MorphTextField
from morphui.uix.behaviors import MorphTextLayerBehavior


class InnerTextWidget(MorphTextLayerBehavior, TextInput):
    """Inner text widget that inherits from MorphTextLayerBehavior."""
    pass


# Usage example - much simpler!
if __name__ == "__main__":
    from kivy.app import App
    from kivy.uix.boxlayout import BoxLayout
    
    class TestApp(App):
        def build(self):
            layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
            
            # Create text field
            text_field = MorphTextField(padding=20)
            text_field.size_hint_y = None
            text_field.height = 50
            
            # Create and set inner widget
            inner_widget = InnerTextWidget()
            text_field.text_widget = inner_widget  # This triggers delegation
            text_field.add_widget(inner_widget)
            
            # Now you can use any MorphTextLayerBehavior property directly!
            # No need for property descriptors or manual delegation
            text_field.surface_color = [0.95, 0.95, 0.95, 1]
            text_field.border_color = [0.2, 0.4, 0.8, 1]
            text_field.border_width = 2
            text_field.radius = [12, 12, 12, 12]
            
            # Methods work too
            text_field.refresh_surface()
            
            # You can even set properties before the inner widget exists
            text_field2 = MorphTextField()
            text_field2.surface_color = [1, 0.9, 0.9, 1]  # Stored as pending
            text_field2.text_widget = InnerTextWidget()   # Properties applied automatically
            
            layout.add_widget(text_field)
            layout.add_widget(text_field2)
            
            return layout
    
    TestApp().run()