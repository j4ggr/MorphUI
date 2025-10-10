from .behaviors import MorphElevationBehavior
from .behaviors import MorphCircularRippleBehavior
from .behaviors import MorphRectangularRippleBehavior

from .label import MorphLabel
from .label import MorphIconLabel

__all__ = [
    'MorphButton',
    'MorphIconButton']


class MorphButton(
        MorphRectangularRippleBehavior,
        # MorphElevationBehavior,
        MorphLabel):
    """A button widget with ripple effect and MorphUI theming.
    
    This class combines Kivy's TouchRippleButtonBehavior with MorphUI's
    MorphLabel to create a button that supports ripple effects and 
    theming.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        print(self.available_states)


class MorphIconButton(
        MorphRectangularRippleBehavior,
        # MorphElevationBehavior,
        MorphIconLabel):
    """A button widget designed for icon display with ripple effect 
    and MorphUI theming.
    
    This class is similar to MorphButton but is intended for use with
    icon fonts or images, providing a button that supports ripple 
    effects and theming.
    """
    pass