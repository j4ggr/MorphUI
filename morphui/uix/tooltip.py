from typing import Any
from typing import Dict

from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout

from morphui.uix.behaviors import MorphElevationBehavior
from morphui.uix.behaviors import MorphAutoSizingBehavior
from morphui.uix.behaviors import MorphMenuMotionBehavior
from morphui.uix.behaviors import MorphColorThemeBehavior
from morphui.uix.behaviors import MorphDeclarativeBehavior
from morphui.uix.behaviors import MorphSurfaceLayerBehavior

from morphui.utils import clean_config

__all__ = [
    'MorphTooltip',]


class MorphTooltip(
        MorphDeclarativeBehavior,
        MorphMenuMotionBehavior,
        MorphColorThemeBehavior,
        MorphSurfaceLayerBehavior,
        MorphElevationBehavior,
        MorphAutoSizingBehavior,
        BoxLayout):
    """A tooltip widget that provides brief information about a UI element
    when hovered over.

    This widget combines the motion behavior for menu-like positioning
    with elevation styling to create a visually distinct tooltip.
    
    Example
    -------
    ```python
    from morphui.app import MorphApp
    from morphui.uix.label import MorphSimpleLabel
    from morphui.uix.button import MorphIconButton
    from morphui.uix.tooltip import MorphTooltip
    from morphui.uix.floatlayout import MorphFloatLayout

    class MyApp(MorphApp):

        def build(self) -> MorphFloatLayout:
            self.theme_manager.theme_mode = 'Dark'
            self.theme_manager.seed_color = 'morphui_teal'
            
            layout = MorphFloatLayout(
                MorphIconButton(
                    tooltip=MorphTooltip(
                        MorphSimpleLabel(
                            text="This is helpful information!",
                            auto_size=True),),
                    icon='information',
                    pos_hint={'center_x': 0.5, 'center_y': 0.5}),
                theme_color_bindings={
                    'normal_surface_color': 'surface_color',},)
            return layout

    if __name__ == '__main__':
        MyApp().run()
    ```
    """

    default_config: Dict[str, Any] = dict(
        theme_color_bindings=dict(
            normal_surface_color='surface_container_highest_color',),
        menu_caller_spacing=dp(8),
        orientation='vertical',
        padding=[dp(8), dp(4)],
        radius=dp(4),
        spacing=dp(5),
        elevation=2,
        scale_enabled=False,
        auto_size=(True, True),)
    """Default configuration for MorphTooltip."""
    
    def __init__(self, *widgets, **kwargs: Any) -> None:
        config = clean_config(self.default_config, kwargs)
        super().__init__(*widgets, **config)

    def _update_caller_bindings(self, *args) -> None:
        """Update bindings to the caller button's position and size.

        This method binds to the caller button's `pos` and `size`
        properties to adjust the tooltip position whenever the caller
        changes. If there is no caller set, it does nothing.
        """
        if self.caller is None:
            return
        
        super()._update_caller_bindings()
        self.caller.bind(
            on_enter=self.open,
            on_leave=self.dismiss,)

