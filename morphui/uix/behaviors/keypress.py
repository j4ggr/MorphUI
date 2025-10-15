from typing import Any
from typing import List
from typing import Dict

from kivy.event import EventDispatcher
from kivy.properties import ListProperty
from kivy.properties import StringProperty
from kivy.properties import BooleanProperty
from kivy.properties import NumericProperty
from kivy.core.window import Window


__all__ = ['MorphKeyPressBehavior']


class MorphKeyPressBehavior(EventDispatcher):
    """Base class for widgets with key press behavior.
    
    This class provides key press and key release events for the keys
    defined in the `key_map` dictionary. You can extend or modify this
    dictionary in subclasses. The key names are used to create events
    like `on_<key_name>_press` and `on_<key_name>_release`.
    
    The class also provides tab navigation between widgets using groups.
    Widgets can be assigned to tab groups by setting their `tab_group` 
    property. When the tab key is pressed, focus will move to the next 
    widget in the same group.
    """

    # Class-level dictionary to store tab groups
    tab_widgets: Dict[str, List[Any]] = {}
    """Class-level dictionary mapping group names to lists of widgets.
    
    This allows multiple independent tab groups to exist. Each group
    contains widgets that will participate in tab navigation within
    that group only.
    
    :attr:`tab_widgets` is a class attribute and defaults to an empty
    dictionary."""

    key_press_enabled: bool = BooleanProperty(True)
    """Disable key press events if False.
    
    :attr:`key_press_enabled` is a 
    :class:`~kivy.properties.BooleanProperty` and defaults to True."""

    tab_group: str | None = StringProperty(None, allownone=True)
    """Tab group name for this widget instance.
    
    When set, this widget will be automatically added to the corresponding
    group in the class-level :attr:`tab_widgets` dictionary. Widgets in
    the same group participate in tab navigation together. Setting this
    to None removes the widget from all tab groups.
    
    :attr:`tab_group` is a :class:`~kivy.properties.StringProperty` and
    defaults to None."""

    index_last_focus: int = NumericProperty(-1)
    """Index of last focus widget. 
    
    Equal to -1 if no widget has focus and :attr:`persist_focus_state` 
    is False. Otherwise, it retains the index of the last focus widget.
    
    :attr:`index_last_focus` is a 
    :class:`~kivy.properties.NumericProperty` and defaults to -1."""

    index_next_focus: int = NumericProperty(0)
    """Index of next focus text field.
    
    Wraps around to 0 if it exceeds the length of :attr:`tab_widgets`.
    
    :attr:`index_next_focus` is a 
    :class:`~kivy.properties.NumericProperty` and defaults to 0."""

    persist_focus_state: bool = BooleanProperty(False)
    """Whether to persist focus state when no widget has focus.

    When True, the focus indices are maintained even when all widgets
    lose focus, allowing tab navigation to resume from the last position.
    When False, focus indices are reset when no widget has focus.

    :attr:`persist_focus_state` is a 
    :class:`~kivy.properties.BooleanProperty` and defaults to False.
    """

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
    
    @property
    def has_focus(self) -> bool:
        """True if any of the widgets in this instance's tab group has
        focus."""
        if not self.tab_group or self.tab_group not in self.tab_widgets:
            return False
        return any(getattr(w, 'focus', False) for w in self.tab_widgets[self.tab_group])
    
    @property
    def current_tab_widgets(self) -> List[Any]:
        """Get the current tab widgets list for this instance's group."""
        if not self.tab_group or self.tab_group not in self.tab_widgets:
            return []
        return self.tab_widgets[self.tab_group]
    
    def _press_event_name(self, key_name: str) -> str:
        """Return the event name for the given key name."""
        return f'on_{key_name}_press'
    
    def _release_event_name(self, key_name: str) -> str:
        """Return the event name for the given key name."""
        return f'on_{key_name}_release'

    def on_tab_group(self, instance: Any, tab_group: str | None) -> None:
        """Handle changes to the tab_group property.
        
        When tab_group is set, adds this widget to the corresponding 
        group. When set to None, removes this widget from all groups.
        
        Parameters
        ----------
        instance : Any
            The instance of the KeyPressBehavior.
        tab_group : str | None
            The new tab group name or None.
        """
        # Remove from all groups first
        for group_name, widgets in self.tab_widgets.items():
            if self in widgets:
                widgets.remove(self)
                
        # Add to new group if specified
        if tab_group:
            if tab_group not in self.tab_widgets:
                self.tab_widgets[tab_group] = []
            if self not in self.tab_widgets[tab_group]:
                self.tab_widgets[tab_group].append(self)
                # Validate that the widget has focus attribute
                assert hasattr(self, 'focus'), (
                    'Widget must have a focus attribute to be added to tab group.')
        
        # Reset focus indices when group changes
        self.index_last_focus = -1
        self.index_next_focus = 0

    def on_index_next_focus(
            self, instance: Any, index_next_focus: int) -> None:
        """Ensure the next focus index is within bounds. Fired when the 
        value of `index_next_focus` is changed.

        Parameters
        ----------
        instance : Any
            The instance of the KeyPressBehavior.
        index_next_focus : int
            The next focus index.
        """
        current_widgets = self.current_tab_widgets
        if self.index_next_focus >= len(current_widgets):
            self.index_next_focus = 0
    
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

    def on_index_last_focus(
            self, instance: Any, index_last_focus: int) -> None:
        """Fired when the value of :attr:`index_last_focus` is changed,
        Usually called when the user navigates through focusable widgets.
        Override this method in subclasses to implement custom behavior.
        
        Parameters
        ----------
        instance : Any
            The instance of the KeyPressBehavior.
        index_last_focus : int
            The last focus index.
        """
        pass

    def on_tab_press(self, *args) -> None:
        """Callback for the tab key. Dispatched when tab key is down.
        It moves the focus to the next widget in the current tab group.
        If no widget has focus, it starts from the beginning of the 
        list. If the last widget has focus, it wraps around to the 
        first widget."""
        current_widgets = self.current_tab_widgets
        if not current_widgets:
            return
        
        if self.has_focus:
            for i, widget in enumerate(current_widgets):
                if getattr(widget, 'focus', False):
                    self.index_last_focus = i
                    self.index_next_focus = i + 1
                    break
    
    def on_tab_release(self, *args) -> None:
        """Callback for the tab key. Dispatched when tab key is up.
        It sets the focus to the next widget in the current tab group.
        If no widget has focus, it starts from the beginning of the
        list. If the last widget has focus, it wraps around to the first
        widget."""
        current_widgets = self.current_tab_widgets
        if not current_widgets:
            return

        if self.index_last_focus >= 0 and self.index_last_focus < len(current_widgets):
            current_widgets[self.index_last_focus].focus = False
        if self.index_next_focus < len(current_widgets):
            current_widgets[self.index_next_focus].focus = True