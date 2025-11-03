from kivy.uix.relativelayout import RelativeLayout

from morphui.uix.behaviors import MorphColorThemeBehavior
from morphui.uix.behaviors import MorphSurfaceLayerBehavior
from morphui.uix.behaviors import MorphDeclarativeBehavior


__all__ = [
    'MorphRelativeLayout',]


class MorphRelativeLayout(
        MorphDeclarativeBehavior,
        MorphColorThemeBehavior,
        MorphSurfaceLayerBehavior,
        RelativeLayout):
    """A RelativeLayout that supports declarative child widgets via
    :class:`~morphui.uix.behaviors.MorphDeclarativeBehavior`.

    This class combines the functionality of Kivy's RelativeLayout with
    several MorphUI behaviors to enhance its capabilities:
    - `MorphDeclarativeBehavior`: Enables declarative property binding.
    - `MorphColorThemeBehavior`: Integrates color theming capabilities.
    - `MorphSurfaceLayerBehavior`: Provides surface styling options.

    Examples
    --------
    ```python
    from morphui.app import MorphApp
    from morphui.uix.label import MorphLabel
    from morphui.uix.relativelayout import MorphRelativeLayout

    class MyApp(MorphApp):
        def build(self) -> MorphRelativeLayout:
            self.theme_manager.seed_color = 'Purple'
            return MorphRelativeLayout(
                MorphLabel(
                    text="Label 1",
                    theme_style='primary'),
                MorphLabel(
                    text="Label 2",
                    theme_style='secondary',
                    auto_size=True,),
                theme_style='surface',)

    MyApp().run()
    ```
    """