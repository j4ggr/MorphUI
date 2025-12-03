"""Comprehensive sizing behaviors for Kivy widgets.

This module provides all size-related functionality through three main behaviors:
- Size bounds/constraints (minimum and maximum size limits)
- Interactive resizing (drag to resize with mouse)
- Auto-sizing (content-driven automatic sizing)

The sizing behaviors support:
- Lower and upper bound size constraints
- Edge and corner resizing with visual feedback
- Automatic sizing based on content and children
- Cursor changes and hover effects for resize
- Aspect ratio preservation
- Event system for resize and auto-size operations
"""
from typing import Any
from typing import List
from typing import Tuple

from kivy.event import EventDispatcher
from kivy.metrics import dp
from kivy.properties import ListProperty
from kivy.properties import AliasProperty
from kivy.properties import BooleanProperty
from kivy.properties import VariableListProperty
from kivy.core.window import Window
from kivy.input.motionevent import MotionEvent

from morphui.constants import NAME

from morphui.utils import clamp
from morphui.utils import FrozenGeometry

from .hover import MorphHoverEnhancedBehavior
from .layer import MorphOverlayLayerBehavior


__all__ = [
    'MorphSizeBoundsBehavior',
    'MorphAutoSizingBehavior', 
    'MorphResizeBehavior',
]


class MorphSizeBoundsBehavior:
    """A behavior that provides size constraint functionality.
    
    This behavior adds lower and upper bound properties for constraining
    widget dimensions. It automatically resolves these bounds considering
    the widget's inherent minimum and maximum dimensions, providing a
    clean interface for size constraint enforcement.
    
    Features
    --------
    - **Lower Bounds**: Minimum size constraints with fallback to inherent minimums
    - **Upper Bounds**: Maximum size constraints with infinity fallback
    - **Automatic Resolution**: Computed properties handle constraint logic
    - **Flexible Configuration**: Disable constraints with negative values
    
    Properties
    ----------
    - :attr:`size_lower_bound`: Minimum width and height constraints
    - :attr:`size_upper_bound`: Maximum width and height constraints
    - :attr:`_resolved_size_lower_bound`: Computed lower bounds (read-only)
    - :attr:`_resolved_size_upper_bound`: Computed upper bounds (read-only)
    
    Examples
    --------
    Basic size-constrained widget:
    
    ```python
    from kivy.uix.widget import Widget
    from morphui.uix.behaviors.sizing import MorphSizeBoundsBehavior
    
    class ConstrainedWidget(MorphSizeBoundsBehavior, Widget):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            # Set minimum size to 100x50, maximum size to 500x300
            self.size_lower_bound = [100, 50]
            self.size_upper_bound = [500, 300]
            
        def constrain_size(self, new_size):
            from morphui.utils import clamp
            width = clamp(new_size[0], 
                         self._resolved_size_lower_bound[0],
                         self._resolved_size_upper_bound[0])
            height = clamp(new_size[1],
                          self._resolved_size_lower_bound[1], 
                          self._resolved_size_upper_bound[1])
            return (width, height)
    ```
    
    Using with negative values to disable constraints:
    
    ```python
    # Only constrain width, not height
    widget.size_lower_bound = [100, -1]  # Min width 100, no min height
    widget.size_upper_bound = [500, -1]  # Max width 500, no max height
    ```
    """

    size_lower_bound = VariableListProperty([-1, -1], length=2)
    """Lower bound size constraints [width, height].
    
    Prevents the widget from being resized smaller than these dimensions.
    Useful for maintaining usability and preventing widgets from becoming
    too small to interact with. Use [0, 0] to disable minimum size
    constraints. If a negative value is specified for a dimension, the 
    widget's inherent minimum size will be used.
    
    :attr:`size_lower_bound` is a :class:`~kivy.properties.VariableListProperty`
    and defaults to [-1, -1].
    """

    _resolved_size_lower_bound = AliasProperty(
        lambda self: (
            (self.size_lower_bound[0] if self.size_lower_bound[0] >= 0 else
                getattr(self, 'minimum_width', 0)),
            (self.size_lower_bound[1] if self.size_lower_bound[1] >= 0 else
                getattr(self, 'minimum_height', 0))),
        bind=['size_lower_bound'],
        cache=True)
    """Resolved lower bound size considering widget's minimum dimensions.

    This property computes the effective minimum size by combining
    :attr:`size_lower_bound` with the widget's inherent minimum dimensions
    (`minimum_width` and `minimum_height`). It ensures that the widget
    cannot be resized below its functional limits if no explicit minimum
    size is set.

    :attr:`_resolved_size_lower_bound` is a
    :class:`~kivy.properties.AliasProperty` and is read-only.
    """

    size_upper_bound = VariableListProperty([-1, -1], length=2)
    """Upper bound size constraints [width, height].
    
    Prevents the widget from being resized larger than these dimensions.
    Use [-1, -1] to disable maximum size constraints.
    
    :attr:`size_upper_bound` is a :class:`~kivy.properties.VariableListProperty`
    and defaults to [-1, -1].
    """

    _resolved_size_upper_bound = AliasProperty(
        lambda self: (
            (self.size_upper_bound[0] if self.size_upper_bound[0] >= 0 else
                float('inf')),
            (self.size_upper_bound[1] if self.size_upper_bound[1] >= 0 else
                float('inf'))),
        bind=['size_upper_bound'],
        cache=True)
    """Resolved upper bound size considering widget's maximum dimensions.

    This property gets the effective maximum size by combining
    :attr:`size_upper_bound` with infinity for any dimension not 
    explicitly set. It ensures that there is no upper limit on resizing
    if no maximum size is defined.

    :attr:`_resolved_size_upper_bound` is a
    :class:`~kivy.properties.AliasProperty` and is read-only.
    """

    def __init__(self, **kwargs) -> None:
        # Bind to minimum/maximum properties if they exist on the widget
        super().__init__(**kwargs)
    
    def _update_size_bounds_bindings(self) -> None:
        """Update bindings for size bounds properties.
        
        This method ensures that the resolved size bounds are updated
        when the widget's inherent minimum/maximum properties change.
        It safely handles cases where these properties don't exist.
        
        Note: This method is called during initialization but doesn't
        recreate AliasProperties since they can't be reassigned.
        """
        # The AliasProperties are already defined with getattr fallbacks
        # so they will work correctly even if minimum_width/height don't exist
        pass
    
    def constrain_size(self, size: Tuple[float, float]) -> Tuple[float, float]:
        """Apply size bounds constraints to a given size.
        
        This convenience method applies both lower and upper bound constraints
        to a size tuple, returning the constrained dimensions.
        
        Parameters
        ----------
        size : Tuple[float, float]
            The size to constrain (width, height)
            
        Returns
        -------
        Tuple[float, float]
            The constrained size (width, height)
            
        Examples
        --------
        ```python
        # Constrain a proposed size
        new_size = (80, 600)  # Too small width, too large height
        constrained = self.constrain_size(new_size)
        # Returns (100, 300) if bounds are [100, 50] to [500, 300]
        ```
        """
        width = clamp(
            size[0], 
            self._resolved_size_lower_bound[0],
            self._resolved_size_upper_bound[0])
        height = clamp(
            size[1],
            self._resolved_size_lower_bound[1], 
            self._resolved_size_upper_bound[1])
        return (width, height)


