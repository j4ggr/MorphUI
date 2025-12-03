from textwrap import dedent

from typing import Any
from typing import Dict
from typing import List
from typing import Sequence

from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import AliasProperty
from kivy.properties import ObjectProperty
from kivy.properties import NumericProperty
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
        size_hint=(1, None),
        auto_size=(True, True),
        auto_size_once=True,
        visible_edges=['right', 'bottom'],)
    """Default configuration for the MorphDataViewBodyLabel."""


class MorphBodyColumnLayout(
        BaseDataViewLayout,
        RecycleDataViewBehavior,
        MorphRecycleBoxLayout):
    """A layout for arranging body cells in a single column.

    This class extends the base data view layout and 
    :class:`~morphui.uix.recycleboxlayout.MorphRecycleBoxLayout`
    to provide a vertical layout suitable for body cells.
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
    
    def _get_cell_type(self) -> type:
        """Return the type of cell label that this layout manages."""
        return MorphDataViewBodyLabel
    
    def _get_values(self) -> List[str]:
        """Get the current values in the column as a list of strings.

        This method constructs a list representing the values of the
        body cells in this column.
        """
        return [child.text for child in reversed(self.children)]
    
    def _set_values(self, values: Sequence[Any]) -> None:
        """Set the values of the column from a list of strings.

        This method takes a list representing the desired values for
        the body cells in this column and updates the data accordingly.
        """
        cell_type = self._get_cell_type()
        self.cells = tuple(map(lambda v: cell_type(text=str(v)), values))

    values: Sequence[str] = AliasProperty(
        _get_values,
        _set_values,
        bind=['children'],)
    """List of values displayed in the column.

    This property allows getting and setting the values of the body
    cells in this column. When set, it updates the cells accordingly.

    :attr:`values` is an :class:`~kivy.properties.AliasProperty` and is
    bound to changes in :attr:`children`.
    """
    
    default_config: Dict[str, Any] = dict(
        theme_color_bindings={
            'normal_surface_color': 'surface_color'},
        orientation='vertical',
        auto_size=(False, True),
        size_hint_x=None,
        width=dp(85),)
    """Default configuration for the MorphBodyColumnLayout."""

    def __init__(self, **kwargs) -> None:
        config = clean_config(self.default_config, kwargs)
        super().__init__(**config)

    def refresh_view_attrs(
            self,
            rv: RecycleView,
            index: int,
            data: List[Dict[str, Any]]
            ) -> None:
        """Refresh the view attributes when the data changes.
        
        This method is called by the RecycleView framework to update
        the view's attributes based on the provided data.
        
        Parameters
        ----------
        rv : RecycleView
            The RecycleView instance managing this view.
        index : int
            The index of this view in the RecycleView data.
        data : List[Dict[str, Any]]
            The data dictionary for this view.
        """
        self.rv = rv
        self.rv_index = index
        self.refresh_auto_sizing()
        return super().refresh_view_attrs(rv, index, data)

class MorphDataViewBodyLayout(
        BaseDataViewLayout,
        MorphRecycleBoxLayout):
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
        orientation='horizontal',
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
            viewclass: 'MorphBodyColumnLayout'
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

    def _get_values(self) -> List[List[str]]:
        """Get the current values in the body as a 2D list.

        This method constructs a list of lists representing the
        values of the body cells, organized by rows and columns.
        The outer list represents columns, and each inner list
        represents the values in that column. This method is used 
        internally for the :attr:`values` property.
        """
        if not self.layout:
            return []
        return [c.values for c in self.layout.children[::-1]]

    def _set_values(self, values: Sequence[Sequence[Any]]) -> None:
        """Set the values of the body from a 2D list.

        This method takes a list of lists representing the desired
        values for the body cells and updates the data accordingly.
        The outer list represents columns, and each inner list
        represents the values in that column. This method is used
        internally for the :attr:`values` property.
        """
        self.data = [{'values': list(map(str, col))} for col in values]

    values: List[List[str]] = AliasProperty(
        _get_values,
        _set_values,
        bind=['data'],)
    """2D list of values displayed in the body.

    This property allows getting and setting the values of the body
    cells in a tabular format. When set, it updates the body's data
    accordingly. The outer list represents columns, and each inner
    list represents the values in that column.

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
        config = clean_config(self.default_config, kwargs)
        super().__init__(**config)
