from typing import List
from typing import Dict

from kivy.event import EventDispatcher
from kivy.properties import DictProperty
from kivy.properties import ColorProperty
from kivy.properties import AliasProperty


__all__ = [
    'MorphDynamicColorPalette',]


def create_color_property_mapping() -> Dict[str, str]:
    """
    Create a mapping between MorphUI color property names and
    material-color-utilities DynamicScheme color property names.
    
    Returns
    -------
    Dict[str, str]
        Mapping from MorphUI property name to DynamicScheme property name.
    """
    # Define the mapping between old MaterialDynamicColors names and new DynamicScheme properties
    return {
        'primary_color': 'primary',
        'content_primary_color': 'on_primary',
        'primary_container_color': 'primary_container',
        'content_primary_container_color': 'on_primary_container',
        'secondary_color': 'secondary',
        'content_secondary_color': 'on_secondary',
        'secondary_container_color': 'secondary_container',
        'content_secondary_container_color': 'on_secondary_container',
        'tertiary_color': 'tertiary',
        'content_tertiary_color': 'on_tertiary',
        'tertiary_container_color': 'tertiary_container',
        'content_tertiary_container_color': 'on_tertiary_container',
        'error_color': 'error',
        'content_error_color': 'on_error',
        'error_container_color': 'error_container',
        'content_error_container_color': 'on_error_container',
        'background_color': 'background',
        'content_background_color': 'on_surface',
        'surface_color': 'surface',
        'content_surface_color': 'on_surface',
        'surface_variant_color': 'surface_variant',
        'content_surface_variant_color': 'on_surface_variant',
        'surface_dim_color': 'surface_dim',
        'surface_bright_color': 'surface_bright',
        'surface_container_lowest_color': 'surface_container_lowest',
        'surface_container_low_color': 'surface_container_low',
        'surface_container_color': 'surface_container',
        'surface_container_high_color': 'surface_container_high',
        'surface_container_highest_color': 'surface_container_highest',
        'surface_tint_color': 'surface_tint',
        'inverse_surface_color': 'inverse_surface',
        'inverse_primary_color': 'inverse_primary',
        'inverse_content_surface_color': 'inverse_on_surface',
        'outline_color': 'outline',
        'outline_variant_color': 'outline_variant',
        'shadow_color': 'shadow',
        'scrim_color': 'scrim',
        # Fixed colors
        'primary_fixed_color': 'primary_fixed',
        'primary_fixed_dim_color': 'primary_fixed_dim',
        'content_primary_fixed_color': 'on_primary_fixed',
        'content_primary_fixed_variant_color': 'on_primary_fixed_variant',
        'secondary_fixed_color': 'secondary_fixed',
        'secondary_fixed_dim_color': 'secondary_fixed_dim',
        'content_secondary_fixed_color': 'on_secondary_fixed',
        'content_secondary_fixed_variant_color': 'on_secondary_fixed_variant',
        'tertiary_fixed_color': 'tertiary_fixed',
        'tertiary_fixed_dim_color': 'tertiary_fixed_dim',
        'content_tertiary_fixed_color': 'on_tertiary_fixed',
        'content_tertiary_fixed_variant_color': 'on_tertiary_fixed_variant',
    }


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
        - background_color, content_background_color
        - surface_color, surface_dim_color, surface_bright_color
        - surface_container_lowest_color, surface_container_low_color,
          surface_container_color
        - surface_container_high_color, surface_container_highest_color
        - content_surface_color, surface_variant_color,
          content_surface_variant_color
        - inverse_surface_color, inverse_content_surface_color
    Outline and shadow colors:
        - outline_color, outline_variant_color
        - shadow_color, scrim_color
    Tint and accent colors:
        - surface_tint_color
    Primary, secondary, tertiary, and error colors
        (and their containers and text variants)
        - primary_color, content_primary_color, primary_container_color,
          content_primary_container_color, inverse_primary_color
        - secondary_color, content_secondary_color,
          secondary_container_color, content_secondary_container_color
        - tertiary_color, content_tertiary_color,
          tertiary_container_color, content_tertiary_container_color
        - error_color, content_error_color, error_container_color,
          content_error_container_color
    Fixed palette colors for accessibility and contrast:
        - primary_fixed_color, primary_fixed_dim_color,
          content_primary_fixed_color,
          content_primary_fixed_variant_color
        - secondary_fixed_color, secondary_fixed_dim_color,
          content_secondary_fixed_color,
          content_secondary_fixed_variant_color
        - tertiary_fixed_color, tertiary_fixed_dim_color,
          content_tertiary_fixed_color,
          content_tertiary_fixed_variant_color
    
    Notes
    -----
    Material colors starting with 'on_' (like 'on_background', 
    'on_primary') are renamed to 'content_' prefixed variants (like 
    'content_background_color', 'content_primary_color') to avoid 
    conflicts  with Kivy's event handling system which treats attributes
    starting with 'on_' as event handlers.
    
    Usage
    -----
    Use this class to define and manage dynamic theme colors for 
    MorphUI-based applications, ensuring consistency and adaptability 
    across different UI components and states.
    """

    _material_color_map: Dict[str, str] = DictProperty(
        create_color_property_mapping())
    """Mapping of MorphUI color property names to DynamicScheme property 
    names."""

    material_color_map: Dict[str, str] = AliasProperty(
        lambda self: self._material_color_map,
        bind=['_material_color_map'],)
    """Get the mapping of color property names to DynamicScheme 
    properties (read-only).

    This mapping is used internally to apply color schemes to all 
    available color properties. Returns a dictionary where:
        - Keys are MorphUI color property names (e.g., 'primary_color', 
        'content_surface_color')
        - Values are the corresponding DynamicScheme property names
        (e.g., 'primary', 'on_surface')

    :attr:`material_color_map` is a 
    :class:`~kivy.properties.AliasProperty` that provides read-only
    access to the internal color property mapping.
    """

    dynamic_color_properties: List[str] = AliasProperty(
        lambda self: list(self._material_color_map.keys()),
        bind=['_material_color_map'],)
    """List of all dynamic color property names in the palette.

    This property returns a list of strings representing the names of
    all dynamic color properties defined in the palette. These names
    correspond to the attributes that hold dynamic color values,
    allowing for easy iteration and management of colors.

    :attr:`dynamic_color_properties` is a
    :class:`~kivy.properties.AliasProperty` that provides read-only
    access to the list of dynamic color property names.
    """

    def _get_colors_initialized(self) -> bool:
        """Check if dynamic colors have been initialized.
        
        Returns True if at least one color property has been set with
        a non-None value, indicating that the color scheme has been
        applied. Returns False if all color properties are None.
        
        Returns
        -------
        bool
            True if colors are initialized, False otherwise.
        """
        key_colors = [
            getattr(self, 'primary_color', None),
            getattr(self, 'background_color', None), 
            getattr(self, 'surface_color', None),
            getattr(self, 'content_surface_color', None)
        ]
        return any(color is not None for color in key_colors)
    
    colors_initialized: bool = AliasProperty(
        _get_colors_initialized,
        cache=True,
        bind=[
            'primary_color',
            'background_color',
            'surface_color',
            'content_surface_color',],)
    """Check if dynamic colors have been initialized.

    Returns True if at least one color property has been set with
    a non-None value, indicating that the color scheme has been applied.
    Returns False if all color properties are None.

    :attr:`colors_initialized` is a
    :class:`~kivy.properties.AliasProperty` that provides read-only
    access to the color initialization status.
    """

    def _get_all_colors_set(self) -> bool:
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
    
    all_colors_set: bool = AliasProperty(
        _get_all_colors_set,)
    """Check if all color properties have been initialized.
        
    Returns True only if all color properties in the palette have been
    set with non-None values. This is a more strict check than
    :attr:`colors_initialized`.

    :attr:`all_colors_set` is a
    :class:`~kivy.properties.AliasProperty` that provides read-only
    access to the all colors set status.
    """

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

    transparent_color: List[float] = ColorProperty([0, 0, 0, 0])
    """Transparent color. This property is always [0, 0, 0, 0] and 
    does not change with the theme. It is provided for convenience.

    :attr:`transparent_color` is a
    :class:`~kivy.properties.ColorProperty` that holds a static color
    value and defaults to [0, 0, 0, 0] (fully transparent)."""

    background_color: List[float] | None = ColorProperty(None)
    """Background color.
    This property holds the dynamic color value set by the theme.

    :attr:`background_color` is a
    :class:`~kivy.properties.ColorProperty` that holds a dynamic color
    value and defaults to None"""

    content_background_color: List[float] | None = ColorProperty(None)
    """Content background color.
    This property holds the dynamic color value set by the theme.

    :attr:`content_background_color` is a
    :class:`~kivy.properties.ColorProperty` that holds a dynamic color
    value and defaults to None"""

    content_error_color: List[float] | None = ColorProperty(None)
    """Content error color.
    This property holds the dynamic color value set by the theme.

    :attr:`content_error_color` is a
    :class:`~kivy.properties.ColorProperty` that holds a dynamic color
    value and defaults to None"""

    content_error_container_color: List[float] | None = ColorProperty(None)
    """Content error container color.
    This property holds the dynamic color value set by the theme.

    :attr:`content_error_container_color` is a
    :class:`~kivy.properties.ColorProperty` that holds a dynamic color
    value and defaults to None"""

    content_primary_color: List[float] | None = ColorProperty(None)
    """Content primary color.
    This property holds the dynamic color value set by the theme.

    :attr:`content_primary_color` is a
    :class:`~kivy.properties.ColorProperty` that holds a dynamic color
    value and defaults to None"""

    content_primary_container_color: List[float] | None = ColorProperty(None)
    """Content primary container color.
    This property holds the dynamic color value set by the theme.

    :attr:`content_primary_container_color` is a
    :class:`~kivy.properties.ColorProperty` that holds a dynamic color
    value and defaults to None"""

    content_primary_fixed_color: List[float] | None = ColorProperty(None)
    """Content primary fixed color.
    This property holds the dynamic color value set by the theme.

    :attr:`content_primary_fixed_color` is a
    :class:`~kivy.properties.ColorProperty` that holds a dynamic color
    value and defaults to None"""

    content_primary_fixed_variant_color: List[float] | None = ColorProperty(None)
    """Content primary fixed variant color.
    This property holds the dynamic color value set by the theme.

    :attr:`content_primary_fixed_variant_color` is a
    :class:`~kivy.properties.ColorProperty` that holds a dynamic color
    value and defaults to None"""

    content_secondary_color: List[float] | None = ColorProperty(None)
    """Content secondary color.
    This property holds the dynamic color value set by the theme.

    :attr:`content_secondary_color` is a
    :class:`~kivy.properties.ColorProperty` that holds a dynamic color
    value and defaults to None"""

    content_secondary_container_color: List[float] | None = ColorProperty(None)
    """Content secondary container color.
    This property holds the dynamic color value set by the theme.

    :attr:`content_secondary_container_color` is a
    :class:`~kivy.properties.ColorProperty` that holds a dynamic color
    value and defaults to None"""

    content_secondary_fixed_color: List[float] | None = ColorProperty(None)
    """Content secondary fixed color.
    This property holds the dynamic color value set by the theme.

    :attr:`content_secondary_fixed_color` is a
    :class:`~kivy.properties.ColorProperty` that holds a dynamic color
    value and defaults to None"""

    content_secondary_fixed_variant_color: List[float] | None = ColorProperty(None)
    """Content secondary fixed variant color.
    This property holds the dynamic color value set by the theme.

    :attr:`content_secondary_fixed_variant_color` is a
    :class:`~kivy.properties.ColorProperty` that holds a dynamic color
    value and defaults to None"""

    content_surface_color: List[float] | None = ColorProperty(None)
    """Content surface color.
    This property holds the dynamic color value set by the theme.

    :attr:`content_surface_color` is a
    :class:`~kivy.properties.ColorProperty` that holds a dynamic color
    value and defaults to None"""

    content_surface_variant_color: List[float] | None = ColorProperty(None)
    """Content surface variant color.
    This property holds the dynamic color value set by the theme.

    :attr:`content_surface_variant_color` is a
    :class:`~kivy.properties.ColorProperty` that holds a dynamic color
    value and defaults to None"""

    content_tertiary_color: List[float] | None = ColorProperty(None)
    """Content tertiary color.
    This property holds the dynamic color value set by the theme.

    :attr:`content_tertiary_color` is a
    :class:`~kivy.properties.ColorProperty` that holds a dynamic color
    value and defaults to None"""

    content_tertiary_container_color: List[float] | None = ColorProperty(None)
    """Content tertiary container color.
    This property holds the dynamic color value set by the theme.

    :attr:`content_tertiary_container_color` is a
    :class:`~kivy.properties.ColorProperty` that holds a dynamic color
    value and defaults to None"""

    content_tertiary_fixed_color: List[float] | None = ColorProperty(None)
    """Content tertiary fixed color.
    This property holds the dynamic color value set by the theme.

    :attr:`content_tertiary_fixed_color` is a
    :class:`~kivy.properties.ColorProperty` that holds a dynamic color
    value and defaults to None"""

    content_tertiary_fixed_variant_color: List[float] | None = ColorProperty(None)
    """Content tertiary fixed variant color.
    This property holds the dynamic color value set by the theme.

    :attr:`content_tertiary_fixed_variant_color` is a
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

    inverse_content_surface_color: List[float] | None = ColorProperty(None)
    """Inverse on surface color.
    This property holds the dynamic color value set by the theme.

    :attr:`inverse_content_surface_color` is a
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

    shadow_color: List[float] | None = ColorProperty(None)
    """Shadow color.
    This property holds the dynamic color value set by the theme.

    :attr:`shadow_color` is a
    :class:`~kivy.properties.ColorProperty` that holds a dynamic color
    value and defaults to None"""

    surface_bright_color: List[float] | None = ColorProperty(None)
    """Surface bright color.
    This property holds the dynamic color value set by the theme.

    :attr:`surface_bright_color` is a
    :class:`~kivy.properties.ColorProperty` that holds a dynamic color
    value and defaults to None"""

    surface_color: List[float] | None = ColorProperty(None)
    """Surface color.
    This property holds the dynamic color value set by the theme.

    :attr:`surface_color` is a
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


if __name__ == '__main__':
    for attr in sorted(create_color_property_mapping().keys()):
        print(f'''
    {attr}: List[float] | None = ColorProperty(None)
    """{" ".join(attr.capitalize().split("_"))}.
    This property holds the dynamic color value set by the theme.

    :attr:`{attr}` is a
    :class:`~kivy.properties.ColorProperty` that holds a dynamic color
    value and defaults to None"""''')
