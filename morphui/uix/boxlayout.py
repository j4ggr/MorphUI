from kivy.uix.boxlayout import BoxLayout

from morphui.uix.behaviors import MorphColorThemeBehavior
from morphui.uix.behaviors import MorphSurfaceLayerBehavior
from morphui.uix.behaviors import MorphAutoSizingBehavior
from morphui.uix.behaviors import MorphDeclarativeBehavior

from morphui.utils import clean_config

__all__ = [
    'MorphBoxLayout',]


class MorphBoxLayout(
        MorphDeclarativeBehavior,
        MorphColorThemeBehavior,
        MorphSurfaceLayerBehavior,
        MorphAutoSizingBehavior,
        BoxLayout):
    """A BoxLayout that supports declarative child widgets via
    :class:`~morphui.uix.behaviors.MorphDeclarativeBehavior`.
    
    This class combines the functionality of Kivy's BoxLayout with
    several MorphUI behaviors to enhance its capabilities:
    - `MorphDeclarativeBehavior`: Enables declarative property binding.
    - `MorphColorThemeBehavior`: Integrates color theming capabilities.
    - `MorphSurfaceLayerBehavior`: Provides surface styling options.
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
                    identity="label1",
                    text="Label 1",
                    theme_color_bindings={
                        'surface_color': 'surface_container_color',
                        'content_color': 'content_surface_color',
                        'border_color': 'outline_color',},
                    radius=[5, 25, 5, 25],),
                MorphLabel(
                    identity="label2",
                    text="Label 2",
                    theme_color_bindings={
                        'surface_color': 'surface_container_low_color',
                        'content_color': 'content_surface_color',
                        'border_color': 'outline_variant_color',},
                    radius=[25, 5, 25, 5],),
                theme_style='surface',
                orientation='vertical',
                padding=50,
                spacing=15,)
            return self.root
            
    MyApp().run()
    """
    
    default_config = dict(
        orientation='horizontal',
        theme_color_bindings=dict(
            surface_color='transparent_color',))
    """Initialize the MorphBoxLayout with the provided configuration."""
    
    def __init__(self, *args, **kwargs) -> None:
        config = clean_config(self.default_config, kwargs)
        super().__init__(*args, **config)
