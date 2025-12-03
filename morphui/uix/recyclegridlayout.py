from kivy.uix.recyclegridlayout import RecycleGridLayout

from morphui.uix.behaviors import MorphAutoSizingBehavior
from morphui.uix.behaviors import MorphColorThemeBehavior
from morphui.uix.behaviors import MorphSurfaceLayerBehavior


__all__ = [
    'MorphRecycleGridLayout',]


class MorphRecycleGridLayout(
        MorphAutoSizingBehavior,
        MorphColorThemeBehavior,
        MorphSurfaceLayerBehavior,
        RecycleGridLayout):
    """A RecycleGridLayout that supports declarative child widgets via
    :class:`~morphui.uix.behaviors.MorphDeclarativeBehavior`.

    This class combines the functionality of Kivy's RecycleGridLayout with
    several MorphUI behaviors to enhance its capabilities:
    - `MorphDeclarativeBehavior`: Enables declarative property binding.
    - `MorphColorThemeBehavior`: Integrates color theming capabilities.
    - `MorphSurfaceLayerBehavior`: Provides surface styling options.

    Examples
    --------
    ```python
    from morphui.app import MorphApp
    from morphui.uix.label import MorphLabel
    from morphui.uix.recycleview import MorphRecycleView
    from morphui.uix.recyclegridlayout import MorphRecycleGridLayout

    class MyApp(MorphApp):
        def build(self) -> MorphRecycleView:
            self.theme_manager.seed_color = 'Purple'
            return MorphRecycleView(
                viewclass='MorphLabel',
                data=[
                    {'text': f'Label {i}', 'theme_style': 'primary'} for i in range(20)],
                layout=MorphRecycleGridLayout(
                    cols=2,
                    spacing=dp(10),
                    padding=dp(10),
                    theme_style='surface',),
                theme_style='surface',)
    MyApp().run()
    ```
    """