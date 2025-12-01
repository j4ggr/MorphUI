"""Data view components for displaying tabular data.

This package provides components for creating data views with headers,
indices, and body content. It includes base classes to eliminate code
duplication across different data view components.
"""

from morphui.uix.dataview.base import BaseDataViewLabel
from morphui.uix.dataview.base import BaseDataViewLayout
from morphui.uix.dataview.base import BaseDataView

__all__ = [
    'BaseDataViewLabel',
    'BaseDataViewLayout', 
    'BaseDataView',
]