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
    """Behavior that provides automatic color theme integration for MorphUI 
    widgets.
    
    This behavior enables widgets to automatically respond to theme 
    changes by updating their color properties when the application 
    theme is modified. It provides a declarative way to bind widget 
    properties to theme colors and includes predefined style 
    configurations for common Material Design patterns.
    
    The behavior integrates seamlessly with other MorphUI behaviors, 
    particularly :class:`MorphBackgroundBehavior`, to provide 
    comprehensive color theming capabilities including background colors,  
    border colors, text colors, and other visual properties.
    
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
    from morphui.uix.behaviors.background import MorphBackgroundBehavior
    from kivy.uix.label import Label
    
    class ThemedButton(MorphColorThemeBehavior, MorphBackgroundBehavior, Label):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            # Bind widget properties to theme colors
            self.theme_color_bindings = {
                'background_color': 'primary_color',
                'border_color': 'outline_color',
                'color': 'text_primary_color'  # text color
            }
    ```
    
    Using predefined styles:
    
    ```python
    class QuickButton(MorphColorThemeBehavior, MorphBackgroundBehavior, Label):
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
                self.apply_theme_color('background_color', 'surface_dim_color')
            else:
                self.apply_theme_color('background_color', 'surface_bright_color')
    ```
    
    See Also
    --------
    MorphBackgroundBehavior : Provides background and border styling capabilities
    MorphTypographyBehavior : Provides typography and text styling capabilities
    ThemeManager : Manages application-wide theming and color schemes
    """

    auto_theme: bool = BooleanProperty(True)
    """Enable automatic theme updates for this widget.

    When True, the widget automatically updates its colors when the theme 
    changes. When False, the widget retains its current colors until 
    manually updated.

    :attr:`auto_theme` is a :class:`~kivy.properties.BooleanProperty` 
    and defaults to True.
    """

    theme_style: str = StringProperty('')
    """Predefined theme style to apply to this widget.

    This property allows you to set a predefined Material Design style
    configuration for the widget. When set to a valid style name, it
    automatically applies the corresponding set of color bindings from
    :attr:`theme_style_mappings` via the :meth:`on_theme_style` event handler.
    
    This provides a quick way to style widgets according to established
    Material Design roles such as 'primary', 'secondary', 'surface', 'error',
    and 'outline'. The property uses Kivy's StringProperty binding system,
    so changes are automatically detected and applied.
    
    When an invalid style name is provided, the change is silently ignored
    and the property retains its previous value. Setting to an empty string
    ('') effectively disables any predefined style without clearing existing
    color bindings.

    Available Styles
    ----------------
    - **'primary'**: High-emphasis style for primary actions
    - **'secondary'**: Medium-emphasis style for secondary actions  
    - **'surface'**: Standard surface style for content areas
    - **'error'**: Error state style for warnings and alerts
    - **'outline'**: Low-emphasis outlined style
    - **''**: Empty string (no predefined style)

    Each style configures appropriate color bindings for background,
    text, and border colors according to Material Design guidelines.

    :attr:`theme_style` is a :class:`~kivy.properties.StringProperty`
    and defaults to ''.
    """

    theme_color_bindings: Dict[str, str] = DictProperty({})
    """Dictionary mapping widget properties to theme color names.
    
    This dictionary defines the automatic color binding configuration 
    for the widget. Each key represents a widget property name (such as 
    'background_color', 'color', 'border_color') and each value 
    represents the corresponding theme color property name from the 
    :class:`ThemeManager` (such as 'primary_color', 'surface_color').

    When the theme changes, widget properties listed here will be
    automatically updated with the corresponding theme color values.
    
    Examples
    --------
    Basic color binding:
    
    ```python
    widget.theme_color_bindings = {
        'background_color': 'primary_color',
        'color': 'text_primary_color',
        'border_color': 'outline_color'
    }
    ```
    
    Error state styling:
    
    ```python
    widget.theme_color_bindings = {
        'background_color': 'error_color',
        'color': 'text_error_color',
        'border_color': 'error_color'
    }
    ```
    
    :attr:`theme_color_bindings` is a :class:`~kivy.properties.DictProperty` 
    and defaults to {}.
    """

    _bound_theme_colors: Dict[str, str] = {}
    """Track currently bound theme colors to widget properties. Where
    keys are widget property names and values are the corresponding
    theme color names."""

    theme_style_mappings: Dict[str, Dict[str, str]] = THEME.STYLES
    """Predefined theme style mappings from constants.
    
    This class attribute contains the default Material Design style
    configurations. Subclasses can override this to provide custom
    or additional style mappings.
    """

    _theme_manager: ThemeManager = MorphApp._theme_manager
    """Reference to the global ThemeManager instance."""

    _theme_bound: bool = False
    """Track if theme manager events are bound."""
    
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.register_event_type('on_theme_changed')
        self.register_event_type('on_colors_updated')

        self.theme_manager.bind(
            on_theme_changed=self.on_theme_changed,
            on_colors_updated=self.on_colors_updated)

        self.refresh_theme_colors()

    @property
    def theme_manager(self) -> ThemeManager:
        """Access the theme manager for theming and style management (read-only).

        The :attr:`theme_manager` attribute provides access to the
        :class:`ThemeManager` instance, which handles theming and style
        management. This instance is automatically initialized as a
        class attribute and shared across all instances of this behavior.
        """
        return self._theme_manager
    
    def bind_property_to_theme_color(
            self, widget_property: str, theme_color: str) -> None:
        """Bind a widget property to a dynamic theme color.

        This method sets up a binding between a widget property and a
        theme color, allowing the widget property to automatically
        update when the theme color changes.

        If the widget property is already bound to the specified
        theme color, this method does nothing.

        Parameters
        ----------
        widget_property : str
            The name of the widget property to bind (e.g., 
            'background_color').
        theme_color : str
            The name of the theme color to bind to (e.g., 
            'primary_color').
        """
        if any((
            not hasattr(self, widget_property),
            not hasattr(self.theme_manager, theme_color),
            self._bound_theme_colors.get(widget_property) == theme_color)):
            return
        
        self.theme_manager.bind(
            **{theme_color: self.setter(widget_property)})
        self._bound_theme_colors[widget_property] = theme_color
    
    def unbind_property_from_theme_color(
            self, widget_property: str, theme_color: str) -> None:
        """Unbind a widget property from a dynamic theme color.

        This method removes the binding between a widget property and a
        theme color.

        If the widget property is not currently bound to the specified
        theme color, this method does nothing.

        Parameters
        ----------
        widget_property : str
            The name of the widget property to unbind (e.g., 
            'background_color').
        theme_color : str
            The name of the theme color to unbind from (e.g., 
            'primary_color').
        """
        if any((
            not hasattr(self, widget_property),
            not hasattr(self.theme_manager, theme_color),
            self._bound_theme_colors.get(widget_property, '') != theme_color)):
            return
        
        self.theme_manager.unbind(
            **{theme_color: self.setter(widget_property)})
        self._bound_theme_colors.pop(widget_property, None)

    def on_theme_color_bindings(
            self, instance: Any, bindings: Dict[str, str]) -> None:
        """Fired when :attr:`theme_color_bindings` property changes. 
        
        This method updates the widget's color bindings based on the
        new dictionary of bindings. It ensures that any previously bound
        properties are unbound if they are no longer present in the new
        bindings, and binds any new properties to their corresponding
        theme colors.
        
        If :attr:`auto_theme` is False, it applies the new colors
        immediately without setting up bindings.
        
        Parameters
        ----------
        instance : Any
            The widget instance that triggered the property change.
        bindings : Dict[str, str]
            The new dictionary mapping widget properties to theme color
            names. Where keys are widget property names (e.g.,
            'background_color') and values are theme color names (e.g.,
            'primary_color').
        """
        for name, color in bindings.items():
            if self.auto_theme:
                old_color = self._bound_theme_colors.get(name, '')
                if color and color != old_color:
                    self.unbind_property_from_theme_color(name, old_color)
                self.bind_property_to_theme_color(name, color)

        self._update_colors()

    def apply_theme_color(self, widget_property: str, theme_color: str) -> bool:
        """Apply a specific theme color to a widget property.
        
        This method provides manual control over theme color application,
        allowing you to update individual widget properties with specific
        theme colors outside of the automatic binding system.
        
        The method safely handles cases where the theme color doesn't exist
        or the widget property is not available, returning False in such cases.
        
        Parameters
        ----------
        widget_property : str
            The name of the widget property to update. Must be a valid
            property on this widget instance (e.g., 'background_color',
            'color', 'border_color').
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
        Apply primary color to background:
        
        ```python
        success = widget.apply_theme_color('background_color', 'primary_color')
        if success:
            print("Color applied successfully")
        ```
        
        Conditional color application:
        
        ```python
        if widget.theme_manager.theme_mode == 'Dark':
            widget.apply_theme_color('background_color', 'surface_dim_color')
        else:
            widget.apply_theme_color('background_color', 'surface_bright_color')
        ```
        """
        if hasattr(self.theme_manager, theme_color):
            color_value = getattr(self.theme_manager, theme_color)
            if color_value is not None and hasattr(self, widget_property):
                setattr(self, widget_property, color_value)
                return True
        return False

    def _update_colors(self) -> None:
        """Update widget colors based on current theme."""
        if not self.auto_theme or not self.theme_color_bindings:
            return
            
        for widget_prop, theme_color in self.theme_color_bindings.items():
            self.apply_theme_color(widget_prop, theme_color)

    def on_auto_theme(self, instance: Any, auto_theme: bool) -> None:
        """Fired when :attr:`auto_theme` property changes."""
        if auto_theme:
            self.on_theme_color_bindings(self, self.theme_color_bindings)
        else:
            for name, color in self.theme_color_bindings.items():
                self.unbind_property_from_theme_color(name, color)

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
        
        Each style configures appropriate color bindings for background,
        text, and border colors according to Material Design guidelines.
        
        Parameters
        ----------
        instance : Any
            The widget instance that triggered the property change.
        style_name : str
            The name of the predefined style to apply. Available 
            options:
            
            - **'primary'**: High-emphasis style for primary actions
              - Uses primary_color for background and borders
              - Uses on_primary_color for text/content
              - Ideal for: Main action buttons, important controls
              
            - **'secondary'**: Medium-emphasis style for secondary 
              actions
              - Uses secondary_color for background and borders
              - Uses on_secondary_color for text/content
              - Ideal for: Secondary buttons, complementary actions
              
            - **'surface'**: Standard surface style for content areas
              - Uses surface_color for background
              - Uses outline_color for borders
              - Uses on_surface_color for text/content
              - Ideal for: Cards, panels, content containers
              
            - **'error'**: Error state style for warnings and alerts
              - Uses error_color for background and borders
              - Uses on_error_color for text/content
              - Ideal for: Error messages, warning dialogs, destructive
                actions
              
            - **'outline'**: Low-emphasis outlined style
              - Uses surface_color for background
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
        if style_mappings:
            self.theme_color_bindings |= style_mappings

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
            'background_color': 'error_container_color',
            'color': 'text_error_container_color',
            'border_color': 'outline_color'
        })
        
        # Now use the custom style
        widget.theme_style = 'warning'
        ```
        
        Add a subtle style:
        
        ```python
        widget.add_custom_style('subtle', {
            'background_color': 'surface_variant_color',
            'color': 'text_surface_variant_color',
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
        self._update_colors()

    def on_theme_changed(self, *args) -> None:
        """Event callback fired when the application theme changes.
        
        This method is bound to the :meth:`ThemeManager.on_theme_changed`
        method and is automatically invoked whenever the theme changes.
        
        Override this method in subclasses to implement custom
        behavior when the theme changes.
        """
        pass

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
    """Behavior that provides automatic typography integration for MorphUI widgets.
    
    This behavior enables widgets to automatically apply Material Design 
    typography styles and respond to typography system changes. It provides 
    a declarative way to set typography roles, sizes, and weights while 
    maintaining consistency with the application's typography system.
    
    Key Features
    ------------
    - Automatic typography updates when app font family changes
    - Material Design typography role system (Display, Headline, Title, Body, Label)
    - Typography size variants (large, medium, small)
    - Font weight control (Thin, Regular, Heavy)
    - Fine-grained control with :attr:`auto_typography` property
    - Event-driven updates with :meth:`on_typography_changed` callback
    
    Typography Integration
    ----------------------
    The behavior automatically connects to the application's 
    :class:`Typography` system and listens for typography change events. When 
    changes occur, it updates the widget's typography properties according to 
    the current role, size, and weight settings.
    
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
    
    Sets the Material Design typography role which automatically configures
    appropriate font family, size, and line height. Available roles: 'Display',
    'Headline', 'Title', 'Body', 'Label'.
    
    When set, the widget automatically applies the corresponding typography
    style based on the current :attr:`typography_size` and app font settings.
    
    :attr:`typography_role` is a :class:`~kivy.properties.OptionProperty`
    and defaults to 'Label'.
    """

    typography_size: Literal['large', 'medium', 'small'] = OptionProperty(
        'medium', options=['large', 'medium', 'small'])
    """Size variant for the typography role.
    
    Available options: 'large', 'medium', 'small'
    Works in conjunction with :attr:`typography_role` to determine
    the final text styling.
    
    :attr:`typography_size` is a :class:`~kivy.properties.OptionProperty`
    and defaults to 'medium'.
    """

    typography_font_weight: Literal['Thin', 'Regular', 'Heavy', ''] = OptionProperty(
        '', options=['Thin', 'Regular', 'Heavy', ''])
    """Weight variant for the typography role.

    Available options: 'Thin', 'Regular', 'Heavy', ''
    Works in conjunction with :attr:`typography_role` to determine
    the final text styling.

    :attr:`typography_font_weight` is a :class:`~kivy.properties.OptionProperty`
    and defaults to ''.
    """

    auto_typography: bool = BooleanProperty(True)
    """Enable automatic typography updates for this widget.
    
    When True, the widget automatically updates its typography when the
    app font family changes or when typography properties are modified.
    
    :attr:`auto_typography` is a :class:`~kivy.properties.BooleanProperty`
    and defaults to True.
    """

    _typography: Typography = MorphApp._typography
    """Reference to the global Typography instance."""
    
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.register_event_type('on_typography_changed')

        self.typography.bind(
            on_typography_changed=self.on_typography_changed)
        self.bind(
            typography_role=self._update_typography,
            typography_size=self._update_typography,
            typography_font_weight=self._update_typography,
            auto_typography=self._update_typography,
            on_typography_changed=self._update_typography)

        self.refresh_typography()

    @property
    def typography(self) -> Typography:
        """Access the typography manager for text style management 
        (read-only).

        The :attr:`typography` attribute provides access to the
        :class:`Typography` instance, which handles typography and text
        style management. This instance is automatically initialized as 
        a class attribute and shared across all instances of this 
        behavior.
        """
        return self._typography

    def apply_typography_style(
            self,
            role: Literal['Display', 'Headline', 'Title', 'Body', 'Label'],
            size: Literal['large', 'medium', 'small'],
            font_weight: Literal['Thin', 'Regular', 'Heavy', ''] = ''
            ) -> bool:
        """Apply typography style to this widget.
        
        Parameters
        ----------
        role : str
            Typography role ('Display', 'Headline', 'Title', 'Body', 'Label')
        size : str
            Size variant ('large', 'medium', 'small')
        font_weight : str, optional
            Font weight ('Thin', 'Regular', 'Heavy', ''), defaults to ''
            
        Returns
        -------
        bool
            True if style was successfully applied
        """ 
        try:
            style = self.typography.get_text_style(
                role=role, size=size, font_weight=font_weight)
            
            # Apply font properties if widget has them
            if hasattr(self, 'font_name') and 'name' in style:
                self.font_name = style['name']
            if hasattr(self, 'font_size') and 'font_size' in style:
                self.font_size = style['font_size']
                
            return True
        except (AssertionError, KeyError):
            return False

    def _update_typography(self, *args) -> None:
        """Update typography based on current settings.
        
        This method applies the typography style to the widget
        based on the current :attr:`typography_role`, 
        :attr:`typography_size`, and :attr:`typography_font_weight`.
        
        If :attr:`auto_typography` is False, the method does nothing.
        This method is typically called when typography-related
        properties change or when the typography system is updated.
        """
        if not self.auto_typography:
            return None
            
        self.apply_typography_style(
            role=self.typography_role,
            size=self.typography_size,
            font_weight=self.typography_font_weight)
    
    def refresh_typography(self) -> None:
        """Manually refresh typography style.
        
        This method forces an update of the typography style,
        useful when you want to ensure typography is up to date."""
        self._update_typography()

    def on_typography_changed(self, *args) -> None:
        """Called when the typography system changes (e.g., font family).

        This method is automatically invoked whenever the typography
        system is updated. Override this method in subclasses to
        implement custom behavior when the typography system changes.
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
    from morphui.uix.behaviors.theming import MorphThemeBehavior
    from morphui.uix.behaviors.background import MorphBackgroundBehavior
    from kivy.uix.label import Label
    
    class FullyThemedLabel(MorphThemeBehavior, MorphBackgroundBehavior, Label):
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
