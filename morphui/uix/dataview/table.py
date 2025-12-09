from typing import Any
from typing import Dict
from typing import List

from kivy.metrics import dp
from kivy.properties import ListProperty
from kivy.properties import BoundedNumericProperty
from kivy.uix.widget import Widget

from morphui.utils import clean_config
from morphui.uix.dataview import MorphDataViewBody
from morphui.uix.dataview import MorphDataViewIndex
from morphui.uix.dataview import MorphDataViewHeader
from morphui.uix.dataview import MorphDataViewNavigation
from morphui.uix.behaviors import MorphThemeBehavior
from morphui.uix.behaviors import MorphOverlayLayerBehavior
from morphui.uix.behaviors import MorphIdentificationBehavior
from morphui.uix.gridlayout import MorphGridLayout


__all__ = [
    'MorphDataViewTable',]


class EmptyCell(
        MorphIdentificationBehavior,
        MorphThemeBehavior,
        MorphOverlayLayerBehavior,
        Widget):
    default_config: Dict[str, Any] = dict(
        size_hint=(None, None),
        overlay_edge_width=dp(0.5),)
    
    def __init__(self, **kwargs) -> None:
        config = clean_config(self.default_config, kwargs)
        super().__init__(**config)



class MorphDataViewTable(MorphGridLayout):
    """A data view table component with MorphUI styling and behavior."""

    rows_per_page: int = BoundedNumericProperty(
        10, min=1, errorvalue=1)
    """The number of rows to display per page in the data view table.
    
    Setting this property controls how many rows of data are shown
    on each page of the table. It must be at least `1`.
    
    :attr:`rows_per_page` is a
    :class:`~kivy.properties.BoundedNumericProperty` and defaults to 
    `10`."""

    values: List[List] = ListProperty([])
    """2D list of values holding the data for the table.

    This property allows getting and setting the values of the body
    cells in a tabular format. When set, it updates the body's data
    accordingly. The outer list represents rows, and each inner list
    represents the values in that row.

    :attr:`values` is an :class:`~kivy.properties.AliasProperty` and 
    defaults to an empty list."""

    header: MorphDataViewHeader
    """The header component of the data view table."""

    index: MorphDataViewIndex
    """The index component of the data view table."""

    body: MorphDataViewBody
    """The body component of the data view table."""

    navigation: MorphDataViewNavigation
    """The navigation component of the data view table."""

    default_config = dict(
        cols=2,
        size_hint=(1, 1),
        spacing=0,
        padding=0,
        theme_color_bindings={
            'normal_surface_color': 'surface_color',  
        },)
    """Default configuration for the MorphDataViewTable."""

    def __init__(
            self,
            kw_header: Dict[str, Any] = {},
            kw_index: Dict[str, Any] = {},
            kw_body: Dict[str, Any] = {},
            kw_navigation: Dict[str, Any] = {},
            **kwargs) -> None:
        """Initialize the data view table component."""
        config = clean_config(self.default_config, kwargs)
        self.header =MorphDataViewHeader(
            identity='header', **kw_header)
        self.index = MorphDataViewIndex(
            identity='index', **kw_index)
        self.body = MorphDataViewBody(
            identity='body', header=self.header, index=self.index, **kw_body)
        self.navigation = MorphDataViewNavigation(
            identity='navigation', **kw_navigation)
        
        super().__init__(
            EmptyCell(identity='top_left', visible_edges=['right', 'bottom']),
            self.header,
            self.index,
            self.body,
            EmptyCell(identity='bottom_left', visible_edges=['top']),
            self.navigation,
            **config)
        
        top_left = self.identities.top_left
        bottom_left = self.identities.bottom_left
        self.index.bind(width=top_left.setter('width'))
        self.index.bind(width=bottom_left.setter('width'))
        self.header.bind(height=top_left.setter('height'))
        top_left.size = (self.index.width, self.header.height)
        bottom_left.size = (self.index.width, self.header.height)