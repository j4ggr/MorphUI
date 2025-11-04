from typing import Any
from typing import Dict

from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleboxlayout import RecycleBoxLayout

from morphui.utils import clean_config
from morphui.uix.behaviors import MorphElevationBehavior
from morphui.uix.behaviors import MorphAutoSizingBehavior
from morphui.uix.behaviors import MorphColorThemeBehavior
from morphui.uix.behaviors import MorphDeclarativeBehavior
from morphui.uix.behaviors import MorphSurfaceLayerBehavior
from morphui.uix.behaviors import MorphDropdownBehavior


class MenuRecycleBoxLayout(
        RecycleBoxLayout):
    """A RecycleBoxLayout specifically for use within the MorphMenu
    widget to layout menu items in a vertical list.
    """
    pass


class MorphMenu(
        MorphDeclarativeBehavior,
        MorphAutoSizingBehavior,
        MorphColorThemeBehavior,
        MorphSurfaceLayerBehavior,
        MorphElevationBehavior,
        RecycleView,):
    """A MorphUI Menu widget that displays a list of items in a dropdown
    menu. Inherits from multiple behaviors to provide a rich set of 
    features including elevation, color theming, and auto-sizing.
    """

    default_config: Dict[str, Any] = dict(
        elevation=2,)

    def __init__(self, **kwargs) -> None:
        config = clean_config(self.default_config, kwargs)
        super().__init__(
            MenuRecycleBoxLayout(identity='layout'),
            **config)
        self.layout=self.identities.layout