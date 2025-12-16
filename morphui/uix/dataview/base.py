"""Base classes for data view components.

This module provides base classes for data view labels and layouts,
eliminating code duplication across header, index, and body components.
"""

from typing import Any
from typing import Dict
from typing import List
from typing import Sequence
from typing import TYPE_CHECKING

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
from morphui.uix.behaviors import MorphIdentificationBehavior

if TYPE_CHECKING:
    from morphui.uix.recycleboxlayout import MorphRecycleBoxLayout
    from morphui.uix.recyclegridlayout import MorphRecycleGridLayout


__all__ = [
    'BaseDataViewLabel',
    'BaseDataView',
]


class BaseDataViewLabel(
        RecycleDataViewBehavior,
        MorphOverlayLayerBehavior,
        MorphThemeBehavior,
        MorphContentLayerBehavior,
        MorphAutoSizingBehavior,
        BaseLabel,):
    """Base class for data view labels.

    This class provides the common functionality shared by all data view
    label types (header, index, and body). It combines several MorphUI
    behaviors to provide a themed, auto-sizing label with content and
    overlay layer capabilities.
    
    Subclasses should override the `default_config` class attribute to
    provide specific styling and behavior for their use case.
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
        self.refresh_auto_sizing()
        self.refresh_content()
        self.refresh_overlay()


class BaseDataView(
        MorphIdentificationBehavior,
        MorphScrollSyncBehavior,
        RecycleView):
    """Base class for data view components.

    This class combines identification and scroll synchronization
    behaviors with RecycleView functionality to create a base
    component suitable for data views.
    
    Subclasses should override the `default_config` class attribute
    to provide specific scroll behavior and sizing for their use case.
    """

    default_config: Dict[str, Any] = dict(
        scroll_distance=dp(120),)
    
    def __init__(self, **kwargs) -> None:
        """Initialize the data view component.

        This constructor applies the default configuration and
        initializes the base RecycleView functionality.
        
        Parameters
        ----------
        **kwargs : dict
            Additional keyword arguments for configuration.
        """
        config = clean_config(self.default_config, kwargs)
        super().__init__(**config)