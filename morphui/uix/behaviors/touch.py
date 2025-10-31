from time import time
from typing import Any
from typing import List
from typing import Dict
from typing import Tuple
from weakref import ref

from kivy.clock import Clock
from kivy.event import EventDispatcher
from kivy.graphics import Color
from kivy.graphics import StencilUse
from kivy.graphics import StencilPop
from kivy.graphics import StencilPush
from kivy.graphics import StencilUnUse
from kivy.graphics import RoundedRectangle
from kivy.animation import Animation
from kivy.properties import ListProperty
from kivy.properties import ColorProperty
from kivy.properties import OptionProperty
from kivy.properties import StringProperty
from kivy.properties import NumericProperty
from kivy.properties import BooleanProperty
from kivy.uix.behaviors import ToggleButtonBehavior
from kivy.input.motionevent import MotionEvent
from kivy.uix.relativelayout import RelativeLayout

from ...constants import NAME


__all__ = [
    'MorphButtonBehavior',
    'MorphRippleBehavior',
    'MorphToggleButtonBehavior',]


class MorphButtonBehavior(EventDispatcher):
    """A mixin class that provides button-like behavior to widgets.

    This behavior can be mixed into other widgets to give them the
    ability to respond to press and release events, similar to a button.
    It defines properties and methods for handling touch events and
    managing the pressed state of the widget.

    The behavior dispatches press/release events similar to
    :class:`~kivy.uix.behaviors.ButtonBehavior`.

    Events
    ------
    on_press() -> None
        Event fired when the widget is pressed.
    on_release() -> None  
        Event fired when the widget is released.

    Examples
    --------
    Create a button-like label:

    ```python
    class ButtonLabel(MorphButtonBehavior, Label):
        pass

    label = ButtonLabel(text="Click me")
    label.bind(on_press=lambda instance: print("Pressed!"))
    label.bind(on_release=lambda instance: print("Released!"))
    ```
    """

    always_release: bool = BooleanProperty(True)
    """Whether to always trigger the release action on touch up.

    When set to True, the release action will be triggered on touch up
    events, regardless of whether the touch up occurs within the bounds
    of the widget. This can be useful for ensuring that the release
    action is always executed after a press.

    :attr:`always_release` is a
    :class:`~kivy.properties.BooleanProperty` and defaults to True.
    """

    pressed: bool = BooleanProperty(False)
    """Indicates whether the widget is currently being pressed.

    This property is set to True when a touch event begins on the
    widget and is set to False when the touch event ends. It can be
    used to track the pressed state of the widget for visual feedback
    or other logic.

    :attr:`pressed` is a :class:`~kivy.properties.BooleanProperty`
    and defaults to `False`.
    """

    active: bool = BooleanProperty(False)
    """Indicates whether the widget is currently active.

    This property is set to True when the widget is in an active state
    (e.g., pressed or toggled on) and is set to False when it is not
    active. It can be used to track the active state of the widget
    for visual feedback or other logic.

    :attr:`active` is a :class:`~kivy.properties.BooleanProperty`
    and defaults to `False`.
    """

    min_state_time: float = NumericProperty(0.035)
    """The minimum period of time which the widget must remain in the
    'down' state.

    This property defines the minimum duration that the widget must
    remain in the 'down' state before it can be released. This can help
    prevent accidental taps or quick presses from triggering the
    release action too quickly.

    :attr:`min_state_time` is a :class:`~kivy.properties.NumericProperty`
    and defaults to 0.035.
    """

    _press_start_time: float | None = None
    """Internal variable to track how long the touch has been down.
    
    This variable stores the timestamp when the touch event began,
    allowing calculation of the elapsed time the widget has been
    pressed.
    """

    _press_duration: float = 0.0
    """Internal variable to track the elapsed time the widget has been
    pressed.
    This variable is updated when the touch event ends to determine
    how long the widget was in the pressed state.
    """

    def __init__(self, **kwargs) -> None:
        self.register_event_type('on_press')
        self.register_event_type('on_release')
        super().__init__(**kwargs)
        self.bind(pressed=self._update_press_timing)

    def on_touch_down(self, touch: MotionEvent) -> bool:
        """Handle touch down events to initiate the press action.

        This method is called when a touch event begins on the widget. If
        the touch event occurs within the widget's bounds, the press
        action will be triggered.

        If the widget also includes ripple behavior (e.g.,
        :class:`MorphRippleBaseBehavior`), it will be called to display
        the ripple effect.

        Parameters
        ----------
        touch : MotionEvent
            The touch event that triggered the press action.

        Returns
        -------
        bool
            True if the touch event was handled, False otherwise.
        
        Notes
        -----
        This implementation is based on Kivy button behavior's, see
        :meth:`~kivy.uix.behaviors.ButtonBehavior.on_touch_down`
        """
        if super().on_touch_down(touch):
            return True
        
        if touch.is_mouse_scrolling:
            return False
        
        if not self.collide_point(touch.x, touch.y):
            return False
        
        if self in touch.ud:
            return False
        
        if getattr(self, 'disabled', False):
            return False
            
        self.last_touch = touch
        touch.grab(self)
        touch.ud[self] = True
        self.pressed = True
        self._do_press()

        if getattr(self, 'ripple_enabled', False):
            assert hasattr(self, 'show_ripple_effect'), (
                'Ripple behavior expected but not found.')
            Clock.schedule_once(lambda dt: self.show_ripple_effect(touch.pos), 0)

        self.dispatch('on_press')
        return True

    def on_touch_move(self, touch: MotionEvent) -> bool:
        """Handle touch move events to update the pressed state.

        This method is called when a touch event moves within the widget.
        If the touch is still within the widget's bounds, the pressed
        state will be maintained.

        If the touch moves outside the widget's bounds, and a ripple
        animation is in progress, the ripple animation will be finished.

        Parameters
        ----------
        touch : MotionEvent
            The touch event that triggered the move action.

        Returns
        -------
        bool
            True if the touch event was handled, False otherwise.
        
        Notes
        -----
        This implementation is based on Kivy button behavior's, see
        :meth:`~kivy.uix.behaviors.ButtonBehavior.on_touch_move`.
        """
        if all((
                not self.collide_point(touch.x, touch.y),
                getattr(self, '_ripple_in_progress', False),
                not getattr(self, '_ripple_is_finishing', False))):
            self.finish_ripple_animation()

        if touch.grab_current is self:
            return True
        
        if super().on_touch_move(touch):
            return True

        return self in touch.ud

    def on_touch_up(self, touch: MotionEvent) -> bool | None:
        """Handle touch up events to complete the press action.

        This method is called when a touch event ends on the widget.
        If the touch event was previously registered, the release
        action will be triggered.

        If the widget also includes ripple behavior (e.g.,
        :class:`MorphRippleBaseBehavior`), it will be called to finish
        the ripple animation.

        Parameters
        ----------
        touch : MotionEvent
            The touch event that triggered the release action.

        Returns
        -------
        bool | None
            True if the touch event was handled, False otherwise.
            None if the widget is disabled or if the release action
            is not allowed due to touch being outside the widget bounds.
        
        Notes
        -----
        This implementation is based on Kivy button behavior's, see
        :meth:`~kivy.uix.behaviors.ButtonBehavior.on_touch_up`
        """
        if touch.grab_current is not self:
            return super().on_touch_up(touch)
        
        assert self in touch.ud, (
            'Inconsistent state: touch up event without matching down event.')

        if not self.pressed:
            return False

        touch.ungrab(self)
        self.pressed = False
        self.last_touch = touch
        if getattr(self, 'disabled', False):
            return None
        
        release_delay = -1
        if getattr(self, 'ripple_enabled', False):
            assert hasattr(self, 'finish_ripple_animation'), (
                'Ripple behavior expected but not found.')
            self.finish_ripple_animation()
            release_delay = (
                0.8 * self.ripple_duration_in # 0.8, in order to achieve a small overlap, which leads to a smoother transition for elements that react to the active state.
                + self.ripple_duration_out)
        
        if not self.always_release and not self.collide_point(*touch.pos):
            self._do_release()
            return None

        if self._press_duration < self.min_state_time:
            release_delay = max(
                release_delay, self.min_state_time - self._press_duration)
        Clock.schedule_once(self._do_release, release_delay)
        Clock.schedule_once(
            lambda dt: self.dispatch('on_release'), release_delay)
        return True

    def _update_press_timing(self, *args) -> None:
        """Record the time when the touch event occurred.

        This method is called when the touch state changes to pressed.
        It stores the current time to calculate the duration of the
        press event later.

        Parameters
        ----------
        *args : Any
            Additional arguments passed to the method (not used).
        """
        if self.pressed:
            self._press_duration = 0.0
            self._press_start_time = time()
        else:
            if self._press_start_time is not None:
                self._press_duration = time() - self._press_start_time
            self._press_start_time = None

    def _do_press(self, *args) -> None:
        """Internal method to handle press logic.

        This method sets the :attr:`active` state to True. Override this 
        method to implement custom press behavior.
        """
        self.active = True

    def _do_release(self, *args) -> None:
        """Internal method to handle release logic.

        This method sets the :attr:`active` state to False. Override 
        this method to implement custom release behavior.
        """
        self.active = False
    
    def on_press(self) -> None:
        """Event fired when the widget is pressed.

        This event is dispatched when a touch down event occurs on the
        widget and the widget is not disabled. It can be used to
        trigger custom behavior when the widget is pressed.
        """
        pass

    def on_release(self) -> None:
        """Event fired when the widget is released.

        This event is dispatched when a touch up event occurs on the
        widget and the widget is not disabled. It can be used to
        trigger custom behavior when the widget is released.
        """
        pass


