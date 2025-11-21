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
from typing import List
from typing import Tuple

from kivy.metrics import dp
from kivy.properties import ListProperty
from kivy.properties import AliasProperty
from kivy.properties import BooleanProperty
from kivy.core.window import Window
from kivy.input.motionevent import MotionEvent

from morphui.constants import NAME

from morphui.utils import clamp
from morphui.utils import FrozenGeometry

from .hover import MorphHoverEnhancedBehavior
from .layer import MorphOverlayLayerBehavior


__all__ = [
    'MorphResizeBehavior',
]


class MorphResizeBehavior(
        MorphHoverEnhancedBehavior,
        MorphOverlayLayerBehavior):
    """A behavior that enables widgets to be resized by dragging edges 
    and corners.
    
    This behavior combines enhanced hover detection with overlay layer
    functionality to provide interactive resizing capabilities. It
    automatically detects when the mouse is over resizable edges or
    corners and provides visual feedback through edge highlighting and
    cursor changes.
    
    Features
    --------
    - **Edge Resizing**: Resize by dragging left, right, top, or bottom
      edges
    - **Corner Resizing**: Resize diagonally by dragging corners
    - **Visual Feedback**: Highlighted edges and appropriate cursor
      changes
    - **Size Constraints**: Minimum and maximum size limits
    - **Aspect Ratio**: Optional aspect ratio preservation
    - **Animation**: Smooth transitions for visual feedback
    - **Events**: Comprehensive event system for resize operations
    
    Events
    ------
    - :meth:`on_resize_progress`: Fired during resize (real-time updates)
    
    Properties
    ----------
    - :attr:`resize_enabled`: Enable/disable resize functionality
    - :attr:`resizable_edges`: List of edges that can be resized
    - :attr:`min_size`: Minimum width and height constraints
    - :attr:`max_size`: Maximum width and height constraints
    - :attr:`preserve_aspect_ratio`: Whether to maintain aspect ratio
      animations
    
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
            
        def on_resizing(self, instance, resizing):
            if resizing:
                print(f"Starting resize from {self.resize_edge_or_corner}")
            else:
                print(f"Finished resizing")
    ```
    """

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

    min_size: List[float | None] = ListProperty([None], length=2)
    """Minimum size constraints [width, height].
    
    Prevents the widget from being resized smaller than these dimensions.
    Useful for maintaining usability and preventing widgets from becoming
    too small to interact with. Use [0, 0] to disable minimum size
    constraints. If None is specified for a dimension, the widget's
    inherent minimum size will be used.
    
    :attr:`min_size` is a :class:`~kivy.properties.ListProperty`
    and defaults to [None, None].
    """

    _resolved_min_size: Tuple[float, float] = AliasProperty(
        lambda self: (
            self.min_size[0] or self.minimum_width,
            self.min_size[1] or self.minimum_height),
        bind=['min_size', 'minimum_width', 'minimum_height'],
        cache=True)
    """Resolved minimum size considering widget's minimum dimensions.

    This property computes the effective minimum size by combining
    :attr:`min_size` with the widget's inherent minimum dimensions
    (`minimum_width` and `minimum_height`). It ensures that the widget
    cannot be resized below its functional limits if no explicit minimum
    size is set.

    :attr:`_resolved_min_size` is a
    :class:`~kivy.properties.AliasProperty` and is read-only.
    """

    max_size: List[float | None] = ListProperty([None], length=2)
    """Maximum size constraints [width, height].
    
    Prevents the widget from being resized larger than these dimensions.
    Use [None, None] to disable maximum size constraints.
    
    :attr:`max_size` is a :class:`~kivy.properties.ListProperty`
    and defaults to [None, None].
    """

    _resolved_max_size: Tuple[float, float] = AliasProperty(
        lambda self: (
            self.max_size[0] or float('inf'),
            self.max_size[1] or float('inf')),
        bind=['max_size'],
        cache=True)
    """Resolved maximum size considering widget's maximum dimensions.

    This property gets the effective maximum size by combining
    :attr:`max_size` with infinity for any dimension not explicitly set.
    It ensures that there is no upper limit on resizing if no maximum
    size is defined.

    :attr:`_resolved_max_size` is a
    :class:`~kivy.properties.AliasProperty` and is read-only.
    """

    preserve_aspect_ratio: bool = BooleanProperty(False)
    """Whether to preserve the widget's aspect ratio during resize.
    
    When True, the widget will maintain its width-to-height ratio during
    resize operations. This is particularly useful for images, video players,
    or other content where aspect ratio is important.
    
    :attr:`preserve_aspect_ratio` is a :class:`~kivy.properties.BooleanProperty`
    and defaults to False.
    """

    resizing: bool = BooleanProperty(False)
    """Indicates whether a resize operation is currently in progress.

    This property is True while the user is actively dragging an edge or
    corner to resize the widget, and False otherwise. It can be used to
    conditionally change behavior or appearance during resize 
    operations. For example, you might want to disable certain 
    interactions while resizing is happening.
    The :class:`morphui.uix.behaviors.states.MorphStateBehavior` 
    listens to this property and so does the 
    :class:`morphui.uix.behaviors.layer.MorphOverlayLayerBehavior`.

    :attr:`resizing` is a :class:`~kivy.properties.BooleanProperty` 
    and defaults to False.
    """

    _resize_reference_geometry: FrozenGeometry
    """Frozen reference geometry for mouse movements when resize 
    operation started."""

    _start_touch_pos: Tuple[float, float] = (0, 0)
    """The mouse position where the resize operation started."""

    _original_size_hint : Tuple[float | None, float | None] = (1.0, 1.0)
    """Internal storage for the original size_hint before resizing.
    This is used to restore the size_hint after resizing."""

    _resize_edge_or_corner: str | None = None
    """The edge or corner being used for current resize operation."""

    _resize_in_progress: bool = False
    """Internal flag indicating if a resize operation is in progress."""

    def __init__(self, **kwargs) -> None:
        self.register_event_type('on_resize_start')
        self.register_event_type('on_resize_progress')
        self.register_event_type('on_resize_end')
        super().__init__(**kwargs)
        
        self.bind(
            hovered_edges=self._update_resize_feedback,
            hovered_corner=self._update_resize_feedback,
            overlay_edge_width=self._update_edge_detection_size,
            overlay_edge_inside=self._update_edge_detection_size,)
        
        self._update_edge_detection_size()

    @property
    def resize_edge_or_corner(self) -> str | None:
        """The edge or corner currently being used for resize operation
        (read-only).
        
        This property is set when a resize operation starts and cleared
        when it ends. It indicates which edge ('left', 'right', 'top',
        'bottom') or corner ('top-left', 'top-right', 'bottom-left',
        'bottom-right') is being dragged to resize the widget.
        If no resize operation is in progress, this will be None.
        """
        return self._resize_edge_or_corner
    
    @property
    def hovered_resizable_edges(self) -> List[str]:
        """List of currently hovered edges that are resizable.
        
        Only edges present in :attr:`resizable_edges` will be included.
        If resize is disabled, this will always be an empty list."""
        if not self.resize_enabled:
            return []
        
        return [e for e in self.hovered_edges if e in self.resizable_edges]
    
    @property
    def hovered_resizable_corner(self) -> str | None:
        """Currently hovered corner if it is resizable, else None."""
        if not self.resize_enabled or self.hovered_corner is None:
            return None
        
        corner_edges = self.hovered_corner.split(NAME.SEP_CORNER)
        if all(edge in self.resizable_edges for edge in corner_edges):
            return self.hovered_corner
    
    def _update_edge_detection_size(self, *args) -> None:
        """Update edge detection size based on current overlay edge width.
        
        This method ensures that the area used for detecting hover over
        edges is always in sync with the visual overlay edge width.
        It is called automatically when the overlay edge width changes.
        """
        if self.overlay_edge_inside:
            self.edge_detection_size = dp(self.overlay_edge_width * 2)
        else:
            self.edge_detection_size = dp(self.overlay_edge_width)

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
        
        if self._resize_in_progress:
            self.resizing = True
        else:
            self.resizing = bool(self.hovered_resizable_edges)
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

    def on_touch_down(self, touch: MotionEvent) -> bool:
        """Handle touch down events for resize operations.

        This method initiates a resize operation if the touch occurs
        over a resizable edge or corner. It sets up the necessary state
        for the resize operation to proceed.

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
        touch.grab(self)
        touch.ud[self] = True
        self._start_resize(touch.pos)
        return True

    def _start_resize(self, touch_pos: Tuple[float, float]) -> None:
        """Internal method to handle the start of a resize operation.
        
        This method sets the resizing state to True. It is called when a
        resize operation is initiated. It also stores the initial
        geometry for reference during the resize.

        Parameters
        ----------
        touch_pos : Tuple[float, float]
            The mouse position where the resize started.
        """
        self._resize_in_progress = True
        self._original_size_hint = self.size_hint
        self.size_hint = (None, None)
        self._resize_reference_geometry = FrozenGeometry.from_widget(self)
        self._start_touch_pos = touch_pos
        
        if self.hovered_resizable_corner is not None:
            self._resize_edge_or_corner = self.hovered_resizable_corner
        else:
            self._resize_edge_or_corner = self.hovered_resizable_edges[0]
        self.dispatch('on_resize_start', self.resize_edge_or_corner)

    def on_touch_move(self, touch: MotionEvent) -> bool:
        """Handle touch move events during resize operations.

        This method updates the size and position of the widget being
        resized based on the current mouse position. It applies size
        constraints and dispatches the appropriate resize event.
        
        Parameters
        ----------
        touch : MotionEvent
            Touch event
            
        Returns
        -------
        bool
            True if touch was handled for resize
        """
        if not self._resize_in_progress:
            return False
            
        self._resize(touch.pos)
        return True

    def _resize(self, mouse_pos: Tuple[float, float]) -> None:
        """Internal method to perform resize calculations and apply
        new dimensions.
        
        This method calculates the new size and position based on the
        current mouse position, applies constraints, and dispatches the
        resize progress event.
        
        Parameters
        ----------
        mouse_pos : Tuple[float, float]
            Current mouse position during resize
        """
        x, y = self._resize_reference_geometry.pos
        w, h = self._resize_reference_geometry.size
        dx = mouse_pos[0] - self._start_touch_pos[0]
        dy = mouse_pos[1] - self._start_touch_pos[1]
        target_ratio = self._resize_reference_geometry.aspect_ratio

        if self.resize_edge_or_corner is not None:
            edges = self.resize_edge_or_corner.split(NAME.SEP_CORNER)
        else:
            edges = []
        for edge in edges:
            if edge == 'left':
                w -= dx
                x += dx
            elif edge == 'right':
                w += dx
            elif edge == 'top':
                h += dy
            elif edge == 'bottom':
                h -= dy
                y += dy

        if self.preserve_aspect_ratio and target_ratio > 0:
            current_ratio = w / h if h > 0 else 1.0

            if round(current_ratio - target_ratio, 3) != 0:
                if current_ratio > target_ratio: 
                    w = h * target_ratio    # Width is too large relative to height
                else: 
                    h = w / target_ratio    # Height is too large relative to width

        w = clamp(w, self._resolved_min_size[0], self._resolved_max_size[0])
        h = clamp(h, self._resolved_min_size[1], self._resolved_max_size[1])
        new_size = (w, h)
        new_pos = (x, y)
        self.dispatch(
            'on_resize_progress', self.resize_edge_or_corner, new_size, new_pos)

    def on_touch_up(self, touch: MotionEvent) -> bool:
        """Handle touch up events to end resize operations.

        This method finalizes the resize operation, resets state, and
        dispatches the resize end event.
        
        Parameters
        ----------
        touch : MotionEvent
            Touch event
            
        Returns
        -------
        bool
            True if touch was handled for resize
        """
        if not self._resize_in_progress:
            return False
            
        touch.ungrab(self)
        self._end_resize()
        return True
    
    def _end_resize(self) -> None:
        """Internal method to handle the end of a resize operation.
        
        This method resets the resizing state and restores the original
        size_hint. It is called when a resize operation is completed.
        """
        self._resize_in_progress = False
        self.size_hint = self._original_size_hint
        self._original_size_hint = (1.0, 1.0)
        self._resize_edge_or_corner = None
        self.dispatch('on_resize_end', self.resize_edge_or_corner)

    def on_resize_start(self, edge_or_corner: str) -> None:
        """Event fired when a resize operation starts.

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

    def on_resize_progress(
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

    def on_leave(self) -> None:
        """Override parent on_leave to reset cursor."""
        super().on_leave()
        if not self._resize_in_progress:
            Window.set_system_cursor('arrow')
            self._update_overlay_layer([])