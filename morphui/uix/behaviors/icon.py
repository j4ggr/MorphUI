from typing import Tuple
from typing import get_args

from kivy.event import EventDispatcher
from kivy.properties import AliasProperty
from kivy.properties import StringProperty
from kivy.properties import BooleanProperty

from morphui._typing import IconState
from morphui.uix.behaviors import MorphScaleBehavior
from morphui.uix.behaviors import MorphAppReferenceBehavior


__all__ = [
    'MorphIconBehavior',]


class MorphIconBehavior(
        EventDispatcher,
        MorphAppReferenceBehavior,):
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

    disabled: bool = BooleanProperty(False)
    """Indicates whether the widget is disabled.

    This property can be used to change the icon based on disabled
    state, if desired.

    :attr:`disabled` is a :class:`~kivy.properties.BooleanProperty` and
    defaults to `False`.
    """

    focus: bool = BooleanProperty(False)
    """Indicates whether the widget is focused.

    This property can be used to change the icon based on focus state,
    if desired.

    :attr:`focus` is a :class:`~kivy.properties.BooleanProperty` and
    defaults to `False`.
    """

    active: bool = BooleanProperty(False)
    """Indicates whether the widget is in an active state.

    This property is used to determine if the widget should apply the
    `active_icon` or `normal_icon`. For example, in toggle buttons or
    checkboxes, this property reflects whether the widget is checked or
    not.

    :attr:`active` is a :class:`~kivy.properties.BooleanProperty` and
    defaults to `False`.
    """

    icon_state_precedence: Tuple[str, ...] = get_args(IconState)
    """Defines the precedence order for icon states.

    This tuple specifies the order in which icon states are checked to
    determine which icon to display. The available states are:
    - 'disabled': When the widget is disabled (i.e., `disabled` is
      `True`)
    - 'focus': When the widget is focused (i.e., `focus` is `True`)
    - 'active': When the widget is active (i.e., `active` is `True`)
    - 'normal': The default state when none of the above states apply.

    Default order is ('disabled', 'focus', 'active', 'normal').
    """

    def _get_icon(self) -> str:
        """Get the current icon based on the current state.

        This method checks the widget's state in the order defined by
        `icon_state_precedence` and returns the corresponding icon name.
        If no specific state icon is set, it returns the `normal_icon`.

        Returns
        -------
        str
            The icon name corresponding to the current state.
        """
        for state in self.icon_state_precedence:
            value = getattr(self, state, False)
            icon = getattr(self, f'{state}_icon', None)
            if value and icon:
                return icon
        return self.normal_icon
    
    def _set_icon(self, icon: str) -> None:
        """Set the icon and update the widget's text accordingly.

        The method looks up the icon name in the typography's icon map
        and sets the widget's text to the corresponding character.

        Parameters
        ----------
        icon : str
            The icon name to set.
        """
        if not hasattr(self, 'text'):
            return
        
        def _set_text(self, text: str) -> None:
            self.text = text
        
        if icon and not (self.normal_icon or self.active_icon):
            self.normal_icon = icon

        if getattr(self, 'typography', None) is None:
            text = icon
        elif icon == '':
            text = ''
        else:
            text = self.typography.get_icon_character(icon)

        if self.text == text:
            return

        if issubclass(type(self), MorphScaleBehavior) and self.scale_enabled:
            if text:
                _set_text(self, text)
                self.animate_scale_in()
            else:
                self.animate_scale_out(callback=lambda *a: _set_text(self, text))
        else:
            _set_text(self, text)

    icon: str = AliasProperty(
        _get_icon,
        _set_icon,
        bind=[
            'normal_icon',
            'active_icon'],)
    """Gets or sets the icon name for the widget.
    
    The `icon` property represents the name of the icon to be displayed
    on the widget. Setting this property will automatically update the
    widget's `text` property to the corresponding icon character based
    on the typography's icon mapping.

    :attr:`icon` is an :class:`~kivy.properties.AliasProperty` that
    gets and sets the icon name.
    """

    normal_icon: str = StringProperty('')
    """Icon name for the 'normal' state of the widget.

    The icon is displayed when the widget is in the 'normal' state
    (i.e., unchecked). The icon name should correspond to a valid icon
    in the Material Design Icons library. To automatically switch icons
    based on the `active` property, bind the :meth:`_update_icon` method
    to the `active` property of the widget.

    :attr:`normal_icon` is a :class:`~kivy.properties.StringProperty` and
    defaults to `""`.
    """

    disabled_icon: str | None = StringProperty(None, allownone=True)
    """Icon name for the 'disabled' state of the widget.

    The icon is displayed when the widget is in the 'disabled' state
    (i.e., disabled). The icon name should correspond to a valid icon in
    the Material Design Icons library. To automatically switch icons
    based on the `disabled` property, bind the :meth:`_update_icon`
    method to the `disabled` property of the widget.

    :attr:`disabled_icon` is a :class:`~kivy.properties.StringProperty` 
    and defaults to `None`.
    """

    focus_icon: str | None = StringProperty(None, allownone=True)
    """Icon name for the 'focus' state of the widget.

    The icon is displayed when the widget is in the 'focus' state
    (i.e., focused). The icon name should correspond to a valid icon in
    the Material Design Icons library. To automatically switch icons
    based on the `focus` property, bind the :meth:`_update_icon` method
    to the `focus` property of the widget.

    :attr:`focus_icon` is a :class:`~kivy.properties.StringProperty` 
    and defaults to `None`.
    """

    active_icon: str | None = StringProperty(None, allownone=True)
    """Icon name for the 'active' state of the widget.

    The icon is displayed when the widget is in the 'active' state
    (i.e., checked). The icon name should correspond to a valid icon in
    the Material Design Icons library. To automatically switch icons
    based on the `active` property, bind the :meth:`_update_icon` method
    to the `active` property of the widget.

    :attr:`active_icon` is a :class:`~kivy.properties.StringProperty` 
    and defaults to `None`.
    """

    def __init__(self, **kwargs) -> None:
        icon = kwargs.pop('icon', '')
        super().__init__(**kwargs)
        self.bind(
            disabled=self._update_icon,
            active=self._update_icon,
            focus=self._update_icon,
            disabled_icon=self._update_icon,
            focus_icon=self._update_icon,
            active_icon=self._update_icon,
            normal_icon=self._update_icon,)
        if icon:
            self.icon = icon
        else:
            self._update_icon()
    
    def _update_icon(self, *args) -> None:
        """Update the displayed icon based on the `active` state.
        
        This method switches the icon between `active_icon` and
        `normal_icon` depending on whether the widget is active.
        
        Bind this method to the `active` property to automatically
        update the icon when the state changes.
        """
        self.icon = self._get_icon()
