from typing import List
from typing import Tuple

from kivy.event import EventDispatcher
from kivy.graphics import Color
from kivy.graphics import Rectangle
from kivy.graphics import SmoothLine
from kivy.graphics import RoundedRectangle
from kivy.properties import ColorProperty
from kivy.properties import NumericProperty
from kivy.properties import BooleanProperty
from kivy.properties import VariableListProperty
from kivy.uix.relativelayout import RelativeLayout

from ...app import MorphApp
from ...constants import THEME
from ...theme.manager import ThemeManager

__all__ = [
    'MorphStateLayerBehavior']

class MorphStateLayerBehavior(EventDispatcher):
    """A behavior class that provides state layer capabilities.

    This behavior adds a state layer on top of widgets, allowing them to
    display an overlay color based on their state (e.g., pressed, focused,
    hovered). It automatically manages the canvas graphics instructions to
    render the state layer.

    Examples
    --------
    ```pythonpython
    from morphui.app import MorphApp
    from morphui.uix.label import MorphLabel
    from morphui.uix.behaviors import MorphHoverBehavior
    from morphui.uix.behaviors import MorphStateLayerBehavior

    class TestWidget(MorphHoverBehavior, MorphStateLayerBehavior, MorphLabel):
        pass
    
    class MyApp(MorphApp):
        def build(self) -> TestWidget:
            return TestWidget()
    MyApp().run()
    ```

    Notes
    -----
    - The state layer color is determined by the current theme (light or
        dark) to ensure visibility against the background.
    - The opacity of the state layer can be customized for different
        states (hovered, pressed, focused).
    - This behavior assumes that the widget using it has `hovered`,
      `pressed`, and `focused` properties. If these properties are not
      present, the corresponding state layers will not be applied.
    - The state layer is implemented as a semi-transparent rectangle
      that covers the entire widget area.
    - Ensure this behavior is added after any background behaviors to
      ensure the state layer appears above the background.
    """

    radius = VariableListProperty([0], length=4)
    """Canvas radius for each corner.
    
    The order of the corners is: top-left, top-right, bottom-right, 
    bottom-left.
    
    :attr:`radius` is a :class:`~kivy.properties.VariableListProperty`
    and defaults to `[0, 0, 0, 0]`."""

    hovered_state_opacity: float = NumericProperty(0.08)
    """Opacity of the state layer when the widget is hovered.
    
    The opacity is specified as a float between 0 and 1. A value of 0
    means no state layer, while a value of 1 means a fully opaque state.
    
    :attr:`hover_state_opacity` is a 
    :class:`~kivy.properties.NumericProperty` and defaults to `0.08`."""

    pressssed_state_opacity: float = NumericProperty(0.10)
    """Opacity of the state layer when the widget is pressed.

    The opacity is specified as a float between 0 and 1. A value of 0
    means no state layer, while a value of 1 means a fully opaque state.

    :attr:`press_state_opacity` is a
    :class:`~kivy.properties.NumericProperty` and defaults to `0.10`."""

    focused_state_opacity: float = NumericProperty(0.10)
    """Opacity of the state layer when the widget is focused.

    The opacity is specified as a float between 0 and 1. A value of 0
    means no state layer, while a value of 1 means a fully opaque state.

    :attr:`focus_state_opacity` is a
    :class:`~kivy.properties.NumericProperty` and defaults to `0.10`."""

    disabled_state_opacity: float = NumericProperty(0.16)
    """Opacity of the state layer when the widget is disabled.

    The opacity is specified as a float between 0 and 1. A value of 0
    means no state layer, while a value of 1 means a fully opaque state.

    :attr:`disabled_state_opacity` is a
    :class:`~kivy.properties.NumericProperty` and defaults to `0.16`."""

    state_layer_enabled: bool = BooleanProperty(True)
    """Whether to enable the state layer to be displayed.
    
    :attr:`state_layer_enabled` is a :class:`~kivy.properties.BooleanProperty`
    and defaults to `True`."""

    state_layer_color: ColorProperty = ColorProperty([0, 0, 0, 0])
    """Color of the state layer.

    The color should be provided as a list of RGBA values between 0 and
    1. Example: `[0, 0, 0, 0.1]` for a semi-transparent black layer.

    :attr:`state_layer_color` is a 
    :class:`~kivy.properties.ColorProperty` and defaults to 
    `[0, 0, 0, 0]`."""

    _supported_states: Tuple[str, ...] = (
        'disabled', 'pressed', 'focused', 'hovered', 'active')
    """States that the state layer behavior can respond to.

    The values are sorted by precedence, with higher precedence states
    appearing earlier in the tuple. This is used to determine which
    state layer to apply when multiple states are active.
    """

    _state_layer_color_instruction: Color
    """Kivy Color instruction for the state layer color."""

    _state_layer_instruction: Rectangle
    """Kivy Rectangle instruction for the state layer shape."""

    def __init__(self, **kwargs) -> None:
        self.register_event_type('on_state_layer_updated')
        super().__init__(**kwargs)
        
        self.bind(
            pos=self._update_state_layer,
            size=self._update_state_layer,
            radius=self._update_state_layer,
            state_layer_color=self._update_state_layer,)

        for s in self.supported_states:
            self.bind(**{s: lambda _, v, s=s: self._on_state_change(s, v)})

        with self.canvas.before:
            self._state_layer_color_instruction = Color(
                rgba=self.state_layer_color)
            self._state_layer_instruction = RoundedRectangle(
                pos=self.pos,
                size=self.size,
                radius=self.radius,)

        self.refresh_state_layer()

    @property
    def theme_manager(self) -> ThemeManager:
        """Get the current theme manager (read-only).
        
        This property retrieves the theme manager instance from the
        running MorphApp. It is used to determine the current theme
        mode (light or dark) for calculating the state layer color.
        """
        return MorphApp._theme_manager

    @property
    def _base_layer_color(self) -> List[float]:
        """Get the base state layer color(read-only).
        
        The base color is white in dark theme and black in light theme.
        This ensures that the state layer is visible against the
        background. The returned list contains RGB values only.
        """
        color = [0.0, 0.0, 0.0]
        if self.theme_manager.theme_mode == THEME.DARK:
            color = [1 - c for c in color]
        return color
    
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
    
    def _update_state_layer(self, *args) -> None:
        """Update the state layer position and size."""
        self._state_layer_instruction.pos = self.pos
        self._state_layer_instruction.size = self.size
        self._state_layer_instruction.radius = self.radius
        self._state_layer_color_instruction.rgba = self.state_layer_color
        self.dispatch('on_state_layer_updated')

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
        exclude_state : Literal['hovered', 'pressed', 'focused', 'disabled', 'active']
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
    
    def apply_state_layer(self, state: str, opacity: float) -> None:
        """Apply the state layer color for the specified state with the
        given opacity.

        This method sets the state layer color based on the widget's
        current theme (light or dark) and the specified opacity. It is
        called when a state becomes active to visually indicate that
        state.

        Parameters
        ----------
        state : Literal['hovered', 'pressed', 'focused', 'disabled', 'active']
            The interactive state that is being applied. This should be
            one of the states defined in :attr:`supported_states`.
        opacity : float
            The opacity of the state layer, specified as a float
            between 0 and 1. A value of 0 means no state layer, while a
            value of 1 means a fully opaque state layer.

        Examples
        --------
        Apply a hover state layer with 8% opacity:
        
        ```python
        self.apply_state_layer('hovered', 0.08)
        ```

        Notes
        -----
        - This method assumes that the widget using this behavior has
          properties corresponding to the states defined in
          :attr:`supported_states`.
        - The method does not check if other states are active; it is
          assumed that precedence logic is handled elsewhere.
        
        Raises
        ------
        AssertionError
            If the specified state is not in :attr:`supported_states`.
        """
        assert state in self.supported_states, (
            f'State {state!r} is not supported. Supported states are: '
            f'{self.supported_states}')
            
        self.state_layer_color = [*self._base_layer_color[:3], opacity]

    def _on_state_change(self, state: str, value: bool) -> None:
        """Handle changes to the specified state.
        
        This method is called whenever one of the widget's interactive
        states changes (e.g., hovered, pressed, focused). It updates the
        state layer color based on the new state and its precedence.
        """
        if not self.state_layer_enabled or self._has_other_active_states(state):
            return None

        if value:
            self.apply_state_layer(
                state,
                getattr(self, f'{state}_state_opacity', 0))
        else:
            self.state_layer_color = self.theme_manager.transparent_color
    
    def refresh_state_layer(self) -> None:
        """Reapply the current state layer based on the widget's state.

        This method is useful when the theme changes or when the
        widget's state properties are modified externally. It ensures
        that the state layer reflects the current state and theme.
        """
        enabled = self.state_layer_enabled
        self.state_layer_enabled = True
        for state in self.supported_states:
            if getattr(self, state, False):
                self._on_state_change(state, True)
                return
        color = self.theme_manager.transparent_color
        self._state_layer_color_instruction.rgba = color
        self.state_layer_enabled = enabled

    def on_state_layer_updated(self, *args) -> None:
        """Event dispatched when the state layer is updated.

        This can be overridden by subclasses to perform additional
        actions when the state layer changes."""
        pass