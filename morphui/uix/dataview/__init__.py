"""Data view components for displaying tabular data.

This package provides components for creating data views with headers,
indices, and body content. It includes base classes to eliminate code
duplication across different data view components.
"""

from morphui.uix.dataview.base import BaseDataViewLabel
from morphui.uix.dataview.base import BaseDataView

from morphui.uix.dataview.header import MorphDataViewHeaderLabel
from morphui.uix.dataview.header import MorphDataViewHeaderLayout
from morphui.uix.dataview.header import MorphDataViewHeader

from morphui.uix.dataview.index import MorphDataViewIndexLabel
from morphui.uix.dataview.index import MorphDataViewIndexLayout
from morphui.uix.dataview.index import MorphDataViewIndex

from morphui.uix.dataview.body import MorphDataViewBodyLabel
from morphui.uix.dataview.body import MorphDataViewBodyLayout
from morphui.uix.dataview.body import MorphDataViewBody

from morphui.uix.dataview.navigation import MorphDataViewNavigationButton
from morphui.uix.dataview.navigation import MorphDataViewNavigationPageLabel
from morphui.uix.dataview.navigation import MorphDataViewNavigation

from morphui.uix.dataview.table import MorphDataViewTable

__all__ = [
    'BaseDataViewLabel',
    'BaseDataView',
    'MorphDataViewHeaderLabel',
    'MorphDataViewHeaderLayout',
    'MorphDataViewHeader',
    'MorphDataViewIndexLabel',
    'MorphDataViewIndexLayout',
    'MorphDataViewIndex',
    'MorphDataViewBodyLabel',
    'MorphDataViewBodyLayout',
    'MorphDataViewBody',
    'MorphDataViewNavigationButton',
    'MorphDataViewNavigationPageLabel',
    'MorphDataViewNavigation',
    'MorphDataViewTable',
]