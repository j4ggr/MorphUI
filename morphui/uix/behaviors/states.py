from typing import Any
from typing import Set
from typing import Tuple
from typing import Literal
from kivy.properties import OptionProperty

from kivy.event import EventDispatcher


__all__ = [
    'MorphStateBehavior',]


class MorphStateBehavior(EventDispatcher):
    """A behavior class that provides interactive state properties.

    This behavior adds the properties necessary to manage and track
    the current and most relevant interactive state of a widget. If
    multiple states are active, the behavior determines the most
    relevant state based on the defined precedence.

    If a widget does not implement any of the state properties,
    it will default to the 'normal' state.

    Notes
    -----
    This behavior does not implement any visual changes itself. It is 
    intended to be used in conjunction with other behaviors that handle
    visual state changes, such as the layer behaviors:
    - :class:`.layer.MorphSurfaceLayerBehavior`
    - :class:`.layer.MorphInteractionLayerBehavior`
    - :class:`.layer.MorphContentLayerBehavior`
    - :class:`.layer.MorphOverlayLayerBehavior`
    """

    current_state: Literal[
        'normal', 'disabled', 'selected', 'focus', 'hovered', 'pressed',
        'active'
        ] = OptionProperty('normal', options=[
            'disabled', 'selected', 'focus', 'hovered', 'pressed',
            'active', 'normal'])
    """The current interactive state of the widget.

    This property reflects the widget's current state based on the
    active state properties. It can be one of the following values:
    'normal', 'disabled', 'pressed', 'selected', 'focus', 'hovered',
    or 'active'. The value is determined by the precedence of the states
    defined in :attr:`states_precedence`.

    :attr:`current_state` is a :class:`~kivy.properties.OptionProperty` 
    and defaults to 'normal'.
    """

    states_precedence: Tuple[
        Literal['disabled'],
        Literal['selected'], 
        Literal['focus'],
        Literal['hovered'],
        Literal['pressed'],
        Literal['active'],
        Literal['normal']] = (
        'disabled', 'selected', 'focus', 'hovered', 'pressed','active', 
        'normal')
    """States that the state layer behavior can respond to.

    The values are sorted by precedence, with higher precedence states
    appearing earlier in the tuple. This is used to determine which
    state layer to apply when multiple states are active.
    """

    _available_states: Set[str]
    """States that are currently available for the widget.

    This is a subset of :attr:`_states_precedence` that the widget
    actually implements. It is determined dynamically based on which
    state properties are currently active.
    """

    def __init__(self, **kwargs) -> None:
        self._available_states = set('normal')
        super().__init__(**kwargs)

        self.update_available_states()
    
    @property
    def available_states(self) -> Set[str]:
        """States that are currently available for the widget
        (read-only).

        This set keeps track of the states that the widget currently
        has properties for and can respond to. It is a subset of
        :attr:`states_precedence`. To automatically manage available
        states based on the widget's properties, call
        :meth:`update_available_states`.
        """
        return self._available_states

    def update_available_states(self) -> None:
        """Update the set of available states based on the widget's
        properties.

        This method checks which of the states defined in
        :attr:`states_precedence` the widget currently has properties
        for and updates the :attr:`available_states` set accordingly.
        """
        for state in self.available_states:
            self.funbind(state, self._update_current_state)
        self._available_states.clear()
        
        for state in self.states_precedence:
            if hasattr(self, state):
                self._available_states.add(state)
                self.fbind(state, self._update_current_state, state=state)
        self._available_states.add('normal')

    def _update_current_state(
            self,
            instance: Any,
            value: bool,
            state: Literal[
                'disabled', 'pressed', 'selected', 'focus', 'hovered', 
                'active', 'normal']
            ) -> None:
        """Handle changes to state properties.

        This method is called whenever one of the state properties
        changes. It updates the :attr:`current_state` property based on
        the active states and their precedence.

        Parameters
        ----------
        instance : Any
            The instance of the class where the property changed.
        value : bool
            The new value of the property.
        state : str
            The name of the state property that changed.
        """
        if state == self.current_state and not value:
            self.current_state = 'normal'
            return None
        
        for resolved_state in self.states_precedence:
            if resolved_state not in self.available_states:
                continue

            if resolved_state == state:
                self.current_state = state if value else 'normal'
                return None

    def on_current_state(
            self,
            instance: Any,
            value: Literal[
                'normal', 'disabled', 'pressed', 'selected', 'focus',
                'hovered', 'active']
            ) -> None:
        """Handle changes to the current_state property.

        This method is called whenever the :attr:`current_state`
        property changes. It can be overridden in subclasses to
        implement custom behavior when the current state changes.

        Parameters
        ----------
        instance : Any
            The instance of the class where the property changed.
        value : str
            The new value of the current_state property.
        """
        pass