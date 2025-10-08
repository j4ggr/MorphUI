import warnings

from typing import Any
from typing import Dict
from typing import Literal

from kivy.event import EventDispatcher
from kivy.properties import DictProperty
from kivy.properties import StringProperty
from kivy.properties import OptionProperty
from kivy.properties import BooleanProperty

from ...app import MorphApp
from ...constants import THEME
from ...theme.manager import ThemeManager
from ...theme.typography import Typography


__all__ = [
    'MorphColorThemeBehavior',
    'MorphTypographyBehavior', 
    'MorphThemeBehavior']


class MorphColorThemeBehavior(EventDispatcher):
    """Behavior that provides automatic color theme integration for 
    MorphUI widgets.
    
    This behavior enables widgets to automatically respond to theme 
    changes by updating their color properties when the application 
    theme is modified. It provides a declarative way to bind widget 
    properties to theme colors and includes predefined style 
    configurations for common Material Design patterns.
    
    The behavior integrates seamlessly with other MorphUI behaviors, 
    particularly :class:`MorphSurfaceLayerBehavior`, to provide 
    comprehensive color theming capabilities including surface 
    colors, border colors, text colors, and other visual properties.
    
    Key Features
    ------------
    - Automatic color updates when theme changes (light/dark mode, 
      color scheme)
    - Declarative color binding through :attr:`theme_color_bindings`
    - Predefined Material Design style configurations
    - Fine-grained control with :attr:`auto_theme` property
    - Event-driven updates with :meth:`on_theme_changed` callback
    
    Theme Integration
    -----------------
    The behavior automatically connects to the application's 
    :class:`ThemeManager` and listens for theme change events. When 
    changes occur, it updates bound widget properties with the 
    corresponding theme colors.
    
    Examples
    --------
    Basic usage with automatic color binding:
    
    ```python
    from morphui.uix.behaviors.theming import MorphColorThemeBehavior
    from morphui.uix.behaviors.layer import MorphSurfaceLayerBehavior
    from kivy.uix.label import Label
    
    class ThemedButton(MorphColorThemeBehavior, MorphSurfaceLayerBehavior, Label):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            # Bind widget properties to theme colors
            self.theme_color_bindings = {
                'surface_color': 'primary_color',
                'border_color': 'outline_color',
                'content_color': 'content_primary_color'  # text color
            }
    ```
    
    Using predefined styles:
    
    ```python
    class QuickButton(MorphColorThemeBehavior, MorphSurfaceLayerBehavior, Label):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            # Apply a predefined Material Design style
            self.theme_style = 'primary'
    ```
    
    Custom theme change handling:
    
    ```python
    class AdvancedWidget(MorphColorThemeBehavior, Widget):
        def on_theme_changed(self):
            # Custom logic when theme changes
            if self.theme_manager.theme_mode == 'Dark':
                self.apply_theme_color('surface_color', 'surface_dim_color')
            else:
                self.apply_theme_color('surface_color', 'surface_bright_color')
    ```
    
    See Also
    --------
    - MorphSurfaceLayerBehavior : Provides surface and border styling 
      capabilities
    - MorphTypographyBehavior : Provides typography and text styling
      capabilities
    - ThemeManager : Manages application-wide theming and color schemes
    """

    auto_theme: bool = BooleanProperty(True)
    """Enable automatic theme updates for this widget.

    When True, the widget automatically updates its colors when the 
    theme changes. When False, the widget retains its current colors 
    until manually updated.

    :attr:`auto_theme` is a :class:`~kivy.properties.BooleanProperty` 
    and defaults to True.
    """

    theme_style: str = StringProperty('')
    """Predefined theme style to apply to this widget.

    This property allows you to set a predefined Material Design style
    configuration for the widget. When set to a valid style name, it
    automatically applies the corresponding set of color bindings from
    :attr:`theme_style_mappings` via the :meth:`on_theme_style` event 
    handler.
    
    This provides a quick way to style widgets according to established
    Material Design roles such as 'primary', 'secondary', 'tertiary',
    'surface', 'error', and 'outline'. The property uses Kivy's 
    StringProperty binding system, so changes are automatically 
    detected and applied.
    
    When an invalid style name is provided, the change is silently 
    ignored and the property retains its previous value. Setting to an
    empty string ('') effectively disables any predefined style without
    clearing existing color bindings.

    Available Styles
    ----------------
    - **'primary'**: High-emphasis style for primary actions
    - **'secondary'**: Medium-emphasis style for secondary actions
    - **'tertiary'**: Medium-emphasis style for tertiary actions
    - **'surface'**: Standard surface style for content areas
    - **'error'**: Error state style for warnings and alerts
    - **'outline'**: Low-emphasis outlined style
    - **''**: Empty string (no predefined style)

    Each style configures appropriate color bindings for surface,
    text, and border colors according to Material Design guidelines.

    :attr:`theme_style` is a :class:`~kivy.properties.StringProperty`
    and defaults to ''.
    """

    theme_color_bindings: Dict[str, str] = DictProperty({})
    """Dictionary mapping widget properties to theme color names.
    
    This dictionary defines the automatic color binding configuration 
    for the widget. Each key represents a widget property name (such as 
    'surface_color', 'content_color', 'border_color') and each value 
    represents the corresponding theme color property name from the 
    :class:`ThemeManager` (such as 'primary_color', 'surface_color').

    When the theme changes, widget properties listed here will be
    automatically updated with the corresponding theme color values.
    
    Examples
    --------
    Basic color binding:
    
    ```python
    widget.theme_color_bindings = {
        'surface_color': 'primary_color',
        'content_color': 'content_primary_color',
        'border_color': 'outline_color'
    }
    ```
    
    Error state styling:
    
    ```python
    widget.theme_color_bindings = {
        'surface_color': 'error_color',
        'content_color': 'content_error_color',
        'border_color': 'error_color'
    }
    ```
    
    :attr:`theme_color_bindings` is a
    :class:`~kivy.properties.DictProperty` and defaults to {}.
    """

    theme_style_mappings: Dict[str, Dict[str, str]] = THEME.STYLES
    """Predefined theme style mappings from constants.
    
    This class attribute contains the default Material Design style
    configurations. Subclasses can override this to provide custom
    or additional style mappings.
    """

    _theme_bound: bool = False
    """Track if theme manager events are bound."""
    
    def __init__(self, **kwargs) -> None:
        self.register_event_type('on_colors_updated')
        super().__init__(**kwargs)

        self.theme_manager.bind(on_colors_updated=self._update_colors)

    @property
    def theme_manager(self) -> ThemeManager:
        """Access the theme manager for theming and style management
        (read-only).

        The :attr:`theme_manager` attribute provides access to the
        :class:`ThemeManager` instance, which handles theming and style
        management. This instance is automatically initialized as a
        class attribute and shared across all instances of this
        behavior.
        """
        return MorphApp._theme_manager

    def on_theme_color_bindings(
            self, instance: Any, bindings: Dict[str, str]) -> None:
        """Fired when :attr:`theme_color_bindings` property changes. 
        
        This method updates the widget's colors based on the new
        dictionary of bindings by calling :meth:`_update_colors`.
        
        Parameters
        ----------
        instance : Any
            The widget instance that triggered the property change.
        bindings : Dict[str, str]
            The new dictionary mapping widget properties to theme color
            names. Where keys are widget property names (e.g.,
            'surface_color') and values are theme color names (e.g.,
            'primary_color').
        """
        self._update_colors()

    def apply_theme_color(self, widget_property: str, theme_color: str) -> bool:
        """Apply a specific theme color to a widget property.
        
        This method provides manual control over theme color
        application, allowing you to update individual widget properties
        with specific theme colors outside of the automatic binding
        system.
        
        The method safely handles cases where the theme color doesn't
        exist or the widget property is not available, returning False
        in such cases.
        
        Parameters
        ----------
        widget_property : str
            The name of the widget property to update. Must be a valid
            property on this widget instance (e.g., 'surface_color',
            'content_color', 'border_color').
        theme_color : str
            The name of the theme color property to use. Must be a valid
            color property on the ThemeManager (e.g., 'primary_color',
            'surface_color', 'on_primary_color').
            
        Returns
        -------
        bool
            True if the color was successfully applied, False if either
            the theme color doesn't exist, the widget property doesn't
            exist, or the theme color value is None.
            
        Examples
        --------
        Apply primary color to surface:
        
        ```python
        success = widget.apply_theme_color('surface_color', 'primary_color')
        if success:
            print("Color applied successfully")
        ```
        
        Conditional color application:
        
        ```python
        if widget.theme_manager.theme_mode == 'Dark':
            widget.apply_theme_color('surface_color', 'surface_dim_color')
        else:
            widget.apply_theme_color('surface_color', 'surface_bright_color')
        ```
        """
        if hasattr(self.theme_manager, theme_color):
            color_value = getattr(self.theme_manager, theme_color)
            if color_value is not None and hasattr(self, widget_property):
                setattr(self, widget_property, color_value)
                return True
        return False

    def _update_colors(self, *args) -> None:
        """Update widget colors based on current theme."""
        if not self.auto_theme or not self.theme_color_bindings:
            return
            
        for widget_prop, theme_color in self.theme_color_bindings.items():
            self.apply_theme_color(widget_prop, theme_color)
        self.dispatch('on_colors_updated')

    def on_auto_theme(self, instance: Any, auto_theme: bool) -> None:
        """Fired when :attr:`auto_theme` property changes."""
        if auto_theme:
            self._update_colors()

    def on_theme_style(self, instance: Any, style_name: str) -> None:
        """Event handler fired when :attr:`theme_style` property 
        changes.
        
        This method is automatically called when the theme_style 
        property is modified, applying the corresponding predefined 
        style configuration from :attr:`theme_style_mappings` to the 
        widget.
        
        The method provides convenient access to common Material Design
        color combinations by applying predefined
        :attr:`theme_color_bindings` based on Material Design component
        roles and states.
        
        Each style configures appropriate color bindings for surface,
        text, and border colors according to Material Design guidelines.
        
        Parameters
        ----------
        instance : Any
            The widget instance that triggered the property change.
        style_name : str
            The name of the predefined style to apply. Available 
            options:
            
            - **'primary'**: High-emphasis style for primary actions
              - Uses primary_color for surface and borders
              - Uses on_primary_color for text/content
              - Ideal for: Main action buttons, important controls
              
            - **'secondary'**: Medium-emphasis style for secondary 
              actions
              - Uses secondary_color for surface and borders
              - Uses on_secondary_color for text/content
              - Ideal for: Secondary buttons, complementary actions
              
            - **'surface'**: Standard surface style for content areas
              - Uses surface_color for surface
              - Uses outline_color for borders
              - Uses on_surface_color for text/content
              - Ideal for: Cards, panels, content containers
              
            - **'error'**: Error state style for warnings and alerts
              - Uses error_color for surface and borders
              - Uses on_error_color for text/content
              - Ideal for: Error messages, warning dialogs, destructive
                actions
              
            - **'outline'**: Low-emphasis outlined style
              - Uses surface_color for surface
              - Uses outline_color for borders (creates outlined
                appearance)
              - Uses on_surface_color for text/content
              - Ideal for: Outlined buttons, optional actions
              
            - **''**: Empty string - no style applied
        
        Notes
        -----
        If an invalid style_name is provided, the method silently 
        ignores the request without raising an error. Empty string
        values are accepted and effectively disable predefined styling.
        
        This method is called automatically by Kivy's property binding
        system when the :attr:`theme_style` property changes. You 
        typically don't need to call this method directly - instead, set 
        the :attr:`theme_style` property:

        ```python
        widget.theme_style = 'primary'  # Triggers on_theme_style automatically
        ```
            
        Examples
        --------
        The following property assignments will trigger this event handler:
        
        ```python
        # High-emphasis action
        widget.theme_style = 'primary'
        
        # Medium-emphasis action  
        widget.theme_style = 'secondary'

        # Medium-emphasis action
        widget.theme_style = 'tertiary'
        
        # Low-emphasis action
        widget.theme_style = 'outline'
        
        # Error/destructive action
        widget.theme_style = 'error'
        
        # Surface container styling
        widget.theme_style = 'surface'
        
        # Clear predefined styling
        widget.theme_style = ''
        ```
        
        See Also
        --------
        - :meth:`bind_theme_colors` : For custom color binding 
          configurations
        - :attr:`theme_color_bindings` : The underlying property that 
          stores color mappings
        - :attr:`theme_style_mappings` : Class attribute containing the 
          style definitions
        """
        style_mappings = self.theme_style_mappings.get(style_name, None)
        if style_mappings is not None:
            self.theme_color_bindings = (
                self.theme_color_bindings.copy() | style_mappings)
        elif style_name != '':
            warnings.warn(
                f"Unknown theme_style '{style_name}', ignoring",
                UserWarning)

    def add_custom_style(
            self, style_name: str, color_mappings: Dict[str, str]) -> None:
        """Add a custom theme style to the available styles.
        
        This method allows you to define new theme styles that can be
        used by setting the :attr:`theme_style` property. Custom styles
        are added to the instance's :attr:`theme_style_mappings` and can 
        be used immediately.

        If a style with the same name already exists, it will be
        overwritten with the new color mappings. This allows you to
        customize or update existing styles as needed.
        
        Parameters
        ----------
        style_name : str
            The name for the new custom style.
        color_mappings : Dict[str, str]
            Dictionary mapping widget properties to theme color names,
            same format as :attr:`theme_color_bindings`.
            
        Examples
        --------
        Add a custom warning style:
        
        ```python
        widget.add_custom_style('warning', {
            'surface_color': 'error_container_color',
            'content_color': 'content_error_container_color',
            'border_color': 'outline_color'
        })
        
        # Now use the custom style
        widget.theme_style = 'warning'
        ```
        
        Add a subtle style:
        
        ```python
        widget.add_custom_style('subtle', {
            'surface_color': 'surface_variant_color',
            'content_color': 'content_surface_variant_color',
            'border_color': 'outline_variant_color'
        })
        ```

        Notes
        -----
        If this is the first custom style being added to the instance,
        the method creates a copy of the class-level theme_style_
        mappings. This ensures that modifications to the instance's
        style mappings do not affect other instances or the class.
        If you want to modify the class-level mappings for all
        instances, you can do so by directly modifying the 
        :attr:`theme_style_mappings` class attribute.
        """
        if self.theme_style_mappings is self.__class__.theme_style_mappings:
            self.theme_style_mappings = self.__class__.theme_style_mappings.copy()
        
        self.theme_style_mappings[style_name] = color_mappings

    def refresh_theme_colors(self) -> None:
        """Manually refresh all theme colors.
        
        This method forces an update of all bound theme colors,
        useful when you want to ensure colors are up to date.
        """
        auto_theme = self.auto_theme
        self.auto_theme = True
        self._update_colors()
        self.auto_theme = auto_theme

    def on_colors_updated(self, *args) -> None:
        """Event callback fired after theme colors are updated within
        the theme manager but before they are applied to the widget.

        This can be used to perform actions or adjustments based on the
        new color values before they are applied to the widget's
        properties.

        Override this method in subclasses to implement custom
        behavior when theme colors are updated.
        """
        pass


