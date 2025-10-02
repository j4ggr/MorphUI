from typing import Any
from typing import List
from typing import Dict

from kivy.event import EventDispatcher
from kivy.uix.widget import Widget
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
    
    The class also provides tab navigation between widgets in the
    :attr:`tab_widgets` list. When the tab key is pressed, focus will 
    move to the next widget in the list.
    """

    disable_key_press: bool = BooleanProperty(False)
    """Disable key press events if True.
    
    :attr:`disable_key_press` is a 
    :class:`~kivy.properties.BooleanProperty` and defaults to False."""

    tab_widgets: List[Any] = ListProperty([])
    """List of widgets to focus on tab key press.
    
    All widgets in this list must have a `focus` attribute (e.g.
    TextInput, Button, etc.). The focus will move to the next widget
    in the list when the tab key is pressed. If no widget has focus
    and :attr:`persist_focus_state` is False, it will start from the
    beginning of the list. Otherwise it will continue from the last
    focused widget. If the last widget has focus, it will wrap around
    to the first widget.
    
    :attr:`tab_widgets` is a :class:`~kivy.properties.ListProperty` and
    defaults to an empty list."""

    index_last_focus: int = NumericProperty(-1)
    """Index of last focused widget. 
    
    Equal to -1 if no widget has focus and :attr:`persist_focus_state` 
    is False. Otherwise, it retains the index of the last focused widget.
    
    :attr:`index_last_focus` is a 
    :class:`~kivy.properties.NumericProperty` and defaults to -1."""

    index_next_focus: int = NumericProperty(0)
    """Index of next focused text field.
    
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
        """True if any of the widgets in `tab_widgets` has focus."""
        return any(getattr(w, 'focus', False) for w in self.tab_widgets)
    
    def _press_event_name(self, key_name: str) -> str:
        """Return the event name for the given key name."""
        return f'on_{key_name}_press'
    
    def _release_event_name(self, key_name: str) -> str:
        """Return the event name for the given key name."""
        return f'on_{key_name}_release'

    def on_tab_widgets(self, instance: Any, tab_widgets: List[Widget]) -> None:
        """Reset index for last and next focus. Fired when the value of 
        `tab_widgets` is changed.
        
        Parameters
        ----------
        instance : Any
            The instance of the KeyPressBehavior.
        tab_widgets : List[Widget]
            The new list of tab widgets.
        
        Raises
        ------
        AssertionError
            If any widget in `tab_widgets` does not have a `focus` 
            attribute.
        """
        assert all(hasattr(w, 'focus') for w in tab_widgets), (
            'All widgets in tab_widgets must have a focus attribute.')
        self.index_last_focus = -1
        self.index_next_focus = 0
    
    def _skip_keypress_event(self, keycode: int) -> bool:
        """Return True if key press event should be ignored.
        By default, key press events are ignored if `disable_key_press`
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
            self.disable_key_press,
            self.ignore_key_press,
            keycode not in self.key_map.keys(),))
        return skip

    def on_key_press(
            self, instance: Any, keyboard: int, keycode: int, text: str | None,
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
            The last focused index.
        """
        pass

    def on_index_next_focus(
            self, instance: Any, index_next_focus: int) -> None:
        """Ensure the next focus index is within bounds. Fired when the 
        value of `index_next_focus` is changed.

        Parameters
        ----------
        instance : Any
            The instance of the KeyPressBehavior.
        index_next_focus : int
            The next focused index.
        """
        if self.index_next_focus >= len(self.tab_widgets):
            self.index_next_focus = 0

    def on_tab_press(self, *args) -> None:
        """Callback for the tab key. Dispatched when tab key is down.
        It moves the focus to the next widget in the :attr:`tab_widgets`
        list. If no widget has focus, it starts from the beginning of 
        the list. If the last widget has focus, it wraps around to the 
        first widget."""
        if not self.tab_widgets:
            return
        
        if self.has_focus:
            for i, widget in enumerate(self.tab_widgets):
                if widget.focus:
                    self.index_last_focus = i
                    self.index_next_focus = i + 1
                    break
    
    def on_tab_release(self, *args) -> None:
        """Callback for the tab key. Dispatched when tab key is up.
        It sets the focus to the next widget in the :attr:`tab_widgets`
        list. If no widget has focus, it starts from the beginning of the
        list. If the last widget has focus, it wraps around to the first
        widget."""
        if not self.tab_widgets:
            return

        self.tab_widgets[self.index_last_focus].focus = False
        self.tab_widgets[self.index_next_focus].focus = True