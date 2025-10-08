"""Hover behaviors for Kivy widgets.

This module provides two hover behaviors:

- MorphHoverBehavior: Basic hover detection (enter/leave events)
- MorphHoverEnhancedBehavior: Advanced hover with edge/corner detection

Choose the appropriate behavior based on your needs:
- Use MorphHoverBehavior for simple hover effects
- Use MorphHoverEnhancedBehavior for complex position-aware interactions
"""

from typing import Any
from typing import List
from typing import Tuple
from typing import Literal

from kivy.event import EventDispatcher
from kivy.properties import ListProperty
from kivy.properties import StringProperty
from kivy.properties import NumericProperty
from kivy.properties import BooleanProperty
from kivy.core.window import Window


__all__ = [
    'MorphHoverBehavior',
    'MorphHoverEnhancedBehavior']


class MorphHoverBehavior(EventDispatcher):
    """Basic hover behavior that detects mouse enter and leave events.
    
    This is a lightweight behavior that provides core hover functionality
    without the overhead of edge and corner detection. Use this when you
    only need basic hover states for simple effects like color changes,
    cursor updates, or simple animations.
    
    Events
    ------
    - :meth:`on_enter`: Fired when mouse enters the widget
    - :meth:`on_leave`: Fired when mouse leaves the widget
    
    Properties
    ----------
    - :attr:`hover_enabled`: Enable/disable hover detection
    - :attr:`hovered`: Current hover state
    - :attr:`enter_pos`: Position where mouse entered (widget coords)
    - :attr:`leave_pos`: Position where mouse left (widget coords) 
    - :attr:`current_pos`: Current mouse position (widget coords)
    
    Examples
    --------
    Simple hover color change:
    
    ```python
    from kivy.uix.label import Label
    from morphui.uix.behaviors.hover import MorphHoverBehavior
    
    class HoverLabel(MorphHoverBehavior, Label):
        def on_enter(self):
            self.color = (1, 0, 0, 1)  # Red on hover
            
        def on_leave(self):
            self.color = (1, 1, 1, 1)  # White when not hovering
    ```
    
    Hover with position tracking:
    
    ```python
    class PositionTracker(MorphHoverBehavior, Widget):
        def on_enter(self):
            print(f"Mouse entered at: {self.enter_pos}")
            
        def on_leave(self):
            print(f"Mouse left at: {self.leave_pos}")
    ```
    """

    hover_enabled = BooleanProperty(True)
    """Enable or disable hover behavior and event detection.
    
    When set to False, the behavior will not track mouse position or fire
    hover events, effectively disabling all hover functionality. This is
    useful for temporarily disabling hover effects without removing the
    behavior from the widget.
    
    Setting this to False will also clear any current hover state and
    stop all hover-related event dispatching until re-enabled.
    
    :attr:`hover_enabled` is a :class:`~kivy.properties.BooleanProperty` 
    and defaults to True.
    
    Examples
    --------
    ```python
    # Temporarily disable hover during animations
    widget.hover_enabled = False
    animation.start(widget)
    animation.bind(on_complete=lambda *args: setattr(widget, 'hover_enabled', True))
    
    # Conditionally enable hover based on widget state
    widget.hover_enabled = not widget.disabled
    ```
    """

    hovered = BooleanProperty(False)
    """Indicates whether the mouse is currently over the widget.
    
    This property is automatically updated based on mouse position
    and widget bounds. You can bind to this property to react to
    hover state changes.
    
    :attr:`hovered` is a :class:`~kivy.properties.BooleanProperty` 
    and defaults to False.
    """

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        
        # Position tracking
        self.enter_pos: Tuple[float, float] = (0, 0)
        self.leave_pos: Tuple[float, float] = (0, 0)
        self.current_pos: Tuple[float, float] = (0, 0)
        
        # Bind to window mouse position
        Window.bind(mouse_pos=self.on_mouse_pos)
        
        # Register events
        self.register_event_type('on_enter')
        self.register_event_type('on_leave')

    @property
    def is_displayed(self) -> bool:
        """Check if widget is displayed (has root window)."""
        return bool(self.get_root_window())

    def on_mouse_pos(self, instance: Any, pos: Tuple[float, float]) -> None:
        """Handle mouse position changes from Window.
        
        This method is automatically called whenever the mouse moves.
        It updates hover state and position tracking based on collision
        detection with the widget bounds.
        
        Parameters
        ----------
        instance : Any
            The Window instance (unused)
        pos : Tuple[float, float]
            Mouse position in window coordinates
        """
        if not self.is_displayed or not self.hover_enabled:
            return

        # Convert to widget coordinates
        self.current_pos = self.to_window(*pos)
        inside = self.collide_point(*pos)

        # Handle hover state changes
        if inside and not self.hovered:
            self.enter_pos = self.current_pos
            self.hovered = True
        elif not inside and self.hovered:
            self.leave_pos = self.current_pos
            self.hovered = False

    def on_hovered(self, instance: Any, hovered: bool) -> None:
        """Event fired when hover state changes.
        
        Automatically dispatches on_enter or on_leave events based
        on the new hover state.
        
        Parameters
        ----------
        instance : Any
            The widget instance
        hovered : bool
            New hover state
        """
        if hovered:
            self.dispatch('on_enter')
        else:
            self.dispatch('on_leave')

    def on_enter(self) -> None:
        """Event fired when mouse enters the widget.
        
        Override this method in subclasses to add custom hover
        behavior. The mouse position where the widget was entered
        is available in :attr:`enter_pos`.
        
        Examples
        --------
        ```python
        def on_enter(self):
            self.surface_color = (0, 1, 0, 0.3)  # Light green
            Animation(opacity=0.8, duration=0.2).start(self)
        ```
        """
        pass

    def on_leave(self) -> None:
        """Event fired when mouse leaves the widget.
        
        Override this method in subclasses to add custom hover
        behavior. The mouse position where the widget was left
        is available in :attr:`leave_pos`.
        
        Examples
        --------
        ```python
        def on_leave(self):
            self.surface_color = (1, 1, 1, 1)  # White
            Animation(opacity=1.0, duration=0.2).start(self)
        ```
        """
        pass