class MorphAutoSizingBehavior(EventDispatcher):
    """Behavior for automatic widget sizing based on content.
    
    This behavior provides three boolean properties that enable automatic 
    sizing of widgets based on their content and children. It can 
    automatically adjust width, height, or both dimensions to fit the 
    minimum required size.
    
    Features
    --------
    - **Auto Width**: Automatically adjust width to fit content
    - **Auto Height**: Automatically adjust height to fit content  
    - **Combined Auto Size**: Automatically adjust both dimensions
    - **Text Integration**: Special handling for text-based widgets
    - **Content Adaptation**: Adapts to minimum/maximum size constraints
    
    Properties
    ----------
    - :attr:`auto_width`: Enable automatic width adjustment
    - :attr:`auto_height`: Enable automatic height adjustment
    - :attr:`auto_size`: Enable both width and height adjustment
    
    Examples
    --------
    Auto-sizing label:
    
    ```python
    from kivy.uix.label import Label
    from morphui.uix.behaviors.sizing import MorphAutoSizingBehavior
    
    class AutoLabel(MorphAutoSizingBehavior, Label):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            self.auto_size = True  # Adjust both width and height
    ```
    
    Auto-width button:
    
    ```python
    from kivy.uix.button import Button
    from morphui.uix.behaviors.sizing import MorphAutoSizingBehavior
    
    class AutoButton(MorphAutoSizingBehavior, Button):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            self.auto_width = True  # Only adjust width
    ```
    
    One-time auto-sizing widget:
    
    ```python
    from kivy.uix.label import Label
    from morphui.uix.behaviors.sizing import MorphAutoSizingBehavior
    
    class OnceAutoLabel(MorphAutoSizingBehavior, Label):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            # Size both dimensions once, then maintain fixed size
            self.auto_width = True
            self.auto_height = True
            self.auto_size_once = True
    
    class OnceAutoWidthButton(MorphAutoSizingBehavior, Button):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            # Size width once based on text, keep height flexible
            self.auto_width = True  # Only width will be calculated once
            self.auto_size_once = True
    ```
    """

    auto_width: bool = BooleanProperty(False)
    """Automatically adjust widget width to minimum required size.
    
    When True, the widget's width will be automatically calculated and 
    set to the minimum size required to accommodate all its content and 
    children. This is useful for creating widgets that adapt their width 
    based on their packed content, such as buttons that resize based on 
    text length or containers that fit their child widgets.
    
    :attr:`auto_width` is a :class:`~kivy.properties.BooleanProperty` 
    and defaults to False.
    """

    auto_height: bool = BooleanProperty(False)
    """Automatically adjust widget height to minimum required size.
    
    When True, the widget's height will be automatically calculated and 
    set to the minimum size required to accommodate all its content and 
    children. This is useful for creating widgets that adapt their 
    height based on their packed content, such as labels that resize 
    based on text height or containers that fit their child widgets 
    vertically.
    
    :attr:`auto_height` is a :class:`~kivy.properties.BooleanProperty` 
    and defaults to False.
    """

    def _get_auto_size(self) -> Tuple[bool, bool]:
        """Get combined auto size as a tuple or single bool.
        
        This method returns the combined auto size state. The return
        value is a tuple of two booleans representing
        (:attr:`auto_width`, :attr:`auto_height`). This method is used
        by the AliasProperty.
        """
        return (self.auto_width, self.auto_height)
    
    def _set_auto_size(self, value: bool | Tuple[bool, bool]) -> None:
        """Set combined auto size from a tuple or single bool.
        
        This method sets both auto_width and auto_height based on the
        provided value. If a single boolean is given, both dimensions
        are set to that value. If a tuple is provided, the first element
        sets auto_width and the second sets auto_height. The method
        is internal and used by the AliasProperty.
        """
        value = (value, value) if isinstance(value, bool) else value
        assert len(value) == 2, "auto_size must be a bool or tuple of two bools"
        self.auto_width, self.auto_height = value

    auto_size: Tuple[bool, bool] = AliasProperty(
        _get_auto_size,
        _set_auto_size,
        bind=('auto_width', 'auto_height'))
    """Automatically adjust both width and height to minimum required 
    size.
    
    When True, both the widget's width and height will be automatically 
    calculated and set to the minimum size required to accommodate all 
    its content and children. This is useful for creating widgets that 
    fully adapt their size based on their packed content.

    Note that setting :attr:`auto_size` to True will set both 
    :attr:`auto_width` and :attr:`auto_height` to True. Conversely,
    setting :attr:`auto_size` to False will set both :attr:`auto_width` 
    and :attr:`auto_height` to False. You can also set :attr:`auto_size`
    to a tuple of two booleans to independently control width and 
    height.

    :attr:`auto_size` is a :class:`~kivy.properties.AliasProperty` and 
    defaults to (False, False).
    """

    auto_size_once: bool = BooleanProperty(False)
    """Automatically adjust size once during initialization based on
    current auto_width and auto_height settings, then disable.
    
    When True, the widget will automatically calculate and set its size
    based on the current values of :attr:`auto_width` and
    :attr:`auto_height` during initialization, then disable those auto
    sizing properties while keeping the corresponding size_hint
    dimensions set to None. This is useful for widgets that need to be
    sized based on their content initially but should maintain a fixed
    size afterward.
    
    The behavior respects the individual settings:
    - If :attr:`auto_width` is True, width will be calculated once then 
      disabled
    - If :attr:`auto_height` is True, height will be calculated once
      then disabled
    - If both are True, both dimensions will be calculated once then
      disabled
    
    :attr:`auto_size_once` is a
    :class:`~kivy.properties.BooleanProperty` and defaults to False.
    """

    _original_size_hint: Tuple[float | None, float | None] = (1.0, 1.0)
    """Internal storage for the original size_hint before auto sizing.
    This is used to restore the size_hint when auto sizing is disabled.
    """

    _original_size : Tuple[float, float] = (0, 0)
    """Internal storage for the original size before auto sizing.
    This is used to restore the size when auto sizing is disabled.
    """

    _has_texture_size: bool | None = None
    """Cache whether the widget has a texture_size attribute. This is
    used to optimize checks for text-based widgets that can use
    texture_size for auto sizing.
    """

    def __init__(self, **kwargs) -> None:
        self.register_event_type('on_auto_size_updated')
        super().__init__(**kwargs)
        
        if self.auto_size_once:
            self.apply_auto_sizing(self.auto_width, self.auto_width)
            self.auto_width = False
            self.auto_height = False

        self._original_size = self.size
        self._original_size_hint = self.size_hint
        
        if self.has_texture_size and hasattr(self, 'text_size'):
            self.bind(text=self._update_text_size)
            self.bind(texture_size=self._update_text_size)

        if hasattr(self, 'minimum_width') and hasattr(self, 'minimum_height'):
            self.fbind('minimum_width', self._update_size)
            self.fbind('minimum_height', self._update_size)
        elif self.has_texture_size:
            self.fbind('texture_size', self._update_size)
        for prop in ('auto_width', 'auto_height'):
            self.fbind(prop, self._update_auto_sizing, prop=prop)
        if hasattr(self, 'maximum_width'):
            self.fbind('maximum_width', self._update_size)
        if hasattr(self, 'maximum_height'):
            self.fbind('maximum_height', self._update_size)

        self.refresh_auto_sizing()
    
    @property
    def has_texture_size(self) -> bool:
        """Check if the widget has a texture_size attribute.

        This property is used to determine if the widget can use
        texture_size for auto sizing. It returns True if the widget
        has a texture_size attribute, which is common for text-based
        widgets like Label.
        """
        if self._has_texture_size is None:
            self._has_texture_size = hasattr(self, 'texture_size')
        return self._has_texture_size

    def _update_size(self, *args) -> None:
        """Update size based on current auto sizing settings.

        This method adjusts the widget's width and/or height based on
        the current values of :attr:`auto_width` and :attr:`auto_height`.
        It uses texture_size if available, otherwise falls back to
        minimum_width and minimum_height.

        This method is called whenever the relevant size properties
        change, ensuring that the widget's size remains consistent with
        its content.
        """
        if not self.auto_width and not self.auto_height:
            return None
        
        width, height = self._original_size
        if self.auto_width:
            if self.has_texture_size:
                width = self.texture_size[0]
            width = getattr(self, 'minimum_width', width)
            if getattr(self, 'maximum_width', None) is not None:
                width = min(width, self.maximum_width)

        if self.auto_height:
            if self.has_texture_size:
                height = self.texture_size[1]
            height = getattr(self, 'minimum_height', height)
            if getattr(self, 'maximum_height', None) is not None:
                height = min(height, self.maximum_height)

        if self.size_hint[0] is None:
            self.width = width
        if self.size_hint[1] is None:
            self.height = height
    
    def _update_text_size(
            self, instance: Any, texture_size: Tuple[float, float]) -> None:
        """Update text_size to match current width when auto_width is 
        enabled. Only applies if the widget has a text_size attribute.
        """
        if not self.auto_width and not self.auto_height:
            return None
        
        w_text, h_text = None, None

        if self.auto_height:
            h_text = self.texture_size[1]
            self.text_size = (None, h_text) # update height first and let width adjust
            self.texture_update() # ensure texture_size is updated

        if self.auto_width:
            w_text = self.texture_size[0]
        
        self.text_size = (w_text, h_text)
        self.texture_update()

    def _update_auto_sizing(
            self, instance: Any, value: bool, prop: str) -> None:
        """Update auto sizing based on property changes.

        This method is called whenever one of the auto sizing properties
        changes. It ensures that the appropriate sizing adjustments are
        made to the widget. If :attr:`auto_size` is changed, it sets
        both :attr:`auto_width` and :attr:`auto_height` to the same
        value, triggering their respective handlers.

        Parameters
        ----------
        instance : Any
            The widget instance that triggered the event.
        value : bool
            The new value of the property that changed.
        prop : str
            The name of the property that changed. One of 'auto_size',
            'auto_width', 'auto_height'.
        """
        self.apply_auto_sizing(self.auto_width, self.auto_height)

    def apply_auto_sizing(self, auto_width: bool, auto_height: bool) -> None:
        """Enforce auto sizing based on provided flags. This will
        not change the property values, but will apply the sizing
        adjustments as if the properties were set.

        This method is responsible for applying the appropriate sizing
        adjustments to the widget based on the provided flags. It stores
        the original size and size_hint before making any changes,
        allowing for restoration when auto sizing is disabled.

        Parameters
        ----------
        auto_width : bool
            Whether to apply auto width sizing.
        auto_height : bool
            Whether to apply auto height sizing.
        """
        if auto_width:
            self.size_hint_x = None
        else:
            self.size_hint_x = self._original_size_hint[0]

        if auto_height:
            self.size_hint_y = None
        else:
            self.size_hint_y = self._original_size_hint[1]
        
        self._update_size()
        self.dispatch('on_auto_size_updated')

    def refresh_auto_sizing(self) -> None:
        """Re-apply the current auto sizing settings.

        This method can be called to refresh the auto sizing behavior,
        for example after dynamic changes to the widget that may affect
        sizing. It re-applies the sizing adjustments based on the current
        values of :attr:`auto_width` and :attr:`auto_height`.

        This method preserves the original size and size_hint
        before re-applying the sizing adjustments, ensuring that the
        widget can return to its original size if needed.
        """
        self.apply_auto_sizing(self.auto_width, self.auto_height)
        if self.has_texture_size and hasattr(self, 'text_size'):
            self._update_text_size(self, self.texture_size)

    def on_auto_size_updated(self, *args) -> None:
        """Event fired after auto sizing has been applied or refreshed.

        This event can be used to perform additional actions after the
        widget's size has been adjusted based on its content. It is
        triggered at the end of the :meth:`apply_auto_sizing` method.
        """
        pass


