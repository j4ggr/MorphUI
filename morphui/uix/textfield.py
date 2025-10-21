from typing import Any
from typing import Dict
from typing import List

from kivy.metrics import dp
from kivy.metrics import sp
from kivy.graphics import Line
from kivy.graphics import Color
from kivy.graphics import BoxShadow
from kivy.properties import AliasProperty
from kivy.properties import StringProperty
from kivy.properties import ObjectProperty
from kivy.properties import BooleanProperty
from kivy.properties import NumericProperty
from kivy.properties import VariableListProperty
from kivy.uix.textinput import TextInput


from ..utils import clamp
from ..utils import clean_config

from .behaviors import MorphThemeBehavior
from .behaviors import MorphTextLayerBehavior
from .behaviors import MorphAutoSizingBehavior
from .behaviors import MorphTypographyBehavior
from .behaviors import MorphContentLayerBehavior
from .behaviors import MorphIdentificationBehavior

from .floatlayout import MorphFloatLayout

from .label import MorphSimpleLabel
from .label import MorphSimpleIconLabel

from .button import MorphIconButton

from ..constants import NAME


__all__ = [
    'TextFieldLabel',
    'TextFieldSupportingLabel',
    'TextFieldLeadingIconLabel',
    'TextFieldTrailingIconButton',
    'MorphTextInput',
    'MorphTextField',]


class TextFieldLabel(MorphSimpleLabel):
    
    default_config: Dict[str, Any] = dict(
        theme_color_bindings=dict(
            content_color='content_surface_color',),
        typography_role='Label',
        typography_size='medium',
        typography_weight='Regular',
        halign='left',
        valign='middle',
        auto_width=True,)


class TextFieldSupportingLabel(MorphSimpleLabel):
    
    default_config: Dict[str, Any] = dict(
        theme_color_bindings=dict(
            content_color='content_surface_color',),
        typography_role='Label',
        typography_size='small',
        typography_weight='Regular',
        halign='left',
        valign='middle',
        auto_width=True,)


class TextFieldLeadingIconLabel(MorphSimpleIconLabel):
    
    default_config: Dict[str, Any] = dict(
        theme_color_bindings=dict(
            content_color='content_surface_color',),
        font_name=MorphSimpleIconLabel.default_config['font_name'],
        typography_role=MorphSimpleIconLabel.default_config['typography_role'],
        typography_size=MorphSimpleIconLabel.default_config['typography_size'],
        halign='center',
        valign='middle',
        size_hint=(None, None),
        size=(dp(24), dp(24)),
        padding=dp(0),)


class TextFieldTrailingIconButton(MorphIconButton):
    
    default_config: Dict[str, Any] = dict(
        theme_color_bindings=dict(
            content_color='primary_color',
            surface_color='transparent_color',
            hovered_content_color='content_surface_variant_color',),
        font_name=MorphIconButton.default_config['font_name'],
        typography_role=MorphIconButton.default_config['typography_role'],
        typography_size=MorphIconButton.default_config['typography_size'],
        halign='center',
        valign='middle',
        round_sides=True,
        ripple_enabled=False,
        size_hint=(None, None),
        size=(dp(24), dp(24)),
        padding=dp(0),)


