from math import pi
from math import sin
from math import cos

from typing import List
from typing import Dict
from typing import Tuple
from typing import Literal
from typing import Generator

from kivy.event import EventDispatcher
from kivy.metrics import dp
from kivy.graphics import Line
from kivy.graphics import Color
from kivy.graphics import Mesh
from kivy.graphics import Rectangle
from kivy.graphics import SmoothLine
from kivy.graphics import SmoothRoundedRectangle
from kivy.properties import ListProperty
from kivy.properties import ColorProperty
from kivy.properties import NumericProperty
from kivy.properties import BooleanProperty
from kivy.properties import AliasProperty
from kivy.properties import VariableListProperty
from kivy.properties import BoundedNumericProperty
from kivy.graphics.tesselator import Tesselator

from morphui._typing import InteractionState
from morphui.constants import NAME
from morphui.utils.helpers import get_effective_pos
from morphui.utils.helpers import get_edges_params

from .appreference import MorphAppReferenceBehavior
from .states import MorphStateBehavior


__all__ = [
    'MorphHighlightLayerBehavior',
    'MorphSurfaceLayerBehavior',
    'MorphInteractionLayerBehavior',
    'MorphContentLayerBehavior',
    'MorphInteractiveLayerBehavior',
    'MorphTextLayerBehavior',
    'MorphCompleteLayerBehavior',]


class BaseLayerBehavior(
        MorphStateBehavior,
        MorphAppReferenceBehavior):
    """Base class for layer behaviors providing core geometric functionality.
    
    This class provides common geometric calculations and mesh generation
    for all layer behaviors without any automatic binding setup. Each
    layer behavior subclass is responsible for setting up its own
    property bindings and event handlers.
    
    Provides:
    - Radius and corner calculations
    - Contour generation for rounded rectangles
    - Mesh generation for filled shapes
    - Parameter calculation helpers
    """

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
            *get_effective_pos(self),
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
    """Get the mesh vertices and indices for the rounded rectangle
    (read-only).
    
    This property returns a tuple containing the vertices and indices
    needed to render the rounded rectangle as a filled shape. It is
    automatically updated when the contour changes.

    :attr:`mesh` is a :class:`~kivy.properties.AliasProperty`
    """

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

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


class MorphHighlightLayerBehavior(EventDispatcher):
    """A behavior class that provides highlight styling capabilities.

    This behavior adds highlight color properties to widgets. It
    automatically manages the canvas graphics instructions to render a
    highlight effect based on the widget's state.
    """
    
    highlight: bool = BooleanProperty(False)
    """Whether to show the highlight effect.

    This property controls whether the highlight effect is rendered on
    the widget. When True, the highlight color is applied.

    :attr:`highlight` is a :class:`~kivy.properties.BooleanProperty` and
    defaults to `False`."""

    normal_highlight_color: List[float] = ColorProperty([0, 0, 0, 0])
    """Current highlight color of the widget.

    This property reflects the active highlight color, which may change
    based on interaction states.

    :attr:`highlight_color` is a :class:`~kivy.properties.ColorProperty`
    and defaults to `[0, 0, 0, 0]` (fully transparent)."""

    highlight_opacity: float | None = BoundedNumericProperty(
        None, min=0, max=1, errorvalue=0.08, allownone=True)
    """Opacity of the highlight color.

    This property controls the transparency level of the highlight
    color, ranging from 0 (fully transparent) to 1 (fully opaque). If
    set to None, the :attr:`highlight_color` alpha value is used as is.

    :attr:`highlight_opacity` is a
    :class:`~kivy.properties.BoundedNumericProperty` and defaults to
    `None`."""

    def _get_highlight_color(self) -> List[float]:
        """Get the highlight color based on the current state.

        This method determines the appropriate highlight color based on
        the widget's current state (normal). If a specific color for
        the state is not set, it falls back to the normal highlight
        color. This method is used by the :attr:`highlight_color`
        AliasProperty.

        Returns
        -------
        List[float]
            The resolved highlight color as a list of RGBA values.
        """
        if not self.highlight:
            return [0, 0, 0, 0]
        
        highlight_color = self.normal_highlight_color
            
        if self.highlight_opacity is not None:
            highlight_color = highlight_color[:3] + [self.highlight_opacity]
        
        return highlight_color
    
    def _set_highlight_color(self, *args) -> None:
        """Set the highlight color based on the current state.

        This method updates the highlight color instruction to reflect
        the appropriate highlight color based on the widget's current
        state.
        """
        self._highlight_color_instruction.rgba = self._get_highlight_color()

    highlight_color: List[float] = AliasProperty(
        _get_highlight_color,
        _set_highlight_color,
        bind=[
            'normal_highlight_color',
            'highlight_opacity',
            'highlight'])

    def _get_highlight_layer_pos(self) -> Tuple[float, float]:
        """Get the position for the highlight layer.

        This method accounts for whether the widget is a
        `RelativeLayout` to ensure the highlight is positioned correctly
        within the layout's coordinate system.

        Returns
        -------
        Tuple[float, float]
            The (x, y) position for the highlight layer.
        """
        return get_effective_pos(self)

    def _set_highlight_layer_pos(self, *args) -> None:
        """Set the position for the highlight layer.

        This method updates the highlight rectangle position to reflect
        the correct position based on whether the widget is a
        `RelativeLayout`.
        """
        self._highlight_instruction.pos = self._get_highlight_layer_pos()

    highlight_layer_pos: Tuple[float, float] = AliasProperty(
        _get_highlight_layer_pos,
        _set_highlight_layer_pos,
        bind=['pos'])

    def _get_highlight_layer_size(self) -> Tuple[float, float]:
        """Get the size for the highlight layer.

        This method accounts for whether the widget is a
        `RelativeLayout` to ensure the highlight is sized correctly
        within the layout's coordinate system.

        Returns
        -------
        Tuple[float, float]
            The (width, height) size for the highlight layer.
        """
        return self.size

    def _set_highlight_layer_size(self, *args) -> None:
        """Set the size for the highlight layer.

        This method updates the highlight rectangle size to reflect
        the correct size based on whether the widget is a
        `RelativeLayout`.
        """
        self._highlight_instruction.size = self._get_highlight_layer_size()

    highlight_layer_size: Tuple[float, float] = AliasProperty(
        _get_highlight_layer_size,
        _set_highlight_layer_size,
        bind=['size'])

    _highlight_color_instruction: Color
    """Internal canvas color instruction for the highlight effect."""

    _highlight_instruction: Rectangle
    """Internal canvas rectangle instruction for the highlight effect."""

    def __init__(self, **kwargs) -> None:
        self.register_event_type('on_highlight_updated')
        super().__init__(**kwargs)

        with self.canvas.before:
            self._highlight_color_instruction = Color(
                rgba=self.highlight_color,
                group=NAME.HIGHLIGHT)
            self._highlight_instruction = Rectangle(
                pos=self.pos,
                size=self.size,)
        
        self.bind(
            highlight=self._set_highlight_color,
            highlight_layer_pos=self._update_highlight,
            highlight_layer_size=self._update_highlight,
            highlight_color=self._update_highlight)
        self.refresh_highlight()
            
    def _resolve_highlight_pos(self) -> Tuple[float, float]:
        """Get the correct position for the highlight rectangle.

        This method accounts for whether the widget is a
        `RelativeLayout` to ensure the highlight is positioned correctly
        within the layout's coordinate system.

        Returns
        -------
        Tuple[float, float]
            The (x, y) position for the highlight rectangle.
        """
        return get_effective_pos(self)
            
    def _update_highlight(self, *args) -> None:
        """Update the highlight rectangle position and size.
        
        This method is called whenever the widget's position or size
        changes."""
        self.highlight_layer_pos = self.highlight_layer_pos
        self.highlight_layer_size = self.highlight_layer_size
        self.highlight_color = self.highlight_color
        self.dispatch('on_highlight_updated')

    def refresh_highlight(self, *args) -> None:
        """Refresh the highlight color.

        This method is useful when external changes affect the highlight
        color and a manual refresh is needed.
        """
        self._update_highlight()

    def on_highlight_updated(self, *args) -> None:
        """Event dispatched when the highlight is updated.

        This event can be used to perform additional actions whenever
        the highlight effect is refreshed.
        """
        pass


