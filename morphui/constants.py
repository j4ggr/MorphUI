import re
import tomllib

from typing import Dict
from typing import Tuple
from typing import Literal
from pathlib import Path
from dataclasses import dataclass
from material_color_utilities import Variant

__all__ = [
    'THEME',
    'PATH',
    'ICON',
    'NAME',
    'FONTS',
    'REGEX',]


@dataclass(frozen=True)
class _Theme_:
    LIGHT: Literal['Light'] = 'Light'
    """Light theme mode."""
    DARK: Literal['Dark'] = 'Dark'
    """Dark theme mode."""
    SCHEMES: Tuple[str, ...] = tuple(Variant.__members__.keys())
    """Available color schemes from Material Color Utilities."""
    
    @property
    def STYLES(self) -> Dict[str, Dict[str, str]]:
        """Predefined theme styles mapping to color roles for common 
        Material Design patterns."""
        return {
            'primary': {
                'surface_color': 'primary_color',
                'content_color': 'content_primary_color',
                'disabled_content_color': 'outline_color',
                'border_color': 'primary_color',},

            'secondary': {
                'surface_color': 'secondary_color', 
                'content_color': 'content_secondary_color',
                'disabled_content_color': 'outline_color',
                'border_color': 'secondary_color',},

            'tertiary': {
                'surface_color': 'tertiary_color',
                'content_color': 'content_tertiary_color',
                'disabled_content_color': 'outline_color',
                'border_color': 'tertiary_color',},

            'surface': {
                'surface_color': 'surface_color',
                'border_color': 'outline_color',},

            'error': {
                'surface_color': 'error_color',
                'content_color': 'content_error_color', 
                'border_color': 'error_color',},

            'outline': {
                'surface_color': 'surface_color',
                'border_color': 'outline_color',
                'disabled_border_color': 'outline_variant_color',},}
THEME = _Theme_()
"""Container for theme-related constants."""


_root_path_: Path = Path(__file__).parent

@dataclass(frozen=True)
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


with open(PATH.ICON_FONTS/'material_icons.toml', 'rb') as f:
    _icon_map_ = tomllib.load(f)['icons']

@dataclass(frozen=True)
class _Icon_:
    DD_MENU_CLOSED: Literal['chevron-up'] = 'chevron-up'
    """Icon for the closed dropdown menu."""
    DD_MENU_OPEN: Literal['chevron-down'] = 'chevron-down'
    """Icon for the open dropdown menu."""
    @property
    def MAP(self) -> Dict[str, str]:
        """Mapping of icon names to their actual Unicode characters.
        
        Returns a dictionary where keys are icon names and values are 
        the corresponding Unicode characters ready for use in labels
        and other text widgets.
        
        Examples
        --------
        ```python
        # Use icon directly in label
        icon_char = ICON.MAP['chevron-up']
        label.text = icon_char
        
        # Or with the predefined constants
        label.text = ICON.MAP[ICON.DD_MENU_CLOSED]  # 'chevron-up'
        ```
        """
        return _icon_map_.copy()
ICON = _Icon_()
"""Container for icon constants."""


