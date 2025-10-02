from typing import Any
from typing import Dict
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
    DMSANS_FONTS: Path = _root_path_/'fonts'/'dmsans'
    """Path to the DM Sans fonts directory."""
    INTER_FONTS: Path = _root_path_/'fonts'/'inter'
    """Path to the Inter fonts directory."""
    ICON_FONTS: Path = _root_path_/'fonts'/'materialicons'
    """Path to the Material Design icon fonts directory."""
PATH = _Path_()
"""Container for path constants."""


@dataclass
class _Fonts_:
    
    @property
    def DMSANS_REGULAR(self) -> Dict[str, str]:
        """Details for the DM Sans Regular weight font family.
        
        DM Sans is a low-contrast geometric sans serif designed for use 
        at smaller text sizes. This variant provides the standard regular
        weight with full italic and bold support.
        
        Returns
        -------
        Dict[str, str]
            Font configuration dictionary with keys:
            - 'name': Font family name for Kivy registration
            - 'fn_regular': Path to regular weight font file
            - 'fn_bold': Path to bold weight font file  
            - 'fn_italic': Path to italic weight font file
            - 'fn_bolditalic': Path to bold italic font file
        """
        return {
            'name': 'DMSans',
            'fn_regular': str(PATH.DMSANS_FONTS/'DMSans-Regular.ttf'),
            'fn_bold': str(PATH.DMSANS_FONTS/'DMSans-Bold.ttf'),
            'fn_italic': str(PATH.DMSANS_FONTS/'DMSans-Italic.ttf'),
            'fn_bolditalic': str(PATH.DMSANS_FONTS/'DMSans-BoldItalic.ttf'),}
    
    @property
    def DMSANS_THIN(self) -> Dict[str, str]:
        """Details for the DM Sans Thin weight font family.
        
        This variant provides the thin weight of DM Sans, ideal for
        headlines and display text where a lighter appearance is desired.
        Bold variants use SemiBold weights for better contrast.
        
        Returns
        -------
        Dict[str, str]
            Font configuration dictionary with keys:
            - 'name': Font family name for Kivy registration
            - 'fn_regular': Path to thin weight font file
            - 'fn_italic': Path to thin italic font file
            - 'fn_bold': Path to semi-bold font file (bold equivalent)
            - 'fn_bolditalic': Path to semi-bold italic font file
        """
        return {
            'name': 'DMSansThin',
            'fn_regular': str(PATH.DMSANS_FONTS/'DMSans-Thin.ttf'),
            'fn_italic': str(PATH.DMSANS_FONTS/'DMSans-ThinItalic.ttf'),
            'fn_bold': str(PATH.DMSANS_FONTS/'DMSans-SemiBold.ttf'),
            'fn_bolditalic': str(PATH.DMSANS_FONTS/'DMSans-SemiBoldItalic.ttf'),}
    
    @property
    def DMSANS_HEAVY(self) -> Dict[str, str]:
        """Details for the DM Sans Heavy weight font family.
        
        This variant provides heavier weights of DM Sans, using Medium
        as the base weight and ExtraBold for bold variants. Ideal for
        strong emphasis and impactful headings.
        
        Returns
        -------
        Dict[str, str]
            Font configuration dictionary with keys:
            - 'name': Font family name for Kivy registration
            - 'fn_regular': Path to medium weight font file (base weight)
            - 'fn_italic': Path to medium italic font file
            - 'fn_bold': Path to extra-bold font file
            - 'fn_bolditalic': Path to extra-bold italic font file
        """
        return {
            'name': 'DMSansHeavy',
            'fn_regular': str(PATH.DMSANS_FONTS/'DMSans-Medium.ttf'),
            'fn_italic': str(PATH.DMSANS_FONTS/'DMSans-MediumItalic.ttf'),
            'fn_bold': str(PATH.DMSANS_FONTS/'DMSans-ExtraBold.ttf'),
            'fn_bolditalic': str(PATH.DMSANS_FONTS/'DMSans-ExtraBoldItalic.ttf'),}

    @property
    def INTER_REGULAR(self) -> Dict[str, str]:
        """Details for the Inter Regular weight font family.
        
        Inter is a typeface specifically designed for computer screens
        and user interfaces. It features excellent legibility at small
        sizes and provides a complete set of weights and styles.
        
        Returns
        -------
        Dict[str, str]
            Font configuration dictionary with keys:
            - 'name': Font family name for Kivy registration
            - 'fn_regular': Path to regular weight font file
            - 'fn_bold': Path to bold weight font file
            - 'fn_italic': Path to italic weight font file
            - 'fn_bolditalic': Path to bold italic font file
        """
        return {
            'name': 'Inter',
            'fn_regular': str(PATH.INTER_FONTS/'Inter-Regular.ttf'),
            'fn_bold': str(PATH.INTER_FONTS/'Inter-Bold.ttf'),
            'fn_italic': str(PATH.INTER_FONTS/'Inter-Italic.ttf'),
            'fn_bolditalic': str(PATH.INTER_FONTS/'Inter-BoldItalic.ttf'),}

    @property
    def INTER_THIN(self) -> Dict[str, str]:
        """Details for the Inter Thin weight font family.
        
        This variant provides the thin weight of Inter, ideal for
        headlines and display text where a lighter appearance is desired.
        Bold variants use ExtraBold weights for better contrast.
        
        Returns
        -------
        Dict[str, str]
            Font configuration dictionary with keys:
            - 'name': Font family name for Kivy registration
            - 'fn_regular': Path to thin weight font file
            - 'fn_italic': Path to thin italic font file
            - 'fn_bold': Path to semi-bold font file (bold equivalent)
            - 'fn_bolditalic': Path to semi-bold italic font file
        """
        return {
            'name': 'InterThin',
            'fn_regular': str(PATH.INTER_FONTS/'Inter-Thin.ttf'),
            'fn_italic': str(PATH.INTER_FONTS/'Inter-ThinItalic.ttf'),
            'fn_bold': str(PATH.INTER_FONTS/'Inter-SemiBold.ttf'),
            'fn_bolditalic': str(PATH.INTER_FONTS/'Inter-SemiBoldItalic.ttf'),}
    
    @property
    def INTER_HEAVY(self) -> Dict[str, str]:
        """Details for the Inter Heavy weight font family.
        
        This variant provides heavier weights of Inter, using Medium
        as the base weight and ExtraBold for bold variants. Ideal for
        strong emphasis and impactful headings.
        
        Returns
        -------
        Dict[str, str]
            Font configuration dictionary with keys:
            - 'name': Font family name for Kivy registration
            - 'fn_regular': Path to medium weight font file (base weight)
            - 'fn_italic': Path to medium italic font file
            - 'fn_bold': Path to extra-bold font file
            - 'fn_bolditalic': Path to extra-bold italic font file
        """
        return {
            'name': 'InterHeavy',
            'fn_regular': str(PATH.INTER_FONTS/'Inter-Medium.ttf'),
            'fn_italic': str(PATH.INTER_FONTS/'Inter-MediumItalic.ttf'),
            'fn_bold': str(PATH.INTER_FONTS/'Inter-ExtraBold.ttf'),
            'fn_bolditalic': str(PATH.INTER_FONTS/'Inter-ExtraBoldItalic.ttf'),}

    @property
    def MATERIAL_ICONS(self) -> Dict[str, str]:
        """Details for the Material Design Icons font.
        
        Material Design Icons Desktop font provides a comprehensive
        collection of vector icons following Google's Material Design
        guidelines. Icons can be used as text characters in UI elements.
        
        Returns
        -------
        Dict[str, str]
            Font configuration dictionary with keys:
            - 'name': Font family name for Kivy registration
            - 'fn_regular': Path to Material Design Icons font file
        
        Notes
        -----
        This is an icon font, so only the regular variant is provided.
        Icons are accessed using Unicode characters or glyph names.
        """
        return {
            'name': 'MaterialIcons',
            'fn_regular': str(PATH.ICON_FONTS/'MaterialDesignIconsDesktop.ttf'),}
    
    @property
    def STYLES(self) -> Dict[str, Dict[str, Dict[str, str | float | int]]]:
        
        return dict(
            Icon=dict(
                regular=dict(
                    name='MaterialIcons',
                    font_size='24sp',
                    line_height=1.0,)),

            Display=dict(
                regular=dict(
                    name='InterRegular',
                    font_size='36sp',
                    line_height=1.44,),
                thin=dict(
                    name='InterThin',
                    font_size='36sp',
                    line_height=1.44,),
                heavy=dict(
                    name='InterHeavy',
                    font_size='36sp',
                    line_height=1.44,),),

            Headline=dict(
                regular=dict(
                    name='InterRegular',
                    font_size='24sp',
                    line_height=1.32,),
                thin=dict(
                    name='InterThin',
                    font_size='24sp',
                    line_height=1.32,),
                heavy=dict(
                    name='InterHeavy',
                    font_size='24sp',
                    line_height=1.32,),),
                    
            Title=dict(
                regular=dict(
                    name='InterRegular',
                    font_size='18sp',
                    line_height=1.24,),
                thin=dict(
                    name='InterThin',
                    font_size='18sp',
                    line_height=1.24,),
                heavy=dict(
                    name='InterHeavy',
                    font_size='18sp',
                    line_height=1.24,),),
                    
            Body=dict(
                regular=dict(
                    name='InterRegular',
                    font_size='14sp',
                    line_height=1.2,),
                thin=dict(
                    name='InterThin',
                    font_size='14sp',
                    line_height=1.2,),
                heavy=dict(
                    name='InterHeavy',
                    font_size='14sp',
                    line_height=1.2,),),
            
            Label=dict(
                regular=dict(
                    name='InterRegular',
                    font_size='12sp',
                    line_height=1.16,),
                thin=dict(
                    name='InterThin',
                    font_size='12sp',
                    line_height=1.16,),
                heavy=dict(
                    name='InterHeavy',
                    font_size='12sp',
                    line_height=1.16,),),)

FONTS = _Fonts_()
"""Container for font-related constants and configurations.

This instance provides access to pre-configured font families used
throughout MorphUI. Each property returns a dictionary with font
details structured for Kivy font registration, including paths to
all weight and style variants.

Font families included:
- DM Sans (Regular, Thin, Heavy variants)
- Inter (UI-optimized font)
- Material Design Icons (vector icon font)

Examples
--------
```python
# Register DM Sans Regular with Kivy
from kivy.core.text import LabelBase
LabelBase.register(**FONTS.DMSANS_REGULAR)

# Use in Label
label = Label(font_name='DMSans', text='Hello World')
```
"""
