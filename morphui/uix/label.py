from typing import Any
from typing import Dict

from kivy.metrics import dp
from kivy.uix.label import Label
from kivy.properties import AliasProperty
from kivy.properties import BooleanProperty
from kivy.properties import NumericProperty

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
    'MorphHeadingLabel',
    'MorphSupportingLabel',
    'MorphTertiaryLabel',
    'MorphTrailingIconLabel',
    'MorphButtonLeadingIconLabel',
    'MorphButtonTrailingIconLabel',
    'MorphButtonTextLabel',
    'MorphChipLeadingIconLabel',
    'MorphChipTextLabel',
    'MorphTextFieldLabel',
    'MorphTextFieldSupportingLabel',
    'MorphTextFieldTextLengthLabel',
    'MorphTextFieldLeadingIconLabel',]


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
        auto_size=(True, True),
        size_hint=(1, None),
        padding=[dp(4), 0],
        pos_hint={'center_y': 0.5},))


class MorphHeadingLabel(
        MorphSimpleLabel):
    """Heading label for containers.
    
    This widget displays a heading text mostly used in between leading and 
    trailing icons or other widgets.
    """
    
    default_config: Dict[str, Any] = (
        MorphSimpleLabel.default_config.copy() | dict(
        auto_size=(True, True),
        size_hint=(1, None),
        padding=[dp(4), 0],
        pos_hint={'center_y': 0.5},
        bold=True,))


MorphSupportingLabel = MorphTextLabel


class MorphTertiaryLabel(
        MorphSimpleLabel):
    """Tertiary label for containers.
    
    This widget displays a tertiary text mostly used in between leading and 
    trailing icons or other widgets.
    """
    
    default_config: Dict[str, Any] = (
        MorphSimpleLabel.default_config.copy() | dict(
        auto_size=(True, True),
        size_hint=(1, None),
        padding=[dp(4), 0],
        pos_hint={'center_y': 0.5},
        italic=True,))


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
    

class MorphButtonLeadingIconLabel(
        MorphLeadingIconLabel):
    """Leading icon label for icon text buttons.
    
    Inherits from :class:`~morphui.uix.label.MorphLeadingIconLabel`.
    """
    pass


class MorphButtonTrailingIconLabel(
        MorphTrailingIconLabel):
    """Trailing icon label for text icon buttons.
    
    Inherits from :class:`~morphui.uix.label.MorphTrailingIconLabel`.
    """
    pass


class MorphButtonTextLabel(
        MorphTextLabel):
    """Text label for icon text buttons.
    
    Inherits from :class:`~morphui.uix.label.MorphTextLabel`.
    """
    default_config: Dict[str, Any] = (
        MorphTextLabel.default_config.copy() | dict(
        padding=[dp(4), 0],
        pos_hint={'center_y': 0.5},
        auto_size=(True, True),))
    

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


class MorphTextFieldLabel(MorphSimpleLabel):
    """Label for text fields with state properties.

    This label is specifically designed for use within text field
    components. It includes properties to indicate whether the label
    is disabled, focused, or in an error state, allowing for dynamic
    styling based on the text field's status.
    """

    disabled: bool = BooleanProperty(False)
    """Indicates whether the text field label is disabled.

    When True, the label is rendered in a disabled state, typically with
    a different color or style to indicate it is not interactive.

    :attr:`disabled` is a :class:`~kivy.properties.BooleanProperty`
    and defaults to False.
    """

    focus: bool = BooleanProperty(False)
    """Indicates whether the text field label is focused.

    When True, the label is rendered in a focused state, typically with
    a different color or style to indicate it is active.

    :attr:`focus` is a :class:`~kivy.properties.BooleanProperty`
    and defaults to False.
    """
    
    error: bool = BooleanProperty(False)
    """Indicates whether the text field label is in an error state.

    When True, the label is rendered in an error state, typically with a
    different color or style to indicate a validation issue.

    :attr:`error` is a :class:`~kivy.properties.BooleanProperty`
    and defaults to False.
    """
    
    default_config: Dict[str, Any] = dict(
        theme_color_bindings=dict(
            normal_content_color='content_surface_color',
            focus_content_color='primary_color',
            error_content_color='error_color',),
        typography_role='Label',
        typography_size='medium',
        typography_weight='Regular',
        halign='left',
        valign='center',
        padding=[4, 0],
        auto_size=True,)