@dataclass(frozen=True)
class _Name_:
    """Standardized names for component parts and rendering layers."""
    
    EDGES: Tuple[
        Literal['left'], Literal['top'], Literal['right'], Literal['bottom']
        ] = ('left', 'top', 'right', 'bottom')
    """Standard edge names for component boundaries."""

    HORIZONTAL_EDGES: Tuple[
        Literal['top'], Literal['bottom']] = ('top', 'bottom')
    """Horizontal edges for components."""

    VERTICAL_EDGES: Tuple[
        Literal['left'], Literal['right']] = ('left', 'right')
    """Vertical edges for components."""

    CORNERS: Tuple[
        Literal['top-left'], Literal['top-right'],
        Literal['bottom-left'], Literal['bottom-right']
        ] = ('top-left', 'top-right', 'bottom-left', 'bottom-right')
    """Standard corner names for component vertices."""

    SEP_CORNER: Literal['-'] = '-'
    """Separator used in corner naming conventions."""
    
    # Canvas instruction groups
    SHADOW: Literal['shadow'] = 'shadow'
    """Canvas instruction group for shadow rendering."""

    SURFACE: Literal['surface'] = 'surface'
    """Canvas instruction group for surface backgrounds."""

    SURFACE_BORDER: Literal['surface_border'] = 'surface_border'
    """Canvas instruction group for surface borders."""
    
    INTERACTION: Literal['interaction'] = 'interaction'
    """Canvas instruction group for interaction state overlays."""

    CONTENT: Literal['content'] = 'content'
    """Canvas instruction group for content rendering (text, icons)."""

    OVERLAY: Literal['overlay'] = 'overlay'
    """Canvas instruction group for overlay effects and decorations."""

    OVERLAY_EDGES: Literal['overlay_edges'] = 'overlay_edges'
    """Canvas instruction group for overlay edge effects and 
    decorations."""

    RIPPLE: Literal['ripple'] = 'ripple'
    """Canvas instruction group for ripple animations and effects."""

    TEXTINPUT_CURSOR: Literal['textinput_cursor'] = 'textinput_cursor'
    """Canvas instruction group for the text input cursor in a text
    field component."""

    TEXTINPUT_TEXT: Literal['textinput_text'] = 'textinput_text'
    """Canvas instruction group for the text content in a text field
    component."""

    # Identifiers for component parts
    INPUT: Literal['input'] = 'input'
    """Standard name for the text input area in a text field component,
    used for identification."""

    LABEL_WIDGET: Literal['label_widget'] = 'label_widget'
    """Standard name for the label widget in a combined component, used
    for identification."""

    SUPPORTING_WIDGET: Literal[
        'supporting_widget'] = 'supporting_widget'
    """Standard name for the supporting widget in a combined
    component, used for identification."""

    TEXT_LENGTH_WIDGET: Literal[
        'text_length_widget'] = 'text_length_widget'
    """Standard name for the text length widget in a text field
    component, used for identification."""

    LEADING_WIDGET: Literal[
        'leading_widget'] = 'leading_widget'
    """Standard name for the leading widget in a combined component, 
    used for identification."""

    TRAILING_WIDGET: Literal[
        'trailing_widget'] = 'trailing_widget'
    """Standard name for the trailing widget in a combined component, 
    used for identification."""

NAME = _Name_()



