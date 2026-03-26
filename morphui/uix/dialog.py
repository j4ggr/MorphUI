from typing import List

from textwrap import dedent

from kivy.lang import Builder
from kivy.metrics import dp
from kivy.uix.widget import Widget
from kivy.properties import ColorProperty
from kivy.properties import AliasProperty
from kivy.properties import ObjectProperty
from kivy.core.window import Window

from morphui.uix.boxlayout import MorphElevationBoxLayout
from morphui.uix.behaviors import MorphSizeBoundsBehavior
from morphui.uix.behaviors import MorphDialogMotionBehavior


__all__ = [
    'MorphScrimLayer',
    'MorphDialog',
    ]


class MorphScrimLayer(Widget):
    """A semi-transparent overlay that appears behind a dialog to focus 
    the user's attention on the dialog content.

    The scrim layer is typically used in conjunction with a dialog to
    create a visual separation between the dialog and the rest of the
    application interface. It helps to emphasize the dialog and reduce
    distractions from the background content.
    """

    color: List[float] = ColorProperty([0, 0, 0, 0.5])
    """The color of the scrim layer, specified as a list of four float 
    values representing the red, green, blue, and alpha (opacity) 
    components of the color.

    :attr:`color` is a :class:`~kivy.properties.ColorProperty` and 
    defaults to `[0, 0, 0, 0.5]`, which means the scrim will be black 
    with 50 % opacity.
    """

    Builder.load_string(dedent('''
        <MorphScrimLayer>:
            canvas:
                Color:
                    rgba: self.color
                Rectangle:
                    pos: self.pos
                    size: self.size
        '''))


class MorphDialog(
        MorphDialogMotionBehavior,
        MorphSizeBoundsBehavior,
        MorphElevationBoxLayout,):
    """A dialog widget that displays content in a modal overlay with a
    scrim layer behind it.

    The :class:`MorphDialog` class provides a customizable dialog 
    component that can be used to display information, prompt the user 
    for input, or present other interactive content in a modal overlay.

    The dialog includes a scrim layer that appears behind it to focus 
    the user's attention on the dialog content and reduce distractions 
    from the background interface.
    """

    def _get_scrim_color(self) -> List[float]:
        """Get the current color of the scrim layer.

        This method retrieves the color of the scrim layer that appears
        behind the dialog.

        Returns
        -------
        List[float]
            A list of four float values representing the red, green, 
            blue, and alpha (opacity) components of the scrim color.
        """
        return self._scrim_widget.color

    def _set_scrim_color(self, color: List[float]) -> None:
        """Set the color of the scrim layer.

        This method updates the color of the scrim layer that appears
        behind the dialog. It is called when the `scrim_color` property
        is updated.

        Parameters
        ----------
        color : List[float]
            A list of four float values representing the red, green, 
            blue, and alpha (opacity) components of the scrim color.
        """
        self._scrim_widget.color = color

    scrim_color: List[float] = AliasProperty(
        _get_scrim_color,
        _set_scrim_color,
        bind=['_scrim_widget'])
    """The color of the scrim layer behind the dialog, specified as a
    list of four float values representing the red, green, blue, and
    alpha (opacity) components of the color.

    :attr:`scrim_color` is an :class:`~kivy.properties.AliasProperty` 
    that provides a convenient way to get and set the color of the scrim 
    layer without directly accessing the internal `_scrim_widget`. It is 
    bound to changes in the :attr:`_scrim_widget` property to ensure 
    that updates to the scrim color are reflected in the scrim widget
    when it is created or updated.
    """

    _scrim_widget: MorphScrimLayer = ObjectProperty()
    """Internal reference to the scrim widget used in the dialog. This
    property is managed internally by the dialog and should not be set
    manually.

    :attr:`_scrim_widget` is a class attribute that holds an instance of 
    :class:`MorphScrimLayer`. It is used to manage the scrim layer that 
    appears behind the dialog.
    """

    default_config = (
        MorphElevationBoxLayout.default_config.copy() | dict(
        theme_color_bindings={
            'normal_surface_color': 'surface_container_highest_color',},
        orientation='vertical',
        radius=dp(12),
        spacing=dp(8),
        padding=dp(16),
        size_hint=(None, None),
        auto_size=(False, True),
        size=(dp(500), dp(360)),))

    def __init__(self, *widgets, **kwargs) -> None:
        self._scrim_widget = MorphScrimLayer()
        super().__init__(**kwargs)
        self.declarative_children = list(widgets)

    def _add_to_window(self, *args) -> None:
        """Add the dialog to the window.

        This method adds the dialog to the window and ensures that the
        scrim layer is also added if it is not already present. If the
        dialog is already open, it does nothing.
        """
        if self.is_open:
            return
        
        if self._scrim_widget.parent is None:
            Window.add_widget(self._scrim_widget)
        
        super()._add_to_window(*args)

    def _remove_from_window(self, *args) -> None:
        """Remove the dialog and scrim from the window.

        This method removes the dialog and its associated scrim layer
        from the window. It is called when the dialog is dismissed.
        """
        if self._scrim_widget.parent:
            Window.remove_widget(self._scrim_widget)
        super()._remove_from_window(*args)
