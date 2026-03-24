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

    In indeterminate mode a bar of fixed width slides continuously from
    left to right.  Clamping the bar to the track bounds creates a
    natural grow/shrink effect at each edge without requiring clipping.
    """

    _INDETERMINATE_BAR_FRACTION: float = 0.35
    """Width of the animated bar as a fraction of the track width in
    indeterminate mode.  Defaults to ``0.35`` (35 %).
    """

    default_config: Dict[str, Any] = (
        _MorphProgressBase.default_config.copy() | dict(
        size_hint=(1, None),
        height=dp(8),))
    """Default configuration for the linear progress indicator.
    Inherits from :attr:`_MorphProgressBase.default_config` and adds
    ``size_hint=(1, None)`` to make the widget expand horizontally by 
    default.
    """

    def on_indeterminate(self, _instance, value: bool) -> None:
        """Start or stop the indeterminate sliding animation.

        Called automatically by Kivy whenever :attr:`indeterminate`
        changes.  Switching modes also refreshes the canvas so the
        correct geometry is drawn immediately.
        """
        if value:
            self._start_indeterminate_anim()
        else:
            self._stop_indeterminate_anim()
        self._refresh_canvas()

    def _start_indeterminate_anim(self) -> None:
        """Start the indeterminate animation.

        A :class:`~kivy.clock.Clock` interval advances a positional
        offset every frame so the bar slides continuously from left to
        right with no frame gap between cycles.
        """
        self._stop_indeterminate_anim()
        self._ind_offset = 0.0
        self._ind_event = Clock.schedule_interval(self._offset_step, 0)

    def _offset_step(self, dt: float) -> None:
        """Advance the bar position by one frame and redraw.

        ``_ind_offset`` increases from ``0`` to ``1`` over
        :attr:`indeterminate_duration` seconds, then wraps.  At ``0``
        the bar's leading edge is at the left boundary of the track;
        at ``1`` it exits the right boundary.
        """
        self._ind_offset = (
            self._ind_offset + dt / self.indeterminate_duration) % 1.0
        self._refresh_canvas()

    def _stop_indeterminate_anim(self) -> None:
        """Stop the sliding animation and reset position state."""
        if hasattr(self, '_ind_event') and self._ind_event:
            self._ind_event.cancel()
            self._ind_event = None
        self._ind_offset = 0.0
        self.value = 0.0

    def _get_bar_bounds(self) -> tuple[float, float] | None:
        """Return ``(draw_left, draw_right)`` of the indeterminate bar.

        Both values are already clamped to the track bounds.  Returns
        ``None`` when the bar is fully outside the visible track area.
        """
        x0 = self.x + self.thickness / 2
        x1 = self.right - self.thickness / 2
        track_w = x1 - x0
        if track_w <= 0:
            return None
        
        bar_w = track_w * self._INDETERMINATE_BAR_FRACTION
        offset = getattr(self, '_ind_offset', 0.0)
        bar_left = x0 - bar_w + offset * (track_w + bar_w)
        draw_left = max(bar_left, x0)
        draw_right = min(bar_left + bar_w, x1)
        if draw_right <= draw_left:
            return None
        
        return (draw_left, draw_right)

    def _get_indicator_points(self) -> List[float]:
        """Return a flat list of points for the active indicator.

        In indeterminate mode the bar bounds come from
        :meth:`_get_bar_bounds`.  In determinate mode points are inset
        by half :attr:`thickness` so rounded caps stay within bounds.
        """
        y = self.center_y
        x0 = self.x + self.thickness / 2
        x1 = self.right - self.thickness / 2
        track_w = x1 - x0
        if track_w <= 0:
            return []

        if self.indeterminate:
            bounds = self._get_bar_bounds()
            if bounds is None:
                return []
            
            draw_left, draw_right = bounds
            return [draw_left, y, draw_right, y]
        
        if self.value >= 1.0 - self._VALUE_EPSILON:
            return [x0, y, x1, y]
        
        if self.value <= self._VALUE_EPSILON:
            return []

        x_indicator_end = x0 + track_w * self.value
        if x_indicator_end <= x0:
            return []
        
        return [x0, y, x_indicator_end, y]

    def _get_track_points(self) -> List[float]:
        """Return points for the left track segment.

        In indeterminate mode the track is split around the sliding bar
        with the same gap as determinate mode; this method returns the
        left segment and :meth:`_get_track_points_right` the right one.
        In determinate mode returns the segment after the indicator gap.
        Returns an empty list when :attr:`value` is at or above
        ``1 - _VALUE_EPSILON`` (fully complete).
        """
        y = self.center_y
        x0 = self.x + self.thickness / 2
        x1 = self.right - self.thickness / 2
        gap = 2 * self.thickness + dp(2)
        if self.indeterminate:
            bounds = self._get_bar_bounds()
            if bounds is None:
                return [x0, y, x1, y]
            draw_left, _draw_right = bounds
            x_left_end = draw_left - gap
            if x_left_end <= x0:
                return []
            return [x0, y, x_left_end, y]
        if self.value >= 1.0 - self._VALUE_EPSILON:
            return []
        if self.value <= self._VALUE_EPSILON:
            return [x0, y, x1, y]
        x_indicator_end = x0 + (x1 - x0) * self.value
        x_track_start = x_indicator_end + gap
        if x_track_start >= x1:
            return []
        return [x_track_start, y, x1, y]

    def _get_track_points_right(self) -> List[float]:
        """Return points for the right track segment in indeterminate mode.

        Returns an empty list in determinate mode.  The segment starts
        after a gap following the indicator bar's right edge.
        """
        if not self.indeterminate:
            return []
        y = self.center_y
        x1 = self.right - self.thickness / 2
        gap = 2 * self.thickness + dp(2)
        bounds = self._get_bar_bounds()
        if bounds is None:
            return []
        _draw_left, draw_right = bounds
        x_right_start = draw_right + gap
        if x_right_start >= x1:
            return []
        return [x_right_start, y, x1, y]

    def _refresh_canvas(self, *args) -> None:
        """Redraw the track and indicator lines."""
        if not hasattr(self, '_track_line'):
            return
        
        self._indicator_line.points = self._get_indicator_points()
        self._track_line.points = self._get_track_points()
        self._track_line_2.points = self._get_track_points_right()

    def _setup_canvas(self) -> None:
        """Create the ``Line`` canvas instructions for track and indicator.

        Two track lines are created so that in indeterminate mode the
        track can be split into a left and a right segment around the
        sliding bar.  Both share the same ``Color`` instruction.
        """
        self.canvas.clear()
        with self.canvas:
            self._track_color_instruction = Color(*self.track_color)
            self._track_line = Line(
                points=[],
                width=self.thickness,
                cap='round')
            self._track_line_2 = Line(
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

    default_config: Dict[str, Any] = (
        _MorphProgressBase.default_config.copy() | dict(
        size_hint=(None, None),
        size=(dp(48), dp(48)),))
    """Default configuration for the circular progress indicator.

    Inherits from :attr:`_MorphProgressBase.default_config` and adds
    ``size_hint=(None, None)`` and ``size=(dp(48), dp(48))`` to set a
    default fixed size.
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


