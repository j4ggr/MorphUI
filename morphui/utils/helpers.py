"""
Helper utilities for MorphUI components
"""
import time
from typing import Any
from typing import Dict
from typing import List
from typing import Tuple
from typing import overload

from functools import lru_cache
from functools import wraps

from dataclasses import dataclass
from kivy.core.text import Label as CoreLabel
from kivy.uix.relativelayout import RelativeLayout

__all__ = [
    'calculate_text_size',
    'clamp',
    'get_effective_pos',
    'calculate_widget_local_pos',
    'get_edges_params',
    'FrozenGeometry',
    'timeit',]


def timeit(func):
    """Decorator to measure and print execution time of a function.
    
    This decorator wraps a function to measure its execution time and
    prints the time taken if it exceeds 1 millisecond. Useful for
    profiling performance-critical code.
    
    Parameters
    ----------
    func : callable
        The function to be timed.
    
    Returns
    -------
    callable
        The wrapped function with timing capability.
    
    Examples
    --------
    ```python
    from morphui.utils import timeit
    
    @timeit
    def slow_function():
        time.sleep(0.1)
        return "done"
    
    slow_function()  # Prints: slow_function: 100.00ms
    ```
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = (time.perf_counter() - start) * 1000
        if elapsed > 1:  # Only log if > 1ms
            print(f"{func.__qualname__}: {elapsed:.2f}ms")
        return result
    return wrapper


def calculate_text_size(text, font_size=16, font_name=None):
    """Calculate the size needed to render text"""
    
    label = CoreLabel(text=text, font_size=font_size)
    if font_name:
        label.options['font_name'] = font_name
    
    label.refresh()
    return label.content_size

@overload
def clamp(
        value: int, 
        min_value: int | None = None, 
        max_value: int | None = None
        ) -> int: ...

@overload
def clamp(
        value: float, 
        min_value: float | None = None, 
        max_value: float | None = None
        ) -> float: ...

def clamp(
        value: int | float, 
        min_value: int | float | None = None, 
        max_value: int | float | None = None
        ) -> int | float:
    """Constrain a numeric value to lie within a specified range.
    
    This function ensures that a value falls within the bounds defined by
    minimum and maximum values. If the value is below the minimum, it returns
    the minimum. If the value is above the maximum, it returns the maximum.
    Otherwise, it returns the original value unchanged.
    
    Parameters
    ----------
    value : float | int
        The value to constrain.
    min_value : float | int | None, optional
        The minimum allowed value. If None, no minimum constraint is applied.
        Defaults to None.
    max_value : float | int | None, optional
        The maximum allowed value. If None, no maximum constraint is applied.
        Defaults to None.
        
    Returns
    -------
    float
        The constrained value within the specified range.
        
    Raises
    ------
    ValueError
        If min_value is greater than max_value when both are specified.
        
    Examples
    --------
    Basic clamping with both bounds:
    
    ```python
    # Clamp to range [0, 100]
    result = clamp(150, 0, 100)  # Returns 100
    result = clamp(-10, 0, 100)  # Returns 0
    result = clamp(50, 0, 100)   # Returns 50
    ```
    
    Clamping with only minimum:
    
    ```python
    # Ensure value is at least 0
    result = clamp(-5, min_value=0)  # Returns 0
    result = clamp(10, min_value=0)  # Returns 10
    ```
    
    Clamping with only maximum:
    
    ```python
    # Ensure value is at most 255
    result = clamp(300, max_value=255)  # Returns 255
    result = clamp(100, max_value=255)  # Returns 100
    ```
    """
    if min_value is not None and max_value is not None: 
        assert min_value <= max_value, (
            f'min_value ({min_value}) cannot be greater than '
            f'max_value ({max_value})')
    
    # Apply constraints
    if min_value is not None:
        value = max(min_value, value)
    if max_value is not None:
        value = min(max_value, value)
        
    return value


def get_effective_pos(widget) -> Tuple[float, float]:
    """Get the effective position for canvas operations.
    
    Returns (0, 0) for RelativeLayout widgets since they use local 
    coordinates, otherwise returns (widget.x, widget.y). This is a
    common pattern in MorphUI for handling position calculations that
    need to work correctly with both regular widgets and RelativeLayout
    containers.
    
    Parameters
    ----------
    widget
        The widget to get the effective position for. Should have x and y
        attributes.
        
    Returns
    -------
    Tuple[float, float]
        The effective (x, y) position for canvas graphics operations.
        
    Examples
    --------
    Use in canvas operations:
    
    ```python
    from morphui.utils.helpers import get_effective_pos
    
    # Get position that works for both regular widgets and RelativeLayout
    x, y = get_effective_pos(self)
    
    # Use in canvas instructions
    with self.canvas:
        Rectangle(pos=(x, y), size=self.size)
    ```
    
    Use in layout calculations:
    
    ```python
    # Calculate absolute position for child widgets
    container_x, container_y = get_effective_pos(container)
    child_absolute_x = container_x + child.x
    child_absolute_y = container_y + child.y
    ```
    
    Notes
    -----
    - RelativeLayout widgets use local coordinate system where (0, 0) is 
      always the bottom-left corner of the layout
    - Regular widgets use absolute coordinates within their parent
    - This function abstracts away this difference for canvas operations
    """
    if isinstance(widget, RelativeLayout):
        return (0, 0)
    
    return (widget.x, widget.y)


def calculate_widget_local_pos(
        widget: Any, 
        window_pos: Tuple[float, float] | List[float]
        ) -> Tuple[float, float]:
    """Calculate widget-local coordinates from window coordinates.
    
    This function converts coordinates from window space to widget-local
    coordinates, accounting for coordinate system differences that occur
    when widgets are placed inside RelativeLayout containers (such as
    Screen widgets).
    
    This function works for all types of coordinate transformations:
    - Touch events (touch down, move, up)
    - Mouse coordinates (position, movement, hovering)
    - Any other window-space coordinates that need widget-local conversion
    
    In RelativeLayout containers, child widgets use local coordinates
    where their position is relative to the container, but events are
    reported in absolute window coordinates. This function calculates
    the necessary offset to transform any window position into the
    widget's coordinate space.
    
    The calculation works by:
    1. Getting the widget's absolute window position using to_window()
    2. Comparing it with the widget's local position to find the offset
    3. Applying this offset to the input coordinates
    
    Parameters
    ----------
    widget
        The widget for which to calculate local coordinates. Must have
        x, y attributes and a to_window() method (like Kivy widgets).
    window_pos : Tuple[float, float] | List[float]
        The position in window coordinates as (x, y).
        
    Returns
    -------
    Tuple[float, float]
        The position in widget-local coordinates as (x, y).
        
    Examples
    --------
    Calculate ripple position for touch events:
    
    ```python
    from morphui.utils.helpers import calculate_widget_local_pos
    
    def on_touch_down(self, touch):
        # Convert window coordinates to widget-local coordinates
        local_pos = calculate_widget_local_pos(self, touch.pos)
        self.ripple_pos = local_pos
    ```
    
    Handle mouse hovering:
    
    ```python
    def on_mouse_pos(self, *args):
        mouse_x, mouse_y = Window.mouse_pos
        local_x, local_y = calculate_widget_local_pos(self, (mouse_x, mouse_y))
        # Use local coordinates for hover effects
        self.is_hovered = self.collide_point(local_x, local_y)
    ```
    
    Handle coordinates in RelativeLayout child:
    
    ```python
    # Widget inside a Screen (RelativeLayout)
    class MyWidget(Widget):
        def on_touch_move(self, touch):
            # This correctly handles coordinate transformation
            local_x, local_y = calculate_widget_local_pos(self, touch.pos)
            # Use local_x, local_y for widget-relative calculations
    ```
    
    Notes
    -----
    - This function is particularly important for widgets inside Screen 
      widgets or other RelativeLayout containers
    - For widgets in regular layouts, this function typically returns
      the same coordinates as the input (no offset needed)
    - Works for any coordinate source: touch events, mouse position,
      programmatic coordinates, etc.
    - The offset calculation handles the coordinate system differences
      automatically
    """
    x_coord, y_coord = window_pos
    x_absolute, y_absolute = widget.to_window(widget.x, widget.y)
    x_offset = widget.x - x_absolute
    y_offset = widget.y - y_absolute
    return (x_coord + x_offset, y_coord + y_offset)

@lru_cache(maxsize=128)
def get_edges_params(
            left: float,
            right: float,
            bottom: float,
            top: float,
            offset: float,
            ) -> Dict[str, List[float]]:
    """Get parameters for creating edge lines around a rectangle.

    This function calculates the start and end points for lines
    representing the edges of a rectangle, with an optional offset
    to adjust the position of the edges inward or outward.

    Parameters
    ----------
    left : float
        The x-coordinate of the left edge.
    right : float
        The x-coordinate of the right edge.
    bottom : float
        The y-coordinate of the bottom edge.
    top : float
        The y-coordinate of the top edge.
    offset : float
        The offset to apply to each edge. Positive values move edges
        outward, negative values move them inward.
    
    Returns
    -------
    Dict[str, List[float]]
        A dictionary with keys 'left', 'right', 'bottom', 'top', each
        containing a list of two floats representing the start and end
        points of the corresponding edge line.
    """
    return {
        'top': [left, top - offset, right, top - offset],
        'right': [right - offset, top, right - offset, bottom],
        'bottom': [right, bottom + offset, left, bottom + offset],
        'left': [left + offset, bottom, left + offset, top],}


@dataclass(frozen=True)
class FrozenGeometry:
    """Immutable snapshot of widget geometry for reference operations.
    
    This dataclass captures and freezes the geometric properties of a 
    widget at a specific point in time. It's particularly useful for
    resize operations, drag-and-drop, animation starting points, and
    other scenarios where you need to preserve the original state of a 
    widget's dimensions and position.
    
    The frozen nature ensures that the captured geometry cannot be
    accidentally modified, providing a reliable reference point for 
    calculations and transformations.
    
    Attributes
    ----------
    x : float
        The x-coordinate of the widget's left edge in pixels.
    y : float  
        The y-coordinate of the widget's bottom edge in pixels.
    width : float
        The width of the widget in pixels.
    height : float
        The height of the widget in pixels.
    
    Properties
    ----------
    pos : Tuple[float, float]
        The position as a (x, y) tuple.
    size : Tuple[float, float]
        The size as a (width, height) tuple.
    center : Tuple[float, float]
        The center point as a (center_x, center_y) tuple.
    right : float
        The x-coordinate of the widget's right edge.
    top : float
        The y-coordinate of the widget's top edge.
    area : float
        The total area of the widget (width * height).
    aspect_ratio : float
        The width-to-height ratio.
    
    Examples
    --------
    Capture widget geometry for resize reference:
    
    ```python
    # Before starting resize operation
    original_geometry = FrozenGeometry.from_widget(widget)
    
    # During resize, calculate relative changes
    width_change = new_width - original_geometry.width
    height_change = new_height - original_geometry.height
    ```
    
    Store geometry for animation:
    
    ```python
    start_geometry = FrozenGeometry.from_widget(widget)
    end_geometry = FrozenGeometry(x=100, y=100, width=200, height=150)
    
    # Animate between the two states
    animate_geometry_transition(widget, start_geometry, end_geometry)
    ```
    
    Calculate relative positioning:
    
    ```python
    container_geometry = FrozenGeometry.from_widget(container)
    child_geometry = FrozenGeometry.from_widget(child)
    
    # Calculate child position relative to container
    relative_x = child_geometry.x - container_geometry.x
    relative_y = child_geometry.y - container_geometry.y
    ```
    """
    
    x: float = 0.0
    """The x-coordinate of the widget's left edge in pixels."""
    
    y: float = 0.0
    """The y-coordinate of the widget's bottom edge in pixels."""
    
    width: float = 0.0
    """The width of the widget in pixels."""
    
    height: float = 0.0
    """The height of the widget in pixels."""

    @classmethod
    def from_widget(cls, widget) -> 'FrozenGeometry':
        """Create a FrozenGeometry instance from a Kivy widget.
        
        This convenience method extracts the current geometry from any 
        Kivy widget and creates an immutable snapshot. It's the 
        recommended way to capture widget geometry for operations that 
        need a reference point.
        
        Parameters
        ----------
        widget : Widget
            Any Kivy widget with pos and size properties.
            
        Returns
        -------
        FrozenGeometry
            An immutable geometry snapshot of the widget.
            
        Examples
        --------
        ```python
        # Capture current widget state
        geometry = FrozenGeometry.from_widget(my_widget)
        
        # Use for calculations
        center_x = geometry.center[0]
        total_area = geometry.area
        ```
        """
        return cls(
            x=float(widget.x),
            y=float(widget.y),
            width=float(widget.width),
            height=float(widget.height))

    @property
    def pos(self) -> Tuple[float, float]:
        """The position of the widget as a (x, y) tuple.
        
        Returns
        -------
        Tuple[float, float]
            The position coordinates (x, y).
        """
        return (self.x, self.y)

    @property
    def size(self) -> Tuple[float, float]:
        """The size of the widget as a (width, height) tuple.
        
        Returns
        -------
        Tuple[float, float]
            The size dimensions (width, height).
        """
        return (self.width, self.height)

    @property
    def center(self) -> Tuple[float, float]:
        """The center point of the widget as a (center_x, center_y) 
        tuple.
        
        Calculates the center coordinates based on position and size.
        
        Returns
        -------
        Tuple[float, float]
            The center coordinates (center_x, center_y).
        """
        center_x = self.x + self.width / 2
        center_y = self.y + self.height / 2
        return (center_x, center_y)

    @property
    def right(self) -> float:
        """The x-coordinate of the widget's right edge.
        
        Returns
        -------
        float
            The x-coordinate of the right edge (x + width).
        """
        return self.x + self.width

    @property
    def top(self) -> float:
        """The y-coordinate of the widget's top edge.
        
        Returns
        -------
        float
            The y-coordinate of the top edge (y + height).
        """
        return self.y + self.height

    @property
    def area(self) -> float:
        """The total area of the widget.
        
        Returns
        -------
        float
            The area in square pixels (width * height).
        """
        return self.width * self.height

    @property
    def aspect_ratio(self) -> float:
        """The aspect ratio of the widget (width divided by height).
        
        Returns
        -------
        float
            The aspect ratio. Returns 1.0 if height is zero to avoid 
            division by zero.
        """
        return self.width / self.height if self.height > 0 else 1.0

    def point_delta(self, x: float, y: float) -> Tuple[float, float]:
        """Calculate the delta from a point to this geometry's position.
        
        This method computes how far a given point is from the widget's
        bottom-left corner (its position). It returns the horizontal and
        vertical differences as a tuple.
        
        Parameters
        ----------
        x : float
            The x-coordinate of the point.
        y : float
            The y-coordinate of the point.
            
        Returns
        -------
        Tuple[float, float]
            A tuple (dx, dy) representing the difference in x and y 
            coordinates from the point to the widget's position.
            
        Examples
        --------
        Calculate how far a mouse click is from the widget's origin:
        
        ```python
        geometry = FrozenGeometry.from_widget(my_widget)
        mouse_x, mouse_y = get_mouse_position()
        
        dx, dy = geometry.point_delta(mouse_x, mouse_y)
        print(f"Mouse is {dx} pixels right and {dy} pixels up from widget origin")
        ```
        """
        dx = x - self.x
        dy = y - self.y
        return (dx, dy)


    def scaled(self, scale_factor: float) -> 'FrozenGeometry':
        """Create a new geometry with scaled dimensions.
        
        Creates a new FrozenGeometry instance with the size scaled by
        the given factor. The position remains unchanged, so the widget
        scales from its bottom-left corner.
        
        Parameters
        ----------
        scale_factor : float
            The scaling factor. 1.0 = no change, 2.0 = double size, 
            0.5 = half size.
            
        Returns
        -------
        FrozenGeometry
            A new geometry with scaled dimensions.
            
        Examples
        --------
        ```python
        original = FrozenGeometry(x=100, y=100, width=200, height=150)
        doubled = original.scaled(2.0)  # 400x300
        halved = original.scaled(0.5)   # 100x75
        ```
        """
        return FrozenGeometry(
            x=self.x,
            y=self.y,
            width=self.width * scale_factor,
            height=self.height * scale_factor)

    def translated(self, dx: float, dy: float) -> 'FrozenGeometry':
        """Create a new geometry with translated position.
        
        Creates a new FrozenGeometry instance with the position offset by
        the given deltas. The size remains unchanged.
        
        Parameters
        ----------
        dx : float
            The horizontal offset to apply.
        dy : float
            The vertical offset to apply.
            
        Returns
        -------
        FrozenGeometry
            A new geometry with translated position.
            
        Examples
        --------
        ```python
        original = FrozenGeometry(x=100, y=100, width=200, height=150)
        moved = original.translated(50, -25)  # New position: (150, 75)
        ```
        """
        return FrozenGeometry(
            x=self.x + dx,
            y=self.y + dy,
            width=self.width,
            height=self.height)

    def resized(
            self, new_width: float, new_height: float) -> 'FrozenGeometry':
        """Create a new geometry with different dimensions.
        
        Creates a new FrozenGeometry instance with the specified size.
        The position remains unchanged.
        
        Parameters
        ----------
        new_width : float
            The new width.
        new_height : float
            The new height.
            
        Returns
        -------
        FrozenGeometry
            A new geometry with the specified dimensions.
            
        Examples
        --------
        ```python
        original = FrozenGeometry(x=100, y=100, width=200, height=150)
        resized = original.resized(300, 200)  # New size: 300x200
        ```
        """
        return FrozenGeometry(
            x=self.x,
            y=self.y,
            width=new_width,
            height=new_height)

    def collide_point(self, x: float, y: float) -> bool:
        """Check if a point is within this geometry's bounds.
        
        Parameters
        ----------
        x : float
            The x-coordinate to check.
        y : float
            The y-coordinate to check.
            
        Returns
        -------
        bool
            True if the point is within the bounds, False otherwise.
            
        Examples
        --------
        ```python
        geometry = FrozenGeometry(x=100, y=100, width=200, height=150)
        
        # Check if mouse position is within widget
        if geometry.collide_point(mouse_x, mouse_y):
            print("Mouse is over widget")
        ```
        """
        return (self.x <= x <= self.x + self.width and
                self.y <= y <= self.y + self.height)

    def distance_to_point(self, x: float, y: float) -> float:
        """Calculate the minimum distance from a point to this geometry.
        
        If the point is inside the geometry, returns 0. Otherwise,
        returns the distance to the nearest edge or corner.
        
        Parameters
        ----------
        x : float
            The x-coordinate of the point.
        y : float
            The y-coordinate of the point.
            
        Returns
        -------
        float
            The minimum distance to the geometry in pixels.
            
        Examples
        --------
        Distance to nearest edge or corner:
        ```python
        geometry = FrozenGeometry(x=100, y=100, width=200, height=150)
        distance = geometry.distance_to_point(50, 50)
        ```
        """
        if self.collide_point(x, y):
            return 0.0
            
        # Calculate distance to nearest edge
        dx = max(0, max(self.x - x, x - self.x - self.width))
        dy = max(0, max(self.y - y, y - self.y - self.height))

        return (dx * dx + dy * dy) ** 0.5

    def __str__(self) -> str:
        """String representation showing position and size.
        
        Returns
        -------
        str
            A human-readable string representation.
        """
        return (
            f'FrozenGeometry(pos=({self.x}, {self.y}), size=({self.width}, '
            f'{self.height}))')

    def __repr__(self) -> str:
        """Detailed string representation for debugging.
        
        Returns
        -------
        str
            A detailed string representation suitable for debugging.
        """
        return (
            f'FrozenGeometry(x={self.x}, y={self.y}, '
            f'width={self.width}, height={self.height})')
