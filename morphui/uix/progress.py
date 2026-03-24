import math
from typing import Any
from typing import Dict
from typing import List
from typing import Tuple
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.graphics import Color
from kivy.graphics import Line
from kivy.graphics.context_instructions import PopMatrix
from kivy.graphics.context_instructions import PushMatrix
from kivy.graphics.context_instructions import Rotate
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

    indeterminate_duration: float = NumericProperty(1.33)
    """Duration in seconds of one full 360\u00b0 rotation in indeterminate mode.

    The complete cycle spans 4 turns, so the total animation time is
    ``4 \u00d7 indeterminate_duration``.  Defaults to ``1.33`` s, matching
    the Material Design specification.

    :attr:`indeterminate_duration` is a
    :class:`~kivy.properties.NumericProperty` and defaults to ``1.33``.
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

    In indeterminate mode the canvas group rotates at constant speed while
    the indicator arc span oscillates between 1/6 and 5/6 of the circle
    over a 4-turn cycle, producing a Material Design comet effect.
    """

    _START_ANGLE: float = 0.0
    """Starting angle in degrees using Kivy's counterclockwise convention
    (0° = 3 o'clock, 90° = 12 o'clock).  Both arcs begin at this angle.
    """

    _SPEED_AMPLITUDE: float = 0.7
    """Amplitude of the sinusoidal speed modulation (0–1).

    At ``0`` the rotation is perfectly constant.  At ``1`` speed varies
    between ``0`` and ``2×`` the mean, which would cause a momentary stop.
    ``0.7`` gives a visually noticeable fast–slow pulse while remaining
    smooth.  The integral over one period is always exactly 360°.
    """

    _anim_rotation: float = NumericProperty(0.0)
    """Current rotation angle in degrees driven by the indeterminate
    animation.  Updating this property rotates the canvas group via the
    :class:`~kivy.graphics.context_instructions.Rotate` instruction.
    """

    _circle_radius: float = AliasProperty(
        lambda self: (min(self.width, self.height) - self.thickness) / 2,
        cache=True,
        bind=['size', 'thickness'],)
    """Radius of the circular track and indicator.

    :attr:`_circle_radius` is a :class:`~kivy.properties.AliasProperty`,
    read-only and bound to the size and thickness of the widget.
    """

    def __init__(self, **kwargs) -> None:
        """Initialise the circular progress widget.

        Binds :attr:`_anim_rotation` so that animation frames update the
        :class:`~kivy.graphics.context_instructions.Rotate` instruction
        angle without touching any ``Line`` geometry.
        """
        super().__init__(**kwargs)
        self.bind(_anim_rotation=self._on_anim_rotation)

    def on_indeterminate(self, _instance, value: bool) -> None:
        """Start or stop the indeterminate rotation animation.

        Called automatically by Kivy whenever :attr:`indeterminate`
        changes.  Switching modes also refreshes the canvas so the
        correct geometry (fixed arc vs value-driven arc) is drawn.
        """
        if value:
            self._start_indeterminate_anim()
        else:
            self._stop_indeterminate_anim()
        self._refresh_canvas()

    def _on_anim_rotation(self, _instance, angle: float) -> None:
        """Propagate the animated angle to the canvas ``Rotate`` instruction.

        This is the only per-frame operation during indeterminate mode —
        no ``Line`` geometry is touched.
        """
        if not hasattr(self, '_rotation_instruction'):
            return
        self._rotation_instruction.angle = angle

    def _start_indeterminate_anim(self) -> None:
        """Start the indeterminate animation.

        Rotation is driven by :meth:`Clock.schedule_interval` so it
        advances every frame with no inter-cycle gap.  Arc span oscillation
        uses :class:`~kivy.animation.Animation` (4 sequential phases);
        the one-frame restart gap is invisible because ``value`` remains
        at ``1/6`` between cycle end and the next phase start.
        """
        self._stop_indeterminate_anim()
        self.value = 1 / 6
        self._turn_elapsed = 0.0
        self._rotation_event = Clock.schedule_interval(self._rotate_step, 0)
        self._restart_span_anim()

    def _rotate_step(self, dt: float) -> None:
        """Advance the rotation by one frame using a sinusoidal speed curve.

        Angular velocity varies as:

        .. code-block:: none

            v(t) = (360 / D) * (1 + A * sin(2π * t / D))

        where ``D`` is :attr:`indeterminate_duration`, ``A`` is
        :attr:`_SPEED_AMPLITUDE`, and ``t`` is time within the current
        turn.  Because ``sin`` integrates to zero over a full period, the
        total angle per turn is exactly 360° for any value of ``A``.
        """
        D = self.indeterminate_duration
        phase = 2 * math.pi * self._turn_elapsed / D
        speed = (360.0 / D) * (1.0 + self._SPEED_AMPLITUDE * math.sin(phase))
        self._anim_rotation -= speed * dt
        self._turn_elapsed = (self._turn_elapsed + dt) % D

    def _restart_span_anim(self) -> None:
        """Build and start one 4-phase arc-span animation cycle."""
        Animation.cancel_all(self, 'value')
        self.value = 1 / 6
        D = self.indeterminate_duration
        span = (
            Animation(value=1 / 6, duration=D)
            + Animation(value=5 / 6, duration=D, transition='out_sine')
            + Animation(value=5 / 6, duration=D)
            + Animation(value=1 / 6, duration=D, transition='out_sine'))
        span.bind(on_complete=self._on_indeterminate_cycle_complete)
        span.start(self)

    def _on_indeterminate_cycle_complete(self, _anim, _widget) -> None:
        """Restart the span animation after each 4-phase cycle completes.

        Rotation continues uninterrupted via :attr:`_rotation_event`.
        """
        if self.indeterminate:
            self._restart_span_anim()

    def _stop_indeterminate_anim(self) -> None:
        """Stop the rotation clock event and cancel the span animation."""
        if hasattr(self, '_rotation_event') and self._rotation_event:
            self._rotation_event.cancel()
            self._rotation_event = None
        Animation.cancel_all(self, 'value')
        self._anim_rotation = 0.0
        self.value = 0.0

    def _refresh_canvas(self, *args) -> None:
        """Redraw the track and indicator arcs and update the rotation origin.

        The :class:`~kivy.graphics.context_instructions.Rotate` pivot must
        track the widget centre whenever position or size changes.
        Uses Kivy's built-in ``Line.circle`` primitive for arc tessellation.
        """
        if not hasattr(self, '_rotation_instruction'):
            return
        self._rotation_instruction.origin = (self.center_x, self.center_y)

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

        In indeterminate mode the arc spans ``value × 360°`` from
        :attr:`_START_ANGLE`; the whole canvas group is rotated by the
        :class:`~kivy.graphics.context_instructions.Rotate` instruction.
        In determinate mode the arc spans ``value × 360°`` driven by the caller.
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

        In indeterminate mode the full circle is always drawn as the track.
        In determinate mode at zero progress the full circle is drawn and a
        small angular gap separates the track from the indicator.
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
        """Create the canvas instructions for track and indicator arcs.

        A :class:`~kivy.graphics.context_instructions.PushMatrix` /
        :class:`~kivy.graphics.context_instructions.Rotate` /
        :class:`~kivy.graphics.context_instructions.PopMatrix` triplet
        wraps both ``Line`` instructions.  During indeterminate mode only
        ``Rotate.angle`` is updated — the ``Line`` geometry stays static.
        """
        self.canvas.clear()
        with self.canvas:
            PushMatrix()
            self._rotation_instruction = Rotate(
                angle=0,
                axis=(0, 0, 1),
                origin=(self.center_x, self.center_y),)
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
            PopMatrix()
