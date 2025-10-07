from kivy.uix.recycleboxlayout import RecycleBoxLayout

from .behaviors import MorphColorThemeBehavior
from .behaviors import MorphBackgroundBehavior
from .behaviors import MorphDeclarativeBehavior


__all__ = [
    'MorphRecycleBoxLayout',]


class MorphRecycleBoxLayout(
        MorphDeclarativeBehavior,
        MorphColorThemeBehavior,
        MorphBackgroundBehavior,
        RecycleBoxLayout):
    """A RecycleBoxLayout that supports declarative child widgets via
    :class:`~morphui.uix.behaviors.MorphDeclarativeBehavior`.

    This class combines the functionality of Kivy's RecycleBoxLayout with
    several MorphUI behaviors to enhance its capabilities:
    - `MorphDeclarativeBehavior`: Enables declarative property binding.
    - `MorphColorThemeBehavior`: Integrates color theming capabilities.
    - `MorphBackgroundBehavior`: Provides background styling options.

    Examples
    --------
    ```python
    from morphui.app import MorphApp
    from morphui.uix.label import MorphLabel
    from morphui.uix.recycleview import MorphRecycleView
    from morphui.uix.recycleboxlayout import MorphRecycleBoxLayout

    class MyApp(MorphApp):
        def build(self) -> MorphRecycleView:
            self.theme_manager.seed_color = 'Purple'
            return MorphRecycleView(
                viewclass='MorphLabel',
                data=[
                    {'text': f'Label {i}', 'theme_style': 'primary'} for i in range(20)],
                layout=MorphRecycleBoxLayout(
                    auto_height=True,
                    orientation='vertical',
                    theme_style='surface',),
                theme_style='surface',)
    MyApp().run()
    ```
    """