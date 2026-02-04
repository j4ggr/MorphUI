from typing import Any
from typing import Dict
from typing import List
from typing import Callable

from kivy.metrics import dp
from kivy.properties import ListProperty
from kivy.properties import DictProperty
from kivy.properties import AliasProperty
from kivy.properties import ObjectProperty
from kivy.properties import BooleanProperty
from kivy.properties import NumericProperty
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.views import RecycleDataViewBehavior

from morphui.utils import clean_config
from morphui.uix.behaviors import MorphHoverBehavior
from morphui.uix.behaviors import MorphRippleBehavior
from morphui.uix.behaviors import MorphButtonBehavior
from morphui.uix.behaviors import MorphKeyPressBehavior
from morphui.uix.behaviors import MorphColorThemeBehavior
from morphui.uix.behaviors import MorphToggleButtonBehavior
from morphui.uix.behaviors import MorphOverlayLayerBehavior
from morphui.uix.behaviors import MorphContentLayerBehavior
from morphui.uix.behaviors import MorphIdentificationBehavior
from morphui.uix.behaviors import MorphDelegatedThemeBehavior
from morphui.uix.behaviors import MorphInteractionLayerBehavior
from morphui.uix.container import MorphIconLabelIconContainer
from morphui.uix.recycleboxlayout import MorphRecycleBoxLayout


__all__ = [
    'MorphListItemFlat',
    'MorphToggleListItemFlat',
    'MorphListLayout',
    'BaseListView',
    ]


