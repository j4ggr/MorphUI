from typing import Any
from typing import Dict
from typing import List
from typing import Tuple

from kivy.clock import Clock
from kivy.event import EventDispatcher
from kivy.metrics import dp
from kivy.metrics import sp
from kivy.graphics import Line
from kivy.graphics import Color
from kivy.graphics import BoxShadow
from kivy.animation import Animation
from kivy.properties import AliasProperty
from kivy.properties import StringProperty
from kivy.properties import ObjectProperty
from kivy.properties import OptionProperty
from kivy.properties import BooleanProperty
from kivy.properties import NumericProperty
from kivy.properties import VariableListProperty
from kivy.uix.textinput import TextInput

from ..utils import clamp
from ..utils import clean_config

from .behaviors import MorphThemeBehavior
from .behaviors import MorphHoverBehavior
from .behaviors import MorphTextLayerBehavior
from .behaviors import MorphAutoSizingBehavior
from .behaviors import MorphTypographyBehavior
from .behaviors import MorphContentLayerBehavior
from .behaviors import MorphIdentificationBehavior
from .behaviors import MorphInteractionLayerBehavior

from .floatlayout import MorphFloatLayout

from .label import MorphSimpleLabel
from .label import MorphSimpleIconLabel

from .button import MorphIconButton

from ..constants import NAME
from ..constants import REGEX


__all__ = [
    'TextFieldLabel',
    'TextFieldSupportingLabel',
    'TextFieldLeadingIconLabel',
    'TextFieldTrailingIconButton',
    'TextValidator',
    'MorphTextInput',
    'MorphTextField',]


class TextFieldLabel(MorphSimpleLabel):

    disabled: bool = BooleanProperty(False)

    focus: bool = BooleanProperty(False)
    
    error: bool = BooleanProperty(False)
    
    default_config: Dict[str, Any] = dict(
        theme_color_bindings=dict(
            content_color='content_surface_color',
            focus_content_color='primary_color',
            error_content_color='error_color',),
        typography_role='Label',
        typography_size='medium',
        typography_weight='Regular',
        halign='left',
        valign='middle',
        padding=[4, 0],
        auto_size=True,)


class TextFieldSupportingLabel(MorphSimpleLabel):

    disabled: bool = BooleanProperty(False)

    focus: bool = BooleanProperty(False)
    
    error: bool = BooleanProperty(False)
    
    default_config: Dict[str, Any] = dict(
        theme_color_bindings=dict(
            content_color='transparent_color',
            focus_content_color='primary_color',
            error_content_color='error_color',),
        typography_role='Label',
        typography_size='small',
        typography_weight='Regular',
        halign='left',
        valign='middle',
        auto_width=True,
        shorten=True,)


class TextFieldLeadingIconLabel(MorphSimpleIconLabel):

    disabled: bool = BooleanProperty(False)

    focus: bool = BooleanProperty(False)
    
    error: bool = BooleanProperty(False)
    
    default_config: Dict[str, Any] = dict(
        theme_color_bindings=dict(
            content_color='content_surface_color',
            focus_content_color='primary_color',
            error_content_color='error_color',),
        font_name=MorphSimpleIconLabel.default_config['font_name'],
        typography_role=MorphSimpleIconLabel.default_config['typography_role'],
        typography_size=MorphSimpleIconLabel.default_config['typography_size'],
        halign='center',
        valign='middle',
        size_hint=(None, None),
        size=(dp(24), dp(24)),
        padding=dp(0),)


class TextFieldTrailingIconButton(MorphIconButton):

    disabled: bool = BooleanProperty(False)

    focus: bool = BooleanProperty(False)

    error: bool = BooleanProperty(False)

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


