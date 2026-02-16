'''
Utility modules for MorphUI
'''

from .dotdict import DotDict
from .dotdict import dotdict

from .helpers import clamp
from .helpers import FrozenGeometry
from .helpers import get_edges_params
from .helpers import calculate_text_size
from .helpers import calculate_widget_local_pos
from .helpers import timeit


__all__ = [
    'DotDict',
    'dotdict',
    'clamp',
    'FrozenGeometry',
    'get_edges_params',
    'calculate_text_size',
    'calculate_widget_local_pos',
    'timeit',]
