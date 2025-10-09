from typing import Any

from kivy.event import EventDispatcher
from kivy.properties import BooleanProperty
from kivy.uix.behaviors import TouchRippleBehavior
from kivy.uix.behaviors import TouchRippleButtonBehavior
from kivy.input.motionevent import MotionEvent

__all__ = [
    'MorphTouchRippleBehavior',
    'MorphTouchRippleButtonBehavior']


class MorphTouchRippleBehavior(EventDispatcher,TouchRippleBehavior):
    """A mixin class that adds configurable touch ripple effects to
    widgets.
    
    This behavior extends Kivy's TouchRippleBehavior with the ability
    to enable or disable the ripple effect dynamically. It can be
    combined with any Kivy widget to provide a visual ripple effect when
    the widget is touched.
    
    The ripple effect can be controlled via the `ripple_enabled`
    property, which allows for runtime enabling/disabling without
    affecting the underlying widget functionality.
    
    Examples
    --------
    ```python
    class MyWidget(MorphTouchRippleBehavior, Widget):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            self.ripple_enabled = True  # Enable ripple effect
    ```
    """

    ripple_enabled: bool = BooleanProperty(True)
    """Controls whether the ripple effect is enabled for touch
    interactions.
    
    When True, touching the widget will produce a visual ripple effect
    that animates outward from the touch point. When False, no ripple
    effect will be shown, but all other touch functionality remains
    intact.
    
    The ripple effect is achieved by temporarily setting ripple
    durations to zero when disabled, which prevents the visual animation
    while maintaining proper touch event handling.
    
    :attr:`ripple_enabled` is a 
    :class:`~kivy.properties.BooleanProperty` and defaults to True.
    """

    _ripple_duration_in: float
    """Internal storage for the original ripple fade-in duration.
    
    This attribute preserves the original ripple_duration_in value so 
    it can be restored when the ripple effect is re-enabled after being
    disabled.
    """
    
    _ripple_duration_out: float
    """Internal storage for the original ripple fade-out duration.
    
    This attribute preserves the original ripple_duration_out value so
    it can be restored when the ripple effect is re-enabled after being
    disabled.
    """

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.bind(
            ripple_enabled=self._update_ripple_state,
            ripple_duration_in=self._update_durations,
            ripple_duration_out=self._update_durations)

        self._ripple_duration_in = self.ripple_duration_in
        self._ripple_duration_out = self.ripple_duration_out
    
    def _update_durations(self, instance: Any, value: float) -> None:
        """Update internal ripple duration storage when public
        properties change.
        
        This method ensures that the internal backup copies of ripple
        durations are kept in sync with the public ripple_duration_in
        and ripple_duration_out properties. This allows the original
        durations to be restored when the ripple effect is re-enabled.
        
        Parameters
        ----------
        instance : Any
            The widget instance (unused but required by Kivy binding)
        value : float
            The new duration value (unused, values read directly from 
            properties)

        Notes
        -----
        Only positive duration values are stored to prevent invalid
        configurations.
        """
        if self.ripple_duration_in > 0:
            self._ripple_duration_in = self.ripple_duration_in
        if self.ripple_duration_out > 0:
            self._ripple_duration_out = self.ripple_duration_out

    def _update_ripple_state(self, instance: Any, ripple_enabled: bool) -> None:
        """Enable or disable the ripple effect by manipulating duration
        properties.
        
        This method responds to changes in the ripple_enabled property
        by either restoring the original ripple durations (when 
        enabling) or setting them to zero (when disabling). Setting 
        durations to zero effectively disables the visual ripple effect
        while maintaining proper touch event handling.
        
        The approach of modifying durations rather than blocking touch
        events ensures that widgets like TouchRippleButtonBehavior
        continue to function correctly, as they may have built-in delays
        for proper event dispatching.
        
        Parameters
        ----------
        instance : Any
            The widget instance (unused but required by Kivy binding)
        ripple_enabled : bool
            Whether to enable (True) or disable (False) the ripple 
            effect
        """
        if ripple_enabled:
            self.ripple_duration_in = self._ripple_duration_in
            self.ripple_duration_out = self._ripple_duration_out
        else:
            self.ripple_duration_in = 0
            self.ripple_duration_out = 0

    def ripple_show(self, touch: MotionEvent) -> None:
        """Display the ripple effect for a touch event if ripple is
        enabled.
        
        This method overrides the parent's ripple_show to add
        conditional execution based on the ripple_enabled property. If
        ripples are disabled, no visual effect is shown.
        
        Parameters
        ----------
        touch : MotionEvent
            The touch event that triggered the ripple
        """

        if not self.ripple_enabled:
            return None
        
        return super().ripple_show(touch)
    
    def ripple_fade(self) -> None:
        """Fade out the ripple effect if ripple is enabled.
        
        This method overrides the parent's ripple_fade to add conditional
        execution based on the ripple_enabled property. If ripples are
        disabled, no fade-out animation is performed.
        
        Returns:
            None if ripple is disabled, otherwise the result of the parent's
            ripple_fade method
        """
        if not self.ripple_enabled:
            return None
        
        return super().ripple_fade()


class MorphTouchRippleButtonBehavior(
        MorphTouchRippleBehavior,
        TouchRippleButtonBehavior):
    """A button behavior combining touch ripple effects with proper button semantics.

    This behavior extends MorphTouchRippleBehavior to work specifically with
    button widgets, incorporating Kivy's TouchRippleButtonBehavior for proper
    button event handling. It provides a complete button experience with
    configurable ripple effects.
    
    The behavior handles the complex interaction between button press/release
    events and ripple animations, ensuring that button functionality remains
    intact even when ripple effects are disabled.
    
    Example:
        class MyButton(MorphTouchRippleButtonBehavior, ButtonBehavior, Widget):
            def __init__(self, **kwargs):
                super().__init__(**kwargs)
                self.ripple_enabled = True  # Enable ripple for button
    
    Note:
        This behavior should be used with widgets that implement button-like
        interactions. For general touch ripples on non-button widgets, use
        MorphTouchRippleBehavior instead.
    """
