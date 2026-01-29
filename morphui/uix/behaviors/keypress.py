from re import L
from typing import Any
from typing import List
from typing import Dict

from kivy.event import EventDispatcher
from kivy.properties import ListProperty
from kivy.properties import DictProperty
from kivy.properties import AliasProperty
from kivy.properties import ObjectProperty
from kivy.properties import StringProperty
from kivy.properties import BooleanProperty
from kivy.properties import NumericProperty
from kivy.core.window import Window


__all__ = [
    'MorphKeyPressBehavior',
    'MorphTabNavigationManagerBehavior',
    'MorphTabNavigableBehavior',]


class MorphKeyPressBehavior(EventDispatcher):
    """Base class for widgets with key press behavior.
    
    This class provides key press and key release events for the keys
    defined in the `key_map` dictionary. You can extend or modify this
    dictionary in subclasses. The key names are used to create events
    like `on_<key_name>_press` and `on_<key_name>_release`.
    """

    key_press_enabled: bool = BooleanProperty(True)
    """Disable key press events if False.
    
    :attr:`key_press_enabled` is a 
    :class:`~kivy.properties.BooleanProperty` and defaults to True."""

    keyboard: int = NumericProperty(0)
    """Keyboard id. Set when a key is pressed.
    
    :attr:`keyboard` is a 
    :class:`~kivy.properties.NumericProperty` and defaults to 0."""

    key_text: str | None = StringProperty('', allownone=True)
    """Text representation of the last pressed key.
    
    Set when a key is pressed. Can be None for non-text keys. For 
    example, the 'a' key will set this property to 'a', while the 'enter' 
    key will set it to None. Note that letter keys will be lowercase
    regardless of whether shift is held. To check for uppercase letters,
    check the `modifiers` property for 'shift'.
    
    :attr:`key_text` is a 
    :class:`~kivy.properties.StringProperty` and defaults to an empty
    string.
    """

    keycode: int = NumericProperty(-1)
    """Keycode of the last pressed key.
    
    This is a numeric representation of the key. Set when a key is 
    pressed.
    
    :attr:`keycode` is a 
    :class:`~kivy.properties.NumericProperty` and defaults to -1.
    """

    modifiers: List[str] = ListProperty([])
    """List of currently held modifier keys.

    Possible values include 'shift', 'ctrl', 'alt', 'numlock', etc.
    Set when a key is pressed.

    :attr:`modifiers` is a 
    :class:`~kivy.properties.ListProperty` and defaults to an empty 
    list.
    """

    key_map: Dict[int, str] = {
        40: 'enter',
        41: 'escape',
        42: 'backspace',
        43: 'tab',
        44: 'space',
        79: 'arrow_right',
        80: 'arrow_left',
        81: 'arrow_down',
        82: 'arrow_up',}
    """Mapping of key codes to key names. You can extend or modify this 
    dictionary in subclasses. The key names are used to create events 
    like `on_<key_name>_press` and `on_<key_name>_release`. 
    
    If a key code is not in this dictionary, it will be ignored!"""

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        for name in self.key_map.values():
            press_name = self._press_event_name(name)
            release_name = self._release_event_name(name)
            if not hasattr(self, press_name):
                setattr(self, press_name, lambda self=self, *args: None)
            if not hasattr(self, release_name):
                setattr(self, release_name, lambda self=self, *args: None)
            self.register_event_type(press_name)
            self.register_event_type(release_name)

        Window.bind(on_key_down=self.on_key_press)
        Window.bind(on_key_up=self.on_key_release)
    
    @property
    def ignore_key_press(self) -> bool:
        """Override this property to provide custom logic for ignoring 
        key press events (read-only). By default, it returns False."""
        return False
    
    def _press_event_name(self, key_name: str) -> str:
        """Return the event name for the given key name."""
        return f'on_{key_name}_press'
    
    def _release_event_name(self, key_name: str) -> str:
        """Return the event name for the given key name."""
        return f'on_{key_name}_release'
    
    def _skip_keypress_event(self, keycode: int) -> bool:
        """Return True if key press event should be ignored.
        By default, key press events are ignored if `key_press_enabled`
        is True, `ignore_key_press` is True, or the keycode is not in
        `key_map`.
        
        Parameters
        ----------
        keycode : int
            The keycode of the key press event.
            
        Returns
        -------
        bool
            True if the key press event should be ignored.
        """
        skip = any((
            not self.key_press_enabled,
            self.ignore_key_press,
            keycode not in self.key_map.keys(),))
        return skip

    def on_key_press(
            self,
            instance: Any,
            keyboard: int,
            keycode: int,
            text: str | None,
            modifiers: List[str]) -> None:
        """Callback for key press events. Binds to the Window's
        on_key_down event.
        
        Parameters
        ----------
        instance : Any
            The instance of the Window.
        keyboard : int
            The keyboard id.
        keycode : int
            The keycode of the pressed key.
        text : str
            The text representation of the pressed key.
        modifiers : List[str]
            List of currently held modifier keys e.g. 'shift', 'ctrl', 
            etc.
        """
        if self._skip_keypress_event(keycode):
            return
        
        self.keyboard = keyboard
        self.key_text = text
        self.keycode = keycode
        self.modifiers = modifiers
        name = self.key_map[keycode]
        method_name = self._press_event_name(name)
        if hasattr(self, method_name):
            self.dispatch(method_name)
        
    def on_key_release(
            self, instance: Any, keyboard: int, keycode: int) -> None:
        """Callback for key release events. Binds to the Window's
        on_key_up event.
        
        Parameters
        ----------
        instance : Any
            The instance of the Window.
        keyboard : int
            The keyboard id.
        keycode : int
            The keycode of the released key.
        """
        if self._skip_keypress_event(keycode):
            return
        
        name = self.key_map[keycode]
        method_name = self._release_event_name(name)
        if hasattr(self, method_name):
            self.dispatch(method_name)


