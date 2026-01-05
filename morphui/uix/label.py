from typing import Any
from typing import Dict

from kivy.metrics import dp
from kivy.uix.label import Label
from kivy.properties import AliasProperty

from morphui.utils import clean_config

from morphui.uix.behaviors import MorphIconBehavior
from morphui.uix.behaviors import MorphScaleBehavior
from morphui.uix.behaviors import MorphThemeBehavior
from morphui.uix.behaviors import MorphAutoSizingBehavior
from morphui.uix.behaviors import MorphRoundSidesBehavior
from morphui.uix.behaviors import MorphSurfaceLayerBehavior
from morphui.uix.behaviors import MorphContentLayerBehavior
from morphui.uix.behaviors import MorphIdentificationBehavior


__all__ = [
    'BaseLabel',
    'MorphSimpleLabel',
    'MorphSimpleIconLabel',
    'MorphLabel',
    'MorphIconLabel',
    'MorphLeadingIconLabel',
    'MorphTextLabel',
    'MorphTrailingIconLabel',
    'MorphChipLeadingIconLabel',
    'MorphChipTextLabel',]


class BaseLabel(Label):
    """Base class for MorphUI labels with auto-sizing support.
    
    This class extends the standard Kivy Label to include auto-sizing
    properties for minimum width and height based on the label's content.
    It serves as a foundation for more specialized label classes in
    MorphUI. The auto-sizing properties calculate the minimum size
    required to display the label's text content, taking into account
    padding and texture size.

    Notes
    -----
    - Inherits from Kivy's Label.
    - Provides :attr:`minimum_height` and :attr:`minimum_width` 
      properties for auto-sizing based on content.
    - Designed to be extended by other MorphUI label classes.
    - Does not include any theming or styling behaviors.
    """

    minimum_height: float = AliasProperty(
        lambda self: self.texture_size[1] + self.padding[1] + self.padding[3],
        bind=['texture_size', 'padding',])
    """The minimum height required to display the label's content.

    This property calculates the minimum height based on the label's
    texture size and padding.

    :attr:`minimum_height` is a :class:`~kivy.properties.AliasProperty`
    """

    minimum_width: float = AliasProperty(
        lambda self: self.texture_size[0] + self.padding[0] + self.padding[2],
        bind=['texture_size', 'padding',])
    """The minimum width required to display the label's content.

    This property calculates the minimum width based on the label's
    texture size and padding.

    :attr:`minimum_width` is a :class:`~kivy.properties.AliasProperty`
    """

    default_config: Dict[str, Any] = dict()
    """Default configuration values for BaseLabel instances.
    """

    def __init__(self, **kwargs) -> None:
        config = clean_config(self.default_config, kwargs)
        super().__init__(**config)
        typography = getattr(self, 'typography', None)
        if typography is not None:
            for prop in typography.available_style_properties:
                if prop in kwargs and hasattr(self, prop):
                    setattr(self, prop, kwargs[prop])


class MorphSimpleLabel(
        MorphIdentificationBehavior,
        MorphThemeBehavior,
        MorphContentLayerBehavior,
        MorphAutoSizingBehavior,
        BaseLabel,
        ):
    """A simplified themed label widget with only content theming.

    This class provides a lightweight label that only handles content
    color theming without background or border styling. It's ideal for
    simple text display where you only need theme-aware text colors.

    Examples
    --------
    ```python
    from morphui.app import MorphApp
    from morphui.uix.label import MorphSimpleLabel
    from morphui.uix.boxlayout import MorphBoxLayout

    class MyApp(MorphApp):
        def build(self):
            return MorphBoxLayout(
                MorphSimpleLabel(text='Simple themed text'),
                orientation='vertical',
                padding=50,
                spacing=15,)
    MyApp().run()
    ```

    Notes
    -----
    - Only provides content color theming (no surface/border styling)
    - Inherits typography support if typography behavior is available
    - Auto-sizing properties can be used for content-based sizing
    - Lighter weight than MorphLabel for simple text display needs
    """

    default_config: Dict[str, Any] = dict(
        theme_color_bindings=dict(
            normal_content_color='content_surface_color',),
        typography_role='Label',
        typography_size='medium',
        typography_weight='Regular',
        halign='left',
        valign='center',)
    """Default configuration values for MorphSimpleLabel instances.
    
    Provides minimal label appearance settings:
    - Left alignment for text readability
    - Middle vertical alignment for centered appearance
    - Content color binding for theme integration
    - Label typography role with medium sizing
    
    These values can be overridden by subclasses or during 
    instantiation.
    """


