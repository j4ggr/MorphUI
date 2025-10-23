from math import pi
from math import sin
from math import cos

from typing import Any
from typing import List
from typing import Dict
from typing import Tuple
from typing import Literal
from typing import Generator

from kivy.metrics import dp
from kivy.graphics import Line
from kivy.graphics import Color
from kivy.graphics import Mesh
from kivy.graphics import SmoothLine
from kivy.graphics import SmoothRoundedRectangle
from kivy.properties import ListProperty
from kivy.properties import ColorProperty
from kivy.properties import NumericProperty
from kivy.properties import BooleanProperty
from kivy.properties import AliasProperty
from kivy.properties import VariableListProperty
from kivy.properties import BoundedNumericProperty
from kivy.uix.relativelayout import RelativeLayout
from kivy.graphics.tesselator import Tesselator

from ..._typing import InteractionState
from ...constants import NAME

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

    clamped_radius: List[float] = AliasProperty(
        lambda self: self._clamp_radius(),
        bind=['size', 'radius'],
        cache=True)
    """Get the clamped radius values (read-only).

    This property returns the radius values adjusted to ensure that
    they do not exceed the widget's dimensions. It is automatically
    updated when the widget's size or radius changes. This property is
    applied internally when rendering rounded rectangles to ensure 
    correct display.

    :attr:`clamped_radius` is a :class:`~kivy.properties.AliasProperty`
    """

    rounded_rectangle_params: List[float] = AliasProperty(
        lambda self: [
            0 if isinstance(self, RelativeLayout) else self.x,
            0 if isinstance(self, RelativeLayout) else self.y,
            self.width,
            self.height,
            *self.clamped_radius], # type: ignore
        bind=['size', 'pos', 'clamped_radius'],
        cache=True)
    """Get the parameters for creating a rounded rectangle (read-only).

    The parameters are returned as a list suitable for use in
    :class:`~kivy.graphics.instructions.SmoothLine` instruction. If the
    widget is a `RelativeLayout`, the position is set to (0, 0) to
    ensure correct rendering within the layout's coordinate system.
    
    Returns
    -------
    list of float
        List containing [x, y, width, height, *radius] for the rounded
        rectangle.
    """

    contour: List[float] = AliasProperty(
        lambda self: self._generate_contour(),
        bind=['size', 'pos', 'clamped_radius'],
        cache=True)
    """Get the contour points for the rounded rectangle (read-only).

    This property returns a flat list of x, y coordinates representing
    the contour of the rounded rectangle. It is automatically updated
    when the widget's size, position, or clamped radius changes.

    :attr:`contour` is a :class:`~kivy.properties.AliasProperty`
    """

    mesh: Tuple[List[float], List[float]] = AliasProperty(
        lambda self: self._generate_mesh(),
        bind=['contour'],
        cache=True)

    def _generate_corner_arc_points(
            self,
            corner: Literal['top-left', 'top-right', 'bottom-left', 'bottom-right'],
            radius: float
            ) -> List[float]:
        """Generate points for a quarter circle arc at the specified 
        corner.
        
        Will return a single point if the radius is less than 1. There
        will be `int(radius) + 1` points if the radius is greater than
        1. The generated points will start at the corner and proceed
        counter-clockwise around the quarter circle.

        Parameters
        ----------
        corner : Literal['top-left', 'top-right', 'bottom-left', 'bottom-right']
            The corner for which to generate the quarter circle points.
        radius : float
            The radius of the quarter circle.

        Returns
        -------
        List[float]
            A flat list of x, y coordinates representing the quarter
            circle points.

        Raises
        ------
        ValueError
            If an invalid corner is specified.
        """
        match corner:
            case 'top-left':
                alpha = 0.5 * pi
                x_center = self.x + radius
                y_center = self.y + self.height - radius
            case 'bottom-left':
                alpha = pi
                x_center = self.x + radius
                y_center = self.y + radius
            case 'bottom-right':
                alpha = 1.5 * pi
                x_center = self.x + self.width - radius
                y_center = self.y + radius
            case 'top-right':
                alpha = 0
                x_center = self.x + self.width - radius
                y_center = self.y + self.height - radius
            case _:
                raise ValueError("Invalid corner specified.")
            
        if radius <= 1:
            return [x_center, y_center]

        n_max = 45 # Limit maximum segments for performance (1 for each degree)
        n_segments = min(int(radius) + 1, n_max)
        def _points(n: int) -> Generator[float, None, None]:
            for i in range(n + 1):  # Include end point for continuity
                # Use normalized angle progression for consistent curvature
                t = i / n  # Normalized parameter from 0 to 1
                angle = 0.5 * pi * t + alpha
                x = x_center + radius * cos(angle)
                y = y_center + radius * sin(angle)
                yield x
                yield y
        return list(_points(n_segments))
    
    def _clamp_radius(self, *args) -> List[float]:
        """Ensure the radius values do not exceed the widget's size.

        This method adjusts the radius values to ensure that the sum of 
        the vertical radius does not exceed the widget's height,
        and the sum of the horizontal radius does not exceed the 
        widget's width.
        
        The radius values are scaled down proportionally if they exceed
        the widget's dimensions.
        """
        if self.width <= 0 or self.height <= 0:
            return [0., 0., 0., 0.]

        v_radius = [r for r in self.radius]
        h_radius = [r for r in self.radius]

        # Check and fix vertical constraints (height)
        left_sum = self.radius[0] + self.radius[3]  # top-left + bottom-left
        if left_sum > self.height:
            scale_factor = self.height / left_sum
            v_radius[0] *= scale_factor
            v_radius[3] *= scale_factor

        right_sum = self.radius[1] + self.radius[2]  # top-right + bottom-right
        if right_sum > self.height:
            scale_factor = self.height / right_sum
            v_radius[1] *= scale_factor
            v_radius[2] *= scale_factor

        # Check and fix horizontal constraints (width)
        top_sum = self.radius[0] + self.radius[1]  # top-left + top-right
        if top_sum > self.width:
            scale_factor = self.width / top_sum
            h_radius[0] *= scale_factor
            h_radius[1] *= scale_factor

        bottom_sum = self.radius[2] + self.radius[3]  # bottom-right + bottom-left
        if bottom_sum > self.width:
            scale_factor = self.width / bottom_sum
            h_radius[2] *= scale_factor
            h_radius[3] *= scale_factor

        # Use the most restrictive constraint for each corner
        return [
            min(v_radius[0], h_radius[0]),
            min(v_radius[1], h_radius[1]),
            min(v_radius[2], h_radius[2]),
            min(v_radius[3], h_radius[3]),]
    
    def _generate_contour(self) -> List[float]:
        """Generate the complete contour points including corners and 
        edges.

        This method generates a list of points that define the contour
        of the rounded rectangle.

        Returns
        -------
        List[float]
            A flat list of x, y coordinates representing the contour
            path.
        """
        radius = self.clamped_radius
        points = [
            self.x + radius[0], self.y + self.height,
            *self._generate_corner_arc_points('top-left', radius[0]),
            self.x, self.y + radius[3],
            *self._generate_corner_arc_points('bottom-left', radius[3]),
            self.x + self.width - radius[2], self.y,
            *self._generate_corner_arc_points('bottom-right', radius[2]),
            self.x + self.width, self.y + self.height - radius[1],
            *self._generate_corner_arc_points('top-right', radius[1]),]

        return points

    def _generate_mesh(self) -> Tuple[List[float], List[int]]:
        """Generate the vertices and indices for the rounded rectangle
        using tessellation.

        This method uses Kivy's Tesselator to create a set of vertices
        and indices that define the filled area of the rounded rectangle.

        Returns
        -------
        Tuple[List[float], List[int]]
            A tuple containing:
            - A flat list of x, y coordinates representing the vertices
              of the rounded rectangle.
            - A list of indices defining the triangles for rendering.
        """
        vertices: List[float] = []
        indices: List[int] = []
        tesselator = Tesselator()
        tesselator.add_contour(self.contour)
        tesselator.tesselate()
        if tesselator.meshes:
            vertices, indices = tesselator.meshes[0]
        return vertices, indices


