import math
from typing import Any
from typing import Dict
from typing import List
from typing import Tuple
from kivy.metrics import dp
from kivy.graphics import Line
from kivy.graphics import Color
from kivy.uix.widget import Widget
from kivy.properties import AliasProperty
from kivy.properties import ColorProperty
from kivy.properties import NumericProperty
from kivy.properties import BooleanProperty
from kivy.properties import BoundedNumericProperty

from morphui.uix.behaviors import MorphColorThemeBehavior
from morphui.uix.behaviors import MorphIdentificationBehavior


class _MorphProgressBase(
        MorphIdentificationBehavior,
        MorphColorThemeBehavior,
        Widget):
    """Internal base class shared by linear and circular progress
    indicators.  Not intended for direct use.
    """
    _VALUE_EPSILON: float = 0.001
    """Threshold for treating value as 0 or 1 to avoid rendering issues
    with floating point precision.
    """

    value: float = BoundedNumericProperty(0.0, min=0.0, max=1.0)
    """Progress value between 0 and 1, where 0 means no progress and 
    1 means complete.

    Ignored while :attr:`indeterminate` is True.

    :attr:`value` is a :class:`~kivy.properties.BoundedNumericProperty`
    and defaults to 0.
    """

    indeterminate: bool = BooleanProperty(False)
    """Whether to show an indefinite animation instead of a fixed value.

    When True the indicator animates continuously.  When False
    :attr:`value` drives the visible progress.

    :attr:`indeterminate` is a :class:`~kivy.properties.BooleanProperty`
    and defaults to False.
    """

    indicator_color: List[float] = ColorProperty([0, 0, 0, 1])
    """Color of the active (filled) indicator segment.

    Defaults are applied via :attr:`default_config` which binds this to
    ``primary_color`` from the theme.

    :attr:`indicator_color` is a :class:`~kivy.properties.ColorProperty`.
    """

    track_color: List[float] = ColorProperty([0, 0, 0, 0.12])
    """Color of the background track.

    Defaults are applied via :attr:`default_config` which binds this to
    ``secondary_container_color`` from the theme.

    :attr:`track_color` is a :class:`~kivy.properties.ColorProperty`.
    """

    thickness: float = NumericProperty(dp(3))
    """Stroke width of both the track and the active indicator in pixels.

    :attr:`thickness` is a :class:`~kivy.properties.NumericProperty`
    and defaults to ``dp(4)``.
    """

    default_config: Dict[str, Any] = dict(
        theme_color_bindings=dict(
            indicator_color='primary_color',
            track_color='secondary_container_color',),)
    """Default theme color bindings applied during ``__init__``.

    Maps :attr:`indicator_color` to ``primary_color`` and
    :attr:`track_color` to ``secondary_container_color`` from the active
    theme.
    """

    def __init__(self, **kwargs) -> None:
        """Initialise the progress indicator, bind properties, and draw
        the initial canvas state.
        """
        config = self.default_config.copy() | kwargs
        super().__init__(**config)
        self.bind(
            pos=self._refresh_canvas,
            size=self._refresh_canvas,
            value=self._refresh_canvas,
            thickness=self._refresh_canvas,
            indicator_color=self._refresh_canvas_color,
            track_color=self._refresh_canvas_color,)
        self._setup_canvas()
        self._refresh_canvas()

    def _setup_canvas(self) -> None:
        """Initialise canvas instructions.  Called once in ``__init__``."""
        raise NotImplementedError

    def _refresh_canvas(self, *args) -> None:
        """Redraw canvas instructions to reflect current state.
        Must be implemented by subclasses.
        """
        raise NotImplementedError

    def _refresh_canvas_color(self, *args) -> None:
        """Update canvas color instructions to reflect current color 
        properties. Called when either :attr:`indicator_color` or 
        :attr:`track_color` changes."""
        self._track_color_instruction.rgba = self.track_color
        self._indicator_color_instruction.rgba = self.indicator_color