class MorphSimpleIconLabel(
        MorphIconBehavior,
        MorphSimpleLabel):
    """A simplified icon label with only content theming.

    This class extends `MorphSimpleLabel` to display icons using icon
    fonts while only providing content color theming. It's ideal for
    simple icon display without background or border styling.

    Examples
    --------
    ```python
from morphui.app import MorphApp
from morphui.uix.label import MorphSimpleIconLabel
from morphui.uix.boxlayout import MorphBoxLayout

class MyApp(MorphApp):
    def build(self):
        return MorphBoxLayout(
            MorphSimpleIconLabel(
                icon='home',
                typography_size='large',),
            MorphSimpleIconLabel(
                icon='user',
                typography_size='large',),
            orientation='vertical',
            padding=50,
            spacing=15,)
MyApp().run()
    ```

    Notes
    -----
    - Only provides content color theming (no surface/border styling)
    - Inherits typography support for icon font rendering
    - Auto-sizing properties available for icon-based sizing
    - Lighter weight than MorphIconLabel for simple icon display
    """

    default_config: Dict[str, Any] = dict(
        theme_color_bindings=dict(
            normal_content_color='content_surface_color',),
        font_name='MaterialIcons',
        typography_role='Label',
        typography_size='large',
        halign='center',
        valign='center',
        auto_size=True,
        padding=dp(4),)
    """Default configuration values for MorphSimpleIconLabel instances.
    
    Provides minimal icon-specific display settings:
    - MaterialIcons font for icon character rendering
    - Center alignment for optimal icon positioning
    - Primary color theme for icon prominence
    - Large size suitable for icon visibility
    - Auto-sizing to fit icon dimensions
    
    These values can be overridden by subclasses or during 
    instantiation.
    """

class MorphLabel(
        MorphRoundSidesBehavior,
        MorphSimpleLabel,
        MorphSurfaceLayerBehavior,
        ):
    """A themed label widget with automatic sizing and typography 
    support.

    This class extends the standard Kivy Label to integrate MorphUI's
    theming, text layering, and auto-sizing behaviors. It provides a
    flexible label component that adapts to the app's theme and
    typography settings.

    Examples
    --------
    ```python
    from morphui.app import MorphApp
    from morphui.uix.label import MorphLabel
    from morphui.uix.boxlayout import MorphBoxLayout

    class MyApp(MorphApp):
        def build(self):
            return MorphBoxLayout(
                MorphLabel(text='Hello, World!'),
                orientation='vertical',
                padding=50,
                spacing=15,
                theme_style='surface',)
    MyApp().run()
    ```

    Notes
    -----
    - The `theme_color_bindings` are automatically removed when 
      `theme_style` is specified.
    - Typography properties are applied if the typography behavior is
      included.
    - Auto-sizing properties can be used to make the label adjust its
      size based on content.
    - Passing `font_size`, `line_height` or other typography-related
      properties in kwargs will override the typography settings.
    """

    default_config: Dict[str, Any] = dict(
        theme_color_bindings=dict(
            normal_content_color='content_surface_color',
            normal_surface_color='surface_color',),
        typography_role='Label',
        typography_size='medium',
        typography_weight='Regular',
        halign='left',
        valign='center',
        padding=dp(8),)
    """Default configuration values for MorphLabel instances.
    
    Provides standard label appearance and behavior settings:
    - Left alignment for text readability
    - Middle vertical alignment for centered appearance
    - Bounded colors for theme integration
    - Label typography role with medium sizing
    
    These values can be overridden by subclasses or during 
    instantiation.
    """


