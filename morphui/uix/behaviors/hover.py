"""Hover behavior for Kivy widgets.
This module provides a base class `MorphHoverBehavior` that can be mixed
into any Kivy widget to add hover functionality. It detects when the
mouse is hovering over the widget and its edges.

It also provides events for mouse enter and leave, as well as edge
hover events. You can enable or disable hover behavior using the
:attr:`allow_hover` property.
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


__all__ = ['MorphHoverBehavior']


class MorphHoverBehavior(EventDispatcher):
    """Base class for widgets with hover behavior.

    This class provides hover events for mouse enter and leave. It also 
    detects when the mouse is hovering over the edges and corners of the
    widget. You can enable or disable hover behavior using the 
    :attr:`allow_hover` property.

    The class provides the following events that you can override in
    subclasses:
    - :meth:`on_enter`: Fired when the mouse enters the widget.
    - :meth:`on_leave`: Fired when the mouse leaves the widget.
    - :meth:`on_enter_edge`: Fired when the mouse enters any edge of
      the widget.
    - :meth:`on_leave_edge`: Fired when the mouse leaves any edge of
      the widget.
    - :meth:`on_enter_corner`: Fired when the mouse enters any corner
      of the widget.
    - :meth:`on_leave_corner`: Fired when the mouse leaves any corner
      of the widget.
    
    You can also bind to the following properties to get the current
    hover state:
    - :attr:`hovered`: Indicates whether the mouse is currently
      hovering over the widget.
    - :attr:`hovered_edges`: List of edges currently being hovered
      over. Possible values are 'left', 'right', 'top', 'bottom'.
    - :attr:`hovered_corner`: The corner currently being hovered over.
      Possible values are 'top-left', 'top-right', 'bottom-left',
      'bottom-right' or 'none'.
    - :attr:`left_edge_hovered`: Indicates whether the mouse is
      currently hovering over the left edge of the widget.
    - :attr:`right_edge_hovered`: Indicates whether the mouse is
      currently hovering over the right edge of the widget.
    - :attr:`top_edge_hovered`: Indicates whether the mouse is
      currently hovering over the top edge of the widget.
    - :attr:`bottom_edge_hovered`: Indicates whether the mouse is
      currently hovering over the bottom edge of the widget.
    - :attr:`enter_pos`: Position where the mouse entered the widget
      (in widget coordinates).
    - :attr:`leave_pos`: Position where the mouse left the widget
      (in widget coordinates).
    - :attr:`current_pos`: Current position of the mouse (in widget
      coordinates).
    
    You can customize the edge detection area using the
    :attr:`edge_size` property.
    :attr:`edge_size` is the size of the edge area to detect edge
    hover (in pixels). It defaults to 4 pixels.

    Example
    -------
    ```python
    from kivy.app import App
    from kivy.uix.button import Button
    from kivy.uix.boxlayout import BoxLayout

    from morphui.uix.behaviors.hover import MorphHoverBehavior


    class HoverButton(Button, MorphHoverBehavior):
        '''A button with hover effects.'''

        hovered_text: str = "Hovered widget"

        normal_text: str = "Hover over me"

        def on_enter(self) -> None:
            self.color = (0, 0.8, 0.5, 1)  # Change color on hover
            self.text = self.hovered_text

        def on_leave(self) -> None:
            self.color = (1, 1, 1, 1)  # Reset color when not hovering
            self.text = self.normal_text

        def on_enter_edge(self, edge: str) -> None:
            self.text = f"Hovered {edge} edge"

        def on_leave_edge(self, edge: str) -> None:
            self.text = self.hovered_text if self.hovered else self.normal_text

        def on_enter_corner(self, corner: str) -> None:
            self.text = f"Hovered {corner} corner"

        def on_leave_corner(self, corner: str) -> None:
            self.text = self.hovered_text if self.hovered else self.normal_text


    class HoverApp(App):
        def build(self) -> BoxLayout:
            layout = BoxLayout(padding=100)
            btn = HoverButton(text="Hover over me")
            layout.add_widget(btn)
            return layout
            
    if __name__ == "__main__":
        HoverApp().run()
    """

    allow_hover = BooleanProperty(True)
    """Enable or disable hover behavior.
    
    :attr:`allow_hover` is a :class:`~kivy.properties.BooleanProperty` 
    and defaults to `True`."""

    hovered = BooleanProperty(False)
    """Indicates whether the mouse is currently hovering over the 
    widget.
    
    :attr:`hovered` is a :class:`~kivy.properties.BooleanProperty` and 
    defaults to `False`."""

    hovered_edges: List[str] = ListProperty([])
    """List of edges currently being hovered over. Possible values are
    'left', 'right', 'top', 'bottom'.

    :attr:`hovered_edges` is a :class:`~kivy.properties.ListProperty`
    and defaults to an empty list.
    """

    hovered_corner: str = StringProperty(
        'none',
        options=(
            'top-left', 'top-right', 'bottom-left', 'bottom-right', 'none'))
    """The corner currently being hovered over. Possible values are
    'top-left', 'top-right', 'bottom-left', 'bottom-right' or 'none'.

    :attr:`hovered_corner` is a :class:`~kivy.properties.StringProperty`
    and defaults to 'none'.
    """

    _last_hovered_corner: str = 'none'
    """Internal attribute to track the last hovered corner."""

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

    enter_pos = Tuple[float, float]
    """Position where the mouse entered the widget (in widget 
    coordinates)."""

    leave_pos = Tuple[float, float]
    """Position where the mouse left the widget (in widget coordinates)."""

    current_pos = Tuple[float, float]
    """Current position of the mouse (in widget coordinates)."""

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        Window.bind(mouse_pos=self.on_mouse_pos)
        self.register_event_type('on_enter')
        self.register_event_type('on_leave')
        self.register_event_type('on_enter_edge')
        self.register_event_type('on_leave_edge')
        self.register_event_type('on_enter_corner')
        self.register_event_type('on_leave_corner')

    @property
    def is_displayed(self) -> bool:
        """Check if the widget is displayed i.e., has a parent and is in 
        the widget tree (read-only)."""
        return bool(self.get_root_window())
    
    @property
    def EDGES(self) -> Tuple[str, str, str, str]:
        """Tuple of valid edge names."""
        return ('left', 'right', 'top', 'bottom')
    
    @property
    def CORNERS(self) -> Tuple[str, str, str, str]:
        """Tuple of valid corner names."""
        return ('top-left', 'top-right', 'bottom-left', 'bottom-right')
    
    def get_hovered_corner(self) -> str:
        """Return the corner being hovered over, or 'none' if not 
        hovering over a corner."""
        if not self.hovered or len(self.hovered_edges) != 2:
            return 'none'
        
        return '-'.join(self.hovered_edges[::-1])

    def get_hovered_edges(self) -> List[str]:
        """Return a list of edges currently being hovered over. """
        return [e for e in self.EDGES if getattr(self, f'{e}_edge_hovered')]

    def on_mouse_pos(self, instance: Any, pos: Tuple[float, float]) -> None:
        if not self.is_displayed or not self.allow_hover:
            return

        self.current_pos = self.to_window(*pos)
        inside = self.collide_point(*pos)
        x = self.current_pos[0] - self.x
        y = self.current_pos[1] - self.y

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

        self.hovered_edges = self.get_hovered_edges()
        self._last_hovered_corner = self.hovered_corner
        self.hovered_corner = self.get_hovered_corner()

    def on_hovered(self, instance: Any, hovered: bool) -> None:
        """Event fired when the hover state changes. Dispatches 
        :meth:`on_enter` or :meth:`on_leave`."""
        if hovered:
            self.dispatch('on_enter')
        else:
            self.dispatch('on_leave')

    def _dispatch_edge_event(self, edge: str, hovered: bool) -> None:
        if hovered:
            self.dispatch('on_enter_edge', edge)
        else:
            self.dispatch('on_leave_edge', edge)
    
    def on_left_edge_hovered(self, instance: Any, hovered: bool) -> None:
        """Event fired when the left edge hover state changes. Dispatches 
        :meth:`on_edge_hovered` with the appropriate parameters."""
        self._dispatch_edge_event('left', hovered)
        
    def on_right_edge_hovered(self, instance: Any, hovered: bool) -> None:
        """Event fired when the right edge hover state changes. Dispatches 
        :meth:`on_edge_hovered` with the appropriate parameters."""
        self._dispatch_edge_event('right', hovered)
    
    def on_top_edge_hovered(self, instance: Any, hovered: bool) -> None:
        """Event fired when the top edge hover state changes. Dispatches 
        :meth:`on_edge_hovered` with the appropriate parameters."""
        self._dispatch_edge_event('top', hovered)
    
    def on_bottom_edge_hovered(self, instance: Any, hovered: bool) -> None:
        """Event fired when the bottom edge hover state changes. Dispatches 
        :meth:`on_edge_hovered` with the appropriate parameters."""
        self._dispatch_edge_event('bottom', hovered)
    
    def on_hovered_corner(
            self,
            instance: Any,
            corner: Literal['top-left', 'top-right', 'bottom-left', 'bottom-right', 'none']
            ) -> None:
        """Event fired when the hovered corner changes. Dispatches
        :meth:`on_enter_corner` or :meth:`on_leave_corner`."""
        if corner != self._last_hovered_corner:
            if self._last_hovered_corner != 'none':
                self.dispatch('on_leave_corner', self._last_hovered_corner)
            if corner != 'none':
                self.dispatch('on_enter_corner', corner)

    def on_enter(self) -> None:
        """Event fired when the mouse enters the widget. Override to add 
        custom behavior."""
        pass

    def on_leave(self) -> None:
        """Event fired when the mouse leaves the widget. Override to add 
        custom behavior."""
        pass

    def on_enter_edge(
            self,
            edge: Literal['left', 'right', 'top', 'bottom']
            ) -> None:
        """Event fired when the mouse enters any edge of the widget.
        Override to add custom behavior.
        
        Parameters
        ----------
        edge : Literal['left', 'right', 'top', 'bottom']
            The edge being hovered over. One of 'left', 'right', 'top', 
            or 'bottom'.
        """
        pass

    def on_leave_edge(
            self,
            edge: Literal['left', 'right', 'top', 'bottom']
            ) -> None:
        """Event fired when the mouse leaves any edge of the widget.
        Override to add custom behavior.
        
        Parameters
        ----------
        edge : Literal['left', 'right', 'top', 'bottom']
            The edge being left. One of 'left', 'right', 'top', or 
            'bottom'.
        """
        pass

    def on_enter_corner(
            self,
            corner: Literal['top-left', 'top-right', 'bottom-left', 'bottom-right']
            ) -> None:
        """Event fired when the mouse enters any corner of the widget.
        Override to add custom behavior.
        
        Parameters
        ----------
        corner : Literal['top-left', 'top-right', 'bottom-left', 'bottom-right']
            The corner being hovered over. One of 'top-left', 
            'top-right', 'bottom-left', or 'bottom-right'.
        """
        pass

    def on_leave_corner(
            self,
            corner: Literal['top-left', 'top-right', 'bottom-left', 'bottom-right']
            ) -> None:
        """Event fired when the mouse leaves any corner of the widget.
        Override to add custom behavior.
        
        Parameters
        ----------
        corner : Literal['top-left', 'top-right', 'bottom-left', 'bottom-right']
            The corner being left. One of 'top-left', 'top-right', 
            'bottom-left', or 'bottom-right'.
        """
        pass