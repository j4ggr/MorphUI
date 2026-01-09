import warnings

from typing import Any
from typing import Dict
from typing import Literal

from kivy.event import EventDispatcher
from kivy.properties import DictProperty
from kivy.properties import StringProperty
from kivy.properties import OptionProperty
from kivy.properties import BooleanProperty
from kivy.properties import ListProperty

from .appreference import MorphAppReferenceBehavior

from morphui.constants import THEME


__all__ = [
    'MorphColorThemeBehavior',
    'MorphTypographyBehavior', 
    'MorphThemeBehavior',
    'MorphDelegatedThemeBehavior',]


class BaseThemeBehavior(EventDispatcher, MorphAppReferenceBehavior):
    """Base class for theme-related behaviors.
    
    This class serves as a common ancestor for theme-related behaviors,
    providing shared functionality and properties. It is not intended
    to be used directly, but rather to be extended by specific theme
    behaviors such as :class:`MorphColorThemeBehavior` and 
    :class:`MorphTypographyBehavior`.
    
    Key Features
    ------------
    - Inherits from :class:`MorphAppReferenceBehavior` to provide access
      to the application instance and theme manager.
    - Serves as a foundation for more specialized theming behaviors.
    
    See Also
    --------
    - MorphColorThemeBehavior : Provides automatic color theme 
      integration for widgets.
    - MorphTypographyBehavior : Provides typography and text styling 
      capabilities.
    - MorphAppReferenceBehavior : Provides access to app instances and 
      MVC components.
    """
    pass


