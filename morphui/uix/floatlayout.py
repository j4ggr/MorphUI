from kivy.uix.floatlayout import FloatLayout

from .behaviors import MorphColorThemeBehavior
from .behaviors import MorphBackgroundBehavior
from .behaviors import MorphAutoSizingBehavior
from .behaviors import MorphDeclarativeBehavior


__all__ = [
    'MorphFloatLayout',]


class MorphFloatLayout(
        MorphDeclarativeBehavior,
        MorphColorThemeBehavior,
        MorphBackgroundBehavior,
        MorphAutoSizingBehavior,
        FloatLayout):
    """A FloatLayout that supports declarative child widgets via
    :class:`~morphui.uix.behaviors.MorphDeclarativeBehavior`.

    This class combines the functionality of Kivy's FloatLayout with
    several MorphUI behaviors to enhance its capabilities:
    - `MorphDeclarativeBehavior`: Enables declarative property binding.
    - `MorphColorThemeBehavior`: Integrates color theming capabilities.
    - `MorphBackgroundBehavior`: Provides background styling options.
    - `MorphAutoSizingBehavior`: Enables automatic sizing based on content.

    Examples
    --------
    ```python
    from morphui.app import MorphApp
    from morphui.uix.floatlayout import MorphFloatLayout
    from morphui.uix.label import MorphLabel
    class MyApp(MorphApp):
        def build(self):
            return MorphFloatLayout(
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