class MorphWavyLinearProgress(MorphLinearProgress):
    """A horizontal linear progress indicator with a sinusoidal wave stroke.

    Inherits all behaviour (including indeterminate mode) from
    :class:`MorphLinearProgress`.  The indicator and track segments are
    rendered as dense polylines tracing a sine wave instead of a straight
    line.

    Because the wave phase is tied to the absolute x coordinate, the
    indicator and track together form one continuous wave pattern with only
    the gap separating them.  In indeterminate mode the sliding bar reveals
    a travelling-wave effect as different x positions scroll into view.
    """

    _LINEAR_WAVELENGTH: float = dp(40)
    """Spatial wavelength of the sine wave in pixels.  Defaults to ``dp(40)``."""

    _WAVE_AMPLITUDE: float = dp(3)
    """Half-height of the wave in pixels (peak to centre).
    Defaults to ``dp(3)``.
    """

    _SAMPLES_PER_WAVELENGTH: int = 8
    """Number of polyline vertices per full wavelength.  ``8`` gives a
    smooth appearance while remaining cheap to compute each frame.
    """

    def _make_wave_points(
            self,
            x_start: float,
            x_end: float,
            y_center: float,
            ) -> List[float]:
        """Return a flat ``[x, y, x, y, …]`` polyline tracing a sine wave.

        Phase is derived from the absolute x coordinate so that adjacent
        segments always share a single continuous wave pattern.
        """
        length = x_end - x_start
        if length <= 0:
            return []
        n = max(2, math.ceil(
            length / self._LINEAR_WAVELENGTH * self._SAMPLES_PER_WAVELENGTH))
        pts: List[float] = []
        for i in range(n + 1):
            x = x_start + (i / n) * length
            y = y_center + self._WAVE_AMPLITUDE * math.sin(
                2 * math.pi * x / self._LINEAR_WAVELENGTH)
            pts.extend((x, y))
        return pts

    def _get_indicator_points(self) -> List[float]:
        y = self.center_y
        x0 = self.x + self.thickness / 2
        x1 = self.right - self.thickness / 2
        track_w = x1 - x0
        if track_w <= 0:
            return []
        if self.indeterminate:
            bounds = self._get_bar_bounds()
            if bounds is None:
                return []
            return self._make_wave_points(bounds[0], bounds[1], y)
        if self.value >= 1.0 - self._VALUE_EPSILON:
            return self._make_wave_points(x0, x1, y)
        if self.value <= self._VALUE_EPSILON:
            return []
        return self._make_wave_points(x0, x0 + track_w * self.value, y)


