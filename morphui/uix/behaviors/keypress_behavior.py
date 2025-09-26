from typing import Any
from typing import List
from typing import Dict

from kivy.event import EventDispatcher
from kivy.uix.widget import Widget
from kivy.properties import ListProperty
from kivy.properties import BooleanProperty
from kivy.properties import NumericProperty
from kivy.core.window import Window


class KeyPressBehavior(EventDispatcher):
    """Base class for widgets with key press behavior.
    
    This class provides key press and key release events for the keys
    defined in the `key_map` dictionary. You can extend or modify this
    dictionary in subclasses. The key names are used to create events
    like `on_<key_name>_press` and `on_<key_name>_release`.
    
    The class also provides tab navigation between widgets in the
    `tab_widgets` list. When the tab key is pressed, focus will move
    to the next widget in the list.
    """

    disable_key_press: bool = BooleanProperty(False)
    """Disable key press events if True."""

    tab_widgets: List[Any] = ListProperty([])
    """List of widgets to focus on tab key press."""

    index_last_focus: int = NumericProperty(-1)
    """Index of last focused widget."""

    index_next_focus: int = NumericProperty(0)
    """Index of next focused text field."""

    keycode: int = NumericProperty(-1)
    """Keycode of the last pressed key."""

    modifiers: List[str] = ListProperty([])
    """List of currently held modifier keys."""

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
    like `on_<key_name>_press` and `on_<key_name>_release`. """

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
        """Override this method to ignore key press events (read-only).
        By default, key press events are ignored if last key pressed is 
        not in key_map."""
        return self.keycode not in self.key_map.keys()
    
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
        """Update index for next focus. Fired when the value of 
        `tab_widgets` is changed."""
        assert all(hasattr(w, 'focus') for w in tab_widgets), (
            'All widgets in tab_widgets must have a focus attribute.')
        self.index_last_focus = -1
        
    def on_key_press(
            self, instance: Any, keyboard: int, keycode: int, text: str,
            modifiers: List[str]) -> None:
        """Callback for key press events."""
        self.keycode = keycode
        self.modifiers = modifiers
        if self.disable_key_press or self.ignore_key_press:
            return

        name = self.key_map[keycode]
        method_name = self._press_event_name(name)
        if not hasattr(self, method_name):
            return

        self.dispatch(method_name)
        
    def on_key_release(
            self, instance: Any, keyboard: int, keycode: int) -> None:
        """Callback for key release events."""
        if self.disable_key_press or self.ignore_key_press:
            return
        
        name = self.key_map[keycode]
        method_name = self._release_event_name(name)
        if not hasattr(self, method_name):
            return

        self.dispatch(method_name)

    def on_index_last_focus(self, instance: Any, index_last_focus: int) -> None:
        """Update index for next focus. Fired when the value of 
        `index_last_focus` is changed."""
        index_next = index_last_focus + 1
        if index_next >= len(self.tab_widgets):
            index_next = 0
        self.index_next_focus = index_next

    def on_tab_press(self, *args) -> None:
        """Callback for the tab key. Dispatched when tab key is down."""
        if not self.tab_widgets:
            return
        
        if not self.has_focus:
            self.index_last_focus = -1
        else:
            for i, widget in enumerate(self.tab_widgets):
                if widget.focus:
                    widget.focus = False
                    self.index_last_focus = i
                    break
    
    def on_tab_release(self, *args) -> None:
        """Callback for the tab key. Dispatched when tab key is up."""
        if not self.tab_widgets:
            return

        self.tab_widgets[self.index_next_focus].focus = True