class MorphRippleBehavior(EventDispatcher):
    """A base behavior class that provides ripple effect functionality.

    This behavior can be mixed into other widgets to add a ripple effect
    that responds to touch events. It defines properties for customizing
    the appearance and animation of the ripple effect, as well as methods
    for handling touch events and managing the ripple animation.

    This class is intended to be subclassed by specific ripple effect
    implementations, which should define the `ripple_canvas_instructions`
    method to specify how the ripple effect is drawn on the canvas.
    """

    ripple_color: List[float] | None = ColorProperty(None)
    """The color of the ripple effect.

    This property defines the color of the ripple effect when it is
    displayed. It is specified as a list of four floats representing
    the RGBA color components, each ranging from 0 to 1.
    
    If set to None, ripple color will fall back to interaction color
    with pressed state opacity, if available, otherwise to gray.

    :attr:`ripple_color` is a
    :class:`~kivy.properties.ColorProperty` and defaults to gray
    ([0.75, 0.75, 0.75, 0.5]).
    """

    _current_ripple_color: List[float] = ColorProperty()
    """The current color of the ripple effect during animation.

    This internal property tracks the color of the ripple effect as it
    animates from its initial color to transparent. It is updated during
    the ripple animation.

    :attr:`_current_ripple_color` is a
    :class:`~kivy.properties.ColorProperty` and is managed internally.
    """

    ripple_duration_in: float = NumericProperty(0.3)
    """The duration of the ripple fade-in animation in seconds.

    This property defines how long it takes for the ripple effect to
    fully appear after a touch event. A shorter duration results in a
    quicker ripple effect, while a longer duration creates a slower,
    more pronounced effect.

    :attr:`ripple_duration_in` is a
    :class:`~kivy.properties.NumericProperty` and defaults to 0.3.
    """

    ripple_duration_in_long: float = NumericProperty(1.5)
    """The duration of the ripple fade-in animation for long presses.

    This property defines how long it takes for the ripple effect to
    fully appear during a long press touch event. A longer duration
    results in a more pronounced ripple effect.

    :attr:`ripple_duration_in_long` is a
    :class:`~kivy.properties.NumericProperty` and defaults to 0.6.
    """

    ripple_duration_out: float = NumericProperty(0.3)
    """The duration of the ripple fade-out animation in seconds.

    This property defines how long it takes for the ripple effect to
    disappear after being fully visible. A shorter duration results in a
    quicker fade-out effect, while a longer duration creates a slower,
    more gradual effect.

    :attr:`ripple_duration_out` is a
    :class:`~kivy.properties.NumericProperty` and defaults to 0.3.
    """

    ripple_transition_in: str = StringProperty('out_quad')
    """The easing function used for the ripple fade-in animation.

    This property defines the easing function that controls the
    acceleration and deceleration of the ripple effect as it fades in.

    :attr:`ripple_transition_in` is a
    :class:`~kivy.properties.StringProperty` and defaults to 'out_quad'.
    """

    ripple_transition_out: str = StringProperty('in_quad')
    """The easing function used for the ripple fade-out animation.

    This property defines the easing function that controls the
    acceleration and deceleration of the ripple effect as it fades out.
    
    :attr:`ripple_transition_out` is a
    :class:`~kivy.properties.StringProperty` and defaults to 'in_quad'.
    """

    ripple_enabled: bool = BooleanProperty(True)
    """Whether the ripple effect is enabled.

    This property allows for enabling or disabling the ripple effect
    dynamically. When set to True, the ripple effect will be shown on
    touch events. When set to False, no ripple effect will be displayed,
    but the touch events will still be processed normally.

    :attr:`ripple_enabled` is a
    :class:`~kivy.properties.BooleanProperty` and defaults to True.
    """

    ripple_pos: List[float] = ListProperty([0, 0], length=4)
    """The position of the ripple effect on the widget.

    This property defines the (x, y) coordinates where the ripple
    effect originates. The coordinates are relative to the widget's
    position.

    :attr:`ripple_pos` is a
    :class:`~kivy.properties.ListProperty` and defaults to [0, 0].
    """

    ripple_initial_radius: float = NumericProperty(5.0)
    """The initial radius of the ripple effect when it starts.

    This property defines the starting size of the ripple effect when a
    touch event occurs. A value of 0 means the ripple starts from a
    point, while higher values make the ripple start larger.

    This property can be adjusted to create different visual effects
    for the ripple animation, allowing for greater flexibility in
    design.

    :attr:`ripple_initial_radius` is a
    :class:`~kivy.properties.NumericProperty` and defaults to 15.
    """

    _current_ripple_radius: float = NumericProperty()
    """The current radius of the ripple effect during animation.
    
    This internal property tracks the size of the ripple effect as it
    animates from its initial radius to its final radius. It is updated
    during the animation process to create the expanding ripple effect.
    
    :attr:`_current_ripple_radius` is a
    :class:`~kivy.properties.NumericProperty` and is managed internally.
    """

    ripple_layer: str = OptionProperty(
        'interaction', options=('interaction', 'overlay'))
    """The layer on which the ripple effect is drawn.

    This property allows you to specify whether the ripple effect should
    be drawn on the 'interaction' layer (between surface and content) or
    the 'overlay' layer (on top of the widget).

    :attr:`ripple_layer` is a
    :class:`~kivy.properties.OptionProperty` and defaults to 'interaction'.
    """

    _ripple_final_radius: float
    """The final radius of the ripple effect when it ends."""

    _ripple_in_progress: bool = False
    """Indicates whether a ripple animation is currently in progress."""

    _ripple_is_finishing: bool = False
    """Indicates whether the ripple animation is currently finishing."""

    _ripple_is_fading: bool = False
    """Indicates whether the ripple is currently fading out."""

    _ripple_color_instruction: Any
    """Kivy Color instruction for the ripple color."""

    _ripple_shape_instruction: Any
    """Kivy instruction of used shape for the ripple effect."""

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        self.bind(
            _current_ripple_color=self._update_ripple_instruction,
            _current_ripple_radius=self._update_ripple_instruction,)
        if hasattr(self, 'disabled'):
            self.fbind('disabled', self.fade_ripple_animation)

    def _evaluate_ripple_pos(self, touch_pos: Tuple[float, float]) -> None:
        """Evaluate the position of the ripple effect based on the touch 
        event.

        This method updates the `ripple_pos` property to reflect the
        current position of the touch event.
        """
        touch_x, touch_y = touch_pos
        if isinstance(self, RelativeLayout):
            x, y = self.to_window(self.x, self.y)
            self.ripple_pos = [touch_x - x, touch_y - y]
        else:
            self.ripple_pos = [touch_x, touch_y]

    def determine_ripple_color(self) -> List[float]:
        """Get the effective ripple color, falling back to interaction 
        color.

        This method returns the ripple color if it is set, otherwise it
        tries to use the interaction color with the pressed state
        opacity. If neither is available, it defaults to a gray color.

        Returns
        -------
        List[float]
            The effective ripple color.
        """
        if self.ripple_color is not None:
            return self.ripple_color
        
        ripple_color = getattr(
            self, 'get_resolved_interaction_color', lambda: [0.0, 0.0, 0.0])()
        opacity = getattr(self, 'pressed_state_opacity', 0.12)
        return ripple_color[:3] + [opacity,]

    def show_ripple_effect(self, touch_pos: Tuple[float, float]) -> None:
        """Display the ripple effect for a touch event if ripple is
        enabled.

        Parameters
        ----------
        touch_pos : Tuple[float, float]
            The position of the touch event.
        """
        if not self.ripple_enabled:
            return None
        
        if self._ripple_in_progress:
            Animation.cancel_all(self, '_current_ripple_radius')
            if self._ripple_is_fading:
                Animation.cancel_all(self, '_current_ripple_color')
            self._on_ripple_complete()

        self._ripple_in_progress = True
        self._ripple_is_fading = False
        self._ripple_is_finishing = False
        self._current_ripple_radius = self.ripple_initial_radius
        self._current_ripple_color = self.determine_ripple_color()
        self._ripple_final_radius = (
            max(getattr(self, 'interaction_layer_size', self.size)) * 2)
        self._evaluate_ripple_pos(touch_pos)
        self.ripple_canvas_instructions()
        self.start_ripple_animation()

    def start_ripple_animation(self) -> None:
        """Start the ripple animation.
        """
        if self._ripple_is_fading or not self._ripple_in_progress:
            return None

        animation = Animation(
            _current_ripple_radius=self._ripple_final_radius,
            duration=self.ripple_duration_in_long,
            t=self.ripple_transition_in)
        animation.bind(on_complete=self.fade_ripple_animation)
        animation.start(self)
    
    def finish_ripple_animation(self) -> None:
        """Finish the ripple animation immediately.
        """
        if self._ripple_is_fading or not self._ripple_in_progress:
            return None
        
        self._ripple_is_finishing = True
        Animation.cancel_all(self, '_current_ripple_radius')
        animation = Animation(
            _current_ripple_radius=self._ripple_final_radius,
            duration=self.ripple_duration_in,
            t=self.ripple_transition_in)
        animation.bind(on_complete=self.fade_ripple_animation)
        animation.start(self)

    def fade_ripple_animation(self, *args) -> None:
        """Fade out the ripple animation.
        """
        if self._ripple_is_fading or not self._ripple_in_progress:
            return None
        
        self._ripple_is_finishing = False
        self._ripple_is_fading = True
        Animation.cancel_all(self, '_current_ripple_color')
        animation = Animation(
            _current_ripple_color=self.determine_ripple_color()[:3] + [0],
            duration=self.ripple_duration_out,
            t=self.ripple_transition_out)
        animation.bind(on_complete=self._on_ripple_complete)
        animation.start(self)

    def ripple_canvas_instructions(self) -> None:
        """Define the canvas instructions for rendering the rectangular
        ripple effect.

        This method creates the necessary canvas instructions to draw
        a rounded rectangular ripple effect that expands from the touch 
        point.

        Notes
        -----
        - The ripple is drawn using a RoundedRectangle instruction, with 
          its size determined by the current ripple radius.
        - Stencil instructions are used to ensure the ripple is clipped
          to the bounds of the widget.
        - Call :meth:`_evaluate_ripple_pos` before invoking this
          method to set the correct ripple position.
        """
        radius = getattr(self, 'radius', [0])
        if isinstance(radius, (int, float)):
            radius = [radius,]
        group = NAME.RIPPLE
        if self.ripple_layer == 'overlay':
            canvas = self.canvas.after
        else:
            canvas = self.canvas.before

        pos = getattr(self, 'interaction_layer_pos', self.pos)
        size = getattr(self, 'interaction_layer_size', self.size)
        with canvas:
            StencilPush(
                group=group)
            RoundedRectangle(
                pos=pos,
                size=size,
                radius=radius,
                group=group)
            StencilUse(group=group)
            self._ripple_color_instruction = Color(
                rgba=self.determine_ripple_color(),
                group=group)
            self._ripple_shape_instruction = RoundedRectangle(
                size=(
                    self.ripple_initial_radius * 2,
                    self.ripple_initial_radius * 2),
                pos=(
                    self.ripple_pos[0] - self._current_ripple_radius / 2,
                    self.ripple_pos[1] - self._current_ripple_radius / 2),
                group=group)
            StencilUnUse(
                group=group)
            RoundedRectangle(
                pos=pos,
                size=size,
                radius=radius,
                group=group)
            StencilPop(
                group=group)

    def _on_ripple_complete(self, *args) -> None:
        """Callback when the ripple animation completes.

        This method is called when the ripple animation finishes. It
        resets the internal state to indicate that no ripple is 
        currently in progress.
        """
        self._ripple_in_progress = False
        self._ripple_is_finishing = False
        self._ripple_is_fading = False
        
        if self.ripple_layer == 'overlay':
            canvas = self.canvas.after
        else:
            canvas = self.canvas.before
        canvas.remove_group(NAME.RIPPLE)

    def _update_ripple_instruction(self, *args) -> None:
        """Update the size and position of the ripple shape during
        animation.

        This method is called whenever the :attr:`_current_ripple_radius` 
        property or the :attr:`_current_ripple_color` property changes,
        either during the animation or the changes. It updates the size
        and position and color of the ripple instructions to reflect the
        current radius and color.
        """
        if hasattr(self, '_ripple_shape_instruction'):
            last_touch = getattr(self, 'last_touch', None)
            x, y = last_touch.pos if last_touch else self.center
            self._evaluate_ripple_pos((x, y))
            self._ripple_shape_instruction.size = (
                self._current_ripple_radius, self._current_ripple_radius)
            self._ripple_shape_instruction.pos = (
                self.ripple_pos[0] - self._current_ripple_radius / 2,
                self.ripple_pos[1] - self._current_ripple_radius / 2)
        if hasattr(self, '_ripple_color_instruction'):
            self._ripple_color_instruction.rgba = self._current_ripple_color
    
    def trigger_ripple(self, *args) -> None:
        """Manually trigger the ripple effect at the center of the 
        widget.

        This method can be used to programmatically display the ripple
        effect at the center of the widget, without requiring a touch
        event.
        """
        center_pos = (self.center_x, self.center_y)
        self.last_touch = None
        self.show_ripple_effect(center_pos)
        self.finish_ripple_animation()


