from typing import Any

from kivy.properties import AliasProperty
from kivy.properties import ObjectProperty
from kivy.properties import StringProperty
from kivy.properties import NumericProperty
from kivy.core.window import Window

from morphui.uix.behaviors import MorphScaleBehavior


__all__ = [
    'MorphMenuMotionBehavior']


class MorphMenuMotionBehavior(MorphScaleBehavior,):
    """Behavior class that adds menu motion functionality to a widget.
    
    This behavior provides properties and methods to manage a menu
    associated with a widget, including tools, open/close state, and
    animation settings.
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

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.bind(size=self._update_position)
        
    def on_caller(self, instance: Any, caller: Any) -> None:
        """Update the menu position when the caller button changes."""
        self.caller.bind(
            pos=self._update_position,
            size=self._update_position,)

    def _resolve_caller_pos(self) -> tuple[float, float]:
        """Get the caller button position in window coordinates."""
        if self.caller is None:
            return (0, 0)
        
        return self.caller.to_window(*self.caller.pos)
    
    def _resolve_pos(self) -> tuple[float, float]:
        """Get the menu position relative to the caller button."""
        caller_pos = self._resolve_caller_pos()
        pos = (caller_pos[0], max(caller_pos[1] - self.height, 0))
        return pos

    def set_scale_origin(self, *args) -> None:
        """Set the scale origin based on the caller button position."""
        caller_pos = self._resolve_caller_pos()
        x_offset = self.caller.width / 2 if self.caller else 0
        self.scale_origin = [caller_pos[0] + x_offset, caller_pos[1]]

    def _update_position(self, *args) -> None:
        """Update the menu position relative to the caller button."""
        self.pos = self._resolve_pos()

    def _add_to_window(self, *args) -> None:
        """Add the menu to the window and update its position."""
        Window.add_widget(self)
        self._update_position()

    def _remove_from_window(self, *args) -> None:
        """Remove the menu from the window."""
        if self.parent is not None:
            Window.remove_widget(self)

    def open(self, *args) -> None:
        """Open the menu with animation."""
        if self.is_open:
            return
        
        self._add_to_window()
        self.scale_animation_duration = self.menu_opening_duration
        self.scale_animation_transition = self.menu_opening_transition
        self.set_scale_origin()
        self.animate_scale_in()

    def dismiss(self, *args) -> None:
        """Dismiss the menu with animation."""
        if not self.is_open:
            return
        
        self.scale_animation_duration = self.menu_dismissing_duration
        self.scale_animation_transition = self.menu_dismissing_transition
        self.set_scale_origin()
        self.animate_scale_out(callback=self._remove_from_window)

    def toggle(self, *args) -> None:
        """Toggle the menu open/closed state with animation."""
        if self.is_open:
            self.dismiss()
        else:
            self.open()
