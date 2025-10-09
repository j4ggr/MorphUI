from typing import Any
from typing import Tuple

from kivy.event import EventDispatcher
from kivy.properties import BooleanProperty


__all__ = [
    'MorphStatesBehavior',]


class MorphStatesBehavior(EventDispatcher):
    """A behavior class that provides interactive state properties.
    
    This behavior adds properties for common interactive states such as
    `disabled`, `pressed`, `focus`, `hovered`, and `active`. It also
    includes a `state_enabled` property to enable or disable state
    handling.
    
    Widgets using this behavior can respond to changes in these state
    properties to update their appearance or behavior accordingly.
    """

    disabled: bool = BooleanProperty(False)
    """Whether the widget is disabled.

    :attr:`disabled` is a :class:`~kivy.properties.BooleanProperty`
    and defaults to `False`.
    """

    pressed: bool = BooleanProperty(False)
    """Whether the widget is pressed.

    :attr:`pressed` is a :class:`~kivy.properties.BooleanProperty`
    and defaults to `False`.
    """

    selected: bool = BooleanProperty(False)
    """Whether the widget is selected.

    :attr:`selected` is a :class:`~kivy.properties.BooleanProperty`
    and defaults to `False`.
    """

    focus: bool = BooleanProperty(False)
    """Whether the widget has focus.

    :attr:`focus` is a :class:`~kivy.properties.BooleanProperty`
    and defaults to `False`.
    """

    hovered: bool = BooleanProperty(False)
    """Whether the mouse is hovering over the widget.

    :attr:`hovered` is a :class:`~kivy.properties.BooleanProperty`
    and defaults to `False`.
    """

    active: bool = BooleanProperty(False)
    """Whether the widget is active.

    :attr:`active` is a :class:`~kivy.properties.BooleanProperty`
    and defaults to `False`.
    """

    state_enabled: bool = BooleanProperty(True)
    """Whether state handling is enabled.

    Disabling state handling will prevent the application of state 
    layers and any visual changes associated with interactive states.

    :attr:`state_enabled` is a :class:`~kivy.properties.BooleanProperty`
    and defaults to `True`.
    """

    _supported_states: Tuple[str, ...] = (
        'disabled', 'pressed', 'selected', 'focus', 'hovered', 'active')
    """States that the state layer behavior can respond to.

    The values are sorted by precedence, with higher precedence states
    appearing earlier in the tuple. This is used to determine which
    state layer to apply when multiple states are active.
    """
    
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        for state in self.supported_states:
            self.fbind(state, self._on_state_change, state=state)
    
    @property
    def supported_states(self) -> Tuple[str, ...]:
        """States that the state layer behavior can respond to
        (read-only).
        
        This tuple defines the interactive states that the behavior
        recognizes and can apply state layers for. Widgets using this
        behavior should have corresponding properties for these states.

        The values are sorted by precedence, with higher precedence
        states appearing earlier in the tuple. This is used to determine
        which state layer to apply when multiple states are active.
        """
        return tuple(s for s in self._supported_states if hasattr(self, s))
    
    def _has_other_active_states(self, exclude_state: str) -> bool:
        """Check if any state other than the excluded one is currently
        active.

        This method determines whether any of the widget's interactive
        states (see :attr:`supported_states`) are currently active, 
        excluding the specified state. This is useful for state
        precedence logic where certain states should take priority over
        others.
        
        Parameters
        ----------
        exclude_state : Literal[
                'disabled', 'pressed', 'selected', 'focus', 'hovered', 'active']
            The state to exclude from the check. Typically this is the
            state that is currently being evaluated for
            activation/deactivation.
            
        Returns
        -------
        bool
            True if any state other than `exclude_state` is currently
            active, False if no other states are active.
            
        Examples
        --------
        Check if other states are active when handling hover:
        
        ```python
        if not self._has_other_active_states('hovered'):
            # Safe to apply hover state layer
            self.apply_hover_layer()
        ```
        
        Notes
        -----
        This method safely handles cases where the widget doesn't have
        one or more of the expected state properties by using getattr
        with a default value of False.
        """
        for state in self.supported_states:
            if state == exclude_state:
                continue
            if state in self.supported_states and getattr(self, state, False):
                return True

        return False

    def _on_state_change(self, instance: Any, value: bool, state: str) -> None:
        """Handle changes to state properties.

        This method is called whenever one of the state properties
        changes. It can be overridden by subclasses to implement custom
        behavior in response to state changes.

        Parameters
        ----------
        instance : Any
            The instance of the class where the property changed.
        value : bool
            The new value of the property.
        state : str
            The name of the state property that changed.
        """
        pass