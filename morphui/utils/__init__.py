'''
Utility modules for MorphUI
'''

from .dotdict import DotDict
from .dotdict import dotdict

from .helpers import calculate_text_size
from .helpers import clean_default_config


__all__ = [
    'DotDict',
    'dotdict',
    'calculate_text_size',
    'clean_default_config',]
