from typing import Any
from typing import Dict
from typing import List

from kivy.metrics import dp
from kivy.properties import ListProperty
from kivy.properties import AliasProperty
from kivy.properties import BoundedNumericProperty
from kivy.uix.widget import Widget

from morphui.utils import clean_config
from morphui.uix.dataview import MorphDataViewBody
from morphui.uix.dataview import MorphDataViewIndex
from morphui.uix.dataview import MorphDataViewHeader
from morphui.uix.dataview import MorphDataViewNavigation
from morphui.uix.behaviors import MorphThemeBehavior
from morphui.uix.behaviors import MorphSurfaceLayerBehavior
from morphui.uix.behaviors import MorphOverlayLayerBehavior
from morphui.uix.behaviors import MorphIdentificationBehavior
from morphui.uix.gridlayout import MorphGridLayout


__all__ = [
    'MorphDataViewTable',]


class TopLeftCorner(
        MorphIdentificationBehavior,
        MorphThemeBehavior,
        MorphOverlayLayerBehavior,
        MorphSurfaceLayerBehavior,
        Widget):
    """An empty cell for the top-left corner of the data view table."""

    default_config: Dict[str, Any] = dict(
        size_hint=(None, None),
        identity='top_left',
        visible_edges=['right', 'bottom'],
        overlay_edge_width=dp(0.5),
        theme_color_bindings={
            'normal_surface_color': 'surface_container_highest_color',
            'normal_overlay_edge_color': 'outline_color'},)
    
    def __init__(self, **kwargs) -> None:
        config = clean_config(self.default_config, kwargs)
        super().__init__(**config)


class BottomLeftCorner(
        MorphIdentificationBehavior,
        Widget):
    """An empty cell for the bottom-left corner of the data view table."""

    default_config: Dict[str, Any] = dict(
        size_hint=(None, None),
        identity='bottom_left',)
    
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

    def _get_current_page(self) -> int:
        """Retrieve the current page number from the navigation component.

        Returns
        -------
        int
            The current page number being displayed in the data view table.
        """
        return self.navigation.current_page
    
    def _set_current_page(self, page: int) -> None:
        """Set the current page number in the navigation component.

        Parameters
        ----------
        page : int
            The page number to set as the current page in the data view table.
        """
        if page < 1 or page > len(self.chunked_values):
            return
        
        if self.navigation.current_page != page:
            self.navigation.current_page = page
        self.navigation.total_pages = len(self.chunked_values)

    current_page: int = AliasProperty(
        _get_current_page,
        _set_current_page,
        bind=['chunked_values'])
    """The current page number being displayed in the data view table.

    This property allows getting and setting the current page number
    displayed in the data view table. It is synchronized with the
    navigation component.

    :attr:`current_page` is an :class:`~kivy.properties.AliasProperty`
    and is bound to changes in `chunked_values`."""

    values: List[List] = ListProperty([])
    """2D list of values holding the data for the table.

    This property allows getting and setting the values of the body
    cells in a tabular format. When set, it updates the body's data
    accordingly. The outer list represents rows, and each inner list
    represents the values in that row.

    :attr:`values` is an :class:`~kivy.properties.AliasProperty` and 
    defaults to an empty list."""

    column_names: List[str] = AliasProperty(
        lambda self: self.header.column_names,
        lambda self, names: setattr(self.header, 'column_names', names))
    """List of column names for the data view table.

    This property holds the names of the columns displayed in the
    header of the table. It can be set to customize the column headers.

    :attr:`column_names` is a :class:`~kivy.properties.ListProperty`
    and defaults to an empty list."""

    row_names: List[str] = ListProperty([])
    """List of row names for the data view table.

    This property holds the names of the rows displayed in the
    index of the table. It can be set to customize the row headers.
    
    :attr:`row_names` is a :class:`~kivy.properties.ListProperty`
    and defaults to an empty list."""

    chunked_values: List[List[List[str]]] = ListProperty([])
    """List of values chunks based on rows_per_page.

    This property holds the values divided into chunks, where each chunk
    corresponds to a page of values containing the specified number of
    rows.

    :attr:`chunked_values` is an :class:`~kivy.properties.AliasProperty`
    and is bound to changes in `values` and `rows_per_page`."""

    def _get_page_values(self) -> List[List[str]]:
        """Retrieve the values for the current page in the table.
        
        Returns
        -------
        List[List[str]]
            A 2D list of values for the current page being displayed
            in the data view table.
        """
        if not self.chunked_values:
            return []
        return self.chunked_values[self.current_page - 1]

    page_values: List[List[str]] = AliasProperty(
        _get_page_values,
        bind=['chunked_values', 'current_page'])
    """2D list of values for the current page in the table (read-only).

    This property provides access to the values currently displayed in
    the body cells of the table for the current page.

    :attr:`page_values` is an :class:`~kivy.properties.AliasProperty`
    and is bound to changes in `chunked_values` and `current_page`."""

    def _get_page_rows(self) -> List[str]:
        """Retrieve the row names for the current page in the table.

        The method calculates the appropriate slice of row names based
        on the current page and the number of rows per page.
        """
        if not self.row_names:
            row_names = list(map(str, range(1, len(self.values) + 1)))
        else:
            row_names = self.row_names
        start = (self.current_page - 1) * self.rows_per_page
        end = min(start + self.rows_per_page, len(row_names))
        return row_names[start:end]
    
    page_rows: List[str] = AliasProperty(
        _get_page_rows,
        bind=['row_names', 'current_page', 'rows_per_page'])
    """List of row names for the current page in the table (read-only).

    This property provides access to the row names currently displayed
    in the index for the current page.

    :attr:`page_rows` is an :class:`~kivy.properties.AliasProperty`
    and is bound to changes in `row_names`, `current_page`, and
    `rows_per_page`."""

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
            TopLeftCorner(),
            self.header,
            self.index,
            self.body,
            BottomLeftCorner(),
            self.navigation,
            **config)
        
        self.bind(
            page_values=self.body.setter('values'),
            page_rows=self.index.setter('row_names'),
            values=self.update_chunked_values,
            rows_per_page=self.update_chunked_values,)
        
        top_left = self.identities.top_left
        bottom_left = self.identities.bottom_left
        self.index.bind(width=top_left.setter('width'))
        top_left.bind(width=bottom_left.setter('width'))
        self.header.bind(height=top_left.setter('height'))
        self.navigation.bind(
            height=bottom_left.setter('height'),
            current_page=self.setter('current_page'),)
        top_left.size = (self.index.width, self.header.height)
        bottom_left.size = (self.index.width, self.navigation.height)
        self.update_chunked_values()
        top_left.refresh_overlay()

    def update_chunked_values(self, *args) -> None:
        """Set the chunked values based on rows_per_page.

        This method divides the full values into chunks according to
        the specified number of rows per page. Each chunk represents
        a page of data in the table. It also updates the navigation
        component with the current page and total pages.

        This method is automatically called when the `values` or
        `rows_per_page` properties change.
        """
        chunked = []
        values = self.values
        rpp = self.rows_per_page
        n_values = len(values)
        for start in range(0, n_values, rpp):
            end = min(start + rpp, n_values)
            chunked.append(values[start:end])
        self.chunked_values = chunked
        self.navigation.current_page = 1
        self.navigation.total_pages = len(chunked)

    def _update_view(self, *args) -> None:
        """Update the body and index views based on current page values."""
        self.body.values = self.page_values
        self.index.row_names = self.page_rows
