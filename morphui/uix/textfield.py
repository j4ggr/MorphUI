from typing import Any
from typing import Dict
from typing import List
from typing import Tuple

from kivy.event import EventDispatcher
from kivy.metrics import dp
from kivy.metrics import sp
from kivy.graphics import Line
from kivy.graphics import Color
from kivy.graphics import BoxShadow
from kivy.animation import Animation
from kivy.properties import DictProperty
from kivy.properties import ColorProperty
from kivy.properties import AliasProperty
from kivy.properties import StringProperty
from kivy.properties import ObjectProperty
from kivy.properties import OptionProperty
from kivy.properties import BooleanProperty
from kivy.properties import NumericProperty
from kivy.properties import VariableListProperty
from kivy.uix.textinput import TextInput

from morphui.utils import clamp
from morphui.utils import clean_config

from morphui.uix.behaviors import MorphThemeBehavior
from morphui.uix.behaviors import MorphHoverBehavior
from morphui.uix.behaviors import MorphSizeBoundsBehavior
from morphui.uix.behaviors import MorphAutoSizingBehavior
from morphui.uix.behaviors import MorphTypographyBehavior
from morphui.uix.behaviors import MorphRoundSidesBehavior
from morphui.uix.behaviors import MorphSurfaceLayerBehavior
from morphui.uix.behaviors import MorphContentLayerBehavior
from morphui.uix.behaviors import MorphIdentificationBehavior
from morphui.uix.behaviors import MorphInteractionLayerBehavior

from morphui.uix.floatlayout import MorphFloatLayout

from morphui.uix.label import MorphTextFieldLabel
from morphui.uix.label import MorphTextFieldSupportingLabel
from morphui.uix.label import MorphTextFieldTextLengthLabel
from morphui.uix.label import MorphTextFieldLeadingIconLabel

from morphui.uix.button import MorphTextFieldTrailingIconButton

from morphui.constants import NAME
from morphui.constants import REGEX


__all__ = [
    'MorphTextValidator',
    'MorphTextInput',
    'MorphTextField',
    'MorphTextFieldOutlined',
    'MorphTextFieldRounded',
    'MorphTextFieldFilled',]


NO_ERROR = 'none'
"""Constant representing no error state."""


