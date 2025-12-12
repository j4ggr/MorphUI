from typing import Any
from typing import Dict

from kivy.properties import ObjectProperty
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleboxlayout import RecycleBoxLayout

from morphui.utils import clean_config
from morphui.uix.behaviors import MorphElevationBehavior
from morphui.uix.behaviors import MorphAutoSizingBehavior
from morphui.uix.behaviors import MorphColorThemeBehavior
from morphui.uix.behaviors import MorphDeclarativeBehavior
from morphui.uix.behaviors import MorphSurfaceLayerBehavior
from morphui.uix.container import LeadingTextTrailingContainer


class MorphMenuItem(LeadingTextTrailingContainer):
    """A single item within the MorphMenu widget.
    
    This widget represents a menu item with support for leading icon,
    text label, and trailing icon. It inherits from
    :class:`~morphui.uix.container.LeadingTextTrailingContainer` which
    provides the layout structure and child widget management.
    """

    default_config: Dict[str, Any] = (
        LeadingTextTrailingContainer.default_config.copy() | dict())

    def __init__(self, **kwargs) -> None:
        config = clean_config(self.default_config, kwargs)
        super().__init__(**config)


class MenuRecycleBoxLayout(
        MorphAutoSizingBehavior,
        RecycleBoxLayout):
    """A RecycleBoxLayout specifically for use within the MorphMenu
    widget to layout menu items in a vertical list.
    """
    default_config: Dict[str, Any] = dict(
        orientation='vertical',)
    
    def __init__(self, **kwargs) -> None:
        config = clean_config(self.default_config, kwargs)
        super().__init__(**config)


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

    layout: MenuRecycleBoxLayout = ObjectProperty(None)
    """The layout manager for the menu items, specifically a
    MenuRecycleBoxLayout instance.

    This property is used to organize and display the menu items
    in a vertical list format.

    :attr:`layout` is an :class:`~kivy.properties.ObjectProperty`
    and defaults to `None`.
    """

    default_config: Dict[str, Any] = dict(
        elevation=2,)

    def __init__(
            self,
            layout: MenuRecycleBoxLayout | None = None,
            **kwargs) -> None:
        self.layout = layout or MenuRecycleBoxLayout()
        config = clean_config(self.default_config, kwargs)
        super().__init__(
            self.layout,
            **config)