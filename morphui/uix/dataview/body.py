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
        auto_size=True,
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
        size_hint_y=None,
        height=dp(200),)
    """Default configuration for the MorphDataViewBodyLayout."""

    def __init__(self, **kwargs) -> None:
        config = clean_config(self.default_config, kwargs)
        super().__init__(**config)


class MorphDataViewBody(BaseDataView):
    """A RecycleView designed to serve as the body of a data view.

    This class extends the base data view to provide a body component
    suitable for displaying tabular data in a data view.
    """
    pass
