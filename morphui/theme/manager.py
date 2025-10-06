"""
Dynamic color management system for MorphUI

This module provides a dynamic color system that automatically updates
all widget colors when switching between light and dark themes.
"""
from typing import Any
from typing import List
from typing import Dict
from typing import Type
from typing import Tuple
from typing import Literal
from typing import overload

from kivy.utils import colormap
from kivy.utils import hex_colormap
from kivy.event import EventDispatcher
from kivy.utils import get_color_from_hex
from kivy.properties import StringProperty
from kivy.properties import OptionProperty
from kivy.properties import BooleanProperty
from kivy.properties import BoundedNumericProperty

from materialyoucolor.hct import Hct
from materialyoucolor.utils.color_utils import argb_from_rgba
from materialyoucolor.utils.platform_utils import SCHEMES
from materialyoucolor.utils.platform_utils import get_dynamic_scheme
from materialyoucolor.scheme.dynamic_scheme import DynamicScheme
from materialyoucolor.dislike.dislike_analyzer import DislikeAnalyzer

from ..constants import THEME

from .._typing import MaterialDynamicScheme

from .palette import MorphDynamicColorPalette

__all__ = [
    'ThemeManager',]


def get_available_seed_colors() -> Tuple[str, ...]:
    """Get a tuple of all available seed color names."""
    return tuple(
        color.capitalize() for color in hex_colormap.keys())


