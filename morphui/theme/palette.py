from typing import List
from typing import Dict
from typing import Tuple
from typing import Generator

from materialyoucolor.dynamiccolor.dynamic_color import DynamicColor
from materialyoucolor.dynamiccolor.material_dynamic_colors import MaterialDynamicColors

from kivy.event import EventDispatcher
from kivy.properties import ColorProperty


__all__ = [
    'MorphDynamicColorPalette',]


def attribute_name_for_color(color: DynamicColor) -> str:
    """
    Generate a valid attribute name for a DynamicColor instance.

    Returns the color's name as a string, ensuring it ends with 
    '_color'. If the input name already ends with '_color', it is 
    returned unchanged; otherwise, '_color' is appended to the name.
    
    Special handling for names starting with 'on_' to avoid conflicts
    with Kivy's event handling system by prefixing them with 'text_'.

    Parameters
    ----------
    color : DynamicColor
        The DynamicColor instance whose name is used.

    Returns
    -------
    str
        The attribute name in the format '<name>_color'.
    """
    name = str(color.name)
    
    # Handle 'on_' prefix to avoid Kivy event handler conflicts
    if name.startswith('on_'):
        # Convert 'on_background' -> 'text_background_color'
        # Convert 'on_primary' -> 'text_primary_color'
        name = 'text_' + name[3:]  # Remove 'on_' and add 'text_'
    
    if not name.endswith('_color'):
        name += '_color'
    return name


def material_dynamic_color_attributes(
        ) -> Generator[Tuple[str, DynamicColor], None, None]:
    """
    Generator yielding attribute names and DynamicColor instances from 
    MaterialDynamicColors.

    Yields tuples containing the attribute name (as a string) and the 
    corresponding DynamicColor instance for each attribute in 
    MaterialDynamicColors that is an instance of DynamicColor.

    Yields
    ------
    Generator[Tuple[str, DynamicColor], None, None]
        Tuples of (attribute_name, DynamicColor instance).
    """
    for attr in dir(MaterialDynamicColors):
        color = getattr(MaterialDynamicColors, attr)
        if isinstance(color, DynamicColor):
            yield (attribute_name_for_color(color), color)


