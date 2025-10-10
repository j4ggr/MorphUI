from typing import List

from kivy.event import EventDispatcher
from kivy.properties import BooleanProperty


__all__ = [
    'MorphRoundSidesBehavior',
    ]


class MorphRoundSidesBehavior(EventDispatcher):
    """Behavior to enable automatic rounding of left and right sides.

    This behavior provides a `round_sides` property that, when enabled,
    automatically adjusts the widget's `radius` property to half of its
    height. This creates perfectly rounded left and right sides, useful
    for pill-shaped buttons, badges, or labels.

    If `height` is greater than `width`, the radius will be set to
    half of the `width`, resulting in a fully rounded shape. Otherwise,
    the radius will be half of the `height`, creating rounded sides.
    This ensures that the widget maintains a visually appealing shape
    regardless of its dimensions.
    """
    
    round_sides: bool = BooleanProperty(False)
    """Enable automatic rounding of left and right sides.
    
    When True, the radius property is automatically bound to half of the
    widget's height, creating perfectly rounded left and right sides
    regardless of the widget's height. This is useful for creating
    pill-shaped buttons, badges, or labels.
    
    When False, the radius property behaves normally and can be set
    independently.

    :attr:`round_sides` is a :class:`~kivy.properties.BooleanProperty` 
    and defaults to False.
    """

    _original_radius: List[int] | None
    """Store original radius value when round_sides is enabled."""

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self._original_radius = getattr(self, 'radius', None)
        self.bind(round_sides=self._update_round_sides)
        self.bind(size=self._update_round_sides)
        self._update_round_sides(self, self.round_sides)

    def _update_round_sides(self, *args) -> None:
        if self.round_sides:
            self.radius = min(self.size) / 2
        elif self._original_radius is not None:
            self.radius = self._original_radius
