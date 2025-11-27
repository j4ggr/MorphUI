from textwrap import dedent

from typing import Any
from typing import Dict
from typing import List
from typing import Sequence

from kivy.lang import Builder
from kivy.metrics import dp
from kivy.uix.label import Label
from kivy.properties import AliasProperty
from kivy.properties import ObjectProperty
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.views import RecycleDataViewBehavior

from morphui.utils import clean_config
from morphui.uix.label import MorphSimpleLabel
from morphui.uix.behaviors import MorphResizeBehavior
from morphui.uix.behaviors import MorphScrollSyncBehavior

from morphui.uix.behaviors import MorphIconBehavior
from morphui.uix.behaviors import MorphThemeBehavior
from morphui.uix.behaviors import MorphAutoSizingBehavior
from morphui.uix.behaviors import MorphRoundSidesBehavior
from morphui.uix.behaviors import MorphSurfaceLayerBehavior
from morphui.uix.behaviors import MorphContentLayerBehavior
from morphui.uix.behaviors import MorphHoverEnhancedBehavior
from morphui.uix.behaviors import MorphOverlayLayerBehavior
from morphui.uix.recycleboxlayout import MorphRecycleBoxLayout


__all__ = [
    'MorphDataViewHeader',
    'MorphDataViewHeaderLayout',
    'MorphDataViewHeaderLabel',]


class MorphDataViewHeaderLabel(
        RecycleDataViewBehavior,
        MorphOverlayLayerBehavior,
        MorphThemeBehavior,
        MorphContentLayerBehavior,
        MorphAutoSizingBehavior,
        Label,):
    """A label widget designed for use as a header in a data view.
    
    This class combines the functionalities of MorphResizeBehavior,
    RecycleDataViewBehavior, and MorphSimpleLabel to create a label
    suitable for displaying header information in data views. It
    supports user-controlled resizing and integrates with Kivy's
    RecycleView framework.
    """
    
    minimum_height: float = AliasProperty(
        lambda self: self.texture_size[1] + self.padding[1] + self.padding[3],
        bind=['texture_size', 'padding',])
    """The minimum height required to display the label's content.

    This property calculates the minimum height based on the label's
    texture size and padding.

    :attr:`minimum_height` is a :class:`~kivy.properties.AliasProperty`
    """

    minimum_width: float = AliasProperty(
        lambda self: self.texture_size[0] + self.padding[0] + self.padding[2],
        bind=['texture_size', 'padding',])
    """The minimum width required to display the label's content.

    This property calculates the minimum width based on the label's
    texture size and padding.

    :attr:`minimum_width` is a :class:`~kivy.properties.AliasProperty`
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
        resizable_edges= ['right',],
        visible_edges=['right', 'bottom'],)
    """Default configuration for the MorphDataViewHeaderLabel."""
    

class MorphDataViewHeaderLayout(
        MorphRecycleBoxLayout):

    cells: List[MorphDataViewHeaderLabel] = AliasProperty(
        lambda self: [
            child for child in self.children
            if isinstance(child, MorphDataViewHeaderLabel)],
        None,
        bind=('children',))
    """List of header label widgets managed by this layout (read-only).

    This property returns a list of all child widgets that are instances
    of :class:`MorphDataViewHeaderLabel`. It allows easy access to the
    header labels contained within the layout.

    :attr:`cells` is an :class:`~kivy.properties.AliasProperty`.
    and is bound to changes in the `children` property.
    """
    
    default_config: Dict[str, Any] = dict(
        orientation='horizontal',
        auto_size=True,
        theme_color_bindings={
            'normal_surface_color': 'surface_color'
        })
    """Default configuration for the MorphDataViewHeaderLayout."""

    def __init__(self, **kwargs) -> None:
        config = clean_config(self.default_config, kwargs)
        super().__init__(**config)


class MorphDataViewHeader(
        MorphScrollSyncBehavior,
        RecycleView):
    """A scrollable header for data views, synchronized with the main
    data view.

    This class provides a header component for data views that can
    scroll horizontally in sync with the associated data view. It uses
    a custom layout manager to arrange header labels and supports
    dynamic column naming.

    Examples
    --------
    ```python
    from morphui.app import MorphApp
    from morphui.uix.recycleview import MorphRecycleView
    from morphui.uix.dataview.header import MorphDataViewHeader
    from morphui.uix.dataview.header import MorphDataViewHeaderLabel
    from morphui.uix.dataview.header import MorphDataViewHeaderLayout
    from morphui.uix.label import MorphLabel
    class MyApp(MorphApp):
        def build(self) -> MorphRecycleView:
            self.theme_manager.seed_color = 'Blue'
            header = MorphDataViewHeader(
                column_names=['Name', 'Age', 'Occupation'],)
            data_view = MorphRecycleView(
                viewclass='MorphLabel',
                data=[
                    {'text': f'Item {i}'} for i in range(100)],)
            # Synchronize horizontal scrolling between header and data view
            header.sync_x_target = data_view
            data_view.sync_x_target = header
            return data_view
    MyApp().run()
    ```
    """
    
    Builder.load_string(dedent('''
        <MorphDataViewHeader>:
            viewclass: 'MorphDataViewHeaderLabel'
            layout: layout
            MorphDataViewHeaderLayout:
                id: layout
        '''))
    
    layout: MorphDataViewHeaderLayout = ObjectProperty()
    """The layout manager for the header, responsible for arranging
    the header labels.

    This property is automatically set to an instance of
    :class:`MorphDataViewHeaderLayout` defined in the KV string.

    :attr:`layout` is a :class:`~kivy.properties.ObjectProperty`.
    """

    def _get_column_names(self) -> List[str]:
        """Retrieve the list of column names from the header data.

        Returns
        -------
        List[str]
            A list of column names extracted from the header's data.
        """
        return [item.get('text', '') for item in self.data]
    
    def _set_column_names(self, names: Sequence) -> None:
        """Set the column names for the header.

        This method updates the header's data to reflect the provided
        column names.

        Parameters
        ----------
        names : Sequence
            A sequence representing the column names to be displayed in 
            the header.
        """
        self.data = [{'text': str(name), 'auto_size': True} for name in names]
        self.height = self.layout.height

    column_names: List[str] = AliasProperty(
        _get_column_names,
        _set_column_names)
    """List of column names displayed in the header.

    This property allows getting and setting the column names for the
    header. When set, it updates the header's data accordingly.
    
    :attr:`column_names` is an :class:`~kivy.properties.AliasProperty`.
    """
    
    default_config: Dict[str, Any] = dict(
        do_scroll_x=True,
        do_scroll_y=False,
        size_hint=(1, None),
        bar_width=0,)
    """Default configuration for the MorphDataViewHeader."""

    def __init__(self, **kwargs) -> None:
        config = clean_config(self.default_config, kwargs)
        super().__init__(**config)
        self.layout.bind(height=self.setter('height'))
                               
