
from kivy.uix.behaviors import ButtonBehavior

from .label import MorphLabel

__all__ = [
    'MorphBaseButton'
]


class MorphBaseButton(ButtonBehavior, MorphLabel):
    pass