class MorphLinearProgress(_MorphProgressBase):
    """A horizontal linear progress indicator.

    Supports both determinate (value-driven) and indeterminate
    (animated) modes.  The ends of the active indicator are always
    rounded, and a small gap separates the indicator from the track.
    """

    def _get_indicator_points(self) -> List[float]:
        """Return a flat list of points for the active indicator.

        Points are inset by half :attr:`thickness` from each edge so the
        rounded caps stay within the widget bounds.  Returns an empty list
        when :attr:`value` is at or below :attr:`_VALUE_EPSILON`.
        """
        y = self.center_y
        x_start = self.x + self.thickness / 2
        x_end = self.right - self.thickness / 2
        if self.value >= 1.0 - self._VALUE_EPSILON:
            return [x_start, y, x_end, y]
        if self.value <= self._VALUE_EPSILON:
            return []
        x_indicator_end = x_start + (x_end - x_start) * self.value
        if x_indicator_end <= x_start:
            return []
        return [x_start, y, x_indicator_end, y]

    def _get_track_points(self) -> List[float]:
        """Return a flat list of points for the background track.

        The track starts after a small gap following the indicator end.
        Returns an empty list when :attr:`value` is at or above
        ``1 - _VALUE_EPSILON`` (fully complete).
        """
        y = self.center_y
        x_start = self.x + self.thickness / 2
        x_end = self.right - self.thickness / 2
        if self.value >= 1.0 - self._VALUE_EPSILON:
            return []
        if self.value <= self._VALUE_EPSILON:
            return [x_start, y, x_end, y]
        x_indicator_end = x_start + (x_end - x_start) * self.value
        x_track_start = x_indicator_end + 2 * self.thickness + dp(2)
        if x_track_start >= x_end:
            return []
        return [x_track_start, y, x_end, y]

    def _refresh_canvas(self, *args) -> None:
        """Redraw the track and indicator lines."""
        self._indicator_line.points = self._get_indicator_points()
        self._track_line.points = self._get_track_points()

    def _setup_canvas(self) -> None:
        """Create the two ``Line`` canvas instructions for track and
        indicator with rounded caps.
        """
        self.canvas.clear()
        with self.canvas:
            self._track_color_instruction = Color(*self.track_color)
            self._track_line = Line(
                points=[],
                width=self.thickness,
                cap='round')
            self._indicator_color_instruction = Color(*self.indicator_color)
            self._indicator_line = Line(
                points=[],
                width=self.thickness,
                cap='round')


class MorphCircularProgress(_MorphProgressBase):
    """A circular (arc) progress indicator.

    Supports both determinate (value-driven) and indeterminate
    (animated) modes.  The ends of the active arc are always rounded,
    and a small angular gap separates the indicator from the track.
    """
    _START_ANGLE: float = 0.0
    """Starting angle in degrees using Kivy's counterclockwise convention
    (0° = 3 o'clock, 90° = 12 o'clock).  Both arcs begin at this angle.
    """

    _circle_radius: float = AliasProperty(
        lambda self: (min(self.width, self.height) - self.thickness) / 2,
        cache=True,
        bind=['size', 'thickness'],)
    """Radius of the circular track and indicator.

    :attr:`_circle_radius` is a :class:`~kivy.properties.AliasProperty`,
    read-only and bound to the size and thickness of the widget.
    """

    def _refresh_canvas(self, *args) -> None:
        """Redraw the track and indicator arcs.

        Uses Kivy's built-in ``Line.circle`` primitive, delegating arc
        tessellation entirely to Kivy's renderer.
        """
        indicator = self._get_indicator_circle()
        if indicator:
            self._indicator_line.circle = indicator
        else:
            self._indicator_line.points = []

        track = self._get_track_circle()
        if track:
            self._track_line.circle = track
        else:
            self._track_line.points = []

    def _get_indicator_circle(self) -> None | Tuple[float, ...]:
        """Return a ``(cx, cy, r[, angle_start, angle_end])`` tuple for the
        active indicator arc, or ``None`` when nothing should be drawn.

        The indicator sweeps clockwise from :attr:`_START_ANGLE` (12 o'clock)
        by ``value × 360°``.
        """
        cx, cy, r = self.center_x, self.center_y, self._circle_radius
        if self.value <= self._VALUE_EPSILON:
            return None
        if self.value >= 1.0 - self._VALUE_EPSILON:
            return (cx, cy, r)
        angle_start = self._START_ANGLE
        angle_end = angle_start + self.value * 360
        return (cx, cy, r, angle_start, angle_end)

    def _get_track_circle(self) -> None | Tuple[float, ...]:
        """Return a ``(cx, cy, r[, angle_start, angle_end])`` tuple for the
        background track arc, or ``None`` when nothing should be drawn.

        At zero progress the full circle is drawn.  A small angular gap
        separates the track from the indicator.
        """
        cx, cy, r = self.center_x, self.center_y, self._circle_radius
        if self.value >= 1.0 - self._VALUE_EPSILON:
            return None
        if self.value <= self._VALUE_EPSILON:
            return (cx, cy, r)
        space = (2 * self.thickness + dp(2)) / r * (180 / math.pi)
        track_start = self._START_ANGLE + self.value * 360 + space
        track_end = self._START_ANGLE + 360 - space
        return (cx, cy, r, track_start, track_end)

    def _setup_canvas(self) -> None:
        """Create the two ``Line`` canvas instructions for track and
        indicator with rounded caps and joints.
        """
        self.canvas.clear()
        with self.canvas:
            self._track_color_instruction = Color(*self.track_color)
            self._track_line = Line(
                points=[],
                width=self.thickness,
                cap='round',
                joint='round',
                close=False)
            self._indicator_color_instruction = Color(*self.indicator_color)
            self._indicator_line = Line(
                points=[],
                width=self.thickness,
                cap='round',
                joint='round',
                close=False)
