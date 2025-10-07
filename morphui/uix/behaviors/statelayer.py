from typing import Any
from typing import List
from typing import Literal

from kivy.event import EventDispatcher
from kivy.graphics import Color
from kivy.graphics import Rectangle
from kivy.properties import NumericProperty
from kivy.properties import VariableListProperty

from ...app import MorphApp
from ...constants import THEME
from ...theme.manager import ThemeManager


__all__ = [
    'MorphStateLayerBehavior',]


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

    hover_state_opacity: float = NumericProperty(0.08)
    """Opacity of the state layer when the widget is hovered.
    
    The opacity is specified as a float between 0 and 1. A value of 0
    means no state layer, while a value of 1 means a fully opaque state.
    
    :attr:`hover_state_opacity` is a 
    :class:`~kivy.properties.NumericProperty` and defaults to `0.08`."""

    press_state_opacity: float = NumericProperty(0.10)
    """Opacity of the state layer when the widget is pressed.

    The opacity is specified as a float between 0 and 1. A value of 0
    means no state layer, while a value of 1 means a fully opaque state.

    :attr:`press_state_opacity` is a
    :class:`~kivy.properties.NumericProperty` and defaults to `0.10`."""

    focus_state_opacity: float = NumericProperty(0.10)
    """Opacity of the state layer when the widget is focused.

    The opacity is specified as a float between 0 and 1. A value of 0
    means no state layer, while a value of 1 means a fully opaque state.

    :attr:`focus_state_opacity` is a
    :class:`~kivy.properties.NumericProperty` and defaults to `0.10`."""

    allow_state_layer: bool = NumericProperty(True)
    """Whether to allow the state layer to be displayed.
    
    :attr:`allow_state_layer` is a :class:`~kivy.properties.BooleanProperty`
    and defaults to `True`."""

    _state_layer_color_instruction: Color
    """Kivy Color instruction for the state layer color."""

    _state_layer_instruction: Rectangle
    """Kivy Rectangle instruction for the state layer shape."""

    _theme_manager: ThemeManager = MorphApp._theme_manager
    """Reference to the global ThemeManager instance."""

    def __init__(self, **kwargs) -> None:
        self.register_event_type('on_state_layer_update')
        super().__init__(**kwargs)
        with self.canvas.before:
            self._state_layer_color_instruction = Color(rgba=[0, 0, 0, 0])
            self._state_layer_instruction = Rectangle(
                pos=self.pos,
                size=self.size,)
        self.bind(
            pos=self._update_state_layer,
            size=self._update_state_layer,
            radius=self._update_state_layer,)
        if hasattr(self, 'hovered'):
            self.bind(hovered=self._on_hovered_state_change)
        if hasattr(self, 'pressed'):
            self.bind(pressed=self._on_pressed_state_change)
        if hasattr(self, 'focused'):
            self.bind(focused=self._on_focused_state_change)
    
    def _update_state_layer(self, *args) -> None:
        """Update the state layer position and size."""
        self._state_layer_instruction.pos = self.pos
        self._state_layer_instruction.size = self.size
        self.dispatch('on_state_layer_update')

    @property
    def _base_state_color(self) -> List[float]:
        """Get the base state color(read-only).
        
        The base color is white in dark theme and black in light theme.
        This ensures that the state layer is visible against the
        background. The returned list contains RGB values only.
        """
        if self._theme_manager.theme_mode == THEME.DARK:
            return [1, 1, 1]
        return [0, 0, 0]
    
    def _has_other_active_states(
            self,
            exclude_state: Literal['hovered', 'pressed', 'focused']
            ) -> bool:
        """Check if any state other than the excluded one is currently active.
        
        This method determines whether any of the widget's interactive states
        (hovered, pressed, focused) are currently active, excluding the specified
        state. This is useful for state precedence logic where certain states
        should take priority over others.
        
        Parameters
        ----------
        exclude_state : Literal['hovered', 'pressed', 'focused']
            The state to exclude from the check. Typically this is the state
            that is currently being evaluated for activation/deactivation.
            
        Returns
        -------
        bool
            True if any state other than `exclude_state` is currently active,
            False if no other states are active.
            
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
        This method safely handles cases where the widget doesn't have one
        or more of the expected state properties by using getattr with a
        default value of False.
        """
        other_states = (
            state for state in ('hovered', 'pressed', 'focused', 'disabled') 
            if state != exclude_state)
        return any(
            getattr(self, state, False) for state in other_states)

    def _on_hovered_state_change(self, instance: Any, hovered: bool) -> None:
        """Handle changes to the hovered state.
        
        If the widget is pressed or focused, hovering does not change 
        the state layer."""
        if self._has_other_active_states('hovered'):
            return None
        
        if hovered:
            color = (*self._base_state_color, self.hover_state_opacity)
        else:
            color = self._theme_manager.transparent_color
        self._state_layer_color_instruction.rgba = color
        self.dispatch('on_state_layer_update')

    def _on_pressed_state_change(self, instance: Any, pressed: bool) -> None:
        """Handle changes to the pressed state."""
        if self._has_other_active_states('pressed'):
            return None

        if pressed:
            color = (*self._base_state_color, self.press_state_opacity)
        else:
            color = self._theme_manager.transparent_color
        self._state_layer_color_instruction.rgba = color
        self.dispatch('on_state_layer_update')

    def _on_focused_state_change(self, instance: Any, focused: bool) -> None:
        """Handle changes to the focused state."""
        if self._has_other_active_states('focused'):
            return None
        
        if focused:
            color = (*self._base_state_color, self.focus_state_opacity)
        else:
            color = self._theme_manager.transparent_color
        self._state_layer_color_instruction.rgba = color
        self.dispatch('on_state_layer_update')

    def on_state_layer_update(self, *args) -> None:
        """Event dispatched when the state layer is updated.

        This can be overridden by subclasses to perform additional
        actions when the state layer changes."""
        pass