class MorphDynamicColorPalette(EventDispatcher):
    """A comprehensive dynamic color palette class for MorphUI themes, 
    providing a wide range of color properties based on Material Design 
    guidelines. Each property is a Kivy `ColorProperty` that holds a 
    dynamic color value, allowing for flexible and adaptive theming.

    Attributes
    ----------
    material_color_map : Dict[str, DynamicColor]
        Maps color property names to MaterialDynamicColors instances for 
        easy reference and dynamic color scheme application.
    Key color properties:
        The following attributes represent key colors for palettes and
        UI elements, each as a `ColorProperty`:
        - primary_palette_key_color, secondary_palette_key_color,
          tertiary_palette_key_color
        - neutral_palette_key_color, neutral_variant_palette_key_color
    Core UI colors:
        - background_color, text_background_color
        - surface_color, surface_dim_color, surface_bright_color
        - surface_container_lowest_color, surface_container_low_color,
          surface_container_color
        - surface_container_high_color, surface_container_highest_color
        - text_surface_color, surface_variant_color,
          text_surface_variant_color
        - inverse_surface_color, inverse_on_surface_color
    Outline and shadow colors:
        - outline_color, outline_variant_color
        - shadow_color, scrim_color
    Tint and accent colors:
        - surface_tint_color
    Primary, secondary, tertiary, and error colors
        (and their containers and text variants)
        - primary_color, text_primary_color, primary_container_color,
          text_primary_container_color, inverse_primary_color
        - secondary_color, text_secondary_color,
          secondary_container_color, text_secondary_container_color
        - tertiary_color, text_tertiary_color, tertiary_container_color,
          text_tertiary_container_color
        - error_color, text_error_color, error_container_color,
          text_error_container_color
    Fixed palette colors for accessibility and contrast:
        - primary_fixed_color, primary_fixed_dim_color,
          text_primary_fixed_color, text_primary_fixed_variant_color
        - secondary_fixed_color, secondary_fixed_dim_color,
          text_secondary_fixed_color, text_secondary_fixed_variant_color
        - tertiary_fixed_color, tertiary_fixed_dim_color,
          text_tertiary_fixed_color, text_tertiary_fixed_variant_color
    
    Notes
    -----
    Material You colors starting with 'on_' (like 'on_background', 
    'on_primary') are renamed to 'text_' prefixed variants (like 
    'text_background_color', 'text_primary_color') to avoid conflicts 
    with Kivy's event handling system which treats attributes starting 
    with 'on_' as event handlers.
    
    Usage
    -----
    Use this class to define and manage dynamic theme colors for 
    MorphUI-based applications, ensuring consistency and adaptability 
    across different UI components and states.
    """

    _material_color_map: Dict[str, DynamicColor] = dict(
        material_dynamic_color_attributes())
    """Mapping of color property names to MaterialDynamicColors instances."""

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

    @property
    def material_color_map(self) -> Dict[str, DynamicColor]:
        """Get the mapping of color property names to Material Design colors (read-only).
        
        Returns a dictionary where:
        - Keys are color property names (e.g., 'primary_color', 'background_color')
        - Values are the corresponding MaterialDynamicColors DynamicColor instances
        
        This mapping is used internally to apply color schemes to all available
        color properties.
        """
        return self._material_color_map
    
    @property
    def dynamic_color_properties(self) -> List[str]:
        """List of all dynamic color property names in the palette.
        
        This property returns a list of strings representing the names
        of all dynamic color properties defined in the palette. These
        names correspond to the attributes that hold dynamic color
        values, allowing for easy iteration and management of colors.
        
        Returns
        -------
        list of str
            List of dynamic color property names.
            
        Examples
        --------
        ```python
        # Iterate over all dynamic color properties
        for color_prop in theme_manager.dynamic_color_properties:
            print(color_prop)
        ```
        """
        return list(self._material_color_map.keys())
    
    @property
    def colors_initialized(self) -> bool:
        """Check if dynamic colors have been initialized.
        
        Returns True if at least one color property has been set with
        a non-None value, indicating that the color scheme has been
        applied. Returns False if all color properties are None.
        
        Returns
        -------
        bool
            True if colors are initialized, False otherwise.
            
        Examples
        --------
        ```python
        # Check if colors are set before using them
        if theme_manager.colors_initialized:
            widget.background_color = theme_manager.background_color
        else:
            # Use fallback colors or initialize the theme
            theme_manager.update_colors()
        ```
        """
        # Check a few key color properties to determine if colors are set
        
        key_colors = [
            getattr(self, 'primary_color', None),
            getattr(self, 'background_color', None), 
            getattr(self, 'surface_color', None),
            getattr(self, 'on_surface_color', None)
        ]
        return any(color is not None for color in key_colors)
    
    @property
    def all_colors_set(self) -> bool:
        """Check if all color properties have been initialized.
        
        Returns True only if all color properties in the palette have
        been set with non-None values. This is a more strict check than
        `colors_initialized`.
        
        Returns
        -------
        bool
            True if all colors are set, False if any are None.
        """
        for attr_name in self._material_color_map.keys():
            color_value = getattr(self, attr_name, None)
            if color_value is None:
                return False
        return True 

    background_color: List[float] | None = ColorProperty(None)
    """Background color.
    This property holds the dynamic color value set by the theme.

    :attr:`background_color` is a
    :class:`~kivy.properties.ColorProperty` that holds a dynamic color
    value and defaults to None"""

    error_color: List[float] | None = ColorProperty(None)
    """Error color.
    This property holds the dynamic color value set by the theme.

    :attr:`error_color` is a
    :class:`~kivy.properties.ColorProperty` that holds a dynamic color
    value and defaults to None"""

    error_container_color: List[float] | None = ColorProperty(None)
    """Error container color.
    This property holds the dynamic color value set by the theme.

    :attr:`error_container_color` is a
    :class:`~kivy.properties.ColorProperty` that holds a dynamic color
    value and defaults to None"""

    inverse_on_surface_color: List[float] | None = ColorProperty(None)
    """Inverse on surface color.
    This property holds the dynamic color value set by the theme.

    :attr:`inverse_on_surface_color` is a
    :class:`~kivy.properties.ColorProperty` that holds a dynamic color
    value and defaults to None"""

    inverse_primary_color: List[float] | None = ColorProperty(None)
    """Inverse primary color.
    This property holds the dynamic color value set by the theme.

    :attr:`inverse_primary_color` is a
    :class:`~kivy.properties.ColorProperty` that holds a dynamic color
    value and defaults to None"""

    inverse_surface_color: List[float] | None = ColorProperty(None)
    """Inverse surface color.
    This property holds the dynamic color value set by the theme.

    :attr:`inverse_surface_color` is a
    :class:`~kivy.properties.ColorProperty` that holds a dynamic color
    value and defaults to None"""

    neutral_palette_key_color: List[float] | None = ColorProperty(None)
    """Neutral palette key color.
    This property holds the dynamic color value set by the theme.

    :attr:`neutral_palette_key_color` is a
    :class:`~kivy.properties.ColorProperty` that holds a dynamic color
    value and defaults to None"""

    neutral_variant_palette_key_color: List[float] | None = ColorProperty(None)
    """Neutral variant palette key color.
    This property holds the dynamic color value set by the theme.

    :attr:`neutral_variant_palette_key_color` is a
    :class:`~kivy.properties.ColorProperty` that holds a dynamic color
    value and defaults to None"""

    text_background_color: List[float] | None = ColorProperty(None)
    """Text background color.
    This property holds the dynamic color value set by the theme.

    :attr:`text_background_color` is a
    :class:`~kivy.properties.ColorProperty` that holds a dynamic color
    value and defaults to None"""

    text_error_color: List[float] | None = ColorProperty(None)
    """Text error color.
    This property holds the dynamic color value set by the theme.

    :attr:`text_error_color` is a
    :class:`~kivy.properties.ColorProperty` that holds a dynamic color
    value and defaults to None"""

    text_error_container_color: List[float] | None = ColorProperty(None)
    """Text error container color.
    This property holds the dynamic color value set by the theme.

    :attr:`text_error_container_color` is a
    :class:`~kivy.properties.ColorProperty` that holds a dynamic color
    value and defaults to None"""

    text_primary_color: List[float] | None = ColorProperty(None)
    """Text primary color.
    This property holds the dynamic color value set by the theme.

    :attr:`text_primary_color` is a
    :class:`~kivy.properties.ColorProperty` that holds a dynamic color
    value and defaults to None"""

    text_primary_container_color: List[float] | None = ColorProperty(None)
    """Text primary container color.
    This property holds the dynamic color value set by the theme.

    :attr:`text_primary_container_color` is a
    :class:`~kivy.properties.ColorProperty` that holds a dynamic color
    value and defaults to None"""

    text_primary_fixed_color: List[float] | None = ColorProperty(None)
    """Text primary fixed color.
    This property holds the dynamic color value set by the theme.

    :attr:`text_primary_fixed_color` is a
    :class:`~kivy.properties.ColorProperty` that holds a dynamic color
    value and defaults to None"""

    text_primary_fixed_variant_color: List[float] | None = ColorProperty(None)
    """Text primary fixed variant color.
    This property holds the dynamic color value set by the theme.

    :attr:`text_primary_fixed_variant_color` is a
    :class:`~kivy.properties.ColorProperty` that holds a dynamic color
    value and defaults to None"""

    text_secondary_color: List[float] | None = ColorProperty(None)
    """Text secondary color.
    This property holds the dynamic color value set by the theme.

    :attr:`text_secondary_color` is a
    :class:`~kivy.properties.ColorProperty` that holds a dynamic color
    value and defaults to None"""

    text_secondary_container_color: List[float] | None = ColorProperty(None)
    """Text secondary container color.
    This property holds the dynamic color value set by the theme.

    :attr:`text_secondary_container_color` is a
    :class:`~kivy.properties.ColorProperty` that holds a dynamic color
    value and defaults to None"""

    text_secondary_fixed_color: List[float] | None = ColorProperty(None)
    """Text secondary fixed color.
    This property holds the dynamic color value set by the theme.

    :attr:`text_secondary_fixed_color` is a
    :class:`~kivy.properties.ColorProperty` that holds a dynamic color
    value and defaults to None"""

    text_secondary_fixed_variant_color: List[float] | None = ColorProperty(None)
    """Text secondary fixed variant color.
    This property holds the dynamic color value set by the theme.

    :attr:`text_secondary_fixed_variant_color` is a
    :class:`~kivy.properties.ColorProperty` that holds a dynamic color
    value and defaults to None"""

    text_surface_color: List[float] | None = ColorProperty(None)
    """Text surface color.
    This property holds the dynamic color value set by the theme.

    :attr:`text_surface_color` is a
    :class:`~kivy.properties.ColorProperty` that holds a dynamic color
    value and defaults to None"""

    text_surface_variant_color: List[float] | None = ColorProperty(None)
    """Text surface variant color.
    This property holds the dynamic color value set by the theme.

    :attr:`text_surface_variant_color` is a
    :class:`~kivy.properties.ColorProperty` that holds a dynamic color
    value and defaults to None"""

    text_tertiary_color: List[float] | None = ColorProperty(None)
    """Text tertiary color.
    This property holds the dynamic color value set by the theme.

    :attr:`text_tertiary_color` is a
    :class:`~kivy.properties.ColorProperty` that holds a dynamic color
    value and defaults to None"""

    text_tertiary_container_color: List[float] | None = ColorProperty(None)
    """Text tertiary container color.
    This property holds the dynamic color value set by the theme.

    :attr:`text_tertiary_container_color` is a
    :class:`~kivy.properties.ColorProperty` that holds a dynamic color
    value and defaults to None"""

    text_tertiary_fixed_color: List[float] | None = ColorProperty(None)
    """Text tertiary fixed color.
    This property holds the dynamic color value set by the theme.

    :attr:`text_tertiary_fixed_color` is a
    :class:`~kivy.properties.ColorProperty` that holds a dynamic color
    value and defaults to None"""

    text_tertiary_fixed_variant_color: List[float] | None = ColorProperty(None)
    """Text tertiary fixed variant color.
    This property holds the dynamic color value set by the theme.

    :attr:`text_tertiary_fixed_variant_color` is a
    :class:`~kivy.properties.ColorProperty` that holds a dynamic color
    value and defaults to None"""

    outline_color: List[float] | None = ColorProperty(None)
    """Outline color.
    This property holds the dynamic color value set by the theme.

    :attr:`outline_color` is a
    :class:`~kivy.properties.ColorProperty` that holds a dynamic color
    value and defaults to None"""

    outline_variant_color: List[float] | None = ColorProperty(None)
    """Outline variant color.
    This property holds the dynamic color value set by the theme.

    :attr:`outline_variant_color` is a
    :class:`~kivy.properties.ColorProperty` that holds a dynamic color
    value and defaults to None"""

    primary_color: List[float] | None = ColorProperty(None)
    """Primary color.
    This property holds the dynamic color value set by the theme.

    :attr:`primary_color` is a
    :class:`~kivy.properties.ColorProperty` that holds a dynamic color
    value and defaults to None"""

    primary_container_color: List[float] | None = ColorProperty(None)
    """Primary container color.
    This property holds the dynamic color value set by the theme.

    :attr:`primary_container_color` is a
    :class:`~kivy.properties.ColorProperty` that holds a dynamic color
    value and defaults to None"""

    primary_fixed_color: List[float] | None = ColorProperty(None)
    """Primary fixed color.
    This property holds the dynamic color value set by the theme.

    :attr:`primary_fixed_color` is a
    :class:`~kivy.properties.ColorProperty` that holds a dynamic color
    value and defaults to None"""

    primary_fixed_dim_color: List[float] | None = ColorProperty(None)
    """Primary fixed dim color.
    This property holds the dynamic color value set by the theme.

    :attr:`primary_fixed_dim_color` is a
    :class:`~kivy.properties.ColorProperty` that holds a dynamic color
    value and defaults to None"""

    primary_palette_key_color: List[float] | None = ColorProperty(None)
    """Primary palette key color.
    This property holds the dynamic color value set by the theme.

    :attr:`primary_palette_key_color` is a
    :class:`~kivy.properties.ColorProperty` that holds a dynamic color
    value and defaults to None"""

    scrim_color: List[float] | None = ColorProperty(None)
    """Scrim color.
    This property holds the dynamic color value set by the theme.

    :attr:`scrim_color` is a
    :class:`~kivy.properties.ColorProperty` that holds a dynamic color
    value and defaults to None"""

    secondary_color: List[float] | None = ColorProperty(None)
    """Secondary color.
    This property holds the dynamic color value set by the theme.

    :attr:`secondary_color` is a
    :class:`~kivy.properties.ColorProperty` that holds a dynamic color
    value and defaults to None"""

    secondary_container_color: List[float] | None = ColorProperty(None)
    """Secondary container color.
    This property holds the dynamic color value set by the theme.

    :attr:`secondary_container_color` is a
    :class:`~kivy.properties.ColorProperty` that holds a dynamic color
    value and defaults to None"""

    secondary_fixed_color: List[float] | None = ColorProperty(None)
    """Secondary fixed color.
    This property holds the dynamic color value set by the theme.

    :attr:`secondary_fixed_color` is a
    :class:`~kivy.properties.ColorProperty` that holds a dynamic color
    value and defaults to None"""

    secondary_fixed_dim_color: List[float] | None = ColorProperty(None)
    """Secondary fixed dim color.
    This property holds the dynamic color value set by the theme.

    :attr:`secondary_fixed_dim_color` is a
    :class:`~kivy.properties.ColorProperty` that holds a dynamic color
    value and defaults to None"""

    secondary_palette_key_color: List[float] | None = ColorProperty(None)
    """Secondary palette key color.
    This property holds the dynamic color value set by the theme.

    :attr:`secondary_palette_key_color` is a
    :class:`~kivy.properties.ColorProperty` that holds a dynamic color
    value and defaults to None"""

    shadow_color: List[float] | None = ColorProperty(None)
    """Shadow color.
    This property holds the dynamic color value set by the theme.

    :attr:`shadow_color` is a
    :class:`~kivy.properties.ColorProperty` that holds a dynamic color
    value and defaults to None"""

    surface_color: List[float] | None = ColorProperty(None)
    """Surface color.
    This property holds the dynamic color value set by the theme.

    :attr:`surface_color` is a
    :class:`~kivy.properties.ColorProperty` that holds a dynamic color
    value and defaults to None"""

    surface_bright_color: List[float] | None = ColorProperty(None)
    """Surface bright color.
    This property holds the dynamic color value set by the theme.

    :attr:`surface_bright_color` is a
    :class:`~kivy.properties.ColorProperty` that holds a dynamic color
    value and defaults to None"""

    surface_container_color: List[float] | None = ColorProperty(None)
    """Surface container color.
    This property holds the dynamic color value set by the theme.

    :attr:`surface_container_color` is a
    :class:`~kivy.properties.ColorProperty` that holds a dynamic color
    value and defaults to None"""

    surface_container_high_color: List[float] | None = ColorProperty(None)
    """Surface container high color.
    This property holds the dynamic color value set by the theme.

    :attr:`surface_container_high_color` is a
    :class:`~kivy.properties.ColorProperty` that holds a dynamic color
    value and defaults to None"""

    surface_container_highest_color: List[float] | None = ColorProperty(None)
    """Surface container highest color.
    This property holds the dynamic color value set by the theme.

    :attr:`surface_container_highest_color` is a
    :class:`~kivy.properties.ColorProperty` that holds a dynamic color
    value and defaults to None"""

    surface_container_low_color: List[float] | None = ColorProperty(None)
    """Surface container low color.
    This property holds the dynamic color value set by the theme.

    :attr:`surface_container_low_color` is a
    :class:`~kivy.properties.ColorProperty` that holds a dynamic color
    value and defaults to None"""

    surface_container_lowest_color: List[float] | None = ColorProperty(None)
    """Surface container lowest color.
    This property holds the dynamic color value set by the theme.

    :attr:`surface_container_lowest_color` is a
    :class:`~kivy.properties.ColorProperty` that holds a dynamic color
    value and defaults to None"""

    surface_dim_color: List[float] | None = ColorProperty(None)
    """Surface dim color.
    This property holds the dynamic color value set by the theme.

    :attr:`surface_dim_color` is a
    :class:`~kivy.properties.ColorProperty` that holds a dynamic color
    value and defaults to None"""

    surface_tint_color: List[float] | None = ColorProperty(None)
    """Surface tint color.
    This property holds the dynamic color value set by the theme.

    :attr:`surface_tint_color` is a
    :class:`~kivy.properties.ColorProperty` that holds a dynamic color
    value and defaults to None"""

    surface_variant_color: List[float] | None = ColorProperty(None)
    """Surface variant color.
    This property holds the dynamic color value set by the theme.

    :attr:`surface_variant_color` is a
    :class:`~kivy.properties.ColorProperty` that holds a dynamic color
    value and defaults to None"""

    tertiary_color: List[float] | None = ColorProperty(None)
    """Tertiary color.
    This property holds the dynamic color value set by the theme.

    :attr:`tertiary_color` is a
    :class:`~kivy.properties.ColorProperty` that holds a dynamic color
    value and defaults to None"""

    tertiary_container_color: List[float] | None = ColorProperty(None)
    """Tertiary container color.
    This property holds the dynamic color value set by the theme.

    :attr:`tertiary_container_color` is a
    :class:`~kivy.properties.ColorProperty` that holds a dynamic color
    value and defaults to None"""

    tertiary_fixed_color: List[float] | None = ColorProperty(None)
    """Tertiary fixed color.
    This property holds the dynamic color value set by the theme.

    :attr:`tertiary_fixed_color` is a
    :class:`~kivy.properties.ColorProperty` that holds a dynamic color
    value and defaults to None"""

    tertiary_fixed_dim_color: List[float] | None = ColorProperty(None)
    """Tertiary fixed dim color.
    This property holds the dynamic color value set by the theme.

    :attr:`tertiary_fixed_dim_color` is a
    :class:`~kivy.properties.ColorProperty` that holds a dynamic color
    value and defaults to None"""

    tertiary_palette_key_color: List[float] | None = ColorProperty(None)
    """Tertiary palette key color.
    This property holds the dynamic color value set by the theme.

    :attr:`tertiary_palette_key_color` is a
    :class:`~kivy.properties.ColorProperty` that holds a dynamic color
    value and defaults to None"""


if __name__ == '__main__':
    for attr, _ in material_dynamic_color_attributes():
        print(f'''
    {attr}: List[float] | None = ColorProperty(None)
    """{" ".join(attr.capitalize().split("_"))}.
    This property holds the dynamic color value set by the theme.

    :attr:`{attr}` is a
    :class:`~kivy.properties.ColorProperty` that holds a dynamic color
    value and defaults to None"""''')