class MorphTypographyBehavior(EventDispatcher):
    """Behavior that provides automatic typography integration for 
    MorphUI widgets.
    
    This behavior enables widgets to automatically apply Material Design 
    typography styles and respond to typography system changes. It
    provides a declarative way to set typography roles, sizes, and
    weights while maintaining consistency with the application's
    typography system.
    
    Key Features
    ------------
    - Automatic typography updates when app font family changes
    - Material Design typography role system (Display, Headline, Title,
      Body, Label)
    - Typography size variants (large, medium, small)
    - Font weight control (Thin, Regular, Heavy)
    - Fine-grained control with :attr:`auto_typography` property
    - Event-driven updates with :meth:`on_typography_changed` callback
    
    Typography Integration
    ----------------------
    The behavior automatically connects to the application's 
    :class:`Typography` system and listens for typography change events.
    When changes occur, it updates the widget's typography properties
    according to the current role, size, and weight settings.
    
    Examples
    --------
    Basic usage with typography role:
    
    ```python
    from morphui.uix.behaviors.theming import MorphTypographyBehavior
    from kivy.uix.label import Label
    
    class TypedLabel(MorphTypographyBehavior, Label):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            self.typography_role = 'Headline'
            self.typography_size = 'large'
    ```
    
    Manual typography application:
    
    ```python
    class CustomWidget(MorphTypographyBehavior, Widget):
        def setup_typography(self):
            self.apply_typography_style(
                role='Body', 
                size='medium', 
                font_weight='Regular'
            )
    ```
    
    See Also
    --------
    MorphColorThemeBehavior : Provides color theme integration
    Typography : Manages application-wide typography styles
    """

    typography_role: Literal['Display', 'Headline', 'Title', 'Body', 'Label'] = OptionProperty(
        'Label', options=['Display', 'Headline', 'Title', 'Body', 'Label'])
    """Typography role for automatic text styling.
    
    Sets the Material Design typography role which automatically
    configures appropriate font family, size, and line height. Available
    roles: 'Display', 'Headline', 'Title', 'Body', 'Label'.
    
    When set, the widget automatically applies the corresponding
    typography style based on the current :attr:`typography_size` and
    app font settings.
    
    :attr:`typography_role` is a :class:`~kivy.properties.OptionProperty`
    and defaults to 'Label'.
    """

    typography_size: Literal['large', 'medium', 'small'] = OptionProperty(
        'medium', options=['large', 'medium', 'small'])
    """Size variant for the typography role.
    
    Available options: 'large', 'medium', 'small'
    Works in conjunction with :attr:`typography_role` to determine
    the final text styling.
    
    :attr:`typography_size` is a
    :class:`~kivy.properties.OptionProperty` and defaults to 'medium'.
    """

    typography_weight: Literal['Thin', 'Regular', 'Heavy'] = OptionProperty(
         'Regular', options=['Thin', 'Regular', 'Heavy'])
    """Weight variant for the typography role.

    Available options: 'Thin', 'Regular', 'Heavy'
    Works in conjunction with :attr:`typography_role` to determine
    the final text styling.

    :attr:`typography_weight` is a
    :class:`~kivy.properties.OptionProperty` and defaults to 'Regular'.
    """

    auto_typography: bool = BooleanProperty(True)
    """Enable automatic typography updates for this widget.
    
    When True, the widget automatically updates its typography when the
    app font family changes or when typography properties are modified.
    
    :attr:`auto_typography` is a
    :class:`~kivy.properties.BooleanProperty` and defaults to True.
    """
    
    def __init__(self, **kwargs) -> None:
        self.register_event_type('on_typography_updated')
        super().__init__(**kwargs)

        self.fbind('typography_role', self._update_typography)
        self.fbind('typography_size', self._update_typography)
        self.fbind('typography_weight', self._update_typography)
        self.typography.bind(
            on_typography_changed=self._update_typography)

    @property
    def typography(self) -> Typography:
        """Access the global typography manager for text style
        management (read-only).

        The :attr:`typography` attribute provides access to the
        :class:`Typography` instance, which handles typography and text
        style management. This instance is automatically initialized as 
        a class attribute and shared across all instances of this 
        behavior.
        """
        return MorphApp._typography

    def apply_typography_style(
            self,
            role: Literal['Display', 'Headline', 'Title', 'Body', 'Label'],
            size: Literal['large', 'medium', 'small'],
            font_weight: Literal['Thin', 'Regular', 'Heavy'] = 'Regular'
            ) -> None:
        """Apply typography style to this widget.

        This method applies the specified typography style to the widget
        based on the provided role, size, and font weight. It retrieves
        the appropriate text style from the :attr:`typography` system and
        updates the widget's font properties accordingly.
        
        Parameters
        ----------
        role : str
            Typography role ('Display', 'Headline', 'Title', 'Body', 'Label')
        size : str
            Size variant ('large', 'medium', 'small')
        font_weight : str, optional
            Font weight ('Thin', 'Regular', 'Heavy'), defaults to 'Regular'
        """ 
        style = self.typography.get_text_style(
            role=role, size=size, font_weight=font_weight)
        
        # Apply font properties if widget has them
        if hasattr(self, 'font_name') and 'name' in style:
            self.font_name = style['name']

        for key, value in style.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.dispatch('on_typography_updated')

    def _update_typography(self, *args) -> None:
        """Update typography based on current settings.
        
        This method applies the typography style to the widget
        based on the current :attr:`typography_role`, 
        :attr:`typography_size`, and :attr:`typography_weight`.
        
        If :attr:`auto_typography` is False, the method does nothing.
        This method is typically called when typography-related
        properties change or when the typography system is updated.
        """
        if not self.auto_typography:
            return None
            
        self.apply_typography_style(
            role=self.typography_role,
            size=self.typography_size,
            font_weight=self.typography_weight)
    
    def refresh_typography(self) -> None:
        """Manually refresh typography style.
        
        This method forces an update of the typography style,
        useful when you want to ensure typography is up to date."""
        auto_typography = self.auto_typography
        self.auto_typography = True
        self._update_typography()
        self.auto_typography = auto_typography

    def on_typography_updated(self, *args) -> None:
        """Called after typography is applied to the widget.

        Override this method in subclasses to implement custom
        behavior when typography is updated.
        """
        pass


