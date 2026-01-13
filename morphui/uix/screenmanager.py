
from kivy.properties import AliasProperty
from kivy.uix.screenmanager import Screen
from kivy.uix.screenmanager import ScreenManager

from morphui.utils.helpers import clean_config
from morphui.uix.behaviors import MorphAutoSizingBehavior
from morphui.uix.behaviors import MorphColorThemeBehavior
from morphui.uix.behaviors import MorphDeclarativeBehavior
from morphui.uix.behaviors import MorphSurfaceLayerBehavior


__all__ = [
    'MorphScreen',
    'MorphScreenManager',]


class MorphScreen(
        MorphDeclarativeBehavior,
        MorphColorThemeBehavior,
        MorphSurfaceLayerBehavior,
        MorphAutoSizingBehavior,
        Screen):
    """A Screen that supports declarative child widgets via
    :class:`~morphui.uix.behaviors.MorphDeclarativeBehavior`.

    This class combines the functionality of Kivy's Screen with
    several MorphUI behaviors to enhance its capabilities:
    - `MorphDeclarativeBehavior`: Enables declarative property binding.
    - `MorphColorThemeBehavior`: Integrates color theming capabilities.
    - `MorphSurfaceLayerBehavior`: Provides surface styling options.

    Examples
    --------
    ```python
    from morphui.app import MorphApp
    from morphui.uix.label import MorphLabel
    from morphui.uix.screenmanager import MorphScreen
    from morphui.uix.screenmanager import MorphScreenManager

    class MyApp(MorphApp):
        def build(self) -> MorphScreenManager:
            self.theme_manager.seed_color = 'Purple'
            sm = MorphScreenManager()
            sm.add_widget(MorphScreen(
                MorphLabel(
                    text="Label 1",
                    theme_style='primary'),
                name='screen1',
                theme_style='surface',))
            sm.add_widget(MorphScreen(
                MorphLabel(
                    text="Label 2",
                    theme_style='secondary',
                    auto_size=True,),
                name='screen2',
                theme_style='surface',))
            return sm
    MyApp().run()
    ```

    Notes
    -----
    - The `identity` property of the screen can be set via the `name`
      keyword argument during instantiation for convenience and vice
      versa.
    - The `minimum_height` and `minimum_width` properties provide
      read-only access to the minimum dimensions required by the screen
      based on its child widgets.
    """

    def _get_minimum_height(self) -> float:
        """Calculate the minimum height required by the screen based on
        its child widgets.

        This method iterates through all child widgets of the screen
        to determine the vertical span they occupy, returning the
        minimum height needed to accommodate them.
        """
        if not self.children:
            return 0.0
        
        y_min = float('inf')
        y_max = float('-inf')
        for child in self.children:
            y_min = min(y_min, child.y)
            y_max = max(y_max, child.y + child.height)
        return y_max - y_min

    minimum_height: float = AliasProperty(
        _get_minimum_height,
        None,
        bind=['children'],
        cache=True,)
    """The minimum height required by the screen based on its child
    widgets (read-only).

    This property is automatically updated whenever the screen's
    children change.

    :attr:`minimum_height` is an 
    :class:`~kivy.properties.AliasProperty` that is read-only and bound
    to the screen's children.
    """

    def _get_minimum_width(self) -> float:
        """Calculate the minimum width required by the screen based on
        its child widgets.

        This method iterates through all child widgets of the screen
        to determine the horizontal span they occupy, returning the
        minimum width needed to accommodate them.
        """
        if not self.children:
            return 0.0
        
        x_min = float('inf')
        x_max = float('-inf')
        for child in self.children:
            x_min = min(x_min, child.x)
            x_max = max(x_max, child.x + child.width)
        return x_max - x_min    
    
    minimum_width: float = AliasProperty(
        _get_minimum_width,
        None,
        bind=['children'],
        cache=True,)
    """The minimum width required by the screen based on its child
    widgets (read-only).

    This property is automatically updated whenever the screen's
    children change.

    :attr:`minimum_width` is an
    :class:`~kivy.properties.AliasProperty` that is read-only and bound
    to the screen's children.
    """

    default_config: dict = dict()
    
    def __init__(self, *widgets, **kwargs) -> None:
        config = clean_config(self.default_config, kwargs)
        if 'name' in config and 'identity' not in config:
            config['identity'] = config['name']
        elif 'identity' in config and 'name' not in config:
            config['name'] = config['identity']
        super().__init__(*widgets, **config)
    

class MorphScreenManager(
        MorphDeclarativeBehavior,
        ScreenManager):
    """A ScreenManager that supports declarative child widgets via
    :class:`~morphui.uix.behaviors.MorphDeclarativeBehavior`.

    This class extends Kivy's ScreenManager by incorporating the
    MorphDeclarativeBehavior, allowing for declarative property binding
    for its child screens.
    Examples
    --------
    ```python
    from morphui.app import MorphApp
    from morphui.uix.button import MorphButton
    from morphui.uix.boxlayout import MorphBoxLayout
    from morphui.uix.screenmanager import MorphScreen
    from morphui.uix.screenmanager import MorphScreenManager

    class MyApp(MorphApp):
        def build(self) -> MorphBoxLayout:
            self.theme_manager.seed_color = 'Purple'

            box = MorphBoxLayout(
                MorphScreenManager(
                    MorphScreen(
                        MorphButton(
                            text="Go to Screen 2",
                            on_release=lambda x: box.screen_manager.current = 'screen2',),
                        name='screen1',),
                    MorphScreen(
                        MorphButton(
                            text="Go to Screen 1",
                            on_release=lambda x: box.screen_manager.current = 'screen1',),
                        name='screen2',),
                    identity='screen_manager',),
                identity='main_layout',
                orientation='vertical',)
            return box
    if __name__ == '__main__':
        MyApp().run()
    ```
    """
    def _get_minimum_width(self) -> float:
        """Calculate the minimum width required by the screen manager
        based on its current screen.

        This method returns the minimum width needed to accommodate
        the currently active screen.
        """
        current_screen = self.current_screen
        if current_screen:
            return current_screen.minimum_width
        return 0.0
    
    minimum_width: float = AliasProperty(
        _get_minimum_width,
        None,
        bind=['current_screen'],
        cache=True,)
    """The minimum width required by the screen manager based on its
    current screen (read-only).

    This property is automatically updated whenever the current
    screen changes. The minimum width is derived from the
    `minimum_width` property of the active screen.

    :attr:`minimum_width` is an
    :class:`~kivy.properties.AliasProperty` that is read-only and bound
    to the current screen's minimum width.
    """

    def _get_minimum_height(self) -> float:
        """Calculate the minimum height required by the screen manager
        based on its current screen.

        This method returns the minimum height needed to accommodate
        the currently active screen.
        """
        current_screen = self.current_screen
        if current_screen:
            return current_screen.minimum_height
        return 0.0

    minimum_height: float = AliasProperty(
        _get_minimum_height,
        None,
        bind=['current_screen'],
        cache=True,)
    """The minimum height required by the screen manager based on its
    current screen (read-only).

    This property is automatically updated whenever the current
    screen changes. The minimum height is derived from the
    `minimum_height` property of the active screen.

    :attr:`minimum_height` is an
    :class:`~kivy.properties.AliasProperty` that is read-only and bound
    to the current screen's minimum height.
    """

    default_config: dict = dict()
    
    def __init__(self, *widgets, **kwargs) -> None:
        config = clean_config(self.default_config, kwargs)
        super().__init__(*widgets, **config)
