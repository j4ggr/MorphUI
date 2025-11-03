from typing import Any

from morphui.app import MorphApp
from morphui.theme.manager import ThemeManager
from morphui.theme.typography import Typography

__all__ = ['MorphAppReferenceBehavior']


class MorphAppReferenceBehavior:
    """Behavior providing convenient access to app instances and MVC 
    components.

    This behavior adds properties to widgets that provide direct access
    to:
    - The main application instance
    - Model-View-Controller (MVC) components (when available)
    - Theme manager for consistent theming

    The controller access is particularly useful for event handling, 
    allowing widgets to easily bind to controller methods for reactive
    programming patterns. All MVC components are optional and will
    return None if not configured in the app.

    Examples
    --------
    Basic usage with controller event binding:

    ```python
    from morphui.uix.label import MorphLabel
    from morphui.uix.behaviors import MorphAppReferenceBehavior

    class MyWidget(MorphAppReferenceBehavior, MorphLabel):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            
            # Bind to controller method if available
            if self.controller and hasattr(self.controller, 'on_data_changed'):
                self.bind(text=self.controller.on_data_changed)
            
            # Access theme manager
            if self.theme_manager.theme_mode == 'Dark':
                self.color = [1, 1, 1, 1]  # White text for dark theme
    ```

    Model-View-Controller integration:

    ```python
    class DataDisplayWidget(MorphAppReferenceBehavior, MorphLabel):
        def on_kv_post(self, base_widget):
            super().on_kv_post(base_widget)
            
            # React to model changes
            if self.model and hasattr(self.model, 'data'):
                self.text = str(self.model.data)
                self.model.bind(data=self.update_display)
        
        def update_display(self, instance, value):
            self.text = str(value)
            
            # Notify controller of display update (optional)
            if self.controller and hasattr(self.controller, 'on_display_updated'):
                self.controller.on_display_updated(self, value)
    ```

    Notes
    -----
    - All properties are read-only and cached for performance
    - MVC components (model, controller, view) are optional - they 
      return None if not configured in the app
    - Controller access enables easy event binding for reactive patterns
    - Theme manager is always available through the MorphApp instance
    - The app reference is automatically obtained and cached on first 
      access
    """

    _app: Any = None
    """Reference to the running app instance (cached)."""

    _model: Any = None
    """Reference to the app's model instance (cached)."""

    _controller: Any = None
    """Reference to the app's controller instance (cached)."""

    _view: Any = None
    """Reference to the app's view instance (cached)."""

    @property
    def app(self) -> Any:
        """Get the reference to the running MorphApp instance
        (read-only).

        This property provides access to the main application instance,
        automatically retrieving and caching it on first access. The app
        instance serves as the central hub for accessing MVC components
        and application-wide services.

        Examples
        --------
        ```python
        # Access app properties
        if self.app:
            print(f"App title: {self.app.title}")
            
        # Check if MVC components are configured
        has_mvc = all([self.app.model, self.app.controller, self.app.view])
        ```
        """
        if self._app is None:
            self._app = MorphApp.get_running_app()
        return self._app
    
    @property
    def theme_manager(self) -> ThemeManager:
        """Get the current theme manager instance (read-only).
        
        This property provides direct access to the application's theme
        manager, which handles theming, color schemes, and appearance
        settings. The theme manager is always available through the
        MorphApp instance.

        Examples
        --------
        ```python
        # Check current theme mode
        if self.theme_manager.theme_mode == 'Dark':
            self.apply_dark_theme()
        
        # Bind to theme changes
        self.theme_manager.bind(theme_mode=self.on_theme_changed)
        
        # Access theme colors
        primary_color = self.theme_manager.primary_color
        ```
        """
        return MorphApp._theme_manager
    
    @property
    def typography(self) -> Typography:
        """Get the current typography manager instance (read-only).

        This property provides direct access to the application's
        typography manager, which handles font styles, sizes, and text
        layout settings. The typography manager is always available
        through the MorphApp instance.
        """
        return MorphApp._typography

    @property
    def model(self) -> Any:
        """Get the application's model instance (read-only).

        This property provides access to the application's model
        component in the MVC pattern. The model typically contains
        application data, business logic, and state management.

        Examples
        --------
        ```python
        # Safe access to model data
        if self.model and hasattr(self.model, 'user_data'):
            self.display_user_info(self.model.user_data)
        
        # Bind to model changes
        if self.model:
            self.model.bind(data_updated=self.on_data_changed)
        ```
        """
        if self._model is None and self.app:
            self._model = getattr(self.app, 'model', None)
        return self._model

    @property
    def controller(self) -> Any:
        """Get the application's controller instance (read-only).

        This property provides access to the application's controller
        component in the MVC pattern. The controller handles user input,
        coordinates between model and view, and contains business logic
        for user interactions.

        **Controller access is particularly powerful for event handling**,
        as it allows widgets to easily bind their events to controller
        methods, enabling clean separation of concerns and reactive
        programming patterns.

        Examples
        --------
        Event binding to controller methods:

        ```python
        # Bind widget events to controller methods
        if self.controller:
            # Button click handling
            if hasattr(self.controller, 'on_save_clicked'):
                self.bind(on_press=self.controller.on_save_clicked)
            
            # Text input validation
            if hasattr(self.controller, 'validate_input'):
                self.bind(text=self.controller.validate_input)
            
            # State change notifications
            if hasattr(self.controller, 'on_selection_changed'):
                self.bind(active=self.controller.on_selection_changed)
        ```

        Reactive programming patterns:

        ```python
        def setup_reactive_bindings(self):
            '''Set up reactive bindings to controller methods.'''
            if not self.controller:
                return  # Gracefully handle missing controller
            
            # Bind multiple events to controller
            event_bindings = {
                'on_focus': 'handle_focus_change',
                'on_text_validate': 'handle_text_input',
                'on_state_change': 'handle_state_update'
            }
            
            for event, method_name in event_bindings.items():
                if hasattr(self.controller, method_name):
                    controller_method = getattr(self.controller, method_name)
                    self.bind(**{event: controller_method})
        ```

        Notes
        -----
        - Controller access enables clean event handling without tight
          coupling
        - Always check if controller exists and has the required methods
        - Controller methods can be bound to any widget event or
          property change
        - This pattern promotes testable, maintainable code architecture
        """
        if self._controller is None and self.app:
            self._controller = getattr(self.app, 'controller', None)
        return self._controller

    @property
    def view(self) -> Any:
        """Get the application's view instance (read-only).

        This property provides access to the application's view
        component in the MVC pattern. The view typically represents the
        main UI container or root widget that manages the overall
        application interface.

        Examples
        --------
        ```python
        # Access main view for navigation or layout changes
        if self.view and hasattr(self.view, 'switch_screen'):
            self.view.switch_screen('settings')
        
        # Get view state for conditional behavior
        if self.view and hasattr(self.view, 'current_mode'):
            if self.view.current_mode == 'editing':
                self.enable_edit_controls()
        ```
        """
        if self._view is None and self.app:
            self._view = getattr(self.app, 'view', None)
        return self._view