@dataclass(frozen=True)
class _Fonts_:
    
    # Typography role constants
    TYPOGRAPHY_ROLES: Tuple[str, ...] = (
        'Display', 'Headline', 'Title', 'Body', 'Label')
    """Available typography roles in the Material Design type system.
    
    These roles represent different levels of hierarchy and emphasis:
    - Display: Large, short, impactful text for hero sections
    - Headline: High-emphasis text for primary headings
    - Title: Medium-emphasis text for section titles
    - Body: Regular content text for paragraphs and reading
    - Label: Text for UI components like buttons and form labels
    """
    
    SIZE_VARIANTS: Tuple[str, ...] = ('large', 'medium', 'small')
    """Available size variants for each typography role.
    
    Each typography role includes three size options:
    - large: Largest size in the role for maximum emphasis
    - medium: Standard size for typical usage
    - small: Compact size for dense layouts or secondary content
    """

    WEIGHT_VARIANTS: Tuple[str, ...] = ('Thin', 'Regular', 'Heavy')
    """Available weight variants for font families.

    Weight variants provide different visual weights:
    - Thin: Lightest weight, ideal for headlines and display text
    - Regular: Standard weight for body text and general use
    - Heavy: Heavier weight for strong emphasis and impactful headings
    """
    
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
            'name': 'DMSansRegular',
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
            'name': 'InterRegular',
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
            'fn_regular': str(PATH.ICON_FONTS/'MaterialDesignIcons-Desktop.ttf'),}
    
    @property
    def DEFAULT_AUTOREGISTERED_FONTS(self) -> Tuple[Dict[str, str], ...]:
        """Default font configurations for automatic registration with 
        Kivy.

        Provides a comprehensive collection of all predefined font 
        families configured for automatic registration during 
        application startup. This includes all DM Sans variants, Inter 
        variants, and Material Design Icons, ensuring consistent 
        typography availability across the MorphUI framework.

        Returns
        -------
        Tuple[Dict[str, str], ...]
            Tuple containing font configuration dictionaries with keys:
            - 'name': Font family name for Kivy registration
            - 'fn_regular': Path to regular weight font file
            - 'fn_italic': Path to italic font file (if available)
            - 'fn_bold': Path to bold font file (if available)
            - 'fn_bolditalic': Path to bold italic font file 
              (if available)

        Font Families Included
        ----------------------
        - **DM Sans Regular**: Standard geometric sans serif
        - **DM Sans Thin**: Lightweight variant for headlines
        - **DM Sans Heavy**: Bold variant for emphasis
        - **Inter Regular**: UI-optimized sans serif
        - **Inter Thin**: Lightweight Inter variant
        - **Inter Heavy**: Bold Inter variant
        - **Material Icons**: Vector icon font

        Notes
        -----
        This tuple is designed to be used with the Typography class's
        automatic font registration system. It can be modified to 
        include a subset of fonts or extended with additional custom 
        fonts as needed. For more details, see the Examples section
        in :class:`Typography`.
        """
        return (
            self.DMSANS_REGULAR,
            self.DMSANS_THIN,
            self.DMSANS_HEAVY,
            self.INTER_REGULAR,
            self.INTER_THIN,
            self.INTER_HEAVY,
            self.MATERIAL_ICONS,)

    @property
    def TEXT_STYLES(self) -> Dict[str, Dict[str, Dict[str, str | float | int]]]:
        """Material Design typography roles with size variants.
        
        Provides a comprehensive set of text styles following Material 
        Design typography guidelines. Each role includes three size 
        variants (large, medium, small) with appropriate font sizes and 
        line heights.
        
        Returns
        -------
        Dict[str, Dict[str, Dict[str, str | float | int]]]
            Nested dictionary structure:
            - First level: Typography role names (Display, Headline, 
              Title, Body, Label)
            - Second level: Size variants ('large', 'medium', 'small')
            - Third level: Style properties ('font_size', 'line_height')
        
        Typography Roles
        ----------------
        - **Display**: Large, short, and impactful text (36sp-24sp)
        - **Headline**: High-emphasis text for shorter content (24sp-18sp)
        - **Title**: Medium-emphasis text for sections (22sp-14sp)
        - **Body**: Regular content text with good readability (12sp-8sp)
        - **Label**: Text for components like buttons and tabs (14sp-10sp)
        
        Examples
        --------
        ```python
        # Access specific typography style
        display_large = FONTS.TEXT_STYLES['Display']['large']
        # Result: {'font_size': '36sp', 'line_height': 1.44}
        
        # Apply to Kivy Label
        label = Label(
            text='Display Text',
            font_size=display_large['font_size'],
            content_size=(None, None)  # Enable line_height
        )
        ```
        
        Notes
        -----
        Font sizes use Kivy's 'sp' (scale-independent pixels) unit for
        accessibility. Line heights are specified as multipliers of font 
        size.
        """
        return dict(
            Display=dict(
                large=dict(
                    font_size='36sp',
                    line_height=1.44,),
                medium=dict(
                    font_size='30sp',
                    line_height=1.44,),
                small=dict(
                    font_size='24sp',
                    line_height=1.44,),),

            Headline=dict(
                large=dict(
                    font_size='24sp',
                    line_height=1.32,),
                medium=dict(
                    font_size='22sp',
                    line_height=1.32,),
                small=dict(
                    font_size='18sp',
                    line_height=1.32,),),
                    
            Title=dict(
                large=dict(
                    font_size='22sp',
                    line_height=1.24,),
                medium=dict(
                    font_size='18sp',
                    line_height=1.24,),
                small=dict(
                    font_size='14sp',
                    line_height=1.24,),),

            Body=dict(
                large=dict(
                    font_size='12sp',
                    line_height=1.1,),
                medium=dict(
                    font_size='10sp',
                    line_height=1.1,),
                small=dict(
                    font_size='8sp',
                    line_height=1.1,),),

            Label=dict(
                large=dict(
                    font_size='14sp',
                    line_height=1.16,),
                medium=dict(
                    font_size='12sp',
                    line_height=1.16,),
                small=dict(
                    font_size='10sp',
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

@dataclass(frozen=True)
class _RegexPattern_:
    """Precompiled regular expressions for common pattern matching."""
    
    HEX_COLOR: re.Pattern = re.compile(
        r'^#(?:[0-9a-fA-F]{3}){1,2}$')
    """Matches valid hex color codes (e.g., #FFF, #FFFFFF)."""

    EMAIL: re.Pattern = re.compile(
        r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
    """Matches valid email addresses."""

    PHONE: re.Pattern = re.compile(
        r'^\+?1?\d{9,15}$')
    """Matches valid phone numbers in international format."""

    DATE_EU: re.Pattern = re.compile(
        r'^(0[1-9]|[12][0-9]|3[01])(\/|-|\.)(0[1-9]|1[1,2])\2(19\d{2}|20\d{2})$')
    """Matches dates in European/international format (DD/MM/YYYY).
    
    Accepts day-first format with flexible separators: forward slash (/), 
    hyphen (-), or period (.). Ensures consistent separator usage throughout
    the date string.
    
    Pattern Components
    ------------------
    - Day: 01-31 (zero-padded, validates range)
    - Separator: / or - or . (must be consistent)
    - Month: 01-12 (zero-padded, validates range)  
    - Year: 1900-2099 (4-digit format only)
    
    Examples
    --------
    Valid: "25/12/2023", "03-07-1995", "31.01.2000"
    Invalid: "32/01/2023", "25/13/2023", "5/3/23"
    
    Notes
    -----
    This pattern does NOT validate actual calendar dates (e.g., Feb 30th
    will match the pattern but is not a real date). Use with datetime
    parsing for full validation.
    """

    DATE_ISO: re.Pattern = re.compile(
        r'^(19\d{2}|20\d{2})(\/|-|\.)(0[1-9]|1[1,2])\2(0[1-9]|[12][0-9]|3[01])$')
    """Matches dates in ISO-style format (YYYY/MM/DD).
    
    Accepts year-first format with flexible separators: forward slash (/),
    hyphen (-), or period (.). Ensures consistent separator usage throughout
    the date string. Similar to ISO 8601 but allows alternative separators.
    
    Pattern Components
    ------------------
    - Year: 1900-2099 (4-digit format only)
    - Separator: / or - or . (must be consistent)
    - Month: 01-12 (zero-padded, validates range)
    - Day: 01-31 (zero-padded, validates range)
    
    Examples
    --------
    Valid: "2023/12/25", "1995-07-03", "2000.01.31"
    Invalid: "23/12/25", "2023/13/01", "2023-12-32"
    
    Notes
    -----
    This pattern does NOT validate actual calendar dates (e.g., Feb 30th
    will match the pattern but is not a real date). Use with datetime
    parsing for full validation.
    """

    DATE_US: re.Pattern = re.compile(
        r'^(0[1-9]|1[1,2])(\/|-|\.)(0[1-9]|[12][0-9]|3[01])\2(19\d{2}|20\d{2})$')
    """Matches dates in US-style format (MM/DD/YYYY).

    Accepts month-first format with flexible separators: forward slash (/),
    hyphen (-), or period (.). Ensures consistent separator usage throughout
    the date string.

    Pattern Components
    ------------------
    - Month: 01-12 (zero-padded, validates range)
    - Separator: / or - or . (must be consistent)
    - Day: 01-31 (zero-padded, validates range)
    - Year: 1900-2099 (4-digit format only)

    Examples
    --------
    Valid: "12/25/2023", "07-03-1995", "01.31.2000"
    Invalid: "13/25/2023", "07/32/1995", "01.31.23"

    Notes
    -----
    This pattern does NOT validate actual calendar dates (e.g., Feb 30th
    will match the pattern but is not a real date). Use with datetime
    parsing for full validation.
    """

    TIME: re.Pattern = re.compile(
        r'^(?:[01]\d|2[0-3]):[0-5]\d(?::[0-5]\d)?(?:\s?[APap][Mm])?$')
    """Matches valid time formats.

    Accepts both 24-hour format (HH:MM or HH:MM:SS) and 12-hour format
    with optional AM/PM suffix. Validates hour, minute, and optional
    seconds components.

    Pattern Components
    ------------------
    - Hour: 00-23 (24-hour format) or 01-12 (12-hour format, zero-padded)
    - Minute: 00-59 (zero-padded)
    - Second: 00-59 (zero-padded, optional)
    - AM/PM: Optional, case-insensitive, with optional leading space

    Examples
    --------
    Valid: "14:30", "09:15:45 AM", "23:59"
    Invalid: "24:00", "12:60", "12:30 PM AM"
    """

    NUMERIC: re.Pattern = re.compile(r'^\d+(\.\d+)?$')
    """Matches valid numeric values (integers and decimals)."""

    ALPHANUMERIC: re.Pattern = re.compile(r'^[a-zA-Z0-9]+$')
    """Matches valid alphanumeric values (letters and numbers)."""

REGEX = _RegexPattern_()
"""Container for precompiled regular expressions."""