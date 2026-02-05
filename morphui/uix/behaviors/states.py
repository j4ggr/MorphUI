from typing import Any
from typing import Set
from typing import Tuple
from typing import Literal
from typing import get_args
from typing import cast

from kivy.event import EventDispatcher
from kivy.properties import StringProperty

from morphui._typing import State
from morphui._typing import SurfaceState
from morphui._typing import ContentState
from morphui._typing import OverlayState
from morphui._typing import InteractionState


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

    current_surface_state: SurfaceState = StringProperty('normal')
    """The current surface state of the widget.

    This property reflects the widget's current state used for surface
    interactions. It can be one of the following values: 'normal',
    'disabled' or 'active'. The value is determined by the
    precedence of the states defined in :attr:`states_precedence`.

    :attr:`current_surface_state` is a
    :class:`~kivy.properties.StringProperty` and defaults to 'normal'.
    """

    current_interaction_state: InteractionState = StringProperty('normal')
    """The current interaction state of the widget.

    This property reflects the widget's current state used for 
    interaction events. It can be one of the following values: 
    'disabled', 'pressed', 'hovered' or 'normal'. The value is 
    determined by the precedence of the states defined in
    :attr:`states_precedence`.

    :attr:`current_interaction_state` is a
    :class:`~kivy.properties.StringProperty` and defaults to 'normal'.
    """

    current_content_state: ContentState = StringProperty('normal')
    """The current content state of the widget.

    This property reflects the widget's current state used for content
    interactions. It can be one of the following values: 'disabled',
    'hovered', 'active' or 'normal'. The value is determined by the 
    precedence of the states defined in :attr:`states_precedence`.

    :attr:`current_content_state` is a
    :class:`~kivy.properties.StringProperty` and defaults to 'normal'.
    """

    current_overlay_state: OverlayState = StringProperty('normal')
    """The current overlay state of the widget.

    This property reflects the widget's current state used for overlay
    interactions. It can be one of the following values: 'disabled',
    'resizing', 'dragging' or 'normal'. The value is determined by the
    precedence of the states defined in :attr:`states_precedence`.

    :attr:`current_overlay_state` is a
    :class:`~kivy.properties.StringProperty` and defaults to 'normal'.
    """

    possible_states: Set[str] = set(get_args(State))
    """All possible states that can be used by the widget.

    This set contains all the states defined in the :class:`State`
    type alias. It is used to validate state properties and ensure
    that only valid states are assigned to the widget.

    Default states are defined by :class:`~morphui._typing.State`.
    """

    surface_state_precedence: Tuple[str, ...] = get_args(SurfaceState)
    """The precedence order for surface states.

    This tuple defines the order of precedence for surface states,
    with the first state having the highest precedence and the last
    state having the lowest precedence.

    Default order is defined by :class:`~morphui._typing.SurfaceState`.
    """

    interaction_state_precedence: Tuple[str, ...] = get_args(InteractionState)
    """The precedence order for interaction states.

    This tuple defines the order of precedence for interaction states,
    with the first state having the highest precedence and the last
    state having the lowest precedence.

    Default order is defined by 
    :class:`~morphui._typing.InteractionState`.
    """

    content_state_precedence: Tuple[str, ...] = get_args(ContentState)
    """The precedence order for content states.

    This tuple defines the order of precedence for content states,
    with the first state having the highest precedence and the last
    state having the lowest precedence.

    Default order is defined by :class:`~morphui._typing.ContentState`.
    """

    overlay_state_precedence: Tuple[str, ...] = get_args(OverlayState)
    """The precedence order for overlay states.

    This tuple defines the order of precedence for overlay states,
    with the first state having the highest precedence and the last
    state having the lowest precedence.

    Default order is defined by :class:`~morphui._typing.OverlayState`.
    """

    _available_states: Set[str]
    """States that are currently available for the widget.

    This is a subset of :attr:`_states_precedence` that the widget
    actually implements. It is determined dynamically based on which
    state properties are currently active.
    """

    def __init__(self, **kwargs) -> None:
        self.register_event_type('on_current_state_changed')
        self._available_states = {'normal'}
        super().__init__(**kwargs)
        self.refresh_state()
    
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
        properties = self.properties()
        for state in self.available_states:
            if state in properties:
                self.funbind(state, self._update_current_state)
        self._available_states.clear()
        
        for state in self.possible_states:
            if hasattr(self, state):
                self._available_states.add(state)
                if state in properties:
                    self.fbind(state, self._update_current_state, state=state)
        self._available_states.add('normal')

    def _update_current_state(
            self,
            instance: Any,
            value: bool,
            state: Literal[
                'disabled', 'pressed', 'focus', 'hovered', 'active', 'normal'] # TODO: generalize
            ) -> None:
        """Handle changes to state properties.

        This method is called whenever one of the state properties
        changes. It updates the current state properties based on
        the active states and their individual precedence.

        Parameters
        ----------
        instance : Any
            The instance of the class where the property changed.
        value : bool
            The new value of the property.
        state : str
            The name of the state property that changed.
        """
        self.current_interaction_state = cast(
            InteractionState,
            self._resolve_state(
                new_state=state,
                current_state=self.current_interaction_state,
                precedence=self.interaction_state_precedence,
                value=value))
        
        self.current_surface_state = cast(
            SurfaceState,
            self._resolve_state(
                new_state=state,
                current_state=self.current_surface_state,
                precedence=self.surface_state_precedence,
                value=value))
        
        self.current_content_state = cast(
            ContentState,
            self._resolve_state(
                new_state=state,
                current_state=self.current_content_state,
                precedence=self.content_state_precedence,
                value=value))
        
        self.current_overlay_state = cast(
            OverlayState,
            self._resolve_state(
                new_state=state,
                current_state=self.current_overlay_state,
                precedence=self.overlay_state_precedence,
                value=value))
        self.dispatch('on_current_state_changed')

    def refresh_state(self) -> None:
        """Re-evaluate the current state based on the widget's
        properties.

        This method is useful when the widget's properties are modified
        externally and the state needs to be updated accordingly. It
        ensures that the current state properties reflect the actual
        state of the widget based on its properties.
        """
        
        self.update_available_states()
        for state in self.available_states:
            value = getattr(self, state, False)
            if not isinstance(value, bool):
                continue
            self._update_current_state(
                instance=self, 
                value=value,
                state=state) # type: ignore

    def _resolve_state(
            self,
            new_state: State,
            current_state: State,
            precedence: Tuple[str, ...],
            value: bool
            ) -> State:
        """Determine the most relevant current state based on active
        states and their precedence.

        This method checks the active states in order of precedence
        and returns the highest precedence state that is currently
        active. If no states are active, it returns 'normal'.

        Parameters
        ----------
        new_state : State
            The new state to consider.
        current_state : State
            The current state of the widget.
        precedence : Tuple[str, ...]
            The order of precedence for the states.
        value : bool
            The new value of the state property.

        Returns
        -------
        State
            The most relevant current state.
        """
        sorted_states = (s for s in precedence if s in self.available_states)
        for state in sorted_states:

            if state == current_state and value:
                return current_state

            if state == new_state and value:
                return new_state
            
            if getattr(self, state, False):
                return state # type: ignore

        return 'normal'

    def on_current_state_changed(self, *args) -> None:
        """Event fired when the current state changes.

        This event is dispatched whenever the current state properties
        are updated. It can be used to trigger visual updates or other
        actions in response to state changes. Override this method
        in subclasses to handle the event.
        """
        pass