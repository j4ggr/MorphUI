
from kivy.uix.widget import Widget
from kivy.properties import StringProperty
from kivy.uix.textinput import TextInput


from .behaviors import MorphIdentificationBehavior
from .behaviors import MorphThemeBehavior
from .behaviors import MorphTextLayerBehavior
from .behaviors import MorphKeyPressBehavior

from .button import MorphIconButton

from .label import MorphSimpleLabel
from .label import MorphSimpleIconLabel


__all__ = [
    'MorphTextField',]

class MorphTextField(
        MorphIdentificationBehavior,
        MorphThemeBehavior,
        MorphTextLayerBehavior,
        MorphKeyPressBehavior,
        Widget,):
    """A text input field with MorphUI theming and key press handling.
    """

    leading_icon: str = StringProperty('')
    """Icon name for the leading icon in the text field."""

    trailing_icon: str = StringProperty('')
    """Icon name for the trailing icon in the text field."""

    leading_icon_label: MorphSimpleIconLabel

    trailing_icon_button: MorphSimpleIconLabel

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