class MorphListItemFlat(
        RecycleDataViewBehavior,
        MorphHoverBehavior,
        MorphRippleBehavior,
        MorphButtonBehavior,
        MorphDelegatedThemeBehavior,
        MorphColorThemeBehavior,
        MorphOverlayLayerBehavior,
        MorphInteractionLayerBehavior,
        MorphContentLayerBehavior,
        MorphIconLabelIconContainer,):
    """A single item within the MorphDropdownMenu widget.
    
    This widget represents a menu item with support for leading icon,
    text label, and trailing icon. It inherits from
    :class:`~morphui.uix.container.MorphIconLabelIconContainer` which
    provides the layout structure and child widget management.
    """

    focus: bool = BooleanProperty(False)
    """Indicates whether this list item is focused.

    This property determines if the list item is currently focused, 
    when pressing the keyboard navigation keys. A focused item
    typically receives keyboard input and may have a visual
    indication of its focused state.

    :attr:`focus` is a :class:`~kivy.properties.BooleanProperty` and
    defaults to `False`.
    """

    release_callback: Callable[[Any, int], None] | None = ObjectProperty(None)
    """Callback function invoked when this list item is released.

    This property holds a reference to a callback function that is
    called whenever this list item is released. The function should
    accept two parameters: the item data and the index of the item
    within the list.

    :attr:`release_callback` is an
    :class:`~kivy.properties.ObjectProperty` and defaults to `None`.
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
        MorphIconLabelIconContainer.default_config.copy() | dict(
            theme_color_bindings={
                'normal_surface_color': 'transparent_color',
                'normal_overlay_edge_color': 'outline_color',
                'normal_content_color': 'content_surface_color',},
            overlay_edge_width=dp(0.5),
            visible_edges=['bottom'],
            auto_size=(False, False),
            size_hint=(1, None),
            height=dp(35),
            ripple_duration_in_long=0.2,
            delegate_content_color=True,))

    def __init__(self, **kwargs) -> None:
        config = clean_config(self.default_config, kwargs)
        super().__init__(**config)
        self.delegated_children = [
            self.leading_widget,
            self.label_widget,
            self.trailing_widget,]

    def refresh_view_attrs(
            self,
            rv: RecycleView,
            index: int,
            data: Dict[str, Any]
            ) -> None:
        """Refreshes the view attributes of this menu item.

        Parameters
        ----------
        rv : RecycleView
            The RecycleView instance managing this menu item.
        index : int
            The index of this menu item within the RecycleView data.
        data : Dict[str, Any]
            The data list containing the attributes for all menu items.
        """
        super().refresh_view_attrs(rv, index, data)
        self.rv = rv
        self.rv_index = index
        self.refresh_auto_sizing()
        self.refresh_content()
        self.refresh_overlay()
        self.refresh_leading_widget()
        self.refresh_label_widget()
        self.refresh_trailing_widget()

    def on_release(self) -> None:
        """Handle the release event for this list item.

        This method is called when the list item is released. It
        invokes the `release_callback` function if it is defined,
        passing the item data and index as arguments.
        """
        if self.release_callback is not None:
            self.release_callback(self, self.rv_index)


class MorphToggleListItemFlat(
        MorphToggleButtonBehavior,
        MorphListItemFlat):
    """A toggleable list item within a MorphUI list view.

    This widget extends the base MorphListItemFlat to include toggle
    button behavior, allowing it to be used as a selectable item
    within a list. It supports active state management and can be
    grouped with other toggle items.
    """

    def refresh_view_attrs(
            self,
            rv: RecycleView,
            index: int,
            data: Dict[str, Any]
            ) -> None:
        """Refreshes the view attributes of this top list item.

        Parameters
        ----------
        rv : RecycleView
            The RecycleView instance managing this list item.
        index : int
            The index of this menu item within the RecycleView data.
        data : Dict[str, Any]
            The data list containing the attributes for all menu items.
        """
        super().refresh_view_attrs(rv, index, data)
        self.leading_widget.active = self.active


class MorphListLayout(
        MorphRecycleBoxLayout):
    """A layout for arranging index labels in a data view.

    This class extends the base data view layout and MorphRecycleBoxLayout
    to provide a vertical layout suitable for index labels.
    """
    
    default_config: Dict[str, Any] = dict(
        theme_color_bindings={
            'normal_surface_color': 'transparent_color',},
        orientation='vertical',
        auto_size=(False, True),
        size_hint_x=1,)
    """Default configuration for the MorphDataViewHeaderLayout."""

    def __init__(self, **kwargs) -> None:
        config = clean_config(self.default_config, kwargs)
        super().__init__(**config)


class BaseListView(
        MorphKeyPressBehavior,
        MorphIdentificationBehavior,
        RecycleView):
    """A base RecycleView subclass for displaying a list of items.

    This class serves as a foundation for list views used in various
    MorphUI components.
    """

    filter_value: Any = ObjectProperty('')
    """The current filter value used to filter displayed items.

    This property holds the value used to filter the list of items.
    Items that do not match this filter will be excluded from the
    displayed data. This property is used to dynamically manage the
    contents of the list view. Override the :meth:`should_filter_item`
    method to customize the filtering logic.

    :attr:`filter_value` is an :class:`~kivy.properties.ObjectProperty`
    and defaults to an empty string."""

    item_release_callback: Callable[[Any, int], None] | None = ObjectProperty(None)
    """Callback function invoked when an item is released.

    This property holds a reference to a callback function that is
    called whenever an item in the list is released. The function
    should accept two parameters: the item instance and the index of the
    item within the list. The item instance provides access to the
    item's properties and methods, allowing for customized handling of
    the release event.

    :attr:`item_release_callback` is an
    :class:`~kivy.properties.ObjectProperty` and defaults to `None`.
    """

    default_data: Dict[str, Any] = DictProperty({})
    """Default data attributes applied to each list item.

    This property holds a dictionary of default attributes that will
    be applied to each item in the list. When setting the `items`
    property, these default attributes will be merged with the item-
    specific attributes.

    :attr:`default_data` is a :class:`~kivy.properties.DictProperty`
    and defaults to an empty dictionary.
    """

    _source_items: List[Dict[str, Any]] = ListProperty([])
    """Internal storage for the full list of items before filtering.

    This property holds the complete list of items that can be displayed
    in the list view, prior to applying any filtering based on the
    current filter value. It is used internally to manage the list data.

    :attr:`_source_items` is a :class:`~kivy.properties.ListProperty`
    and defaults to an empty list.
    """

    def _get_items(self) -> List[Dict[str, Any]]:
        """Retrieve the list of items after applying the current filter.

        This method returns the list of items that should be displayed
        in the list view after filtering out items based on the current
        filter value.

        Returns
        -------
        List[Dict[str, Any]]
            A list of dictionaries representing the filtered list items.
        """
        return list(filter(
            lambda item: not self.should_filter_item(item),
            self._source_items))
    
    def _set_items(self, items: List[Dict[str, Any]]) -> None:
        """Set the list of items to be displayed in the list view.

        This method updates the internal storage of items and refreshes
        the displayed data in the RecycleView.

        Parameters
        ----------
        items : List[Dict[str, Any]]
            A list of dictionaries representing the items to be displayed
            in the list view.
        """
        self._source_items = [
            {   
                **self.default_data,
                **item_data,
                'release_callback': self.item_release_callback} 
            for item_data in items]
        self.data = self._get_items()

    items: List[Dict[str, Any]] = AliasProperty(
        _get_items,
        _set_items,
        bind=[
            '_source_items',
            'filter_value',
            'item_release_callback'])
    """The list of items to display in the list view.

    This property allows getting and setting the list of items. Each 
    item is represented as a dictionary of attributes. Setting this
    property updates the internal `_items` storage and refreshes the
    displayed data. Items that are filtered out based on the current
    `filter_value` will not be included in the displayed data. This
    property is used to dynamically manage the contents of the list
    view.

    :attr:`items` is an :class:`~kivy.properties.AliasProperty` and
    is bound to changes in the :attr:`_items` and :attr:`filter_value`
    properties.
    """

    default_config: Dict[str, Any] = dict(
        do_scroll_x=False,
        do_scroll_y=True,
        size_hint=(1, 1),
        bar_width=dp(4),
        scroll_type=['bars', 'content'],
        scroll_distance=dp(120),)
    """Default configuration for the BaseListView."""

    def __init__(self, **kwargs) -> None:
        """Initialize the list view component.

        This constructor applies the default configuration and
        initializes the base RecycleView functionality.
        
        Parameters
        ----------
        **kwargs : dict
            Additional keyword arguments to customize the list view.
        """
        config = clean_config(self.default_config, kwargs)
        super().__init__(**config)
        self.bind(items=self.refresh_data) # type: ignore
        self.refresh_data()

    def should_filter_item(self, item: Dict[str, Any]) -> bool:
        """Determine if a list item should be filtered out based on
        the current filter value.

        This method checks if the provided list item matches the
        filter criteria. If it does not match, the item is considered
        filtered out and will not be displayed in the list.
        Override this method to implement custom filtering logic.

        Parameters
        ----------
        item : Dict[str, Any]
            A dictionary representing a single list item.

        Returns
        -------
        bool
            `True` if the item should be filtered out, `False`
            otherwise.
        """
        if not self.filter_value:
            return False
        
        filter_val = str(self.filter_value).lower()
        item_text = str(item.get('text', item.get('label_text', ''))).lower()
        return filter_val not in item_text
    
    def refresh_data(self, *args) -> None:
        """Refresh the displayed data in the list view.

        This method updates the RecycleView's data based on the
        current list of items after applying any filtering. First, it
        ensures that the internal `_items` storage is up to date,
        then it refreshes the displayed data accordingly.
        """
        self._set_items(self._source_items)
        self.data = self.items