class MorphTextValidator(EventDispatcher):

    error: bool = BooleanProperty(False)
    """Indicates whether the text widget is in an error state.

    This property reflects the error state of the internal text. 
    When True, the text widget is marked as having an error,
    When False, it is not in an error state.

    :attr:`error` is a :class:`~kivy.properties.BooleanProperty`
    and defaults to False."""

    error_type: str = StringProperty('')
    """The type of error associated with the current error state.

    This property holds a string that describes the type of error
    encountered in the text input. It can be used to provide
    specific feedback to the user about the nature of the error.
    The possible values are the same as those defined for the
    :attr:`validator` property plus `required` and `max_text_length`.

    :attr:`error_type` is a :class:`~kivy.properties.StringProperty`
    and defaults to an empty string."""

    required: bool = BooleanProperty(False)
    """Indicates whether the text is required.

    When True, the :attr:`text` must contain valid text to be 
    considered valid. When False, the text widget can be left empty 
    without error.

    :attr:`required` is a :class:`~kivy.properties.BooleanProperty`
    and defaults to False."""

    max_text_length: int = NumericProperty(0)
    """The maximum length of the text input.

    This property sets a limit on the number of characters that can be
    entered into the text widget. If the text exceeds this length,
    it will be truncated or rejected based on the implementation.

    :attr:`max_length` is a :class:`~kivy.properties.NumericProperty`
    and defaults to 0, which means no limit."""

    validator: str | None = OptionProperty(
        None,
        allownone=True,
        options=[
            'email', 'phone', 'date', 'time', 'datetime', 'numeric', 
            'alphanumeric'])
    """The type of validation to apply to the text.

    This property determines the kind of validation that will be 
    performed on the text content. Supported options are:
    - 'email': Validates that the text is a properly formatted email 
      address.
    - 'phone': Validates that the text is a properly formatted phone 
      number.
    - 'date': Validates that the text is a properly formatted date.
    - 'time': Validates that the text is a properly formatted time.
    - 'datetime': Validates that the text is a properly formatted 
      datetime.
    - 'numeric': Validates that the text is a valid numeric value.
    - 'alphanumeric': Validates that the text contains only letters
      and numbers.

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

    def is_valid_numeric(self, text: str) -> bool:
        """Check if the given text is a valid numeric value.

        Parameters
        ----------
        text : str
            The text input to validate.

        Returns
        -------
        bool
            True if the input is a valid numeric value, False otherwise.
        """
        return REGEX.NUMERIC.match(text) is not None
    
    def is_valid_alphanumeric(self, text: str) -> bool:
        """Check if the given text is a valid alphanumeric value.

        Parameters
        ----------
        text : str
            The text input to validate.

        Returns
        -------
        bool
            True if the input is a valid alphanumeric value, False 
            otherwise.
        """
        return REGEX.ALPHANUMERIC.match(text) is not None

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
        if self.required and not text:
            self.error = True
            self.error_type = 'required'
            return False
        
        if self.max_text_length > 0 and len(text) > self.max_text_length:
            self.error = True
            self.error_type = 'max_text_length'
            return False
        
        if self.validator is None:
            self.error = False
            self.error_type = NO_ERROR
            return True
        
        if hasattr(self, f'is_valid_{self.validator}'):
            is_valid_method = getattr(self, f'is_valid_{self.validator}')
            is_valid = is_valid_method(text)
        else:
            is_valid = True
        self.error = not is_valid
        self.error_type = NO_ERROR if is_valid else self.validator
        return is_valid


class MorphTextInput(
        MorphIdentificationBehavior,
        MorphThemeBehavior,
        MorphContentLayerBehavior,
        MorphSurfaceLayerBehavior,
        MorphAutoSizingBehavior,
        MorphSizeBoundsBehavior,
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

    def _get_minimum_height(self) -> Any:
        """Calculate the minimum height required for the TextInput.
        
        This method computes the minimum height needed to display all
        lines of text without clipping, taking into account line height,
        line spacing, and padding. If the TextInput is not multiline, it
        simply returns the line height.
        
        Overrides the default behavior to provide accurate sizing
        for multiline TextInputs."""
        lines = 1 if not self.multiline else len(self._lines)
        minimum_height = (
            lines * self.row_height
            + self.padding[1]
            + self.padding[3])
        return clamp(minimum_height, self.row_height, self.maximum_height)

    minimum_height: int = AliasProperty(
        _get_minimum_height,
        cache=True,
        bind=[
            '_lines',
            'line_height',
            'line_spacing',
            'padding',
            'multiline',
            'password',
            'maximum_height'],)
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
        cache=True,
        bind=[
            'cursor_pos',
            'line_height'],)
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
            focus=self.update_cursor,)

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
        MorphTextValidator,
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

    password: bool = BooleanProperty(False)
    """Indicates whether the text field is a password input.

    When True, the text field obscures the input text for password
    protection. When False, it displays the input text normally. It is
    bound bidirectionally to the password property of the internal
    :class:`MorphTextInput`.

    :attr:`password` is a :class:`~kivy.properties.BooleanProperty`
    and defaults to False."""

    selected_text_color: List[float] = ColorProperty(None, allownone=True)
    """The color of the text selection highlight.

    This property defines the RGBA color used to highlight selected
    text within the text field. It is bound bidirectionally to the
    selected_text_color property of the internal :class:`MorphTextInput`.

    :attr:`selected_text_color` is a :class:`~kivy.properties.ColorProperty`
    and defaults to None."""

    selected_text_color_opacity: float = NumericProperty(0.4)
    """The opacity of the text selection highlight color.

    :attr:`selected_text_color_opacity` is a
    :class:`~kivy.properties.NumericProperty` and defaults to 0.4."""

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

    supporting_error_texts: Dict[str, str] = DictProperty({})
    """Mapping of error types to supporting error messages.

    This property holds a dictionary that maps specific error types to
    corresponding error messages. When the text field enters an error
    state, the appropriate error message can be displayed based on the
    error type. The keys in the dictionary should match the possible
    values of the :attr:`validator` property. If you want to set a
    supporting text if there is no error, use the 'none' key.

    :attr:`supporting_error_texts` is a
    :class:`~kivy.properties.DictProperty` and defaults to an empty 
    dictionary."""

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

    label_widget: MorphTextFieldLabel = ObjectProperty()
    """The main label widget displayed above the text input area.

    This widget represents the label associated with the text field.
    It is automatically created and managed by the MorphTextField class.

    :attr:`label_widget` is by default an instance of
    :class:`~morphui.uix.label.MorphTextFieldLabel`."""

    supporting_widget: MorphTextFieldSupportingLabel = ObjectProperty()
    """The supporting label widget displayed below the text input area.

    This widget represents the supporting text associated with the text
    field. It is automatically created and managed by the MorphTextField
    class.

    :attr:`supporting_widget` is by default an instance of
    :class:`~morphui.uix.label.MorphTextFieldSupportingLabel`."""

    text_length_widget: MorphTextFieldTextLengthLabel = ObjectProperty()
    """The text length label widget displayed to the right of the
    supporting text area.

    This widget shows the current length of the text input, useful for
    fields with maximum length constraints. It is automatically created
    and managed by the :class:`MorphTextField` class.

    :attr:`text_length_widget` is a 
    :class:`~kivy.properties.ObjectProperty` and defaults to a
    MorphTextFieldTextLengthLabel instance."""

    leading_widget: MorphTextFieldLeadingIconLabel = ObjectProperty()
    """The leading icon widget displayed to the left of the text input
    area.

    This widget represents the leading icon associated with the text
    field. It is automatically created and managed by the MorphTextField
    class.

    :attr:`leading_widget` is by default an instance of
    :class:`~morphui.uix.label.MorphTextFieldLeadingIconLabel`."""

    trailing_widget: MorphTextFieldTrailingIconButton = ObjectProperty()
    """The trailing icon button widget displayed to the right of the text input
    area.

    This widget represents the trailing icon button associated with the text
    field. It is automatically created and managed by the MorphTextField
    class.

    :attr:`trailing_widget` is by default an instance of
    :class:`~morphui.uix.button.MorphTextFieldTrailingIconButton`."""

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

    _text_input_padding: List[float] = VariableListProperty(dp(0), length=4)
    """The padding around the internal text input widget.

    This property defines the padding space around the internal
    :class:`MorphTextInput` widget within the text field. It is used
    for layout calculations and positioning. The padding is defined
    as [left, bottom, right, top].

    :attr:`_text_input_padding` is a
    :class:`~kivy.properties.VariableListProperty` of length 4."""

    text_input_default_padding: List[float] = VariableListProperty(
        [dp(8), dp(8), dp(8), dp(8)], length=4)
    """The default padding values around the internal text input widget.

    This property defines the base padding space that is applied around
    the internal :class:`MorphTextInput` widget before any adjustments
    for icons or other widgets. The padding is defined as
    [left, bottom, right, top].

    :attr:`text_input_default_padding` is a
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
            self._text_input_min_width),
        bind=['size', '_text_input_padding', '_text_input_min_width'],
        cache=True)
    """The minimum width of the text field (read-only).

    This property calculates the minimum width required to accommodate
    the internal text input widget along with the defined padding.

    :attr:`minimum_width` is a :class:`~kivy.properties.AliasProperty`
    and is read-only."""
    
    minimum_height: float = AliasProperty(
        lambda self: (
            self._text_input_height),
        bind=['size', '_text_input_padding', '_text_input_height'],
        cache=True)
    """The minimum height of the text field (read-only).

    This property calculates the minimum height required to accommodate
    the internal text input widget along with the defined padding.
    
    :attr:`minimum_height` is a :class:`~kivy.properties.AliasProperty`
    and is read-only."""

    default_config = dict(
        theme_color_bindings=dict(
            normal_surface_color='surface_color',
            normal_border_color='outline_color',
            error_border_color='error_color',
            focus_border_color='primary_color',
            disabled_border_color='outline_variant_color',
            normal_content_color='content_surface_color',
            selected_text_color='secondary_color',),
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

        child_classes = dict(
            label_widget=MorphTextFieldLabel,
            supporting_widget=MorphTextFieldSupportingLabel,
            text_length_widget=MorphTextFieldTextLengthLabel,
            leading_widget=MorphTextFieldLeadingIconLabel,
            trailing_widget=MorphTextFieldTrailingIconButton,)
        config = clean_config(self.default_config, kwargs)
        for attr, cls in child_classes.items():
            if attr not in config:
                config[attr] = cls()

        super().__init__(**config)
        text_input_color_bindings = {
            prop: color 
            for prop, color in config.get('theme_color_bindings', {}).items()
            if 'content' in prop}
        self._text_input = MorphTextInput(
            theme_color_bindings=dict(
                normal_surface_color='transparent_color',
                **text_input_color_bindings),
            identity=NAME.INPUT,
            size_hint=(None, None),
            padding=dp(0),
            auto_height=True)
        
        self.add_widget(self._text_input)
        self._label_initial_color_bindings = (
            self.label_widget.theme_color_bindings.copy())
        self._label_initial_font_size = self.label_widget.font_size
        if self.selected_text_color is None:
            self.selected_text_color = self._text_input.selection_color

        bidirectional_binding = (
            'text',
            'focus',
            'disabled',
            'multiline',
            'password',)
        for prop in bidirectional_binding:
            self.fbind(prop, self._text_input.setter(prop))
            self._text_input.fbind(prop, self.setter(prop))
            setattr(self._text_input, prop, getattr(self, prop))

        self._text_input.bind(
            _lines=self._update_layout,
            padding=self._update_layout,
            height=self.setter('_text_input_height'),
            minimum_width=self.setter('_text_input_min_width'),)
        
        self.bind(
            pos=self._update_layout,
            size=self._update_layout,
            declarative_children=self._update_layout,
            focus=self._animate_on_focus,
            selected_text_color=self._update_selection_color,
            selected_text_color_opacity=self._update_selection_color,
            error_type=self._update_supporting_error_text,
            supporting_error_texts=self._update_supporting_error_text,
            current_content_state=self._update_children_states,
            minimum_height=self.setter('height'),
            maximum_height=self._text_input.setter('maximum_height'),)
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
        self.fbind(
            'max_text_length',
            self._update_text_length_widget,
            identity=NAME.TEXT_LENGTH_WIDGET)

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
        add_widget = bool(text)
        match identity:
            case NAME.LABEL_WIDGET:
                widget = self.label_widget
            case NAME.SUPPORTING_WIDGET:
                widget = self.supporting_widget
                add_widget = bool(self.supporting_error_texts)
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
        
        if add_widget and identity not in self.identities:
            widget.identity = identity
            self.add_widget(widget)
        elif not add_widget and identity in self.identities:
            self.remove_widget(widget)
        self._update_layout()
    
    def _update_text_length_widget(
            self, instance: Any, max_length: int, identity: str) -> None:
        """Update the text length widget based on the maximum length.

        This method sets the maximum length for the text length widget
        and updates its visibility based on the current content state.

        Parameters
        ----------
        instance : Any
            The instance of the widget being updated.
        max_length : int
            The maximum length to set for the text length widget.
        identity : str
            The identity of the child widget being updated.
        """
        if identity != NAME.TEXT_LENGTH_WIDGET or not self.text_length_widget:
            return

        show_length = max_length > 0
        if not show_length and identity in self.identities:
            self.remove_widget(self.text_length_widget)
        elif show_length and identity not in self.identities:
            self.text_length_widget.identity = identity
            self.add_widget(self.text_length_widget)

        self.text_length_widget.text = f'{len(self.text)}/{max_length}'
        self._update_layout()

    def _update_layout(self, *args) -> None:
        """Update the layout of the text field and its child widgets.

        This method recalculates the positions and sizes of the child
        widgets based on the current layout settings.
        """
        Animation.stop_all(self.label_widget)
        Animation.stop_all(self._text_input)
        Animation.stop_all(self)
        
        spacing = dp(4)
        x_input, y_input = self.pos
        w_input, h_input = self.size
        if NAME.LEADING_WIDGET in self.identities:
            self.leading_widget.x = self.x + self._horizontal_padding
            self.leading_widget.center_y = self.y + self.height / 2
            x_input = self.leading_widget.x + self.leading_widget.width
            w_input -= (x_input - self.x)

        if NAME.TRAILING_WIDGET in self.identities:
            self.trailing_widget.right = (
                self.x + self.width - self._horizontal_padding)
            self.trailing_widget.center_y = self.y + self.height / 2
            w_input -= (self.x + self.width - self.trailing_widget.x)

        if NAME.SUPPORTING_WIDGET in self.identities:
            self.supporting_widget.x = self.x + self._horizontal_padding
            self.supporting_widget.y = (
                self.y - self.supporting_widget.height - spacing)
            self.supporting_widget.maximum_width = (
                self.width - 2 * self._horizontal_padding)
        
        if NAME.TEXT_LENGTH_WIDGET in self.identities:
            self.text_length_widget.right = (
                self.x + self.width - self._horizontal_padding)
            self.text_length_widget.y = (
                    self.y - self.text_length_widget.height - spacing)
            if NAME.SUPPORTING_WIDGET in self.identities:
                self.supporting_widget.y = self.text_length_widget.y
                self.supporting_widget.maximum_width = (
                    self.width
                    - 2 * self._horizontal_padding
                    - self.text_length_widget.width
                    - spacing)

        self._text_input.pos = x_input, y_input
        self._text_input.padding = self._resolve_text_input_padding()
        self._text_input.width = max(self._text_input.minimum_width, w_input)
        self._text_input.height = max(self._text_input.minimum_height, h_input)

        self.width = max(self.width, self.minimum_width)
        self.height = max(self._text_input.height, self.minimum_height)

        if NAME.LABEL_WIDGET in self.identities:
            self.label_widget.font_size = self._resolve_label_font_size()
            self.label_widget.pos = self._resolve_label_position()
            self.border_open_x, self.border_open_length = (
                self._resolve_border_open_params())
        
    def refresh_textfield_content(self, *args) -> None:
        """Refresh the content of the text field and its child widgets.

        This method updates the text and icons of the child widgets
        by calling the _update_child_widget method for each widget.
        """
        self._text_input_height = self._text_input.height
        self._text_input_min_width = self._text_input.minimum_width

        self._update_text_length_widget(
            self, self.max_text_length, NAME.TEXT_LENGTH_WIDGET)
        self._update_supporting_error_text()

        self._update_child_widget(
            self, self.label_text, NAME.LABEL_WIDGET)
        self._update_child_widget(
            self, self.supporting_text, NAME.SUPPORTING_WIDGET)
        self._update_child_widget(
            self, self.leading_icon, NAME.LEADING_WIDGET)
        self._update_child_widget(
            self, self.trailing_icon, NAME.TRAILING_WIDGET)
    
        self._update_layout()
        self.validate(self.text)
        self._text_input.refresh_content()

    def _update_children_states(self, *args) -> None:
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
            for state in self.available_states:
                if hasattr(child, state):
                    child.setter(state)(self, getattr(self, state, False))

    def _resolve_label_position(self) -> Tuple[float, float]:
        """Get the position of the main label widget.

        Returns
        -------
        Tuple[float, float]
            The (x, y) position of the main label widget.
        """
        padding = self._resolve_text_input_padding()
        x = self._text_input.x + padding[0]
        y = self.y + self.height / 2 - self.label_widget.height / 2
        if not self.focus and not self.text:
            return (x, y)
        
        match self.label_focus_behavior:
            case 'hide':
                pass
            case 'move_above':
                x = self._text_input.x
                y = (
                self.y
                + self.height
                - padding[1]
                + dp(2))
            case 'float_to_border':
                x = max(
                    self.x + self._horizontal_padding,
                    self.x + self.clamped_radius[0])
                y = self.y + self.height - dp(8)
            
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

    def _resolve_border_open_params(self) -> Tuple[float | None, float]:
        """Get the open border segment parameters for the text field.

        The open border segment is used when the label floats over
        the border. It defines where the border should be open to
        accommodate the label.

        Returns
        -------
        Tuple[float | None, float]
            The (x, length) of the open border segment for the text field.
        """
        open_x = None
        open_length = 0.0
        if self.label_focus_behavior != 'float_to_border':
            pass
        
        elif self.focus or self.text:
            open_x = self._resolve_label_position()[0]
            open_length = (
                self.label_widget.width
                * self._label_size_factor)
        return open_x, open_length

    def _resolve_text_input_padding(self) -> List[float]:
        """Get the padding values for the internal text input widget.

        Returns
        -------
        List[float]
            The padding values [left, bottom, right, top] for the
            internal text input widget.
        """
        padding = self.text_input_default_padding.copy()
        if self.label_focus_behavior == 'move_above' and (self.focus or self.text):
            padding[1] = dp(24)
            padding[3] = dp(4)
        return padding

    def _animate_on_focus(self, *args) -> None:
        """Handle focus changes for the text field.

        This method animates the main label widget to a new position
        and font size when the text field gains or loses focus.
        """
        if NAME.LABEL_WIDGET not in self.identities:
            return

        Animation.cancel_all(self.label_widget)
        Animation.cancel_all(self._text_input)
        Animation.cancel_all(self)

        font_size = self._resolve_label_font_size()
        target_pos = self._resolve_label_position()

        self.border_width = dp(1.5) if self.focus else dp(1)

        if self.label_focus_behavior == 'hide':
            color_bindings = self._label_initial_color_bindings.copy()
            if self.focus or self.text:
                _colors = (k for k in color_bindings if 'content' in k)
                color_bindings.update(
                    {c: 'transparent_color' for c in _colors})
            self.label_widget.theme_color_bindings = color_bindings
            Animation(
                font_size=font_size,
                color=self.label_widget.get_resolved_content_color(),
                d=self.focus_animation_duration,
                t=self.focus_animation_transition,
            ).start(self.label_widget)
            return
        
        label_animation = Animation(
            x=target_pos[0],
            y=target_pos[1],
            font_size=font_size,
            d=self.focus_animation_duration,
            t=self.focus_animation_transition,)

        if self.label_focus_behavior == 'float_to_border':
            border_open_x, border_open_length = (
                self._resolve_border_open_params())
            self.border_open_x = border_open_x
            Animation(
                border_open_length=border_open_length,
                d=self.focus_animation_duration,
                t=self.focus_animation_transition
            ).start(self)
        elif self.label_focus_behavior == 'move_above':
            input_animation = Animation(
                padding=self._resolve_text_input_padding(),
                d=self.focus_animation_duration,
                t=self.focus_animation_transition)
            label_animation.bind(
                on_complete=lambda *args: input_animation.start(self._text_input))

        label_animation.start(self.label_widget)

    def _update_selection_color(self, instance: Any, color: List[float]) -> None:
        """Fired when the selected text color changes.

        This method ensures that the :attr:`selection_color` of the
        :attr:`_text_input` always has the correct opacity by combining
        the RGB values with the defined
        :attr:`selected_text_color_opacity`.

        Parameters
        ----------
        instance : Any
            The instance of the text field.
        color : List[float]
            The new RGBA color for text selection.
        """
        selection_color = color[:3] + [self.selected_text_color_opacity]
        self._text_input.selection_color = selection_color
    
    def _update_supporting_error_text(self, *args) -> None:
        """Update the supporting text based on the error type.

        This method sets the :attr:`supporting_text` property of the
        text field based on the current error type. If there is an
        error type and a corresponding message in
        :attr:`supporting_error_texts`, it updates the supporting text
        accordingly.
        """
        if not self.supporting_error_texts:
            return
        
        error_text = self.supporting_error_texts.get(self.error_type, '')
        self.supporting_text = error_text

    def on_text(self, instance: Any, text: str) -> None:
        """Fired when the text content changes.

        This method updates the text length widget to reflect the
        current length of the text input.

        Parameters
        ----------
        instance : Any
            The instance of the text field.
        text : str
            The new text content of the text field.
        """
        self.validate(text)
        self._update_text_length_widget(
            self, self.max_text_length, NAME.TEXT_LENGTH_WIDGET)


class MorphTextFieldOutlined(
        MorphTextField,):
    """A MorphTextField with outlined style.

    This class provides an outlined appearance for the text field,
    adhering to Material Design guidelines.
    """

    default_config: Dict[str, Any] = (
        MorphTextField.default_config.copy() | dict(
            label_focus_behavior='float_to_border',
            border_bottom_line_only=False,
            multiline=False,
            radius=[2, 2, 2, 2],))


class MorphTextFieldRounded(
        MorphRoundSidesBehavior,
        MorphTextField,):
    """A MorphTextField with rounded sides and elevation behavior.

    This class combines the features of MorphTextField with rounded
    sides and elevation behavior for enhanced visual appearance.
    """

    default_config: Dict[str, Any] = (
        MorphTextField.default_config.copy() | dict(
            label_focus_behavior='hide',
            round_sides=True,
            elevation=1,))


class MorphTextFieldFilled(
        MorphTextField,):
    """A MorphTextField with filled style.

    This class provides a filled appearance for the text field,
    adhering to Material Design guidelines.
    """

    default_config: Dict[str, Any] = (
        MorphTextField.default_config.copy() | dict(            
            label_focus_behavior='move_above',
            border_bottom_line_only=True,
            text_input_default_padding=[8, 8, 18, 18],
            multiline=False,
            radius=[16, 16, 0, 0],))