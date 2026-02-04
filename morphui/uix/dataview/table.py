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
        visible_edges=['right', 'bottom'],
        overlay_edge_width=dp(0.5),
        theme_color_bindings={
            'normal_surface_color': 'transparent_color',
            'normal_overlay_edge_color': 'outline_color'},)
    
    def __init__(self, **kwargs) -> None:
        config = clean_config(self.default_config, kwargs)
        super().__init__(**config)


class BottomLeftCorner(
        MorphIdentificationBehavior,
        Widget):
    """An empty cell for the bottom-left corner of the data view table."""

    default_config: Dict[str, Any] = dict(
        size_hint=(None, None),)
    
    def __init__(self, **kwargs) -> None:
        config = clean_config(self.default_config, kwargs)
        super().__init__(**config)


class MorphDataViewTable(MorphGridLayout):
    """A data view table component with MorphUI styling and behavior.
    
    This class provides a structured data view table with header, index,
    body, and navigation components. It supports pagination and
    customizable styling and behavior.
    
    Examples
    --------
    Create a simple data view table with sample data:
    ```python
    from morphui.app import MorphApp
    from morphui.uix.dataview.table import MorphDataViewTable
    class TestApp(MorphApp):
        def build(self):
            table = MorphDataViewTable(
                rows_per_page=5,
                values=[
                    ['Alice', '24', 'Engineer'],
                    ['Bob', '30', 'Designer'],
                    ['Charlie', '28', 'Teacher'],
                    ['David', '35', 'Manager'],
                    ['Eve', '22', 'Intern'],
                    ['Frank', '29', 'Developer'],],
                column_names=['Name', 'Age', 'Occupation'],)
            return table
    TestApp().run()
    ```

    Create a larger data view table with more rows and custom row names:
    ```python
    from kivy.clock import Clock
    from morphui.app import MorphApp
    from morphui.uix.dataview import MorphDataViewTable

    class MyApp(MorphApp):
        def build(self) -> MorphDataViewTable:
            self.theme_manager.theme_mode = 'Dark'
            self.theme_manager.seed_color = 'morphui_teal'

            self.table = MorphDataViewTable(
                rows_per_page=13,)

            Clock.schedule_once(self.set_data, 0)
            return self.table

        def set_data(self, *args) -> None:
            self.table.column_names = [
                'Name', 'Age', 'Occupation', 'Country', 'Email', 'Phone', 'Company',
                'Position', 'Department', 'Start Date', 'End Date', 'Status',
                'Notes', 'Salary', 'Bonus', 'Manager', 'Team', 'Location',
                'Project', 'Task', 'Deadline', 'Priority', 'Comments', 'Feedback',
                'Rating', 'Score', 'Level', 'Experience', 'Skills', 'Certifications',
                'Languages', 'Hobbies', 'Interests', 'Social Media', 'Website',]
            self.table.values = [[
                f'Name {i}',
                str(20 + i % 30),
                'Occupation ' + str(i % 10),
                'Country ' + str(i % 5),
                'email' + str(i) + '@example.com',
                '123-456-7890',
                'Company ' + str(i % 7),
                'Position ' + str(i % 8),
                'Department ' + str(i % 6),
                '2020-01-01',
                '2023-12-31',
                'Active' if i % 2 == 0 else 'Inactive',
                'Notes for entry ' + str(i),
                str(50000 + (i % 10) * 5000),
                str(5000 + (i % 5) * 1000),
                'Manager ' + str(i % 4),
                'Team ' + str(i % 3),
                'Location ' + str(i % 6),
                'Project ' + str(i % 9),
                'Task ' + str(i % 12),
                '2023-12-' + str(10 + i % 20).zfill(2),
                'High' if i % 3 == 0 else 'Low',
                'Comments for entry ' + str(i),
                'Feedback for entry ' + str(i),
                str(1 + i % 5),
                str(50 + i % 50),
                str(1 + i % 4),
                str(1 + i % 10) + ' years',
                'Skill ' + str(i % 15),
                'Certification ' + str(i % 7),
                'Language ' + str(i % 5),
                'Hobby ' + str(i % 8),
                'Interest ' + str(i % 6),
                'http://socialmedia' + str(i) + '.com',
                'http://website' + str(i) + '.com',
                ]
                for i in range(1, 51)]
            self.table.row_names = [f'Row {i}' for i in range(1, 51)]

    if __name__ == "__main__":
        MyApp().run()
    """

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

    def _get_is_empty(self) -> bool:
        """Check if the data view table has no data.

        Returns
        -------
        bool
            `True` if the table has no values, column names, or row
            names; `False` otherwise.
        """
        return not any((
            bool(self.values),
            bool(self.column_names),
            bool(self.row_names)))

    is_empty: bool = AliasProperty(
        _get_is_empty,
        None,
        bind=['values', 'column_names', 'row_names'])
    """Flag indicating whether the data view table is empty (read-only).

    This property returns `True` if the table has no values, column
    names, or row names; otherwise, it returns `False`.

    :attr:`is_empty` is an :class:`~kivy.properties.AliasProperty` and
    is bound to changes in `values`, `column_names`, and `row_names`.
    """

    header: MorphDataViewHeader
    """The header component of the data view table."""

    index: MorphDataViewIndex
    """The index component of the data view table."""

    body: MorphDataViewBody
    """The body component of the data view table."""

    navigation: MorphDataViewNavigation
    """The navigation component of the data view table."""

    top_left: TopLeftCorner
    """The top-left corner component of the data view table."""

    bottom_left: BottomLeftCorner
    """The bottom-left corner component of the data view table."""

    _top_left_visible_edges: List[str]
    """Storage of visible edges for the top-left corner component."""

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
        self.top_left = TopLeftCorner()
        self.bottom_left = BottomLeftCorner()
        
        super().__init__(
            self.top_left,
            self.header,
            self.index,
            self.body,
            self.bottom_left,
            self.navigation,
            **config)
        self._top_left_visible_edges = self.top_left.visible_edges.copy()
        self.bind(
            page_values=self.body.setter('values'),
            page_rows=self.index.setter('row_names'),
            values=self.update_chunked_values,
            rows_per_page=self.update_chunked_values,
            is_empty=self._update_view,)
        
        self.index.bind(width=self.top_left.setter('width'))
        self.top_left.bind(width=self.bottom_left.setter('width')) # type: ignore
        self.header.bind(height=self.top_left.setter('height'))
        self.navigation.bind(
            height=self.bottom_left.setter('height'), # type: ignore
            current_page=self._update_view,)
        self.top_left.size = (self.index.width, self.header.height)
        self.bottom_left.size = (self.index.width, self.navigation.height)
        self.update_chunked_values()
        self.top_left.refresh_overlay()

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
        """Update the body and index views based on current page values.
        
        This method refreshes the body and index components of the
        data view table with the values and row names corresponding
        to the current page. It also manages the visibility of the
        top-left corner component based on whether the table is empty.
        """
        self.body.values = self.page_values
        self.index.row_names = self.page_rows

        if self.is_empty:
            self._top_left_visible_edges = self.top_left.visible_edges.copy()
            self.top_left.visible_edges = []
        else:
            self.top_left.visible_edges = self._top_left_visible_edges.copy()
