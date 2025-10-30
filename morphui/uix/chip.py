from kivy.uix.boxlayout import BoxLayout

from morphui.uix.behaviors import MorphHoverBehavior
from morphui.uix.behaviors import MorphRippleBehavior
from morphui.uix.behaviors import MorphButtonBehavior
from morphui.uix.behaviors import MorphSurfaceLayerBehavior
from morphui.uix.behaviors import MorphContentLayerBehavior
from morphui.uix.behaviors import MorphInteractionLayerBehavior



class MorphChip(
        MorphHoverBehavior,
        MorphRippleBehavior,
        MorphButtonBehavior,
        MorphContentLayerBehavior,
        MorphInteractionLayerBehavior,
        MorphSurfaceLayerBehavior,
        BoxLayout,):
    pass