class MorphToggleButtonBehavior(MorphButtonBehavior):
    """A mixin class that provides toggle button behavior to widgets.

    This behavior can be mixed into other widgets to give them the
    ability to act as toggle buttons, allowing them to switch between
    'normal' and 'down' states. It supports grouping of toggle buttons
    to allow only one button in a group to be in the 'down' state at a
    time.

    The behavior dispatches press/release events similar to
    :class:`~kivy.uix.behaviors.ButtonBehavior`.

    Properties
    ----------
    state : str
        The current state of the toggle button, either 'normal' or 'down'.
    group : str | None
        The group identifier for the toggle button. Buttons in the same
        group will enforce mutual exclusivity.
    allow_no_selection : bool
        Whether the toggle button allows no selection in its group.

    Events
    ------
    on_press() -> None
        Event fired when the widget is pressed.
    on_release() -> None  
        Event fired when the widget is released.

    Examples
    --------
    Create a toggle button:

    ```python
    class MyToggleButton(MorphToggleButtonBehavior, Button):
        pass

    toggle_button = MyToggleButton(text="Toggle me")
    toggle_button.bind(on_press=lambda instance: print("Pressed!"))
    toggle_button.bind(on_release=lambda instance: print("Released!"))
    ```

    Notes
    -----
    This implementation is based on Kivy's ToggleButtonBehavior, see
    :class:`~kivy.uix.behaviors.ToggleButtonBehavior`.
    """

    __groups: Dict[str, List[ref]] = {}
    """Internal dictionary to manage groups of toggle buttons.
    
    This class-level dictionary keeps track of toggle button groups,
    allowing for mutual exclusivity among buttons in the same group.
    """

    group: str | None = StringProperty(None, allownone=True)
    """The group identifier for the toggle button.

    Buttons in the same group will enforce mutual exclusivity, meaning
    that only one button in the group can be in the 'down' state at a
    time.

    :attr:`group` is a :class:`~kivy.properties.StringProperty`
    and defaults to `None`.
    """

    allow_no_selection: bool = BooleanProperty(True)
    """Whether the toggle button allows no selection in its group.

    If set to `True`, the toggle button can be deselected, allowing
    no button in the group to be in the 'active' state. If set to
    `False`, at least one button in the group must be active at
    all times.

    :attr:`allow_no_selection` is a :class:`~kivy.properties.BooleanProperty`
    and defaults to `True`.
    """

    _previous_group: str | None = None
    """Internal variable to track the previous group of the toggle 
    button.
    """

    def __init__(self, **kwargs) -> None:
        self._previous_group = None
        super().__init__(**kwargs)
        self.bind(group=self._on_group_change,)

        self.refresh_toggle_group()
    
    @staticmethod
    def _clear_groups(weak_ref: ref) -> None:
        """Clear the weak reference from all groups when the widget is
        deleted.

        This static method is used as a callback for weak references to
        remove the reference from all groups when the widget is garbage
        collected.

        Parameters
        ----------
        weak_ref : ref
            The weak reference to the toggle button instance.
        """
        groups = MorphToggleButtonBehavior.__groups
        for grouped_items in list(groups.values()):
            if weak_ref in grouped_items:
                grouped_items.remove(weak_ref)
                break
    
    @staticmethod
    def get_widgets(group: str) -> List[Any]:
        """Get all toggle button widgets in the specified group.

        This static method retrieves all toggle button instances that
        belong to the specified group.

        Parameters
        ----------
        group : str
            The group identifier.

        Returns
        -------
        List[Any]
            A list of toggle button instances in the specified group.
        """
        widgets = []
        groups = MorphToggleButtonBehavior.__groups
        grouped_items = groups.get(group, [])
        for item in grouped_items:
            widget = item()
            if widget is not None:
                widgets.append(widget)
        return widgets

    def refresh_toggle_group(self) -> None:
        """Refresh the toggle button's group registration.

        This method ensures that the toggle button is correctly
        registered in its current group. It removes the button from its
        previous group (if any) and adds it to the new group.
        """
        self._on_group_change(self, self.group)

    def _on_group_change(self, instance: Any, group: str | None) -> None:
        """Handle changes to the group property.

        This method updates the internal group management when the
        `group` property changes. It ensures that the toggle button is
        correctly registered in its new group and removed from its old
        group.

        Parameters
        ----------
        instance : Any
            The instance of the toggle button.
        group : str | None
            The new group identifier.
        """
        groups = MorphToggleButtonBehavior.__groups
        if self._previous_group is not None and self._previous_group in groups:
            grouped_items = groups[self._previous_group]
            for item in grouped_items[:]:
                if item() is self:
                    grouped_items.remove(item)
                    break

        self._previous_group = group
        if group is None:
            return None
        
        if group not in groups:
            groups[group] = []
        groups[group].append(ref(self, ToggleButtonBehavior._clear_groups))

    def _release_group(self, current: ToggleButtonBehavior) -> None:
        """Release other buttons in the same group when this button is
        active.

        This method sets the `active` state of all other buttons in
        the same group to `False`, ensuring mutual exclusivity.

        Parameters
        ----------
        current : ToggleButtonBehavior
            The current toggle button instance.
        """
        if self.group is None:
            return None
        
        grouped_items = self.__groups.get(self.group, [])
        for item in grouped_items:
            widget = item()
            if widget is None:
                grouped_items.remove(item)
            elif widget is current:
                continue
            else:
                widget.active = False

    def _do_press(self, *args) -> None:
        """Handle the press action for the toggle button.

        This method updates the :attr:`active` state and manages the
        group exclusivity when the button is pressed.
        """
        if all((
                self.active,
                self.group is not None,
                not self.allow_no_selection,)):
            return None
        
        self._release_group(self)
    
    def _do_release(self, *args) -> None:
        """Handle the release action for the toggle button.

        This method is overridden to prevent changing the active
        state on release, as toggle buttons only change state on press.
        """
        self.active = not self.active