class MorphWavyCircularProgress(MorphCircularProgress):
    """A circular arc progress indicator with a sinusoidal radial wave stroke.

    Inherits all behaviour (including indeterminate mode) from
    :class:`MorphCircularProgress`.  The indicator and track arcs are
    rendered as dense polylines with a radial sine perturbation instead of
    using the built-in ``Line.circle`` primitive.

    Phase is based on arc length measured from 0° so indicator and track
    share a single continuous global wave pattern around the circle.  The
    entire polyline group is still rotated by the canvas
    :class:`~kivy.graphics.context_instructions.Rotate` instruction during
    indeterminate mode.
    """

    _CIRCULAR_WAVELENGTH: float = dp(15)
    """Arc-length wavelength of the sine wave in pixels.
    Defaults to ``dp(15)``.
    """

    _WAVE_AMPLITUDE: float = dp(2)
    """Radial amplitude of the wave in pixels (peak deviation from the base
    radius).  Defaults to ``dp(2)``.
    """

    _SAMPLES_PER_WAVELENGTH: int = 8
    """Number of polyline vertices per full wavelength."""

    def _make_wave_arc_points(
            self,
            cx: float,
            cy: float,
            r: float,
            angle_start: float,
            angle_end: float,
            ) -> List[float]:
        """Return a wavy arc as a flat ``[x, y, …]`` polyline.

        The wave oscillates radially around ``r``.  Phase is computed as
        arc length from 0° (``angle * π/180 * r``) so all arc segments
        on the same circle share a continuous wave pattern.
        """
        arc_length = abs(angle_end - angle_start) * math.pi / 180 * r
        if arc_length <= 0:
            return []
        
        n = max(2, math.ceil(
            arc_length / self._CIRCULAR_WAVELENGTH * self._SAMPLES_PER_WAVELENGTH))
        pts: List[float] = []
        for i in range(n + 1):
            angle_deg = angle_start + (i / n) * (angle_end - angle_start)
            angle_rad = math.radians(90.0 - angle_deg)
            arc_pos = angle_deg * math.pi / 180 * r  # phase from 0°
            radius = r + self._WAVE_AMPLITUDE * math.sin(
                2 * math.pi * arc_pos / self._CIRCULAR_WAVELENGTH)
            pts.extend((
                cx + radius * math.cos(angle_rad),
                cy + radius * math.sin(angle_rad),
            ))
        return pts

    def _circle_to_points(self, circle: Tuple[float, ...]) -> List[float]:
        """Convert a ``(cx, cy, r)`` or ``(cx, cy, r, a_start, a_end)``
        circle tuple into wavy arc polyline points.
        """
        if len(circle) == 3:
            cx, cy, r = circle
            return self._make_wave_arc_points(cx, cy, r, 0.0, 360.0)
        
        cx, cy, r, a_start, a_end = circle
        return self._make_wave_arc_points(cx, cy, r, a_start, a_end)

    def _refresh_canvas(self, *args) -> None:
        """Redraw the wavy indicator and the straight track arc.

        The indicator is rendered as a dense wavy polyline via
        :meth:`_circle_to_points`.  The track uses the parent's
        ``Line.circle`` primitive so it remains a plain arc.
        The :class:`~kivy.graphics.context_instructions.Rotate` pivot is
        updated on every call.
        """
        if not hasattr(self, '_rotation_instruction'):
            return
        
        self._rotation_instruction.origin = (self.center_x, self.center_y)
        indicator = self._get_indicator_circle()
        self._indicator_line.points = (
            self._circle_to_points(indicator) if indicator else [])

        track = self._get_track_circle()
        if track:
            self._track_line.circle = track
        else:
            self._track_line.points = []
