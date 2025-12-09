"""Base classes for data view components.

This module provides base classes for data view labels and layouts,
eliminating code duplication across header, index, and body components.
"""

from typing import Any
from typing import Dict
from typing import List
from typing import Sequence
from typing import TYPE_CHECKING

from kivy.properties import AliasProperty
from kivy.properties import ObjectProperty
from kivy.properties import NumericProperty
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.views import RecycleDataViewBehavior

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
    'BaseDataViewLayout', 
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
        rv.data[index]['width'] = self.width
        rv.data[index]['height'] = self.height
        return super().refresh_view_attrs(rv, index, data)


class BaseDataViewLayout:
    """Base mixin class for data view layouts.

    This mixin provides common functionality for data view layouts,
    including cell management and refresh capabilities. It should be
    mixed with either MorphRecycleBoxLayout or MorphRecycleGridLayout.
    
    Subclasses should:
    1. Override `_get_cell_type()` to return the appropriate label class
    2. Mix this class with the appropriate layout class
    3. Override `default_config` for specific styling
    """

    def _get_cell_type(self) -> type:
        """Get the type of cell label that this layout manages.
        
        This method should be overridden by subclasses to return the
        appropriate label class (e.g., MorphDataViewHeaderLabel).
        
        Returns
        -------
        type
            The class type for cell labels managed by this layout.
        
        Raises
        ------
        NotImplementedError
            If not implemented by subclass.
        """
        raise NotImplementedError("Subclasses must implement _get_cell_type()")

    def _get_cells(self) -> List[BaseDataViewLabel]:
        """Retrieve the list of cell labels managed by this layout.

        The method iterates through the child widgets of the layout
        and filters to return only those that are instances of the
        appropriate cell label type.
        
        Returns
        -------
        List[BaseDataViewLabel]
            A list of all cell label widgets within this layout.
        """
        cell_type = self._get_cell_type()
        return [
            child for child in self.children # type: ignore
            if isinstance(child, cell_type)]
    
    def _set_cells(self, cells: Sequence[BaseDataViewLabel]) -> None:
        """Set the cell labels managed by this layout.

        This method replaces the current child widgets of the layout
        with the provided list of cell labels.

        Parameters
        ----------
        cells : Sequence[BaseDataViewLabel]
            A sequence of cell label widgets to be set as children
            of this layout.

        Raises
        ------
        AssertionError
            If the layout does not have the required methods to
            manage child widgets.
        """
        assert hasattr(self, 'clear_widgets') and hasattr(self, 'add_widget'), (
            'The layout must have clear_widgets and add_widget methods')
        self.clear_widgets() # type: ignore
        for cell in cells:
            self.add_widget(cell) # type: ignore

    cells: Sequence[BaseDataViewLabel] = AliasProperty(
        _get_cells,
        _set_cells,
        bind=['children'],)
    """A list of all cell labels within this layout.

    This property returns a list of all child widgets that are instances
    of the appropriate cell label type. It allows easy access to the
    cell labels contained within the layout.

    :attr:`cells` is an :class:`~kivy.properties.AliasProperty`
    and is bound to changes in the `children` property.
    """

    def on_cells(
            self,
            instance: 'BaseDataViewLayout',
            cells: List[BaseDataViewLabel]) -> None:
        """Handle updates when the list of cell labels changes.

        This method is called whenever the `cells` property changes,
        allowing for any necessary updates or refreshes to the cell
        labels.

        Parameters
        ----------
        instance : BaseDataViewLayout
            The instance of the layout where the change occurred.
        cells : List[BaseDataViewLabel]
            A list of cell label widgets managed by this layout.
        """
        for cell in cells:
            if cell.rv and cell.rv.data and cell.rv_index < len(cell.rv.data):
                cell.refresh_view_attrs(
                    rv=cell.rv,
                    index=cell.rv_index,
                    data=cell.rv.data[cell.rv_index])


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
    pass