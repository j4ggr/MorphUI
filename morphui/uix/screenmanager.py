from kivy.uix.screenmanager import Screen

from .behaviors import MorphColorThemeBehavior
from .behaviors import MorphBackgroundBehavior
from .behaviors import MorphDeclarativeBehavior


__all__ = [
    'MorphScreen',]


class MorphScreen(
        MorphDeclarativeBehavior,
        MorphColorThemeBehavior,
        MorphBackgroundBehavior,
        Screen):
    """A Screen that supports declarative child widgets via
    :class:`~morphui.uix.behaviors.MorphDeclarativeBehavior`.

    This class combines the functionality of Kivy's Screen with
    several MorphUI behaviors to enhance its capabilities:
    - `MorphDeclarativeBehavior`: Enables declarative property binding.
    - `MorphColorThemeBehavior`: Integrates color theming capabilities.
    - `MorphBackgroundBehavior`: Provides background styling options.

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