class MorphColorThemeBehavior(BaseThemeBehavior):
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
                'normal_surface_color': 'primary_color',
                'normal_border_color': 'outline_color',
                'normal_content_color': 'content_primary_color'  # text color
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
    overrides any existing :attr:`theme_color_bindings` with the
    corresponding color mappings for that style at
    :attr:`effective_theme_color_bindings`.

    This provides a quick way to style widgets according to established
    Material Design roles such as 'primary', 'secondary', 'tertiary',
    'surface', 'error', and 'outline'. The property uses Kivy's 
    StringProperty binding system, so changes are automatically 
    detected and applied.

    :attr:`theme_style` is a :class:`~kivy.properties.StringProperty` 
    and defaults to '' (no style).
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
        'normal_surface_color': 'primary_color',
        'normal_content_color': 'content_primary_color',
        'normal_border_color': 'outline_color'
    }
    ```
    
    Error state styling:
    
    ```python
    widget.theme_color_bindings = {
        'normal_surface_color': 'error_color',
        'normal_content_color': 'content_error_color',
        'normal_border_color': 'error_color'
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

    _theme_style_color_bindings: Dict[str, str] = DictProperty({})
    """Dictionary mapping theme style names to color bindings.

    This dictionary is populated with the color bindings for each
    theme style defined in :attr:`theme_style_mappings`. It allows
    for quick lookups of color bindings based on the current theme
    style.

    The finally applied color bindings are a merge of the
    :attr:`theme_color_bindings` and the bindings from the current
    theme style.

    :attr:`_theme_style_color_bindings` is a
    :class:`~kivy.properties.DictProperty` and defaults to {}.
    """

    _theme_bound: bool = False
    """Track if theme manager events are bound."""
    
    def __init__(self, **kwargs) -> None:
        self.register_event_type('on_colors_updated')
        super().__init__(**kwargs)

        self.bind(
            theme_style=self._update_theme_style,
            auto_theme=self._update_colors,
            theme_color_bindings=self._update_colors,
            _theme_style_color_bindings=self._update_colors)

        self.theme_manager.bind(
            on_colors_updated=self._update_colors)
        
        self.refresh_theme_colors()

    @property
    def effective_color_bindings(self) -> Dict[str, str]:
        """Get the effective color bindings after merging style and 
        custom bindings.

        This property returns the final dictionary of color bindings
        that will be applied to the widget. It merges the current
        :attr:`theme_color_bindings` with any bindings defined by the
        current :attr:`theme_style`, giving precedence to explicit
        :attr:`theme_color_bindings`. When both define the same widget
        property, the values from :attr:`theme_style` have priority.
        """
        merged = {
            **self.theme_color_bindings,
            **self._theme_style_color_bindings}
        return merged

    def apply_theme_color(self, property_name: str, theme_color: str) -> bool:
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
        property_name : str
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
        color_value = getattr(self.theme_manager, theme_color, None)
        if color_value is not None and hasattr(self, property_name):
            setattr(self, property_name, color_value)
            return True
        
        return False

    def _update_colors(self, *args) -> None:
        """Update widget colors based on current theme."""
        color_bindings = self.effective_color_bindings
        if not self.auto_theme or not color_bindings:
            return None

        for property_name, theme_color in color_bindings.items():
            self.apply_theme_color(property_name, theme_color)
        self.dispatch('on_colors_updated')

    def _update_theme_style(self, instance: Any, style_name: str) -> None:
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
        if style_name in self.theme_style_mappings:
            self._theme_style_color_bindings = self.theme_style_mappings[
                style_name].copy()
        elif style_name:
            warnings.warn(
                f"Unknown theme_style '{style_name}', ignoring",
                UserWarning)
            self._theme_style_color_bindings = {}

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
            'normal_surface_color': 'error_container_color',
            'normal_content_color': 'content_error_container_color',
            'normal_border_color': 'outline_color'
        })
        
        # Now use the custom style
        widget.theme_style = 'warning'
        ```
        
        Add a subtle style:
        
        ```python
        widget.add_custom_style('subtle', {
            'normal_surface_color': 'surface_variant_color',
            'normal_content_color': 'content_surface_variant_color',
            'normal_border_color': 'outline_variant_color'
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
            self.theme_style_mappings = (
                self.__class__.theme_style_mappings.copy())
        
        self.theme_style_mappings[style_name] = color_mappings

    def refresh_theme_colors(self) -> None:
        """Manually refresh all theme colors.
        
        This method forces an update of all bound theme colors,
        useful when you want to ensure colors are up to date.
        """
        auto_theme = self.auto_theme
        self.auto_theme = True
        self._update_theme_style(self, self.theme_style)
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


class MorphTypographyBehavior(BaseThemeBehavior):
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
        assert self.typography._registered_fonts, (
            "No fonts registered in Typography system. "
            "Ensure you are using MorphApp and it is initialized before using "
            "MorphTypographyBehavior.")

        self.fbind('typography_role', self._update_typography)
        self.fbind('typography_size', self._update_typography)
        self.fbind('typography_weight', self._update_typography)
        self.typography.bind(
            on_typography_changed=self._update_typography)
        self.refresh_typography()

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
            font_name=getattr(self, 'font_name', None),
            role=self.typography_role,
            size=self.typography_size,
            font_weight=self.typography_weight)

    def apply_typography_style(
            self,
            font_name: str | None,
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
        font_name : str | None
            Optional font name to override the default font family from
            the typography system. If None, uses the default font family
            defined in the typography settings.
        role : str
            Typography role ('Display', 'Headline', 'Title', 'Body', 'Label')
        size : str
            Size variant ('large', 'medium', 'small')
        font_weight : str, optional
            Font weight ('Thin', 'Regular', 'Heavy'), defaults to 'Regular'
        """ 
        style = self.typography.get_text_style(
            font_name=font_name, role=role, size=size, font_weight=font_weight)
        
        # Apply font properties if widget has them
        if hasattr(self, 'font_name') and 'name' in style:
            self.font_name = style['name']

        for key, value in style.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.dispatch('on_typography_updated')
    
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


class MorphThemeBehavior(
        MorphColorThemeBehavior,
        MorphTypographyBehavior):
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


class MorphDelegatedThemeBehavior(EventDispatcher):
    """Behavior that allows a container widget to delegate theme
    properties to its child widgets.
    
    This behavior is designed for container widgets that hold other
    themed widgets. It enables the container to manage and propagate
    theme colors to its children, ensuring consistent theming across
    all contained widgets.

    Examples
    --------
    Using the delegated theme behavior in a container:
    
    ```python
    from morphui.uix.behaviors.theming import MorphDelegatedThemeBehavior
    from morphui.uix.boxlayout import MorphBoxLayout
    class ThemedContainer(
            MorphDelegatedThemeBehavior,
            MorphBoxLayout):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            # Child widgets will inherit theme properties from this container
    ```

    Notes
    -----
    This behavior is intended to be used in conjunction with container
    widgets that hold other themed widgets. It ensures that all child
    widgets receive consistent theming based on the container's theme
    settings. Ensure that the subclassed container widget also 
    implements the necessary behaviors:
    - :class:`MorphColorThemeBehavior` for color theming
    - :class:`MorphContentLayerBehavior` for content color theming
    """

    delegate_content_color: bool = BooleanProperty(True)
    """Whether to delegate content color theming to child widgets.

    When True, the container will manage the content color of its
    children, ensuring consistent text and icon colors. When False,
    children will manage their own content colors independently.

    :attr:`delegate_content_color` is a
    :class:`~kivy.properties.BooleanProperty` and defaults to True.
    """

    delegate_to_children: list = ListProperty([])
    """List of child widgets to which theme delegation should be applied.

    This property allows you to specify which child widgets should
    have their theme properties delegated by the container. If the list
    is empty (default), delegation applies to all children. If the list
    contains specific widget instances, only those widgets will have
    their theme properties managed by the container.

    :attr:`delegate_to_children` is a
    :class:`~kivy.properties.ListProperty` and defaults to [] 
    (all children).
    
    Examples
    --------
    Delegate to all children (default):
    
    ```python
    container.delegate_to_children = []
    ```
    
    Delegate to specific children only:
    
    ```python
    label1 = Label()
    label2 = Label()
    button = Button()
    container.add_widget(label1)
    container.add_widget(label2)
    container.add_widget(button)
    
    # Only delegate to label1 and label2, not button
    container.delegate_to_children = [label1, label2]
    ```
    """

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.bind(
            delegate_to_children=self._update_delegated_children)
        self._update_delegated_children(self, self.delegate_to_children)

    def _update_delegated_children(
            self,
            instance: Any,
            children: list) -> None:
        """Event handler fired when :attr:`delegate_to_children` property
        changes.

        This method is automatically called when the
        :attr:`delegate_to_children` property is modified. It updates
        the theme bindings for all child widgets based on the new list.

        Parameters
        ----------
        instance : Any
            The widget instance that triggered the property change.
        children : list
            The new list of child widgets to which theme delegation
            should be applied.
        """
        for child in children:
            self._delegate_content_color_to_child(child)

    def _delegate_content_color_to_child(self, widget: Any) -> None:
        """Delegate content color theming to a specific child widget.

        This method sets up the necessary bindings on the specified
        child widget to allow it to receive content color updates from
        the container. If :attr:`delegate_content_color` is False, or if
        the widget is not a child of the container, no action is taken.

        Parameters
        ----------
        widget : Any
            The child widget from which to remove content color
            bindings.
        """
        delegate_to_children = self.delegate_to_children or self.children
        if (not self.delegate_content_color
                or widget is None
                or widget not in delegate_to_children):
            return None
        
        widget._get_content_color = self._get_content_color
