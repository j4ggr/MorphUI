
from kivy.uix.behaviors import TouchRippleButtonBehavior

from .label import MorphLabel

__all__ = [
    'MorphBaseButton'
]


class MorphBaseButton(
        TouchRippleButtonBehavior,
        MorphLabel):
    pass