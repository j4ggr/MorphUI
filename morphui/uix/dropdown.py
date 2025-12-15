from typing import Any
from typing import Dict
from typing import List
from typing import Tuple

from kivy.properties import ListProperty
from kivy.properties import ObjectProperty

from morphui.uix.menu import MorphDropdownMenu
from morphui.uix.textfield import MorphTextField
from morphui.uix.textfield import MorphTextFieldOutlined
from morphui.uix.textfield import MorphTextFieldRounded
from morphui.uix.textfield import MorphTextFieldFilled


class MorphDropdownFilterField(MorphTextField):
    """A text field used for filtering items in a dropdown menu.

    Inherits from :class:`~morphui.uix.textfield.MorphTextField` and
    is designed to be used within dropdown menus to provide
    filtering capabilities.

    Examples
    --------
    Basic usage with a simple list of items:

    ```python
    from morphui.app import MorphApp
    from morphui.uix.boxlayout import MorphBoxLayout
    from morphui.uix.dropdown import MorphDropdownFilterField
    from morphui.uix.menu import MorphDropdownMenu

    class MyApp(MorphApp):
        def build(self):
            layout = MorphBoxLayout(orientation='vertical')
            
            # Create the dropdown menu
            menu = MorphDropdownMenu(
                items=[
                    {'text': 'Apple'},
                    {'text': 'Banana'},
                    {'text': 'Cherry'},
                    {'text': 'Date'},
                    {'text': 'Elderberry'},
                ])
            
            # Create the filter field linked to the menu
            filter_field = MorphDropdownFilterField(
                menu=menu,
                label_text='Select a fruit',
                trailing_icon='chevron-down')
            
            layout.add_widget(filter_field)
            return layout

    if __name__ == '__main__':
        MyApp().run()
    ```

    Advanced example - Icon picker with all available icons:

    ```python
    from morphui.app import MorphApp
    from morphui.uix.boxlayout import MorphBoxLayout
    from morphui.uix.dropdown import MorphDropdownFilterField
    from morphui.uix.menu import MorphDropdownMenu

    class IconPickerApp(MorphApp):
        def build(self):
            layout = MorphBoxLayout(orientation='vertical', padding=20, spacing=10)
            
            # Get all available icons from Typography
            icon_items = [
                {
                    'text': icon_name,
                    'leading_icon': icon_name,
                }
                for icon_name in sorted(self.typography.icon_map.keys())
            ]
            
            # Create the dropdown menu with icon items
            menu = MorphDropdownMenu(items=icon_items)
            
            # Set up callback to handle icon selection
            def on_icon_selected(item, index):
                filter_field.text = item.text
                filter_field.leading_icon = item.text
                menu.dismiss()
            
            menu.on_item_release = on_icon_selected
            
            # Create the filter field with icon preview
            filter_field = MorphDropdownFilterField(
                menu=menu,
                label_text='Search icons...',
                trailing_icon='magnify')
            
            layout.add_widget(filter_field)
            return layout

    if __name__ == '__main__':
        IconPickerApp().run()
    ```
    """

    menu_state_icons: List[str] = ListProperty(
        ['chevron-down', 'chevron-up'])
    """Icons for the dropdown filter field.

    This property holds a tuple of two strings representing the icons
    used for the dropdown filter field. The first icon is typically used
    to indicate the closed state, while the second icon indicates the
    open state.

    :attr:`icons` is a :class:`~kivy.properties.ListProperty` and
    defaults to `['chevron-down', 'chevron-up']`.
    """

    menu: MorphDropdownMenu = ObjectProperty(None)
    """The dropdown menu associated with this filter field.

    This property holds a reference to the :class:`MorphDropdownMenu`
    instance that is linked to this filter field.

    :attr:`menu` is a :class:`~kivy.properties.ObjectProperty` and
    defaults to `None`.
    """

    default_config: Dict[str, Any] = (
        MorphTextField.default_config.copy() | dict())
    """Default configuration for the MorphDropdownFilterField."""

    def __init__(self, **kwargs) -> None:
        menu = kwargs.pop('menu', 
            MorphDropdownMenu(
                caller=self,
                items=kwargs.pop('items', [])))
        super().__init__(menu=menu, **kwargs)
        self.bind(
            menu_state_icons=self._update_menu_state_icons,
            text=self._on_text_changed,
            focus=self._on_focus_changed,)
        self._update_menu_state_icons(self, self.menu_state_icons)
        self._on_text_changed(self, self.text)
        self._on_focus_changed(self, self.focus)
    
    def _update_menu_state_icons(
            self,
            instance: 'MorphDropdownFilterField',
            icons: List[str]) -> None:
        """Handle changes to the menu_state_icons property.

        This method is called whenever the menu_state_icons property
        changes. It updates the trailing widget's icons accordingly.

        Parameters
        ----------
        instance : MorphDropdownFilterField
            The instance of the filter field where the change occurred.
        icons : Tuple[str, str]
            The new tuple of icons for the filter field.
        
        Raises
        ------
        AssertionError
            If the provided icons list does not contain exactly two
            icon names.
        """
        assert len(icons) == 2, (
            "menu_state_icons must be a list of two icon names.")
        self.trailing_widget.normal_icon = icons[0]
        self.trailing_widget.active_icon = icons[1]
        
    def _on_text_changed(
            self,
            instance: 'MorphDropdownFilterField',
            text: str) -> None:
        """Handle changes to the text property.

        This method is called whenever the text in the filter field
        changes. It updates the associated dropdown menu's filter value
        accordingly.

        Parameters
        ----------
        instance : MorphDropdownFilterField
            The instance of the filter field where the change occurred.
        text : str
            The new text value of the filter field.
        """
        self.menu.filter_value = text
    
    def _on_focus_changed(
            self,
            instance: 'MorphDropdownFilterField',
            focused: bool) -> None:
        """Handle changes to the focus property.

        This method is called whenever the focus state of the filter
        field changes. It opens or closes the associated dropdown menu
        based on the focus state.

        Parameters
        ----------
        instance : MorphDropdownFilterField
            The instance of the filter field where the change occurred.
        focused : bool
            The new focus state of the filter field.
        """
        self.trailing_widget.active = focused
        if focused:
            self.menu.open()
        else:
            self.menu.dismiss()


class MorphDropdownFilterFieldOutlined(
    MorphDropdownFilterField):
    """An outlined text field used for filtering items in a dropdown 
    menu.

    Uses same default configuration as
    :class:`~morphui.uix.textfield.MorphTextFieldOutlined`
    """

    default_config: Dict[str, Any] = (
        MorphTextFieldOutlined.default_config.copy() | dict())
    """Default configuration for the
    :class:`MorphDropdownFilterFieldOutlined`."""


class MorphDropdownFilterFieldRounded(
    MorphDropdownFilterField):
    """A rounded text field used for filtering items in a dropdown 
    menu.

    Uses same default configuration as
    :class:`~morphui.uix.textfield.MorphTextFieldRounded`
    """

    default_config: Dict[str, Any] = (
        MorphTextFieldRounded.default_config.copy() | dict())
    """Default configuration for the
    :class:`MorphDropdownFilterFieldRounded`."""


class MorphDropdownFilterFieldFilled(
    MorphDropdownFilterField):
    """A filled text field used for filtering items in a dropdown 
    menu.

    Uses same default configuration as
    :class:`~morphui.uix.textfield.MorphTextFieldFilled`
    """

    default_config: Dict[str, Any] = (
        MorphTextFieldFilled.default_config.copy() | dict())
    """Default configuration for the
    :class:`MorphDropdownFilterFieldFilled`."""
