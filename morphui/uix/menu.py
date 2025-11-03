
from kivy.uix.boxlayout import BoxLayout

from morphui.uix.behaviors import MorphElevationBehavior
from morphui.uix.behaviors import MorphAutoSizingBehavior
from morphui.uix.behaviors import MorphColorThemeBehavior
from morphui.uix.behaviors import MorphDeclarativeBehavior
from morphui.uix.behaviors import MorphSurfaceLayerBehavior
from morphui.uix.behaviors import MorphDropdownBehavior



class MorphMenu(
        MorphDeclarativeBehavior,
        MorphAutoSizingBehavior,
        MorphColorThemeBehavior,
        MorphSurfaceLayerBehavior,
        MorphElevationBehavior,
        BoxLayout):
    pass