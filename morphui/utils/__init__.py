'''
Utility modules for MorphUI
'''

from .dotdict import DotDict
from .dotdict import dotdict

from .helpers import clamp
from .helpers import clean_config
from .helpers import FrozenGeometry
from .helpers import get_edges_params
from .helpers import calculate_text_size
from .helpers import calculate_widget_local_pos


__all__ = [
    'DotDict',
    'dotdict',
    'clamp',
    'clean_config',
    'FrozenGeometry',
    'get_edges_params',
    'calculate_text_size',
    'calculate_widget_local_pos',]
