from typing import List
from typing import Tuple
from typing import Literal

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
    'MorphBackgroundBehavior',
    'MorphStateLayerBehavior']


class MorphBackgroundBehavior(EventDispatcher):
    """A behavior class that provides background and border styling 
    capabilities.

    This behavior adds background color, border color, border width, and 
    corner radius properties to widgets. It automatically manages the 
    canvas graphics instructions to render a rounded rectangle 
    background with optional border.
    """

    radius = VariableListProperty([0], length=4)
    """Canvas radius for each corner.
    
    The order of the corners is: top-left, top-right, bottom-right, 
    bottom-left.
    
    :attr:`radius` is a :class:`~kivy.properties.VariableListProperty`
    and defaults to `[0, 0, 0, 0]`."""

    background_color: ColorProperty = ColorProperty()
    """Background color of the widget.
    
    The color should be provided as a list of RGBA values between 0 and 
    1. Example: `[1, 0, 0, 1]` for solid red.
    
    :attr:`background_color` is a :class:`~kivy.properties.ColorProperty`
    and defaults to `[1, 1, 1, 1]` (white)."""

    border_color: ColorProperty = ColorProperty([0, 0, 0, 0])
    """Border color of the widget.
    
    The color should be provided as a list of RGBA values between 0 and 
    1. Example: `[0, 1, 0, 1]` for solid green.

    :attr:`border_color` is a :class:`~kivy.properties.ColorProperty`
    and defaults to `[0, 0, 0, 0]` (transparent)."""

    border_width: float = NumericProperty(1, min=0.01)
    """Width of the border.

    The width is specified in pixels.
    
    :attr:`border_width` is a :class:`~kivy.properties.NumericProperty`
    and defaults to `1` (1 pixel wide).
    """

    _background_color_instruction: Color
    """Kivy Color instruction for the background color."""

    _background_instruction: RoundedRectangle
    """Kivy RoundedRectangle instruction for the background shape."""

    _border_color_instruction: Color
    """Kivy Color instruction for the border color."""

    _border_instruction: SmoothLine
    """Kivy SmoothLine instruction for the border."""

    def __init__(self, **kwargs) -> None:
        """Initialize the background behavior with canvas graphics 
        instructions.
        
        Parameters
        ----------
        **kwargs
            Additional keyword arguments passed to the parent class.
        """
        self.register_event_type('on_background_update')
        super().__init__(**kwargs)
        self.bind(
            background_color=self._update_background,
            size=self._update_background,
            pos=self._update_background,
            radius=self._update_background,
            border_color=self._update_background,
            border_width=self._update_background,)
        
        with self.canvas.before:
            self._background_color_instruction = Color(*self.background_color)
            self._background_instruction = RoundedRectangle(
                size=self.size,
                pos=self.pos,
                radius=self.radius)
            self._border_color_instruction = Color(*self.border_color)
            self._border_instruction = SmoothLine(
                width=self.border_width,
                rounded_rectangle=self._rounded_rectangle)
    
    @property
    def _rounded_rectangle(self) -> RoundedRectangle:
        """Get the parameters for creating a rounded rectangle (read-only).
        
        Returns
        -------
        list of float
            List containing [x, y, width, height, *radius] for the 
            rounded rectangle.
        """
        is_relative = isinstance(self, RelativeLayout)
        return [
            0 if is_relative else self.x,
            0 if is_relative else self.y,
            self.width,
            self.height,
            *self.radius,]
    
    def _update_background(self, *args) -> None:
        """Update the background when any relevant property changes."""
        self._background_color_instruction.rgba = self.background_color
        self._background_instruction.pos = self.pos
        self._background_instruction.size = self.size
        self._background_instruction.radius = self.radius
        
        self._border_color_instruction.rgba = self.border_color
        self._border_instruction.width = self.border_width
        self._border_instruction.rounded_rectangle = self._rounded_rectangle

        self.dispatch('on_background_update')

    def on_background_update(self, *args) -> None:
        """Event dispatched when the background is updated.
        
        This can be overridden by subclasses to perform additional
        actions when the background changes."""
        pass


class MorphStateLayerBehavior(MorphBackgroundBehavior):
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

    allow_state_layer: bool = BooleanProperty(True)
    """Whether to allow the state layer to be displayed.
    
    :attr:`allow_state_layer` is a :class:`~kivy.properties.BooleanProperty`
    and defaults to `True`."""

    _supported_states: Tuple[str, ...] = (
        'pressed', 'focused', 'hovered', 'disabled', 'active')
    """States that the state layer behavior can respond to."""

    _state_layer_color_instruction: Color
    """Kivy Color instruction for the state layer color."""

    _state_layer_instruction: Rectangle
    """Kivy Rectangle instruction for the state layer shape."""

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
        
        for s in self.supported_states:
            self.bind(**{s: lambda _, v, s=s: self._on_state_change(s, v)})

    def _update_state_layer(self, *args) -> None:
        """Update the state layer position and size."""
        self._state_layer_instruction.pos = self.pos
        self._state_layer_instruction.size = self.size
        self.dispatch('on_state_layer_update')

    @property
    def _base_layer_color(self) -> List[float]:
        """Get the base state layer color(read-only).
        
        The base color is white in dark theme and black in light theme.
        This ensures that the state layer is visible against the
        background. The returned list contains RGB values only.
        """
        if self.theme_manager.theme_mode == THEME.DARK:
            return [1, 1, 1]
        return [0, 0, 0]
    
    @property
    def supported_states(self) -> Tuple[str, ...]:
        """States that the state layer behavior can respond to
        (read-only).
        
        This tuple defines the interactive states that the behavior
        recognizes and can apply state layers for. Widgets using this
        behavior should have corresponding properties for these states.
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
        other_states = (
            s for s in self.supported_states if s != exclude_state)
        return any(
            getattr(self, state, False) for state in other_states)
    
    def _on_state_change(self, state: str, value: bool) -> None:
        """Handle changes to the specified state."""
        if not self.allow_state_layer or self._has_other_active_states(state):
            return None
        
        if state in ('hovered', 'pressed', 'focused'):
            if value:
                opacity = getattr(self, f'{state}_state_opacity', 0)
                color = (*self._base_layer_color, opacity)
            else:
                color = self.theme_manager.transparent_color
            self._state_layer_color_instruction.rgba = color
            self.dispatch('on_state_layer_update')

    def on_state_layer_update(self, *args) -> None:
        """Event dispatched when the state layer is updated.

        This can be overridden by subclasses to perform additional
        actions when the state layer changes."""
        pass