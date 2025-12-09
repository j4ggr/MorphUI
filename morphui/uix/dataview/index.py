from textwrap import dedent

from typing import Any
from typing import Dict
from typing import List
from typing import Sequence

from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import AliasProperty
from kivy.properties import ObjectProperty

from morphui.utils import clean_config
from morphui.uix.dataview.base import BaseDataViewLabel
from morphui.uix.dataview.base import BaseDataViewLayout
from morphui.uix.dataview.base import BaseDataView
from morphui.uix.recycleboxlayout import MorphRecycleBoxLayout


__all__ = [
    'MorphDataViewIndexLabel',
    'MorphDataViewIndexLayout',
    'MorphDataViewIndex',]


class MorphDataViewIndexLabel(BaseDataViewLabel):
    """A label widget designed for use as an index label in a data view.

    This class extends the base data view label to provide specific
    styling and behavior for index labels.
    """

    default_config: Dict[str, Any] = dict(
        theme_color_bindings=dict(
            normal_content_color='content_surface_color',
            normal_overlay_edge_color='outline_color',),
        typography_role='Label',
        typography_size='medium',
        typography_weight='Regular',
        halign='right',
        valign='center',
        padding=[dp(8), dp(4)],
        overlay_edge_width=dp(1),
        size_hint=(1, None),
        auto_size=(False, True),
        auto_size_once=True,
        visible_edges=['right', 'bottom'],)
    """Default configuration for the MorphDataViewIndexLabel."""


class MorphDataViewIndexLayout(
        BaseDataViewLayout,
        MorphRecycleBoxLayout):
    """A layout for arranging index labels in a data view.

    This class extends the base data view layout and MorphRecycleBoxLayout
    to provide a vertical layout suitable for index labels.
    """
    
    def _get_cell_type(self) -> type:
        """Return the type of cell label that this layout manages."""
        return MorphDataViewIndexLabel
    
    default_config: Dict[str, Any] = dict(
        theme_color_bindings={
            'normal_surface_color': 'surface_color'},
        orientation='vertical',
        auto_size=(False, True),
        size_hint_x=None,
        width=dp(85),)
    """Default configuration for the MorphDataViewHeaderLayout."""

    def __init__(self, **kwargs) -> None:
        config = clean_config(self.default_config, kwargs)
        super().__init__(**config)


class MorphDataViewIndex(BaseDataView):
    """A scrollable index for data views, synchronized with the main
    data view.

    This class provides an index component for data views that can
    scroll vertically in sync with the associated data view. It uses
    a custom layout manager to arrange index labels and supports
    dynamic row naming.

    Example
    -------
    ```python
    from morphui.app import MorphApp
    from morphui.uix.dataview.index import MorphDataViewIndex

    class MyApp(MorphApp):
        def build(self) -> MorphDataViewIndex:
            self.theme_manager.theme_mode = 'Dark'
            self.theme_manager.seed_color = 'morphui_teal'
            index = MorphDataViewIndex()
            index.row_names = [f'Row {i}' for i in range(1, 51)]
            return index
    MyApp().run()
    ```
    """
    
    Builder.load_string(dedent('''
        <MorphDataViewIndex>:
            viewclass: 'MorphDataViewIndexLabel'
            layout: layout
            MorphDataViewIndexLayout:
                id: layout
        '''))
    
    layout: MorphDataViewIndexLayout = ObjectProperty()
    """The layout manager for the index, responsible for arranging
    the index labels.

    This property is automatically set to an instance of
    :class:`MorphDataViewIndexLayout` defined in the KV string.

    :attr:`layout` is a :class:`~kivy.properties.ObjectProperty`.
    """

    def _get_row_names(self) -> List[str]:
        """Retrieve the list of row names from the index data.

        Returns
        -------
        List[str]
            A list of row names extracted from the index's data.
        """
        return [item.get('text', '') for item in self.data]
    
    def _set_row_names(self, names: Sequence) -> None:
        """Set the row names for the index.

        This method updates the index's data to reflect the provided
        row names.

        Parameters
        ----------
        names : Sequence
            A sequence representing the row names to be displayed in 
            the index.
        """
        self.data = [
            {'text': str(n), **MorphDataViewIndexLabel.default_config}
            for n in names]
        self.dispatch('on_rows_updated')

    row_names: List[str] = AliasProperty(
        _get_row_names,
        _set_row_names,
        bind=['data'])
    """List of row names displayed in the index.

    This property allows getting and setting the row names for the
    index. When set, it updates the index's data accordingly.
    
    :attr:`row_names` is an :class:`~kivy.properties.AliasProperty` and
    is bound to changes in the `data` property.
    """
    
    default_config: Dict[str, Any] = dict(
        do_scroll_x=False,
        do_scroll_y=True,
        size_hint=(None, 1),
        bar_width=0,)
    """Default configuration for the :class:`MorphDataViewIndex`."""

    def __init__(self, **kwargs) -> None:
        self.register_event_type('on_rows_updated')
        config = clean_config(self.default_config, kwargs)
        super().__init__(**config)
        self.layout.bind(width=self.setter('width'))
        self.width = self.layout.width

    def on_rows_updated(self, *args) -> None:
        """Event handler called when the rows are updated.

        This event is dispatched whenever the row names are changed,
        allowing for custom behavior to be implemented in response to
        row updates.
        """
        pass