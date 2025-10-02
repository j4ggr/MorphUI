from typing import Tuple
from typing import Literal
from pathlib import Path
from dataclasses import dataclass
from materialyoucolor.utils.platform_utils import SCHEMES

__all__ = [
    'ICON',
    'THEME',
    'PATH',]


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

_root_path_: Path = Path(__file__).parent

@dataclass
class _Path_:
    ROOT: Path = _root_path_
    """Root directory of the project."""
    FONTS: Path = _root_path_/'fonts'
    """Directory containing font files."""
PATH = _Path_()
"""Container for path constants."""