class MorphTextInput(
        MorphIdentificationBehavior,
        MorphThemeBehavior,
        MorphTextLayerBehavior,
        MorphAutoSizingBehavior,
        TextInput):

    minimum_width: int = NumericProperty(dp(80))
    """The minimum width of the TextInput based on content.

    :attr:`minimum_width` is a :class:`~kivy.properties.NumericProperty`
    and defaults to dp(80).
    """

    def _get_min_height(self) -> Any:
        """Calculate the minimum height required for the TextInput.
        
        This method computes the minimum height needed to display all
        lines of text without clipping, taking into account line height,
        line spacing, and padding. If the TextInput is not multiline, it
        simply returns the line height.
        
        Overrides the default behavior to provide accurate sizing
        for multiline TextInputs."""
        default = self.line_height
        if not self.multiline:
            return default
        
        minimum_height = (
            len(self._lines) * (self.line_height + self.line_spacing)
            + self.padding[1]
            + self.padding[3])
        return max(minimum_height, default)

    minimum_height: int = AliasProperty(
        _get_min_height,
        bind=[
            '_lines', 'line_height', 'line_spacing', 'padding', 'multiline',
            'password'],
        cache=True)

    cursor_path: List[float] = AliasProperty(
        lambda self: [
            *self.cursor_pos,
            self.cursor_pos[0],
            self.cursor_pos[1] - self.line_height],
        bind=['cursor_pos', 'line_height'],
        cache=True)
    """The path points for the cursor line (read-only).

    This property defines the points for drawing the cursor line based
    on the current cursor position and line height.

    :attr:`cursor_path` is a :class:`~kivy.properties.AliasProperty`.
    """
    
    _text_color_instruction: Color
    """Kivy Color instruction for the text color."""

    _cursor_instruction: Color
    """Kivy Line instruction for the cursor."""

    _cursor_color_instruction: Line
    """Kivy Color instruction for the cursor color."""

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        for child in self.canvas.before.children:
            if child.group is None and not isinstance(child, BoxShadow):
                self.canvas.before.remove(child)

        with self.canvas.before:
            self._cursor_color_instruction = Color(
                rgba=self.cursor_color,
                group=NAME.TEXTINPUT_CURSOR)
            self._cursor_instruction = Line(
                width=self.cursor_width,
                points=self.cursor_path,
                group=NAME.TEXTINPUT_CURSOR)
        
        # Since we are playing around with the canvas instruction the text 
        # loses its color, so we have to provide another one.
        # This is a workaround until we have a better solution.
        with self.canvas.before:
            self._text_color_instruction = Color(
                rgba=self.content_color,
                group=NAME.TEXTINPUT_TEXT)

        self.bind(
            _cursor_blink=self.update_cursor,
            cursor_path=self.update_cursor,
            cursor_color=self.update_cursor,
            cursor_width=self.update_cursor,
            focus=self.update_cursor,
            content_color=self.setter('cursor_color'),)

    def update_cursor(self, *args) -> None:
        """Update the cursor appearance based on focus and blink state.
        
        This method updates the cursor's color and position based on
        whether the TextInput is focused and if the cursor blink is
        active.

        It overrides the default behavior to ensure the cursor is
        displayed correctly with MorphUI theming.
        """
        if self.focus and self._cursor_blink:
            self._cursor_color_instruction.rgba = self.cursor_color
        else:
            self._cursor_color_instruction.rgba = [0, 0, 0, 0]
        self._cursor_instruction.points = self.cursor_path