class MorphSurfaceLayerBehavior(BaseLayerBehavior):
    """A behavior class that provides surface and border styling 
    capabilities. Also known as the "surface" layer".

    This behavior adds surface color, border color, border width, and 
    corner radius properties to widgets. It automatically manages the 
    canvas graphics instructions to render a rounded rectangle 
    surface with optional border.
    """

    surface_color: ColorProperty = ColorProperty()
    """Surface color of the widget.
    
    The color should be provided as a list of RGBA values between 0 and 
    1. Example: `[1, 0, 0, 1]` for solid red.
    
    :attr:`surface_color` is a :class:`~kivy.properties.ColorProperty`
    and defaults to `[1, 1, 1, 1]` (white)."""

    disabled_surface_color: List[float] | None = ColorProperty([0, 0, 0, 0])
    """Surface color when the widget is disabled.

    This color is applied when the widget is in a disabled state.
    It should be a fully transparent color if you are using state layer.
    Otherwise, it can be set to any RGBA color.

    :attr:`disabled_surface_color` is a
    :class:`~kivy.properties.ColorProperty` and defaults to
    `[0, 0, 0, 0]` (fully transparent)."""

    error_surface_color: List[float] | None = ColorProperty(None)
    """Surface color when the widget is in an error state.

    This color is applied when the widget is in an error state.

    :attr:`error_surface_color` is a
    :class:`~kivy.properties.ColorProperty` and defaults to
    `None`."""

    focus_surface_color: List[float] | None = ColorProperty(None)
    """Surface color when the widget is focused.

    :attr:`focus_surface_color` is a
    :class:`~kivy.properties.ColorProperty` and defaults to
    `None`."""

    active_surface_color: List[float] | None = ColorProperty(None)
    """Surface color when the widget is active.

    :attr:`active_surface_color` is a
    :class:`~kivy.properties.ColorProperty` and defaults to
    `None`."""

    selected_surface_color: List[float] | None = ColorProperty(None)
    """Surface color when the widget is selected.

    This color is applied when the widget is in a selected state.

    :attr:`selected_surface_color` is a
    :class:`~kivy.properties.ColorProperty` and defaults to
    `None`."""

    border_color: List[float] = ColorProperty([0, 0, 0, 0])
    """Border color of the widget.
    
    The color should be provided as a list of RGBA values between 0 and 
    1. Example: `[0, 1, 0, 1]` for solid green.

    :attr:`border_color` is a :class:`~kivy.properties.ColorProperty`
    and defaults to `[0, 0, 0, 0]` (fully transparent)."""

    disabled_border_color: List[float] | None = ColorProperty(None)
    """Border color when the widget is disabled.

    This color is applied when the widget is in a disabled state.

    :attr:`disabled_border_color` is a
    :class:`~kivy.properties.ColorProperty` and defaults to
    `None`."""

    error_border_color: List[float] | None = ColorProperty(None)
    """Border color when the widget is in an error state.

    :attr:`error_border_color` is a
    :class:`~kivy.properties.ColorProperty` and defaults to
    `None`."""

    focus_border_color: List[float] | None = ColorProperty(None)
    """Border color when the widget is focused.

    :attr:`focus_border_color` is a
    :class:`~kivy.properties.ColorProperty` and defaults to
    `None`."""

    active_border_color: List[float] | None = ColorProperty(None)
    """Border color when the widget is active.

    :attr:`active_border_color` is a
    :class:`~kivy.properties.ColorProperty` and defaults to
    `None`."""

    selected_border_color: List[float] | None = ColorProperty(None)
    """Border color when the widget is selected.

    This color is applied when the widget is in a selected state.

    :attr:`selected_border_color` is a
    :class:`~kivy.properties.ColorProperty` and defaults to
    `None`."""

    border_width: float = NumericProperty(1, min=0.01)
    """Width of the border.

    The width is specified in pixels.
    
    :attr:`border_width` is a :class:`~kivy.properties.NumericProperty`
    and defaults to `1` (1 pixel wide).
    """

    border_open_length: float = NumericProperty(0, min=0)
    """Length of the open section of the border at the top edge.

    This property allows you to create an open border effect by
    specifying a length in pixels for the open section. A value of 0
    means a closed border.

    :attr:`border_open_length` is a
    :class:`~kivy.properties.NumericProperty` and defaults to `0`.
    """

    border_bottom_line_only: bool = BooleanProperty(False)
    """Whether to show only a bottom line instead of the full border.

    When True, only the bottom edge of the widget is drawn as a line.
    When False, the full border outline is drawn as usual.

    :attr:`border_bottom_line_only` is a
    :class:`~kivy.properties.BooleanProperty` and defaults to `False`.
    """
    
    border_path = AliasProperty(
        lambda self: self._generate_border_path(),
        bind=['contour', 'border_bottom_line_only', 'border_open_length', 'border_closed'],
        cache=True)
    """Get the border path points (read-only).

    This property returns a flat list of x, y coordinates representing
    the border path of the rounded rectangle. It is automatically
    updated when any relevant property changes.

    :attr:`border_path` is a :class:`~kivy.properties.AliasProperty`
    """

    border_closed = AliasProperty(
        lambda self: (
            not self.border_bottom_line_only 
            and self.border_open_length < dp(1)),
        bind=['border_bottom_line_only', 'border_open_length'])
    """Whether the border is closed (read-only).

    This property returns True if the border is closed (i.e., 
    `border_open_length` is 0), and False otherwise. When
    `border_bottom_line_only` is True, this always returns False since
    a single line would be drawn twice.
    """

    _surface_color_instruction: Color
    """Kivy Color instruction for the surface color."""

    _surface_instruction: Mesh
    """Kivy Mesh instruction for the surface shape."""

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

        with self.canvas.before:

            self._surface_color_instruction = Color(
                rgba=self.surface_color,
                group=NAME.SURFACE)
            self._surface_instruction = Mesh(
                vertices=self.mesh[0],
                indices=self.mesh[1],
                mode='triangle_fan',
                group=NAME.SURFACE)
            
            self._border_color_instruction = Color(
                rgba=self.border_color,
                group=NAME.SURFACE_BORDER)
            self._border_instruction = SmoothLine(
                width=dp(self.border_width),
                points=self.border_path,
                close=self.border_closed,
                group=NAME.SURFACE_BORDER)
            
        self.bind(
            contour=self._update_surface_layer,
            border_color=self._update_surface_layer,
            border_width=self._update_surface_layer,
            border_closed=self._update_surface_layer,
            surface_color=self._update_surface_layer,
            current_surface_state=self._update_surface_layer,)
        self.refresh_surface()

    def _generate_border_path(self) -> List[float]:
        """Calculate the complete border path points including corners
        and edges.

        This method generates a list of points that define the border
        path of the rounded rectangle.

        Returns
        -------
        List[float]
            A flat list of x, y coordinates representing the border 
            path.
        """
        # If only bottom line is requested, return just the bottom line points
        if self.border_bottom_line_only:
            return [self.x, self.y, self.x + self.width, self.y]
        
        path: List[float] = self._generate_contour()

        if self.border_open_length > 0:
            path.extend([
                min(path[0] + self.border_open_length, path[-2]),
                path[-1]])

        return path
    
    def get_resolved_surface_colors(
            self) -> Tuple[List[float], List[float]]:
        """Determine the appropriate surface and border colors based
        on the current state.

        This method checks the widget's current surface state and
        returns the corresponding surface and border colors. If a
        specific color for the state is not set, it falls back to the
        default colors.

        Override this method in subclasses to customize color
        resolution logic.

        Returns
        -------
        Tuple[List[float], List[float]]
            A tuple containing the resolved surface color and border
            color as lists of RGBA values.
        """
        state = self.current_surface_state
        surface_color = getattr(self, f'{state}_surface_color', None)
        border_color = getattr(self, f'{state}_border_color', None)

        if surface_color is None:
            surface_color = self.surface_color
        if border_color is None:
            border_color = self.border_color

        return surface_color, border_color
        
    def _update_surface_layer(self, *args) -> None:
        """Update the surface when any relevant property changes."""
        surface_color, border_color = self.get_resolved_surface_colors()

        self._surface_color_instruction.rgba = surface_color
        self._surface_instruction.vertices = self.mesh[0]
        self._surface_instruction.indices = self.mesh[1]
        
        self._border_color_instruction.rgba = border_color
        self._border_instruction.width = dp(self.border_width)
        self._border_instruction.points = self._generate_border_path()
        self._border_instruction.close = self.border_closed

        self.dispatch('on_surface_updated')
    
    def refresh_surface(self) -> None:
        """Reapply the current surface and border colors based on the
        widget's state.

        This method is useful when the theme changes or when the
        widget's state properties are modified externally. It ensures
        that the surface and border colors reflect the current state
        and theme.
        """
        self._update_surface_layer()

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

    focus_state_opacity: float = NumericProperty(0.05)
    """Opacity of the state layer when the widget is focus.

    The opacity is specified as a float between 0 and 1. A value of 0
    means no state layer, while a value of 1 means a fully opaque state.

    :attr:`focus_state_opacity` is a
    :class:`~kivy.properties.NumericProperty` and defaults to `0.05`."""

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

    interaction_gray_value: float = BoundedNumericProperty(0.0, min=0, max=1)
    """Base color value for the interaction layer.
    
    This value determines the base color (black or white) used for the
    interaction layer. In dark theme, this value is inverted to ensure
    visibility against the surface. The opacity of the layer is
    determined by the specific state (hovered, pressed, focus, etc.).
    
    :attr:`interaction_gray_value` is a 
    :class:`~kivy.properties.BoundedNumericProperty` and defaults to
    `0.0` (black).
    """

    _interaction_color_instruction: Color
    """Kivy Color instruction for the state layer color."""

    _interaction_instruction: SmoothRoundedRectangle
    """Kivy SmoothRoundedRectangle instruction for the state layer shape."""

    def __init__(self, **kwargs) -> None:
        self.register_event_type('on_interaction_updated')
        super().__init__(**kwargs)

        group = NAME.INTERACTION
        with self.canvas.before:
            self._interaction_color_instruction = Color(
                rgba=self.theme_manager.transparent_color,
                group=group)
            self._interaction_instruction = SmoothRoundedRectangle(
                pos=self.pos,
                size=self.size,
                radius=self.clamped_radius,
                group=group)
        
        self.bind(
            pos=self._update_interaction_layer,
            size=self._update_interaction_layer,
            radius=self._update_interaction_layer,
            current_interaction_state=self._on_interaction_state_change,)

        self.refresh_interaction()

    def get_resolved_interaction_color(self) -> List[float]:
        """Get the interaction layer color.
        
        The base color is white in dark theme and black in light theme.
        This ensures that the interaction layer is visible against the
        surface. The returned list contains RGB values only.
        """
        opacity = getattr(
            self, f'{self.current_interaction_state}_state_opacity', None)
    
        if opacity is None:
            return self.theme_manager.transparent_color
        
        value = self.interaction_gray_value
        if self.theme_manager.is_dark_mode:
            value = 1 - value
        return [value, value, value, opacity]

    def _update_interaction_layer(self, *args) -> None:
        """Update the state layer position and size."""
        interaction_color = self.get_resolved_interaction_color()
        self._interaction_color_instruction.rgba = interaction_color

        self._interaction_instruction.pos = self.pos
        self._interaction_instruction.size = self.size
        self._interaction_instruction.radius = self.clamped_radius
        self.dispatch('on_interaction_updated')

    def _on_interaction_state_change(self, instance: Any, value: bool) -> None:
        """Handle changes to the specified state.
        
        This method is called whenever one of the widget's interactive
        states changes (e.g., hovered, pressed, focus, etc.). It
        updates the interaction layer color based on the new state and
        its precedence.
        """
        if not self.interaction_enabled:
            return None

        self.apply_interaction(self.current_interaction_state)

    def apply_interaction(self, state: InteractionState) -> None:
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
        self.current_interaction_state = state
        self._update_interaction_layer()
    
    def refresh_interaction(self) -> None:
        """Reapply the current state layer based on the widget's state.

        This method is useful when the theme changes or when the
        widget's state properties are modified externally. It ensures
        that the state layer reflects the current state and theme.
        """
        enabled = self.interaction_enabled
        self.interaction_enabled = True
        self._on_interaction_state_change(
            self, getattr(self, self.current_interaction_state, False))
            
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

    error_content_color: List[float] | None = ColorProperty(None)
    """Content color to use when the widget is in an error state.

    This property allows you to specify a different content color for
    the widget when it is in an error state. If not set, the default
    content color will be used.

    :attr:`error_content_color` is a
    :class:`~kivy.properties.ColorProperty` and defaults to None.
    """

    focus_content_color: List[float] | None = ColorProperty(None)
    """Content color to use when the widget is focused.

    This property allows you to specify a different content color for
    the widget when it is in the focused state. If not set, the default
    content color will be used.

    :attr:`focus_content_color` is a
    :class:`~kivy.properties.ColorProperty` and defaults to None."""

    hovered_content_color: List[float] | None = ColorProperty(None)
    """Content color to use when the widget is hovered.

    This property allows you to specify a different content color for
    the widget when it is in the hovered state. If not set, the default
    content color will be used.

    :attr:`hovered_content_color` is a :class:`~kivy.properties.ColorProperty`
    and defaults to None.
    """

    active_content_color: List[float] | None = ColorProperty(None)
    """Content color to use when the widget is active.

    This property allows you to specify a different content color for
    the widget when it is in the active state. If not set, the default
    content color will be used.

    :attr:`active_content_color` is a :class:`~kivy.properties.ColorProperty`
    and defaults to None.
    """

    selected_content_color: List[float] | None = ColorProperty(None)
    """Content color to use when the widget is selected.

    This property allows you to specify a different content color for
    the widget when it is in the selected state. If not set, the default
    content color will be used.

    :attr:`selected_content_color` is a :class:`~kivy.properties.ColorProperty`
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
        
        if hasattr(self, 'disabled_color'):
            self.disabled_color = (
                self.disabled_content_color or self.disabled_color)
        if hasattr(self, 'disabled_foreground_color'):
            self.disabled_foreground_color = (
                self.disabled_content_color or self.disabled_foreground_color)

        self.bind(
            content_color=self._update_content_layer,
            disabled_content_color=self._update_content_layer,
            current_content_state=self._update_content_layer,)
        
        self.refresh_content()

    def get_resolved_content_color(self) -> List[float] | None:
        """Determine the appropriate content color based on the current
        state.

        This method checks the widget's current content state and
        returns the corresponding content color. If a specific color
        for the state is not set, it falls back to the default
        `content_color`.

        Override this method in subclasses to customize color
        resolution logic.

        Returns
        -------
        List[float] | None
            The resolved content color as a list of RGBA values.
        """
        state = self.current_content_state
        content_color = getattr(self, f'{state}_content_color', None)
        
        if content_color is None:
            content_color = self.content_color

        return content_color
    
    def _update_content_layer(self, *args) -> None:
        """Update the content layer based on the current properties.
        
        This method is called whenever relevant properties change,
        such as `content_color` or `disabled`. It applies the
        appropriate content color based on the current state.
        """
        if self.current_content_state == 'disabled':
            self.dispatch('on_content_updated')
            return None

        color = self.get_resolved_content_color()
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
        if hasattr(self, '_text_color_instruction'):
            self._text_color_instruction.rgba = color # see: MorphTextInput
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

    disabled_overlay_color: ColorProperty = ColorProperty([0, 0, 0, 0])
    """Color of the overlay when the widget is disabled.

    This color is applied when the widget is in a disabled state.

    :attr:`disabled_overlay_color` is a
    :class:`~kivy.properties.ColorProperty` and defaults to 
    `[0, 0, 0, 0]`.
    """

    resizing_overlay_color: ColorProperty = ColorProperty([0, 0, 0, 0])
    """Color of the overlay during resizing.

    The color should be provided as a list of RGBA values between 0 and
    1. Example: `[0, 0, 0, 0.1]` for a semi-transparent black overlay.

    :attr:`resizing_overlay_color` is a
    :class:`~kivy.properties.ColorProperty` and defaults to
    `[0, 0, 0, 0]`.
    """

    overlay_edge_color: ColorProperty = ColorProperty([0, 0, 0, 0])
    """Edge color of the overlay.

    The edge color should be provided as a list of RGBA values between 
    0 and 1. Example: `[0, 0, 0, 0.1]` for a semi-transparent black edge.
    The edges can be used to show a resize border when hovering.

    :attr:`overlay_edge_color` is a
    :class:`~kivy.properties.ColorProperty` and defaults to
    `[0, 0, 0, 0]`."""

    disabled_overlay_edge_color: ColorProperty = ColorProperty([0, 0, 0, 0])
    """Edge color of the overlay when the widget is disabled.

    This color is applied when the widget is in a disabled state.

    :attr:`disabled_overlay_edge_color` is a
    :class:`~kivy.properties.ColorProperty` and defaults to
    `[0, 0, 0, 0]`.
    """

    resizing_overlay_edge_color: ColorProperty = ColorProperty([0, 0, 0, 0])
    """Edge color of the overlay during resizing.

    The edge color should be provided as a list of RGBA values between
    0 and 1. Example: `[0, 0, 0, 0.1]` for a semi-transparent black edge.
    The edges can be used to show a resize border when hovering.

    :attr:`resizing_overlay_edge_color` is a
    :class:`~kivy.properties.ColorProperty` and defaults to
    `[0, 0, 0, 0]`.
    """

    overlay_edge_width: float = NumericProperty(2)
    """Width of the overlay edge.

    :attr:`overlay_edge_width` is a
    :class:`~kivy.properties.NumericProperty` and defaults to 3.
    """

    overlay_edge_inside: bool = BooleanProperty(True)
    """Whether the overlay edges are drawn inside the widget bounds.

    If True, the edges are drawn inside the widget bounds. If False,
    the edges are drawn centered on the widget bounds.

    :attr:`overlay_edges_inside` is a
    :class:`~kivy.properties.BooleanProperty` and defaults to True.
    """

    visible_edges : List[str] = ListProperty([])
    """List of edges to show for the overlay.

    The edges can be 'top', 'right', 'bottom', 'left'. If empty, no
    edges are shown. Example: `['top', 'bottom']` to show only the top
    and bottom edges.

    :attr:`visible_edges ` is a
    :class:`~kivy.properties.ListProperty` and defaults to an 
    empty list.
    """

    _overlay_color_instruction: Color
    """Kivy Color instruction for the overlay color."""

    _overlay_instruction: SmoothRoundedRectangle
    """Kivy SmoothRoundedRectangle instruction for the overlay shape."""

    _overlay_edges_color_instructions: Dict[str, Line]
    """Kivy Color instructions for the overlay edges.
    
    The edges are drawn in the order: top, right, bottom, left."""

    _overlay_edges_instruction: Dict[str, Line]
    """Kivy Line instructions for the overlay edges.
    
    The edges are drawn in the order: top, right, bottom, left."""

    def __init__(self, **kwargs) -> None:
        self.register_event_type('on_overlay_updated')
        super().__init__(**kwargs)

        self._overlay_edges_color_instructions = {}
        self._overlay_edges_instruction = {}

        with self.canvas.after:
            self._overlay_color_instruction = Color(
                rgba=self.overlay_color,
                group=NAME.OVERLAY)
            self._overlay_instruction = SmoothRoundedRectangle(
                pos=self.pos,
                size=self.size,
                radius=self.clamped_radius,
                group=NAME.OVERLAY)
            for name, points in self._overlay_edges_params.items():
                self._overlay_edges_color_instructions[name] = Color(
                    rgba=self.theme_manager.transparent_color,
                    group=NAME.OVERLAY_EDGES)
                self._overlay_edges_instruction[name] = Line(
                    points=points,
                    width=dp(self.overlay_edge_width),
                    cap='none',
                    group=NAME.OVERLAY_EDGES)

        self.bind(
            pos=self._update_overlay_layer,
            size=self._update_overlay_layer,
            radius=self._update_overlay_layer,
            overlay_color=self._update_overlay_layer,
            overlay_edge_color=self._update_overlay_layer,
            overlay_edge_width=self._update_overlay_layer,
            visible_edges=self._update_overlay_layer,)

        self.refresh_overlay()
        
    @property
    def _overlay_edges_params(self) -> Dict[str, List[float]]:
        """Get the parameters for creating overlay edge lines
        (read-only).

        The parameters are returned as a list of lists, each inner list
        containing the points for one edge line. The edges are defined
        in the order: top, right, bottom, left.
        
        Returns
        -------
        dict of str to list of float
            List containing four lists, each with [x1, y1, x2, y2]
            coordinates for the edge lines.
        """
        is_relative = isinstance(self, RelativeLayout)
        left = (0 if is_relative else self.x)
        bottom = (0 if is_relative else self.y)
        right = left + self.width
        top = bottom + self.height
        offset = dp(self.overlay_edge_width) if self.overlay_edge_inside else 0

        edges = {
            'top': [left, top-offset, right, top-offset],
            'right': [right-offset, top, right-offset, bottom],
            'bottom': [right, bottom+offset, left, bottom+offset],
            'left': [left+offset, bottom, left+offset, top],}
        return edges

    def _update_overlay_layer(self, *args) -> None:
        """Update the overlay position and size."""
        if self.current_overlay_state == 'disabled':
            color = self.disabled_overlay_color
            edge_color = self.disabled_overlay_edge_color
        elif self.current_overlay_state == 'resizing':
            color = self.resizing_overlay_color
            edge_color = self.resizing_overlay_edge_color
        else:
            color = self.overlay_color
            edge_color = self.overlay_edge_color

        self._overlay_instruction.pos = self.pos
        self._overlay_instruction.size = self.size
        self._overlay_instruction.radius = self.clamped_radius
        self._overlay_color_instruction.rgba = color

        for name, line in self._overlay_edges_instruction.items():
            line.points = self._overlay_edges_params[name]
            line.width = dp(self.overlay_edge_width)
            if name in self.visible_edges:
                self._overlay_edges_color_instructions[name].rgba = edge_color
            else:
                self._overlay_edges_color_instructions[name].rgba = (
                    self.theme_manager.transparent_color)
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
