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
    
    Parameters
    ----------
    radius : list of float
        Corner radii in order:
        [top_left, top_right, bottom_right, bottom_left].
        Defaults to [0, 0, 0, 0]."""

    background_color: ColorProperty = ColorProperty()
    """Background color of the widget.
    
    Parameters
    ----------
    background_color : list of float
        RGBA color values for the background. Defaults to [1, 1, 1, 1]."""

    border_line_color: ColorProperty = ColorProperty([0, 0, 0, 0])
    """Border line color of the widget.
    
    Parameters
    ----------
    border_line_color : list of float
        RGBA color values for the border line. Defaults to [0, 0, 0, 0]."""

    border_line_width: float = NumericProperty(0)
    """Width of the border line.
    
    Parameters
    ----------
    border_line_width : float
        Width of the border line in pixels. Defaults to 0.
    """

    _background_color: Color
    """Kivy Color instruction for the background color."""

    _background_rectangle: RoundedRectangle
    """Kivy RoundedRectangle instruction for the background shape."""

    _border_line_color: Color
    """Kivy Color instruction for the border line color."""

    _border_line: SmoothLine
    """Kivy SmoothLine instruction for the border line."""

    def __init__(self, **kwargs) -> None:
        """Initialize the background behavior with canvas graphics 
        instructions.
        
        Parameters
        ----------
        **kwargs
            Additional keyword arguments passed to the parent class.
        """
        super().__init__(**kwargs)
        with self.canvas:
            self._background_color = Color(*self.background_color)
            self._background_rectangle = RoundedRectangle(
                size=self.size, pos=self.pos, radius=self.radius)
            self._border_line_color = Color(*self.border_line_color)
            self._border_line = SmoothLine(
                width=self.border_line_width,
                rounded_rectangle=self._rounded_rectangle)
        self.bind(
            background_color=self._update_background_color,
            size=self._update_size,
            pos=self._update_position,
            radius=self._update_radius,
            border_line_color=self._update_border_line_color,
            border_line_width=self._update_border_line_width,
            )
    
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
            self.x if is_relative else 0,
            self.y if is_relative else 0,
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
        self._background_color.rgba = self._ensure_alpha(color)
    
    def _update_border_line_color(
            self, instance: Any, color: List[float]):
        """Update the border line color when the property changes.
        
        Parameters
        ----------
        instance : Any
            The widget instance.
        color : list of float
            New border line color values.
        """
        self._border_line_color.rgba = self._ensure_alpha(color)

    def _update_border_line_width(
            self, instance: Any, width: float):
        """Update the border line width when the property changes.
        
        Parameters
        ----------
        instance : Any
            The widget instance.
        width : float
            New border line width.
        """
        self._border_line.width = width

    def _update_size(self, instance: Any, size: List[float]):
        """Update the background and border when the widget size changes.
        
        Parameters
        ----------
        instance : Any
            The widget instance.
        size : list of float
            New size values [width, height].
        """
        self._background_rectangle.size = size
        self._border_line.rounded_rectangle = self._rounded_rectangle

    def _update_position(self, instance: Any, pos: List[float]):
        """Update the background and border when the widget position changes.
        
        Parameters
        ----------
        instance : Any
            The widget instance.
        pos : list of float
            New position values [x, y].
        """
        self._background_rectangle.pos = pos
        self._border_line.rounded_rectangle = self._rounded_rectangle

    def _update_radius(self, instance: Any, radius: List[float]):
        """Update the background and border when the radius changes.
        
        Parameters
        ----------
        instance : Any
            The widget instance.
        radius : list of float
            New radius values [top_left, top_right, bottom_right, bottom_left].
        """
        self._background_rectangle.radius = radius
        self._border_line.rounded_rectangle = self._rounded_rectangle