class MorphIconLabel(
        MorphIconBehavior,
        MorphLabel):
    """A label designed to display icons using icon fonts.

    This class extends `MorphLabel` to facilitate the use of icon fonts,
    allowing for easy integration of icons into your UI. It inherits all
    properties and behaviors from `MorphLabel`, including theming and
    auto-sizing capabilities.

    Examples
    --------
    ```python
    from morphui.app import MorphApp
    from morphui.uix.iconlabel import MorphIconLabel
    from morphui.uix.boxlayout import MorphBoxLayout

    class MyApp(MorphApp):
        def build(self):
            self.theme_manager.seed_color = 'Purple'
            return MorphBoxLayout(
                MorphIconLabel(
                    icon='home',
                    theme_style='primary',
                    typography_size='huge',),
                MorphIconLabel(
                    icon='user',
                    theme_style='secondary',
                    typography_size='huge',),
                orientation='vertical',
                padding=50,
                spacing=15,
                theme_style='surface',)
            )
    MyApp().run()
    ```

    Notes
    -----
    - The `theme_color_bindings` are automatically removed when 
      `theme_style` is specified.
    - Typography properties are applied if the typography behavior is
      included.
    - Auto-sizing properties can be used to make the label adjust its
      size based on content.
    - Passing `font_size`, `line_height` or other typography-related
      properties in kwargs will override the typography settings.
    """

    default_config: Dict[str, Any] = dict(
        theme_color_bindings=dict(
            normal_content_color='content_surface_variant_color',
            normal_surface_color='transparent_color',),
        font_name='MaterialIcons',
        typography_role='Label',
        typography_size='large',
        halign='center',
        valign='center',
        auto_size=True,
        padding=dp(8),)
    """Default configuration values for MorphIconLabel instances.
    
    Provides icon-specific display and behavior settings:
    - MaterialIcons font for icon character rendering
    - Center alignment for optimal icon positioning
    - Primary color theme for icon prominence
    - Font size suitable for icon visibility
    - Auto-sizing to fit icon dimensions
    
    These values can be overridden by subclasses or during 
    instantiation.
    """



class MorphLeadingIconLabel(
        MorphScaleBehavior,
        MorphSimpleIconLabel):
    """Leading icon label for containers.
    
    This widget displays an icon on the left side of a container,
    with support for scale animations.
    """
    
    default_config: Dict[str, Any] = (
        MorphSimpleIconLabel.default_config.copy() | dict(
        padding=dp(0),
        pos_hint={'center_y': 0.5},))


class MorphTextLabel(
        MorphSimpleLabel):
    """Text label for containers.
    
    This widget displays text mostly used in between leading and 
    trailing icons or other widgets.
    """
    
    default_config: Dict[str, Any] = (
        MorphSimpleLabel.default_config.copy() | dict(
        auto_size=(False, True),
        size_hint=(1, None),
        padding=dp(0),
        pos_hint={'center_y': 0.5},))


class MorphTrailingIconLabel(
        MorphScaleBehavior,
        MorphSimpleIconLabel):
    """Trailing icon label for containers.
    
    This widget displays an icon on the right side of a container,
    with support for scale animations.
    """
    
    default_config: Dict[str, Any] = (
        MorphSimpleIconLabel.default_config.copy() | dict(
        padding=dp(0),
        pos_hint={'center_y': 0.5},))
    

class MorphChipLeadingIconLabel(
        MorphLeadingIconLabel):
    """Leading icon label for chips.
    
    Inherits from :class:`~morphui.uix.label.MorphLeadingIconLabel`.
    """
    pass


class MorphChipTextLabel(
        MorphTextLabel):
    """Text label for chips.
    
    Inherits from :class:`~morphui.uix.label.MorphTextLabel`.
    """
    default_config: Dict[str, Any] = (
        MorphTextLabel.default_config.copy() | dict(
            auto_size=(True, True),))