from kivy.event import EventDispatcher
from kivy.graphics import Color
from kivy.graphics import SmoothLine
from kivy.graphics import RoundedRectangle
from kivy.properties import ColorProperty
from kivy.properties import NumericProperty
from kivy.properties import BooleanProperty
from kivy.properties import VariableListProperty
from kivy.uix.relativelayout import RelativeLayout


__all__ = [
    'MorphBackgroundBehavior',]


class MorphBackgroundBehavior(EventDispatcher):
    """A behavior class that provides background and border styling 
    capabilities.

    This behavior adds background color, border color, border width, and 
    corner radius properties to widgets. It automatically manages the 
    canvas graphics instructions to render a rounded rectangle 
    background with optional border.
    """

    radius = VariableListProperty([0], length=4)
    """Canvas radius for each corner.
    
    The order of the corners is: top-left, top-right, bottom-right, 
    bottom-left.
    
    :attr:`radius` is a :class:`~kivy.properties.VariableListProperty`
    and defaults to `[0, 0, 0, 0]`."""

    background_color: ColorProperty = ColorProperty()
    """Background color of the widget.
    
    The color should be provided as a list of RGBA values between 0 and 
    1. Example: `[1, 0, 0, 1]` for solid red.
    
    :attr:`background_color` is a :class:`~kivy.properties.ColorProperty`
    and defaults to `[1, 1, 1, 1]` (white)."""

    disabled_background_color: ColorProperty = ColorProperty([0, 0, 0, 0])
    """Background color when the widget is disabled.

    This color is applied when the widget is in a disabled state.
    It should be a fully transparent color if you are using state layer.
    Otherwise, it can be set to any RGBA color.

    :attr:`disabled_background_color` is a
    :class:`~kivy.properties.ColorProperty` and defaults to 
    `[0, 0, 0, 0]` (transparent)."""

    border_color: ColorProperty = ColorProperty([0, 0, 0, 0])
    """Border color of the widget.
    
    The color should be provided as a list of RGBA values between 0 and 
    1. Example: `[0, 1, 0, 1]` for solid green.

    :attr:`border_color` is a :class:`~kivy.properties.ColorProperty`
    and defaults to `[0, 0, 0, 0]` (transparent)."""

    disabled_background_color: ColorProperty = ColorProperty([0, 0, 0, 0])
    """Background color when the widget is disabled.

    This color is applied when the widget is in a disabled state.
    It should be a fully transparent color if you are using state layer.
    Otherwise, it can be set to any RGBA color.

    :attr:`disabled_background_color` is a 
    :class:`~kivy.properties.ColorProperty` and defaults to 
    `[0, 0, 0, 0]` (transparent)."""

    border_width: float = NumericProperty(1, min=0.01)
    """Width of the border.

    The width is specified in pixels.
    
    :attr:`border_width` is a :class:`~kivy.properties.NumericProperty`
    and defaults to `1` (1 pixel wide).
    """

    disabled: bool = BooleanProperty(False)
    """Whether the widget is disabled.

    When `True`, the `disabled_background_color` is used for the 
    background and border colors. Changing the background or border
    colors while disabled will have no effect until `disabled` is set
    to `False`.

    :attr:`disabled` is a :class:`~kivy.properties.BooleanProperty`
    and defaults to `False`.
    """

    _background_color_instruction: Color
    """Kivy Color instruction for the background color."""

    _background_instruction: RoundedRectangle
    """Kivy RoundedRectangle instruction for the background shape."""

    _border_color_instruction: Color
    """Kivy Color instruction for the border color."""

    _border_instruction: SmoothLine
    """Kivy SmoothLine instruction for the border."""

    def __init__(self, **kwargs) -> None:
        """Initialize the background behavior with canvas graphics 
        instructions.
        
        Parameters
        ----------
        **kwargs
            Additional keyword arguments passed to the parent class.
        """
        self.register_event_type('on_background_update')
        super().__init__(**kwargs)
        self.bind(
            background_color=self._update_background,
            size=self._update_background,
            pos=self._update_background,
            radius=self._update_background,
            border_color=self._update_background,
            border_width=self._update_background,
            disabled=self._update_background,)
        
        with self.canvas.before:
            self._background_color_instruction = Color(*self.background_color)
            self._background_instruction = RoundedRectangle(
                size=self.size,
                pos=self.pos,
                radius=self.radius)
            self._border_color_instruction = Color(*self.border_color)
            self._border_instruction = SmoothLine(
                width=self.border_width,
                rounded_rectangle=self._rounded_rectangle)
    
    @property
    def _rounded_rectangle(self) -> RoundedRectangle:
        """Get the parameters for creating a rounded rectangle (read-only).
        
        Returns
        -------
        list of float
            List containing [x, y, width, height, *radius] for the 
            rounded rectangle.
        """
        is_relative = isinstance(self, RelativeLayout)
        return [
            0 if is_relative else self.x,
            0 if is_relative else self.y,
            self.width,
            self.height,
            *self.radius,]
    
    def _update_background(self, *args) -> None:
        """Update the background when any relevant property changes."""
        if self.disabled:
            background_color = self.disabled_background_color
            border_color = self.disabled_background_color
        else:
            background_color = self.background_color
            border_color = self.border_color

        self._background_color_instruction.rgba = background_color
        self._background_instruction.pos = self.pos
        self._background_instruction.size = self.size
        self._background_instruction.radius = self.radius
        
        self._border_color_instruction.rgba = border_color
        self._border_instruction.width = self.border_width
        self._border_instruction.rounded_rectangle = self._rounded_rectangle

        self.dispatch('on_background_update')

    def on_background_update(self, *args) -> None:
        """Event dispatched when the background is updated.
        
        This can be overridden by subclasses to perform additional
        actions when the background changes."""
        pass
