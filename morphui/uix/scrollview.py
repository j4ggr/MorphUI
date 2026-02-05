
from kivy.uix.scrollview import ScrollView

from morphui.uix.behaviors import MorphDeclarativeBehavior

__all__ = [
    'MorphScrollView', ]


class MorphScrollView(
        MorphDeclarativeBehavior,
        ScrollView):
    """A ScrollView using MorphUI declarative behaviors.

    This class combines the functionality of Kivy's ScrollView with
    MorphUI's declarative behaviors to enhance its capabilities. It 
    allows for adding child widgets in a declarative manner while 
    maintaining the standard behavior and features of a ScrollView.

    Examples
    --------
    ```python
    from morphui.app import MorphApp
    from morphui.uix.label import MorphLabel
    from morphui.uix.boxlayout import MorphBoxLayout
    from morphui.uix.scrollview import MorphScrollView

    class MyApp(MorphApp):

        def build(self) -> MorphScrollView:
            self.theme_manager.theme_mode = 'Dark'
            self.theme_manager.seed_color = 'morphui_teal'

            return MorphScrollView(
                    MorphBoxLayout(
                        MorphLabel(text='Label 1', theme_style='primary'),
                        MorphLabel(text='Label 2', theme_style='secondary'),
                        MorphLabel(text='Label 3', theme_style='tertiary'),
                        size_hint=(1, None),
                        height=1000,
                        theme_style='surface',
                        orientation='vertical',
                        identity='scroll_content'),
                    identity='scroll_view',)

    MyApp().run()
    ```

    Notes
    -----
    The :class:`~kivy.uix.scrollview.ScrollView` accepts a single child 
    widget, which is typically a layout containing multiple widgets. And
    so does the :class:`~morphui.uix.scrollview.MorphScrollView`.

    The scroll view can be used to create scrollable content areas. It
    supports both vertical and horizontal scrolling, depending on the
    layout of its child widgets. The example above demonstrates a 
    vertical scroll view containing a box layout with several labels. 
    The scroll view will allow the user to scroll through the content if 
    it exceeds the visible area.
    """