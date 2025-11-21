from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.recycleview.layout import LayoutSelectionBehavior

from morphui.uix.behaviors import MorphAutoSizingBehavior
from morphui.uix.behaviors import MorphColorThemeBehavior
from morphui.uix.behaviors import MorphSurfaceLayerBehavior


__all__ = [
    'MorphRecycleBoxLayout',
    'MorphSelectableRecycleBoxLayout',]


class MorphRecycleBoxLayout(
        MorphAutoSizingBehavior,
        MorphColorThemeBehavior,
        MorphSurfaceLayerBehavior,
        RecycleBoxLayout):
    """A RecycleBoxLayout using MorphUI theming and surface layer 
    behaviors.

    This class combines the functionality of Kivy's RecycleBoxLayout 
    with several MorphUI behaviors to enhance its capabilities:
    - `MorphColorThemeBehavior`: Integrates color theming capabilities.
    - `MorphSurfaceLayerBehavior`: Provides surface styling options.

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


class MorphSelectableRecycleBoxLayout(
        LayoutSelectionBehavior,
        MorphRecycleBoxLayout):
    """A selectable RecycleBoxLayout using MorphUI theming and surface
    layer behaviors.

    This class extends the MorphRecycleBoxLayout by adding selection
    capabilities through the LayoutSelectionBehavior. It allows for
    selecting items within the RecycleBoxLayout while maintaining the
    theming and surface layer features provided by MorphUI.
    """