class MorphTextField(
        MorphFloatLayout,
        MorphAutoSizingBehavior,
        MorphTypographyBehavior,
        MorphContentLayerBehavior,):
    
    text: str = StringProperty('')
    """The text content of the text field.

    This property holds the current text entered in the text field. It
    can be accessed and modified programmatically to get or set the
    text value.

    :attr:`text` is a :class:`~kivy.properties.StringProperty` and defaults to ''."""
    
    focus: bool = BooleanProperty(False)
    """Indicates whether the text field is focused (active for input).
    
    This property reflects the focus state of the internal text input
    widget. When True, the text field is active and ready to receive
    keyboard input. When False, it is inactive.
    
    :attr:`focus` is a :class:`~kivy.properties.BooleanProperty`
    and defaults to False."""

    multiline: bool = BooleanProperty(False)
    """Indicates whether the text field supports multiple lines of input.
    
    When True, the text field allows multiple lines of text input.
    When False, it restricts input to a single line.

    :attr:`multiline` is a :class:`~kivy.properties.BooleanProperty`
    and defaults to False."""

    label_text: str = StringProperty('')
    """The main label text displayed above the text input area.

    When set, this text appears as a label above the input field,
    providing context for the expected input. On focus, the label may
    animate or change style to indicate active input state.

    :attr:`label_text` is a :class:`~kivy.properties.StringProperty`
    and defaults to ''."""

    supporting_text: str = StringProperty('')
    """The supporting text displayed below the text input area.

    This text provides additional information or instructions related
    to the input field. It appears below the main input area and can
    change style based on the input state.

    :attr:`supporting_text` is a :class:`~kivy.properties.StringProperty`
    and defaults to ''."""

    leading_icon: str = StringProperty('')
    """The icon displayed to the leading (left) side of the text input 
    area.

    This icon can be used to visually represent the purpose of the input
    field or to provide additional context. It appears to the left of
    the main input area and can change style based on the input state.

    :attr:`leading_icon` is a :class:`~kivy.properties.StringProperty`
    and defaults to ''."""

    trailing_icon: str = StringProperty('')
    """The icon displayed to the trailing (right) side of the text input
    area.

    This icon can be used to visually represent the action associated
    with the input field or to provide additional context. It appears to
    the right of the main input area and can change style based on the
    input state.

    :attr:`trailing_icon` is a :class:`~kivy.properties.StringProperty`
    and defaults to ''."""

    label: TextFieldLabel = ObjectProperty()
    """The main label widget displayed above the text input area.

    This widget represents the label associated with the text field.
    It is automatically created and managed by the MorphTextField class.

    :attr:`label` is a :class:`~kivy.properties.ObjectProperty`
    and defaults to a TextFieldLabel instance."""

    supporting_label: TextFieldSupportingLabel = ObjectProperty()
    """The supporting label widget displayed below the text input area.

    This widget represents the supporting text associated with the text
    field. It is automatically created and managed by the MorphTextField
    class.

    :attr:`supporting_label` is a :class:`~kivy.properties.ObjectProperty`
    and defaults to a TextFieldSupportingLabel instance."""

    leading_widget: TextFieldLeadingIconLabel = ObjectProperty()
    """The leading icon widget displayed to the left of the text input
    area.

    This widget represents the leading icon associated with the text
    field. It is automatically created and managed by the MorphTextField
    class.

    :attr:`leading_widget` is a :class:`~kivy.properties.ObjectProperty`
    and defaults to a TextFieldLeadingIconLabel instance."""

    trailing_widget: TextFieldTrailingIconButton = ObjectProperty()
    """The trailing icon button widget displayed to the right of the text input
    area.

    This widget represents the trailing icon button associated with the text
    field. It is automatically created and managed by the MorphTextField
    class.
    
    :attr:`trailing_widget` is a :class:`~kivy.properties.ObjectProperty`
    and defaults to a TextFieldTrailingIconButton instance."""

    spacing: float = NumericProperty(dp(16))
    """The spacing between child widgets within the text field.

    This property defines the amount of space (in pixels) between
    the various child widgets (labels, icons, input area) contained
    within the text field.

    :attr:`spacing` is a :class:`~kivy.properties.NumericProperty`
    and defaults to dp(16)."""

    padding: List[float] = VariableListProperty(dp(16), length=4)
    """The padding around the text field content.

    This property defines the amount of space (in pixels) between
    the text field content and its outer edges. This padding is updated
    automatically based on the presence of leading and trailing icons.

    :attr:`padding` is a :class:`~kivy.properties.VariableListProperty`
    and defaults to dp(16)."""

    maximum_height: float = NumericProperty(dp(100))
    """The maximum height of the text field. 

    This property limits how tall the text field can grow, even when
    auto-sizing is enabled. It helps maintain layout consistency.

    :attr:`maximum_height` is a :class:`~kivy.properties.NumericProperty`
    and defaults to dp(100)."""

    minimum_width: float = AliasProperty(
        lambda self: (
            self.padding[0] + self._text_input.minimum_width + self.padding[2]),
        bind=['size', 'padding'],
        cache=True)
    """The minimum width of the text field (read-only).

    This property calculates the minimum width required to accommodate
    the internal text input widget along with the defined padding.

    :attr:`minimum_width` is a :class:`~kivy.properties.AliasProperty`
    and is read-only."""
    
    minimum_height: float = AliasProperty(
        lambda self: (
            self.padding[1] + self._text_input.minimum_height + self.padding[3]),
        bind=['size', 'padding'],
        cache=True)
    """The minimum height of the text field (read-only).

    This property calculates the minimum height required to accommodate
    the internal text input widget along with the defined padding.
    
    :attr:`minimum_height` is a :class:`~kivy.properties.AliasProperty`
    and is read-only."""
    
    minimum_size: List[float] = AliasProperty(
        lambda self: [self.minimum_width, self.minimum_height],
        bind=['minimum_width', 'minimum_height'],
        cache=True)
    """The minimum size of the text field as [width, height]
    (read-only).

    This property calculates the minimum size required to accommodate
    the internal text input widget along with the defined padding.

    :attr:`minimum_size` is a :class:`~kivy.properties.AliasProperty`
    and is read-only."""

    default_config = dict(
        radius=[2, 2, 2, 2],
        theme_color_bindings=dict(
            surface_color='surface_color',
            border_color='outline_color',
            error_border_color='error_color',
            focused_border_color='primary_color',
            disabled_border_color='outline_variant_color',
            content_color='content_surface_color',),
        auto_height=True,)
    """Default configuration values for MorphTextField.

    Provides standard text field appearance and behavior settings:
    - Single-line input for concise data entry.
    - Rounded corners for a modern look.
    - Themed colors for consistency with the overall UI design.
    """

    _text_input: MorphTextInput
    """The internal text input widget used for user input.
    This widget handles the actual text input functionality and is
    managed internally by the MorphTextField class."""

    def __init__(self, **kwargs) -> None:
        self._text_input = MorphTextInput(
            identity=NAME.INPUT,
            size_hint=(None, None),
            auto_size=False)

        child_classes = dict(
            label=TextFieldLabel,
            supporting_label=TextFieldSupportingLabel,
            leading_widget=TextFieldLeadingIconLabel,
            trailing_widget=TextFieldTrailingIconButton,)
        config = clean_config(self.default_config, kwargs)
        for attr, cls in child_classes.items():
            if attr not in config:
                config[attr] = cls()

        super().__init__(self._text_input, **config)

        self._text_input.bind(
            text=self.setter('text'),
            focus=self.setter('focus'),
            _lines=self._update_appearance,)
        
        self.bind(
            pos=self._update_appearance,
            size=self._update_appearance,
            declarative_children=self._update_appearance,
            multiline=self._text_input.setter('multiline'),
            text=self._text_input.setter('text'),)
        self.fbind(
            'label_text', self._update_child_widget,
            identity=NAME.LABEL)
        self.fbind(
            'supporting_text', self._update_child_widget,
            identity=NAME.SUPPORTING_LABEL)
        self.fbind(
            'leading_icon', self._update_child_widget,
            identity=NAME.LEADING_WIDGET)
        self.fbind(
            'trailing_icon', self._update_child_widget,
            identity=NAME.TRAILING_WIDGET)

        self.refresh_textfield_content()

    def _update_child_widget(
            self, instance: Any, text: str, identity: str) -> None:
        """Add, update, or remove a child widget based on the provided 
        text and identity.

        This method manages the presence and content of child widgets
        (labels, icons) within the text field. It adds the widget if
        text is provided and the widget is not already present. It
        updates the widget's content if it exists. If no text is
        provided, the widget is removed.

        Parameters
        ----------
        instance : Any
            The instance of the widget being updated.
        text : str
            The text content to set for the child widget.
        identity : str
            The identity of the child widget being updated.
        """
        match identity:
            case NAME.LABEL:
                widget = self.label
            case NAME.SUPPORTING_LABEL:
                widget = self.supporting_label
            case NAME.LEADING_WIDGET:
                widget = self.leading_widget
            case NAME.TRAILING_WIDGET:
                widget = self.trailing_widget
            case _:
                raise ValueError(
                    f'Widget not found for identity: {identity!r}')

        if hasattr(widget, 'icon'):
            widget.icon = text
        else:
            widget.text = text
        
        if text and identity not in self.identities:
            widget.identity = identity
            self.add_widget(widget)
        elif not text and identity in self.identities:
            self.remove_widget(widget)
        self._update_appearance()

    def _update_appearance(self, *args) -> None:
        """Update the layout and appearance of the text field and its
        child widgets.

        This method recalculates the positions and sizes of the child
        widgets based on the current layout and appearance settings.
        """
        self.padding = [
            dp(12) if NAME.LEADING_WIDGET not in self.identities else dp(16),
            dp(8),
            dp(12) if NAME.TRAILING_WIDGET not in self.identities else dp(16),
            dp(8)]
        
        input_x = self.x + self.padding[0]
        center_y = self.y + self.height / 2

        if NAME.LEADING_WIDGET in self.identities:
            self.leading_widget.x = self.x + self.padding[0]
            self.leading_widget.center_y = center_y
            input_x = self.leading_widget.right + self.spacing

        if NAME.TRAILING_WIDGET in self.identities:
            self.trailing_widget.right = self.width - self.padding[2]
            self.trailing_widget.center_y = center_y

        if NAME.SUPPORTING_LABEL in self.identities:
            self.supporting_label.y = self.supporting_label.height - dp(4)
            self.supporting_label.x = self.padding[0]
        
        self._update_text_input_size()
        self._text_input.x = input_x
        self._text_input.center_y = center_y

    def _update_text_input_size(self, *args) -> None:
        """Update the size of the internal text input widget based on
        the current layout and appearance settings.
        """
        if NAME.TRAILING_WIDGET in self.identities:
            input_right = self.trailing_widget.x - self.spacing
        else:
            input_right = self.x + self.width - self.padding[2]
        self._text_input.width = input_right - self._text_input.x

        height = min(
            self._text_input.minimum_height,
            self.maximum_height - self.padding[1] - self.padding[3])
        self._text_input.height = height

    def refresh_textfield_content(self, *args) -> None:
        """Refresh the content of the text field and its child widgets.

        This method updates the text and icons of the child widgets
        by calling the _update_child_widget method for each widget.
        """
        self._update_child_widget(
            self, self.label_text, NAME.LABEL)
        self._update_child_widget(
            self, self.supporting_text, NAME.SUPPORTING_LABEL)
        self._update_child_widget(
            self, self.leading_icon, NAME.LEADING_WIDGET)
        self._update_child_widget(
            self, self.trailing_icon, NAME.TRAILING_WIDGET)
        
        self._update_appearance()
    
    def _update_size(self, *args) -> None:
        super()._update_size(*args)
        self.height = clamp(
            self.height, self.minimum_height, self.maximum_height)
