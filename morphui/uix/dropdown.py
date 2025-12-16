from typing import Any
from typing import Dict
from typing import List
from typing import Tuple

from kivy.properties import ListProperty
from kivy.properties import ObjectProperty

from morphui.uix.list import MorphFlatItemListView
from morphui.uix.behaviors import MorphMenuMotionBehavior
from morphui.uix.behaviors import MorphElevationBehavior
from morphui.uix.textfield import MorphTextField
from morphui.uix.textfield import MorphTextFieldOutlined
from morphui.uix.textfield import MorphTextFieldRounded
from morphui.uix.textfield import MorphTextFieldFilled


class MorphDropdownList(
        MorphElevationBehavior,
        MorphMenuMotionBehavior,
        MorphFlatItemListView):
    """A dropdown list widget that combines list view with menu motion.
    
    This widget extends MorphFlatItemListView with dropdown menu
    capabilities, including open/dismiss animations and elevation
    effects. It's designed to work seamlessly with 
    :class:`~morphui.uix.dropdown.MorphDropdownFilterField`.
    """
    
    default_config: Dict[str, Any] = (
        MorphFlatItemListView.default_config.copy() | dict(
            size_hint=(None, None),
            elevation=2,))
    """Default configuration for the MorphDropdownList widget."""


class MorphDropdownFilterField(MorphTextField):
    """A text field used for filtering items in a dropdown list.

    Inherits from :class:`~morphui.uix.textfield.MorphTextField` and
    is designed to be used within dropdown lists to provide
    filtering capabilities.

    Examples
    --------
    Basic usage with a simple list of items:

    ```python
    from morphui.app import MorphApp
    from morphui.uix.boxlayout import MorphBoxLayout
    from morphui.uix.dropdown import MorphDropdownFilterField

    class MyApp(MorphApp):
        def build(self):
            layout = MorphBoxLayout(orientation='vertical')
            
            # Create the filter field with items
            filter_field = MorphDropdownFilterField(
                items=[
                    {'text': 'Apple'},
                    {'text': 'Banana'},
                    {'text': 'Cherry'},
                    {'text': 'Date'},
                    {'text': 'Elderberry'},
                ],
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
            
            # Set up callback to handle icon selection
            def on_icon_selected(item, index):
                filter_field.text = item.text
                filter_field.leading_icon = item.text
                filter_field.dropdown.dismiss()
            
            # Create the filter field with icon items
            filter_field = MorphDropdownFilterField(
                items=icon_items,
                item_release_callback=on_icon_selected,
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

    This property holds a list of two strings representing the icons
    used for the dropdown filter field. The first icon is typically used
    to indicate the closed state, while the second icon indicates the
    open state.

    :attr:`menu_state_icons` is a :class:`~kivy.properties.ListProperty` and
    defaults to `['chevron-down', 'chevron-up']`.
    """

    dropdown: MorphDropdownList = ObjectProperty(None)
    """The dropdown list associated with this filter field.

    This property holds a reference to the :class:`MorphDropdownList`
    instance that is linked to this filter field.

    :attr:`dropdown` is a :class:`~kivy.properties.ObjectProperty` and
    defaults to `None`.
    """

    default_config: Dict[str, Any] = (
        MorphTextField.default_config.copy() | dict())
    """Default configuration for the MorphDropdownFilterField."""

    def __init__(self, **kwargs) -> None:
        dropdown = MorphDropdownList(
            caller=self,
            items=kwargs.pop('items', []),
            item_release_callback=kwargs.pop('item_release_callback', None))
        super().__init__(dropdown=dropdown, **kwargs)
        self.bind(
            menu_state_icons=self._update_menu_state_icons,
            text=self._on_text_changed,
            focus=self._on_focus_changed,
            width=self.dropdown.setter('width'))
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
        changes. It updates the associated dropdown list's filter value
        accordingly.

        Parameters
        ----------
        instance : MorphDropdownFilterField
            The instance of the filter field where the change occurred.
        text : str
            The new text value of the filter field.
        """
        full_texts = [item['label_text'] for item in self.dropdown._source_items]    
        self.dropdown.filter_value = '' if text in full_texts else text
    
    def _on_focus_changed(
            self,
            instance: 'MorphDropdownFilterField',
            focused: bool) -> None:
        """Handle changes to the focus property.

        This method is called whenever the focus state of the filter
        field changes. It opens or closes the associated dropdown list
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
            self.dropdown.open()
        else:
            self.dropdown.dismiss()


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
