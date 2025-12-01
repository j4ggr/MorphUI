from typing import Any

from kivy.event import EventDispatcher
from kivy.properties import ObjectProperty
from kivy.effects.scroll import ScrollEffect


__all__ = [
    'MorphScrollSyncBehavior',]


class MorphScrollSyncBehavior(EventDispatcher):
    """A behavior that enables synchronization of scroll positions with 
    other scrollable widgets.
    
    This behavior can be mixed into scrollable widgets to synchronize
    their horizontal and/or vertical scroll positions with other
    scrollable widgets. When this widget's scroll position changes, it
    will automatically update the scroll position of the target widgets.
    
    The synchronization is one-way from this widget to the target
    widgets. To achieve bidirectional synchronization, both widgets
    should include this behavior and reference each other as sync
    targets.
    
    Examples
    --------
    Synchronize two RecycleViews:
    
    ```python
    from morphui.uix.recycleview import MorphRecycleView
    from morphui.uix.behaviors import MorphScrollSyncBehavior
    
    class SyncRecycleView(MorphScrollSyncBehavior, MorphRecycleView):
        pass
    
    # Create two synchronized RecycleViews
    view1 = SyncRecycleView(data=[{'text': f'Item {i}'} for i in range(100)])
    view2 = SyncRecycleView(data=[{'text': f'Other {i}'} for i in range(100)])
    
    # Synchronize both directions
    view1.sync_x_target = view2
    view1.sync_y_target = view2
    view2.sync_x_target = view1
    view2.sync_y_target = view1
    ```
    
    Synchronize only horizontal scrolling:
    
    ```python
    table_header = SyncRecycleView(...)
    table_body = SyncRecycleView(...)
    
    # Only sync horizontal scrolling from body to header
    table_body.sync_x_target = table_header
    ```
    """

    sync_x_target = ObjectProperty(None, allownone=True)
    """The target widget to synchronize horizontal scrolling with.
    
    When this widget's horizontal scroll position (scroll_x) changes,
    the target widget's scroll_x will be automatically updated to match.
    The target widget must have a 'scroll_x' property.

    :attr:`sync_x_target` is a :class:`~kivy.properties.ObjectProperty`
    and defaults to `None`.
    """

    sync_y_target = ObjectProperty(None, allownone=True)
    """The target widget to synchronize vertical scrolling with.
    
    When this widget's vertical scroll position (scroll_y) changes,
    the target widget's scroll_y will be automatically updated to match.
    The target widget must have a 'scroll_y' property.
    
    :attr:`sync_y_target` is a :class:`~kivy.properties.ObjectProperty`
    and defaults to `None`.
    """
    
    effect_cls = ObjectProperty(ScrollEffect)
    """The scroll effect class to use for this widget.

    This property defines the class used to create scroll effects
    for this widget.
    
    By default, it is set to 
    :class:`kivy.effects.scroll.ScrollEffect`, which does not allow
    scroll beyond the content boundaries.
    """

    def __init__(self, **kwargs) -> None:
        """Initialize the scroll sync behavior.
        
        Sets up event bindings to monitor scroll position changes and
        synchronize with target widgets.
        """
        super().__init__(**kwargs)
        
        self.bind(
            scroll_x=self._on_scroll_x_change,
            scroll_y=self._on_scroll_y_change)

    def _on_scroll_x_change(self, instance: Any, value: float) -> None:
        """Handle horizontal scroll position changes.
        
        This private method is called when the widget's scroll_x 
        property changes. It synchronizes the horizontal scroll position
        with the target widget if one is set.
        
        Parameters
        ----------
        instance : Any
            The widget instance that triggered the scroll change.
        value : float
            The new horizontal scroll position (0.0 to 1.0).
        """
        if self.sync_x_target is None:
            return
        
        if self.sync_x_target.scroll_x != value:
            self.sync_x_target.scroll_x = value

    def _on_scroll_y_change(self, instance: Any, value: float) -> None:
        """Handle vertical scroll position changes.
        
        This private method is called when the widget's scroll_y 
        property changes. It synchronizes the vertical scroll position 
        with the target widget if one is set.
        
        Parameters
        ----------
        instance : Any
            The widget instance that triggered the scroll change.
        value : float
            The new vertical scroll position (0.0 to 1.0).
        """
        if self.sync_y_target is None:
            return
        
        if self.sync_y_target.scroll_y != value:
            self.sync_y_target.scroll_y = value

    def set_sync_targets(
            self, x_target: Any = None, y_target: Any = None) -> None:
        """Convenience method to set both sync targets at once.
        
        This method provides a convenient way to set both horizontal and
        vertical sync targets in a single call.
        
        Parameters
        ----------
        x_target : Any, optional
            The widget to synchronize horizontal scrolling with.
            Must have a 'scroll_x' property. Defaults to None.
        y_target : Any, optional
            The widget to synchronize vertical scrolling with.
            Must have a 'scroll_y' property. Defaults to None.
            
        Examples
        --------
        ```python
        # Set both targets
        widget.set_sync_targets(x_target=header_view, y_target=sidebar_view)
        
        # Set only horizontal sync
        widget.set_sync_targets(x_target=header_view)
        
        # Clear both targets
        widget.set_sync_targets()
        ```
        """
        if x_target is not None:
            self.sync_x_target = x_target
        if y_target is not None:
            self.sync_y_target = y_target

    def clear_sync_targets(self) -> None:
        """Clear both sync targets to disable synchronization.
        
        This method removes both horizontal and vertical sync targets,
        effectively disabling scroll synchronization for this widget.
        """
        self.sync_x_target = None
        self.sync_y_target = None