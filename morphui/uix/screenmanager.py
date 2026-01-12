from kivy.uix.screenmanager import Screen
from kivy.uix.screenmanager import ScreenManager

from morphui.utils.helpers import clean_config
from morphui.uix.behaviors import MorphColorThemeBehavior
from morphui.uix.behaviors import MorphSurfaceLayerBehavior
from morphui.uix.behaviors import MorphDeclarativeBehavior


__all__ = [
    'MorphScreen',
    'MorphScreenManager',]


class MorphScreen(
        MorphDeclarativeBehavior,
        MorphColorThemeBehavior,
        MorphSurfaceLayerBehavior,
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
    """
    default_config: dict = dict()
    
    def __init__(self, *widgets, **kwargs) -> None:
        config = clean_config(self.default_config, kwargs)
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
    def __init__(self, *widgets, **kwargs) -> None:
        super().__init__(*widgets, **kwargs)