class MorphResizeBehavior(
        MorphSizeBoundsBehavior,
        MorphHoverEnhancedBehavior,
        MorphOverlayLayerBehavior):
    """A behavior that enables widgets to be resized by dragging edges 
    and corners.
    
    This behavior combines size bounds, enhanced hover detection, and overlay 
    layer functionality to provide interactive resizing capabilities. It
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
    - **Size Constraints**: Minimum and maximum size limits via inheritance
    - **Aspect Ratio**: Optional aspect ratio preservation
    - **Animation**: Smooth transitions for visual feedback
    - **Events**: Comprehensive event system for resize operations
    
    Events
    ------
    - :meth:`on_resize_start`: Fired when resize operation begins
    - :meth:`on_resize_progress`: Fired during resize (real-time updates)
    - :meth:`on_resize_end`: Fired when resize operation completes
    
    Properties
    ----------
    - :attr:`resize_enabled`: Enable/disable resize functionality
    - :attr:`resizable_edges`: List of edges that can be resized
    - :attr:`size_lower_bound`: Minimum width and height constraints (inherited)
    - :attr:`size_upper_bound`: Maximum width and height constraints (inherited)
    - :attr:`preserve_aspect_ratio`: Whether to maintain aspect ratio
    
    Examples
    --------
    Basic resizable widget:
    
    ```python
    from kivy.uix.widget import Widget
    from morphui.uix.behaviors.sizing import MorphResizeBehavior
    
    class ResizableWidget(MorphResizeBehavior, Widget):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            self.size = (200, 150)
            self.pos = (100, 100)
            # Set size constraints
            self.size_lower_bound = [50, 50]
            self.size_upper_bound = [400, 300]
            
        def on_resize_start(self, edge_or_corner):
            print(f"Starting resize from {edge_or_corner}")
            
        def on_resize_end(self, edge_or_corner):
            print(f"Finished resizing")
    ```
    
    Resizable widget with aspect ratio preservation:
    
    ```python
    class AspectResizableWidget(MorphResizeBehavior, Widget):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            self.preserve_aspect_ratio = True
            self.size_lower_bound = [100, 75]  # 4:3 ratio minimum
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

        new_size = self.constrain_size((w, h))
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
        def on_resize_progress(self, edge_or_corner, new_size, new_pos):
            # Custom validation
            if new_size[0] < 100:
                return  # Don't allow width less than 100
                
            # Apply resize
            super().on_resize_progress(edge_or_corner, new_size, new_pos)
            
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