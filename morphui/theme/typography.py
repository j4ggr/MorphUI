"""
Typography system for MorphUI themes
"""
import warnings

from typing import Dict
from typing import Literal
from pathlib import Path

from kivy.core.text import LabelBase
from kivy.properties import StringProperty

from ..constants import FONTS


def _register_font(
        name: str,
        fn_regular: str | Path,
        fn_italic: str | Path | None = None,
        fn_bold: str | Path | None = None,
        fn_bolditalic: str | Path | None = None
        ) -> str:
    """Register a font with Kivy's LabelBase.

    Parameters
    ----------
    data : dict
        Dictionary with font registration parameters.
    """
    LabelBase.register(
        name=name,
        fn_regular=fn_regular,
        fn_italic=fn_italic,
        fn_bold=fn_bold,
        fn_bolditalic=fn_bolditalic)
    return name

_fonts_to_register = [
    FONTS.DMSANS_REGULAR,
    FONTS.DMSANS_THIN,
    FONTS.DMSANS_HEAVY,
    FONTS.INTER_REGULAR,
    FONTS.MATERIAL_ICONS]

class Typography:
    """Typography styles for themes"""

    font_name: str = StringProperty('Inter')
    """Font family name for the typography style.

    :attr:`font_name` is a :class:`~kivy.properties.StringProperty` and
    defaults to 'Inter'."""

    _registered_fonts: set = set(
        _register_font(**font_data) for font_data in _fonts_to_register)
    """Set of registered font family names to avoid duplicate 
    registrations."""

    def register_font(
            self,
            name: str,
            fn_regular: str | Path,
            fn_italic: str | Path | None = None,
            fn_bold: str | Path | None = None,
            fn_bolditalic: str | Path | None = None
            ) -> None:
        """Register a custom font with Kivy's LabelBase.
        
        If the font is already registered, this is a no-op.
        
        Parameters
        ----------
        name : str
            Name of the font family.
        fn_regular : str or Path
            Path to the regular font file.
        fn_italic : str or Path, optional
            Path to the italic font file.
        fn_bold : str or Path, optional
            Path to the bold font file.
        fn_bolditalic : str or Path, optional
            Path to the bold italic font file."""
        if name in self._registered_fonts:
            return
        
        _register_font(
            name=name,
            fn_regular=fn_regular,
            fn_italic=fn_italic,
            fn_bold=fn_bold,
            fn_bolditalic=fn_bolditalic)
        self._registered_fonts.add(name)

    def get_style(
            self,
            role: Literal['Display', 'Headline', 'Title', 'Body', 'Label'],
            size: Literal['large', 'medium', 'small'],
            weight: Literal['Regular', 'Thin', 'Heavy', ''] = ''
            ) -> Dict[str, str | float | int]:
        """Get the style dictionary for the current role and size.

        Returns
        -------
        dict
            Dictionary with 'font_size' and 'line_height' keys.

        Raises
        ------
        ValueError
            If the role or size is invalid.
        """
        assert role in FONTS.TYPOGRAPHY_ROLES,(
            f'Invalid role {role:r}, must be one of {FONTS.TYPOGRAPHY_ROLES}')
        assert size in FONTS.SIZE_VARIANTS, (
            f'Invalid size {size:r}, must be one of {FONTS.SIZE_VARIANTS}')
        
        font_name = self.font_name
        if font_name not in self._registered_fonts:
            _name = f'{font_name}{weight}'
            if _name not in self._registered_fonts:
                font_name = 'InterRegular'
                warnings.warn(
                    f'Font "{_name}" not registered, falling back to '
                    f'"{font_name}"')
            else:
                font_name = _name

        try:
            return FONTS.TEXT_STYLES[self.role][self.size]
        except KeyError as e:
            raise ValueError(f"Invalid role '{self.role}' or size '{self.size}'") from e

