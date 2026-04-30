"""
Text field widgets for MorphUI.

This module provides single-line text input components with built-in
validation, error state display, leading icon support, trailing icon
button support, heading labels, and supporting text. Three visual
styles are available: filled, outlined, and rounded.

Classes
-------
MorphTextValidator
    Standalone validator that tracks error state and type.
MorphTextInput
    Internal ``TextInput`` subclass with MorphUI theming.
MorphTextField
    Filled text field (default style).
MorphTextFieldFilled
    Explicit alias for the filled style.
MorphTextFieldOutlined
    Outlined border style.
MorphTextFieldRounded
    Fully rounded border style.
"""
from typing import Any
from typing import Dict
from typing import List
from typing import Tuple
from typing import Literal

from kivy.clock import Clock
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
from kivy.properties import OptionProperty
from kivy.properties import BooleanProperty
from kivy.properties import NumericProperty
from kivy.properties import VariableListProperty
from kivy.uix.textinput import TextInput

from morphui.utils import clamp

from morphui.uix.behaviors import MorphThemeBehavior
from morphui.uix.behaviors import MorphHoverBehavior
from morphui.uix.behaviors import MorphSizeBoundsBehavior
from morphui.uix.behaviors import MorphAutoSizingBehavior
from morphui.uix.behaviors import MorphTypographyBehavior
from morphui.uix.behaviors import MorphRoundSidesBehavior
from morphui.uix.behaviors import MorphTripleLabelBehavior
from morphui.uix.behaviors import MorphSurfaceLayerBehavior
from morphui.uix.behaviors import MorphContentLayerBehavior
from morphui.uix.behaviors import MorphLeadingWidgetBehavior
from morphui.uix.behaviors import MorphTrailingWidgetBehavior
from morphui.uix.behaviors import MorphDelegatedThemeBehavior
from morphui.uix.behaviors import MorphIdentificationBehavior
from morphui.uix.behaviors import MorphInteractionLayerBehavior

from morphui.uix.floatlayout import MorphFloatLayout

from morphui.uix.label import MorphTextFieldHeadingLabel
from morphui.uix.label import MorphTextFieldTertiaryLabel
from morphui.uix.label import MorphTextFieldSupportingLabel
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


