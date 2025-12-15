from typing import Any
from typing import Literal

from kivy.properties import AliasProperty
from kivy.properties import ObjectProperty
from kivy.properties import StringProperty
from kivy.properties import OptionProperty
from kivy.properties import NumericProperty
from kivy.core.window import Window

from morphui.utils import clamp
from morphui.uix.behaviors import MorphScaleBehavior


__all__ = [
    'MorphMenuMotionBehavior']


class MorphMenuMotionBehavior(MorphScaleBehavior,):
    """Behavior class that adds menu motion functionality to a widget.
    
    This behavior provides properties and methods to manage a menu
    associated with a widget, including tools, open/close state, and
    animation settings.
    
    Notes
    -----
    If the widget also inherits from :class:`MorphSizeBoundsBehavior`,
    this behavior will automatically set the `size_upper_bound` property
    to constrain the menu size within the window bounds when opened.
    """

    caller: Any = ObjectProperty(None)
    """Caller button that opened this menu.
    
    This property holds a reference to the widget that triggered the 
    opening of this toolbar menu. It can be used to manage the position
    and behavior of the menu in relation to the caller button.
    
    :attr:`caller` is a :class:`~kivy.properties.ObjectProperty`
    and defaults to `None`."""

    is_open: bool = AliasProperty(
        lambda self: bool(self.parent),
        bind=['parent'])
    """Flag indicating whether the menu is currently open.

    This property is `True` when the menu is visible and `False`
    when it is closed.

    :attr:`is_open` is a :class:`~kivy.properties.AliasProperty` and is
    read-only."""


    menu_anchor_position: Literal['left', 'center', 'right'] = OptionProperty(
        'center', options=['left', 'center', 'right'])
    """Position of the menu relative to the caller widget.

    This property defines the horizontal alignment of the menu relative
    to the caller button. Options are:
    - 'left': Align the menu's left edge with the caller's left edge
    - 'center': Center the menu horizontally with the caller
    - 'right': Align the menu's right edge with the caller's right edge

    :attr:`menu_anchor_position` is a
    :class:`~kivy.properties.OptionProperty` and defaults to `'center'`.
    """

    menu_opening_direction: Literal['up', 'down'] = OptionProperty(
        'down', options=['up', 'down'])
    """Direction in which the menu opens.

    This property defines the direction in which the menu will open
    relative to the caller button. It can be either 'up' or 'down'.

    :attr:`menu_opening_direction` is a
    :class:`~kivy.properties.OptionProperty` and defaults to `'down'`.
    """

    menu_opening_duration: float = NumericProperty(0.15)
    """Duration of the menu opening animation in seconds.

    This property defines how long the animation takes when the menu
    is opened. It is specified in seconds.
    
    :attr:`menu_opening_duration` is a
    :class:`~kivy.properties.NumericProperty` and defaults to `0.15`."""

    menu_opening_transition: str = StringProperty('out_sine')
    """Transition type for the menu opening animation.

    This property defines the type of transition used during the menu
    opening animation. It should be a valid Kivy transition name.

    :attr:`menu_opening_transition` is a
    :class:`~kivy.properties.StringProperty` and defaults to 
    `'out_sine'`."""

    menu_dismissing_duration: float = NumericProperty(0.15)
    """Duration of the menu dismiss animation in seconds.

    This property defines how long the animation takes when the menu
    is dismissed. It is specified in seconds.

    :attr:`menu_dismiss_duration` is a
    :class:`~kivy.properties.NumericProperty` and defaults to `0.1`."""

    menu_dismissing_transition: str = StringProperty('in_sine')
    """Transition type for the menu dismiss animation.

    This property defines the type of transition used during the menu
    dismiss animation. It should be a valid Kivy transition name.

    :attr:`menu_dismiss_transition` is a
    :class:`~kivy.properties.StringProperty` and defaults to 
    `'in_sine'`."""

    menu_window_margin: float = NumericProperty(8)
    """Margin from the window edges in pixels.

    This property defines the minimum distance (in pixels) that the menu
    should maintain from the edges of the window. This ensures the menu
    remains fully visible and doesn't extend beyond the window bounds.

    :attr:`menu_window_margin` is a
    :class:`~kivy.properties.NumericProperty` and defaults to `8`."""

    def __init__(self, **kwargs) -> None:
        self.register_event_type('on_pre_open')
        self.register_event_type('on_pre_dismiss')
        self.register_event_type('on_open')
        self.register_event_type('on_dismiss')
        super().__init__(**kwargs)
        self.bind(size=self._update_position)
        
    def on_caller(self, instance: Any, caller: Any) -> None:
        """Update the menu position when the caller button changes."""
        self.caller.bind(
            pos=self._update_position,
            size=self._update_position,)

    def _resolve_caller_pos(self) -> tuple[float, float]:
        """Get the caller button position in window coordinates.
        
        This method returns the position of the caller button in window
        coordinates. If the caller is not set, it returns (0, 0)."""
        if self.caller is None:
            return (0, 0)
        
        return self.caller.to_window(*self.caller.pos)
    
    def _resolve_caller_size(self) -> tuple[float, float]:
        """Get the caller button size.
        
        This method returns the size of the caller button. If the caller
        is not set, it returns (0, 0).
        """
        if self.caller is None:
            return (0, 0)
        
        return self.caller.size
    
    def _resolve_pos(self) -> tuple[float, float]:
        """Get the menu position relative to the caller button.
        
        This method calculates the position of the menu based on the
        position and size of the caller button, as well as the specified
        anchor position and opening direction. The position is clamped
        to ensure the menu stays within window bounds with the specified
        margin.
        """
        caller_x, caller_y = self._resolve_caller_pos()
        caller_width, caller_height = self._resolve_caller_size()
        
        match self.menu_anchor_position:
            case 'left':
                x = caller_x - self.width
                match self.menu_opening_direction:
                    case 'down':
                        y = caller_y - self.height + caller_height
                    case 'up':
                        y = caller_y

            case 'center':
                x = caller_x + (caller_width - self.width) / 2
                match self.menu_opening_direction:
                    case 'down':
                        y = caller_y - self.height
                    case 'up':
                        y = caller_y + caller_height

            case 'right':
                x = caller_x + caller_width
                match self.menu_opening_direction:
                    case 'down':
                        y = caller_y - self.height + caller_height
                    case 'up':
                        y = caller_y
        
        margin = self.menu_window_margin
        x = clamp(x, margin, Window.width - self.width - margin)
        y = clamp(y, margin, Window.height - self.height - margin)
        
        return (x, y)
    
    def set_scale_origin(self, *args) -> None:
        """Set the scale origin based on the caller button position and 
        anchor.
        
        This method calculates the scale origin point for the menu
        based on the position and size of the caller button, ensuring 
        that the menu scales from the appropriate point when opened or
        closed.
        """
        caller_x, caller_y = self._resolve_caller_pos()
        caller_width, caller_height = self._resolve_caller_size()

        self.scale_origin = [
            caller_x + caller_width / 2,
            caller_y + caller_height / 2]

    def _update_position(self, *args) -> None:
        """Update the menu position relative to the caller button."""
        self.pos = self._resolve_pos()

    def _add_to_window(self, *args) -> None:
        """Add the menu to the window and update its position.
        
        This method adds the menu widget to the window and updates its
        position based on the caller button. If the widget also inherits
        from :class:`MorphSizeBoundsBehavior`, it will set the
        `size_upper_bound` property to ensure the menu fits within the
        window bounds, respecting the :attr:`menu_window_margin`.
        """
        Window.add_widget(self)
        self._update_position()
        if hasattr(self, 'size_upper_bound'):
            self.size_upper_bound = (
                Window.width - self.x - self.menu_window_margin,
                Window.height - self.y - self.menu_window_margin)

    def _remove_from_window(self, *args) -> None:
        """Remove the menu from the window."""
        if self.parent is not None:
            Window.remove_widget(self)

    def open(self, *args) -> None:
        """Open the menu with animation."""
        if self.is_open:
            return
        
        self.dispatch('on_pre_open')
        self._add_to_window()
        self.scale_animation_duration = self.menu_opening_duration
        self.scale_animation_transition = self.menu_opening_transition
        self.set_scale_origin()
        self.animate_scale_in()
        self.dispatch('on_open')

    def dismiss(self, *args) -> None:
        """Dismiss the menu with animation."""
        if not self.is_open:
            return
        
        self.dispatch('on_pre_dismiss')
        self.scale_animation_duration = self.menu_dismissing_duration
        self.scale_animation_transition = self.menu_dismissing_transition
        self.set_scale_origin()
        self.animate_scale_out(callback=self._remove_from_window)
        self.dispatch('on_dismiss')

    def toggle(self, *args) -> None:
        """Toggle the menu open/closed state with animation."""
        if self.is_open:
            self.dismiss()
        else:
            self.open()

    def on_pre_open(self, *args) -> None:
        """Event fired before the menu is opened."""
        pass

    def on_pre_dismiss(self, *args) -> None:
        """Event fired before the menu is dismissed."""
        pass

    def on_open(self, *args) -> None:
        """Event fired when the menu is opened."""
        pass

    def on_dismiss(self, *args) -> None:
        """Event fired when the menu is dismissed."""
        pass