class ThemeManager(EventDispatcher, MorphDynamicColorPalette):
    """Manage the theme and dynamic colors for the application.
    
    This class handles the overall theme management, including
    switching between light and dark modes. It automatically
    updates colors for all widgets that have `auto_theme` enabled.
    """

    auto_theme: bool = BooleanProperty(True)
    """Enable automatic theme updates across all widgets.

    When True, widgets automatically update their colors when the theme 
    changes. When False, widgets retain their current colors until 
    manually updated.

    :attr:`auto_theme` is a :class:`~kivy.properties.BooleanProperty` 
    and defaults to True.
    """

    seed_color: str = StringProperty('Blue')
    """The seed color used to generate the dynamic color palette.

    This property sets the source color from which all other theme 
    colors are generated using the Material You color system. Changing 
    this property will regenerate the entire color palette and 
    automatically update all widgets that have `auto_theme` enabled.

    :attr:`seed_color` is a :class:`~kivy.properties.OptionProperty`
    and defaults to 'Blue'.
    """

    color_scheme: str = OptionProperty('FIDELITY', options=THEME.SCHEMES)
    """The color scheme used for generating dynamic colors.

    This property determines the algorithm used to generate colors
    based on the primary color. Available shemes are defined in
    :obj:`morphui.constants.THEME.SCHEMES`.

    :attr:`color_scheme` is a :class:`~kivy.properties.OptionProperty`
    and defaults to 'FIDELITY'.
    """

    color_scheme_contrast: float = BoundedNumericProperty(
        0.0, min=0.0, max=1.0, errorhandler=lambda x: max(0.0, min(x, 1.0)))
    """Adjusts the contrast level of the selected color scheme.

    This property modifies the contrast of the generated color scheme.
    A value of 0 means no adjustment, while 1 applies the maximum
    contrast enhancement.

    :attr:`color_scheme_contrast` is a 
    :class:`~kivy.properties.BoundedNumericProperty` and defaults to 0.
    """

    color_quality: int = BoundedNumericProperty(1, min=1, errorvalue=1)
    """The quality level for color generation. 

    Must be an integer and higher or equal to 1. Where 1 is the maximum
    quality and higher numbers reduce the quality for performance.
    
    :attr:`color_quality` is a :class:`~kivy.properties.NumericProperty`
    and defaults to 1.
    """

    theme_mode: str = OptionProperty(
        THEME.LIGHT, options=[THEME.LIGHT, THEME.DARK])
    """The overall theme mode, either 'Light' or 'Dark'.

    This property determines the base colors for backgrounds, text, and
    other UI elements. Changing this property will automatically update
    all widgets that have `auto_theme` enabled.

    :attr:`theme_mode` is a :class:`~kivy.properties.OptionProperty`
    and defaults to THEME.LIGHT.
    """

    mode_transition: bool = BooleanProperty(True)
    """Enable smooth transitions when switching between theme modes.

    When True, theme mode changes (light/dark) will be animated with
    smooth color transitions. When False, theme changes happen instantly.

    :attr:`mode_transition` is a :class:`~kivy.properties.BooleanProperty`
    and defaults to True.
    """

    mode_transition_duration: float = BoundedNumericProperty(0.3, min=0.0)
    """Duration of theme mode transition animations in seconds.

    This property controls how long the transition animation takes when
    switching between light and dark modes. Only applies when
    `mode_transition` is True.

    :attr:`mode_transition_duration` is a 
    :class:`~kivy.properties.BoundedNumericProperty` and defaults to 0.3.
    """

    _available_seed_colors: Tuple[str, ...] = get_available_seed_colors()
    """List of available seed colors (read-only)."""

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.register_event_type('on_theme_changed')
        self.register_event_type('on_colors_updated')
        self.bind(on_seed_color=self.on_theme_changed)
        self.bind(on_color_scheme=self.on_theme_changed)
        self.bind(on_color_scheme_contrast=self.on_theme_changed)
        self.bind(on_color_quality=self.on_theme_changed)
        self.bind(on_theme_mode=self.on_theme_changed)

    @property
    def available_seed_colors(self) -> Tuple[str, ...]:
        """List of available seed colors (read-only)."""
        return self._available_seed_colors

    @property
    def inverse_mode(self) -> Literal['Light', 'Dark']:
        """Get the inverse theme mode (read-only).
        
        Returns the opposite of the current theme_mode. If current mode
        is 'Light', returns 'Dark', and vice versa.
        """
        return THEME.DARK if self.theme_mode == THEME.LIGHT else THEME.LIGHT

    @property
    def material_schemes(self) -> Dict[str, Type[MaterialDynamicScheme]]:
        """Get the available Material You color schemes (read-only).
        
        Returns a dictionary of available color scheme classes from
        Material You Color library.
        """
        return SCHEMES

    def toggle_theme_mode(self) -> None:
        """Toggle between light and dark theme modes.
        
        Switches the current theme_mode to its inverse. If currently 
        'Light', switches to 'Dark', and vice versa. The transition will
        be animated if `mode_transition` is enabled.
        
        Examples
        --------
        ```python
        # Simple toggle
        theme_manager.toggle_theme_mode()
        
        # Toggle with custom animation settings
        theme_manager.mode_transition = True
        theme_manager.mode_transition_duration = 0.5
        theme_manager.toggle_theme_mode()
        ```
        """
        self.theme_mode = self.inverse_mode

    def switch_to_light(self) -> None:
        """Switch to light theme mode.
        
        Sets the theme_mode to 'Light'. If already in light mode,
        this method has no effect. The transition will be animated
        if `mode_transition` is enabled.
        """
        self.theme_mode = THEME.LIGHT

    def switch_to_dark(self) -> None:
        """Switch to dark theme mode.
        
        Sets the theme_mode to 'Dark'. If already in dark mode,
        this method has no effect. The transition will be animated
        if `mode_transition` is enabled.
        """
        self.theme_mode = THEME.DARK

    def register_seed_color(self, color_name: str, hex_value: str) -> None:
        """Register a new seed color.

        This method allows adding custom seed colors to the theme.
        The color name must be a valid hex color code (e.g. '#FF5733').

        Parameters
        ----------
        color_name : str
            The name of the new seed color.
        hex_value : str
            The hex color code for the new seed color.

        Examples
        --------
        ```python
        theme_manager.register_seed_color('MyCyan', '#00F0D0')
        theme_manager.seed_color = 'MyCyan'
        ```
        """
        assert hex_value.startswith('#') and len(hex_value) in (7, 9), (
            'hex_value must be a valid hex color code.')
        
        color_name = color_name.lower()
        hex_colormap[color_name] = hex_value
        colormap[color_name] = get_color_from_hex(hex_value)
        self._available_seed_colors = get_available_seed_colors()

    def on_seed_color(self, instance: Any, seed_color: str) -> None:
        """Event handler for when the seed color changes.

        This method is automatically called whenever the `seed_color`
        property is updated. It triggers the `on_theme_changed` event 
        which regenerates the color scheme and updates all dynamic 
        colors accordingly.

        Parameters
        ----------
        instance : Any
            The instance that triggered the event (usually self).
        seed_color : str
            The new seed color value.
        """
        assert seed_color in self.available_seed_colors, (
            f'Seed color {seed_color!r} is not registered. Use '
            'register_seed_color() to add it. Available colors: '
            f'{self.available_seed_colors}')
        self.dispatch('on_theme_changed')

    def on_theme_changed(self, *args) -> None:
        """Handle theme changes and update all colors based on current 
        settings.

        This method is automatically called whenever theme properties 
        change (seed_color, color_scheme, theme_mode, etc.) and forces 
        an update of all dynamic colors. It can also be called manually 
        when multiple properties have been changed and you want to apply
        the changes immediately.

        Examples
        --------
        ```python
        theme_manager.seed_color = 'Red'
        theme_manager.color_scheme = 'VIBRANT'
        theme_manager.on_theme_changed()  # Manual trigger if needed
        ```
        """
        if not self.auto_theme and self.colors_initialized:
            return
        
        scheme = self.generate_color_scheme()
        self.apply_color_scheme(scheme)

    @overload
    def get_seed_color_rgba(self, as_float: Literal[True]) -> List[float]:
        ...

    @overload
    def get_seed_color_rgba(
            self, as_float: Literal[False] = False) -> List[int]:
        ...

    def get_seed_color_rgba(
            self, as_float: bool = False) -> List[int] | List[float]:
        """Get the RGBA representation of the seed color.

        This method converts the current seed color from its hex
        representation to RGBA values. The values can be returned as
        either integers (0-255) or floats (0.0-1.0) based on the
        `as_float` parameter.

        Parameters
        ----------
        as_float : bool, optional
            If True, returns RGBA values as floats between 0.0 and 1.0.
            If False, returns RGBA values as integers between 0 and 255.
            Default is False.

        Returns
        -------
        List[int] | List[float]
            A list of 4 RGBA values. If `as_float` is True, returns 
            floats in range [0.0, 1.0]. If False, returns integers in 
            range [0, 255].

        Examples
        --------
        ```python
        # Get integer RGBA values (0-255)
        rgba_int = theme_manager.get_seed_color_rgba()
        # Returns: [33, 150, 243, 255] for blue

        # Get float RGBA values (0.0-1.0) 
        rgba_float = theme_manager.get_seed_color_rgba(as_float=True)
        # Returns: [0.129, 0.588, 0.953, 1.0] for blue
        ```

        Raises
        ------
        KeyError
            If the seed_color is not found in the color map.
        """
        rgba_values = get_color_from_hex(
            hex_colormap[self.seed_color.lower()])
        if as_float:
            return list(rgba_values)
        return [int(component * 255) for component in rgba_values]

    def generate_color_scheme(self) -> DynamicScheme | MaterialDynamicScheme:
        """Create a Material You color scheme based on current theme 
        settings.
        
        This method is the primary interface for generating color 
        schemes in MorphUI. It intelligently chooses between two color 
        generation strategies:
        
        1. **Dynamic Wallpaper-Based Colors** (when `auto_theme=True`):
           Attempts to extract colors from the user's system wallpaper 
           using the Material You Color library. This provides a 
           personalized color experience that adapts to the user's 
           environment and preferences.
        
        2. **Seed Color-Based Colors** (fallback or when 
           `auto_theme=False`):
           Generates colors from the specified `seed_color` using the 
           selected `color_scheme` algorithm. This ensures consistent, 
           predictable theming.
        
        The method automatically respects all current theme settings 
        including theme mode (light/dark), contrast level, color 
        quality, and the selected color scheme algorithm.
        
        Returns
        -------
        DynamicScheme | MaterialDynamicScheme
            A Material You dynamic color scheme object ready for 
            application. The scheme contains all necessary color roles 
            (primary, secondary, surface, etc.) in the appropriate theme 
            mode.
        
        Color Generation Process
        ------------------------
        1. If `auto_theme` is enabled, attempts dynamic wallpaper color 
           extraction
        2. If dynamic extraction fails or is disabled, falls back to 
           seed colors
        3. Applies current contrast level and quality settings
        4. Generates appropriate colors for the current theme mode 
           (light/dark)
        
        Examples
        --------
        ```python
        # Generate scheme with current settings
        theme_manager = ThemeManager()
        scheme = theme_manager.generate_color_scheme()
        
        # Configure settings before generation
        theme_manager.seed_color = 'Purple'
        theme_manager.color_scheme = 'VIBRANT'
        theme_manager.theme_mode = 'Dark'
        theme_manager.color_scheme_contrast = 0.5
        scheme = theme_manager.generate_color_scheme()
        
        # Use with apply_color_scheme
        scheme = theme_manager.generate_color_scheme()
        theme_manager.apply_color_scheme(scheme)
        ```
        
        See Also
        --------
        apply_color_scheme : Apply a generated scheme to update all 
        colors
        on_theme_changed : Event handler that calls this method 
        automatically
        """
        scheme = None
        if self.auto_theme:
            scheme = self._extract_wallpaper_scheme()
        
        if scheme is None:
            scheme = self._generate_seed_scheme()
        return scheme

    def _extract_wallpaper_scheme(
            self,
            ) -> DynamicScheme | MaterialDynamicScheme | None:
        """Extract color scheme from system wallpaper using Material You.

        Returns None if wallpaper-based color extraction is unavailable
        or fails, allowing graceful fallback to seed color generation.
        """
        scheme = get_dynamic_scheme(
            dark_mode=self.theme_mode == THEME.DARK,
            contrast=self.color_scheme_contrast,
            dynamic_color_quality=self.color_quality,
            fallback_wallpaper_path=None, # TODO: add wallpaper support
            fallback_scheme_name=self.color_scheme,
            force_fallback_wallpaper=False,
            message_logger=print, # TODO: Add global logging support
            logger_head='ThemeManager',)
        return scheme

    def _generate_seed_scheme(self) -> DynamicScheme | MaterialDynamicScheme:
        """Generate color scheme from the current seed color.
        
        Uses the specified color_scheme algorithm and applies dislike
        analysis to ensure pleasant color combinations.
        """
        argb = argb_from_rgba(self.get_seed_color_rgba(as_float=False))
        hct = DislikeAnalyzer.fix_if_disliked(Hct.from_int(argb))
        scheme = self.material_schemes[self.color_scheme](
            source_color_hct=hct,
            is_dark=self.theme_mode == THEME.DARK,
            contrast_level=self.color_scheme_contrast,)
        return scheme

    def apply_color_scheme(
            self, scheme: DynamicScheme | MaterialDynamicScheme) -> None:
        """Apply the given color scheme to the theme manager.

        This method updates the theme manager's color properties based on
        the provided color scheme.

        Parameters
        ----------
        scheme : DynamicScheme | MaterialDynamicScheme
            The color scheme to apply.
        """ 
        if not self.auto_theme and self.colors_initialized:
            return

        for attr_name, color in self.material_color_map.items():
            rgba = [c/255 for c in color.get_hct(scheme).to_rgba()]
            setattr(self, attr_name, rgba)

        if self.auto_theme:
            self.dispatch('on_colors_updated')

    def on_colors_updated(self, *args) -> None:
        """Event fired after color properties have been applied.

        This is a more specific event than `on_theme_changed` that fires
        specifically when color values have been calculated and set on
        the theme manager. Use this event when you only need to respond
        to color changes, not other potential theme changes.

        Note: This event only fires when `auto_theme` is True.

        Examples
        --------
        ```python
        def update_widget_colors(self):
            self.background_color = theme_manager.background_color
            self.text_color = theme_manager.on_background_color

        theme_manager.bind(on_colors_updated=update_widget_colors)
        ```
        """
        pass
