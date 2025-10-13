"""Resize behaviors for Kivy widgets.

This module provides resize functionality through mouse interaction,
allowing widgets to be resized by dragging edges and corners. The behavior
combines hover detection with visual feedback through overlay layers.

The resize behavior supports:
- Edge resizing (horizontal, vertical)
- Corner resizing (diagonal)
- Visual feedback with edge highlighting
- Cursor changes for different resize directions
- Minimum and maximum size constraints
- Aspect ratio preservation (optional)
"""

from typing import Any
from typing import List
from typing import Tuple
from typing import Optional

from kivy.core.window import Window
from kivy.properties import ListProperty
from kivy.properties import NumericProperty
from kivy.properties import BooleanProperty
from kivy.input.motionevent import MotionEvent

from ...constants import NAME

from ...utils import FrozenGeometry

from .hover import MorphHoverEnhancedBehavior
from .layer import MorphOverlayLayerBehavior


__all__ = [
    'MorphResizeBehavior',
]


class MorphResizeBehavior(
        MorphHoverEnhancedBehavior,
        MorphOverlayLayerBehavior):
    """A behavior that enables widgets to be resized by dragging edges and corners.
    
    This behavior combines enhanced hover detection with overlay layer functionality
    to provide interactive resizing capabilities. It automatically detects when the
    mouse is over resizable edges or corners and provides visual feedback through
    edge highlighting and cursor changes.
    
    Features
    --------
    - **Edge Resizing**: Resize by dragging left, right, top, or bottom edges
    - **Corner Resizing**: Resize diagonally by dragging corners
    - **Visual Feedback**: Highlighted edges and appropriate cursor changes
    - **Size Constraints**: Minimum and maximum size limits
    - **Aspect Ratio**: Optional aspect ratio preservation
    - **Animation**: Smooth transitions for visual feedback
    - **Events**: Comprehensive event system for resize operations
    
    Events
    ------
    - :meth:`on_resize_start`: Fired when resize operation begins
    - :meth:`on_resize`: Fired during resize (real-time updates)
    - :meth:`on_resize_end`: Fired when resize operation completes
    
    Properties
    ----------
    - :attr:`resize_enabled`: Enable/disable resize functionality
    - :attr:`resizable_edges`: List of edges that can be resized
    - :attr:`min_size`: Minimum width and height constraints
    - :attr:`max_size`: Maximum width and height constraints
    - :attr:`preserve_aspect_ratio`: Whether to maintain aspect ratio
    - :attr:`resize_animation_duration`: Duration for visual feedback animations
    
    Examples
    --------
    Basic resizable widget:
    
    ```python
    from kivy.uix.widget import Widget
    from morphui.uix.behaviors.resize import MorphResizeBehavior
    
    class ResizableWidget(MorphResizeBehavior, Widget):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            self.size = (200, 150)
            self.pos = (100, 100)
    ```
    
    Resizable with constraints:
    
    ```python
    class ConstrainedWidget(MorphResizeBehavior, Widget):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            self.min_size = (100, 75)
            self.max_size = (400, 300)
            self.preserve_aspect_ratio = True
            
        def on_resize_start(self, edge_or_corner):
            print(f"Starting resize from {edge_or_corner}")
            
        def on_resize_end(self, edge_or_corner):
            print(f"Finished resizing from {edge_or_corner}")
    ```
    
    Custom resize feedback:
    
    ```python
    class CustomResizeWidget(MorphResizeBehavior, Widget):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            self.resize_edge_color = [0, 1, 0, 0.6]  # Green highlight
            self.resize_animation_duration = 0.15
            
        def on_resize(self, edge_or_corner, new_size, new_pos):
            # Custom resize logic here
            self.size = new_size
            self.pos = new_pos
    ```
    """

    # Resize functionality properties
    resize_enabled: bool = BooleanProperty(True)
    """Enable or disable resize functionality.
    
    When set to False, the widget will not respond to resize operations,
    but hover detection and visual feedback will still work. This is useful
    for temporarily disabling resize while maintaining visual consistency.
    
    :attr:`resize_enabled` is a :class:`~kivy.properties.BooleanProperty`
    and defaults to True.
    """

    resizable_edges: List[str] = ListProperty(NAME.EDGES)
    """List of edges that can be used for resizing.
    
    Controls which edges of the widget can be dragged to resize. Can contain
    any combination of 'left', 'right', 'top', 'bottom'. Corner resizing
    is automatically enabled when two adjacent edges are both resizable.
    
    :attr:`resizable_edges` is a :class:`~kivy.properties.ListProperty`
    and defaults to all edges (left, right, top, bottom).
    """

    min_size: List[float] = ListProperty([50, 50])
    """Minimum size constraints [width, height].
    
    Prevents the widget from being resized smaller than these dimensions.
    Useful for maintaining usability and preventing widgets from becoming
    too small to interact with.
    
    :attr:`min_size` is a :class:`~kivy.properties.ListProperty`
    and defaults to [50, 50].
    """

    max_size: List[float] = ListProperty([1000, 1000])
    """Maximum size constraints [width, height].
    
    Prevents the widget from being resized larger than these dimensions.
    Use [0, 0] or negative values to disable maximum size constraints.
    
    :attr:`max_size` is a :class:`~kivy.properties.ListProperty`
    and defaults to [1000, 1000].
    """

    preserve_aspect_ratio: bool = BooleanProperty(False)
    """Whether to preserve the widget's aspect ratio during resize.
    
    When True, the widget will maintain its width-to-height ratio during
    resize operations. This is particularly useful for images, video players,
    or other content where aspect ratio is important.
    
    :attr:`preserve_aspect_ratio` is a :class:`~kivy.properties.BooleanProperty`
    and defaults to False.
    """

    resize_animation_duration: float = NumericProperty(0.2)
    """Duration for visual feedback animations in seconds.
    
    Controls how long it takes for edge highlighting and other visual
    effects to transition. Shorter values create snappier feedback,
    longer values create smoother transitions.
    
    :attr:`resize_animation_duration` is a :class:`~kivy.properties.NumericProperty`
    and defaults to 0.2.
    """

    # Internal state tracking
    _resize_in_progress: bool = False
    """Whether a resize operation is currently in progress."""

    _resize_reference_geometry: FrozenGeometry
    """Frozen reference geometry for mouse movements when resize 
    operation started."""
    
    _resize_start_pos: Tuple[float, float] = (0, 0)
    """Mouse position where resize operation started."""
    
    _resize_start_size: Tuple[float, float] = (0, 0)
    """Widget size when resize operation started."""
    
    _resize_start_widget_pos: Tuple[float, float] = (0, 0)
    """Widget position when resize operation started."""
    
    _resize_edge_or_corner: Optional[str] = None
    """The edge or corner being used for current resize operation."""
    
    _original_aspect_ratio: float = 1.0
    """Original aspect ratio for preservation during resize."""

    def __init__(self, **kwargs) -> None:
        # Register resize events
        self.register_event_type('on_resize_start')
        self.register_event_type('on_resize')
        self.register_event_type('on_resize_end')
        
        super().__init__(**kwargs)
        
        # Bind to touch events for resize functionality
        self.bind(on_touch_down=self._handle_resize_touch_down)
        self.bind(on_touch_move=self._handle_resize_touch_move)
        self.bind(on_touch_up=self._handle_resize_touch_up)
        
        # Update cursor and visuals based on hover state
        self.bind(
            hovered_edges=self._update_resize_feedback,
            hovered_corner=self._update_resize_feedback,)
    
    @property
    def hovered_resizable_edges(self) -> List[str]:
        """List of currently hovered edges that are resizable.
        
        Only edges present in :attr:`resizable_edges` will be included.
        If resize is disabled, this will always be an empty list."""
        if not self.resize_enabled:
            return []
        return list(filter(self._is_edge_resizable, self.hovered_edges))
    
    @property
    def hovered_resizable_corner(self) -> str | None:
        """Currently hovered corner if it is resizable, else None."""
        if not self.resize_enabled or self.hovered_corner is None:
            return None
        if self.is_corner_resizable(self.hovered_corner):
            return self.hovered_corner
        return None

    def _is_edge_resizable(self, edge: str) -> bool:
        """Check if a specific edge can be used for resizing.
        
        Parameters
        ----------
        edge : str
            Edge name to check ('left', 'right', 'top', 'bottom')
            
        Returns
        -------
        bool
            True if the edge can be used for resizing
        """
        return self.resize_enabled and edge in self.resizable_edges

    def is_corner_resizable(self, corner: str | None) -> bool:
        """Check if a specific corner can be used for resizing.

        A corner is considered resizable if both adjacent edges are 
        resizable.
        
        Parameters
        ----------
        corner : str | None
            Corner name to check (e.g., 'top-left', 'bottom-right')
            
        Returns
        -------
        bool
            True if the corner can be used for resizing
        """
        if not self.resize_enabled or corner is None:
            return False
         
        return all(
            e in self.resizable_edges for e in corner.split(NAME.SEP_CORNER))

    def _update_resize_feedback(self, *args) -> None:
        """Update visual feedback based on current hover state.
        
        This method updates edge highlighting and mouse cursor based on
        which edges or corners are currently hovered and resizable.
        It is called automatically when hover state changes.
        The cursor is only updated if no resize operation is in progress.
        
        Notes
        -----
        If resize is disabled, no edges will be highlighted and the
        cursor will always be the default arrow.
        Available cursors depend on the operating system, so some
        cursors may not be supported everywhere. For more details, see:
        [Kivy Documentation](https://kivy.org/doc/stable/api-kivy.core.window.html#kivy.core.window.WindowBase.set_system_cursor)
        """
        if not self.resize_enabled:
            return None
        
        self.visible_edges = self.hovered_resizable_edges
        
        cursor = 'arrow'
        if self.hovered_resizable_corner is not None:
            cursor = 'size_all'
        elif self.hovered_resizable_edges:
            edge = self.hovered_resizable_edges[0]
            if edge in NAME.HORIZONTAL_EDGES:
                cursor = 'size_ns'
            elif edge in NAME.VERTICAL_EDGES:
                cursor = 'size_we'
        Window.set_system_cursor(cursor)

    def _calculate_new_size_and_pos(
            self,
            mouse_pos: Tuple[float, float]
            ) -> Tuple[Tuple[float, float], Tuple[float, float]]:
        """Calculate new size and position based on mouse position
        during resize operation.
        
        Parameters
        ----------
        edge_or_corner : str
            The edge or corner being dragged
        mouse_pos : Tuple[float, float]
            Current mouse position
            
        Returns
        -------
        Tuple[Tuple[float, float], Tuple[float, float]]
            New size (width, height) and new position (x, y)
        """
        reference = self._resize_reference_geometry
        x, y = reference.pos
        width, height = reference.size
        dx, dy = reference.point_delta(*mouse_pos)

        if self.hovered_resizable_corner is not None:
            edges = self.hovered_resizable_corner.split(NAME.SEP_CORNER)
        elif self.hovered_resizable_edges:
            edges = [self.hovered_resizable_edges[0]]
        else:
            edges = []

        for edge in edges:
            if edge == 'left':
                width -= dx
                x += dx
            elif edge == 'right':
                width += dx
            elif edge == 'top':
                height += dy
            elif edge == 'bottom':
                height -= dy
                y += dy
        return (width, height), (x, y)

    def _apply_resize_constraints(
            self,
            width: float,
            height: float
            ) -> Tuple[float, float]:
        """Apply size constraints and aspect ratio preservation to 
        resize dimensions.
        
        This method enforces minimum/maximum size limits and preserves
        aspect ratio if enabled. It ensures that resize operations
        respect all configured constraints while maintaining visual
        consistency.
        
        Parameters
        ----------
        width : float
            Proposed new width
        height : float
            Proposed new height

        Returns
        -------
        Tuple[float, float]
            Constrained size after applying all restrictions.
            
        Notes
        -----
        Constraints are applied in this order:
        1. Aspect ratio preservation (if enabled)
        2. Minimum size constraints
        3. Maximum size constraints
        
        The aspect ratio is preserved by adjusting the dimension that 
        would result in the smaller change, maintaining the most natural
        resize feel.
        """
        reference = self._resize_reference_geometry
        target_ratio = reference.aspect_ratio
        
        if self.preserve_aspect_ratio and target_ratio > 0:
            current_ratio = width / height if height > 0 else 1.0
            
            if abs(current_ratio - target_ratio) > 0.001:  # Small tolerance for floating point
                if current_ratio > target_ratio:
                    # Width is too large relative to height
                    width = height * target_ratio
                else:
                    # Height is too large relative to width
                    height = width / target_ratio

        width = max(self.min_size[0], width)
        height = max(self.min_size[1], height)
        
        # Apply maximum size constraints (if specified)
        if self.max_size[0] > 0:
            width = min(self.max_size[0], width)
        if self.max_size[1] > 0:
            height = min(self.max_size[1], height)

        return width, height

    def apply_new_size_and_pos(
            self, 
            new_size: Tuple[float, float], 
            new_pos: Tuple[float, float]
            ) -> None:
        """Apply new size and position to the widget.
        
        Parameters
        ----------
        new_size : Tuple[float, float]
            New size (width, height)
        new_pos : Tuple[float, float]
            New position (x, y)
        """
        self.size = new_size
        self.pos = new_pos

    def _handle_resize_touch_down(self, instance: Any, touch: MotionEvent) -> bool:
        """Handle touch down events for resize operations.
        
        Parameters
        ----------
        instance : Any
            Widget instance (self)
        touch : MotionEvent
            Touch event
            
        Returns
        -------
        bool
            True if touch was handled for resize
        """
        if any((
                not self.resize_enabled,
                not self.hovered_resizable_edges,
                self._resize_in_progress,)):
            return False
            
        self._resize_in_progress = True
        self._resize_reference_geometry = FrozenGeometry(
            x=touch.x,
            y=touch.y,
            width=self.width,
            height=self.height)
        
        if self.hovered_resizable_corner is not None:
            resize_target = self.hovered_resizable_corner
        else:
            resize_target = self.hovered_resizable_edges[0]
        self.dispatch('on_resize_start', resize_target)
        return True

    def _handle_resize_touch_move(self, instance: Any, touch: MotionEvent) -> bool:
        """Handle touch move events during resize operations.
        
        Parameters
        ----------
        instance : Any
            Widget instance (self)
        touch : MotionEvent
            Touch event
            
        Returns
        -------
        bool
            True if touch was handled for resize
        """
        if any((
                not self._resize_in_progress,
                touch.grab_current != self,
                not self._resize_in_progress)):
            return False
            
        # Calculate new size and position
        new_size, new_pos = self._calculate_new_size_and_pos(touch.pos)
        new_size = self._apply_resize_constraints(*new_size)
        
        # Dispatch resize event with new dimensions
        self.dispatch('on_resize', self._resize_edge_or_corner, new_size, new_pos)
        
        return True

    def _handle_resize_touch_up(self, instance: Any, touch: MotionEvent) -> bool:
        """Handle touch up events to end resize operations.
        
        Parameters
        ----------
        instance : Any
            Widget instance (self)
        touch : MotionEvent
            Touch event
            
        Returns
        -------
        bool
            True if touch was handled for resize
        """
        if not self._resize_in_progress or touch.grab_current != self:
            return False
            
        # End resize operation
        edge_or_corner = self._resize_edge_or_corner
        self._resize_in_progress = False
        self._resize_edge_or_corner = None
        
        # Release touch grab
        touch.ungrab(self)
        
        # Dispatch resize end event
        self.dispatch('on_resize_end', edge_or_corner)
        
        return True

    # Event methods (override in subclasses)
    def on_resize_start(self, edge_or_corner: str) -> None:
        """Event fired when a resize operation begins.
        
        This event is dispatched when the user starts dragging an edge or
        corner to resize the widget. Override this method to add custom
        behavior at the start of resize operations.
        
        Parameters
        ----------
        edge_or_corner : str
            The edge or corner being used for resize ('left', 'right', 'top',
            'bottom', or corner names like 'top-left')
            
        Examples
        --------
        ```python
        def on_resize_start(self, edge_or_corner):
            print(f"Starting resize from {edge_or_corner}")
            self.opacity = 0.8  # Make widget semi-transparent during resize
        ```
        """
        pass

    def on_resize(
            self, 
            edge_or_corner: str, 
            new_size: Tuple[float, float], 
            new_pos: Tuple[float, float]
    ) -> None:
        """Event fired during resize operations with new dimensions.
        
        This event is dispatched continuously while the user drags to resize
        the widget. The default implementation applies the new size and position
        to the widget. Override this method to customize resize behavior or
        add validation.
        
        Parameters
        ----------
        edge_or_corner : str
            The edge or corner being used for resize
        new_size : Tuple[float, float]
            New widget size (width, height)
        new_pos : Tuple[float, float]
            New widget position (x, y)
            
        Examples
        --------
        ```python
        def on_resize(self, edge_or_corner, new_size, new_pos):
            # Custom validation
            if new_size[0] < 100:
                return  # Don't allow width less than 100
                
            # Apply resize
            super().on_resize(edge_or_corner, new_size, new_pos)
            
            # Update content
            self.update_content_layout()
        ```
        """
        # Default implementation: apply new size and position
        self.size = new_size
        self.pos = new_pos

    def on_resize_end(self, edge_or_corner: str) -> None:
        """Event fired when a resize operation completes.
        
        This event is dispatched when the user releases the mouse after
        resizing the widget. Override this method to add custom behavior
        at the end of resize operations, such as saving the new size or
        triggering layout updates.
        
        Parameters
        ----------
        edge_or_corner : str
            The edge or corner that was used for resize
            
        Examples
        --------
        ```python
        def on_resize_end(self, edge_or_corner):
            print(f"Finished resizing from {edge_or_corner}")
            self.opacity = 1.0  # Restore full opacity
            self.save_size_to_config()  # Save new size
        ```
        """
        pass

    # Override hover behavior to reset cursor when leaving widget
    def on_leave(self) -> None:
        """Override parent on_leave to reset cursor."""
        super().on_leave()
        if not self._resize_in_progress:
            Window.set_system_cursor('arrow')
            self._update_edge_highlighting([])