from typing import Any
from typing import Dict
from typing import List

from kivy.metrics import dp
from kivy.metrics import sp
from kivy.properties import StringProperty
from kivy.properties import ObjectProperty
from kivy.properties import NumericProperty
from kivy.properties import BooleanProperty
from kivy.properties import VariableListProperty
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget

from ..utils import clean_config

from .behaviors import MorphThemeBehavior
from .behaviors import MorphTextLayerBehavior
from .behaviors import MorphColorThemeBehavior
from .behaviors import MorphAutoSizingBehavior
from .behaviors import MorphDeclarativeBehavior
from .behaviors import MorphIdentificationBehavior

from .label import MorphSimpleLabel
from .label import MorphSimpleIconLabel

from .button import MorphIconButton

from ..constants import NAME


__all__ = [
    'MorphTextField',]


class TextFieldLabel(MorphSimpleLabel):
    
    default_config: Dict[str, Any] = dict(
        halign='left',
        valign='middle',
        theme_color_bindings=dict(
            content_color='content_surface_color',),
        typography_role='Label',
        typography_size='medium',
        typography_weight='Regular',
        auto_width=True,)


class TextFieldSupportingLabel(MorphSimpleLabel):
    
    default_config: Dict[str, Any] = dict(
        halign='left',
        valign='middle',
        theme_color_bindings=dict(
            content_color='content_surface_color',),
        typography_role='Label',
        typography_size='small',
        typography_weight='Regular',
        auto_width=True,)


class TextFieldLeadingIconLabel(MorphSimpleIconLabel):
    
    default_config: Dict[str, Any] = dict(
        halign='center',
        valign='middle',
        theme_color_bindings=dict(
            content_color='content_surface_color',),
        font_size=sp(20),
        size_hint=(None, None),
        size=(dp(24), dp(24)),)


class TextFieldTrailingIconButton(MorphIconButton):
    
    default_config: Dict[str, Any] = dict(
        halign='center',
        valign='middle',
        theme_color_bindings=dict(
            content_color='primary_color',
            surface_color='primary_color',
            hovered_content_color='content_surface_variant_color',),
        font_size=sp(20),
        padding=5,
        round_sides=True,
        ripple_enabled=False,
        size_hint=(None, None),
        size=(dp(24), dp(24)),)


class MorphTextField(
        MorphDeclarativeBehavior,
        MorphColorThemeBehavior,
        MorphTextLayerBehavior,
        MorphAutoSizingBehavior,
        TextInput):

    label_text: str = StringProperty('')

    supporting_text: str = StringProperty('')

    leading_icon: str = StringProperty('')

    trailing_icon: str = StringProperty('')

    label: TextFieldLabel = ObjectProperty()

    supporting_label: TextFieldSupportingLabel = ObjectProperty()

    leading_icon_label: TextFieldLeadingIconLabel = ObjectProperty()

    trailing_icon_button: TextFieldTrailingIconButton = ObjectProperty()

    minimum_width: int = NumericProperty(dp(100))

    minimum_height: int = NumericProperty(dp(40))

    default_config = dict(
        # multiline=True,
        radius=[2, 2, 2, 2],
        theme_color_bindings=dict(
            surface_color='transparent_color',
            border_color='outline_color',
            error_border_color='error_color',
            focused_border_color='primary_color',
            disabled_border_color='outline_variant_color',
            content_color='content_surface_color',),
        auto_height=True,
        background_color=(0, 0, 0, 0),)
    """Default configuration values for MorphTextField.

    Provides standard text field appearance and behavior settings:
    - Single-line input for concise data entry.
    - Rounded corners for a modern look.
    - Themed colors for consistency with the overall UI design.
    """

    def __init__(self, **kwargs) -> None:
        config = clean_config(self.default_config, kwargs)
        self.label = config.pop(
            'label', TextFieldLabel())
        self.supporting_label = config.pop(
            'supporting_label', TextFieldSupportingLabel())
        self.leading_icon_label = config.pop(
            'leading_icon_label', TextFieldLeadingIconLabel())
        self.trailing_icon_button = config.pop(
            'trailing_icon_button', TextFieldTrailingIconButton())
        super().__init__(**config)

        self.bind(
            declarative_children=self._adjust_label_positioning,
            label_text=self.setter('hint_text'))
        self.hint_text = self.label_text

        self.fbind(
            'label_text', self._update_content,
            identity=NAME.TEXTFIELD_LABEL)
        self.fbind(
            'supporting_text', self._update_content,
            identity=NAME.TEXTFIELD_SUPPORTING_LABEL)
        self.fbind(
            'leading_icon', self._update_content,
            identity=NAME.TEXTFIELD_LEADING_ICON_LABEL)
        self.fbind(
            'trailing_icon', self._update_content,
            identity=NAME.TEXTFIELD_TRAILING_ICON_BUTTON)
        self.fbind(
            'trailing_icon_button', self._update_content, 
            identity=NAME.TEXTFIELD_TRAILING_ICON_BUTTON)
        
        self.refresh_textfield_content()

    def _update_content(self, instance: Any, text: str, identity: str) -> None:
        match identity:
            case NAME.TEXTFIELD_LABEL:
                widget = self.label
                is_icon = False
            case NAME.TEXTFIELD_SUPPORTING_LABEL:
                widget = self.supporting_label
                is_icon = False
            case NAME.TEXTFIELD_LEADING_ICON_LABEL:
                widget = self.leading_icon_label
                is_icon = True
            case NAME.TEXTFIELD_TRAILING_ICON_BUTTON:
                widget = self.trailing_icon_button
                is_icon = True
            case _:
                raise ValueError(
                    f'Widget not found for identity: {identity!r}')

        if is_icon:
            widget.icon = text
        else:
            widget.text = text
        
        if identity not in self.identities and text:
            widget.identity = identity
            self.add_widget(widget)
            print(f'Added widget with identity: {identity}')
        elif identity in self.identities and not text:
            self.remove_widget(widget)
    
    def _adjust_label_positioning(self, *args) -> None:
        self.padding = [dp(16), dp(16), dp(16), dp(16)]

        if NAME.TEXTFIELD_LEADING_ICON_LABEL in self.identities:
            self.leading_icon_label.x = dp(12)
            self.padding[0] = self.leading_icon_label.right + dp(16)

        if NAME.TEXTFIELD_TRAILING_ICON_BUTTON in self.identities:
            self.trailing_icon_button.right = self.width - dp(12)
            self.padding[2] = self.width - self.trailing_icon_button.x + dp(16)

        if NAME.TEXTFIELD_SUPPORTING_LABEL in self.identities:
            self.supporting_label.y = (
                self.y - self.supporting_label.height - dp(4))

    def _update_minimum_width(self, *args) -> None:
        self.minimum_width = self._lines_labels

    def refresh_textfield_content(self) -> None:
        self._update_content(
            self, self.label_text, NAME.TEXTFIELD_LABEL)
        self._update_content(
            self, self.supporting_text, NAME.TEXTFIELD_SUPPORTING_LABEL)
        self._update_content(
            self, self.leading_icon, NAME.TEXTFIELD_LEADING_ICON_LABEL)
        self._update_content(
            self, self.trailing_icon, NAME.TEXTFIELD_TRAILING_ICON_BUTTON)
        self._adjust_label_positioning()

