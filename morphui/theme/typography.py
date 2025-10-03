"""
Typography system for MorphUI themes
"""
import warnings

from typing import Dict
from typing import Tuple
from typing import Literal
from pathlib import Path

from kivy.event import EventDispatcher
from kivy.core.text import LabelBase
from kivy.properties import StringProperty

from ..constants import FONTS


__all__ = [
    'Typography',]


class Typography(EventDispatcher):
    """Typography system for consistent text styling across MorphUI 
    themes.
    
    Provides a centralized interface for managing typography styles 
    based on Material Design typography guidelines. Handles font 
    registration, style configuration, and automatic fallbacks for
    missing fonts.

    The typography system organizes text into hierarchical roles 
    (Display, Headline, Title, Body, Label) with size variants (large, 
    medium, small) and supports multiple font weights for each family.
    
    Attributes
    ----------
    font_name : str
        Base font family name used for text styling.
    fonts_to_autoregister : Tuple[Dict[str, str], ...]
        Tuple of font registration dictionaries that are automatically
        registered when the typography system is initialized. This
        happens when a new :class:`MorphApp` instance is created.

    Examples
    --------

    To use the typography system, set the desired base font family in
    your application class that inherits from :class:`MorphApp`. The
    default is 'Inter', which uses InterRegular, InterThin, and 
    InterHeavy.

    ```python
    from morphui.app import MorphApp

    class MyApp(MorphApp):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)

        on_start(self):
            # Use DMSansRegular, DMSansThin and DMSansHeavy.
            self.typography.font_name = 'DMSans'  

    app = MyApp()
    app.run()
    ```
    
    To change the auto-registration behavior, you need to modify the
    class attribute :attr:`Typography.fonts_to_autoregister`:
    
    ```python
    from morphui.app import MorphApp
    from morphui.constants import FONTS
    from morphui.theme.typography import Typography

    # Change the auto-registration tuple before app initialization
    # Do not instantiate Typography
    Typography.fonts_to_autoregister = (
        user_font_dict_regular,
        user_font_dict_thin,
        user_font_dict_heavy,
        FONTS.MATERIAL_ICONS,)
    ```

    To register a custom font at runtime, use the
    :meth:`MorphApp.typography.register_font` method within your app 
    class. A good place is in the `on_start` method:

    ```python
    from morphui.app import MorphApp

    class MyApp(MorphApp):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)

        on_start(self):
            # Register custom fonts on app start
            self.typography.register_font(user_font_dict_regular)
            self.typography.register_font(user_font_dict_thin)
            self.typography.register_font(user_font_dict_heavy)

    app = MyApp()
    app.run()
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

    fonts_to_autoregister: Tuple[Dict[str, str], ...] = (
        FONTS.DEFAULT_AUTOREGISTERED_FONTS)
    """Tuple of font registration dictionaries.

    All these fonts are automatically registered when instantiating the
    :class:`MorphApp`. If you need to register additional fonts
    automatically, modify this class attribute before instantiation of
    :class:`MorphApp`. You can also register fonts manually using
    the `register_font` method. Each dictionary should contain the
    following keys:

    - `name`: Unique font family name
    - `fn_regular`: Path to the regular font file
    - `fn_italic`: Path to the italic font file (optional)
    - `fn_bold`: Path to the bold font file (optional)
    - `fn_bolditalic`: Path to the bold italic font file (optional)
    """

    _registered_fonts: Tuple[str, ...]
    """Tuple of currently registered font family names."""

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self._registered_fonts = ()
        self.register_event_type('on_typography_changed')
        self.bind(font_name=self.on_typography_changed)

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
        
        LabelBase.register(
            name=name,
            fn_regular=fn_regular,
            fn_italic=fn_italic,
            fn_bold=fn_bold,
            fn_bolditalic=fn_bolditalic)
        self._registered_fonts += (name,)

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
    
    def on_typography_changed(self, *args) -> None:
        """Event handler called when the `font_name` property changes.
        
        Dispatches the `on_typography_changed` event to notify listeners
        that the typography configuration has changed. This allows UI
        components to react and update their text styles accordingly.
        
        Parameters
        ----------
        *args : tuple
            Additional arguments passed by the property change event.
        
        Examples
        --------
        ```python
        from morphui.app import MorphApp

        def on_typography_changed(self, *args):
            # Update UI components with new typography styles
            new_style = self.typography.get_text_style('Body', 'medium')
            self.label.font_name = new_style['name']
            self.label.font_size = new_style['font_size']
        
        typography = MorphApp.get_running_app().typography
        typography.bind(on_typography_changed=on_typography_changed)
        typography.font_name = 'DMSans'  # Triggers the event
        ```
        
        Notes
        -----
        - This method is automatically called by Kivy when `font_name`
          changes due to the property binding.
        - UI components should bind to this event to refresh their styles.
        """
        pass
