from kivy.uix.widget import Widget

from .behaviors import MorphThemeBehavior
from .behaviors import MorphCompleteLayerBehavior
from .behaviors import MorphAutoSizingBehavior
from .behaviors import MorphIdentificationBehavior


__all__ = [
    'MorphWidget',]


class MorphWidget(
        MorphIdentificationBehavior,
        MorphThemeBehavior,
        MorphCompleteLayerBehavior,
        MorphAutoSizingBehavior,
        Widget):
    """Base widget class for MorphUI components.
    
    MorphWidget extends Kivy's Widget class with complete layer styling,
    theming, and automatic sizing capabilities through behavior mixins.

    This class combines the following behaviors:
    - `MorphIdentificationBehavior`: Enables identity-based widget 
      identification. For more information see
      :class:`~morphui.uix.behaviors.MorphIdentificationBehavior`.
    - `MorphThemeBehavior`: Integrates theming capabilities, allowing the
      widget to adapt its colors based on the current theme.
      For more information see
      :class:`~morphui.uix.behaviors.MorphThemeBehavior`.
    - `MorphCompleteLayerBehavior`: Provides all layer styling capabilities
      including surface, interaction, content, and overlay layers.
      For more information see
      :class:`~morphui.uix.behaviors.MorphCompleteLayerBehavior`.
    - `MorphAutoSizingBehavior`: Enables automatic sizing of the widget
      based on its content. For more information see
      :class:`~morphui.uix.behaviors.MorphAutoSizingBehavior`.

    Layer Stack (bottom to top):
    1. Surface Layer - Background colors, borders, radius
    2. Interaction Layer - State feedback (hover, press, focus)
    3. Content Layer - Text/icon color management
    4. Overlay Layer - Top-level overlays and effects

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
                    surface_color=[0.2, 0.6, 0.8, 1],
                    radius=[10, 10, 10, 10],
                ),
                MorphWidget(
                    surface_color=[0.8, 0.4, 0.2, 1],
                    radius=[5, 5, 5, 5],
                ),
                orientation='vertical',
                padding=10,
                spacing=10)
            return root

    MyApp().run()
    ```

    Notes
    -----
    - This widget provides complete layer functionality out of the box
    - For simpler use cases, consider using more specific mixins like
      `MorphInteractiveLayerBehavior` or `MorphTextLayerBehavior`
    - All layer properties are available and properly themed
    - Interaction states require additional behavior mixins (e.g., MorphHoverBehavior)
    """