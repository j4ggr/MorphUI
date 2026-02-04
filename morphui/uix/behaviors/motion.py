from typing import Any
from typing import Tuple
from typing import Literal

from kivy.clock import Clock
from kivy.metrics import dp
from kivy.animation import Animation
from kivy.properties import AliasProperty
from kivy.properties import BooleanProperty
from kivy.properties import ObjectProperty
from kivy.properties import StringProperty
from kivy.properties import OptionProperty
from kivy.properties import NumericProperty
from kivy.core.window import Window
from kivy.input.motionevent import MotionEvent

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

    same_width_as_caller: bool = BooleanProperty(False)
    """Whether the menu should match the caller button's width.

    If set to `True`, the menu will automatically adjust its width to
    match the width of the caller button when opened.

    :attr:`same_width_as_caller` is a
    :class:`~kivy.properties.BoolProperty` and defaults to `False`.
    """

    menu_anchor_position: Literal['left', 'center', 'right'] = OptionProperty(
        'center', options=['left', 'center', 'right'])
    """Position of the menu relative to the caller widget.

    This property defines the horizontal alignment of the menu relative
    to the caller button. Options are:
    - 'left': Align the menu's right edge with the caller's left edge
    - 'center': Center the menu horizontally with the caller
    - 'right': Align the menu's left edge with the caller's right edge

    :attr:`menu_anchor_position` is a
    :class:`~kivy.properties.OptionProperty` and defaults to `'center'`.
    """

    menu_opening_direction: Literal['up', 'center', 'down'] = OptionProperty(
        'down', options=['up', 'center', 'down'])
    """Direction in which the menu opens.

    This property defines the direction in which the menu will open
    relative to the caller button. It can be either 'up', 'center' or 
    'down'.

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

    menu_window_margin: float = NumericProperty(dp(8))
    """Margin from the window edges in pixels.

    This property defines the minimum distance (in pixels) that the menu
    should maintain from the edges of the window. This ensures the menu
    remains fully visible and doesn't extend beyond the window bounds.

    :attr:`menu_window_margin` is a
    :class:`~kivy.properties.NumericProperty` and defaults to `8`."""

    menu_caller_spacing: float = NumericProperty(dp(2))
    """Spacing between the menu and the caller button in pixels.

    This property defines the vertical spacing (in pixels) between the
    menu and the caller button when the menu is opened.

    :attr:`menu_caller_spacing` is a
    :class:`~kivy.properties.NumericProperty` and defaults to `2`."""

    auto_adjust_position: bool = BooleanProperty(True)
    """Whether to automatically adjust menu position to fit within window bounds.

    This property determines if the menu should automatically adjust its
    position and opening direction when there is insufficient space in
    the window to fully display the menu. If set to `True`, the menu
    will switch its anchor position and/or opening direction to fit
    within the window bounds.

    :attr:`auto_adjust_position` is a
    :class:`~kivy.properties.BoolProperty` and defaults to `True`."""

    min_space_required: float = NumericProperty(dp(100))
    """Minimum space required (in pixels) before adjusting menu position.

    This property defines the minimum amount of space (in pixels)
    required in the desired direction for the menu to open. If there is
    insufficient space, the menu may switch its position or opening
    direction based on the :attr:`auto_adjust_position` setting.

    :attr:`min_space_required` is a
    :class:`~kivy.properties.NumericProperty` and defaults to `100`.
    """

    dismiss_allowed: bool = BooleanProperty(True)
    """Whether dismissing the menu by touching outside is allowed.

    This property determines if the menu can be dismissed by touching
    outside its bounds. If set to `True`, touching outside the menu
    will close it.

    :attr:`dismiss_allowed` is a
    :class:`~kivy.properties.BoolProperty` and defaults to `True`.
    """

    def __init__(self, **kwargs) -> None:
        self.register_event_type('on_pre_open')
        self.register_event_type('on_pre_dismiss')
        self.register_event_type('on_open')
        self.register_event_type('on_dismiss')
        super().__init__(**kwargs)
        self.bind(
            caller=self._update_caller_bindings)
        self._update_caller_bindings()
        
    def _update_caller_bindings(self, *args) -> None:
        """Update bindings to the caller button's position and size.
        
        This method binds to the caller button's `pos` and `size`
        properties to adjust the menu position whenever the caller
        changes. If there is no caller set, it does nothing.
        """
        if self.caller is None:
            return
        
        self.caller.bind(
            pos=self._adjust_and_reposition,
            size=self._adjust_and_reposition,)
        self._adjust_and_reposition()

    def _adjust_and_reposition(self, *args) -> None:
        """Adjust the menu position and size to fit within the window.
        
        This method adjusts the menu's position and size based on the
        available space in the window. It ensures that the menu fits
        within the window bounds while respecting the specified margin.

        Notes
        -----
        Call this method after the menu size has changed to ensure
        correct positioning.
        """
        if not self.is_open:
            return

        if hasattr(self, 'layout_manager'):
            size = self.layout_manager.size
            padding = getattr(self, 'padding', [0]*4)
            self.size = (
                size[0] + padding[0] + padding[2],
                size[1] + padding[1] + padding[3],)
        self._adjust_to_fit_window()
        self.pos = self._resolve_pos()
        self.size = self._resolve_size()

    def _resolve_caller_pos(self) -> Tuple[float, float]:
        """Get the caller button position in window coordinates.
        
        This method returns the position of the caller button in window
        coordinates. If the caller is not set, it returns 
        `(0, Window.height)`.
        """
        if self.caller is None:
            return (0, Window.height)
        
        return self.caller.to_window(*self.caller.pos)
    
    def _resolve_caller_size(self) -> Tuple[float, float]:
        """Get the caller button size.
        
        This method returns the size of the caller button. If the caller
        is not set, it returns `(0, 0)`.
        """
        if self.caller is None:
            return (0, 0)
        
        return self.caller.size
        
    def _adjust_to_fit_window(self) -> None:
        """Adjust the menu anchor position and opening direction based
        on available space in the window.
        
        This method checks the available space around the caller button
        and adjusts the menu's anchor position and opening direction to
        ensure it fits within the window bounds. It uses the
        :attr:`auto_adjust_position` and :attr:`min_space_required`
        properties to determine when adjustments are necessary.

        Notes
        -----
        Call this method before :meth:`_resolve_pos` and
        :meth:`_resolve_size` to ensure correct calculations.
        """
        if self.caller is None or not self.auto_adjust_position:
            return
    
        caller_x, caller_y = self._resolve_caller_pos()
        caller_width, caller_height = self._resolve_caller_size()
        margin = self.menu_window_margin
        w, h = self.size
        
        space_above = Window.height - (caller_y + caller_height) - margin
        space_below = caller_y - margin
        if all((
                self.menu_opening_direction == 'down',
                h > space_below,
                space_below < self.min_space_required,)):
            self.menu_opening_direction = 'up'
        elif all((
                self.menu_opening_direction == 'up',
                h > space_above,
                space_above < self.min_space_required,)):
            self.menu_opening_direction = 'down'
        
        space_left = caller_x - margin
        space_right = Window.width - (caller_x + caller_width) - margin
        if all((
                self.menu_anchor_position == 'left',
                w > space_right,
                space_left < self.min_space_required,)):
            self.menu_anchor_position = 'right'
        elif all((
                self.menu_anchor_position == 'right',
                w > space_left,
                space_right < self.min_space_required,)):
            self.menu_anchor_position = 'left'
    
    def _resolve_pos(self) -> Tuple[float, float]:
        """Get the menu position relative to the caller button.
        
        This method calculates the position of the menu based on the
        position and size of the caller button, as well as the specified
        anchor position and opening direction. The position is clamped
        to ensure the menu stays within window bounds with the specified
        margin.

        Returns
        -------
        Tuple[float, float]
            The (x, y) position of the menu in window coordinates.

        Notes
        -----
        Call this method after :meth:`_adjust_to_fit_window` to ensure
        correct calculations.
        """
        caller_x, caller_y = self._resolve_caller_pos()
        caller_width, caller_height = self._resolve_caller_size()

        match self.menu_opening_direction:
            case 'up':
                y = caller_y
                if self.menu_anchor_position == 'center':
                    y += caller_height + self.menu_caller_spacing
            case 'center':
                y = caller_y + (caller_height - self.height) / 2
            case 'down':
                y = caller_y - self.height
                if self.menu_anchor_position == 'center':
                    y -= self.menu_caller_spacing
                else:
                    y += caller_height
        
        match self.menu_anchor_position:
            case 'left':
                x = caller_x - self.width - self.menu_caller_spacing
            case 'center':
                x = caller_x + (caller_width - self.width) / 2
            case 'right':
                x = caller_x + caller_width + self.menu_caller_spacing
        
        x = max(x, self.menu_window_margin)
        y = max(y, self.menu_window_margin)
        return (x, y)
    
    def _resolve_size(self) -> Tuple[float, float]:
        """Get the menu size constrained within window bounds.
        
        This method calculates the size of the menu, ensuring it fits
        within the window bounds while respecting the specified margin.

        If the widget also inherits from :class:`MorphSizeBoundsBehavior`,
        it will set the `size_upper_bound` property accordingly.

        Returns
        -------
        Tuple[float, float]
            The (width, height) of the menu constrained within window
            bounds.

        Notes
        -----
        Call this method after :meth:`_adjust_to_fit_window` and
        :meth:`_resolve_pos` to ensure correct calculations. Therefore,
        we can assume that the position (self.x and self.y) always has 
        at least the necessary margin.
        """
        margin = self.menu_window_margin
        caller_x, caller_y = self._resolve_caller_pos()
        caller_width, caller_height = self._resolve_caller_size()

        match self.menu_opening_direction:
            case 'up':
                max_height = Window.height - self.y - margin
            case 'center':
                max_height = Window.height - 2 * margin
            case 'down':
                max_height = caller_y - self.y
                if self.menu_anchor_position in ('left', 'right'):
                    max_height += caller_height
        max_height = max(max_height, 0)

        match self.menu_anchor_position:
            case 'left':
                max_width = caller_x - self.x
            case 'center':
                max_width = Window.width - 2 * margin
            case 'right':
                max_width = Window.width - self.x - margin
        max_width = max(max_width, 0)

        if hasattr(self, 'size_upper_bound'):
            self.size_upper_bound = (max_width, max_height)

        if self.same_width_as_caller and self.caller is not None:
            width = caller_width
        else:
            width = clamp(self.width, 0, max_width)
        height = clamp(self.height, 0, max_height)
        
        return width, height
    
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

    def _add_to_window(self, *args) -> None:
        """Add the menu to the window.
        
        This method adds the menu widget to the window and updates its
        position based on the caller button. If the widget also inherits
        from :class:`MorphSizeBoundsBehavior`, it will set the
        `size_upper_bound` property to ensure the menu fits within the
        window bounds, respecting the :attr:`menu_window_margin`.
        """
        if self.parent:
            return
        Window.add_widget(self)

    def _remove_from_window(self, *args) -> None:
        """Remove the menu from the window."""
        if self.is_open:
            Window.remove_widget(self)
        self.dispatch('on_dismiss')

    def open(self, *args) -> None:
        """Open the menu with animation.
        
         This method opens the menu with an animation. If the menu is
         already open, it does nothing. The menu position is adjusted to
         fit within the window bounds before opening.
        """
        if self.is_open:
            Animation.cancel_all(self)
            return
        
        self.dismiss_allowed = False
        self.dispatch('on_pre_open')
        self._add_to_window()
        self._adjust_and_reposition()
        if self.scale_enabled:
            self.scale_animation_duration = self.menu_opening_duration
            self.scale_animation_transition = self.menu_opening_transition
            self.set_scale_origin()
            self.animate_scale_in(lambda *_: self.dispatch('on_open'))
        else:
            self.dispatch('on_open')

    def dismiss(self, *args) -> None:
        """Dismiss the menu with animation."""
        if not self.dismiss_allowed:
            return
        
        if not self.is_open:
            Animation.cancel_all(self)
            return
        
        self.dispatch('on_pre_dismiss')
        if self.scale_enabled:
            self.scale_animation_duration = self.menu_dismissing_duration
            self.scale_animation_transition = self.menu_dismissing_transition
            self.set_scale_origin()
            self.animate_scale_out(callback=self._remove_from_window)
        else:
            self._remove_from_window()

    def toggle(self, *args) -> None:
        """Toggle the menu open/closed state with animation."""
        if self.is_open:
            self.dismiss()
        else:
            self.open()
    
    def on_touch_up(self, touch: MotionEvent) -> Literal[True] | None:
        """Handle touch up events to close the menu when touching
        outside.

        This method overrides the default touch up behavior to
        close the date picker menu if a touch event occurs outside
        its bounds.
        """
        if not self.collide_point(*touch.pos):
            Clock.schedule_once(self.dismiss, 0)
            return None
        return super().on_touch_up(touch)

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