class MorphThemeBehavior(MorphColorThemeBehavior, MorphTypographyBehavior):
    """Combined behavior providing both color theming and typography integration.
    
    This behavior combines :class:`MorphColorThemeBehavior` and 
    :class:`MorphTypographyBehavior` to provide comprehensive theming 
    capabilities including automatic color updates, typography styling,
    and theme integration.
    
    This is a convenience class that provides the same functionality as
    the original MorphThemeBehavior while allowing users to choose between
    the combined behavior or individual specialized behaviors.
    
    For new code, consider using the individual behaviors (:class:`MorphColorThemeBehavior`
    and :class:`MorphTypographyBehavior`) for better modularity and clearer separation
    of concerns.
    
    Examples
    --------
    Using the combined behavior:
    
    ```python
    from morphui.uix.behaviors.layer import MorphSurfaceLayerBehavior
    from morphui.uix.behaviors.theming import MorphThemeBehavior
    from kivy.uix.label import Label
    
    class FullyThemedLabel(MorphThemeBehavior, MorphSurfaceLayerBehavior, Label):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            self.theme_style = 'primary'
            self.typography_role = 'Headline'
            self.typography_size = 'large'
    ```
    
    See Also
    --------
    MorphColorThemeBehavior : Provides color theme integration only
    MorphTypographyBehavior : Provides typography integration only
    """
    pass