class MorphHoverEnhancedBehavior(MorphHoverBehavior):
    """Enhanced hover behavior with edge and corner detection.
    
    This behavior extends the base hover functionality with detailed
    edge and corner detection. It's ideal for widgets that need to
    respond differently based on where the mouse is positioned within
    the widget bounds.
    
    Additional Events (beyond base hover)
    ------------------------------------
    - :meth:`on_enter_edge`: Fired when mouse enters any edge
    - :meth:`on_leave_edge`: Fired when mouse leaves any edge
    - :meth:`on_enter_corner`: Fired when mouse enters any corner
    - :meth:`on_leave_corner`: Fired when mouse leaves any corner
    
    Additional Properties
    --------------------
    - :attr:`hovered_edges`: List of currently hovered edges
    - :attr:`hovered_corner`: Currently hovered corner
    - :attr:`edge_size`: Size of edge detection area in pixels
    - Individual edge properties: left_edge_hovered, right_edge_hovered, etc.
    
    Common Use Cases
    ---------------
    - Resizable widgets with visual resize handles
    - Tooltips that change based on widget area
    - Cursor changes for different widget regions
    - Complex hover animations based on position
    
    Examples
    --------
    Resizable widget with visual feedback:
    
    ```python
    from kivy.uix.widget import Widget
    from kivy.core.window import Window
    from morphui.uix.behaviors.hover import MorphHoverEnhancedBehavior
    
    class ResizableWidget(MorphHoverEnhancedBehavior, Widget):
        def on_enter_edge(self, edge):
            if edge in ['left', 'right']:
                Window.set_system_cursor('size_we')  # Horizontal resize
            else:
                Window.set_system_cursor('size_ns')  # Vertical resize
                
        def on_enter_corner(self, corner):
            if corner in ['top-left', 'bottom-right']:
                Window.set_system_cursor('size_nwse')
            else:
                Window.set_system_cursor('size_nesw')
                
        def on_leave(self):
            Window.set_system_cursor('arrow')  # Reset cursor
    ```
    
    Dynamic tooltips:
    
    ```python
    class SmartTooltip(MorphHoverEnhancedBehavior, Widget):
        def on_enter_edge(self, edge):
            self.show_tooltip(f"Drag {edge} edge to resize")
            
        def on_enter_corner(self, corner):
            self.show_tooltip(f"Drag {corner} corner to resize diagonally")
            
        def on_enter(self):
            if not self.hovered_edges:
                self.show_tooltip("Click to select widget")
    ```
    """

    # Edge and corner detection properties
    hovered_edges: List[str] = ListProperty([])
    """List of edges currently being hovered over.
    
    Contains edge names from ['left', 'right', 'top', 'bottom'] that
    are currently under the mouse cursor. Updated automatically based
    on mouse position and edge_size.
    
    :attr:`hovered_edges` is a :class:`~kivy.properties.ListProperty`
    and defaults to an empty list.
    """

    hovered_corner: str = StringProperty(
        'none',
        options=('top-left', 'top-right', 'bottom-left', 'bottom-right', 'none'))
    """The corner currently being hovered over.
    
    Automatically determined from hovered_edges when exactly two adjacent
    edges are hovered. Possible values are corner names or 'none'.
    
    :attr:`hovered_corner` is a :class:`~kivy.properties.StringProperty`
    and defaults to 'none'.
    """

    # Individual edge hover states
    left_edge_hovered = BooleanProperty(False)
    """Whether the left edge is currently hovered.
    
    :attr:`left_edge_hovered` is a :class:`~kivy.properties.BooleanProperty`
    and defaults to False.
    """

    right_edge_hovered = BooleanProperty(False)
    """Whether the right edge is currently hovered.
    
    :attr:`right_edge_hovered` is a :class:`~kivy.properties.BooleanProperty`
    and defaults to False.
    """

    top_edge_hovered = BooleanProperty(False)
    """Whether the top edge is currently hovered.
    
    :attr:`top_edge_hovered` is a :class:`~kivy.properties.BooleanProperty`
    and defaults to False.
    """

    bottom_edge_hovered = BooleanProperty(False)
    """Whether the bottom edge is currently hovered.
    
    :attr:`bottom_edge_hovered` is a :class:`~kivy.properties.BooleanProperty`
    and defaults to False.
    """

    edge_size = NumericProperty(4)
    """Size of the edge area for detection in pixels.
    
    Determines how many pixels from the widget edge count as "edge area"
    for hover detection. Larger values make edges easier to target but
    reduce the center area.
    
    :attr:`edge_size` is a :class:`~kivy.properties.NumericProperty`
    and defaults to 4.
    """

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        
        # Track last corner for proper event dispatching
        self._last_hovered_corner: str = 'none'
        
        # Register additional events
        self.register_event_type('on_enter_edge')
        self.register_event_type('on_leave_edge')
        self.register_event_type('on_enter_corner')
        self.register_event_type('on_leave_corner')

    @property
    def EDGES(self) -> Tuple[str, str, str, str]:
        """Tuple of valid edge names."""
        return ('left', 'right', 'top', 'bottom')

    @property
    def CORNERS(self) -> Tuple[str, str, str, str]:
        """Tuple of valid corner names."""
        return ('top-left', 'top-right', 'bottom-left', 'bottom-right')

    def get_hovered_corner(self) -> str:
        """Determine corner from currently hovered edges.
        
        Returns
        -------
        str
            Corner name if exactly two adjacent edges are hovered,
            'none' otherwise.
        """
        if not self.hovered or len(self.hovered_edges) != 2:
            return 'none'
        
        # Convert edge combination to corner name
        edges = sorted(self.hovered_edges)
        if len(edges) == 2:
            edge_tuple = (edges[0], edges[1])
            corner_map = {
                ('bottom', 'left'): 'bottom-left',
                ('bottom', 'right'): 'bottom-right',
                ('left', 'top'): 'top-left',
                ('right', 'top'): 'top-right'
            }
            return corner_map.get(edge_tuple, 'none')
        return 'none'

    def get_hovered_edges(self) -> List[str]:
        """Get list of currently hovered edges.
        
        Returns
        -------
        List[str]
            List of edge names that are currently hovered.
        """
        return [edge for edge in self.EDGES 
                if getattr(self, f'{edge}_edge_hovered')]

    def on_mouse_pos(self, instance: Any, pos: Tuple[float, float]) -> None:
        """Enhanced mouse position handling with edge detection.
        
        Extends the base behavior to also calculate edge and corner
        hover states based on mouse position within the widget.
        
        Parameters
        ----------
        instance : Any
            The Window instance
        pos : Tuple[float, float]
            Mouse position in window coordinates
        """
        # Call parent method for basic hover detection
        super().on_mouse_pos(instance, pos)
        
        if not self.is_displayed or not self.hover_enabled:
            return

        # Only calculate edges if we're hovering over the widget
        if self.hovered:
            self._update_edge_detection()
        else:
            self._clear_edge_detection()

    def _update_edge_detection(self) -> None:
        """Update edge and corner detection based on current mouse position."""
        # Calculate relative position within widget
        x = self.current_pos[0] - self.x
        y = self.current_pos[1] - self.y

        # Update individual edge states
        self.left_edge_hovered = (x <= self.edge_size)
        self.right_edge_hovered = (x >= self.width - self.edge_size)
        self.top_edge_hovered = (y >= self.height - self.edge_size)
        self.bottom_edge_hovered = (y <= self.edge_size)

        # Update edge list and corner detection
        self.hovered_edges = self.get_hovered_edges()
        self._last_hovered_corner = self.hovered_corner
        self.hovered_corner = self.get_hovered_corner()

    def _clear_edge_detection(self) -> None:
        """Clear all edge and corner detection when not hovering."""
        self.left_edge_hovered = False
        self.right_edge_hovered = False
        self.top_edge_hovered = False
        self.bottom_edge_hovered = False
        self.hovered_edges = []
        self._last_hovered_corner = self.hovered_corner
        self.hovered_corner = 'none'

    def _dispatch_edge_event(self, edge: str, hovered: bool) -> None:
        """Dispatch appropriate edge event based on hover state.
        
        Parameters
        ----------
        edge : str
            Edge name ('left', 'right', 'top', 'bottom')
        hovered : bool
            Whether the edge is now hovered or not
        """
        if hovered:
            self.dispatch('on_enter_edge', edge)
        else:
            self.dispatch('on_leave_edge', edge)

    # Edge event handlers
    def on_left_edge_hovered(self, instance: Any, hovered: bool) -> None:
        """Handle left edge hover state changes."""
        self._dispatch_edge_event('left', hovered)

    def on_right_edge_hovered(self, instance: Any, hovered: bool) -> None:
        """Handle right edge hover state changes."""
        self._dispatch_edge_event('right', hovered)

    def on_top_edge_hovered(self, instance: Any, hovered: bool) -> None:
        """Handle top edge hover state changes."""
        self._dispatch_edge_event('top', hovered)

    def on_bottom_edge_hovered(self, instance: Any, hovered: bool) -> None:
        """Handle bottom edge hover state changes."""
        self._dispatch_edge_event('bottom', hovered)

    def on_hovered_corner(self, instance: Any, corner: str) -> None:
        """Handle corner hover state changes.
        
        Dispatches enter/leave corner events when the corner changes.
        
        Parameters
        ----------
        instance : Any
            The widget instance
        corner : str
            New corner value
        """
        if corner != self._last_hovered_corner:
            if self._last_hovered_corner != 'none':
                self.dispatch('on_leave_corner', self._last_hovered_corner)
            if corner != 'none':
                self.dispatch('on_enter_corner', corner)

    # Event methods to override
    def on_enter_edge(self, edge: Literal['left', 'right', 'top', 'bottom']) -> None:
        """Event fired when mouse enters any edge.
        
        Parameters
        ----------
        edge : Literal['left', 'right', 'top', 'bottom']
            The edge being entered
            
        Examples
        --------
        ```python
        def on_enter_edge(self, edge):
            self.edge_highlight[edge] = True
            if edge in ['left', 'right']:
                Window.set_system_cursor('size_we')
            else:
                Window.set_system_cursor('size_ns')
        ```
        """
        pass

    def on_leave_edge(self, edge: Literal['left', 'right', 'top', 'bottom']) -> None:
        """Event fired when mouse leaves any edge.
        
        Parameters
        ----------
        edge : Literal['left', 'right', 'top', 'bottom']
            The edge being left
        """
        pass

    def on_enter_corner(self, corner: Literal['top-left', 'top-right', 'bottom-left', 'bottom-right']) -> None:
        """Event fired when mouse enters any corner.
        
        Parameters
        ----------
        corner : Literal['top-left', 'top-right', 'bottom-left', 'bottom-right']
            The corner being entered
            
        Examples
        --------
        ```python
        def on_enter_corner(self, corner):
            if corner in ['top-left', 'bottom-right']:
                Window.set_system_cursor('size_nwse')
            else:
                Window.set_system_cursor('size_nesw')
        ```
        """
        pass

    def on_leave_corner(self, corner: Literal['top-left', 'top-right', 'bottom-left', 'bottom-right']) -> None:
        """Event fired when mouse leaves any corner.
        
        Parameters
        ----------
        corner : Literal['top-left', 'top-right', 'bottom-left', 'bottom-right']
            The corner being left
        """
        pass