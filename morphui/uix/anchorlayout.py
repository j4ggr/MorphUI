from kivy.uix.anchorlayout import AnchorLayout

from .behaviors import MorphColorThemeBehavior
from .behaviors import MorphSurfaceLayerBehavior
from .behaviors import MorphDeclarativeBehavior


__all__ = [
    'MorphAnchorLayout',]


class MorphAnchorLayout(
        MorphDeclarativeBehavior,
        MorphColorThemeBehavior,
        MorphSurfaceLayerBehavior,
        AnchorLayout):
    """An AnchorLayout that supports declarative child widgets via
    :class:`~morphui.uix.behaviors.MorphDeclarativeBehavior`.

    This class combines the functionality of Kivy's AnchorLayout with
    several MorphUI behaviors to enhance its capabilities:
    - `MorphDeclarativeBehavior`: Enables declarative property binding.
    - `MorphColorThemeBehavior`: Integrates color theming capabilities.
    - `MorphSurfaceLayerBehavior`: Provides surface styling options.
    
    Examples
    --------
    ```python
    from morphui.app import MorphApp
    from morphui.uix.label import MorphLabel
    from morphui.uix.anchorlayout import MorphAnchorLayout

    class MyApp(MorphApp):
        def build(self) -> MorphAnchorLayout:
            self.theme_manager.seed_color = 'Purple'
            return MorphAnchorLayout(
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