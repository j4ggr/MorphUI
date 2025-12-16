from textwrap import dedent

from typing import Any
from typing import Dict
from typing import List
from typing import Sequence

from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import AliasProperty

from morphui.utils import clean_config
from morphui.uix.dataview.base import BaseDataViewLabel
from morphui.uix.dataview.base import BaseDataView
from morphui.uix.recycleboxlayout import MorphRecycleBoxLayout


__all__ = [
    'MorphDataViewHeaderLabel',
    'MorphDataViewHeaderLayout',
    'MorphDataViewHeader',]


class MorphDataViewHeaderLabel(BaseDataViewLabel): # TODO: maybe adding HoverEnhanceBehavior and handle the resizing via RV touch?
    """A label widget designed for use as a header in a data view.
    
    This class extends the base data view label to provide specific
    styling and behavior for header labels.
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
        overlay_edge_width=dp(0.5),
        size_hint=(None, 1),
        auto_size=(False, False),
        width=dp(150),
        visible_edges=['right', 'bottom'],)
    """Default configuration for the MorphDataViewHeaderLabel."""


class MorphDataViewHeaderLayout(MorphRecycleBoxLayout):
    """A layout for arranging header labels in a data view.

    This class extends the base data view layout and MorphRecycleBoxLayout
    to provide a horizontal layout suitable for header labels.
    """
    
    default_config: Dict[str, Any] = dict(
        theme_color_bindings={
            'normal_surface_color': 'surface_container_high_color'},
        orientation='horizontal',
        auto_size=(True, False),
        size_hint_y=None,
        height=dp(35),)
    """Default configuration for the MorphDataViewHeaderLayout."""

    def __init__(self, **kwargs) -> None:
        config = clean_config(self.default_config, kwargs)
        super().__init__(**config)


class MorphDataViewHeader(BaseDataView):
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
            MorphDataViewHeaderLayout:
        '''))

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
        self.dispatch('on_columns_updated')

    column_names: List[str] = AliasProperty(
        _get_column_names,
        _set_column_names,
        bind=['data'])
    """List of column names displayed in the header.

    This property allows getting and setting the column names for the
    header. When set, it updates the header's data accordingly.
    
    :attr:`column_names` is an :class:`~kivy.properties.AliasProperty`
    and is bound to changes in the `data` property.
    """
    
    default_config: Dict[str, Any] = dict(
        do_scroll_x=True,
        do_scroll_y=False,
        size_hint=(1, None),
        bar_width=0,)
    """Default configuration for the :class:`MorphDataViewHeader`."""

    def __init__(self, **kwargs) -> None:
        self.register_event_type('on_columns_updated')
        config = clean_config(self.default_config, kwargs)
        super().__init__(**config)
        self.layout_manager.bind(height=self.setter('height'))
        self.height = self.layout_manager.height

    def on_columns_updated(self, *args) -> None:
        """Event handler called when the columns are updated.

        This event is dispatched whenever the column names are changed,
        allowing for custom behavior to be implemented in response to
        column updates.
        """
        pass