from typing import Any
from typing import List
from typing import Dict

from kivy.clock import Clock
from kivy.properties import ListProperty
from kivy.properties import ObjectProperty
from kivy.properties import StringProperty
from kivy.properties import NumericProperty

from ...constants import ICON


__all__ = [
    'DropdownBehavior',]


class MorphDropdownMenu:
    """A mock class representing a dropdown menu. Replace with the actual
    implementation."""
    
    def __init__(self, caller: Any, items: List[Dict[str, Any]], position: str) -> None:
        self.caller = caller
        self.items = items
        self.position = position
        self.parent = None  # Represents if the menu is open or not



class DropdownBehavior:
    """This is a base class used for opening a Dropdown Menu with a list 
    of entries.
    
    The entries can be of any type, but must
    be convertible to string via the `_entry_text` method. The
    dropdown menu is opened when the `open_menu` method is called.
    """

    entries: List[Any] = ListProperty([])
    """List of entries to show in the dropdown menu"""

    menu: Any = ObjectProperty()
    """Dropdown menu object"""

    current_icon: str = StringProperty(ICON.DD_MENU_CLOSED)
    """Current icon of the dropdown item"""

    dropdown_position: str = StringProperty('bottom')
    """Dropdown menu position must be 'top', 'auto', 'center' or 
    'bottom'."""

    menu_open_delay: float = NumericProperty(0.1)
    """Delay in seconds before opening the dropdown menu when the
    text field is focused."""

    _menu_state_icon: Dict[str, str] = {
        ICON.DD_MENU_OPEN: ICON.DD_MENU_CLOSED,
        ICON.DD_MENU_CLOSED: ICON.DD_MENU_OPEN,}
    """Mapping of icons for open and closed menu states."""

    @property
    def menu_is_open(self) -> bool:
        """True if the dropdown menu is open (read-only)."""
        if not self.menu:
            return False
        return bool(self.menu.parent)
    
    def entry_contains_text(self, entry: Any, text: str) -> bool:
        """Check if the text is in the provided entry."""
        entry_text = self._entry_text(entry)
        return text.lower() in entry_text.lower()

    def entries_contains_text(self, text: str) -> bool:
        """Check if the text is in any of the entries."""
        return any(self._entry_text(e) == text for e in self.entries)

    def _entry_text(self, entry: Any) -> str:
        """Get the text for a given entry."""
        if isinstance(entry, str):
            return entry
        elif isinstance(entry, dict):
            return str(entry.get('text', ''))
        elif hasattr(entry, 'text'):
            return str(entry.text)
        else:
            raise ValueError(
                'Entry must be of type str or have a text attribute')

    def _menu_item_instruction(self, entry: Any) -> Dict[str, Any]:
        """Convert an entry to a menu item instruction as expected from 
        `items` property of `MorphDropdownMenu`."""
        instruction = {
                'on_release': lambda x=entry: self.item_callback(x),
                'text': self._entry_text(entry),
            } | getattr(entry, 'instruction', {})
        return instruction
    
    def get_menu_item_instructions(self) -> List[Dict[str, Any]]:
        """Get the menu items instructions from the entries. Override 
        this method if you want to change the way entries are converted
        to menu item instructions. You can also override the 
        `_menu_item_instruction` method."""
        return list(map(self._menu_item_instruction, self.entries))

    def on_menu(self, instance: Any, menu: Any) -> None:
        """Called when the menu property is set. Binds the on_dismiss event."""
        if menu:
            assert hasattr(menu, 'bind'), (
                'menu must have a bind method to bind on_dismiss event.')
            assert hasattr(menu, 'dismiss'), (
                'menu must have a dismiss method to close the menu.')
            assert hasattr(menu, 'open'), (
                'menu must have an open method to open the menu.')
            assert hasattr(menu, 'items'), (
                'menu must have an items property to set the menu items.')
            menu.bind(on_dismiss=self.on_menu_dismiss)
    
    def open_menu(self, *args) -> None:
        """Open the dropdown menu."""
        if not self.entries or not self.menu or self.menu_is_open:
            return
        
        self.menu.items = self.get_menu_item_instructions()
        Clock.schedule_once(lambda dt: self.menu.open(), self.menu_open_delay)
        self.on_menu_open(self.menu)
        
    def item_callback(self, entry: Any) -> None:
        """Fired when an item is selected from the dropdown menu. Set 
        the text field's text to the selected item. You can override 
        this method, but keep in mind it is used within 
        `_menu_items_instructions` method."""
        self.text = self._entry_text(entry)
        self.safe_dismiss_menu()

    def on_menu_open(self, instance: Any) -> None:
        """Called when the menu is opened."""
        self.current_icon = self._menu_state_icon.get(
            self.current_icon, ICON.DD_MENU_OPEN)

    def on_menu_dismiss(self, instance: Any) -> None:
        """Called when the menu is dismissed."""
        self.current_icon = self._menu_state_icon.get(
            self.current_icon, ICON.DD_MENU_CLOSED)
    
    def on_current_icon(self, instance: Any, icon: str) -> None:
        """Fired when the `current_icon` property is set."""
    
    def safe_dismiss_menu(self) -> None:
        """Dismiss the menu if it is open."""
        if self.menu_is_open:
            self.menu.dismiss()
        