from typing import Dict
from typing import Tuple
from typing import Generator

from materialyoucolor.dynamiccolor.dynamic_color import DynamicColor
from materialyoucolor.dynamiccolor.material_dynamic_colors import MaterialDynamicColors

from kivy.properties import ColorProperty


__all__ = ['MorphDynamicColorPalette']


def attribute_name_for_color(color: DynamicColor) -> str:
    """
    Generate a valid attribute name for a DynamicColor instance.

    Returns the color's name as a string, ensuring it ends with 
    '_color'. If the input name already ends with '_color', it is 
    returned unchanged; otherwise, '_color' is appended to the name.

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


class MorphDynamicColorPalette:
    """A comprehensive dynamic color palette class for MorphUI themes, 
    providing a wide range of color properties based on Material Design 
    guidelines. Each property is a Kivy `ColorProperty` that holds a 
    dynamic color value, allowing for flexible and adaptive theming.

    Attributes
    ----------
    ATTRIBUTE_MAP : Dict[str, DynamicColor]
        Maps attribute names to MaterialDynamicColors attributes for 
        easy reference and dynamic assignment.
    Key color properties:
        The following attributes represent key colors for palettes and
        UI elements, each as a `ColorProperty`:
        - primary_palette_key_color, secondary_palette_key_color,
          tertiary_palette_key_color
        - neutral_palette_key_color, neutral_variant_palette_key_color
    Core UI colors:
        - background_color, on_background_color
        - surface_color, surface_dim_color, surface_bright_color
        - surface_container_lowest_color, surface_container_low_color,
          surface_container_color
        - surface_container_high_color, surface_container_highest_color
        - on_surface_color, surface_variant_color,
          on_surface_variant_color
        - inverse_surface_color, inverse_on_surface_color
    Outline and shadow colors:
        - outline_color, outline_variant_color
        - shadow_color, scrim_color
    Tint and accent colors:
        - surface_tint_color
    Primary, secondary, tertiary, and error colors
        (and their containers and "on" variants)
        - primary_color, on_primary_color, primary_container_color,
          on_primary_container_color, inverse_primary_color
        - secondary_color, on_secondary_color,
          secondary_container_color, on_secondary_container_color
        - tertiary_color, on_tertiary_color, tertiary_container_color,
          on_tertiary_container_color
        - error_color, on_error_color, error_container_color,
          on_error_container_color
    Fixed palette colors for accessibility and contrast:
        - primary_fixed_color, primary_fixed_dim_color,
          on_primary_fixed_color, on_primary_fixed_variant_color
        - secondary_fixed_color, secondary_fixed_dim_color,
          on_secondary_fixed_color, on_secondary_fixed_variant_color
        - tertiary_fixed_color, tertiary_fixed_dim_color,
          on_tertiary_fixed_color, on_tertiary_fixed_variant_color
    
    Usage
    -----
    Use this class to define and manage dynamic theme colors for 
    MorphUI-based applications, ensuring consistency and adaptability 
    across different UI components and states.
    """

    _attribute_map: Dict[str, DynamicColor] = dict(
        material_dynamic_color_attributes())
    """Mapping of attribute names to MaterialDynamicColors attributes."""

    @property
    def attribute_map(self) -> Dict[str, DynamicColor]:
        """Get the mapping of attribute names to MaterialDynamicColors 
        attributes (read-only)."""
        return self._attribute_map
    
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
        for attr_name in self._attribute_map.keys():
            color_value = getattr(self, attr_name, None)
            if color_value is None:
                return False
        return True 

    background_color = ColorProperty()
    """Background color.
    This property holds the dynamic color value set by the theme.

    :attr:`background_color` is a
    :class:`~kivy.properties.ColorProperty` that holds a dynamic color
    value and defaults to None"""

    error_color = ColorProperty()
    """Error color.
    This property holds the dynamic color value set by the theme.

    :attr:`error_color` is a
    :class:`~kivy.properties.ColorProperty` that holds a dynamic color
    value and defaults to None"""

    error_container_color = ColorProperty()
    """Error container color.
    This property holds the dynamic color value set by the theme.

    :attr:`error_container_color` is a
    :class:`~kivy.properties.ColorProperty` that holds a dynamic color
    value and defaults to None"""

    inverse_on_surface_color = ColorProperty()
    """Inverse on surface color.
    This property holds the dynamic color value set by the theme.

    :attr:`inverse_on_surface_color` is a
    :class:`~kivy.properties.ColorProperty` that holds a dynamic color
    value and defaults to None"""

    inverse_primary_color = ColorProperty()
    """Inverse primary color.
    This property holds the dynamic color value set by the theme.

    :attr:`inverse_primary_color` is a
    :class:`~kivy.properties.ColorProperty` that holds a dynamic color
    value and defaults to None"""

    inverse_surface_color = ColorProperty()
    """Inverse surface color.
    This property holds the dynamic color value set by the theme.

    :attr:`inverse_surface_color` is a
    :class:`~kivy.properties.ColorProperty` that holds a dynamic color
    value and defaults to None"""

    neutral_palette_key_color = ColorProperty()
    """Neutral palette key color.
    This property holds the dynamic color value set by the theme.

    :attr:`neutral_palette_key_color` is a
    :class:`~kivy.properties.ColorProperty` that holds a dynamic color
    value and defaults to None"""

    neutral_variant_palette_key_color = ColorProperty()
    """Neutral variant palette key color.
    This property holds the dynamic color value set by the theme.

    :attr:`neutral_variant_palette_key_color` is a
    :class:`~kivy.properties.ColorProperty` that holds a dynamic color
    value and defaults to None"""

    on_background_color = ColorProperty()
    """On background color.
    This property holds the dynamic color value set by the theme.

    :attr:`on_background_color` is a
    :class:`~kivy.properties.ColorProperty` that holds a dynamic color
    value and defaults to None"""

    on_error_color = ColorProperty()
    """On error color.
    This property holds the dynamic color value set by the theme.

    :attr:`on_error_color` is a
    :class:`~kivy.properties.ColorProperty` that holds a dynamic color
    value and defaults to None"""

    on_error_container_color = ColorProperty()
    """On error container color.
    This property holds the dynamic color value set by the theme.

    :attr:`on_error_container_color` is a
    :class:`~kivy.properties.ColorProperty` that holds a dynamic color
    value and defaults to None"""

    on_primary_color = ColorProperty()
    """On primary color.
    This property holds the dynamic color value set by the theme.

    :attr:`on_primary_color` is a
    :class:`~kivy.properties.ColorProperty` that holds a dynamic color
    value and defaults to None"""

    on_primary_container_color = ColorProperty()
    """On primary container color.
    This property holds the dynamic color value set by the theme.

    :attr:`on_primary_container_color` is a
    :class:`~kivy.properties.ColorProperty` that holds a dynamic color
    value and defaults to None"""

    on_primary_fixed_color = ColorProperty()
    """On primary fixed color.
    This property holds the dynamic color value set by the theme.

    :attr:`on_primary_fixed_color` is a
    :class:`~kivy.properties.ColorProperty` that holds a dynamic color
    value and defaults to None"""

    on_primary_fixed_variant_color = ColorProperty()
    """On primary fixed variant color.
    This property holds the dynamic color value set by the theme.

    :attr:`on_primary_fixed_variant_color` is a
    :class:`~kivy.properties.ColorProperty` that holds a dynamic color
    value and defaults to None"""

    on_secondary_color = ColorProperty()
    """On secondary color.
    This property holds the dynamic color value set by the theme.

    :attr:`on_secondary_color` is a
    :class:`~kivy.properties.ColorProperty` that holds a dynamic color
    value and defaults to None"""

    on_secondary_container_color = ColorProperty()
    """On secondary container color.
    This property holds the dynamic color value set by the theme.

    :attr:`on_secondary_container_color` is a
    :class:`~kivy.properties.ColorProperty` that holds a dynamic color
    value and defaults to None"""

    on_secondary_fixed_color = ColorProperty()
    """On secondary fixed color.
    This property holds the dynamic color value set by the theme.

    :attr:`on_secondary_fixed_color` is a
    :class:`~kivy.properties.ColorProperty` that holds a dynamic color
    value and defaults to None"""

    on_secondary_fixed_variant_color = ColorProperty()
    """On secondary fixed variant color.
    This property holds the dynamic color value set by the theme.

    :attr:`on_secondary_fixed_variant_color` is a
    :class:`~kivy.properties.ColorProperty` that holds a dynamic color
    value and defaults to None"""

    on_surface_color = ColorProperty()
    """On surface color.
    This property holds the dynamic color value set by the theme.

    :attr:`on_surface_color` is a
    :class:`~kivy.properties.ColorProperty` that holds a dynamic color
    value and defaults to None"""

    on_surface_variant_color = ColorProperty()
    """On surface variant color.
    This property holds the dynamic color value set by the theme.

    :attr:`on_surface_variant_color` is a
    :class:`~kivy.properties.ColorProperty` that holds a dynamic color
    value and defaults to None"""

    on_tertiary_color = ColorProperty()
    """On tertiary color.
    This property holds the dynamic color value set by the theme.

    :attr:`on_tertiary_color` is a
    :class:`~kivy.properties.ColorProperty` that holds a dynamic color
    value and defaults to None"""

    on_tertiary_container_color = ColorProperty()
    """On tertiary container color.
    This property holds the dynamic color value set by the theme.

    :attr:`on_tertiary_container_color` is a
    :class:`~kivy.properties.ColorProperty` that holds a dynamic color
    value and defaults to None"""

    on_tertiary_fixed_color = ColorProperty()
    """On tertiary fixed color.
    This property holds the dynamic color value set by the theme.

    :attr:`on_tertiary_fixed_color` is a
    :class:`~kivy.properties.ColorProperty` that holds a dynamic color
    value and defaults to None"""

    on_tertiary_fixed_variant_color = ColorProperty()
    """On tertiary fixed variant color.
    This property holds the dynamic color value set by the theme.

    :attr:`on_tertiary_fixed_variant_color` is a
    :class:`~kivy.properties.ColorProperty` that holds a dynamic color
    value and defaults to None"""

    outline_color = ColorProperty()
    """Outline color.
    This property holds the dynamic color value set by the theme.

    :attr:`outline_color` is a
    :class:`~kivy.properties.ColorProperty` that holds a dynamic color
    value and defaults to None"""

    outline_variant_color = ColorProperty()
    """Outline variant color.
    This property holds the dynamic color value set by the theme.

    :attr:`outline_variant_color` is a
    :class:`~kivy.properties.ColorProperty` that holds a dynamic color
    value and defaults to None"""

    primary_color = ColorProperty()
    """Primary color.
    This property holds the dynamic color value set by the theme.

    :attr:`primary_color` is a
    :class:`~kivy.properties.ColorProperty` that holds a dynamic color
    value and defaults to None"""

    primary_container_color = ColorProperty()
    """Primary container color.
    This property holds the dynamic color value set by the theme.

    :attr:`primary_container_color` is a
    :class:`~kivy.properties.ColorProperty` that holds a dynamic color
    value and defaults to None"""

    primary_fixed_color = ColorProperty()
    """Primary fixed color.
    This property holds the dynamic color value set by the theme.

    :attr:`primary_fixed_color` is a
    :class:`~kivy.properties.ColorProperty` that holds a dynamic color
    value and defaults to None"""

    primary_fixed_dim_color = ColorProperty()
    """Primary fixed dim color.
    This property holds the dynamic color value set by the theme.

    :attr:`primary_fixed_dim_color` is a
    :class:`~kivy.properties.ColorProperty` that holds a dynamic color
    value and defaults to None"""

    primary_palette_key_color = ColorProperty()
    """Primary palette key color.
    This property holds the dynamic color value set by the theme.

    :attr:`primary_palette_key_color` is a
    :class:`~kivy.properties.ColorProperty` that holds a dynamic color
    value and defaults to None"""

    scrim_color = ColorProperty()
    """Scrim color.
    This property holds the dynamic color value set by the theme.

    :attr:`scrim_color` is a
    :class:`~kivy.properties.ColorProperty` that holds a dynamic color
    value and defaults to None"""

    secondary_color = ColorProperty()
    """Secondary color.
    This property holds the dynamic color value set by the theme.

    :attr:`secondary_color` is a
    :class:`~kivy.properties.ColorProperty` that holds a dynamic color
    value and defaults to None"""

    secondary_container_color = ColorProperty()
    """Secondary container color.
    This property holds the dynamic color value set by the theme.

    :attr:`secondary_container_color` is a
    :class:`~kivy.properties.ColorProperty` that holds a dynamic color
    value and defaults to None"""

    secondary_fixed_color = ColorProperty()
    """Secondary fixed color.
    This property holds the dynamic color value set by the theme.

    :attr:`secondary_fixed_color` is a
    :class:`~kivy.properties.ColorProperty` that holds a dynamic color
    value and defaults to None"""

    secondary_fixed_dim_color = ColorProperty()
    """Secondary fixed dim color.
    This property holds the dynamic color value set by the theme.

    :attr:`secondary_fixed_dim_color` is a
    :class:`~kivy.properties.ColorProperty` that holds a dynamic color
    value and defaults to None"""

    secondary_palette_key_color = ColorProperty()
    """Secondary palette key color.
    This property holds the dynamic color value set by the theme.

    :attr:`secondary_palette_key_color` is a
    :class:`~kivy.properties.ColorProperty` that holds a dynamic color
    value and defaults to None"""

    shadow_color = ColorProperty()
    """Shadow color.
    This property holds the dynamic color value set by the theme.

    :attr:`shadow_color` is a
    :class:`~kivy.properties.ColorProperty` that holds a dynamic color
    value and defaults to None"""

    surface_color = ColorProperty()
    """Surface color.
    This property holds the dynamic color value set by the theme.

    :attr:`surface_color` is a
    :class:`~kivy.properties.ColorProperty` that holds a dynamic color
    value and defaults to None"""

    surface_bright_color = ColorProperty()
    """Surface bright color.
    This property holds the dynamic color value set by the theme.

    :attr:`surface_bright_color` is a
    :class:`~kivy.properties.ColorProperty` that holds a dynamic color
    value and defaults to None"""

    surface_container_color = ColorProperty()
    """Surface container color.
    This property holds the dynamic color value set by the theme.

    :attr:`surface_container_color` is a
    :class:`~kivy.properties.ColorProperty` that holds a dynamic color
    value and defaults to None"""

    surface_container_high_color = ColorProperty()
    """Surface container high color.
    This property holds the dynamic color value set by the theme.

    :attr:`surface_container_high_color` is a
    :class:`~kivy.properties.ColorProperty` that holds a dynamic color
    value and defaults to None"""

    surface_container_highest_color = ColorProperty()
    """Surface container highest color.
    This property holds the dynamic color value set by the theme.

    :attr:`surface_container_highest_color` is a
    :class:`~kivy.properties.ColorProperty` that holds a dynamic color
    value and defaults to None"""

    surface_container_low_color = ColorProperty()
    """Surface container low color.
    This property holds the dynamic color value set by the theme.

    :attr:`surface_container_low_color` is a
    :class:`~kivy.properties.ColorProperty` that holds a dynamic color
    value and defaults to None"""

    surface_container_lowest_color = ColorProperty()
    """Surface container lowest color.
    This property holds the dynamic color value set by the theme.

    :attr:`surface_container_lowest_color` is a
    :class:`~kivy.properties.ColorProperty` that holds a dynamic color
    value and defaults to None"""

    surface_dim_color = ColorProperty()
    """Surface dim color.
    This property holds the dynamic color value set by the theme.

    :attr:`surface_dim_color` is a
    :class:`~kivy.properties.ColorProperty` that holds a dynamic color
    value and defaults to None"""

    surface_tint_color = ColorProperty()
    """Surface tint color.
    This property holds the dynamic color value set by the theme.

    :attr:`surface_tint_color` is a
    :class:`~kivy.properties.ColorProperty` that holds a dynamic color
    value and defaults to None"""

    surface_variant_color = ColorProperty()
    """Surface variant color.
    This property holds the dynamic color value set by the theme.

    :attr:`surface_variant_color` is a
    :class:`~kivy.properties.ColorProperty` that holds a dynamic color
    value and defaults to None"""

    tertiary_color = ColorProperty()
    """Tertiary color.
    This property holds the dynamic color value set by the theme.

    :attr:`tertiary_color` is a
    :class:`~kivy.properties.ColorProperty` that holds a dynamic color
    value and defaults to None"""

    tertiary_container_color = ColorProperty()
    """Tertiary container color.
    This property holds the dynamic color value set by the theme.

    :attr:`tertiary_container_color` is a
    :class:`~kivy.properties.ColorProperty` that holds a dynamic color
    value and defaults to None"""

    tertiary_fixed_color = ColorProperty()
    """Tertiary fixed color.
    This property holds the dynamic color value set by the theme.

    :attr:`tertiary_fixed_color` is a
    :class:`~kivy.properties.ColorProperty` that holds a dynamic color
    value and defaults to None"""

    tertiary_fixed_dim_color = ColorProperty()
    """Tertiary fixed dim color.
    This property holds the dynamic color value set by the theme.

    :attr:`tertiary_fixed_dim_color` is a
    :class:`~kivy.properties.ColorProperty` that holds a dynamic color
    value and defaults to None"""

    tertiary_palette_key_color = ColorProperty()
    """Tertiary palette key color.
    This property holds the dynamic color value set by the theme.

    :attr:`tertiary_palette_key_color` is a
    :class:`~kivy.properties.ColorProperty` that holds a dynamic color
    value and defaults to None"""


if __name__ == '__main__':
    for attr, _ in material_dynamic_color_attributes():
        print(f'''
    {attr} = ColorProperty()
    """{" ".join(attr.capitalize().split("_"))}.
    This property holds the dynamic color value set by the theme.

    :attr:`{attr}` is a
    :class:`~kivy.properties.ColorProperty` that holds a dynamic color
    value and defaults to None"""''')
