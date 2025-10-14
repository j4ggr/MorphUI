from typing import List

from kivy.event import EventDispatcher
from kivy.graphics import Color
from kivy.graphics import BoxShadow
from kivy.properties import ListProperty
from kivy.properties import ColorProperty
from kivy.properties import BooleanProperty
from kivy.properties import BoundedNumericProperty


from ...constants import NAME


__all__ = [
    'MorphElevationBehavior',]


class MorphElevationBehavior(EventDispatcher):
    """A behavior class that provides elevation and shadow effects.

    This behavior adds elevation properties to widgets, allowing them to
    cast shadows based on their elevation level. It automatically manages
    the canvas graphics instructions to render shadows.

    Notes
    -----
    - Elevation is represented as a non-negative integer. Higher values
      result in more pronounced shadows.
    - The shadow's blur radius is calculated as
      `elevation * shadow_blur_factor`.
    - The shadow can be customized with color, offset, and whether it is
      inset or outset.

    for more details on the BoxShadow instruction, see:
    https://kivy.org/doc/stable/api-kivy.graphics.html#kivy.graphics.BoxShadow
    """

    elevation: int = BoundedNumericProperty(0, min=0, val_type=int)
    """Elevation level of the widget.

    The elevation is specified as a non-negative integer. Higher values
    result in more pronounced shadows. The value is clamped to be at
    least 0. To create a shadow, set this value to 1 or higher. A value
    of 0 means no elevation and no shadow. The blur radius is calculated
    as `elevation * shadow_blur_factor`.

    :attr:`elevation` is a 
    :class:`~kivy.properties.BoundedNumericProperty` and defaults to `0`.
    """

    shadow_inset: bool = BooleanProperty(False)
    """Whether the shadow is inset or outset.

    Defines whether the shadow is drawn from the inside out or from the 
    outline to the inside of the BoxShadow instruction.

    :attr:`shadow_inset` is a :class:`~kivy.properties.BooleanProperty`
    and defaults to `False` (outset)."""

    shadow_offset: List[float] = ListProperty([2, -2], length=2)
    """Offset of the shadow in the x and y directions.

    Specifies shadow offsets in (horizontal, vertical) format. Positive
    values for the offset indicate that the shadow should move to the 
    right and/or top. The negative ones indicate that the shadow should 
    move to the left and/or down.

    :attr:`shadow_offset` is a :class:`~kivy.properties.ListProperty`
    and defaults to `[1, -1]`."""

    shadow_blur_factor: int = BoundedNumericProperty(
        4, min=1, max=7, val_type=int, errorhandler=lambda x: max(1, min(x, 7)))
    """Factor to calculate blur radius from elevation.

    This factor is multiplied by the elevation to determine the blur radius.
    Higher values result in more blurred shadows. The value is clamped
    between 1 and 7 and must be an integer.

    :attr:`shadow_blur_factor` is a
    :class:`~kivy.properties.BoundedNumericProperty` and defaults to `4`.
    """

    shadow_color: List[float] = ColorProperty([0, 0, 0, 0.65])
    """Color of the shadow.

    The color should be provided as a list of RGBA values between 0 and
    1. Example: `[0, 0, 0, 0.65]` for a semi-transparent black shadow.

    :attr:`shadow_color` is a :class:`~kivy.properties.ColorProperty`
    and defaults to `[0, 0, 0, 0.65]`.
    """

    shadow_border_radius: List[float] = ListProperty([0, 0, 0, 0], length=4)
    """Border radius for the shadow corners.

    The order of the corners is: top-left, top-right, bottom-right,
    bottom-left. If the widget has a `radius` property (e.g. from
    `MorphSurfaceLayerBehavior`), that value will be used instead.

    :attr:`shadow_border_radius` is a
    :class:`~kivy.properties.ListProperty` and defaults to 
    `[0, 0, 0, 0]`."""

    _shadow_color_instruction: Color
    """Kivy Color instruction for the shadow color."""

    _shadow_instruction: BoxShadow
    """Kivy BoxShadow instruction for the shadow effect."""

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        
        group = NAME.SHADOW_LAYER
        with self.canvas.before:
            self._shadow_color_instruction = Color(
                rgba=self.shadow_color,
                group=group)
            self._shadow_instruction = BoxShadow(
                group=group,
                **self.shadow_params)
        
        self.bind(
            pos=self._update_elevation,
            size=self._update_elevation,
            elevation=self._update_elevation,
            shadow_color=self._update_elevation,
            shadow_offset=self._update_elevation,
            shadow_inset=self._update_elevation,
            shadow_blur_factor=self._update_elevation,
            shadow_border_radius=self._update_elevation,)
        if hasattr(self, 'radius'):
            self.bind(radius=self.setter('shadow_border_radius'))
            self.shadow_border_radius = self.radius
        self.refresh_elevation()

    @property
    def shadow_blur_radius(self) -> float:
        """Calculate blur radius based on elevation (read-only).
        
        The blur radius is determined by multiplying the 
        :attr:`elevation` by the :attr:`shadow_blur_factor`.
        """
        return self.elevation * self.shadow_blur_factor

    def _update_elevation(self, *args) -> None:
        """Update the shadow based on current elevation and properties."""
        rgba = [0, 0, 0, 0] if self.elevation < 1 else self.shadow_color
        self._shadow_color_instruction.rgba = rgba
        for key, value in self.shadow_params.items():
            setattr(self._shadow_instruction, key, value)
                    
    
    def refresh_elevation(self) -> None:
        """Manually refresh the elevation and shadow effect.

        This method can be called to force an update of the shadow
        effect, for example after changing multiple properties at once.
        """
        self._update_elevation()

    @property
    def shadow_params(self) -> dict:
        """Get current shadow parameters as a dictionary used
        for :class:`~kivy.graphics.instructions.BoxShadow` (read-only).

        If the elevation is less than 1, the shadow will be disabled
        by setting the offset to [0, 0] and blur_radius to 0.

        Returns
        -------
        dict
            A dictionary containing the current shadow parameters:
            - 'inset': Whether the shadow is inset or outset.
            - 'size': Current size of the widget.
            - 'pos': Current position of the widget.
            - 'offset': Current shadow offset as a list [x, y].
            - 'blur_radius': Calculated blur radius.
            - 'border_radius': Current border radius for the shadow 
              corners.
        
        Notes
        -----
        This dictionary is used to update the BoxShadow instruction
        whenever relevant properties change. The 'color' key is excluded
        here since it is managed separately by the Color instruction.
        """
        params = dict(
            inset=self.shadow_inset,
            size=self.size,
            pos=self.pos,
            offset=self.shadow_offset,
            blur_radius=self.shadow_blur_radius,
            border_radius=self.shadow_border_radius,)
        if self.elevation < 1:
            params |= dict(
                offset=[0, 0],
                blur_radius=0,)
        return params
