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
from kivy.uix.label import Label
from kivy.uix.button import Button

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
class MorphTextInput(TextInput):

    _cursor_instruction: Color

    _cursor_color_instruction: Line

    cursor_path: List[float] = AliasProperty(
        lambda self: [
            *self.cursor_pos,
            self.cursor_pos[0],
            self.cursor_pos[1] - self.line_height],
        bind=['cursor_pos', 'line_height'],
        cache=True)
    
    # _cursor_blink: BooleanProperty = BooleanProperty(False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.canvas.before.clear()
        with self.canvas.before:
            self._cursor_instruction = Color(
                rgba=self.cursor_color,
                group=NAME_TEXTINPUT_CURSOR)
            self._cursor_color_instruction = SmoothLine(
                width=self.cursor_width,
                points=self.cursor_path)
        self.bind(
            _cursor_blink=self.update_cursor,
            cursor_path=self.update_cursor,
            cursor_color=self.update_cursor,
            cursor_width=self.update_cursor)

    def update_cursor(self, *args):
        color = self.cursor_color if self._cursor_blink else [0, 0, 0, 0]
        self._cursor_instruction.rgba = color
        self._cursor_color_instruction.points = self.cursor_path
        

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
        TextInput):
    """A text input field with enhanced features and MorphUI theming.

    This class extends Kivy's TextInput to provide a more feature-rich
    text field that integrates seamlessly with MorphUI's theming and
    behavior system. It includes support for labels, icons, and
    auto-sizing capabilities.

    Attributes
    ----------
    label_text : str
        The main label text displayed as a hint in the text field.
    supporting_text : str
        Additional supporting text displayed below the text field.
    leading_icon : str
        The name of the leading icon to display inside the text field.
    trailing_icon : str
        The name of the trailing icon to display inside the text field.
    label : TextFieldLabel
        The label widget instance for the main label.
    supporting_label : TextFieldSupportingLabel
        The label widget instance for the supporting text.
    leading_icon_label : TextFieldLeadingIconLabel
        The icon label widget instance for the leading icon.
    trailing_icon_button : TextFieldTrailingIconButton
        The icon button widget instance for the trailing icon.
    minimum_width : int
        The minimum width of the text field.
    minimum_height : int
        The minimum height of the text field.

    Examples
    --------
    ```python
    from morphui.app import MorphApp
    from morphui.uix.textfield import MorphTextField

    class MyApp(MorphApp):
        def build(self) -> MorphTextField:
            self.theme_manager.seed_color = 'Purple'
            return MorphTextField(
                label_text="Username",
                supporting_text="Enter your username",
                leading_icon='account',
                trailing_icon='close',)

    MyApp().run()
    ```
    """

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

    def __init__(self, **kwargs) -> None:
        self.label = Label(text='This is the label')
        self.supporting_label = Label(text='This is the supporting label')
        self.leading_icon_label = Label(text='icon')
        self.trailing_icon_button = Button(text='icon_button')
        super().__init__(**kwargs)
        for child in self.canvas.before.children:
            print(f'Canvas before child: {child}, group={child.group}')
        self.add_widget(self.label)
        self.add_widget(self.supporting_label)
        self.add_widget(self.leading_icon_label)
        self.add_widget(self.trailing_icon_button)

# class MorphTextField(
#         MorphDeclarativeBehavior,
#         MorphColorThemeBehavior,
#         MorphTextLayerBehavior,
#         MorphAutoSizingBehavior,
#         TextInput):

#     label_text: str = StringProperty('')

#     supporting_text: str = StringProperty('')

#     leading_icon: str = StringProperty('')

#     trailing_icon: str = StringProperty('')

#     label: TextFieldLabel = ObjectProperty()

#     supporting_label: TextFieldSupportingLabel = ObjectProperty()

#     leading_icon_label: TextFieldLeadingIconLabel = ObjectProperty()

#     trailing_icon_button: TextFieldTrailingIconButton = ObjectProperty()

#     minimum_width: int = NumericProperty(dp(100))

#     minimum_height: int = NumericProperty(dp(40))

#     default_config = dict(
#         # multiline=True,
#         radius=[2, 2, 2, 2],
#         theme_color_bindings=dict(
#             surface_color='transparent_color',
#             border_color='outline_color',
#             error_border_color='error_color',
#             focused_border_color='primary_color',
#             disabled_border_color='outline_variant_color',
#             content_color='content_surface_color',),
#         auto_height=True,
#         background_color=(0, 0, 0, 0),)
#     """Default configuration values for MorphTextField.

