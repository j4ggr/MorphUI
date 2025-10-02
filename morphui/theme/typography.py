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


__all__ = [
    'Typography',]


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
    """Typography system for consistent text styling across MorphUI themes.
    
    Provides a centralized interface for managing typography styles based on
    Material Design typography guidelines. Handles font registration, style
    configuration, and automatic fallbacks for missing fonts.
    
    The typography system organizes text into hierarchical roles (Display,
    Headline, Title, Body, Label) with size variants (large, medium, small)
    and supports multiple font weights for each family.
    
    Attributes
    ----------
    font_name : str
        Base font family name used for text styling.
    
    Examples
    --------
    ```python
    # Create typography instance
    typography = Typography()
    typography.font_name = 'DMSans'
    
    # Get styled text configuration
    style = typography.get_text_style('Headline', 'large')
    
    # Apply to UI component
    label = Label(
        text='Page Title',
        font_name=style['name'],
        font_size=style['font_size']
    )
    ```
    """

    font_name: str = StringProperty('Inter')
    """Base font family name for typography styling.
    
    Specifies the primary font family to use when generating text styles.
    Font weight variants are created by appending weight names (Regular,
    Thin, Heavy) to this base name. Falls back to 'InterRegular' if the
    specified font family is not registered.
    
    :attr:`font_name` is a :class:`~kivy.properties.StringProperty`
    and defaults to 'Inter'.
    
    Examples
    --------
    ```python
    typography = Typography()
    typography.font_name = 'DMSans'  # Will use DMSansRegular, DMSansThin, etc.
    ```
    """

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
        """Register a custom font family with Kivy's text rendering system.
        
        Registers font files for use in Kivy applications, enabling the font
        to be referenced by name in text widgets. Supports regular, italic,
        bold, and bold-italic variants. Skips registration if the font name
        is already registered to avoid conflicts.
        
        Parameters
        ----------
        name : str
            Unique font family name for registration. This name will be used
            to reference the font in text widgets and style configurations.
        fn_regular : str or Path
            Absolute or relative path to the regular weight font file.
            Typically a .ttf or .otf file.
        fn_italic : str or Path, optional
            Path to the italic variant font file. If not provided, Kivy
            will use synthetic italics when italic=True is set.
        fn_bold : str or Path, optional
            Path to the bold variant font file. If not provided, Kivy
            will use synthetic bold when bold=True is set.
        fn_bolditalic : str or Path, optional
            Path to the bold italic variant font file. If not provided,
            Kivy will combine synthetic bold and italic effects.
        
        Examples
        --------
        ```python
        # Register a complete font family
        typography = Typography()
        typography.register_font(
            name='CustomFont',
            fn_regular='fonts/Custom-Regular.ttf',
            fn_italic='fonts/Custom-Italic.ttf',
            fn_bold='fonts/Custom-Bold.ttf',
            fn_bolditalic='fonts/Custom-BoldItalic.ttf'
        )
        
        # Register with only regular variant
        typography.register_font(
            name='IconFont',
            fn_regular='fonts/Icons.ttf'
        )
        
        # Use the registered font
        typography.font_name = 'CustomFont'
        style = typography.get_text_style('Headline', 'large')
        ```
        
        Notes
        -----
        - Font names must be unique across the application
        - Missing style variants will use synthetic effects
        - Registration is persistent for the application session
        - Duplicate registrations are safely ignored
        """
        if name in self._registered_fonts:
            return
        
        _register_font(
            name=name,
            fn_regular=fn_regular,
            fn_italic=fn_italic,
            fn_bold=fn_bold,
            fn_bolditalic=fn_bolditalic)
        self._registered_fonts.add(name)

    def get_text_style(
            self,
            role: Literal['Display', 'Headline', 'Title', 'Body', 'Label'],
            size: Literal['large', 'medium', 'small'],
            font_weight: Literal['Regular', 'Thin', 'Heavy', ''] = ''
            ) -> Dict[str, str | float | int]:
        """Get typography style configuration for specified role and size.
        
        Retrieves the complete style dictionary including font family,
        size, and line height for the specified typography role and size
        variant. Automatically handles font registration validation and
        provides fallback to InterRegular if requested font is unavailable.
        
        Parameters
        ----------
        role : {'Display', 'Headline', 'Title', 'Body', 'Label'}
            Typography role defining the text's hierarchical importance:
            - 'Display': Large, impactful text for hero sections (24-36sp)
            - 'Headline': High-emphasis headings (18-24sp)
            - 'Title': Medium-emphasis section titles (14-22sp) 
            - 'Body': Regular content text (8-12sp)
            - 'Label': UI component text like buttons (10-14sp)
        size : {'large', 'medium', 'small'}
            Size variant within the typography role:
            - 'large': Maximum emphasis, largest size in role
            - 'medium': Standard usage, typical size for role
            - 'small': Compact layout, smallest size in role
        font_weight : {'Regular', 'Thin', 'Heavy', ''}, optional
            Font weight variant to append to base font family name.
            Empty string uses the base font family. Default is ''.
        
        Returns
        -------
        Dict[str, str | float | int]
            Style configuration dictionary containing:
            - 'font_size': Font size in Kivy 'sp' units (str)
            - 'line_height': Line height multiplier (float)
            - 'name': Resolved font family name (str)
        
        Raises
        ------
        AssertionError
            If role is not in FONTS.TYPOGRAPHY_ROLES or
            size is not in FONTS.SIZE_VARIANTS.
        
        Examples
        --------
        ```python
        # Get display text style
        typography = Typography()
        display_style = typography.get_text_style('Display', 'large')
        # Returns: {'font_size': '36sp', 'line_height': 1.44, 'name': 'InterRegular'}
        
        # Use with specific font weight
        heading_style = typography.get_text_style(
            'Headline', 'medium', font_weight='Heavy'
        )
        
        # Apply to Kivy Label
        label = Label(
            text='Sample Text',
            font_name=display_style['name'],
            font_size=display_style['font_size']
        )
        ```
        
        Notes
        -----
        - Font sizes use 'sp' (scale-independent pixels) for accessibility
        - Line heights are multipliers applied to font size
        - Unregistered fonts automatically fall back to 'InterRegular'
        - Font weight variants are appended to base font family name
        """
        assert role in FONTS.TYPOGRAPHY_ROLES,(
            f'Invalid role {role:r}, must be one of {FONTS.TYPOGRAPHY_ROLES}')
        assert size in FONTS.SIZE_VARIANTS, (
            f'Invalid size {size:r}, must be one of {FONTS.SIZE_VARIANTS}')
        
        resolved_font_name = self.font_name
        if resolved_font_name not in self._registered_fonts:
            font_with_weight = f'{resolved_font_name}{font_weight}'
            if font_with_weight in self._registered_fonts:
                resolved_font_name = font_with_weight
            else:
                resolved_font_name = 'InterRegular'
                warnings.warn(
                    f'Font "{font_with_weight}" not registered, '
                    f'falling back to "{resolved_font_name}"',
                    UserWarning, stacklevel=2)

        text_style = FONTS.TEXT_STYLES[role][size].copy()
        text_style['name'] = resolved_font_name
        return text_style
