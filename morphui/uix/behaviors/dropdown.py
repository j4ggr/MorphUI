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
    'MorphDropdownBehavior',]


class MorphDropdownBehavior:
    """This is a base class used for opening a Dropdown Menu with a list 
    of items.
    
    The items can be of any type, but must
    be convertible to string via the `_item_text` method. The
    dropdown menu is opened when the `open_menu` method is called.
    """

    items: List[Any] = ListProperty([])
    """List of items to show in the dropdown menu"""

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

    item_viewclass: str = StringProperty('OneLineListItem')
    """The viewclass to use for the recycled items in the dropdown menu."""

    @property
    def menu_is_open(self) -> bool:
        """True if the dropdown menu is open (read-only)."""
        if not self.menu:
            return False
        return bool(self.menu.parent)
    
    def item_contains_text(self, item: Any, text: str) -> bool:
        """Check if the text is in the provided item."""
        item_text = self._item_text(item)
        return text.lower() in item_text.lower()

    def items_contains_text(self, text: str) -> bool:
        """Check if the text is in any of the items."""
        return any(self._item_text(e) == text for e in self.items)

    def _item_text(self, item: Any) -> str:
        """Get the text for a given item."""
        if isinstance(item, str):
            return item
        elif isinstance(item, dict):
            return str(item.get('text', ''))
        elif hasattr(item, 'text'):
            return str(item.text)
        else:
            raise ValueError(
                'Item must be of type str, dict with a "text" key, or '
                'have a text attribute')

    def _menu_item_instruction(self, item: Any) -> Dict[str, Any]:
        """Convert an item to a menu item instruction as expected from
        :attr:`items` property of the :class:`MorphDropdownMenu`.
        Override this method if you want to change the way items are
        converted to menu item instructions.

        It creates a dictionary with 'viewclass', 'on_release' and 
        'text' keys, where 'viewclass' is the :attr:`item_viewclass`, 
        'on_release' is a callback to :meth:`item_callback` method and
        'text' is the string representation of the item. If the item has
        an 'instruction' attribute (which should be a dictionary), it 
        merges that dictionary into the resulting instruction.
        
        Parameters
        ----------
        item : Any 
            The item to convert to a menu item instruction. It can be
            a string, a dictionary with a 'text' key, or an object
            with a 'text' attribute.

        Returns
        -------
        Dict[str, Any]:
            A dictionary representing the menu item instruction."""
        instruction = {
                'viewclass': self.item_viewclass,
                'on_release': lambda x=item: self.item_callback(x),
                'text': self._item_text(item),
            } | getattr(item, 'instruction', {})
        return instruction
    
    def get_menu_item_instructions(self) -> List[Dict[str, Any]]:
        """Get the menu items instructions from the items. Override 
        this method if you want to change the way items are converted
        to menu item instructions. You can also override the
        :meth:`_menu_item_instruction` method.
        
        Returns
        -------
        List[Dict[str, Any]]:
            A list of dictionaries representing the menu item
            instructions."""
        return list(map(self._menu_item_instruction, self.items))

    def on_menu(self, instance: Any, menu: Any) -> None:
        """Called when the menu property is set. Binds the on_dismiss 
        event.

        Parameters
        ----------
        instance : Any
            The instance of the dropdown menu.
        menu : Any
            The menu that was opened.
        
        Raises
        ------
        AssertionError
            If the menu does not have the required methods and 
            properties.
        """
        if menu:
            assert hasattr(menu, 'bind'), (
                'menu must have a bind method to bind on_dismiss event.')
            assert hasattr(menu, 'dismiss'), (
                'menu must have a dismiss method to close the menu.')
            assert hasattr(menu, 'open'), (
                'menu must have an open method to open the menu.')
            assert hasattr(menu, 'data'), (
                'menu must have a data property to set the recycled items.')
            menu.bind(on_dismiss=self.on_menu_dismiss)
    
    def open_menu(self, *args) -> None:
        """Open the dropdown menu. Sets the menu items from the
        :attr:`items` property using the 
        :meth:`get_menu_item_instructions` method. If the menu is
        already open or there are no items, it does nothing."""
        if not self.items or not self.menu or self.menu_is_open:
            return
        
        self.menu.data = self.get_menu_item_instructions()
        Clock.schedule_once(lambda dt: self.menu.open(), self.menu_open_delay)
        self.on_menu_open(self.menu)
        
    def item_callback(self, item: Any) -> None:
        """Fired when an item is selected from the dropdown menu. Set
        the text field's text to the selected item. You can override
        this method, but keep in mind it is set to each item within
        :meth:`_menu_items_instructions` method."""
        self.text = self._item_text(item)
        self.safe_dismiss_menu()

    def on_menu_open(self, instance: Any) -> None:
        """Called when the menu is opened. Sets the current icon
        to the open state."""
        self.current_icon = self._menu_state_icon.get(
            self.current_icon, ICON.DD_MENU_OPEN)

    def on_menu_dismiss(self, instance: Any) -> None:
        """Called when the menu is dismissed. Sets the current icon
        to the closed state."""
        self.current_icon = self._menu_state_icon.get(
            self.current_icon, ICON.DD_MENU_CLOSED)
    
    def on_current_icon(self, instance: Any, icon: str) -> None:
        """Fired when the `current_icon` property is set. Override
        this method if you want to customize the behavior."""
    
    def safe_dismiss_menu(self) -> None:
        """Dismiss the menu if it is open."""
        if self.menu_is_open:
            self.menu.dismiss()
        