class MorphSurfaceLayerBehavior(BaseLayerBehavior):
    """A behavior class that provides surface and border styling 
    capabilities. Also known as the "surface" layer".

    This behavior adds surface color, border color, border width, and 
    corner radius properties to widgets. It automatically manages the 
    canvas graphics instructions to render a rounded rectangle 
    surface with optional border.
    """

    normal_surface_color: List[float] = ColorProperty([0, 0, 0, 0])
    """Surface color of the widget when it is in its normal state.
    
    The color should be provided as a list of RGBA values between 0 and 
    1. Example: `[1, 0, 0, 1]` for solid red.
    
    :attr:`normal_surface_color` is a :class:`~kivy.properties.ColorProperty`
    and defaults to `[0, 0, 0, 0]` (fully transparent)."""

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

    def _get_surface_color(self, *args) -> List[float]:
        """Get the surface color based on the current state.

        This method determines the appropriate surface color based on
        the widget's current state (normal, disabled, error, focus,
        active). If a specific color for the state is not set, it falls
        back to the normal surface color. This method is used by the
        :attr:`surface_color` AliasProperty.

        Returns
        -------
        List[float]
            The resolved surface color as a list of RGBA values.
        """
        return (
            getattr(self, f'{self.current_surface_state}_surface_color', None)
            or self.normal_surface_color
            or self.theme_manager.transparent_color)
    
    def _set_surface_color(self, *args) -> None:
        """Set the surface color based on the current state.

        This method updates the surface color instruction to reflect the
        appropriate surface color based on the widget's current state.
        """
        self._surface_color_instruction.rgba = self._get_surface_color()

    surface_color: List[float] = AliasProperty(
        _get_surface_color,
        _set_surface_color,
        bind=[
            'normal_surface_color',
            'disabled_surface_color',
            'error_surface_color',
            'focus_surface_color',
            'active_surface_color',
            'current_surface_state'])
    """Get the current surface color based on the current state or
    trigger updates.

    This property automatically resolves the appropriate surface color
    based on the widget's current state (normal, disabled, error,
    focus, active). Setting this property updates the surface color
    accordingly. Passing different values will have no effect since it 
    is always synced to the widget's state. However, it can be useful to
    trigger updates.

    :attr:`surface_color` is a :class:`~kivy.properties.AliasProperty`
    and defaults to the resolved surface color based on the current
    state."""

    normal_border_color: List[float] = ColorProperty([0, 0, 0, 0])
    """Border color of the widget when in the normal state.
    
    The color should be provided as a list of RGBA values between 0 and 
    1. Example: `[0, 1, 0, 1]` for solid green.

    :attr:`normal_border_color` is a :class:`~kivy.properties.ColorProperty`
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

    def _get_border_color(self, *args) -> List[float]:
        """Get the border color based on the current state.

        This method determines the appropriate border color based on
        the widget's current state (normal, disabled, error, focus,
        active). If a specific color for the state is not set, it falls
        back to the normal border color. This method is used by the
        :attr:`border_color` AliasProperty.

        Returns
        -------
        List[float]
            The resolved border color as a list of RGBA values.
        """
        return (
            getattr(self, f'{self.current_surface_state}_border_color', None)
            or self.normal_border_color
            or self.theme_manager.transparent_color)
    
    def _set_border_color(self, *args) -> None:
        """Set the border color based on the current state.

        This method updates the border color instruction to reflect the
        appropriate border color based on the widget's current state.
        """
        self._border_color_instruction.rgba = self._get_border_color()

    border_color: List[float] = AliasProperty(
        _get_border_color,
        _set_border_color,
        bind=[
            'normal_border_color',
            'disabled_border_color',
            'error_border_color',
            'focus_border_color',
            'active_border_color',
            'current_surface_state'])
    """Get the current border color based on the current state or
    trigger updates.

    This property automatically resolves the appropriate border color
    based on the widget's current state (normal, disabled, error,
    focus, active). Setting this property updates the border color
    accordingly. Passing different values will have no effect since it 
    is always synced to the widget's state. However, it can be useful to
    trigger updates.

    :attr:`border_color` is a :class:`~kivy.properties.AliasProperty`
    and defaults to the resolved border color based on the current
    state."""

    border_width: float = BoundedNumericProperty(dp(0.5), min=0.01, errorvalue=1)
    """Width of the border.

    The width is specified in pixels.
    
    :attr:`border_width` is a 
    :class:`~kivy.properties.BoundedNumericProperty` and defaults to 
    `0.5` (0.5 pixels wide).
    """

    border_open_x: float | None = NumericProperty(None, allownone=True)
    """X position of the open section of the border.

    This property allows you to create an open border effect by
    specifying the X position in pixels for the open section.

    :attr:`border_open_x` is a :class:`~kivy.properties.NumericProperty`
    and defaults to `None`.
    """

    border_open_length: float = BoundedNumericProperty(0, min=0, errorvalue=0)
    """Length of the open section of the border at the top edge.

    This property allows you to create an open border effect by
    specifying a length in pixels for the open section. A value of 0
    means a closed border.

    :attr:`border_open_length` is a
    :class:`~kivy.properties.BoundedNumericProperty` and defaults to `0`.
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
        cache=True,
        bind=[
            'contour',
            'border_bottom_line_only',
            'border_open_x',
            'border_open_length',
            'border_closed'],)
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
        bind=[
            'border_bottom_line_only',
            'border_open_length'])
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
            current_surface_state=self._update_surface_layer,
            contour=self._update_surface_layer,
            border_width=self._update_surface_layer,
            border_path=self._update_surface_layer,
            surface_color=self.on_surface_updated,
            border_color=self.on_surface_updated,)
        
        for state in self.surface_state_precedence:
            self.fbind(
                f'{state}_surface_color',
                self.setter('surface_color'),)
            self.fbind(
                f'{state}_border_color',
                self.setter('border_color'),)

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

        if self.border_open_x is not None:
            path = [self.border_open_x, path[1], *path]

        if self.border_open_length > 0:
            path.extend([
                min(path[0] + self.border_open_length, path[-2]),
                path[-1]])

        return path
        
    def _update_surface_layer(self, *args) -> None:
        """Update the surface when any relevant property changes."""
        self._surface_instruction.vertices = self.mesh[0]
        self._surface_instruction.indices = self.mesh[1]
        self.surface_color = self._get_surface_color()
        
        self._border_instruction.width = self.border_width
        self._border_instruction.points = self._generate_border_path()
        self._border_instruction.close = self.border_closed
        self.border_color = self._get_border_color()

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

    pressed_state_opacity: float = NumericProperty(0.16)
    """Opacity of the state layer when the widget is pressed.

    The opacity is specified as a float between 0 and 1. A value of 0
    means no state layer, while a value of 1 means a fully opaque state.

    :attr:`pressed_state_opacity` is a
    :class:`~kivy.properties.NumericProperty` and defaults to `0.12`."""

    focus_state_opacity: float = NumericProperty(0.05)
    """Opacity of the state layer when the widget is focus.

    The opacity is specified as a float between 0 and 1. A value of 0
    means no state layer, while a value of 1 means a fully opaque state.

    :attr:`focus_state_opacity` is a
    :class:`~kivy.properties.NumericProperty` and defaults to `0.05`."""

    disabled_state_opacity: float = NumericProperty(0.0)
    """Opacity of the state layer when the widget is disabled.

    The opacity is specified as a float between 0 and 1. A value of 0
    means no state layer, while a value of 1 means a fully opaque state.

    :attr:`disabled_state_opacity` is a
    :class:`~kivy.properties.NumericProperty` and defaults to `0.0`."""

    interaction_enabled: bool = BooleanProperty(True)
    """Whether to enable the interaction layer (state-layer) to be 
    displayed.

    :attr:`interaction_enabled` is a 
    :class:`~kivy.properties.BooleanProperty` and defaults to `True`."""

    interaction_gray_value: float | None = BoundedNumericProperty(
        None, min=0, max=1, allownone=True)
    """Base color value for the interaction layer.
    
    This value determines the base grayscale color used for the
    interaction layer. When set to None (default), the color is
    automatically determined based on the theme: white (1.0) for dark
    theme and black (0.0) for light theme to ensure visibility against
    the surface. When set to a specific value (0-1), that value is used
    regardless of theme. The opacity of the layer is determined by the
    specific state (hovered, pressed, focus, etc.).
    
    :attr:`interaction_gray_value` is a 
    :class:`~kivy.properties.BoundedNumericProperty` and defaults to
    `None` (theme-based automatic selection).
    """

    interaction_expansion: List[float] = VariableListProperty(
        [dp(0)], length=4)
    """Expansion values for the interaction layer.
    
    When positive, these values make the interaction layer bigger than
    the widget size. The values represent expansion in pixels for each
    edge in the order: left, bottom, right, top.
    
    :attr:`interaction_expansion` is a 
    :class:`~kivy.properties.VariableListProperty` and defaults to
    `[0, 0, 0, 0]`."""

    def _get_interaction_pos(self, *args) -> Tuple[float, float]:
        """Get the position of the interaction layer.
        
        The (x, y) position of the interaction layer is calculated
        by accounting for any expansion. This method is used internally
        by the :attr:`interaction_pos` property."""
        x, y = get_effective_pos(self)
        pos = (
            x - self.interaction_expansion[0],
            y - self.interaction_expansion[1],)
        return pos
    
    def _set_interaction_pos(self, *args) -> None:
        """Set the position of the interaction layer.
        
        The (x, y) position of the interaction layer is calculated
        by accounting for any expansion. This method is used internally
        by the :attr:`interaction_pos` property."""
        self._interaction_instruction.pos = self._get_interaction_pos()
        
    interaction_pos: Tuple[float, float] = AliasProperty(
        _get_interaction_pos,
        _set_interaction_pos,
        bind=['pos', 'interaction_expansion'],
        cache=True)
    """Get the current position of the interaction layer or trigger
    updates.

    The (x, y) position of the interaction layer is calculated
    by accounting for any expansion. Setting this property updates the 
    position of the interaction layer accordingly. Passing different
    values will have no effect since it is always synced to the widget's
    position and expansion. However, it can be useful to trigger updates.
    
    :attr:`interaction_pos` is a
    :class:`~kivy.properties.AliasProperty` and is bound to the
    `pos` and `interaction_expansion` properties.
    """

    def _get_interaction_size(self, *args) -> Tuple[float, float]:
        """Get the size of the interaction layer.
        
        The (width, height) size of the interaction layer is calculated
        by accounting for any expansion. This method is used internally
        by the :attr:`interaction_size` property."""
        expansion = self.interaction_expansion
        size = (
            self.width + (expansion[0] + expansion[2]),
            self.height + (expansion[1] + expansion[3]),)
        return size
    
    def _set_interaction_size(self, *args) -> None:
        """Set the size of the interaction layer.
        
        The (width, height) size of the interaction layer is calculated
        by accounting for any expansion. This method is used internally
        by the :attr:`interaction_size` property."""
        if not self.interaction_enabled:
            return
        
        self._interaction_instruction.size = self._get_interaction_size()

    interaction_size: Tuple[float, float] = AliasProperty(
        _get_interaction_size,
        _set_interaction_size,
        bind=['size', 'interaction_expansion'],
        cache=True)
    """Get the current size of the interaction layer or trigger updates.

    The (width, height) size of the interaction layer is calculated
    by accounting for any expansion. Setting this property updates the 
    size of the interaction layer accordingly. Passing different values
    will have no effect since it is always synced to the widget's size
    and expansion. However, it can be useful to trigger updates.
    
    :attr:`interaction_size` is a
    :class:`~kivy.properties.AliasProperty` and is bound to the
    `size` and `interaction_expansion` properties.
    """

    def _get_interaction_radius(self, *args) -> List[float]:
        """Get the radius of the interaction layer.
        
        The radius values of the interaction layer are the same as the
        widget's clamped radius. This method is used internally by the
        :attr:`interaction_radius` property."""
        return self.clamped_radius
    
    def _set_interaction_radius(self, *args) -> None:
        """Set the radius of the interaction layer.
        
        The radius values of the interaction layer are the same as the
        widget's clamped radius. This method is used internally by the
        :attr:`interaction_radius` property."""
        if not self.interaction_enabled:
            return
        
        self._interaction_instruction.radius = self.clamped_radius

    interaction_radius: List[float] = AliasProperty(
        _get_interaction_radius,
        _set_interaction_radius,
        bind=['radius'],
        cache=True)
    """Get the current radius of the interaction layer or trigger 
    updates.

    The radius values of the interaction layer are the same as the
    widget's clamped radius. Setting this property updates the radius
    of the interaction layer accordingly. Passing different values
    will have no effect since it is always synced to the widget's
    clamped radius. However, it can be useful to trigger updates.
    
    :attr:`interaction_radius` is a
    :class:`~kivy.properties.AliasProperty` and is bound to the
    `radius` property.
    """

    def _get_interaction_color(self, *args) -> List[float]:
        """Get the interaction layer color.
        
        Returns the interaction layer color as RGBA values. The base 
        color is determined by the interaction_gray_value property: if 
        None, it automatically uses white (1.0) in dark theme and black
        (0.0) in light theme to ensure visibility against the surface.
        If a specific value is set, that value is used regardless of 
        theme. The opacity is determined by the current interaction
        state's opacity setting.

        It is used internally by the :attr:`interaction_color`
        property.
        
        Returns
        -------
        List[float]
            RGBA color values [r, g, b, a] where r=g=b is the gray value
            and a is the state-specific opacity.
        """
        state = self.current_interaction_state
        opacity = getattr(self, f'{state}_state_opacity', None)

        if opacity is None:
            return self.theme_manager.transparent_color

        if self.interaction_gray_value is None:
            value = 1.0 if self.theme_manager.is_dark_mode else 0.0
        else:
            value = self.interaction_gray_value
            
        return [value, value, value, opacity]

    def _set_interaction_color(self, *args) -> None:
        """Set the interaction layer color.
        
        This method updates the interaction layer color instruction
        based on the resolved interaction layer color. It is used
        internally by the :attr:`interaction_color` property.
        """
        if not self.interaction_enabled:
            return
        
        state = self.current_interaction_state
        if state != 'pressed' or not getattr(self, 'ripple_enabled', False):
            interaction_color = self._get_interaction_color()
            self._interaction_color_instruction.rgba = interaction_color

    interaction_color: List[float] = AliasProperty(
        _get_interaction_color,
        _set_interaction_color,
        bind=[
            'current_interaction_state',
            'hovered_state_opacity',
            'pressed_state_opacity',
            'focus_state_opacity',
            'disabled_state_opacity',
            'interaction_gray_value',
            'interaction_enabled'])
    """Get the interaction layer color or trigger updates.

    The interaction layer color is determined by the current theme
    (light or dark) and the specific state opacity. Setting this
    property updates the interaction layer color accordingly.
    
    :attr:`interaction_color` is a
    :class:`~kivy.properties.AliasProperty`.
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
            pos=self.setter('interaction_pos'),
            size=self.setter('interaction_size'),
            radius=self.setter('interaction_radius'),
            current_interaction_state=self.setter('interaction_color'),
            hovered_state_opacity=self.setter('interaction_color'),
            pressed_state_opacity=self.setter('interaction_color'),
            focus_state_opacity=self.setter('interaction_color'),
            disabled_state_opacity=self.setter('interaction_color'),
            interaction_gray_value=self.setter('interaction_color'),
            interaction_enabled=self._update_interaction_layer,
            interaction_expansion=self._update_interaction_layer,
            interaction_pos=self.on_interaction_updated,
            interaction_size=self.on_interaction_updated,
            interaction_radius=self.on_interaction_updated,)

        self.refresh_interaction()
    
    def collide_point(self, x: float, y: float) -> bool:
        """Check if a point collides with the interaction layer.

        This method overrides the default collide_point to account
        for any expansion of the interaction layer.

        Parameters
        ----------
        x : float
            The x coordinate of the point to check.
        y : float
            The y coordinate of the point to check.

        Returns
        -------
        bool
            True if the point collides with the interaction layer,
            False otherwise.
        """
        layer_x, layer_y = self.interaction_pos
        layer_width, layer_height = self.interaction_size
        return (
            layer_x <= x <= layer_x + layer_width and
            layer_y <= y <= layer_y + layer_height)

    def _update_interaction_layer(self, *args) -> None:
        """Update the state layer position, size, radius and color.
        
        This method updates the interaction layer's position, size,
        radius, and color based on the current properties. It is called
        whenever any relevant property changes."""
        self.interaction_pos = self.pos
        self.interaction_size = self.size
        self.interaction_radius = self.radius
        self.interaction_color = [0, 0, 0, 0]  # Trigger update

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
                'disabled', 'pressed', 'focus', 'hovered', 'active']
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
        self._update_interaction_layer()
            
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
    
    normal_content_color: List[float] | None = ColorProperty(None)
    """Explicit content color property for theme binding disambiguation.

    This property provides a clear, dedicated binding target for content
    colors in theme configurations. Since Kivy uses the generic
    'color' property for text rendering, this explicit `content_color`
    property allows theme bindings to unambiguously specify content
    color intentions in :attr:`theme_color_bindings`.

    :attr:`normal_content_color` is a 
    :class:`~kivy.properties.ColorProperty` and defaults to None.
    """

    _disabled_content_color: List[float] | None = ColorProperty(None, allownone=True)
    """Internal property to store the disabled content color. 

    This property is used to manage the disabled content color
    separately from the normal content color. It is not intended to be
    set directly by users, but is used internally to resolve the
    disabled content color based on the widget's state and other related
    properties.
    """

    def _get_disabled_content_color(self, *args) -> List[float] | None:
        """Get the disabled content color.

        This method determines the appropriate content color to use when
        the widget is in a disabled state. If `disabled_content_color` is
        set, it returns that color. Otherwise, it falls back to the normal
        content color or other relevant properties as defined in the
        :attr:`content_color` resolution logic.

        Returns
        -------
        List[float] | None
            The resolved disabled content color as a list of RGBA values,
            or None if no specific color is set.
        """
        return (
            self._disabled_content_color
            or getattr(self, 'disabled_color', None)
            or getattr(self, 'disabled_foreground_color', None))

    def _set_disabled_content_color(self, color: List[float] | None) -> None:
        """Set the disabled content color.

        This method updates the internal `_disabled_content_color` 
        property as well as any related properties that may be used for
        disabled content color resolution. This ensures that the 
        disabled content color is properly managed and can be resolved 
        correctly when the widget is in a disabled state.

        Parameters
        ----------
        color : List[float] | None
            The RGBA color values to set as the disabled content color, or
            None to clear it.
        """
        self._disabled_content_color = color
        if color is None:
            return
        if hasattr(self, 'disabled_color'):
            self.disabled_color = color
        if hasattr(self, 'disabled_foreground_color'):
            self.disabled_foreground_color = color

    disabled_content_color: List[float] | None = AliasProperty(
        _get_disabled_content_color,
        _set_disabled_content_color,
        bind=('_disabled_content_color',))
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

    def _get_content_color(self, *args) -> List[float] | None:
        """Get the content color based on the current state.

        This method determines the appropriate content color based on
        the widget's current content state (normal, disabled, error, 
        focus, hovered, active). If a specific color for the state is 
        not set, it falls back to the color of the text instruction 
        (if available) or the normal content color. If none of those are
        set, it falls back to the widget's `color` or `foreground_color` 
        property, or finally to the theme's `content_surface_color` as 
        a last resort. This method is used by the :attr:`content_color` 
        AliasProperty.

        Returns
        -------
        List[float] | None
            The resolved content color as a list of RGBA values.
        """

        color = (
            getattr(self, f'{self.current_content_state}_content_color', None)
            or self.normal_content_color)

        if color is None:
            if hasattr(self, 'color'):
                color = self.color
            elif hasattr(self, 'foreground_color'):
                color = self.foreground_color
            elif getattr(self, 'disabled', False):
                color = self.theme_manager.outline_variant_color
            else:
                color = self.theme_manager.content_surface_color
        return color
    
    def _set_content_color(self, *args) -> None:
        """Set the content color based on the current state.

        This method updates the widget's content color to reflect the
        appropriate content color based on the widget's current state.
        """
        color = self._get_content_color()
        if color is not None:
            self.apply_content(color)

    content_color: List[float] | None = AliasProperty(
        _get_content_color,
        _set_content_color,
        bind=[
            'normal_content_color',
            'disabled_content_color',
            'error_content_color',
            'focus_content_color',
            'hovered_content_color',
            'active_content_color',
            'current_content_state'])
    """Get the current content color based on the current state or
    trigger updates.

    This property automatically resolves the appropriate content color
    based on the widget's current state (normal, disabled, error,
    focus, hovered, active). Setting this property updates the content 
    color accordingly. Passing different values will have no effect since it 
    is always synced to the widget's state. However, it can be useful to
    trigger updates.

    :attr:`content_color` is a :class:`~kivy.properties.AliasProperty`
    and defaults to the resolved content color based on the current
    state."""

    def __init__(self, **kwargs) -> None:
        self.register_event_type('on_content_updated')
        super().__init__(**kwargs)
        if self.normal_content_color is None:
            self.normal_content_color = self._get_content_color()
            
        self.bind(
            content_color=self._update_content_layer,)

        for state in self.content_state_precedence:
            self.fbind(
                f'{state}_content_color',
                self.setter('content_color'),)

        self.refresh_content()
    
    def _update_content_layer(self, *args) -> None:
        """Update the content layer based on the current properties.
        
        This method is called whenever relevant properties change,
        such as `content_color` or the current state. It applies the
        appropriate content color based on the current state.
        """
        self._set_content_color()
    
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
        self._set_disabled_content_color(self._get_disabled_content_color())
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

    normal_overlay_color: ColorProperty = ColorProperty([0, 0, 0, 0])
    """Color of the overlay.

    The color should be provided as a list of RGBA values between 0 and
    1. Example: `[0, 0, 0, 0.1]` for a semi-transparent black overlay.

    :attr:`normal_overlay_color` is a 
    :class:`~kivy.properties.ColorProperty` and defaults to 
    `[0, 0, 0, 0]`."""

    disabled_overlay_color: List[float] | None = ColorProperty(None)
    """Color of the overlay when the widget is disabled.

    This color is applied when the widget is in a disabled state.

    :attr:`disabled_overlay_color` is a
    :class:`~kivy.properties.ColorProperty` and defaults to 
    `None`.
    """

    resizing_overlay_color: List[float] | None = ColorProperty(None)
    """Color of the overlay during resizing.

    The color should be provided as a list of RGBA values between 0 and
    1. Example: `[0, 0, 0, 0.1]` for a semi-transparent black overlay.

    :attr:`resizing_overlay_color` is a
    :class:`~kivy.properties.ColorProperty` and defaults to
    `None`.
    """

    def _get_overlay_color(self, *args) -> List[float]:
        """Get the overlay color based on the current overlay state.

        This method returns the appropriate overlay color depending on
        the current overlay state of the widget. If a specific color for
        the state is not set, it falls back to the normal overlay
        color. It is used internally by the :attr:`overlay_color`
        property.
        """
        return (
            getattr(self, f'{self.current_overlay_state}_overlay_color', None)
            or self.normal_overlay_color
            or self.theme_manager.transparent_color)

    def _set_overlay_color(self, *args) -> None:
        """Set the overlay color based on the current overlay state.

        This method updates the overlay color instruction based on the
        resolved overlay color. It is used internally by the
        :attr:`overlay_color` property.
        """
        self._overlay_color_instruction.rgba = self._get_overlay_color()

    overlay_color: List[float] = AliasProperty(
        _get_overlay_color,
        _set_overlay_color,
        bind=[
            'normal_overlay_color',
            'disabled_overlay_color',
            'resizing_overlay_color',
            'current_overlay_state',],)
    """Get the overlay color or trigger updates.

    The overlay color is determined by the current overlay state.
    Passing different values will have no effect since it is always
    synced to the widget's state. However, it can be useful to trigger
    updates.

    :attr:`overlay_color` is a
    :class:`~kivy.properties.AliasProperty`.
    """

    normal_overlay_edge_color: ColorProperty = ColorProperty([0, 0, 0, 0])
    """Edge color of the overlay.

    The edge color should be provided as a list of RGBA values between 
    0 and 1. Example: `[0, 0, 0, 0.1]` for a semi-transparent black edge.
    The edges can be used to show a resize border when hovering.

    :attr:`normal_overlay_edge_color` is a
    :class:`~kivy.properties.ColorProperty` and defaults to
    `[0, 0, 0, 0]`."""

    disabled_overlay_edge_color: List[float] | None = ColorProperty(None)
    """Edge color of the overlay when the widget is disabled.

    This color is applied when the widget is in a disabled state.

    :attr:`disabled_overlay_edge_color` is a
    :class:`~kivy.properties.ColorProperty` and defaults to
    `None`.
    """

    resizing_overlay_edge_color: List[float] | None = ColorProperty(None)
    """Edge color of the overlay during resizing.

    The edge color should be provided as a list of RGBA values between
    0 and 1. Example: `[0, 0, 0, 0.1]` for a semi-transparent black edge.
    The edges can be used to show a resize border when hovering.

    :attr:`resizing_overlay_edge_color` is a
    :class:`~kivy.properties.ColorProperty` and defaults to
    `None`.
    """

    active_overlay_edge_color: List[float] | None = ColorProperty(None)
    """Edge color of the overlay when the widget is active.

    This color is applied when the widget is in an active state.

    :attr:`active_overlay_edge_color` is a
    :class:`~kivy.properties.ColorProperty` and defaults to
    `None`.
    """

    def _get_overlay_edge_color(self, *args) -> List[float]:
        """Get the overlay edge color based on the current overlay state.

        This method returns the appropriate overlay edge color depending
        on the current overlay state of the widget. If a specific color 
        for the state is not set, it falls back to the normal overlay 
        edge color. If that is also not set, it falls back to the 
        theme's transparent color. It is used internally by the 
        :attr:`overlay_edge_color` property.
        """
        return (
            getattr(self, f'{self.current_overlay_state}_overlay_edge_color', None)
            or self.normal_overlay_edge_color
            or self.theme_manager.transparent_color)

    def _set_overlay_edge_color(self, *args) -> None:
        """Set the overlay edge color based on the current overlay state.

        This method updates the overlay edge color instruction based
        on the resolved overlay edge color. It is used internally by
        the :attr:`overlay_edge_color` property.
        """
        color = self._get_overlay_edge_color()
        for name, instruction in self._overlay_edges_color_instructions.items():
            if name in self.visible_edges:
                instruction.rgba = color
            else:
                instruction.rgba = self.theme_manager.transparent_color
    
    overlay_edge_color: List[float] = AliasProperty(
        _get_overlay_edge_color,
        _set_overlay_edge_color,
        bind=[
            'normal_overlay_edge_color',
            'disabled_overlay_edge_color',
            'resizing_overlay_edge_color',
            'current_overlay_state',
            'visible_edges'],)
    """Get the overlay edge color or trigger updates.

    The overlay edge color is determined by the current overlay state.
    Passing different values will have no effect since it is always
    synced to the widget's state. However, it can be useful to trigger
    updates.

    :attr:`overlay_edge_color` is a
    :class:`~kivy.properties.AliasProperty`.
    """

    overlay_edge_width: float = NumericProperty(dp(1))
    """Width of the overlay edge.

    This width is applied when the widget is in a normal state.

    :attr:`overlay_edge_width` is a
    :class:`~kivy.properties.NumericProperty` and defaults to 1.
    """

    resizing_overlay_edge_width: float = NumericProperty(dp(3))
    """Width of the overlay edge during resizing.

    This width is applied when the widget is in a resizing state.

    :attr:`resizing_overlay_edge_width` is a
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

    def _get_overlay_layer_pos(self, *args) -> Tuple[float, float]:
        """Get the position of the overlay layer.
        
        The (x, y) position of the overlay layer. This method is used
        internally by the :attr:`overlay_layer_pos` property.
        """
        return get_effective_pos(self)
    
    def _set_overlay_layer_pos(self, *args) -> None:
        """Set the position of the overlay layer.
        
        This method updates the overlay position instruction. It is used
        internally by the :attr:`overlay_layer_pos` property.
        """
        if hasattr(self, '_overlay_instruction'):
            self._overlay_instruction.pos = self._get_overlay_layer_pos()

    overlay_layer_pos: Tuple[float, float] = AliasProperty(
        _get_overlay_layer_pos,
        _set_overlay_layer_pos,
        bind=['pos'],
        cache=True)
    """Get or set the position of the overlay layer or trigger update.

    The (x, y) position of the overlay layer. Passing different values
    will have no effect since it is always synced to the widget's
    position. However, it can be useful to trigger updates.
    
    :attr:`overlay_layer_pos` is a
    :class:`~kivy.properties.AliasProperty` and is bound to the
    `pos` property.
    """

    def _get_overlay_layer_size(self, *args) -> Tuple[float, float]:
        """Get the size of the overlay layer.
        
        The (width, height) size of the overlay layer. This method is used
        internally by the :attr:`overlay_layer_size` property.
        """
        return (self.width, self.height)
    
    def _set_overlay_layer_size(self, *args) -> None:
        """Set the size of the overlay layer.
        
        This method updates the overlay size instruction. It is used
        internally by the :attr:`overlay_layer_size` property.
        """
        if hasattr(self, '_overlay_instruction'):
            self._overlay_instruction.size = self._get_overlay_layer_size()

    overlay_layer_size: Tuple[float, float] = AliasProperty(
        _get_overlay_layer_size,
        _set_overlay_layer_size,
        bind=['size'],
        cache=True)
    """Get the size of the overlay layer.

    The (width, height) size of the overlay layer.
    
    :attr:`overlay_layer_size` is a
    :class:`~kivy.properties.AliasProperty` and is bound to the
    `size` property.
    """

    def _get_overlay_layer_radius(self, *args) -> List[float]:
        """Get the radius of the overlay layer.
        
        The radius values of the overlay layer are the same as the
        widget's clamped radius. This method is used internally by the
        :attr:`overlay_layer_radius` property.
        """
        return self.clamped_radius
    
    def _set_overlay_layer_radius(self, *args) -> None:
        """Set the radius of the overlay layer.
        
        This method updates the overlay radius instruction. It is used
        internally by the :attr:`overlay_layer_radius` property.
        """
        if hasattr(self, '_overlay_instruction'):
            self._overlay_instruction.radius = self.clamped_radius

    overlay_layer_radius: List[float] = AliasProperty(
        _get_overlay_layer_radius,
        _set_overlay_layer_radius,
        bind=['radius'],
        cache=True)
    """Get the radius of the overlay layer.

    The radius values of the overlay layer are the same as the
    widget's clamped radius.
    
    :attr:`overlay_layer_radius` is a
    :class:`~kivy.properties.AliasProperty` and is bound to the
    `radius` property.
    """

    def _get_overlay_edges_params(self, *args) -> Dict[str, List[float]]:
        """Get the parameters for creating overlay edge lines.

        The parameters are returned as a dictionary with edge names as keys
        and coordinate lists as values. This method is used internally by
        the :attr:`overlay_edges_params` property.
        
        Returns
        -------
        Dict[str, List[float]]
            Dictionary containing edge names mapped to [x1, y1, x2, y2]
            coordinates for the edge lines.
        """
        left, bottom = get_effective_pos(self)
        right = left + self.width
        top = bottom + self.height
        offset = self.overlay_edge_width if self.overlay_edge_inside else 0

        return get_edges_params(left, right, bottom, top, offset)
    
    def _set_overlay_edges_params(self, *args) -> None:
        """Update the overlay edge line parameters.
        
        This method updates the overlay edge line instructions based on the
        calculated edge parameters. It is used internally by the
        :attr:`overlay_edges_params` property.
        """
        if hasattr(self, '_overlay_edges_instruction'):
            edges = self._get_overlay_edges_params()
            for name, line in self._overlay_edges_instruction.items():
                line.points = edges[name]
                line.width = self.get_resolved_edge_width(name)

    overlay_edges_params: Dict[str, List[float]] = AliasProperty(
        _get_overlay_edges_params,
        _set_overlay_edges_params,
        bind=[
            'pos',
            'size', 
            'overlay_edge_width', 
            'resizing_overlay_edge_width',
            'overlay_edge_inside'],
        cache=True)
    """Get the parameters for creating overlay edge lines.

    The parameters are returned as a dictionary with edge names as keys
    and coordinate lists as values.
    
    :attr:`overlay_edges_params` is a
    :class:`~kivy.properties.AliasProperty`.
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
            for name, points in self.overlay_edges_params.items():
                self._overlay_edges_color_instructions[name] = Color(
                    rgba=self.theme_manager.transparent_color,
                    group=NAME.OVERLAY_EDGES)
                self._overlay_edges_instruction[name] = Line(
                    points=points,
                    width=self.overlay_edge_width,
                    cap='none',
                    group=NAME.OVERLAY_EDGES)

        self.bind(
            pos=self.setter('overlay_layer_pos'),
            size=self.setter('overlay_layer_size'),
            radius=self.setter('overlay_layer_radius'),
            overlay_edge_width=self.setter('overlay_edges_params'),
            resizing_overlay_edge_width=self.setter('overlay_edges_params'),
            overlay_edge_inside=self.setter('overlay_edges_params'),
            overlay_edges_params=self.setter('overlay_edges_params'),
            visible_edges=self.setter('overlay_edge_color'),
            current_overlay_state=self.setter('overlay_color'),
            normal_overlay_color=self.setter('overlay_color'),
            disabled_overlay_color=self.setter('overlay_color'),
            resizing_overlay_color=self.setter('overlay_color'),
            normal_overlay_edge_color=self.setter('overlay_edge_color'),
            disabled_overlay_edge_color=self.setter('overlay_edge_color'),
            resizing_overlay_edge_color=self.setter('overlay_edge_color'),
            overlay_layer_pos=self._update_overlay_layer,
            overlay_layer_size=self._update_overlay_layer,
            overlay_layer_radius=self._update_overlay_layer,
            overlay_edge_color=self._update_overlay_layer,
            overlay_color=self._update_overlay_layer,)

        self.refresh_overlay()
    
    def get_resolved_edge_width(self, edge: str | None) -> float:
        """Get the overlay edge width based on the current state.

        Parameters
        ----------
        edge : str | None
            The name of the edge for which to get the width. If `None`,
            the default overlay edge width is returned.

        Returns
        -------
        float
            The width of the overlay edge. If the current overlay state
            is 'resizing', the `resizing_overlay_edge_width` is returned;
            otherwise, the standard `overlay_edge_width` is returned.
        """
        current_state = self.current_overlay_state
        resizible_edges = getattr(self, 'resizible_edges', [])
        if current_state == 'resizing' and edge in resizible_edges:
            return self.resizing_overlay_edge_width
        return self.overlay_edge_width

    def _update_overlay_layer(self, *args) -> None:
        """Update the overlay layer position, size, radius, color and edges.
        
        This method updates all overlay layer properties based on the current
        state and properties. It is called whenever any relevant property changes.
        """
        self.overlay_layer_pos = self.pos
        self.overlay_layer_size = self.size
        self.overlay_layer_radius = self.radius
        self.overlay_color = [0, 0, 0, 0]  # Trigger update
        self.overlay_edge_color = [0, 0, 0, 0]  # Trigger update
        self.overlay_edges_params = {}  # Trigger update
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
        """Reapply the current overlay colors and properties.

        This method is useful when the theme changes or when the
        widget's properties are modified externally. It ensures that
        the overlay colors and properties reflect the current state and theme.
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
