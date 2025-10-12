from typing import Any
from typing import List

from kivy.graphics import Color
from kivy.graphics import Rectangle
from kivy.graphics import SmoothLine
from kivy.graphics import RoundedRectangle
from kivy.properties import ColorProperty
from kivy.properties import NumericProperty
from kivy.properties import BooleanProperty
from kivy.properties import VariableListProperty
from kivy.uix.relativelayout import RelativeLayout

from ...constants import INSTRUCTION_GROUP

from .appreference import MorphAppReferenceBehavior
from .states import MorphStateBehavior


__all__ = [
    'MorphSurfaceLayerBehavior',
    'MorphInteractionLayerBehavior',
    'MorphContentLayerBehavior',
    'MorphInteractiveLayerBehavior',
    'MorphTextLayerBehavior',
    'MorphCompleteLayerBehavior',]


class BaseLayerBehavior(
        MorphStateBehavior,
        MorphAppReferenceBehavior):
    """Base class for layer behaviors to provide common functionality."""

    radius = VariableListProperty([0], length=4)
    """Canvas radius for each corner.
    
    The order of the corners is: top-left, top-right, bottom-right, 
    bottom-left.
    
    :attr:`radius` is a :class:`~kivy.properties.VariableListProperty`
    and defaults to `[0, 0, 0, 0]`."""
    
    @property
    def _rectangle_params(self) -> List[float]:
        """Get the parameters for creating a rounded rectangle
        (read-only).

        The parameters are returned as a list suitable for use in
        :class:`~kivy.graphics.instructions.SmoothLine` instruction. If 
        the widget is a `RelativeLayout`, the position is set to (0, 0)
        to ensure correct rendering within the layout's coordinate
        system.
        
        Returns
        -------
        list of float
            List containing [x, y, width, height, *radius] for the 
            rounded rectangle.
        """
        is_relative = isinstance(self, RelativeLayout)
        params = [
            0 if is_relative else self.x,
            0 if is_relative else self.y,
            self.width,
            self.height,
            *self.radius,]
        return params
    

