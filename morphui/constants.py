from typing import Tuple
from typing import Literal
from dataclasses import dataclass
from materialyoucolor.utils.platform_utils import SCHEMES

__all__ = [
    'ICON',
    'THEME',]


@dataclass
class _Icon_:
    DD_MENU_CLOSED: Literal['chevron-up'] = 'chevron-up'
    """Icon for the closed dropdown menu."""
    DD_MENU_OPEN: Literal['chevron-down'] = 'chevron-down'
    """Icon for the open dropdown menu."""
ICON = _Icon_()
"""Container for icon constants."""


@dataclass
class _Theme_:
    LIGHT: Literal['Light'] = 'Light'
    """Light theme mode."""
    DARK: Literal['Dark'] = 'Dark'
    """Dark theme mode."""
    SCHEMES: Tuple[str, ...] = tuple(SCHEMES.keys())
    """Available color schemes from Material You Color."""
THEME = _Theme_()
"""Container for theme-related constants."""