class TextValidator(EventDispatcher):

    error: bool = BooleanProperty(False)
    """Indicates whether the text widget is in an error state.

    This property reflects the error state of the internal text. 
    When True, the text widget is marked as having an error,
    When False, it is not in an error state.

    :attr:`error` is a :class:`~kivy.properties.BooleanProperty`
    and defaults to False."""

    required: bool = BooleanProperty(False)
    """Indicates whether the text is required.

    When True, the :attr:`text` must contain valid text to be 
    considered valid. When False, the text widget can be left empty 
    without error.

    :attr:`required` is a :class:`~kivy.properties.BooleanProperty`
    and defaults to False."""

    validator: str | None = OptionProperty(
        None,
        allownone=True,
        options=['email', 'phone', 'date', 'time', 'datetime'])
    """The type of validation to apply to the text.

    This property determines the kind of validation that will be 
    performed on the text content. Supported options are:
    - 'email': Validates that the text is a properly formatted email 
      address.
    - 'phone': Validates that the text is a properly formatted phone 
      number.
    - 'date': Validates that the text is a properly formatted date.
    - 'time': Validates that the text is a properly formatted time.
    - 'datetime': Validates that the text is a properly formatted datetime.
    When set to None, no validation is performed.
    :attr:`validator` is a :class:`~kivy.properties.OptionProperty`
    and defaults to None.
    """

    def is_valid_email(self, text: str) -> bool:
        """Check if the given text is a valid email address.

        Parameters
        ----------
        text : str
            The text input to validate.

        Returns
        -------
        bool
            True if the input is a valid email address, False otherwise.
        """
        return REGEX.EMAIL.match(text) is not None

    def is_valid_phone(self, text: str) -> bool:
        """Check if the given text is a valid phone number.

        Parameters
        ----------
        text : str
            The text input to validate.

        Returns
        -------
        bool
            True if the input is a valid phone number, False otherwise.
        """
        text = (text
            .replace(" ", "")
            .replace("-", "")
            .replace("(", "")
            .replace(")", ""))
        return REGEX.PHONE.match(text) is not None
    
    def is_valid_date(self, text: str) -> bool:
        """Check if the given text is a valid date.

        This method checks the text against various date formats to
        determine its validity.

        Parameters
        ----------
        text : str
            The text input to validate.

        Returns
        -------
        bool
            True if the input is a valid date, False otherwise.
        """
        return any((
            REGEX.DATE_EU.match(text) is not None,
            REGEX.DATE_ISO.match(text) is not None,
            REGEX.DATE_US.match(text) is not None))
    
    def is_valid_time(self, text: str) -> bool:
        """Check if the given text is a valid time.

        Parameters
        ----------
        text : str
            The text input to validate.

        Returns
        -------
        bool
            True if the input is a valid time, False otherwise.
        """
        return REGEX.TIME.match(text) is not None
    
    def is_valid_datetime(self, text: str) -> bool:
        """Check if the given text is a valid datetime.

        Splits the text into date and time components and validates
        each part separately. Permits both 'T' and space as separators.
        Where the date must be the first part and the time the second 
        part. Then checks if both parts are valid. The expected format is
        'YYYY-MM-DDTHH:MM:SS' or 'YYYY-MM-DD HH:MM:SS'.

        Parameters
        ----------
        text : str
            The text input to validate.

        Returns
        -------
        bool
            True if the input is a valid datetime, False otherwise.
        """
        if 'T' in text:
            date_part, time_part = text.split('T', 1)
        elif ' ' in text:
            date_part, time_part = text.split(' ', 1)
        else:
            return False
        return self.is_valid_date(date_part) and self.is_valid_time(time_part)

    def validate(self, text: str) -> bool:
        """Validate the given text based on the current settings.

        This method checks the text against the required and validator
        properties to determine if it is valid.

        Parameters
        ----------
        text : str
            The text input to validate.
        
        Returns
        -------
        bool
            True if the text is valid according to the current settings,
            False otherwise.
        """
        if self.validator is None:
            self.error=False
            return True
        
        if self.required and not text:
            self.error = True
            return False

        match self.validator:
            case 'email':
                is_valid = self.is_valid_email(text)
            case 'phone':
                is_valid = self.is_valid_phone(text)
            case _:
                is_valid = True

        self.error = not is_valid
        return is_valid


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

    row_height: float = AliasProperty(
        lambda self: self.line_height + self.line_spacing,
        bind=['line_height', 'line_spacing'],
        cache=True)
    """The height of a single row of text.

    :attr:`row_height` is a :class:`~kivy.properties.AliasProperty`.
    """

    def _get_min_height(self) -> Any:
        """Calculate the minimum height required for the TextInput.
        
        This method computes the minimum height needed to display all
        lines of text without clipping, taking into account line height,
        line spacing, and padding. If the TextInput is not multiline, it
        simply returns the line height.
        
        Overrides the default behavior to provide accurate sizing
        for multiline TextInputs."""
        if not self.multiline:
            return self.row_height

        minimum_height = (
            len(self._lines) * self.row_height
            + self.padding[1]
            + self.padding[3])
        return clamp(minimum_height, self.row_height, self.maximum_height)

    minimum_height: int = AliasProperty(
        _get_min_height,
        bind=[
            '_lines', 'line_height', 'line_spacing', 'padding', 'multiline',
            'password', 'maximum_height'],
        cache=True)
    """The minimum height of the TextInput based on content (read-only).

    This property calculates the minimum height required to display
    all lines of text without clipping, taking into account line height,
    line spacing, and padding. If the TextInput is not multiline, it
    simply returns the line height.

    :attr:`minimum_height` is a :class:`~kivy.properties.AliasProperty`.
    """

    maximum_height: int = NumericProperty(dp(300))
    """The maximum height of the TextInput when auto_height is enabled.

    Sets the upper limit for the height of the TextInput when
    auto_height is True. This prevents the TextInput from growing
    excessively tall.

    :attr:`maximum_height` is a :class:`~kivy.properties.NumericProperty`
    and defaults to dp(300)."""

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
        TextValidator,
        MorphHoverBehavior,
        MorphTypographyBehavior,
        MorphContentLayerBehavior,
        MorphInteractionLayerBehavior,
        MorphFloatLayout,):
    
    text: str = StringProperty('')
    """The text content of the text field.

    This property holds the current text entered in the text field. It
    can be accessed and modified programmatically to get or set the
    text value. It is bound bidirectionally to the text property of the
    internal :class:`MorphTextInput`.

    :attr:`text` is a :class:`~kivy.properties.StringProperty` and 
    defaults to ''."""
    
    disabled: bool = BooleanProperty(False)
    """Indicates whether the text field is disabled.
    
    When True, the text field is disabled and does not accept input.
    When False, it is enabled and can receive user input. It is bound
    bidirectionally to the disabled property of the internal
    :class:`MorphTextInput`.

    :attr:`disabled` is a :class:`~kivy.properties.BooleanProperty`
    and defaults to False."""

    focus: bool = BooleanProperty(False)
    """Indicates whether the text field is focused (active for input).
    
    This property reflects the focus state of the internal text input
    widget. When True, the text field is active and ready to receive
    keyboard input. When False, it is inactive. It is bound
    bidirectionally to the focus state of the internal
    :class:`MorphTextInput`.

    :attr:`focus` is a :class:`~kivy.properties.BooleanProperty`
    and defaults to False."""

    multiline: bool = BooleanProperty(False)
    """Indicates whether the text field supports multiple lines of input.
    
    When True, the text field allows multiple lines of text input.
    When False, it restricts input to a single line. It is bound
    bidirectionally to the multiline property of the internal
    :class:`MorphTextInput`.

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

    label_widget: TextFieldLabel = ObjectProperty()
    """The main label widget displayed above the text input area.

    This widget represents the label associated with the text field.
    It is automatically created and managed by the MorphTextField class.

    :attr:`label_widget` is a :class:`~kivy.properties.ObjectProperty`
    and defaults to a TextFieldLabel instance."""

    supporting_widget: TextFieldSupportingLabel = ObjectProperty()
    """The supporting label widget displayed below the text input area.

    This widget represents the supporting text associated with the text
    field. It is automatically created and managed by the MorphTextField
    class.

    :attr:`supporting_widget` is a :class:`~kivy.properties.ObjectProperty`
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

    maximum_height: float = NumericProperty(dp(100))
    """The maximum height of the text field. 

    This property limits how tall the text field can grow, even when
    auto-sizing is enabled. It helps maintain layout consistency.

    :attr:`maximum_height` is a :class:`~kivy.properties.NumericProperty`
    and defaults to dp(100)."""

    focus_animation_duration: float = NumericProperty(0.15)
    """The duration of the focus animation in seconds.

    This property defines how long the animation takes when the text
    field gains or loses focus. It affects the speed of visual
    transitions related to focus changes.

    :attr:`focus_animation_duration` is a
    :class:`~kivy.properties.NumericProperty` and defaults to 0.15."""

    focus_animation_transition: str = StringProperty('out_sine')
    """The transition type for the focus animation.

    This property determines the easing function used for the focus
    animation. It affects the style of the animation when the text
    field gains or loses focus. For a list of supported transitions,
    refer to the 
    [Kivy documentation](https://kivy.org/doc/stable/api-kivy.animation.html)

    :attr:`focus_animation_transition` is a 
    :class:`~kivy.properties.StringProperty` and defaults to 'out_sine'.
    """

    label_focus_behavior: str = OptionProperty(
        'float_to_border',
        options=['hide', 'float_to_border', 'move_above'])
    """Controls how the label widget behaves when the text field gains 
    focus.

    This property determines the animation and positioning behavior of 
    the label widget during focus transitions:

    - 'hide': The label disappears when the text field is focused
    - 'float_to_border': The label moves up and floats over the border 
    (current Material Design implementation)
    - 'move_above': The label moves completely above the input area, 
    pushing the input field down slightly

    :attr:`label_focus_behavior` is a 
    :class:`~kivy.properties.OptionProperty` and defaults to 
    'float_to_border'."""

    _text_input_margin: List[float] = VariableListProperty(dp(0), length=4)
    """The margin around the internal text input widget.

    This property defines the margin space around the internal
    :class:`MorphTextInput` widget within the text field. It is used
    for layout calculations and positioning. The margins are defined
    as [left, bottom, right, top].

    :attr:`_text_input_margin` is a
    :class:`~kivy.properties.VariableListProperty` of length 4."""

    text_input_default_margin: List[float] = VariableListProperty(
        [dp(8), dp(8), dp(8), dp(8)], length=4)
    """The default margin values around the internal text input widget.

    This property defines the base margin space that is applied around
    the internal :class:`MorphTextInput` widget before any adjustments
    for icons or other widgets. The margins are defined as 
    [left, bottom, right, top].

    :attr:`text_input_default_margin` is a
    :class:`~kivy.properties.VariableListProperty` of length 4 and
    defaults to [dp(8), dp(8), dp(8), dp(8)]."""

    _horizontal_padding: float = NumericProperty(dp(12))
    """The horizontal padding applied around the widgets.

    This padding is applied to the left and right sides of the leading
    and trailing widgets if present. Otherwise for the internal text
    input area, it ensures consistent alignment of the widgets.

    :attr:`_horizontal_padding` is a 
    :class:`~kivy.properties.NumericProperty` and defaults to dp(12)."""

    _text_input_min_width: float = NumericProperty(dp(0))
    """The current minimum width of the internal text input widget.

    This property is used for layout calculations and reflects the
    current minimum width of the internal text input widget.

    :attr:`_text_input_min_width` is a
    :class:`~kivy.properties.NumericProperty`."""

    _text_input_height: float = NumericProperty(dp(0))
    """The current height of the internal text input widget.

    This property is used for layout calculations and reflects the
    current height of the internal text input widget.

    :attr:`_text_input_height` is a
    :class:`~kivy.properties.NumericProperty`."""

    minimum_width: float = AliasProperty(
        lambda self: (
            self._text_input_min_width
            + self._text_input_margin[0]
            + self._text_input_margin[2]),
        bind=['size', '_text_input_margin', '_text_input_min_width'],
        cache=True)
    """The minimum width of the text field (read-only).

    This property calculates the minimum width required to accommodate
    the internal text input widget along with the defined padding.

    :attr:`minimum_width` is a :class:`~kivy.properties.AliasProperty`
    and is read-only."""
    
    minimum_height: float = AliasProperty(
        lambda self: (
            self._text_input_height
            + self._text_input_margin[1]
            + self._text_input_margin[3]),
        bind=['size', '_text_input_margin', '_text_input_height'],
        cache=True)
    """The minimum height of the text field (read-only).

    This property calculates the minimum height required to accommodate
    the internal text input widget along with the defined padding.
    
    :attr:`minimum_height` is a :class:`~kivy.properties.AliasProperty`
    and is read-only."""

    default_config = dict(
        radius=[2, 2, 2, 2],
        theme_color_bindings=dict(
            surface_color='surface_color',
            border_color='outline_color',
            error_border_color='error_color',
            focus_border_color='primary_color',
            disabled_border_color='outline_variant_color',
            content_color='content_surface_color',),
        size_hint_y=None,)
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

    _label_initial_color_bindings: dict[str, str] = {}
    """Stores the initial color bindings of the label widget for
    restoration after focus changes."""

    _label_initial_font_size: float = sp(1)
    """Stores the initial font size of the label widget for
    restoration after focus changes."""

    _label_size_factor: float = 1.0
    """Stores the size factor of the label widget for scaling purposes."""

    def __init__(self, **kwargs) -> None:
        self._text_input = MorphTextInput(
            identity=NAME.INPUT,
            size_hint=(None, None),
            padding=dp(0),
            auto_height=True)

        child_classes = dict(
            label_widget=TextFieldLabel,
            supporting_widget=TextFieldSupportingLabel,
            leading_widget=TextFieldLeadingIconLabel,
            trailing_widget=TextFieldTrailingIconButton,)
        config = clean_config(self.default_config, kwargs)
        for attr, cls in child_classes.items():
            if attr not in config:
                config[attr] = cls()

        super().__init__(**config)
        self.add_widget(self._text_input)
        self._label_initial_color_bindings = (
            self.label_widget.theme_color_bindings.copy())
        self._label_initial_font_size = self.label_widget.font_size

        bidirectional_binding = (
            'text',
            'focus',
            'disabled',
            'multiline',
            'content_color',)
        for prop in bidirectional_binding:
            self.fbind(prop, self._text_input.setter(prop))
            self._text_input.fbind(prop, self.setter(prop))
            setattr(self._text_input, prop, getattr(self, prop))

        self._text_input.bind(
            _lines=self._update_layout,
            height=self.setter('_text_input_height'),
            minimum_width=self.setter('_text_input_min_width'),)
        
        self.bind(
            pos=self._update_layout,
            width=self._update_layout,
            declarative_children=self._update_layout,
            _text_input_margin=self._update_text_input_coordinates,
            focus=self._animate_on_focus,
            minimum_height=self.setter('height'),)
        self.fbind(
            'label_text',
            self._update_child_widget,
            identity=NAME.LABEL_WIDGET)
        self.fbind(
            'supporting_text',
            self._update_child_widget,
            identity=NAME.SUPPORTING_WIDGET)
        self.fbind(
            'leading_icon',
            self._update_child_widget,
            identity=NAME.LEADING_WIDGET)
        self.fbind(
            'trailing_icon',
            self._update_child_widget,
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
            case NAME.LABEL_WIDGET:
                widget = self.label_widget
            case NAME.SUPPORTING_WIDGET:
                widget = self.supporting_widget
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
        self._update_layout()

    def _update_layout(self, *args) -> None:
        """Update the layout of the text field and its child widgets.

        This method recalculates the positions and sizes of the child
        widgets based on the current layout settings.
        """
        if NAME.LEADING_WIDGET in self.identities:
            self.leading_widget.x = self.x + self._horizontal_padding
            self.leading_widget.center_y = self.center_y

        if NAME.TRAILING_WIDGET in self.identities:
            self.trailing_widget.right = (
                self.x + self.width - self._horizontal_padding)
            self.trailing_widget.center_y = self.center_y

        if NAME.SUPPORTING_WIDGET in self.identities:
            self.supporting_widget.x = self.x + self._horizontal_padding
            self.supporting_widget.y = (
                self.y - self.supporting_widget.height - dp(4))

        self._text_input_margin = self._resolve_text_input_margin()
        self._update_text_input_coordinates()
        self.width = max(self.width, self.minimum_width)

        if NAME.LABEL_WIDGET in self.identities:
            self.label_widget.pos = self._resolve_label_position()

    def _update_text_input_coordinates(self, *args) -> None:
        """Update the coordinates of the internal text input widget 
        based on the current layout and appearance settings.
        """
        self._text_input.x = self.x + self._text_input_margin[0]
        self._text_input.y = self.y + self._text_input_margin[1]
        width = (
            self.width
            - self._text_input_margin[0]
            - self._text_input_margin[2])
        self._text_input.width = max(self._text_input.minimum_width, width)
        maximum_height = (
            self.maximum_height
            - self._text_input_margin[1]
            - self._text_input_margin[3])
        self._text_input.maximum_height = maximum_height
        
    def refresh_textfield_content(self, *args) -> None:
        """Refresh the content of the text field and its child widgets.

        This method updates the text and icons of the child widgets
        by calling the _update_child_widget method for each widget.
        """
        self._text_input_height = self._text_input.height
        self._text_input_min_width = self._text_input.minimum_width

        self._update_child_widget(
            self, self.label_text, NAME.LABEL_WIDGET)
        self._update_child_widget(
            self, self.supporting_text, NAME.SUPPORTING_WIDGET)
        self._update_child_widget(
            self, self.leading_icon, NAME.LEADING_WIDGET)
        self._update_child_widget(
            self, self.trailing_icon, NAME.TRAILING_WIDGET)
        
        self._update_layout()
        self.on_current_content_state(self, self.current_content_state)

    def on_current_content_state(self, instance: Any, state: str) -> None:
        """Handle changes to the current content state of the text field.

        This method updates the appearance of the text field and its
        child widgets based on the current content state (e.g., normal,
        focused, error).

        Parameters
        ----------
        state : str
            The new content state of the text field.
        """
        for child in self.declarative_children:
            for state in self.possible_states:
                if not hasattr(child, state):
                    continue

                value = getattr(self, state, None)
                if value is not None:
                    setattr(child, state, value)

    def _resolve_label_position(self) -> Tuple[float, float]:
        """Get the position of the main label widget.

        Returns
        -------
        Tuple[float, float]
            The (x, y) position of the main label widget.
        """
        x = self._text_input.x
        y = self._text_input.center_y - self.label_widget.height / 2
        if any((
                self.label_focus_behavior == 'hide',
                not self.focus and not self.text)):
            return (x, y)
        
        if self.label_focus_behavior == 'move_above':
            x = self._text_input.x
            y = (
                self.y
                + self._resolve_text_input_margin()[1]
                + self._text_input_height
                + dp(4))
        elif self.label_focus_behavior == 'float_to_border':
            x = max(
                self.x + self._horizontal_padding,
                self.x + self.clamped_radius[0])
            y = self.y + self.height - self.label_widget.height / 2
        return (x, y)
    
    def _resolve_label_font_size(self) -> float:
        """Get the font size for the main label widget.

        Returns
        -------
        float
            The font size for the main label widget.
        """
        if self.focus or self.text:
            font_size = self.typography.get_font_size(
                role=self.label_widget.typography_role,
                size='small')
        else:
            font_size = self._label_initial_font_size

        if isinstance(font_size, str):
            font_size = sp(int(font_size.replace('sp', '')))
        self._label_size_factor = font_size / self._label_initial_font_size
        return font_size
    
    def _resolve_text_input_margin(self) -> List[float]:
        """Get the margin values for the internal text input widget.

        Returns
        -------
        List[float]
            The margin values [left, bottom, right, top] for the
            internal text input widget.
        """
        margin = self.text_input_default_margin.copy()
        if NAME.LEADING_WIDGET in self.identities:
            margin[0] = (
                margin[0]
                + self.leading_widget.width
                + self._horizontal_padding)
        if NAME.TRAILING_WIDGET in self.identities:
            margin[2] = (
                margin[2]
                + self.trailing_widget.width 
                + self._horizontal_padding)
        if self.label_focus_behavior == 'move_above' and (self.focus or self.text):
            spacing = dp(4)
            margin[1] = spacing
            margin[3] = dp(24)
        return margin

    def _animate_on_focus(self, *args) -> None:
        """Handle focus changes for the text field.

        This method animates the main label widget to a new position
        and font size when the text field gains or loses focus.
        """
        if NAME.LABEL_WIDGET not in self.identities:
            return

        Animation.stop_all(self.label_widget, 'pos', 'font_size', 'color')
        Animation.stop_all(self, 'border_open_length', '_text_input_margin')

        font_size = self._resolve_label_font_size()
        target_pos = self._resolve_label_position()

        self.border_width = dp(2) if self.focus else dp(1)

        if self.label_focus_behavior == 'hide':
            color_bindings = self._label_initial_color_bindings.copy()
            if self.focus:
                _colors = (k for k in color_bindings if 'content' in k)
                color_bindings.update(
                    {c: 'transparent_color' for c in _colors})
            self.label_widget.theme_color_bindings = color_bindings
            Animation(
                x=target_pos[0],
                y=target_pos[1],
                font_size=font_size,
                color=self.label_widget.get_resolved_content_color(),
                d=self.focus_animation_duration,
                t=self.focus_animation_transition,
            ).start(self.label_widget)
            return

        Animation(
            x=target_pos[0],
            y=target_pos[1],
            font_size=font_size,
            d=self.focus_animation_duration,
            t=self.focus_animation_transition,
        ).start(self.label_widget)
        
        if self.label_focus_behavior == 'float_to_border':
            if self.focus:
                border_open_length = (
                    self.label_widget.width * self._label_size_factor)
            else:
                border_open_length = 0
            Animation(
                border_open_length=border_open_length,
                d=self.focus_animation_duration,
                t=self.focus_animation_transition
            ).start(self)
        elif self.label_focus_behavior == 'move_above':
            Animation(
                _text_input_margin=self._resolve_text_input_margin(),
                d=self.focus_animation_duration,
                t=self.focus_animation_transition
            ).start(self)
        
    