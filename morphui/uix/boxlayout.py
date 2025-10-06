from kivy.uix.boxlayout import BoxLayout

from .behaviors import MorphThemeBehavior
from .behaviors import MorphBackgroundBehavior
from .behaviors import MorphAutoSizingBehavior
from .behaviors import MorphDeclarativeBehavior


__all__ = [
    'MorphBoxLayout',]


class MorphBoxLayout(
        MorphDeclarativeBehavior,
        MorphThemeBehavior,
        MorphBackgroundBehavior,
        MorphAutoSizingBehavior,
        BoxLayout):
    """A BoxLayout that supports declarative child widgets via
    :class:`~morphui.uix.behaviors.MorphDeclarativeBehavior`.
    
    This class combines the functionality of Kivy's BoxLayout with
    several MorphUI behaviors to enhance its capabilities:
    - `MorphDeclarativeBehavior`: Enables declarative property binding.
    - `MorphThemeBehavior`: Integrates theming capabilities.
    - `MorphBackgroundBehavior`: Provides background styling options.
    - `MorphAutoSizingBehavior`: Enables automatic sizing based on content.

    Examples
    --------
    ```python
    from morphui.app import MorphApp
    from morphui.uix.boxlayout import MorphBoxLayout
    from morphui.uix.label import MorphLabel

    class MyApp(MorphApp):
        def build(self):
            return MorphBoxLayout(
                MorphLabel(
                    text="Label 1",
                    theme_style='primary'),
                MorphLabel(
                    text="Label 2",
                    theme_style='secondary'),
                theme_style='surface',
                orientation='vertical',
                padding=10,
                spacing=10,)
    MyApp().run()
    """
    pass