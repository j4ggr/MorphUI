from textwrap import dedent

from typing import Any
from typing import Callable
from typing import Dict
from typing import List
from typing import Optional

from kivy.lang import Builder
from kivy.properties import ListProperty
from kivy.properties import AliasProperty
from kivy.properties import ObjectProperty
from kivy.properties import NumericProperty
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleboxlayout import RecycleBoxLayout

from morphui.utils import clean_config
from morphui.uix.behaviors import MorphHoverBehavior
from morphui.uix.behaviors import MorphRippleBehavior
from morphui.uix.behaviors import MorphButtonBehavior
from morphui.uix.behaviors import MorphElevationBehavior
from morphui.uix.behaviors import MorphMenuMotionBehavior
from morphui.uix.behaviors import MorphAutoSizingBehavior
from morphui.uix.behaviors import MorphColorThemeBehavior
from morphui.uix.behaviors import MorphDeclarativeBehavior
from morphui.uix.behaviors import MorphSurfaceLayerBehavior
from morphui.uix.behaviors import MorphInteractionLayerBehavior
from morphui.uix.container import LeadingTextTrailingContainer


__all__ = [
    'MorphDropdownMenuItem',
    'MenuRecycleBoxLayout',
    'MorphDropdownMenu',
    ]


class MorphDropdownMenuItem(
        MorphHoverBehavior,
        MorphRippleBehavior,
        MorphButtonBehavior,
        MorphColorThemeBehavior,
        MorphInteractionLayerBehavior,
        LeadingTextTrailingContainer,):
    """A single item within the MorphDropdownMenu widget.
    
    This widget represents a menu item with support for leading icon,
    text label, and trailing icon. It inherits from
    :class:`~morphui.uix.container.LeadingTextTrailingContainer` which
    provides the layout structure and child widget management.
    """

    rv_index: int = NumericProperty(0)
    """The index of this label within the RecycleView data.

    :attr:`rv_index` is a :class:`~kivy.properties.NumericProperty`
    and defaults to `0`.
    """

    rv: RecycleView = ObjectProperty(None)
    """The RecycleView instance managing this label.

    :attr:`rv` is a :class:`~kivy.properties.ObjectProperty`
    and defaults to `None`.
    """

    default_config: Dict[str, Any] = (
        LeadingTextTrailingContainer.default_config.copy() | dict())

    def __init__(self, **kwargs) -> None:
        config = clean_config(self.default_config, kwargs)
        super().__init__(**config)

    def refresh_view_attrs(
            self,
            rv: RecycleView,
            index: int,
            data: List[Dict[str, Any]]
            ) -> None:
        """Refreshes the view attributes of this menu item.

        Parameters
        ----------
        rv : RecycleView
            The RecycleView instance managing this menu item.
        index : int
            The index of this menu item within the RecycleView data.
        data : List[Dict[str, Any]]
            The data list containing the attributes for all menu items.
        """
        super().refresh_view_attrs(rv, index, data)
        self.rv = rv
        self.rv_index = index
        self.refresh_auto_sizing()
        rv.data[index]['width'] = self.width
        rv.data[index]['height'] = self.height


class MenuRecycleBoxLayout(
        MorphAutoSizingBehavior,
        RecycleBoxLayout):
    """A RecycleBoxLayout specifically for use within the MorphMenu
    widget to layout menu items in a vertical list.
    """
    default_config: Dict[str, Any] = dict(
        orientation='vertical',
        size_hint=(None, None),
        size=(500, 200),)
    
    def __init__(self, **kwargs) -> None:
        config = clean_config(self.default_config, kwargs)
        super().__init__(**config)


