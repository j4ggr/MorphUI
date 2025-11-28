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
    'MorphDataViewHeaderLabel',
    'MorphDataViewHeaderLayout',
    'MorphDataViewHeader',]


class MorphDataViewHeaderLabel( # TODO: maybe adding HoverEnhanceBehavior and handle the resizing via RV touch?
        RecycleDataViewBehavior,
        MorphOverlayLayerBehavior,
        MorphThemeBehavior,
        MorphContentLayerBehavior,
        MorphAutoSizingBehavior,
        BaseLabel,):
    """A label widget designed for use as a header in a data view.
    
    This class combines the functionalities of MorphResizeBehavior,
    RecycleDataViewBehavior, and MorphSimpleLabel to create a label
    suitable for displaying header information in data views. It
    supports user-controlled resizing and integrates with Kivy's
    RecycleView framework.
    """

    rv_index: int = NumericProperty(0)
    """The index of this label in the RecycleView data.

    :attr:`index` is a :class:`~kivy.properties.NumericProperty`
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
        halign='left',
        valign='center',
        padding=[dp(8), dp(4)],
        overlay_edge_width=dp(1),
        auto_size=True,
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
        theme_color_bindings={
            'normal_surface_color': 'surface_color'},
        orientation='horizontal',
        auto_size=(True, False),
        size_hint_y=None,
        height=dp(35),)
    """Default configuration for the MorphDataViewHeaderLayout."""

    def __init__(self, **kwargs) -> None:
        config = clean_config(self.default_config, kwargs)
        super().__init__(**config)
    
    def on_cells(
            self, instance: Any, cells: List[MorphDataViewHeaderLabel]) -> None:
        """Called when the list of header label widgets changes.

        This method is triggered whenever the `cells` property changes,
        allowing for any necessary updates or refreshes to the header
        labels.
        """
        for cell in cells:
            index = cell.rv_index
            rv = cell.rv
            cell.refresh_view_attrs(rv, index, rv.data[index])


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
    from morphui.uix.dataview.header import MorphDataViewHeader

    class MyApp(MorphApp):
        def build(self) -> MorphDataViewHeader:
            self.theme_manager.theme_mode = 'Dark'
            self.theme_manager.seed_color = 'morphui_teal'
            header = MorphDataViewHeader()
            header.column_names = [
                'Name', 'Age', 'Occupation', 'Country', 'Email', 'Phone', 'Company',
                'Position', 'Department', 'Start Date', 'End Date', 'Status',
                'Notes', 'Salary', 'Bonus', 'Manager', 'Team', 'Location',
                'Project', 'Task', 'Deadline', 'Priority', 'Comments', 'Feedback',
                'Rating', 'Score', 'Level', 'Experience', 'Skills', 'Certifications',
                'Languages', 'Hobbies', 'Interests', 'Social Media', 'Website',]
            return header
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
        self.data = [
            {'text': str(n), **MorphDataViewHeaderLabel.default_config}
            for n in names]

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
    """Default configuration for the :class:`MorphDataViewHeader`."""

    def __init__(self, **kwargs) -> None:
        config = clean_config(self.default_config, kwargs)
        super().__init__(**config)
        self.layout.bind(height=self.setter('height'))
        self.height = self.layout.height