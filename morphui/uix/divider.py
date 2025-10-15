from typing import Any
from typing import Dict

from kivy.metrics import dp
from kivy.uix.widget import Widget
from kivy.properties import StringProperty
from kivy.properties import NumericProperty

from ..utils import clean_default_config

from .behaviors import MorphColorThemeBehavior
from .behaviors import MorphSurfaceLayerBehavior


__all__ = [
    'MorphDivider',]


class MorphDivider(
        MorphColorThemeBehavior,
        MorphSurfaceLayerBehavior,
        Widget):
    """A divider widget that visually separates content areas.

    This class combines the functionality of Kivy's Widget with
    several MorphUI behaviors to enhance its capabilities:
    - `MorphColorThemeBehavior`: Integrates color theming capabilities.
    - `MorphSurfaceLayerBehavior`: Provides surface styling options.

    Examples
    --------
    ```python
    from morphui.app import MorphApp
    from morphui.uix.boxlayout import MorphBoxLayout
    from morphui.uix.divider import MorphDivider
    from morphui.uix.label import MorphLabel

    class MyApp(MorphApp):
        def build(self) -> MorphBoxLayout:
            self.theme_manager.seed_color = 'Purple'
            return MorphBoxLayout(
                MorphLabel(
                    text="Above the Divider",
                    theme_style='primary'),
                MorphDivider(
                    orientation='horizontal',
                    thickness=1,),
                MorphLabel(
                    text="Below the Divider",
                    theme_style='secondary',
                    auto_size=True,),
                orientation='vertical',
                spacing=15,
                padding=50,)
                
    MyApp().run()
    ```
    """

    orientation: str = StringProperty(
        'horizontal', options=('horizontal', 'vertical'))
    """Orientation of the divider, either 'horizontal' or 'vertical'.

    This property determines the layout direction of the divider.

    :attr:`orientation` is a
    :class:`~kivy.properties.StringProperty` and defaults to 
    'horizontal'."""

    thickness: float = NumericProperty(1.0)
    """Thickness of the divider line in pixels.

    :attr:`thickness` is a :class:`~kivy.properties.NumericProperty` and
    defaults to 1.0."""

    default_config: Dict[str, Any] = dict(
        theme_color_bindings=dict(
            surface_color='outline_color'))
    """Default configuration values for MorphDivider.

    Provides standard appearance and behavior settings:
    - `theme_color_bindings`: Maps the `surface_color` to the
        `outline_color` from the theme for consistent styling.
    """

    def __init__(self, **kwargs) -> None:
        config = clean_default_config(self.default_config) | kwargs
        super().__init__(**config)
        self.bind(
            orientation=self._update_appearance,
            thickness=self._update_appearance,)
        
        self._update_appearance()

    def _update_appearance(self, *args) -> None:
        """Update the divider's visual properties."""
        if self.orientation == 'horizontal':
            self.size_hint_y = None
            self.height = dp(self.thickness)
            self.size_hint_x = 1
        else:
            self.size_hint_x = None
            self.width = dp(self.thickness)
            self.size_hint_y = 1