class MorphSurfaceLayerBehavior(BaseLayerBehavior):
    """A behavior class that provides surface and border styling 
    capabilities. Also known as the "surface" layer".

    This behavior adds surface color, border color, border width, and 
    corner radius properties to widgets. It automatically manages the 
    canvas graphics instructions to render a rounded rectangle 
    surface with optional border.
    """

    surface_color: ColorProperty = ColorProperty()
    """Background color of the widget.
    
    The color should be provided as a list of RGBA values between 0 and 
    1. Example: `[1, 0, 0, 1]` for solid red.
    
    :attr:`surface_color` is a :class:`~kivy.properties.ColorProperty`
    and defaults to `[1, 1, 1, 1]` (white)."""

    disabled_surface_color: ColorProperty = ColorProperty([0, 0, 0, 0])
    """Background color when the widget is disabled.

    This color is applied when the widget is in a disabled state.
    It should be a fully transparent color if you are using state layer.
    Otherwise, it can be set to any RGBA color.

    :attr:`disabled_surface_color` is a
    :class:`~kivy.properties.ColorProperty` and defaults to 
    `[0, 0, 0, 0]` (transparent)."""

    selected_surface_color: ColorProperty = ColorProperty([0, 0, 0, 0])
    """Background color when the widget is selected.

    This color is applied when the widget is in a selected state.

    :attr:`selected_surface_color` is a
    :class:`~kivy.properties.ColorProperty` and defaults to
    `[0, 0, 0, 0]` (transparent)."""

    active_surface_color: ColorProperty = ColorProperty([0, 0, 0, 0])
    """Background color when the widget is active.

    :attr:`active_surface_color` is a
    :class:`~kivy.properties.ColorProperty` and defaults to
    `[0, 0, 0, 0]` (transparent)."""

    border_color: ColorProperty = ColorProperty([0, 0, 0, 0])
    """Border color of the widget.
    
    The color should be provided as a list of RGBA values between 0 and 
    1. Example: `[0, 1, 0, 1]` for solid green.

    :attr:`border_color` is a :class:`~kivy.properties.ColorProperty`
    and defaults to `[0, 0, 0, 0]` (transparent)."""

    disabled_border_color: ColorProperty = ColorProperty([0, 0, 0, 0])
    """Border color when the widget is disabled.

    This color is applied when the widget is in a disabled state.

    :attr:`disabled_border_color` is a
    :class:`~kivy.properties.ColorProperty` and defaults to
    `[0, 0, 0, 0]` (transparent)."""

    selected_border_color: ColorProperty = ColorProperty([0, 0, 0, 0])
    """Border color when the widget is selected.

    This color is applied when the widget is in a selected state.

    :attr:`selected_border_color` is a
    :class:`~kivy.properties.ColorProperty` and defaults to
    `[0, 0, 0, 0]` (transparent)."""

    active_border_color: ColorProperty = ColorProperty([0, 0, 0, 0])
    """Border color when the widget is active.

    :attr:`active_border_color` is a
    :class:`~kivy.properties.ColorProperty` and defaults to
    `[0, 0, 0, 0]` (transparent)."""

    border_width: float = NumericProperty(1, min=0.01)
    """Width of the border.

    The width is specified in pixels.
    
    :attr:`border_width` is a :class:`~kivy.properties.NumericProperty`
    and defaults to `1` (1 pixel wide).
    """

    _surface_color_instruction: Color
    """Kivy Color instruction for the surface color."""

    _surface_instruction: RoundedRectangle
    """Kivy RoundedRectangle instruction for the surface shape."""

    _border_color_instruction: Color
    """Kivy Color instruction for the border color."""

    _border_instruction: SmoothLine
    """Kivy SmoothLine instruction for the border."""

    def __init__(self, **kwargs) -> None:
        """Initialize the surface behavior with canvas graphics 
        instructions.
        
        Parameters
        ----------
        **kwargs
            Additional keyword arguments passed to the parent class.
        """
        self.register_event_type('on_surface_updated')
        super().__init__(**kwargs)

        group = INSTRUCTION_GROUP.SURFACE
        with self.canvas.before:
            self._surface_color_instruction = Color(
                rgba=self.surface_color,
                group=group)
            self._surface_instruction = RoundedRectangle(
                size=self.size,
                pos=self.pos,
                radius=self.radius,
                group=group)
            self._border_color_instruction = Color(
                rgba=self.border_color,
                group=group)
            self._border_instruction = SmoothLine(
                width=self.border_width,
                rounded_rectangle=self._rectangle_params,
                group=group)

        self.bind(
            surface_color=self._update_surface_layer,
            size=self._update_surface_layer,
            pos=self._update_surface_layer,
            radius=self._update_surface_layer,
            border_color=self._update_surface_layer,
            border_width=self._update_surface_layer,
            current_state=self._update_surface_layer,)
    
    def _update_surface_layer(self, *args) -> None:
        """Update the surface when any relevant property changes."""
        match self.current_state:
            case 'disabled':
                surface_color = self.disabled_surface_color
                border_color = self.disabled_border_color
            case 'selected':
                surface_color = self.selected_surface_color
                border_color = self.selected_border_color
            case 'active':
                surface_color = self.active_surface_color
                border_color = self.active_border_color
            case _:
                surface_color = self.surface_color
                border_color = self.border_color

        self._surface_color_instruction.rgba = surface_color
        self._surface_instruction.pos = self.pos
        self._surface_instruction.size = self.size
        self._surface_instruction.radius = self.radius
        
        self._border_color_instruction.rgba = border_color
        self._border_instruction.width = self.border_width
        self._border_instruction.rounded_rectangle = self._rectangle_params

        self.dispatch('on_surface_updated')

    def on_surface_updated(self, *args) -> None:
        """Event dispatched when the surface is updated.
        
        This can be overridden by subclasses to perform additional
        actions when the surface changes."""
        pass


