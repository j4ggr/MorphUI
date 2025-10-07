from typing import Any
from typing import List

from kivy.event import EventDispatcher
from kivy.graphics import Color
from kivy.graphics import SmoothLine
from kivy.graphics import RoundedRectangle
from kivy.properties import ColorProperty
from kivy.properties import NumericProperty
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

    border_color: ColorProperty = ColorProperty([0, 0, 0, 0])
    """Border color of the widget.
    
    The color should be provided as a list of RGBA values between 0 and 
    1. Example: `[0, 1, 0, 1]` for solid green.

    :attr:`border_color` is a :class:`~kivy.properties.ColorProperty`
    and defaults to `[0, 0, 0, 0]` (transparent)."""

    border_width: float = NumericProperty(0)
    """Width of the border.

    The width is specified in pixels.
    
    :attr:`border_width` is a :class:`~kivy.properties.NumericProperty`
    and defaults to `0` (no border).
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
        super().__init__(**kwargs)
        self.bind(
            background_color=self._update_background_color,
            size=self._update_size,
            pos=self._update_position,
            radius=self._update_radius,
            border_color=self._update_border_color,
            border_width=self._update_border_width,)
        
        with self.canvas.before:
            self._background_color_instruction = Color(*self.background_color)
            self._background_instruction = RoundedRectangle(
                size=self.size, pos=self.pos, radius=self.radius)
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

    def _ensure_alpha(self, color: List[float]) -> List[float]:
        """Ensure the color has an alpha channel.
        
        Parameters
        ----------
        color : list of float
            Color list with RGB or RGBA values.
            
        Returns
        -------
        list of float
            Color list with RGBA values (alpha defaults to 1 if not provided).
        """
        if len(color) == 3:
            color = [*color, 1]
        return color

    def _update_background_color(
            self, instance: Any, color: List[float]):
        """Update the background color when the property changes.
        
        Parameters
        ----------
        instance : Any
            The widget instance.
        color : list of float
            New background color values.
        """
        self._background_color_instruction.rgba = self._ensure_alpha(color)
    
    def _update_border_color(
            self, instance: Any, color: List[float]):
        """Update the border color when the property changes.
        
        Parameters
        ----------
        instance : Any
            The widget instance.
        color : list of float
            New border color values.
        """
        self._border_color_instruction.rgba = self._ensure_alpha(color)

    def _update_border_width(
            self, instance: Any, width: float):
        """Update the border width when the property changes.
        
        Parameters
        ----------
        instance : Any
            The widget instance.
        width : float
            New border width.
        """
        self._border_instruction.width = width

    def _update_size(self, instance: Any, size: List[float]):
        """Update the background and border when the widget size changes.
        
        Parameters
        ----------
        instance : Any
            The widget instance.
        size : list of float
            New size values [width, height].
        """
        self._background_instruction.size = size
        self._border_instruction.rounded_rectangle = self._rounded_rectangle

    def _update_position(self, instance: Any, pos: List[float]):
        """Update the background and border when the widget position changes.
        
        Parameters
        ----------
        instance : Any
            The widget instance.
        pos : list of float
            New position values [x, y].
        """
        self._background_instruction.pos = pos
        self._border_instruction.rounded_rectangle = self._rounded_rectangle

    def _update_radius(self, instance: Any, radius: List[float]):
        """Update the background and border when the radius changes.
        
        Parameters
        ----------
        instance : Any
            The widget instance.
        radius : list of float
            New radius values [top_left, top_right, bottom_right, bottom_left].
        """
        self._background_instruction.radius = radius
        self._border_instruction.rounded_rectangle = self._rounded_rectangle