NO_ERROR: Literal['none'] = 'none'
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
            'email', 'phone', 'date', 'time', 'datetime', 'daterange', 
            'numeric', 'alphanumeric'])
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
    - 'daterange': Validates that the text is a valid date range. Where
      the separator is a hyphen (-) and the format is any of the
      supported date formats for each date, e.g.,
      'YYYY-MM-DD - YYYY-MM-DD'. For more information, see
      :meth:`is_valid_daterange`.
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
        The supported formats are:
        - European format: 'DD/MM/YYYY' or 'DD-MM-YYYY'
        - ISO format: 'YYYY-MM-DD'
        - US format: 'MM/DD/YYYY' or 'MM-DD-YYYY'

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
    
    def is_valid_daterange(self, text: str) -> bool:
        """Check if the given text is a valid date range.

        Splits the text into two date components using a hyphen (-) as
        the separator. Then checks if both parts are valid dates. The
        format is expected to be 'YYYY-MM-DD - YYYY-MM-DD'. But other
        date formats are also supported for each date. For more
        information, see :meth:`is_valid_date`.

        Parameters
        ----------
        text : str
            The text input to validate.

        Returns
        -------
        bool
            True if the input is a valid date range, False otherwise.
        """
        if ' - ' not in text:
            return False
        start_date, end_date = map(str.strip, text.split(' - ', 1))
        return self.is_valid_date(start_date) and self.is_valid_date(end_date)

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

    maximum_height: float = NumericProperty(dp(300))
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

    default_config: Dict[str, Any] = dict(
        theme_color_bindings={
            'cursor_color': 'secondary_color',}) # TODO: not working yet

    def __init__(self, **kwargs) -> None:
        config = self.default_config.copy() | kwargs
        super().__init__(**config)

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
        MorphDelegatedThemeBehavior,
        MorphLeadingWidgetBehavior,
        MorphTripleLabelBehavior,
        MorphTrailingWidgetBehavior,
        MorphTypographyBehavior,
        MorphContentLayerBehavior,
        MorphInteractionLayerBehavior,
        MorphFloatLayout,):
    """A versatile text field widget with validation, theming, and 
    flexible layout. Designed for various text input scenarios, it 
    supports single-line and multi-line input, password fields, and 
    real-time validation.

    It consists of an internal :class:`MorphTextInput` for handling text 
    input and additional widgets for labels, supporting text, and icons.
    These child widgets are managed internally and can be customized or
    replaced as needed. The main child widgets include:
    - :attr:`heading_widget`: Internal widget for the main label of the 
      text field. It displays the primary label that describes the 
      purpose of the text field.
    - :attr:`supporting_widget`: Displays supporting text for the 
      text field. This is typically used to show error messages or 
      additional information.
    - :attr:`tertiary_widget`: Displays the current text length and
      character count for the text field.
    - :attr:`leading_icon_widget`: Displays a leading icon for the text 
      field. This icon is positioned at the start of the text field and 
      can be used to indicate the purpose of the text field or provide
      visual context.
    - :attr:`trailing_icon_widget`: Displays a trailing icon for the
      text field. This icon is positioned at the end of the text field 
      and can be used to indicate additional actions or provide visual
      context.
    """

    text: str = StringProperty('')
    """The text content of the text field.

    This property holds the current text entered in the text field. It
    can be accessed and modified programmatically to get or set the
    text value. It is bound bidirectionally to the text property of the
    internal :class:`MorphTextInput`.

    :attr:`text` is a :class:`~kivy.properties.StringProperty` and 
    defaults to ''.
    """
    
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

    spacing: List[float] = VariableListProperty([dp(4), dp(4)], length=2)
    """The spacing between the child widgets.
    
    This property defines the amount of space (in pixels) between the
    child widgets within the text field, such as the heading, supporting
    and text input widgets. It helps to maintain a visually appealing
    layout by providing consistent spacing. The spacing is defined as 
    [horizontal_spacing, vertical_spacing].
    
    :attr:`spacing` is a :class:`~kivy.properties.VariableListProperty`
    and defaults to [dp(4), dp(4)]."""

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

    heading_focus_behavior: str = OptionProperty(
        'float_to_border',
        options=['hide', 'float_to_border', 'move_above'])
    """Controls how the heading widget behaves when the text field gains 
    focus.

    This property determines the animation and positioning behavior of 
    the heading widget during focus transitions:

    - 'hide': The heading disappears when the text field is focused
    - 'float_to_border': The heading moves up and floats over the border 
    (current Material Design implementation)
    - 'move_above': The heading moves completely above the input area, 
    pushing the input field down slightly

    :attr:`heading_focus_behavior` is a 
    :class:`~kivy.properties.OptionProperty` and defaults to 
    'float_to_border'."""

    padding: List[float] = VariableListProperty(
        [dp(4), dp(4), dp(4), dp(4)], length=4)
    """The padding values around the text field content.

    This property defines the padding space that is applied around the
    content of the text field. The padding is defined as
    [left, top, right, bottom].

    :attr:`padding` is a :class:`~kivy.properties.VariableListProperty`
    of length 4 and defaults to [dp(4), dp(4), dp(4), dp(4)]."""

    input_widget_padding: List[float] = VariableListProperty(
        [dp(4), dp(4), dp(4), dp(4)], length=4)
    """The padding values around the internal input widget.

    This property defines the base padding space that is applied around
    the internal :class:`MorphTextInput` widget before any adjustments
    for icons or other widgets. The padding is defined as
    [left, top, right, bottom].

    :attr:`input_widget_padding` is a
    :class:`~kivy.properties.VariableListProperty` of length 4 and
    defaults to [dp(4), dp(4), dp(4), dp(4)]."""

    def _get_input_margin(self) -> Tuple[float, float, float, float]:
        """Calculate the margin values for the internal input widget.

        This method computes the margin space that should be applied
        around the internal input widget (e.g. TextInput) based on the
        presence of leading and trailing widgets. It adjusts the base
        padding accordingly to ensure proper spacing and alignment of 
        the input widget within the text field.

        Returns
        -------
        Tuple[float, float, float, float]
            The calculated margin values as (left, top, right, bottom).
        """
        left, top, right, bottom = self.padding

        if self.shows_leading_icon:
            left += self.leading_widget.width + self.spacing[0]

        if self.shows_trailing_icon:
            right += self.trailing_widget.width + self.spacing[0]

        if self.heading_focus_behavior == 'move_above' and self.engaged:
            top += bottom
            bottom = 0
        
        return (left, top, right, bottom)

    input_margin: Tuple[float, float, float, float] = AliasProperty(
        _get_input_margin,
        None,
        bind=[
            'shows_leading_icon',
            'shows_trailing_icon',
            'padding',
            'spacing',
            'heading_focus_behavior',
            'engaged',])
    """The margin values applied to the internal input widget
    (read-only).

    This property defines the margin space that is applied around
    the internal input widget (e.g. TextInput for TextField or other 
    input widgets). This margin is required for positioning the internal 
    widgets correctly. It means that this margin is the space needed 
    between input widget and outer frame. So that when we calculate the 
    position of the input widget, we can use this margin to determine 
    how much space to leave around it for positioning the other widgets.
    The margin is defined as (left, top, right, bottom)

    :attr:`input_margin` is a
    :class:`~kivy.properties.AliasProperty` and defaults to 
    (dp(4), dp(4), dp(4), dp(4))."""

    _input_min_width: float = NumericProperty(dp(0))
    """The current minimum width of the internal input widget.

    This property is used for layout calculations and reflects the
    current minimum width of the internal input widget.

    :attr:`_input_min_width` is a
    :class:`~kivy.properties.NumericProperty`."""

    _input_height: float = NumericProperty(dp(0))
    """The current height of the internal input widget.

    This property is used for layout calculations and reflects the
    current height of the internal input widget.

    :attr:`_input_height` is a
    :class:`~kivy.properties.NumericProperty`."""

    def _get_minimum_width(self) -> float:
        """Calculate the minimum width required for the text field.

        This method computes the minimum width needed to accommodate the
        internal text input widget along with the defined padding and any
        leading or trailing widgets. It takes into account the presence
        of these widgets and adjusts the padding accordingly.

        Returns
        -------
        float
            The calculated minimum width for the text field.
        """
        minimum_width = (
            self._input_min_width
            + self.input_margin[0]
            + self.input_margin[2])
        return minimum_width

    minimum_width: float = AliasProperty(
        _get_minimum_width,
        None,
        bind=[
            'input_margin',
            '_input_min_width'],)
    """The minimum width of the text field (read-only).

    This property calculates the minimum width required to accommodate
    the internal text input widget along with the defined padding.

    :attr:`minimum_width` is a :class:`~kivy.properties.AliasProperty`
    and is read-only."""

    def _get_minimum_height(self) -> float:
        """Calculate the minimum height required for the text field.

        This method computes the minimum height needed to accommodate the
        internal text input widget along with the defined padding and any
        heading or supporting widgets. It takes into account the presence
        of these widgets and adjusts the padding accordingly.

        Returns
        -------
        float
            The calculated minimum height for the text field.
        """
        minimum_height = (
            self._input_height
            + self.input_margin[1]
            + self.input_margin[3])
        return minimum_height
    
    minimum_height: float = AliasProperty(
        _get_minimum_height,
        None,
        bind=[
            'input_margin',
            '_input_height'],
        cache=True)
    """The minimum height of the text field (read-only).

    This property calculates the minimum height required to accommodate
    the internal text input widget along with the defined padding.
    
    :attr:`minimum_height` is a :class:`~kivy.properties.AliasProperty`
    and is read-only."""

    engaged: bool = AliasProperty(
        lambda self: self.focus or bool(self.text),
        None,
        bind=[
            'focus',
            'text'],
        cache=True)
    """Whether the text field is active — focused or has content (read-only).

    Used to drive heading animation, border state, and padding transitions.
    Override in subclasses to add further conditions, e.g. a date picker
    that treats a selected date as active even without typed text.

    :attr:`is_active` is a :class:`~kivy.properties.AliasProperty`
    bound to `focus` and `text`."""

    content_bbox: List[float] = AliasProperty(
        lambda self: [
            self.x + self.padding[0],
            self.y + self.height - self.padding[1],
            self.x + self.width - self.padding[2],
            self.y + self.padding[3]],
        None,
        bind=[
            'pos',
            'size',
            'padding'])
    """The bounding box of the content area (read-only).

    This property calculates the bounding box of the content area
    based on the text field's position, size, and padding.

    :attr:`content_bbox` is a :class:`~kivy.properties.AliasProperty`
    and is read-only."""

    input_bbox: List[float] = AliasProperty(
        lambda self: [
            self.x + self.input_margin[0],
            self.y + self.height - self.input_margin[1],
            self.x + self.width - self.input_margin[2],
            self.y + self.input_margin[3]],
        None,
        bind=[
            'pos',
            'size',
            'input_margin'])
    """The bounding box of the internal input widget (read-only).

    This property calculates the bounding box of the internal input 
    widget based on the text field's position, size, and input margins.

    :attr:`input_bbox` is a :class:`~kivy.properties.AliasProperty`
    and is read-only."""

    default_config = dict(
        theme_color_bindings=dict(
            normal_surface_color='surface_color',
            normal_border_color='outline_color',
            error_border_color='error_color',
            focus_border_color='primary_color',
            disabled_border_color='outline_variant_color',
            normal_content_color='content_surface_color',
            error_content_color='error_color',
            disabled_content_color='outline_variant_color',
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

    _heading_initial_font_size: float = sp(1)
    """Stores the initial font size of the heading widget for
    restoration after focus changes."""

    _heading_size_factor: float = 1.0
    """Stores the size factor of the heading widget for scaling purposes."""

    @property
    def input_widget(self) -> MorphTextInput:
        """The internal text input widget (read-only).

        This property provides access to the internal :class:`MorphTextInput`
        widget that is used for handling user input. It allows external
        code to interact with the text input widget directly if needed.
        Internal it is used to bind properties for bidirectional updates 
        and to set properties like padding and maximum height.

        Returns
        -------
        MorphTextInput
            The internal text input widget.
        """
        return self._text_input

    def __init__(self, **kwargs) -> None:
        child_widgets = dict(
            heading_widget=MorphTextFieldHeadingLabel,
            supporting_widget=MorphTextFieldSupportingLabel,
            tertiary_widget=MorphTextFieldTertiaryLabel,
            leading_widget=MorphTextFieldLeadingIconLabel,
            trailing_widget=MorphTextFieldTrailingIconButton,)
        config = (
            self.default_config.copy()
            | {k: v() for k, v in child_widgets.items()  if k not in kwargs}
            | kwargs)
        _bindings = config.get('theme_color_bindings') or {}
        color_bindings = {p: c  for p, c in _bindings.items() if 'content' in p}
        self._text_input = MorphTextInput(
            theme_color_bindings=dict(
                normal_surface_color='transparent_color',
                **color_bindings),
            size_hint=(None, None),
            auto_height=True)
        super().__init__(**config)
        self._heading_initial_font_size = self.heading_widget.font_size
        self.selected_text_color = (
            self.selected_text_color or self._text_input.selection_color)

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
            _lines=self._update_layout,)
        
        self.input_widget.bind(
            padding=self._update_layout,
            height=self.setter('_input_height'),
            minimum_width=self.setter('_input_min_width'),)
        
        self.bind(
            size=self._update_layout,
            pos=self._update_layout,
            padding=self._update_layout,
            spacing=self._update_layout,
            engaged=self._trigger_validation,
            focus=lambda *args: Clock.schedule_once(self._animate_on_focus),
            selected_text_color=self._update_selection_color,
            selected_text_color_opacity=self._update_selection_color,
            error_type=self._update_supporting_error_text,
            supporting_error_texts=self._update_supporting_error_text,
            minimum_height=self.setter('height'),
            maximum_height=self.input_widget.setter('maximum_height'),
            input_widget_padding=self.input_widget.setter('padding'),)

        self._add_widgets_to_layout()
        self.refresh_textfield_content()

    def _add_widgets_to_layout(self) -> None:
        """Add child widgets to the layout in the correct order.

        This method ensures that the child widgets are added to the 
        layout in the correct order. The order is important for proper 
        layering and visual appearance.
        """
        self.clear_widgets()
        children = (
            self.leading_widget,
            self.heading_widget,
            self.tertiary_widget,
            self.supporting_widget,
            self.trailing_widget,)
        self.delegated_children = [c for c in children if c is not None]
        for child in self.delegated_children:
            self.add_widget(child)

        self.add_widget(self.input_widget)
        
    def _update_tertiary_text(self, instance: Any, max_length: int) -> None:
        """Update the tertiary text based on the maximum length.

        This method sets the maximum length for the tertiary widget
        and updates its visibility based on the current content state.

        Parameters
        ----------
        instance : Any
            The instance of the widget being updated.
        max_length : int
            The maximum length to set for the tertiary widget.
        """
        if self.tertiary_widget is None:
            return

        if max_length > 0:
            self.tertiary_text = f'{len(self.text)}/{max_length}'
        else:
            self.tertiary_text = ''
        self._update_layout()

    def _update_layout(self, *args) -> None:
        """Update the layout of the text field and its child widgets.

        This method recalculates the positions and sizes of the child
        widgets based on the current layout settings.

        Notes
        -----
        If width or height is non-positive, the method exits early to 
        avoid layout issues. This occurs when the widget is not yet 
        fully initialized or visible (by ScreenManager).

        This method stops any ongoing animations on the child widgets
        before updating their positions and sizes to ensure smooth
        transitions. 
        """
        if self.size[0] <= 0 or self.size[1] <= 0: # ScreenManager issue when widget was not visible yet.
            return
        
        Animation.stop_all(self.heading_widget)
        Animation.stop_all(self.input_widget)
        Animation.stop_all(self)

        h_padding = self.padding[0] + self.padding[2]
        
        if self.shows_leading_icon:
            self.leading_widget.x = self.content_bbox[0]

        if self.shows_trailing_icon:
            self.trailing_widget.right = self.content_bbox[2]

        if self.shows_supporting:
            self.supporting_widget.x = self.content_bbox[0]
            self.supporting_widget.top = self.y - self.spacing[1]
            _w_max = self.width - h_padding
            if self.shows_tertiary:
                _w_max -= (self.tertiary_widget.width + self.spacing[0])
            self.supporting_widget.maximum_width = _w_max
        
        if self.shows_tertiary:
            self.tertiary_widget.right = self.content_bbox[2]
            self.tertiary_widget.top = self.y - self.spacing[1]

        self.input_widget.pos = self.input_bbox[0], self.input_bbox[3]
        self.input_widget.width = max(
            self.input_bbox[2] - self.input_bbox[0],
            self.input_widget.minimum_width,)
        self.input_widget.height = max(
            self.input_bbox[1] - self.input_bbox[3],
            self.input_widget.minimum_height,)

        self.width = max(self.width, self.minimum_width)

        if self.shows_heading:
            self.heading_widget.font_size = self._resolve_heading_font_size()
            self.heading_widget.pos = self._resolve_heading_position()
            self.border_open_x, self.border_open_length = (
                self._resolve_border_open_params())
        
    def refresh_textfield_content(self, *args) -> None:
        """Refresh the content of the text field and its child widgets.

        This method updates the text and icons of the child widgets
        by calling the _update_child_widget method for each widget.
        """
        self._update_supporting_error_text()
        self._update_layout()

        self.validate(self.text)
        self.refresh_leading_widget()
        self.refresh_trailing_widget()
        self.refresh_triple_labels()
        
        def _input_widget_updates(*args) -> None:
            self._input_height = self.input_widget.height
            self._input_min_width = self.input_widget.minimum_width
            self.input_widget.maximum_height = self.maximum_height
            self.input_widget.padding = self.input_widget_padding
            self.input_widget.refresh_content()
        Clock.schedule_once(_input_widget_updates)

    def _resolve_heading_position(self) -> Tuple[float, float]:
        """Get the position of the heading widget.

        Returns
        -------
        Tuple[float, float]
            The (x, y) position of the heading widget.
        """
        x = self.input_widget.x + self.input_widget_padding[0]
        y = self.y + self.height / 2 - self.heading_widget.height / 2
        if self.engaged:
            match self.heading_focus_behavior:
                case 'hide':
                    x = x
                    y = y
                case 'move_above':
                    x = self.input_widget.x
                    y = (
                    self.y
                    + self.input_widget.height
                    - self.input_widget_padding[1]
                    + self.spacing[1])
                case 'float_to_border':
                    x = max(
                        self.x + self.padding[0],
                        self.x + self.clamped_radius[0])
                    y = self.y + self.height - dp(8)
            
        return (x, y)
    
    def _resolve_heading_font_size(self) -> float:
        """Get the font size for the heading widget.

        Returns
        -------
        float
            The font size for the heading widget.
        """
        if self.engaged:
            if self.heading_focus_behavior == 'hide':
                return 0
            
            font_size = self.typography.get_font_size(
                role=self.heading_widget.typography_role,
                size='small')
        else:
            font_size = self._heading_initial_font_size

        if isinstance(font_size, str):
            font_size = sp(int(font_size.replace('sp', '')))
        self._heading_size_factor = font_size / self._heading_initial_font_size
        return font_size

    def _resolve_border_open_params(self) -> Tuple[float | None, float]:
        """Get the open border segment parameters for the text field.

        The open border segment is used when the heading floats over
        the border. It defines where the border should be open to
        accommodate the heading.

        Returns
        -------
        Tuple[float | None, float]
            The (x, length) of the open border segment for the text field.
        """
        open_x = None
        open_length = 0.0
        if self.heading_focus_behavior != 'float_to_border':
            pass
        
        elif self.engaged:
            open_x = self._resolve_heading_position()[0]
            open_length = (
                self.heading_widget.width
                * self._heading_size_factor)
        return open_x, open_length

    def _animate_on_focus(self, *args) -> None:
        """Handle focus changes for the text field.

        This method animates the heading widget to a new position
        and font size when the text field gains or loses focus.
        """
        if self.heading_widget is None:
            return

        Animation.cancel_all(self.heading_widget)
        Animation.cancel_all(self.input_widget)
        Animation.cancel_all(self)

        font_size = self._resolve_heading_font_size()
        target_pos = self._resolve_heading_position()

        self.border_width = dp(1.5) if self.focus else dp(1)

        if self.heading_focus_behavior == 'hide':
            heading_animation = Animation(
                font_size=font_size,
                duration=self.focus_animation_duration,
                transition=self.focus_animation_transition,)
            if self.heading_widget.parent is None:
                self.add_widget(self.heading_widget)
                self.heading_widget.font_size = 0
            else:
                heading_animation.bind(
                    on_complete=(
                        lambda *args: self.remove_widget(self.heading_widget)))
        else:
            heading_animation = Animation(
                x=target_pos[0],
                y=target_pos[1],
                font_size=font_size,
                duration=self.focus_animation_duration,
                transition=self.focus_animation_transition,)

        if self.heading_focus_behavior == 'float_to_border':
            border_open_x, border_open_length = (
                self._resolve_border_open_params())
            self.border_open_x = border_open_x
            Animation(
                border_open_length=border_open_length,
                duration=self.focus_animation_duration,
                transition=self.focus_animation_transition
            ).start(self)
        elif self.heading_focus_behavior == 'move_above':
            input_animation = Animation(
                padding=self.input_widget_padding,
                duration=self.focus_animation_duration,
                transition=self.focus_animation_transition)
            heading_animation.bind(
                on_complete=lambda *args: input_animation.start(self.input_widget))

        heading_animation.start(self.heading_widget)

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

    def _trigger_validation(self, *args) -> None:
        """Trigger validation of the text field content.

        This method is called when the text field becomes engaged 
        (focused). It triggers the validation of the text field content 
        by calling the :attr:`validate` method with the current text. It
        also updates the tertiary text based on the maximum text length.
        """
        self.validate(self._text_input.text)
        self._update_tertiary_text(self, self.max_text_length)


class MorphTextFieldOutlined(
        MorphTextField,):
    """A MorphTextField with outlined style.

    This class provides an outlined appearance for the text field,
    adhering to Material Design guidelines.
    """

    default_config: Dict[str, Any] = (
        MorphTextField.default_config.copy() | dict(
            heading_focus_behavior='float_to_border',
            border_bottom_line_only=False,
            multiline=False,
            radius=[dp(4), dp(4), dp(4), dp(4)],))


class MorphTextFieldRounded(
        MorphRoundSidesBehavior,
        MorphTextField,):
    """A MorphTextField with rounded sides and elevation behavior.

    This class combines the features of MorphTextField with rounded
    sides and elevation behavior for enhanced visual appearance.
    """

    default_config: Dict[str, Any] = (
        MorphTextField.default_config.copy() | dict(
            heading_focus_behavior='hide',
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
            heading_focus_behavior='move_above',
            border_bottom_line_only=True,
            input_widget_padding=[dp(8), dp(8), dp(18), dp(18)],
            multiline=False,
            radius=[dp(16), dp(16), 0, 0],))
