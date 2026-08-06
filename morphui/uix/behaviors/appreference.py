from collections.abc import Callable
from functools import wraps
from typing import Any
from typing import Generic
from typing import TypeVar

from kivy.logger import Logger

from morphui.app import MorphApp
from morphui.theme.manager import ThemeManager
from morphui.theme.typography import Typography

__all__ = [
    'MorphAppReferenceBehavior',
    'require_view',
    'require_model',
    'require_controller',
]

AppT = TypeVar('AppT', bound=MorphApp, default=MorphApp)
"""Type of the running app instance, bound to :class:`MorphApp`."""

ModelT = TypeVar('ModelT', default=Any)
"""Type of the app's model instance."""

ControllerT = TypeVar('ControllerT', default=Any)
"""Type of the app's controller instance."""

ViewT = TypeVar('ViewT', default=Any)
"""Type of the app's view instance."""


def _phrase(func: Callable) -> str:
    """Turn a method name like ``on_input_change`` into an action
    phrase such as ``'handle input change'`` for warning messages."""
    name = func.__name__
    if name.startswith('on_'):
        return f'handle {name[3:]}'.replace('_', ' ')
    return name.replace('_', ' ')


def _warn(self: Any, message: str) -> None:
    """Emit *message* via the host's own ``log_warning`` method if it
    has one, otherwise fall back to Kivy's ``Logger``."""
    log_warning = getattr(self, 'log_warning', None)
    if callable(log_warning):
        log_warning(message)
    else:
        Logger.warning(f'MorphUI: {message}')


def require_view(message: str | None = None) -> Callable[[Callable], Callable]:
    """Decorator factory: skip the method and log a warning instead of
    raising if ``self.view`` is not yet available.

    Avoids a repetitive ``if self.view is None: ...; return`` guard in
    every method of a :class:`MorphAppReferenceBehavior` subclass that
    may run before the view has been attached to the running app. The
    warning is emitted via the host's own ``log_warning`` method if it
    has one, otherwise via Kivy's ``Logger``.

    Parameters
    ----------
    message : str | None
        Action phrase used in the warning, e.g. ``'save settings'``.
        Defaults to the decorated method's name with underscores
        replaced by spaces (``on_`` prefixes become ``'handle ...'``).

    Examples
    --------
    ```python
    class MyController(MorphAppReferenceBehavior):
        @require_view()
        def save_settings(self, *args) -> None:
            self.view.settings['theme_mode'] = 'Dark'

        @require_view('switch primary palette')
        def switch_seed_color(self, palette_name: str) -> None:
            self.view.theme_manager.seed_color = palette_name
    ```
    """
    def decorator(func: Callable) -> Callable:
        action = message or _phrase(func)

        @wraps(func)
        def wrapper(self, *args, **kwargs):
            if self.view is None:
                _warn(self, f'View not yet available, cannot {action}.')
                return None
            return func(self, *args, **kwargs)
        return wrapper
    return decorator


def require_model(message: str | None = None) -> Callable[[Callable], Callable]:
    """Decorator factory: skip the method and log a warning instead of
    raising if ``self.model`` is not yet available.

    See :func:`require_view` for details; this variant guards
    ``self.model`` instead.
    """
    def decorator(func: Callable) -> Callable:
        action = message or _phrase(func)

        @wraps(func)
        def wrapper(self, *args, **kwargs):
            if self.model is None:
                _warn(self, f'Model not yet available, cannot {action}.')
                return None
            return func(self, *args, **kwargs)
        return wrapper
    return decorator


def require_controller(
        message: str | None = None) -> Callable[[Callable], Callable]:
    """Decorator factory: skip the method and log a warning instead of
    raising if ``self.controller`` is not yet available.

    See :func:`require_view` for details; this variant guards
    ``self.controller`` instead.
    """
    def decorator(func: Callable) -> Callable:
        action = message or _phrase(func)

        @wraps(func)
        def wrapper(self, *args, **kwargs):
            if self.controller is None:
                _warn(self, f'Controller not yet available, cannot {action}.')
                return None
            return func(self, *args, **kwargs)
        return wrapper
    return decorator


class MorphAppReferenceBehavior(Generic[AppT, ModelT, ControllerT, ViewT]):
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

    class MyWidget(
        MorphAppReferenceBehavior[MyApp, MyModel, MyController, MyView],
        MorphLabel,
    ):
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
    - Subclasses can specialize the ``App``, ``Model``, ``Controller`` 
      and ``View`` types by parameterizing this generic behavior, 
      e.g. ``MorphAppReferenceBehavior[MyApp, MyModel, MyController, 
      MyView]``, so that ``app``, ``model``, ``controller`` and 
      ``view`` are typed accordingly instead of falling back to 
      ``Any``
    """

    _app: AppT | None = None
    """Reference to the running app instance (cached)."""

    _model: ModelT | None = None
    """Reference to the app's model instance (cached)."""

    _controller: ControllerT | None = None
    """Reference to the app's controller instance (cached)."""

    _view: ViewT | None = None
    """Reference to the app's view instance (cached)."""

    @property
    def app(self) -> AppT:
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
        return self._app  # type: ignore[return-value]
    
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
    def model(self) -> ModelT | None:
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
    def controller(self) -> ControllerT | None:
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
    def view(self) -> ViewT | None:
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
