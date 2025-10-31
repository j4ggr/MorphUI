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

    active_icon = StringProperty('checkbox-marked')
    """Icon name for the 'active' state of the widget.

    The icon is displayed when the widget is in the 'active' state
    (i.e., checked). The icon name should correspond to a valid icon in
    the Material Design Icons library. To automatically switch icons
    based on the `active` property, bind the :meth:`_update_icon` method
    to the `active` property of the widget.

    :attr:`active_icon` is a :class:`~kivy.properties.StringProperty` 
    and defaults to `"checkbox-marked"`.
    """

    normal_icon = StringProperty('checkbox-blank-outline')
    """Icon name for the 'normal' state of the widget.

    The icon is displayed when the widget is in the 'normal' state
    (i.e., unchecked). The icon name should correspond to a valid icon
    in the Material Design Icons library. To automatically switch icons
    based on the `active` property, bind the :meth:`_update_icon` method
    to the `active` property of the widget.

    :attr:`normal_icon` is a :class:`~kivy.properties.StringProperty` and
    defaults to `"checkbox-blank-outline"`.
    """

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.bind(# type: ignore
            normal_icon=self._update_icon,
            active_icon=self._update_icon,
            icon=self._apply_icon)
        
        if self.icon:
            self._apply_icon(self, self.icon)
        elif self.normal_icon or self.active_icon:
            self._update_icon()

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
        if icon == '':
            self.text = ''
            return
        
        if hasattr(self, 'text') and hasattr(self, 'typography'):
            self.text = self.typography.get_icon_character(icon)
    
    def _update_icon(self, *args) -> None:
        """Update the displayed icon based on the `active` state.
        
        This method switches the icon between `active_icon` and
        `normal_icon` depending on whether the widget is active.
        
        Bind this method to the `active` property to automatically
        update the icon when the state changes.
        """
        active = getattr(self, 'active', False)
        self.icon = self.active_icon if active else self.normal_icon
