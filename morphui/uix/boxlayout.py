from kivy.uix.boxlayout import BoxLayout

from .behaviors.declarative import MorphDeclarativeBehavior

class MorphBoxLayout(MorphDeclarativeBehavior, BoxLayout):
    """A BoxLayout that supports declarative child widgets via
    :class:`MorphDeclarativeBehavior`.
    
    This class combines the functionality of Kivy's BoxLayout with
    the declarative child management provided by 
    :class:`MorphDeclarativeBehavior`. You can add child widgets
    declaratively by adding them to the :attr:`declarative_children`
    list.
    """
    pass