#     Provides standard text field appearance and behavior settings:
#     - Single-line input for concise data entry.
#     - Rounded corners for a modern look.
#     - Themed colors for consistency with the overall UI design.
#     """

#     def __init__(self, **kwargs) -> None:
#         config = clean_config(self.default_config, kwargs)
#         self.label = config.pop(
#             'label', TextFieldLabel())
#         self.supporting_label = config.pop(
#             'supporting_label', TextFieldSupportingLabel())
#         self.leading_icon_label = config.pop(
#             'leading_icon_label', TextFieldLeadingIconLabel())
#         self.trailing_icon_button = config.pop(
#             'trailing_icon_button', TextFieldTrailingIconButton())
#         super().__init__(**config)

#         self.bind(
#             declarative_children=self._adjust_label_positioning,
#             label_text=self.setter('hint_text'))
#         self.hint_text = self.label_text

#         self.fbind(
#             'label_text', self._update_content,
#             identity=NAME.TEXTFIELD_LABEL)
#         self.fbind(
#             'supporting_text', self._update_content,
#             identity=NAME.TEXTFIELD_SUPPORTING_LABEL)
#         self.fbind(
#             'leading_icon', self._update_content,
#             identity=NAME.TEXTFIELD_LEADING_ICON_LABEL)
#         self.fbind(
#             'trailing_icon', self._update_content,
#             identity=NAME.TEXTFIELD_TRAILING_ICON_BUTTON)
#         self.fbind(
#             'trailing_icon_button', self._update_content, 
#             identity=NAME.TEXTFIELD_TRAILING_ICON_BUTTON)
        
#         self.refresh_textfield_content()

#     def _update_content(self, instance: Any, text: str, identity: str) -> None:
#         match identity:
#             case NAME.TEXTFIELD_LABEL:
#                 widget = self.label
#                 is_icon = False
#             case NAME.TEXTFIELD_SUPPORTING_LABEL:
#                 widget = self.supporting_label
#                 is_icon = False
#             case NAME.TEXTFIELD_LEADING_ICON_LABEL:
#                 widget = self.leading_icon_label
#                 is_icon = True
#             case NAME.TEXTFIELD_TRAILING_ICON_BUTTON:
#                 widget = self.trailing_icon_button
#                 is_icon = True
#             case _:
#                 raise ValueError(
#                     f'Widget not found for identity: {identity!r}')

#         if is_icon:
#             widget.icon = text
#         else:
#             widget.text = text
        
#         if identity not in self.identities and text:
#             widget.identity = identity
#             self.add_widget(widget)
#             print(f'Added widget with identity: {identity}')
#         elif identity in self.identities and not text:
#             self.remove_widget(widget)
    
#     def _adjust_label_positioning(self, *args) -> None:
#         self.padding = [dp(16), dp(16), dp(16), dp(16)]

#         if NAME.TEXTFIELD_LEADING_ICON_LABEL in self.identities:
#             self.leading_icon_label.x = dp(12)
#             self.padding[0] = self.leading_icon_label.right + dp(16)

#         if NAME.TEXTFIELD_TRAILING_ICON_BUTTON in self.identities:
#             self.trailing_icon_button.right = self.width - dp(12)
#             self.padding[2] = self.width - self.trailing_icon_button.x + dp(16)

#         if NAME.TEXTFIELD_SUPPORTING_LABEL in self.identities:
#             self.supporting_label.y = (
#                 self.y - self.supporting_label.height - dp(4))

#     def _update_minimum_width(self, *args) -> None:
#         self.minimum_width = self._lines_labels

#     def refresh_textfield_content(self) -> None:
#         self._update_content(
#             self, self.label_text, NAME.TEXTFIELD_LABEL)
#         self._update_content(
#             self, self.supporting_text, NAME.TEXTFIELD_SUPPORTING_LABEL)
#         self._update_content(
#             self, self.leading_icon, NAME.TEXTFIELD_LEADING_ICON_LABEL)
#         self._update_content(
#             self, self.trailing_icon, NAME.TEXTFIELD_TRAILING_ICON_BUTTON)
#         self._adjust_label_positioning()

