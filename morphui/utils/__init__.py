'''
Utility modules for MorphUI
'''

from .dotdict import DotDict
from .dotdict import dotdict

from .helpers import clamp
from .helpers import FrozenGeometry
from .helpers import calculate_text_size
from .helpers import clean_config
from .helpers import calculate_widget_local_pos


__all__ = [
    'DotDict',
    'dotdict',
    'clamp',
    'FrozenGeometry',
    'calculate_text_size',
    'clean_config',
    'calculate_widget_local_pos',]
