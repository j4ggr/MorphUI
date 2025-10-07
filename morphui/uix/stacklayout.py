from kivy.uix.stacklayout import StackLayout

from .behaviors import MorphColorThemeBehavior
from .behaviors import MorphBackgroundBehavior
from .behaviors import MorphDeclarativeBehavior


__all__ = [
    'MorphStackLayout',]


class MorphStackLayout(
        MorphDeclarativeBehavior,
        MorphColorThemeBehavior,
        MorphBackgroundBehavior,
        StackLayout):
    """A StackLayout that supports declarative child widgets via
    :class:`~morphui.uix.behaviors.MorphDeclarativeBehavior`.

    This class combines the functionality of Kivy's StackLayout with
    several MorphUI behaviors to enhance its capabilities:
    - `MorphDeclarativeBehavior`: Enables declarative property binding.
    - `MorphColorThemeBehavior`: Integrates color theming capabilities.
    - `MorphBackgroundBehavior`: Provides background styling options.

    Examples
    --------
    ```python
    from morphui.app import MorphApp
    from morphui.uix.stacklayout import MorphStackLayout
    from morphui.uix.label import MorphLabel
    class MyApp(MorphApp):
        def build(self):
            return MorphStackLayout(
                MorphLabel(
                    text="Label 1",
                    theme_style='primary'),
                MorphLabel(
                    text="Label 2",
                    theme_style='secondary'),
                theme_style='surface',
                padding=50,
                spacing=15,)
    MyApp().run()
    ```
    """
    pass