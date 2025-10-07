from kivy.uix.gridlayout import GridLayout

from .behaviors import MorphColorThemeBehavior
from .behaviors import MorphBackgroundBehavior
from .behaviors import MorphAutoSizingBehavior
from .behaviors import MorphDeclarativeBehavior


__all__ = [
    'MorphGridLayout',]


class MorphGridLayout(
        MorphDeclarativeBehavior,
        MorphColorThemeBehavior,
        MorphBackgroundBehavior,
        MorphAutoSizingBehavior,
        GridLayout):
    """A GridLayout that supports declarative child widgets via
    :class:`~morphui.uix.behaviors.MorphDeclarativeBehavior`.

    This class combines the functionality of Kivy's GridLayout with
    several MorphUI behaviors to enhance its capabilities:
    - `MorphDeclarativeBehavior`: Enables declarative property binding.
    - `MorphColorThemeBehavior`: Integrates color theming capabilities.
    - `MorphBackgroundBehavior`: Provides background styling options.
    - `MorphAutoSizingBehavior`: Enables automatic sizing based on content.

    Examples
    --------
    ```python
    from morphui.app import MorphApp
    from morphui.uix.gridlayout import MorphGridLayout
    from morphui.uix.label import MorphLabel
    class MyApp(MorphApp):
        def build(self):
            return MorphGridLayout(
                MorphLabel(
                    text="Label 1",
                    theme_style='primary'),
                MorphLabel(
                    text="Label 2",
                    theme_style='secondary'),
                theme_style='surface',
                cols=2,
                padding=50,
                spacing=15,)
    MyApp().run()
    ```
    """
    pass
