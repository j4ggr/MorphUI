"""
Dynamic color management system for MorphUI

This module provides a dynamic color system that automatically updates
all widget colors when switching between light and dark themes.
"""
from typing import Any
from typing import Tuple
from typing import Literal

from kivy.utils import colormap
from kivy.utils import hex_colormap
from kivy.utils import get_color_from_hex
from kivy.properties import StringProperty
from kivy.properties import OptionProperty
from kivy.properties import BooleanProperty
from kivy.properties import BoundedNumericProperty

from material_color_utilities import Theme
from material_color_utilities import Variant
from material_color_utilities import DynamicScheme
from material_color_utilities import theme_from_color

from morphui.constants import THEME

from morphui.theme.palette import MorphDynamicColorPalette

__all__ = [
    'ThemeManager',]


def get_available_seed_colors() -> Tuple[str, ...]:
    """Get a tuple of all available seed color names."""
    return tuple(
        color.capitalize() for color in hex_colormap.keys())


class ThemeManager(MorphDynamicColorPalette):
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

    color_scheme: str = OptionProperty('VIBRANT', options=THEME.SCHEMES)
    """The color scheme used for generating dynamic colors.

    This property determines the algorithm used to generate colors
    based on the primary color. Available shemes are defined in
    :obj:`morphui.constants.THEME.SCHEMES`.

    :attr:`color_scheme` is a :class:`~kivy.properties.OptionProperty`
    and defaults to 'VIBRANT'.
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

    This property determines the base colors for surfaces, text, and
    other UI elements. Changing this property will automatically update
    all widgets that have `auto_theme` enabled.

    :attr:`theme_mode` is a :class:`~kivy.properties.OptionProperty`
    and defaults to THEME.LIGHT.
    """
    
    # TODO: Implement smooth transitions when switching modes at layers, but i think we need a flag when switching mode was triggered by user or programatically
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
    
    _cached_theme: Theme | None = None
    """Cached theme containing both light and dark schemes."""

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.register_event_type('on_theme_changed')
        self.register_event_type('on_colors_updated')
        
        self.bind(
            seed_color=self._regenerate_theme,
            color_scheme=self._regenerate_theme,
            color_scheme_contrast=self._regenerate_theme,
            color_quality=self._regenerate_theme,
            theme_mode=self._switch_theme_mode)

        self.refresh_theme_colors()

    @property
    def available_seed_colors(self) -> Tuple[str, ...]:
        """List of available seed colors (read-only)."""
        return self._available_seed_colors
    
    @property
    def is_dark_mode(self) -> bool:
        """Check if the current theme mode is dark (read-only)."""
        return self.theme_mode == THEME.DARK

    @property
    def inverse_mode(self) -> Literal['Light', 'Dark']:
        """Get the inverse theme mode (read-only).
        
        Returns the opposite of the current theme_mode. If current mode
        is 'Light', returns 'Dark', and vice versa.
        """
        return THEME.LIGHT if self.is_dark_mode else THEME.DARK
    
    @property
    def cached_theme(self) -> Theme | None:
        """Get the currently cached theme (read-only).
        
        Returns the cached theme object containing both light and dark
        schemes, or None if no theme is cached. This is useful for
        debugging and understanding the internal state.
        
        Returns
        -------
        Theme | None
            The cached theme object or None if not cached.
        """
        return self._cached_theme

    @property  
    def light_scheme(self) -> DynamicScheme:
        """Get the light scheme from cached theme."""
        if self._cached_theme is None:
            self._cached_theme = self._generate_theme(False)
        return self._cached_theme.schemes.light
    
    @property
    def dark_scheme(self) -> DynamicScheme:
        """Get the dark scheme from cached theme.""" 
        if self._cached_theme is None:
            self._cached_theme = self._generate_theme(False)
        return self._cached_theme.schemes.dark
    
    @property
    def current_scheme(self) -> DynamicScheme:
        """Get the current scheme based on theme mode."""
        return self.dark_scheme if self.is_dark_mode else self.light_scheme

    def toggle_theme_mode(self, *args) -> None:
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

    def switch_to_light(self, *args) -> None:
        """Switch to light theme mode.
        
        Sets the theme_mode to 'Light'. If already in light mode,
        this method has no effect. The transition will be animated
        if `mode_transition` is enabled.
        """
        self.theme_mode = THEME.LIGHT

    def switch_to_dark(self, *args) -> None:
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
        property is updated. It is bound to the `on_theme_changed` event 
        which regenerates the color scheme and updates all dynamic 
        colors accordingly.

        Parameters
        ----------
        instance : Any
            The instance that triggered the event (usually self).
        seed_color : str
            The new seed color value.
        """
        _seed_color = seed_color.lower().capitalize()
        if _seed_color != seed_color:
            self.seed_color = _seed_color
            return
        
        assert seed_color in self.available_seed_colors, (
            f'Seed color {seed_color!r} is not registered. Use '
            'register_seed_color() to add it. Available colors: '
            f'{self.available_seed_colors}')
    
    def _regenerate_theme(self, *args) -> None:
        """Regenerate the theme when core properties change.
        
        This method is called when properties that affect the entire theme
        change (seed_color, color_scheme, contrast_level, etc.). It clears
        the cached theme and generates a new one.
        """
        if not self.auto_theme and self.colors_initialized:
            return
            
        self._cached_theme = self._generate_theme(bypass_cache=True)
        self._apply_current_scheme()
    
    def _switch_theme_mode(self, *args) -> None:
        """Efficiently switch between light and dark modes.
        
        This method is called when only theme_mode changes. It uses the
        cached theme if available, avoiding unnecessary regeneration.
        If no cached theme exists, it generates one.
        """
        if not self.auto_theme and self.colors_initialized:
            return
            
        self._cached_theme = self._generate_theme(bypass_cache=False)
        self._apply_current_scheme()

    def _generate_theme(self, bypass_cache: bool) -> Theme:
        """Generate theme and apply the current scheme.

        This method creates a new theme based on the current seed color,
        color scheme, and contrast level. If a cached theme already 
        exists, it is reused to avoid unnecessary computation.

        Parameters
        ----------
        bypass_cache : bool
            If True, forces regeneration of the theme even if a cached 
            version exists.

        Returns
        -------
        Theme
            The generated or cached theme object containing both light 
            and dark schemes.
        """
        if self._cached_theme is None or bypass_cache:
            hex_color = hex_colormap[self.seed_color.lower()]
            variant = getattr(Variant, self.color_scheme)
            
            theme = theme_from_color(
                source=hex_color,
                contrast_level=self.color_scheme_contrast,
                variant=variant)
        else:
            theme = self._cached_theme
        
        self.dispatch('on_theme_changed')
        return theme
    
    def _apply_current_scheme(self) -> None:
        """Apply the current scheme (light or dark) from cached theme.
        
        This method updates all dynamic color properties based on the
        current theme mode (light or dark). It retrieves the appropriate
        scheme from the cached theme and sets all color attributes
        accordingly."""
        if self._cached_theme is None:
            return

        for attr_name, scheme_property in self.material_color_map.items():
            print(attr_name, scheme_property)
            if hasattr(self.current_scheme, scheme_property):
                hex_color = getattr(self.current_scheme, scheme_property)
                rgba = list(get_color_from_hex(hex_color))
                setattr(self, attr_name, rgba)

        if self.auto_theme:
            self.dispatch('on_colors_updated')
    
    def refresh_theme_colors(self) -> None:
        """Manually refresh and apply the current theme colors.

        This method can be called to force a refresh of all dynamic
        colors based on the current theme settings. It is useful when
        multiple properties have been changed and you want to apply the
        changes immediately.

        Examples
        --------
        ```python
        theme_manager.seed_color = 'Red'
        theme_manager.color_scheme = 'VIBRANT'
        theme_manager.refresh_theme_colors()  # Manual refresh
        ```
        """
        auto_theme = self.auto_theme
        self.auto_theme = True
        self._cached_theme = self._generate_theme(bypass_cache=True)
        self._apply_current_scheme()
        self.auto_theme = auto_theme

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
        pass

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
            self.surface_color = theme_manager.background_color
            self.content_color = theme_manager.content_background_color

        theme_manager.bind(on_colors_updated=update_widget_colors)
        ```
        """
        pass