class MorphInteractionLayerBehavior(BaseLayerBehavior):
    """A behavior class that provides state layer capabilities.

    This behavior adds a state layer on top of widgets, allowing them to
    display an overlay color based on their state (e.g., pressed, focus,
    hovered). It automatically manages the canvas graphics instructions to
    render the state layer.

    Examples
    --------
    ```pythonpython
    from morphui.app import MorphApp
    from morphui.uix.label import MorphLabel
    from morphui.uix.behaviors import MorphHoverBehavior
    from morphui.uix.behaviors import MorphInteractionLayerBehavior

    class TestWidget(MorphHoverBehavior, MorphInteractionLayerBehavior, MorphLabel):
        pass
    
    class MyApp(MorphApp):
        def build(self) -> TestWidget:
            return TestWidget()
    MyApp().run()
    ```

    Notes
    -----
    - The interaction layer color is determined by the current theme 
      (light or dark) to ensure visibility against the surface.
    - The opacity of the state layer can be customized for different
        states (hovered, pressed, focus).
    - This behavior assumes that the widget using it has `hovered`,
      `pressed`, and `focus` properties. If these properties are not
      present, the corresponding state layers will not be applied.
    - The state layer is implemented as a semi-transparent rectangle
      that covers the entire widget area.
    - Ensure this behavior is added after any surface behaviors to
      ensure the state layer appears above the surface.
    """

    hovered_state_opacity: float = NumericProperty(0.08)
    """Opacity of the state layer when the widget is hovered.
    
    The opacity is specified as a float between 0 and 1. A value of 0
    means no state layer, while a value of 1 means a fully opaque state.
    
    :attr:`hovered_state_opacity` is a 
    :class:`~kivy.properties.NumericProperty` and defaults to `0.08`."""

    pressed_state_opacity: float = NumericProperty(0.10)
    """Opacity of the state layer when the widget is pressed.

    The opacity is specified as a float between 0 and 1. A value of 0
    means no state layer, while a value of 1 means a fully opaque state.

    :attr:`pressed_state_opacity` is a
    :class:`~kivy.properties.NumericProperty` and defaults to `0.10`."""

    focus_state_opacity: float = NumericProperty(0.10)
    """Opacity of the state layer when the widget is focus.

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

    interaction_enabled: bool = BooleanProperty(True)
    """Whether to enable the interaction layer (state-layer) to be 
    displayed.

    :attr:`interaction_enabled` is a 
    :class:`~kivy.properties.BooleanProperty` and defaults to `True`."""

    interaction_color: ColorProperty = ColorProperty([0, 0, 0, 0])
    """Color of the state layer.

    The color should be provided as a list of RGBA values between 0 and
    1. Example: `[0, 0, 0, 0.1]` for a semi-transparent black layer.

    :attr:`interaction_color` is a 
    :class:`~kivy.properties.ColorProperty` and defaults to 
    `[0, 0, 0, 0]`."""

    _interaction_color_instruction: Color
    """Kivy Color instruction for the state layer color."""

    _interaction_instruction: Rectangle
    """Kivy Rectangle instruction for the state layer shape."""

    def __init__(self, **kwargs) -> None:
        self.register_event_type('on_interaction_updated')
        super().__init__(**kwargs)

        group = INSTRUCTION_GROUP.INTERACTION
        with self.canvas.before:
            self._interaction_color_instruction = Color(
                rgba=self.interaction_color,
                group=group)
            self._interaction_instruction = RoundedRectangle(
                pos=self.pos,
                size=self.size,
                radius=self.radius,
                group=group)
        
        self.bind(
            pos=self._update_interaction_layer,
            size=self._update_interaction_layer,
            radius=self._update_interaction_layer,
            interaction_color=self._update_interaction_layer,
            current_state=self._on_state_change,)

        self.refresh_interaction()

    @property
    def _interaction_color(self) -> List[float]:
        """Get the base interaction layer color (read-only).
        
        The base color is white in dark theme and black in light theme.
        This ensures that the interaction layer is visible against the
        surface. The returned list contains RGB values only.
        """
        color = [0.0, 0.0, 0.0]
        if self.theme_manager.is_dark_mode:
            color = [1 - c for c in color]
        return color
    
    def _update_interaction_layer(self, *args) -> None:
        """Update the state layer position and size."""
        self._interaction_instruction.pos = self.pos
        self._interaction_instruction.size = self.size
        self._interaction_instruction.radius = self.radius
        self._interaction_color_instruction.rgba = self.interaction_color
        self.dispatch('on_interaction_updated')

    def _on_state_change(self, instance: Any, value: bool) -> None:
        """Handle changes to the specified state.
        
        This method is called whenever one of the widget's interactive
        states changes (e.g., hovered, pressed, focus, etc.). It
        updates the interaction layer color based on the new state and
        its precedence.
        """
        if not self.interaction_enabled:
            return None

        if value:
            self.apply_interaction(
                self.current_state,
                getattr(self, f'{self.current_state}_state_opacity', 0))
        else:
            self.interaction_color = self.theme_manager.transparent_color
    
    def apply_interaction(self, state: str, opacity: float) -> None:
        """Apply the interaction layer color for the specified state
        with the given opacity.

        This method sets the interaction layer color based on the 
        widget's current theme (light or dark) and the specified 
        opacity. It is called when a state becomes active to visually
        indicate that state.

        Parameters
        ----------
        state : Literal[
                'disabled', 'pressed', 'selected', 'focus', 'hovered', 'active']
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
        self.apply_interaction('hovered', 0.08)
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
            If the specified state is not in :attr:`available_states`.
        """
        assert state in self.available_states, (
            f'State {state!r} is not supported. Supported states are: '
            f'{self.available_states}')

        self.interaction_color = [*self._interaction_color[:3], opacity]
    
    def refresh_interaction(self) -> None:
        """Reapply the current state layer based on the widget's state.

        This method is useful when the theme changes or when the
        widget's state properties are modified externally. It ensures
        that the state layer reflects the current state and theme.
        """
        enabled = self.interaction_enabled
        self.interaction_enabled = True
        self._on_state_change(self, getattr(self, self.current_state, False))
            
        color = self.theme_manager.transparent_color
        self._interaction_color_instruction.rgba = color
        self.interaction_enabled = enabled

    def on_interaction_updated(self, *args) -> None:
        """Event dispatched when the state layer is updated.

        This can be overridden by subclasses to perform additional
        actions when the state layer changes."""
        pass


class MorphContentLayerBehavior(BaseLayerBehavior):
    """A behavior class that provides content layer capabilities.

    This behavior adds content color properties to widgets, allowing
    them to style their content (e.g., text, icons) based on
    different states. It automatically manages the content color
    based on the widget's state (e.g., disabled).

    Notes
    -----
    The kivy Label widget uses the generic `color` property for text
    rendering. This can lead to ambiguity in theme configurations where
    the intention is to specify a content color. The `content_color`
    property provides a clear, dedicated binding target for content
    colors in theme configurations. The label widget does also support
    a `outline_color` and `disabled_outline_color` property, which can 
    be used for text outlines/shadows, but this is less commonly used.
    """
    
    content_color: List[float] | None = ColorProperty(None)
    """Explicit content color property for theme binding disambiguation.

    This property provides a clear, dedicated binding target for content
    colors in theme configurations. Since Kivy uses the generic
    'color' property for text rendering, this explicit `content_color`
    property allows theme bindings to unambiguously specify content
    color intentions in :attr:`theme_color_bindings`.

    :attr:`content_color` is a :class:`~kivy.properties.ColorProperty`
    and defaults to None.
    """

    disabled_content_color: List[float] | None = ColorProperty(None)
    """Content color to use when the widget is disabled.

    This property allows you to specify a different content color for
    the widget when it is in the disabled state. If not set, the default
    content color will be used.

    :attr:`disabled_content_color` is a 
    :class:`~kivy.properties.ColorProperty` and defaults to None.
    """

    hovered_content_color: List[float] | None = ColorProperty(None)
    """Content color to use when the widget is hovered.

    This property allows you to specify a different content color for
    the widget when it is in the hovered state. If not set, the default
    content color will be used.

    :attr:`hovered_content_color` is a :class:`~kivy.properties.ColorProperty`
    and defaults to None.
    """

    def __init__(self, **kwargs) -> None:
        self.register_event_type('on_content_updated')
        super().__init__(**kwargs)
        if self.content_color is None:
            if hasattr(self, 'color'):
                self.content_color = self.color
            elif hasattr(self, 'foreground_color'):
                self.content_color = self.foreground_color
            else:
                self.content_color = self.theme_manager.text_color

        self.bind(
            content_color=self._update_content_layer,
            disabled_content_color=self._update_content_layer,
            current_state=self._update_content_layer,)
        
        self.refresh_content()
    
    def _update_content_layer(self, *args) -> None:
        """Update the content layer based on the current properties.
        
        This method is called whenever relevant properties change,
        such as `content_color` or `disabled`. It applies the
        appropriate content color based on the current state.
        """
        if hasattr(self, 'disabled_color'):
            self.disabled_color = (
                self.disabled_content_color or self.disabled_color)
        if hasattr(self, 'disabled_foreground_color'):
            self.disabled_foreground_color = (
                self.disabled_content_color or self.disabled_foreground_color)
        
        if self.current_state == 'disabled':
            self.dispatch('on_content_updated')
            return None

        color = None
        if self.current_state == 'hovered':
            color = self.hovered_content_color or self.content_color
        elif self.current_state == 'normal':
            color = self.content_color or self.theme_manager.text_color

        if color is not None:
            self.apply_content(color)
    
    def apply_content(self, color: List[float]) -> None:
        """Apply the specified content color to the widget.

        This method sets the widget's content color, which is typically
        used for text or icon colors. It can be called to update the
        content color based on theme changes or other conditions.

        Parameters
        ----------
        color : list of float
            The RGBA color to apply to the content, with values between
            0 and 1. Example: `[1, 0, 0, 1]` for solid red.
        """
        if hasattr(self, 'color'):
            self.color = color
        if hasattr(self, 'foreground_color'):
            self.foreground_color = color
        self.dispatch('on_content_updated')
    
    def refresh_content(self) -> None:
        """Reapply the current content color based on the widget's state.

        This method is useful when the theme changes or when the
        widget's state properties are modified externally. It ensures
        that the content color reflects the current state and theme.
        """
        self._update_content_layer()
    
    def on_content_updated(self, *args) -> None:
        """Event dispatched when the content layer is updated.

        This can be overridden by subclasses to perform additional
        actions when the content layer changes."""
        pass


class MorphOverlayLayerBehavior(BaseLayerBehavior):
    """A behavior class that provides an overlay layer capability.

    This behavior adds an overlay color on top of widgets, allowing them
    to display a semi-transparent overlay. It automatically manages the
    canvas graphics instructions to render the overlay.

    Examples
    --------
    ```pythonpython
    from morphui.app import MorphApp
    from morphui.uix.label import MorphLabel
    from morphui.uix.behaviors import MorphOverlayLayerBehavior

    class TestWidget(MorphOverlayLayerBehavior, MorphLabel):
        pass
    
    class MyApp(MorphApp):
        def build(self) -> TestWidget:
            return TestWidget()
    MyApp().run()
    ```

    Notes
    -----
    - The overlay color can be customized to achieve different visual
      effects.
    - The overlay is implemented as a semi-transparent rectangle that
      covers the entire widget area.
    - Ensure this behavior is added after any surface behaviors to
      ensure the overlay appears above the surface.
    """

    overlay_color: ColorProperty = ColorProperty([0, 0, 0, 0])
    """Color of the overlay.

    The color should be provided as a list of RGBA values between 0 and
    1. Example: `[0, 0, 0, 0.1]` for a semi-transparent black overlay.

    :attr:`overlay_color` is a 
    :class:`~kivy.properties.ColorProperty` and defaults to 
    `[0, 0, 0, 0]`."""

    _overlay_color_instruction: Color
    """Kivy Color instruction for the overlay color."""

    _overlay_instruction: Rectangle
    """Kivy Rectangle instruction for the overlay shape."""

    def __init__(self, **kwargs) -> None:
        self.register_event_type('on_overlay_updated')
        super().__init__(**kwargs)

        group = INSTRUCTION_GROUP.OVERLAY
        with self.canvas.after:
            self._overlay_color_instruction = Color(
                rgba=self.overlay_color,
                group=group)
            self._overlay_instruction = RoundedRectangle(
                pos=self.pos,
                size=self.size,
                radius=self.radius,
                group=group)
        
        self.bind(
            pos=self._update_overlay_layer,
            size=self._update_overlay_layer,
            radius=self._update_overlay_layer,
            overlay_color=self._update_overlay_layer,)

    def _update_overlay_layer(self, *args) -> None:
        """Update the overlay position and size."""
        self._overlay_instruction.pos = self.pos
        self._overlay_instruction.size = self.size
        self._overlay_instruction.radius = self.radius
        self._overlay_color_instruction.rgba = self.overlay_color
        self.dispatch('on_overlay_updated')
    
    def apply_overlay(self, color: List[float]) -> None:
        """Apply the specified overlay color to the widget.

        This method sets the widget's overlay color, which is typically
        used for visual effects. It can be called to update the overlay
        color based on theme changes or other conditions.

        Parameters
        ----------
        color : list of float
            The RGBA color to apply to the overlay, with values between
            0 and 1. Example: `[1, 0, 0, 0.5]` for semi-transparent red.
        """
        self.overlay_color = color
    
    def refresh_overlay(self) -> None:
        """Reapply the current overlay color.

        This method is useful when the theme changes or when the
        widget's properties are modified externally. It ensures that
        the overlay color reflects the current state and theme.
        """
        self._update_overlay_layer()
    
    def on_overlay_updated(self, *args) -> None:
        """Event dispatched when the overlay is updated.

        This can be overridden by subclasses to perform additional
        actions when the overlay changes."""
        pass


# Convenience Mixin Classes for Common Layer Combinations

class MorphInteractiveLayerBehavior(
        MorphInteractionLayerBehavior,
        MorphSurfaceLayerBehavior):
    """Convenience mixin combining surface and interaction layers.
    
    This behavior combines surface styling with interaction state 
    management, making it ideal for interactive widgets like buttons, 
    cards, and other clickable elements that need both visual styling 
    and hover/press feedback.
    
    Provides:
    - Surface color, border, and radius styling
    - Interaction state layers (hover, press, focus)
    - Automatic theme-aware state colors
    
    Examples
    --------
    ```python
    from morphui.uix.behaviors import MorphInteractiveLayerBehavior
    from morphui.uix.behaviors import MorphHoverBehavior
    from kivy.uix.label import Label
    
    class InteractiveCard(
        MorphHoverBehavior,
        MorphInteractiveLayerBehavior, 
        Label
    ):
        pass
    ```
    
    Notes
    -----
    - Ensure hover/press behaviors are included for full functionality
    - The interaction layer automatically appears above the surface
    - State colors adapt to the current theme (light/dark)
    """
    pass


class MorphTextLayerBehavior(
        MorphContentLayerBehavior,
        MorphSurfaceLayerBehavior):
    """Convenience mixin combining surface and content layers.
    
    This behavior combines surface styling with content color management,
    making it ideal for text-based widgets like labels, buttons with text,
    and other widgets that need both background styling and text color 
    theming.
    
    Provides:
    - Surface color, border, and radius styling  
    - Content/text color management
    - Disabled state color handling
    - Theme-aware color bindings
    
    Examples
    --------
    ```python
    from morphui.uix.behaviors import MorphTextLayerBehavior
    from kivy.uix.label import Label
    
    class ThemedLabel(MorphTextLayerBehavior, Label):
        pass
    ```
    
    Notes
    -----
    - Content colors automatically adapt to theme changes
    - Disabled state colors are handled automatically
    - Works with any widget that has a 'color' property
    """
    pass


class MorphCompleteLayerBehavior(
        MorphOverlayLayerBehavior,
        MorphContentLayerBehavior,
        MorphInteractionLayerBehavior,
        MorphSurfaceLayerBehavior):
    """Convenience mixin providing all layer behaviors.
    
    This behavior combines all available layer behaviors, providing
    complete styling and interaction capabilities. It's ideal for
    complex interactive widgets that need full theming support.
    
    Provides:
    - Surface color, border, and radius styling
    - Interaction state layers (hover, press, focus)
    - Content/text color management  
    - Overlay layer capability
    - Complete theme integration
    - Disabled state handling
    
    Layer Stack (bottom to top):
    1. Surface Layer - Background, borders
    2. Interaction Layer - State feedback  
    3. Content Layer - Text/icon colors
    4. Overlay Layer - Top-level overlays
    
    Examples
    --------
    ```python
    from morphui.uix.behaviors import MorphCompleteLayerBehavior
    from morphui.uix.behaviors import MorphHoverBehavior
    from kivy.uix.button import Button
    
    class FullFeaturedButton(
        MorphHoverBehavior,
        MorphCompleteLayerBehavior,
        Button
    ):
        pass
    ```
    
    Notes
    -----
    - This is equivalent to using MorphWidget as a base
    - Include appropriate interaction behaviors for full functionality
    - All layers are properly stacked and themed
    - Consider using more specific mixins if not all layers are needed
    """
    pass
