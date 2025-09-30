from typing import Any
from typing import List
from typing import Tuple

from kivy.event import EventDispatcher
from kivy.properties import NumericProperty
from kivy.properties import BooleanProperty
from kivy.core.window import Window


__all__ = ['HoverBehavior']


class HoverBehavior(EventDispatcher):
    """Base class for widgets with hover behavior.

    This class provides hover events for mouse enter and leave. It also 
    detects when the mouse is hovering over the edges and corners of the
    widget. You can enable or disable hover behavior using the 
    :attr:`allow_hover` property.
    """

    hovered = BooleanProperty(False)
    """Indicates whether the mouse is currently hovering over the 
    widget.
    
    :attr:`hovered` is a :class:`~kivy.properties.BooleanProperty` and 
    defaults to `False`."""

    allow_hover = BooleanProperty(True)
    """Enable or disable hover behavior.
    
    :attr:`allow_hover` is a :class:`~kivy.properties.BooleanProperty` 
    and defaults to `True`."""

    left_edge_hovered = BooleanProperty(False)
    """Indicates whether the mouse is currently hovering over the left 
    edge of the widget.

    :attr:`left_edge_hovered` is a 
    :class:`~kivy.properties.BooleanProperty` and defaults to `False`."""

    right_edge_hovered = BooleanProperty(False)
    """Indicates whether the mouse is currently hovering over the right 
    edge of the widget.

    :attr:`right_edge_hovered` is a 
    :class:`~kivy.properties.BooleanProperty` and defaults to `False`."""

    top_edge_hovered = BooleanProperty(False)
    """Indicates whether the mouse is currently hovering over the top 
    edge of the widget.

    :attr:`top_edge_hovered` is a 
    :class:`~kivy.properties.BooleanProperty` and defaults to `False`."""

    bottom_edge_hovered = BooleanProperty(False)
    """Indicates whether the mouse is currently hovering over the bottom 
    edge of the widget.

    :attr:`bottom_edge_hovered` is a 
    :class:`~kivy.properties.BooleanProperty` and defaults to `False`."""

    edge_size = NumericProperty(4)
    """Size of the edge area to detect edge hover (in pixels).
    
    :attr:`edge_size` is a :class:`~kivy.properties.NumericProperty` and 
    defaults to `4`."""

    enter_pos = Tuple[int, int]
    """Position where the mouse entered the widget (in widget 
    coordinates)."""

    leave_pos = Tuple[int, int]
    """Position where the mouse left the widget (in widget coordinates)."""

    current_pos = Tuple[int, int]
    """Current position of the mouse (in widget coordinates)."""

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        Window.bind(mouse_pos=self.on_mouse_pos)
        self.register_event_type('on_enter')
        self.register_event_type('on_leave')
        self.register_event_type('on_edge_hovered')
        self.register_event_type('on_corner_hovered')

    @property
    def is_displayed(self) -> bool:
        """Check if the widget is displayed i.e., has a parent and is in 
        the widget tree (read-only)."""
        return bool(self.get_root_window())
    
    def hovered_corner(self) -> str | None:
        """Return the corner being hovered over, or None if not hovering 
        over a corner."""
        if self.left_edge_hovered and self.top_edge_hovered:
            return 'top-left'
        if self.right_edge_hovered and self.top_edge_hovered:
            return 'top-right'
        if self.left_edge_hovered and self.bottom_edge_hovered:
            return 'bottom-left'
        if self.right_edge_hovered and self.bottom_edge_hovered:
            return 'bottom-right'
        return None
    
    def hovered_edges(self) -> List[str]:
        """Return a list of edges being hovered over."""
        def hovered(edge: str) -> bool:
            return getattr(self, f'{edge}_edge_hovered')

        edges = [n for n in ('left', 'right', 'top', 'bottom') if hovered(n)]
        return edges

    def on_mouse_pos(self, instance: Any, pos: Tuple[int, int]) -> None:
        if not self.is_displayed or not self.allow_hover:
            return
        
        self.current_pos = self.to_widget(*pos)
        x, y = self.current_pos
        inside = self.collide_point(x, y)

        if inside and not self.hovered:
            self.enter_pos = self.current_pos
            self.hovered = True
        elif not inside and self.hovered:
            self.leave_pos = self.current_pos
            self.hovered = False

        self.left_edge_hovered = inside and (x <= self.edge_size)
        self.right_edge_hovered = inside and (x >= self.width - self.edge_size)
        self.top_edge_hovered = inside and (y >= self.height - self.edge_size)
        self.bottom_edge_hovered = inside and (y <= self.edge_size)

    def on_hovered(self, instance: Any, hovered: bool) -> None:
        """Event fired when the hover state changes. Dispatches 
        :meth:`on_enter` or :meth:`on_leave`."""
        if hovered:
            self.dispatch('on_enter', self.enter_pos)
        else:
            self.dispatch('on_leave', self.leave_pos)

    def _dispatch_edge_hovered(self, edge: str, hovered: bool) -> None:
        if hovered:
            self.dispatch('on_edge_hovered', self.enter_pos, edge)
            corner = self.hovered_corner()
            if corner:
                self.dispatch('on_corner_hovered', self.enter_pos, corner)
    
    def on_left_edge_hovered(self, instance: Any, hovered: bool) -> None:
        """Event fired when the left edge hover state changes. Dispatches 
        :meth:`on_edge_hovered` with the appropriate parameters."""
        self._dispatch_edge_hovered('left', hovered)
        
    def on_right_edge_hovered(self, instance: Any, hovered: bool) -> None:
        """Event fired when the right edge hover state changes. Dispatches 
        :meth:`on_edge_hovered` with the appropriate parameters."""
        self._dispatch_edge_hovered('right', hovered)
    
    def on_top_edge_hovered(self, instance: Any, hovered: bool) -> None:
        """Event fired when the top edge hover state changes. Dispatches 
        :meth:`on_edge_hovered` with the appropriate parameters."""
        self._dispatch_edge_hovered('top', hovered)
    
    def on_bottom_edge_hovered(self, instance: Any, hovered: bool) -> None:
        """Event fired when the bottom edge hover state changes. Dispatches 
        :meth:`on_edge_hovered` with the appropriate parameters."""
        self._dispatch_edge_hovered('bottom', hovered)

    def on_enter(self, pos: Tuple[int, int]) -> None:
        """Event fired when the mouse enters the widget. Override to add 
        custom behavior."""
        pass

    def on_leave(self, pos: Tuple[int, int]) -> None:
        """Event fired when the mouse leaves the widget. Override to add 
        custom behavior."""
        pass

    def on_edge_hovered(self, pos: Tuple[int, int], edge: str) -> None:
        """Event fired when the mouse hovers over any edge of the widget.
        Override to add custom behavior."""
        pass

    def on_corner_hovered(self, pos: Tuple[int, int]) -> None:
        """Event fired when the mouse hovers over any corner of the widget.
        Override to add custom behavior."""
        pass