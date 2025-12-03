from textwrap import dedent

from typing import Any
from typing import Dict
from typing import List
from typing import Sequence

from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import AliasProperty
from kivy.properties import ObjectProperty
from kivy.properties import ListProperty
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.views import RecycleDataViewBehavior

from morphui.utils import clean_config
from morphui.uix.dataview.base import BaseDataViewLabel
from morphui.uix.dataview.base import BaseDataViewLayout
from morphui.uix.dataview.base import BaseDataView
from morphui.uix.recycleboxlayout import MorphRecycleBoxLayout
from morphui.uix.recyclegridlayout import MorphRecycleGridLayout


__all__ = [
    'MorphDataViewBodyLabel',
    'MorphDataViewBodyLayout',
    'MorphDataViewBody',]


class MorphDataViewBodyLabel(BaseDataViewLabel):
    """A label widget designed for use as a body cell in a data view.

    This class extends the base data view label to provide specific
    styling and behavior for body cells.
    """
    
    default_config: Dict[str, Any] = dict(
        theme_color_bindings=dict(
            normal_content_color='content_surface_color',
            normal_overlay_edge_color='outline_color',),
        typography_role='Label',
        typography_size='medium',
        typography_weight='Regular',
        halign='left',
        valign='center',
        padding=[dp(8), dp(4)],
        overlay_edge_width=dp(1),
        size_hint=(None, None),
        auto_size=(True, True),
        auto_size_once=True,
        visible_edges=['right', 'bottom'],)
    """Default configuration for the MorphDataViewBodyLabel."""


class MorphDataViewBodyLayout(
        BaseDataViewLayout,
        MorphRecycleGridLayout):
    """A layout for arranging body cells in a data view.

    This class extends the base data view layout and MorphRecycleGridLayout
    to provide a grid layout suitable for body cells.
    """
    
    def _get_cell_type(self) -> type:
        """Return the type of cell label that this layout manages."""
        return MorphDataViewBodyLabel

    default_config: Dict[str, Any] = dict(
        theme_color_bindings={
            'normal_surface_color': 'surface_color'},
        auto_size=(True, True),)
    """Default configuration for the MorphDataViewBodyLayout."""

    def __init__(self, **kwargs) -> None:
        config = clean_config(self.default_config, kwargs)
        super().__init__(**config)


class MorphDataViewBody(BaseDataView):
    """A RecycleView designed to serve as the body of a data view.

    This class extends the base data view to provide a body component
    suitable for displaying tabular data in a data view.
    """
    
    Builder.load_string(dedent('''
        <MorphDataViewBody>:
            viewclass: 'MorphDataViewBodyLabel'
            layout: layout
            MorphDataViewBodyLayout:
                id: layout
        '''))
    
    layout: MorphDataViewBodyLayout = ObjectProperty(None)
    """The layout managing the body cells, responsible for their 
    arrangement and sizing.

    This property is automatically set to the internal layout instance.
    :attr:`layout` is a :class:`~kivy.properties.ObjectProperty`
    and defaults to `None`.
    """

    column_widths: List[float] = ListProperty([])
    """List of widths for each column in the body.
    
    This property defines the widths of each column in the body. The
    number of widths should correspond to the number of columns
    displayed.
    
    :attr:`column_widths` is a :class:`~kivy.properties.ListProperty`
    and defaults to an empty list."""

    row_heights: List[float] = ListProperty([])
    """List of heights for each row in the body.
    
    This property defines the heights of each row in the body. The
    number of heights should correspond to the number of rows displayed.
    
    :attr:`row_heights` is a :class:`~kivy.properties.ListProperty`
    and defaults to an empty list."""

    def _get_values(self) -> List[List[str]]:
        """Get the current values in the body as a 2D list.

        This method constructs a list of lists representing the values
        of the body cells, organized by rows and columns. The outer list
        represents rows, and each inner list represents the values in
        that row. This method is used internally for the 
        :attr:`values` property.
        """
        if not self.layout:
            return []
        return [c.values for c in self.layout.children[::-1]]

    def _set_values(self, values: Sequence[Sequence[Any]]) -> None:
        """Set the values of the body from a 2D list.

        This method takes a list of lists representing the desired
        values for the body cells and updates the data accordingly. The
        outer list represents rows, and each inner list represents the
        values in that row. This method is used internally for the
        :attr:`values` property.
        """
        n_rows = len(values)
        n_cols = max(len(row) for row in values) if values else 0

        if len(self.column_widths) == n_cols:
            widths = self.column_widths
        else:
            widths = [dp(100)] * n_cols
        
        if len(self.row_heights) == n_rows:
            heights = self.row_heights
        else:
            heights = [dp(40)] * n_rows

        self.layout.cols = n_cols
        self.data = [
            {'text': str(value), 'size': (w, h)} 
            for w, row in zip(widths, values)
            for h, value in zip(heights, row)]
        self.dispatch('on_values_updated')

    values: List[List[str]] = AliasProperty(
        _get_values,
        _set_values,
        bind=['data'],)
    """2D list of values displayed in the body.

    This property allows getting and setting the values of the body
    cells in a tabular format. When set, it updates the body's data
    accordingly. The outer list represents rows, and each inner list
    represents the values in that row.

    :attr:`values` is an :class:`~kivy.properties.AliasProperty` and is
    bound to changes in :attr:`children`.
    """

    default_config: Dict[str, Any] = dict(
        do_scroll_x=True,
        do_scroll_y=True,
        size_hint=(1, 1),
        bar_width=dp(4),)
    """Default configuration for the MorphDataViewBody."""
    
    def __init__(self, **kwargs) -> None:
        self.register_event_type('on_values_updated')
        config = clean_config(self.default_config, kwargs)
        super().__init__(**config)

    def on_values_updated(self, *args) -> None:
        """Event handler called when the values in the body are updated.

        This method is triggered whenever the `values` property is set
        and can be overridden to perform additional actions when the
        body data changes.
        """
        pass