from dataclasses import dataclass


__all__ = [
    'ICON',]


@dataclass
class _Icon_:
    DD_MENU_CLOSED: str = 'chevron-up'
    """Icon for the closed dropdown menu."""
    DD_MENU_OPEN: str = 'chevron-down'
    """Icon for the open dropdown menu."""
ICON = _Icon_()
"""Container for icon constants."""