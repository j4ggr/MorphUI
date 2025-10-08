from kivy.uix.widget import Widget

from .behaviors import MorphThemeBehavior
from .behaviors import MorphSurfaceLayerBehavior
from .behaviors import MorphAutoSizingBehavior
from .behaviors import MorphIdentificationBehavior


__all__ = [
    'MorphWidget',]


class MorphWidget(
        MorphIdentificationBehavior,
        MorphThemeBehavior,
        MorphSurfaceLayerBehavior,
        MorphAutoSizingBehavior,
        Widget):
    """Base widget class for MorphUI components.
    
    MorphWidget extends Kivy's Widget class with automatic sizing 
    capabilities and surface styling through behavior mixins.

    This class combines the following behaviors:
    - `MorphIdentificationBehavior`: Enables identity-based widget 
      identification. For more information see
      :class:`~morphui.uix.behaviors.MorphIdentificationBehavior`.
    - `MorphThemeBehavior`: Integrates theming capabilities, allowing the
      widget to adapt its colors based on the current theme.
      for more information see
      :class:`~morphui.uix.behaviors.MorphThemeBehavior`.
    - `MorphSurfaceLayerBehavior`: Provides surface styling options for
      the widget.
      for more information see
      :class:`~morphui.uix.behaviors.MorphSurfaceLayerBehavior`.
    - `MorphAutoSizingBehavior`: Enables automatic sizing of the widget
      based on its content.
      for more information see
      :class:`~morphui.uix.behaviors.MorphAutoSizingBehavior`.

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
                    ),
                MorphWidget(),
                orientation='vertical',
                padding=10,
                spacing=10)
            return root

    MyApp().run()
    ```
    """