class MorphDropdownMenu(
        MorphDeclarativeBehavior,
        MorphAutoSizingBehavior,
        MorphColorThemeBehavior,
        MorphSurfaceLayerBehavior,
        MorphElevationBehavior,
        MorphMenuMotionBehavior,
        RecycleView,):
    """A MorphUI Menu widget that displays a list of items in a dropdown
    menu. Inherits from multiple behaviors to provide a rich set of 
    features including elevation, color theming, and auto-sizing.
    """
    Builder.load_string(dedent('''
        <MorphDropdownMenu>:
            viewclass: 'MorphDropdownMenuItem'
            layout: layout
            MenuRecycleBoxLayout:
                id: layout
                default_size: None, dp(48)
                default_size_hint: 1, None
                size_hint_y: None
                height: self.minimum_height
                orientation: "vertical"
        '''))

    layout: MenuRecycleBoxLayout = ObjectProperty(None)
    """The layout manager for the menu items, specifically a
    MenuRecycleBoxLayout instance.

    This property is used to organize and display the menu items
    in a vertical list format.

    :attr:`layout` is an :class:`~kivy.properties.ObjectProperty`
    and defaults to `None`.
    """

    filter_value: Any = ObjectProperty('')
    """The current filter value used to filter menu items.

    This property holds the value used to filter the menu items. Items
    that do not match the filter criteria will be excluded from the
    displayed list. Override the :meth:`should_filter_item` method to
    customize the filtering behavior.

    :attr:`filter_value` is an :class:`~kivy.properties.ObjectProperty`
    and defaults to an empty string."""

    on_item_release: Optional[Callable[[Any, int], None]] = ObjectProperty(None)
    """Callback function called when a menu item is released.

    This callback is triggered when a user releases a menu item after
    clicking or tapping it. The callback should accept two parameters:
    the menu item widget instance and its index.

    Example
    -------
    ```python
    def handle_item_release(item, index):
        print(f"Item {index} released: {item.text}")
    menu.on_item_release = handle_item_release
    ```

    :attr:`on_item_release` is an :class:`~kivy.properties.ObjectProperty`
    and defaults to `None`."""

    _items: List[Dict[str, Any]] = ListProperty([])
    """Internal storage for the list of menu items."""

    def _get_items(self) -> List[Dict[str, Any]]:
        """Get the list of menu items, filtered based on the current
        filter value.

        Returns
        -------
        List[Dict[str, Any]]
            A list of dictionaries representing the menu items that
            are not filtered out.
        """
        return list(filter(
            lambda item: not self.should_filter_item(item),
            self._items))

    def _set_items(self, items: List[Dict[str, Any]]) -> None:
        """Set the menu items for the dropdown menu.

        This method updates the RecycleView's data to reflect the
        provided list of menu items. Each item dictionary is
        augmented with an `on_release` callback that points to the
        menu's :meth:`on_item_release` method if it is not already
        provided.

        Parameters
        ----------
        items : List[Dict[str, Any]]
            A list of dictionaries representing the menu items. Each
            dictionary should contain the properties for a single
            MorphDropdownMenuItem.
        """
        if self.on_item_release is None:
            self._items = items
        else:
            self._items = [
                {'on_release': self.on_item_release, **item} for item in items]

    items: List[Dict[str, Any]] = AliasProperty(
        _get_items,
        _set_items,
        bind=[
            '_items',
            'filter_value'])
    """List of menu items available for the dropdown menu.

    This property allows getting and setting the list of menu items.
    Items that are filtered out based on the current filter value
    will not be included in the returned list. This property is used to 
    dynamically update the menu contents. Override the 
    :meth:`should_filter_item` method to customize filtering behavior.

    :attr:`items` is an :class:`~kivy.properties.AliasProperty` and
    is bound to changes in the `_items` and `filter_value` properties.
    """

    default_config: Dict[str, Any] = dict(
        size_hint=(None, None),
        auto_size=(True, True),
        elevation=2,)
    """Default configuration for the `MorphDropdownMenu` widget."""

    def __init__(self, **kwargs) -> None:
        config = clean_config(self.default_config, kwargs)
        super().__init__(**config)
        self.bind(items=self.setter('data'))
        self.data = self.items

    def should_filter_item(self, item: Dict[str, Any]) -> bool:
        """Determine if a menu item should be filtered out based on
        the current filter value.

        This method checks if the provided menu item matches the
        filter criteria. If it does not match, the item is considered
        filtered out and will not be displayed in the menu.
        Override this method to implement custom filtering logic.

        Parameters
        ----------
        item : Dict[str, Any]
            A dictionary representing a single menu item.

        Returns
        -------
        bool
            `True` if the item should be filtered out, `False`
            otherwise.
        """
        filter_val = str(self.filter_value).lower()
        item_text = str(item.get('text', '')).lower()
        return filter_val not in item_text



