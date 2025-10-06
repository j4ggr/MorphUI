
from typing import Dict
from typing import Any

from kivy.event import EventDispatcher
from kivy.properties import BooleanProperty
from kivy.properties import DictProperty

from ...app import MorphApp
from ...theme.manager import ThemeManager
from ...constants import THEME


__all__ = [
    'MorphThemeBehavior']


class MorphThemeBehavior(EventDispatcher):
    """Behavior that provides automatic theme integration for MorphUI 
    widgets.
    
    This behavior enables widgets to automatically respond to theme 
    changes by updating their color properties when the application 
    theme is modified. It provides a declarative way to bind widget 
    properties to theme colors and includes predefined style 
    configurations for common Material Design patterns.
    
    The behavior integrates seamlessly with other MorphUI behaviors, 
    particularly :class:`MorphBackgroundBehavior`, to provide 
    comprehensive theming capabilities including background colors,  
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
    from morphui.uix.behaviors.theming import MorphThemeBehavior
    from morphui.uix.behaviors.background import MorphBackgroundBehavior
    from kivy.uix.label import Label
    
    class ThemedButton(MorphThemeBehavior, MorphBackgroundBehavior, Label):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            # Bind widget properties to theme colors
            self.theme_color_bindings = {
                'background_color': 'primary_color',
                'border_color': 'outline_color',
                'color': 'on_primary_color'  # text color
            }
    ```
    
    Using predefined styles:
    
    ```python
    class QuickButton(MorphThemeBehavior, MorphBackgroundBehavior, Label):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            # Apply a predefined Material Design style
            self.set_theme_style('primary')
    ```
    
    Custom theme change handling:
    
    ```python
    class AdvancedWidget(MorphThemeBehavior, Widget):
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

    theme_color_bindings: Dict[str, str] = DictProperty({})
    """Dictionary mapping widget properties to theme color names.
    
    This dictionary defines the automatic color binding configuration for the widget.
    Each key represents a widget property name (such as 'background_color', 'color', 
    'border_color') and each value represents the corresponding theme color property
    name from the :class:`ThemeManager` (such as 'primary_color', 'surface_color').
    
    When the theme changes, the behavior automatically updates each bound widget
    property with the current value of its corresponding theme color.
    
    Common Widget Properties
    ------------------------
    - 'background_color' : Widget background color (from MorphBackgroundBehavior)
    - 'border_color' : Widget border color (from MorphBackgroundBehavior)  
    - 'color' : Text color (for Label-based widgets)
    - Any other color property available on the widget
    
    Common Theme Colors
    -------------------
    - 'primary_color', 'on_primary_color' : Primary theme colors
    - 'secondary_color', 'on_secondary_color' : Secondary theme colors
    - 'surface_color', 'on_surface_color' : Surface background colors
    - 'error_color', 'on_error_color' : Error state colors
    - 'outline_color', 'outline_variant_color' : Border and outline colors
    
    Examples
    --------
    Basic color binding:
    
    ```python
    widget.theme_color_bindings = {
        'background_color': 'primary_color',
        'color': 'on_primary_color'
    }
    ```
    
    Surface styling:
    
    ```python
    widget.theme_color_bindings = {
        'background_color': 'surface_container_color',
        'border_color': 'outline_variant_color',
        'color': 'on_surface_color'
    }
    ```
    
    Error state styling:
    
    ```python
    widget.theme_color_bindings = {
        'background_color': 'error_container_color',
        'color': 'on_error_container_color',
        'border_color': 'error_color'
    }
    ```
    
    :attr:`theme_color_bindings` is a :class:`~kivy.properties.DictProperty` 
    and defaults to {}.
    """

    _theme_manager: ThemeManager = MorphApp._theme_manager
    """Reference to the global ThemeManager instance."""

    _theme_bound: bool = False
    """Track if theme manager events are bound."""

    theme_style_mappings: Dict[str, Dict[str, str]] = THEME.STYLES
    """Predefined theme style mappings from constants.
    
    This class attribute contains the default Material Design style
    configurations. Subclasses can override this to provide custom
    or additional style mappings.
    """

    @property
    def theme_manager(self) -> ThemeManager:
        """Access the theme manager for theming and style management (read-only).

        The :attr:`theme_manager` attribute provides access to the
        :class:`ThemeManager` instance, which handles theming and style
        management. This instance is automatically initialized as a
        class attribute and shared across all instances of this behavior.
        """
        return self._theme_manager
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.register_event_type('on_theme_changed')
        self._bind_to_theme_manager()
    
    def _bind_to_theme_manager(self) -> None:
        """Bind to the theme manager for automatic updates. And apply
        initial colors if auto_theme is enabled."""
        if self._theme_bound:
            return
        
        assert self._theme_manager, (
            'ThemeManager instance is required for MorphThemeBehavior')
        
        self._theme_manager.bind(
            on_theme_changed=self._on_theme_manager_changed,
            on_colors_updated=self._on_colors_updated)
        self._theme_bound = True
        if self.auto_theme:
            self._update_colors()

    def _unbind_from_theme_manager(self) -> None:
        """Unbind from the theme manager."""
        if not self._theme_bound:
            return
        
        self._theme_manager.unbind(on_theme_changed=self._on_theme_manager_changed)
        self._theme_manager.unbind(on_colors_updated=self._on_colors_updated)
        self._theme_bound = False

    def bind_theme_colors(self, color_mappings: Dict[str, str]) -> None:
        """Bind widget color properties to theme colors.
        
        This is a convenience method to set theme_color_bindings and 
        immediately apply the color updates.
        
        Parameters
        ----------
        color_mappings : Dict[str, str]
            Dictionary mapping widget property names to theme color names.
            Example: {'background_color': 'primary_color'}
        """
        self.theme_color_bindings.update(color_mappings)
        if self.auto_theme:
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
        if hasattr(self._theme_manager, theme_color):
            color_value = getattr(self._theme_manager, theme_color)
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

    def _on_theme_manager_changed(self, *args) -> None:
        """Called when theme manager signals a theme change."""
        if self.auto_theme:
            self._update_colors()
            self.dispatch('on_theme_changed')

    def _on_colors_updated(self, *args) -> None:
        """Called when theme manager colors are updated."""
        if self.auto_theme:
            self._update_colors()

    def on_auto_theme(self, instance: Any, value: bool) -> None:
        """Fired when :attr:`auto_theme` property changes."""
        if value:
            self._bind_to_theme_manager()
            self._update_colors()
        else:
            self._unbind_from_theme_manager()

    def on_theme_color_bindings(
            self, instance: Any, bindings: Dict[str, str]) -> None:
        """Fired when :attr:`theme_color_bindings` property changes."""
        if self.auto_theme:
            self._update_colors()

    def set_theme_style(self, style_name: str) -> None:
        """Apply a predefined theme style configuration to this widget.
        
        This method provides convenient access to common Material Design color
        combinations by applying predefined :attr:`theme_color_bindings` based
        on Material Design component roles and states.
        
        Each style configures appropriate color bindings for background,
        text, and border colors according to Material Design guidelines.
        
        Parameters
        ----------
        style_name : str
            The name of the predefined style to apply. Available options:
            
            - **'primary'**: High-emphasis style for primary actions
              - Uses primary_color for background and borders
              - Uses on_primary_color for text/content
              - Ideal for: Main action buttons, important controls
              
            - **'secondary'**: Medium-emphasis style for secondary actions  
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
              - Ideal for: Error messages, warning dialogs, destructive actions
              
            - **'outline'**: Low-emphasis outlined style
              - Uses surface_color for background
              - Uses outline_color for borders (creates outlined appearance)
              - Uses on_surface_color for text/content
              - Ideal for: Outlined buttons, optional actions
        
        Raises
        ------
        None
            If an invalid style_name is provided, the method silently ignores
            the request without raising an error.
            
        Examples
        --------
        Apply primary style to a button:
        
        ```python
        class PrimaryButton(MorphThemeBehavior, MorphBackgroundBehavior, Label):
            def __init__(self, **kwargs):
                super().__init__(**kwargs)
                self.set_theme_style('primary')
        ```
        
        Create different button variants:
        
        ```python
        # High-emphasis action
        save_button.set_theme_style('primary')
        
        # Medium-emphasis action  
        cancel_button.set_theme_style('secondary')
        
        # Low-emphasis action
        help_button.set_theme_style('outline')
        
        # Error/destructive action
        delete_button.set_theme_style('error')
        ```
        
        Surface container styling:
        
        ```python
        # Content card or panel
        card.set_theme_style('surface')
        ```
        
        See Also
        --------
        bind_theme_colors : For custom color binding configurations
        theme_color_bindings : The underlying property that stores color mappings
        theme_style_mappings : Class attribute containing the style definitions
        """
        if style_name in self.theme_style_mappings:
            self.bind_theme_colors(self.theme_style_mappings[style_name])

    def add_custom_style(self, style_name: str, color_mappings: Dict[str, str]) -> None:
        """Add a custom theme style to the available styles.
        
        This method allows you to define new theme styles that can be used
        with :meth:`set_theme_style`. Custom styles are added to the instance's
        theme_style_mappings and can be used immediately.
        
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
            'color': 'on_error_container_color',
            'border_color': 'outline_color'
        })
        
        # Now use the custom style
        widget.set_theme_style('warning')
        ```
        
        Add a subtle style:
        
        ```python
        widget.add_custom_style('subtle', {
            'background_color': 'surface_variant_color',
            'color': 'on_surface_variant_color',
            'border_color': 'outline_variant_color'
        })
        ```
        """
        # Create a copy of the class mappings if this is the first custom style
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
        
        This method is automatically called after the widget's bound theme
        colors have been updated in response to a theme change. It provides
        a hook for subclasses to implement custom logic that should occur
        when themes change, such as updating non-color properties or
        triggering animations.
        
        The event is only fired when :attr:`auto_theme` is True and a theme
        change occurs in the connected :class:`ThemeManager`.
        
        Parameters
        ----------
        *args
            Variable arguments passed from the event dispatcher.
            Typically not used but provided for compatibility.
            
        Notes
        -----
        This is an event method that can be overridden in subclasses.
        When overriding, you can either:
        
        1. Override the method directly in your class
        2. Bind to the 'on_theme_changed' event
        
        The automatic color updates happen before this method is called,
        so all bound theme colors will already be up to date when this
        method executes.
        
        Examples
        --------
        Override in a subclass:
        
        ```python
        class CustomThemedWidget(MorphThemeBehavior, Widget):
            def on_theme_changed(self):
                # Custom theme change logic
                if self.theme_manager.theme_mode == 'Dark':
                    self.opacity = 0.9
                else:
                    self.opacity = 1.0
                    
                # Trigger a smooth transition animation
                self.animate_theme_transition()
        ```
        
        Bind to the event:
        
        ```python
        def handle_theme_change(widget):
            print(f"Theme changed on {widget}")
            widget.update_custom_styling()
            
        widget.bind(on_theme_changed=handle_theme_change)
        ```
        
        Access theme information:
        
        ```python
        class ResponsiveWidget(MorphThemeBehavior, Widget):
            def on_theme_changed(self):
                current_mode = self.theme_manager.theme_mode
                current_seed = self.theme_manager.seed_color
                
                print(f"Theme changed to {current_mode} mode with {current_seed} seed")
                
                # Apply mode-specific styling
                if current_mode == 'Dark':
                    self.apply_dark_mode_extras()
                else:
                    self.apply_light_mode_extras()
        ```
        """
        pass
