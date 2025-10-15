
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty
from kivy.properties import ObjectProperty


from .behaviors import MorphIdentificationBehavior
from .behaviors import MorphThemeBehavior
from .behaviors import MorphKeyPressBehavior

from .label import MorphSimpleIconLabel


__all__ = [
    'MorphTextField',]



class MorphTextField(
        MorphIdentificationBehavior,
        MorphThemeBehavior,
        MorphKeyPressBehavior,
        BoxLayout,):
    """A text input field with MorphUI theming and key press handling.
    
    This class dynamically delegates properties and methods from 
    MorphTextLayerBehavior to an inner widget using magic methods.
    
    Usage
    -----
    ```python
    # Create a text field
    text_field = MorphTextField()
    
    # Set an inner widget that has MorphTextLayerBehavior
    text_field.text_widget = InnerTextWidget()
    
    # Now use any MorphTextLayerBehavior properties directly
    text_field.surface_color = [0.9, 0.9, 0.9, 1]
    text_field.border_color = [0.5, 0.5, 0.5, 1]
    text_field.refresh_surface()  # Methods work too
    ```
    """

    leading_icon: str = StringProperty('')
    """Icon name for the leading icon in the text field."""

    trailing_icon: str = StringProperty('')
    """Icon name for the trailing icon in the text field."""

    text_widget = ObjectProperty(None)
    """The inner text widget that has MorphTextLayerBehavior."""

    leading_icon_label: MorphSimpleIconLabel
    trailing_icon_button: MorphSimpleIconLabel

    # Properties that should be delegated to the inner widget
    _delegated_properties = {
        # Surface layer properties
        'surface_color', 'disabled_surface_color', 'error_surface_color',
        'focus_surface_color', 'active_surface_color', 'selected_surface_color',
        'border_color', 'disabled_border_color', 'error_border_color',
        'focus_border_color', 'active_border_color', 'selected_border_color',
        'border_width', 'border_open_length', 'border_bottom_line_only',
        'radius',
        # Content layer properties
        'content_color', 'disabled_content_color', 'error_content_color',
        'hovered_content_color', 'active_content_color', 'selected_content_color',
        # State properties
        'current_surface_state', 'current_content_state',
    }

    # Methods that should be delegated to the inner widget
    _delegated_methods = {
        'get_resolved_surface_colors', 'refresh_surface', 'apply_content',
        'refresh_content', 'calculate_border_path',
    }

    def __init__(self, **kwargs):
        # Store pending properties before super().__init__
        self._pending_properties = {}
        super().__init__(**kwargs)

    def __getattr__(self, name):
        """Dynamically delegate attribute access to the inner text widget."""
        # Check if this is a property or method we should delegate
        if name in self._delegated_properties or name in self._delegated_methods:
            if self.text_widget and hasattr(self.text_widget, name):
                attr = getattr(self.text_widget, name)
                # If it's a method, return it directly
                if callable(attr):
                    return attr
                # If it's a property, return the value
                return attr
            
            # If no inner widget, check pending properties
            if name in self._pending_properties:
                return self._pending_properties[name]
                
        # If not found, raise AttributeError as normal
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")

    def __setattr__(self, name, value):
        """Dynamically delegate attribute setting to the inner text widget."""
        # Check if this is a property we should delegate
        if hasattr(self, '_delegated_properties') and name in self._delegated_properties:
            if hasattr(self, 'text_widget') and self.text_widget and hasattr(self.text_widget, name):
                # Set on the inner widget
                setattr(self.text_widget, name, value)
                return
            
            # Store for later if no inner widget yet
            if not hasattr(self, '_pending_properties'):
                self._pending_properties = {}
            self._pending_properties[name] = value
            return
        
        # For all other attributes, use normal setting
        super().__setattr__(name, value)

    def on_text_widget(self, instance, widget):
        """Called when text_widget property changes."""
        if widget:
            # Apply any pending properties
            if hasattr(self, '_pending_properties'):
                for prop_name, value in self._pending_properties.items():
                    if hasattr(widget, prop_name):
                        setattr(widget, prop_name, value)
                # Clear pending properties
                self._pending_properties.clear()

    default_config = dict(
        multiline=False,
        radius=[2, 2, 2, 2],
        theme_color_bindings=dict(
            surface_color='surface_container_color',
            border_color='outline_color',
            error_border_color='error_color',
            focused_border_color='primary_color',
            disabled_border_color='outline_variant_color',
            content_color='content_surface_color',
            ),
        padding=[16, 16, 16, 16],)