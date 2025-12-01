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
from morphui.uix.label import BaseLabel
from morphui.uix.behaviors import MorphThemeBehavior
from morphui.uix.behaviors import MorphScrollSyncBehavior
from morphui.uix.behaviors import MorphAutoSizingBehavior
from morphui.uix.behaviors import MorphContentLayerBehavior
from morphui.uix.behaviors import MorphOverlayLayerBehavior
from morphui.uix.recycleboxlayout import MorphRecycleBoxLayout


__all__ = [
    'MorphDataViewIndexLabel',
    'MorphDataViewIndexLayout',
    'MorphDataViewIndex',]


class MorphDataViewIndexLabel(
        RecycleDataViewBehavior,
        MorphOverlayLayerBehavior,
        MorphThemeBehavior,
        MorphContentLayerBehavior,
        MorphAutoSizingBehavior,
        BaseLabel,):
    """A label widget designed for use as an index label in a data view.

    This class combines several MorphUI behaviors to provide a themed,
    auto-sizing label with content and overlay layer capabilities.
    It is intended to be used within a data view layout to display
    index information for rows or items.
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
        auto_size=(False, True),
        auto_size_once=True,
        visible_edges=['right', 'bottom'],)
    """Default configuration for the MorphDataViewHeaderLabel."""

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
        self.refresh_content()
        self.refresh_overlay()
        return super().refresh_view_attrs(rv, index, data)


class MorphDataViewIndexLayout(
        MorphRecycleBoxLayout):

    cells: List[MorphDataViewIndexLabel] = AliasProperty(
        lambda self: [
            child for child in self.children
            if isinstance(child, MorphDataViewIndexLabel)],
        None,
        bind=('children',))
    """List of index label widgets managed by this layout (read-only).

    This property returns a list of all child widgets that are instances
    of :class:`MorphDataViewIndexLabel`. It allows easy access to the
    index labels contained within the layout.

    :attr:`cells` is an :class:`~kivy.properties.AliasProperty`.
    and is bound to changes in the `children` property.
    """
    
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
    
    def on_cells(
            self, instance: Any, cells: List[MorphDataViewIndexLabel]) -> None:
        """Called when the list of header label widgets changes.

        This method is triggered whenever the `cells` property changes,
        allowing for any necessary updates or refreshes to the header
        labels.
        """
        for cell in cells:
            index = cell.rv_index
            rv = cell.rv
            cell.refresh_view_attrs(rv, index, rv.data[index])


class MorphDataViewIndex(
        MorphScrollSyncBehavior,
        RecycleView):
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

    row_names: List[str] = AliasProperty(
        _get_row_names,
        _set_row_names)
    """List of row names displayed in the index.

    This property allows getting and setting the row names for the
    index. When set, it updates the index's data accordingly.
    
    :attr:`row_names` is an :class:`~kivy.properties.AliasProperty`.
    """
    
    default_config: Dict[str, Any] = dict(
        do_scroll_x=False,
        do_scroll_y=True,
        size_hint=(None, 1),
        bar_width=0,)
    """Default configuration for the :class:`MorphDataViewIndex`."""

    def __init__(self, **kwargs) -> None:
        config = clean_config(self.default_config, kwargs)
        super().__init__(**config)
        self.layout.bind(width=self.setter('width'))
        self.width = self.layout.width
