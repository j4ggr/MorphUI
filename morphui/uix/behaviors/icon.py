from typing import Any

from kivy.properties import StringProperty

from .appreference import MorphAppReferenceBehavior


__all__ = [
    'MorphIconBehavior',]


class MorphIconBehavior(MorphAppReferenceBehavior):
    """A behavior that provides icon functionality to widgets.

    This behavior adds icon property and automatic text updating based
    on icon names. It requires the widget to have a `text` property
    and access to typography through the app reference.

    Examples
    --------
    ```python
    from morphui.uix.behaviors import MorphIconBehavior
    from kivy.uix.label import Label

    class IconWidget(MorphIconBehavior, Label):
        pass

    widget = IconWidget()
    widget.icon = 'home'  # Automatically sets text to icon character
    ```

    Notes
    -----
    - Requires the widget to have a `text` property for icon display
    - Uses typography's icon mapping to convert icon names to characters
    - Automatically updates text when icon property changes
    """

    icon: str = StringProperty('')
    """The name of the icon to display, corresponding to the icon font 
    mapping.
    
    This property should match a key in the typography's icon map.
    Changing this property will update the widget's text to show the
    corresponding icon character.
    
    :attr:`icon` is a :class:`~kivy.properties.StringProperty`
    and defaults to ''.
    """

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.bind(icon=self._apply_icon) # type: ignore
        if self.icon:
            self._apply_icon(self, self.icon)

    def _apply_icon(self, instance: Any, icon: str) -> None:
        """Update the widget's text when the icon property changes.
        
        This method looks up the icon name in the typography's icon map
        and sets the widget's text to the corresponding character.

        Parameters
        ----------
        instance : Any
            The widget instance (typically self).
        icon : str
            The icon name to apply.
        """
        if hasattr(self, 'text') and hasattr(self, 'typography'):
            self.text = self.typography.get_icon_character(icon)