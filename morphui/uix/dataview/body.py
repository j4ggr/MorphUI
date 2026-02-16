from textwrap import dedent

from typing import Any
from typing import Dict
from typing import List
from typing import Sequence

from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import AliasProperty
from kivy.properties import ObjectProperty
from kivy.uix.recycleview import RecycleView

from morphui.uix.dataview import BaseDataView
from morphui.uix.dataview import BaseDataViewLabel
from morphui.uix.dataview import MorphDataViewIndex
from morphui.uix.dataview import MorphDataViewHeader
from morphui.uix.dataview import MorphDataViewIndexLabel
from morphui.uix.dataview import MorphDataViewHeaderLabel
from morphui.uix.recyclegridlayout import MorphRecycleGridLayout


__all__ = [
    'MorphDataViewBodyLabel',
    'MorphDataViewBodyLayout',
    'MorphDataViewBody',]


class MorphDataViewBodyLabel(
        BaseDataViewLabel,):
    """A label widget designed for use as a body cell in a data view.

    This class extends the base data view label to provide specific
    styling and behavior for body cells.
    """

    header: MorphDataViewHeader = ObjectProperty(None)
    """Reference to the header associated with this body label.

    This property holds a reference to the header component of the data
    view, allowing the body label to access header information if
    needed.

    :attr:`header` is a :class:`~kivy.properties.ObjectProperty` and
    defaults to `None`.
    """

    index: MorphDataViewIndex = ObjectProperty(None)
    """Reference to the index associated with this body label.

    This property holds a reference to the index component of the data
    view, allowing the body label to access index information if
    needed.

    :attr:`index` is a :class:`~kivy.properties.ObjectProperty` and
    defaults to `None`.
    """
    
    default_config: Dict[str, Any] = dict(
        theme_color_bindings=dict(
            normal_content_color='content_surface_color',
            normal_overlay_edge_color='outline_color',),
        typography_role='Label',
        typography_size='medium',
        typography_weight='Regular',
        halign='center',
        valign='center',
        shorten=True,
        padding=[dp(8), dp(4)],
        overlay_edge_width=dp(0.5),
        auto_size=(False, False),
        size_hint=(None, None),
        size=(
            MorphDataViewHeaderLabel.default_config.get('width', dp(120)),
            MorphDataViewIndexLabel.default_config.get('height', dp(30)),),
        text_size=(
            MorphDataViewHeaderLabel.default_config.get('width', dp(120)) - dp(16),
            MorphDataViewIndexLabel.default_config.get('height', dp(30)) - dp(8),),
        visible_edges=['bottom'],)
    """Default configuration for the MorphDataViewBodyLabel."""
    
    def refresh_view_attrs(
            self,
            rv: RecycleView,
            index: int,
            data: Dict[str, Any]
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
        data : Dict[str, Any]
            The data dictionary for this view.
        """
        super().refresh_view_attrs(rv, index, data)
        self.rv = rv
        self.rv_index = index
        self.refresh_content()
        self.refresh_overlay()
        rv.data[index]['width'] = self.width
        rv.data[index]['height'] = self.height


class MorphDataViewBodyLayout(MorphRecycleGridLayout):
    """A layout for arranging body cells in a data view.

    This class extends the base data view layout and 
    :class:`MorphRecycleGridLayout` to provide a grid layout suitable
    for body cells.
    """

    header: MorphDataViewHeader = ObjectProperty(None)
    """Reference to the header associated with this body label.

    This property holds a reference to the header component of the data
    view, allowing the body label to access header information if
    needed.

    :attr:`header` is a :class:`~kivy.properties.ObjectProperty` and
    defaults to `None`.
    """

    index: MorphDataViewIndex = ObjectProperty(None)
    """Reference to the index associated with this body label.

    This property holds a reference to the index component of the data
    view, allowing the body label to access index information if
    needed.

    :attr:`index` is a :class:`~kivy.properties.ObjectProperty` and
    defaults to `None`.
    """

    default_config: Dict[str, Any] = dict(
        theme_color_bindings={
            'normal_surface_color': 'surface_container_low_color'},
        auto_size=(True, True),)
    """Default configuration for the MorphDataViewBodyLayout."""

    def __init__(self, **kwargs) -> None:
        config = self.default_config.copy() | kwargs
        super().__init__(**config)


class MorphDataViewBody(BaseDataView):
    """A RecycleView designed to serve as the body of a data view.

    This class extends the base data view to provide a body component
    suitable for displaying tabular data in a data view.
    """
    
    Builder.load_string(dedent('''
        <MorphDataViewBody>:
            viewclass: 'MorphDataViewBodyLabel'
            MorphDataViewBodyLayout:
        '''))

    header: MorphDataViewHeader = ObjectProperty(None)
    """Reference to the header associated with this body label.

    This property holds a reference to the header component of the data
    view, allowing the body label to access header information if
    needed.

    :attr:`header` is a :class:`~kivy.properties.ObjectProperty` and
    defaults to `None`.
    """

    index: MorphDataViewIndex = ObjectProperty(None)
    """Reference to the index associated with this body label.

    This property holds a reference to the index component of the data
    view, allowing the body label to access index information if
    needed.

    :attr:`index` is a :class:`~kivy.properties.ObjectProperty` and
    defaults to `None`.
    """

    def _get_values(self) -> List[List[str]]:
        """Get the current values in the body as a 2D list.

        This method constructs a list of lists representing the values
        of the body cells, organized by rows and columns. The outer list
        represents rows, and each inner list represents the values in
        that row. This method is used internally for the 
        :attr:`values` property.
        """
        if not self.layout_manager or not self.layout_manager.children:
            return []
        children = self.layout_manager.children[::-1]
        n_cols = self.layout_manager.cols
        return [
            [children[i + j * n_cols].text for i in range(n_cols)]
            for j in range(len(children) // n_cols)]

    def _set_values(self, values: Sequence[Sequence[Any]]) -> None:
        """Set the values of the body from a 2D list.

        This method takes a list of lists representing the desired
        values for the body cells and updates the data accordingly. The
        outer list represents rows, and each inner list represents the
        values in that row. This method is used internally for the
        :attr:`values` property.
        """
        n_cols = max(len(row) for row in values) if values else 0

        self.layout_manager.cols = n_cols
        self.data = [
            {
                'text': str(value),
                'header': self.header,
                'index': self.index,
                **MorphDataViewBodyLabel.default_config,} 
            for row in values
            for value in row]
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
        bar_width=dp(3),)
    """Default configuration for the MorphDataViewBody."""
    
    def __init__(self, **kwargs) -> None:
        self.register_event_type('on_values_updated')
        config = self.default_config.copy() | kwargs
        super().__init__(**config)
    
    def on_header(self, instance: Any, header: Any) -> None:
        """Handle changes to the associated header data view.

        This method is called whenever the `header` property is set
        and synchronizes the horizontal scrolling between the body and
        header.
        """
        self.sync_x_target = header
        header.sync_x_target = self
        if self.layout_manager is not None:
            self.layout_manager.header = header

    def on_index(self, instance: Any, index: Any) -> None:
        """Handle changes to the associated index data view.

        This method is called whenever the `index` property is set
        and synchronizes the vertical scrolling between the body and
        index.
        """
        self.sync_y_target = index
        index.sync_y_target = self
        if self.layout_manager is not None:
            self.layout_manager.index = index

    def on_layout_manager(self, instance: Any, layout_manager: Any) -> None:
        """Handle changes to the associated layout.

        This method is called whenever the `layout_manager` property is set
        and configures the layout to reference the associated header
        and index.
        """
        layout_manager.header = self.header
        layout_manager.index = self.index

    def on_values_updated(self, *args) -> None:
        """Event handler called when the values in the body are updated.

        This method is triggered whenever the `values` property is set
        and can be overridden to perform additional actions when the
        body data changes.
        """
        pass