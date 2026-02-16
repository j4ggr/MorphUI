'''
Utility modules for MorphUI
'''

from .dotdict import DotDict
from .dotdict import dotdict

from .helpers import clamp
from .helpers import timeit
from .helpers import refresh_widget
from .helpers import FrozenGeometry
from .helpers import get_edges_params
from .helpers import calculate_text_size
from .helpers import calculate_widget_local_pos


__all__ = [
    'DotDict',
    'dotdict',
    'clamp',
    'timeit',
    'refresh_widget',
    'FrozenGeometry',
    'get_edges_params',
    'calculate_text_size',
    'calculate_widget_local_pos',]