class MorphTabNavigationManagerBehavior(MorphKeyPressBehavior):
    """Base class for widgets with tab navigation behavior.
    
    This class provides tab navigation between widgets using groups.
    Widgets can be assigned to tab groups by setting their `tab_group` 
    property. When the tab key is pressed, focus will move to the next 
    widget in the same group.

    Notes
    -----
    Use this class only once in your widget hierarchy to manage tab
    navigation. Best practice is to have a single root widget (e.g. the
    main application widget) inherit from this class.

    Widgets that should participate in tab navigation must inherit from
    :class:`MorphTabBehavior` and set their `tab_group` property to the 
    desired group name and their `tab_manager` property to the instance
    of this class.
    """

    current_tab_group: str = StringProperty('')
    """Current tab group name.

    This property determines which group of widgets will be used for
    tab navigation. Only widgets in this group will be considered when
    navigating with the tab key.
    
    :attr:`current_tab_group` is a
    :class:`~kivy.properties.StringProperty` and defaults to an
    empty string."""

    _index_last_focus: Dict[str, int] = DictProperty({})
    """Store the index of the last focus widget."""

    def _get_index_last_focus(self) -> int:
        """Get the index of the last focus widget for the current tab 
        group. This will be -1 if no widget in the current tab group has
        focus."""
        index = self._index_last_focus.get(self.current_tab_group, None)
        if index is None:
            for i, w in enumerate(self.tab_widgets):
                if getattr(w, 'focus', False):
                    index = i
                    self._index_last_focus[self.current_tab_group] = index
                    break
            else:
                index = -1
        return max(index, len(self.tab_widgets) - 1)
    
    def _set_index_last_focus(self, value: int) -> None:
        """Set the index of the last focus widget for the current tab 
        group."""
        self._index_last_focus[self.current_tab_group] = value

    index_last_focus: int = AliasProperty(
        _get_index_last_focus,
        _set_index_last_focus,
        bind=[
            '_index_last_focus',
            'current_tab_group'])
    """Index of last focus widget.

    Returns -1 if no widget in the current tab group has focus.
    
    :attr:`index_last_focus` is a
    :class:`~kivy.properties.AliasProperty` and defaults to -1.
    """

    def _get_index_next_focus(self) -> int:
        """Get the index of the next focus widget for the current tab 
        group. If no widget has focus, it returns 0. If the last widget
        has focus, it wraps around to 0."""
        index = self._index_last_focus.get(self.current_tab_group, -1) + 1
        if index >= len(self.tab_widgets):
            index = 0
        return index
    
    index_next_focus: int = AliasProperty(
        _get_index_next_focus,
        None,
        bind=[
            '_index_last_focus',
            'current_tab_group'])
    """Index of next focus widget (read-only).

    If no widget has focus, it returns 0. If the last widget has focus,
    it wraps around to 0.

    :attr:`index_next_focus` is a
    :class:`~kivy.properties.AliasProperty` and defaults to 0.
    """

    _tab_widgets: Dict[str, List[Any]] = DictProperty({})
    """Tab groups dictionary mapping group names to lists of widgets.
    
    This allows multiple independent tab groups to exist. Each group
    contains widgets that will participate in tab navigation within
    that group only.
    
    :attr:`tab_widgets` is a :class:`~kivy.properties.DictProperty`
    and defaults to an empty dictionary."""

    def _get_tab_widgets(self) -> List[Any]:
        """Get the list of widgets in the current tab group.
         Only returns widgets that are not disabled."""
        return [
            widget for widget in
            self._tab_widgets.get(self.current_tab_group, [])
            if not getattr(widget, 'disabled', False)]

    tab_widgets: List[Any] = AliasProperty(
        _get_tab_widgets,
        None,
        bind=[
            '_tab_widgets',
            'current_tab_group'])
    """List of widgets in the current tab group (read-only).

    This list contains the widgets that will participate in tab
    navigation for the current tab group.

    :attr:`tab_widgets` is a
    :class:`~kivy.properties.AliasProperty` and defaults to an empty
    list."""

    def on_tab_release(self, *args) -> None:
        """Callback for the tab key. Dispatched when tab key is up.
        It sets the focus to the next widget in the current tab group.
        If no widget has focus, it starts from the beginning of the
        list. If the last widget has focus, it wraps around to the first
        widget."""
        if not self.tab_widgets:
            return

        if self.index_last_focus >= 0:
            self.tab_widgets[self.index_last_focus].focus = False

        self.tab_widgets[self.index_next_focus].focus = True


