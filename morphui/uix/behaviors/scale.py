from typing import List

from kivy.event import EventDispatcher
from kivy.graphics import Scale
from kivy.graphics import PopMatrix
from kivy.graphics import PushMatrix
from kivy.properties import BoundedNumericProperty
from kivy.properties import VariableListProperty

__all__ = [
    'MorphScaleBehavior',]


class MorphScaleBehavior(EventDispatcher):
    """Behavior that adds scaling capabilities to widgets.

    This behavior provides properties to control scaling factors along
    the X, Y, and Z axes, as well as the origin point for scaling
    transformations. It utilizes Kivy's graphics instructions to apply
    scaling effects to the widget.
    """

    scale_factor_x: float = BoundedNumericProperty(
        1.0, min=0.0, errorvalue=0.0)
    """Scaling factor along the X-axis.

    Defines the scaling factor applied to the widget along the X-axis.
    A value of `1.0` means no scaling, values greater than `1.0` will
    enlarge the widget, and values between `0.0` and `1.0` will shrink 
    it. The value is clamped to be at least `0.0`.

    :attr:`scale_factor_x` is a
    :class:`~kivy.properties.BoundedNumericProperty` and defaults to 
    `1.0`.
    """

    scale_factor_y: float = BoundedNumericProperty(
        1.0, min=0.0, errorvalue=0.0)
    """Scaling factor along the Y-axis.

    Defines the scaling factor applied to the widget along the Y-axis.
    A value of `1.0` means no scaling, values greater than `1.0` will
    enlarge the widget, and values between `0.0` and `1.0` will shrink
    it. The value is clamped to be at least `0.0`.

    :attr:`scale_factor_y` is a
    :class:`~kivy.properties.BoundedNumericProperty` and defaults to
    `1.0`.
    """

    scale_factor_z: float = BoundedNumericProperty(
        1.0, min=0.0, errorvalue=0.0)
    """Scaling factor along the Z-axis.

    Defines the scaling factor applied to the widget along the Z-axis.
    A value of `1.0` means no scaling, values greater than `1.0` will
    enlarge the widget, and values between `0.0` and `1.0` will shrink
    it. The value is clamped to be at least `0.0`.

    :attr:`scale_factor_z` is a
    :class:`~kivy.properties.BoundedNumericProperty` and defaults to
    `1.0`.
    """

    scale_origin: List[float] = VariableListProperty([0.0, 0.0, 0.0], length=3)
    """Origin point for scaling transformations.
    
    This property defines the point around which the scaling occurs.
    It is a 3D point represented by a list of three floats (x, y, z).

    :attr:`scale_origin` is a
    :class:`~kivy.properties.VariableListProperty` of length 3 and
    defaults to `[0.0, 0.0, 0.0]`.
    """

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        with self.canvas.before:
            PushMatrix()
            self._scale_instruction = Scale(
                x=self.scale_factor_x,
                y=self.scale_factor_y,
                z=self.scale_factor_z,
                origin=self.scale_origin)
        with self.canvas.after:
            PopMatrix()

        self.bind(
            scale_factor_x=self._update_scale,
            scale_factor_y=self._update_scale,
            scale_factor_z=self._update_scale,
            scale_origin=self._update_scale)

    def _update_scale(self, *args) -> None:
        """Update the scale transformation based on the current 
        properties.
        
        This method updates the Scale instruction with the current
        scaling factors and origin point whenever any of the related
        properties change.
        """
        self._scale_instruction.x = self.scale_factor_x
        self._scale_instruction.y = self.scale_factor_y
        self._scale_instruction.z = self.scale_factor_z
        self._scale_instruction.origin = self.scale_origin
