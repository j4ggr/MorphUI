
from kivy.uix.label import Label

from .behaviors import MorphBackgroundBehavior


__all__ = [
    'MorphLabel'
]


class MorphLabel(MorphBackgroundBehavior, Label):
    pass