class MorphTabNavigableBehavior(EventDispatcher):
    """Base class for widgets with tab navigation behavior.
    
    This class provides tab navigation between widgets using groups.
    Widgets can be assigned to tab groups by setting their `tab_group` 
    property. When the tab key is pressed, focus will move to the next 
    widget in the same group.
    """

    focus: bool = BooleanProperty(False)
    """Indicates whether the widget currently has focus.

    This property should is set to True when the widget gains focus by
    tab navigation, and set to False when it loses focus.

    :attr:`focus` is a :class:`~kivy.properties.BooleanProperty` and
    defaults to False."""

    tab_manager: MorphTabNavigationManagerBehavior | None = ObjectProperty(
        None, allownone=True)
    """Reference to the tab navigation manager instance.

    This should be an instance of :class:`MorphTabNavigationManagerBehavior`
    that manages tab navigation for this widget. If None, the widget
    will not participate in tab navigation.

    :attr:`tab_manager` is a :class:`~kivy.properties.ObjectProperty`
    and defaults to None."""

    tab_group: str | None = StringProperty(None, allownone=True)
    """Tab group name for this widget instance.
    
    When set, this widget will be automatically added to the corresponding
    group in the class-level :attr:`tab_widgets` dictionary. Widgets in
    the same group participate in tab navigation together. Setting this
    to None removes the widget from all tab groups.
    
    :attr:`tab_group` is a :class:`~kivy.properties.StringProperty` and
    defaults to None."""

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.bind(
            tab_group=self._register_tab_group,
            focus=self._sync_focus_to_manager,)
        self._register_tab_group(self, self.tab_group)
        self._sync_focus_to_manager()
    
    def _register_tab_group(
            self,
            instance: Any,
            tab_group: str | None) -> None:
        """Register or unregister the widget in the tab manager's
        tab widgets dictionary based on the `tab_group` property.

        First, it removes the widget from all existing groups. Then,
        if `tab_group` is not None, it adds the widget to the specified
        group.
        
        Parameters
        ----------
        instance : Any
            The instance of the widget.
        tab_group : str | None
            The tab group name. If None, the widget is unregistered from
            all groups.
        """
        if not self.tab_manager:
            return
        
        for group, widgets in self.tab_manager._tab_widgets.items():
            if self in widgets:
                widgets.remove(self)
        
        if tab_group is not None:
            if tab_group not in self.tab_manager._tab_widgets:
                self.tab_manager._tab_widgets[tab_group] = []
            if self not in self.tab_manager._tab_widgets[tab_group]:
                self.tab_manager._tab_widgets[tab_group].append(self)

    def _sync_focus_to_manager(self, *args) -> None:
        """Sync the widget's focus state with the tab manager.
        
        When the widget gains focus, it updates the tab manager's
        `current_tab_group` and `index_last_focus` properties
        accordingly."""
        if self.focus and self.tab_manager and self.tab_group:
            self.tab_manager.current_tab_group = self.tab_group
            for i, widget in enumerate(self.tab_manager.tab_widgets):
                if widget is self:
                    self.tab_manager.index_last_focus = i
                    break