class MorphTextFieldSupportingLabel(MorphSimpleLabel):
    """Supporting label for text fields with state properties.

    This label is specifically designed for use within text field
    components. It includes properties to indicate whether the label
    is disabled, focused, or in an error state, allowing for dynamic
    styling based on the text field's status.
    """

    disabled: bool = BooleanProperty(False)
    """Indicates whether the supporting label is disabled.

    When True, the label is rendered in a disabled state, typically with
    a different color or style to indicate it is not interactive.
    
    :attr:`disabled` is a :class:`~kivy.properties.BooleanProperty`
    and defaults to False.
    """

    focus: bool = BooleanProperty(False)
    """Indicates whether the supporting label is focused.

    When True, the label is rendered in a focused state,typically with a
    different color or style to indicate it is active.

    :attr:`focus` is a :class:`~kivy.properties.BooleanProperty`
    and defaults to False.
    """
    
    error: bool = BooleanProperty(False)
    """Indicates whether the supporting label is in an error state.
    
    When True, the label is rendered in an error state, typically with a
    different color or style to indicate a validation issue.

    :attr:`error` is a :class:`~kivy.properties.BooleanProperty`
    and defaults to False.
    """

    maximum_width: int = NumericProperty(dp(200))
    """The maximum width for the supporting label.

    This property defines the maximum width that the supporting label
    can occupy. It helps in constraining the label's size within the
    text field layout.

    :attr:`maximum_width` is a :class:`~kivy.properties.NumericProperty`
    and defaults to dp(200).
    """
    
    default_config: Dict[str, Any] = dict(
        theme_color_bindings=dict(
            normal_content_color='content_surface_color',
            error_content_color='error_color',),
        typography_role='Label',
        typography_size='small',
        typography_weight='Regular',
        halign='left',
        valign='center',
        auto_size=True,)


class MorphTextFieldTextLengthLabel(MorphSimpleLabel):
    """Text length label for text fields with state properties.

    This label is specifically designed for use within text field
    components to display the current text length. It includes
    properties to indicate whether the label is disabled or in an
    error state, allowing for dynamic styling based on the text field's
    status.
    """

    disabled: bool = BooleanProperty(False)
    """Indicates whether the text length label is disabled.

    When True, the label is rendered in a disabled state, typically with
    a different color or style to indicate it is not interactive.

    :attr:`disabled` is a :class:`~kivy.properties.BooleanProperty`
    and defaults to False.
    """
    
    error: bool = BooleanProperty(False)
    """Indicates whether the text length label is in an error state.

    When True, the label is rendered in an error state, typically with a
    different color or style to indicate a validation issue.

    :attr:`error` is a :class:`~kivy.properties.BooleanProperty`
    and defaults to False.
    """
    
    default_config: Dict[str, Any] = dict(
        theme_color_bindings=dict(
            normal_content_color='content_surface_color',
            error_content_color='error_color',),
        typography_role='Label',
        typography_size='small',
        typography_weight='Regular',
        halign='right',
        valign='center',
        auto_size=True,)


class MorphTextFieldLeadingIconLabel(MorphSimpleIconLabel):
    """Leading icon label for text fields with state properties.

    This label is specifically designed for use within text field
    components to display a leading icon. It includes properties to
    indicate whether the label is disabled, focused, or in an error
    state, allowing for dynamic styling based on the text field's
    status.
    """

    disabled: bool = BooleanProperty(False)
    """Indicates whether the leading icon label is disabled.

    When True, the label is rendered in a disabled state, typically with
    a different color or style to indicate it is not interactive.

    :attr:`disabled` is a :class:`~kivy.properties.BooleanProperty`
    and defaults to False.
    """

    focus: bool = BooleanProperty(False)
    """Indicates whether the leading icon label is focused.

    When True, the label is rendered in a focused state,typically with a
    different color or style to indicate it is active.

    :attr:`focus` is a :class:`~kivy.properties.BooleanProperty`
    and defaults to False.
    """
    
    error: bool = BooleanProperty(False)
    """Indicates whether the leading icon label is in an error state.

    When True, the label is rendered in an error state, typically with a
    different color or style to indicate a validation issue.

    :attr:`error` is a :class:`~kivy.properties.BooleanProperty`
    and defaults to False.
    """
    
    default_config: Dict[str, Any] = dict(
        theme_color_bindings=dict(
            normal_content_color='content_surface_color',
            focus_content_color='primary_color',
            error_content_color='error_color',),
        font_name=MorphSimpleIconLabel.default_config['font_name'],
        typography_role=MorphSimpleIconLabel.default_config['typography_role'],
        typography_size=MorphSimpleIconLabel.default_config['typography_size'],
        halign='center',
        valign='center',
        pos_hint={'center_y': 0.5},
        size_hint=(None, None),
        size=(dp(24), dp(24)),
        padding=dp(0),)
