
from kivy.uix.widget import Widget

from morphui.uix.behaviors import MorphBackgroundBehavior
from morphui.uix.behaviors import MorphAutoSizingBehavior


__all__ = [
    'MorphWidget',]


class MorphWidget(
        MorphAutoSizingBehavior,
        MorphBackgroundBehavior,
        Widget):
    """Base widget class for MorphUI components.
    
    MorphWidget extends Kivy's Widget class with automatic sizing 
    capabilities and background styling through behavior mixins.

    This class combines the following behaviors:
    - `MorphAutoSizingBehavior`: Enables automatic sizing of the widget 
      based on its content.
    - `MorphBackgroundBehavior`: Provides background styling options for
      the widget.

    Examples
    --------

    ```python
    from morphui.app import MorphApp
    from morphui.uix.widget import MorphWidget
    from morphui.uix.boxlayout import MorphBoxLayout

    class MyApp(MorphApp):
        def build(self):
            root = MorphBoxLayout( 
                MorphWidget(
                    size_hint=(None, None),
                    size=(200, 100),
                    background_color=(1, 0, 0, 0.5),  # semi-transparent red
                    border_color=(0, 1, 0, 0.5),
                    radius=[20, 20, 20, 20],  # rounded corners
                    border_width=2,),
                MorphWidget(
                    size_hint=(None, None),
                    size=(200, 100),
                    background_color=(0, 0, 1, 0.5),  # semi-transparent blue
                    border_color=(1, 1, 0, 0.5),
                    radius=[5, 25, 5, 25],  # different corner radii
                    border_width=3,),
                orientation='vertical',
                padding=10,
                spacing=10)
            return root

    MyApp().run()
    ```
    """