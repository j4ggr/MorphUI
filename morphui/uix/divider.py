from kivy.uix.widget import Widget
from kivy.properties import ColorProperty
from kivy.properties import StringProperty
from kivy.properties import NumericProperty

from .behaviors import MorphColorThemeBehavior
from .behaviors import MorphSurfaceLayerBehavior


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
                    height=1,
                    theme_style='surface',),
                MorphLabel(
                    text="Below the Divider",
                    theme_style='secondary',
                    auto_size=True,),
                orientation='vertical',)
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

    divider_thickness: float = NumericProperty(1.0)
    """Thickness of the divider line in pixels.

    :attr:`divider_thickness` is a
    :class:`~kivy.properties.NumericProperty` and defaults to 1.0."""

    divider_color: list = ColorProperty([0.8, 0.8, 0.8, 1])
    """Color of the divider line in RGBA format.

    The color should be provided as a list of RGBA values between 0 and
    1. Example: `[0.8, 0.8, 0.8, 1]` for a light gray divider.

    :attr:`divider_color` is a :class:`~kivy.properties.ColorProperty`
    and defaults to `[0.8, 0.8, 0.8, 1]`.
    """

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.bind(
            pos=self._update_canvas,
            size=self._update_canvas,
            orientation=self._update_canvas,
            divider_thickness=self._update_canvas,
            divider_color=self._update_canvas,)
        
        self._update_divider()

    def _update_divider(self, *args) -> None:
        """Update the divider's visual properties."""

        self.canvas.before.clear()
        with self.canvas.before:
            Color(*self.divider_color)
            if self.orientation == 'horizontal':
                Rectangle(
                    pos=self.pos,
                    size=(self.width, self.divider_thickness))
            else:
                Rectangle(
                    pos=self.pos,
                    size=(self.divider_thickness, self.height))