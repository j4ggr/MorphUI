from textwrap import dedent

from typing import Any
from typing import List
from typing import Dict
from typing import Literal

from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import DictProperty
from kivy.properties import AliasProperty
from kivy.properties import StringProperty
from kivy.properties import ObjectProperty

from morphui.uix.list import BaseListView
from morphui.uix.list import MorphListLayout # noqa F401
from morphui.uix.list import MorphListItemFlat
from morphui.uix.button import MorphTextIconButton
from morphui.uix.boxlayout import MorphElevationBoxLayout
from morphui.uix.behaviors import MorphToggleButtonBehavior
from morphui.uix.behaviors import MorphMenuMotionBehavior
from morphui.uix.behaviors import MorphSizeBoundsBehavior
from morphui.uix.behaviors import MorphRoundSidesBehavior

from morphui.uix.textfield import MorphTextField
from morphui.uix.textfield import MorphTextFieldFilled
from morphui.uix.textfield import MorphTextFieldRounded
from morphui.uix.textfield import MorphTextFieldOutlined


__all__ = [
    'MorphDropdownList',
    'MorphDropdownMenu',
    'MorphDropdownFilterField',
    'MorphDropdownFilterFieldOutlined',
    'MorphDropdownFilterFieldRounded',
    'MorphDropdownFilterFieldFilled',
    ]


class MorphDropdownList(
        BaseListView):
    """A dropdown list widget that combines list view with menu motion.
    
    This widget extends :class:`~morphui.uix.list.BaseListView` with
    dropdown menu capabilities, including open/dismiss animations and
    elevation effects. It's designed to work seamlessly with 
    :class:`~morphui.uix.dropdown.MorphDropdownFilterField`.
    """
    
    Builder.load_string(dedent('''
        <MorphDropdownList>:
            viewclass: 'MorphListItemFlat'
            MorphListLayout:
        '''))

    default_data: Dict[str, Any] = DictProperty(
        MorphListItemFlat.default_config.copy() | {
        'leading_icon': '',
        'trailing_icon': '',
        'label_text': '',
        })
    
    def _clear_focus(self) -> None:
        """Clear focus from all child items in the list.
        
        This method sets the `focus` property of all child items to
        `False`."""
        for child in self.layout_manager.children:
            child.focus = False

    def _clear_hover(self) -> None:
        """Clear hover state from all child items in the list.
        
        This method sets the `hovered` property of all child items to
        `False`."""
        for child in self.layout_manager.children:
            child.hovered = False

    def set_focus_by_text(self, text: str) -> None:
        """Set focus to the child item with the specified label text.

        Parameters
        ----------
        text : str
            The label text of the item to focus.
        """
        children = self.layout_manager.children
        n_children = len(children)
        if n_children == 0:
            return
        
        for child in children:
            if child.label_text == text:
                self._clear_focus()
                child.focus = True
                return
    
    def set_neighbor_focus(
            self,
            current_focus_child: Any,
            direction: Literal['up', 'down']
            ) -> None:
        """Set focus to the neighboring child item in the specified
        direction.

        Parameters
        ----------
        current_focus_child : Any
            The currently focused child item.
        direction : Literal['up', 'down']
            The direction to move focus, either 'up' or 'down'.
        """
        children = self.layout_manager.children
        n_children = len(children)
        if n_children == 0:
            return
        
        n_children_after = 0
        delta_y = float('inf')
        ref_y = current_focus_child.y
        new_child = current_focus_child
        for child in children:
            _dy = child.y - ref_y if direction == 'up' else ref_y - child.y
            if _dy <= 0 or _dy >= delta_y:
                continue
            
            n_children_after += 1
            delta_y = _dy
            new_child = child

        self._clear_focus()
        new_child.focus = True
        if n_children_after <= 2:
            self.scroll_by_item(direction, 2 - n_children_after)

    def scroll_by_item(
            self,
            direction: Literal['up', 'down'],
            n_items: int
            ) -> None:
        """Scroll the list by the specified number of items in the given
        direction.

        Parameters
        ----------
        direction : Literal['up', 'down']
            The direction to scroll, either 'up' or 'down'.
        n_items : int
            The number of items to scroll by.
        """
        total_items = len(self.data)
        if total_items == 0:
            return
        
        delta = n_items / total_items
        if direction == 'up':
            self.scroll_y = min(1, self.scroll_y + delta)
        elif direction == 'down':
            self.scroll_y = max(0, self.scroll_y - delta)
    
    def on_arrow_down_press(self) -> None:
        """Handle the arrow down key press event.

        This method is called when the arrow down key is pressed.
        It moves the focus to the next item in the list.
        """
        children = self.layout_manager.children
        n_children = len(children)
        total_items = len(self.data)
        if n_children == 0:
            return
        
        focused_child = next((c for c in children if c.focus), None)
        if focused_child is None or n_children == 1 or total_items == 1:
            children[-1].focus = True
            return
        
        self.set_neighbor_focus(focused_child, 'down')

    def on_arrow_up_press(self) -> None:
        """Handle the arrow up key press event.

        This method is called when the arrow up key is pressed.
        It moves the focus to the previous item in the list.
        """
        children = self.layout_manager.children
        n_children = len(children)
        total_items = len(self.data)
        if n_children == 0:
            return
        
        focused_child = next((c for c in children if c.focus), None)
        if focused_child is None or n_children == 1 or total_items == 1:
            children[0].focus = True
            return
        
        self.set_neighbor_focus(focused_child, 'up')
    
    def on_enter_press(self) -> None:
        """Handle the enter key press event.

        This method is called when the enter key is pressed.
        It triggers the release action on the currently focused item.
        """
        children = self.layout_manager.children
        if not children:
            return
        
        if not self.parent.is_open:
            return
        
        for child in children[::-1]:
            if child.focus:
                child.trigger_action()
                return


class MorphDropdownMenu(
        MorphMenuMotionBehavior,
        MorphSizeBoundsBehavior,
        MorphElevationBoxLayout,):
    """A base dropdown menu class with color theme, surface layer,
    elevation, and menu motion behaviors.
    """

    dropdown_list: MorphDropdownList = ObjectProperty(None)
    """The dropdown list associated with this menu.

    This property holds a reference to the :class:`MorphDropdownList`
    instance that is linked to this filter field.

    :attr:`dropdown` is a :class:`~kivy.properties.ObjectProperty` and
    defaults to `None`.
    """
    
    items: List[Dict[str, Any]] = AliasProperty(
        lambda self: self.dropdown_list._get_items(),
        lambda self, items: self.dropdown_list._set_items(items),)
    """The list of items in the dropdown menu.

    This property provides access to the items displayed in the
    dropdown list. It allows getting and setting the list of items.

    :attr:`items` is a :class:`~kivy.properties.AliasProperty`.
    """
    
    item_release_callback: Any = AliasProperty(
        lambda self: self.dropdown_list.item_release_callback,
        lambda self, callback: setattr(
            self.dropdown_list, 'item_release_callback', callback),)
    """Callback function for item release events.

    This property allows getting and setting the callback function that
    is called when an item in the dropdown list is released.

    :attr:`items_release_callback` is a
    :class:`~kivy.properties.AliasProperty`.
    """

    layout_manager: MorphListLayout = ObjectProperty(None)
    """The layout manager for the dropdown list.

    This property holds a reference to the layout manager used by the
    dropdown list to arrange its items. It is set during initialization.

    :attr:`layout_manager` is a :class:`~kivy.properties.ObjectProperty`
    and defaults to `None`.
    """
    
    default_config: Dict[str, Any] = dict(
            theme_color_bindings=dict(
                normal_surface_color='surface_container_highest_color',),
            size_lower_bound=(150, 100),
            size_hint=(None, None),
            radius=[0, 0, dp(8), dp(8)],
            padding=dp(8),
            elevation=2,
            same_width_as_caller=True,)
    """Default configuration for the MorphDropdownMenu."""
    
    def __init__(self, **kwargs) -> None:
        self.dropdown_list = MorphDropdownList()
        super().__init__(**kwargs)
        self.layout_manager = self.dropdown_list.layout_manager
        self.add_widget(self.dropdown_list)
        self.bind(is_open=self.dropdown_list.setter('key_press_enabled'))
        self.key_press_enabled = self.is_open

    def _update_caller_bindings(self, *args) -> None:
        """Update bindings to the caller button's position and size.

        This method binds to the caller button's `pos` and `size`
        properties to adjust the tooltip position whenever the caller
        changes. If there is no caller set, it does nothing.
        """
        if self.caller is None:
            return
        
        super()._update_caller_bindings()
        self.caller.bind(
            focus=lambda _, focus: setattr(self, 'dismiss_allowed', not focus))
    
    def on_pre_open(self, *args) -> None:
        """Handle actions before the dropdown menu opens.

        This method is called just before the dropdown menu is opened.
        It sets the focus in the dropdown list based on the caller's
        current text value.
        """
        text = getattr(self.caller, 'text', '')
        if text in self.dropdown_list.available_texts:
            self.dropdown_list.set_focus_by_text(text)
        self.dropdown_list.refresh_from_data()
    
    def on_pre_dismiss(self, *args) -> None:
        """Handle actions before the dropdown menu is dismissed.

        This method is called just before the dropdown menu is
        dismissed. It refreshes the dropdown list to ensure that any 
        changes made while the dropdown was open are reflected when it 
        is opened again.
        """
        self.dropdown_list.refresh_from_data()

    def on_dismiss(self, *args) -> None:
        """Handle actions after the dropdown menu is dismissed.

        This method is called just after the dropdown menu is
        dismissed. It clears the focus and hover states from all items
        in the dropdown list.
        """
        self.dropdown_list._clear_focus()
        self.dropdown_list._clear_hover()


class MorphDropdownSelect(
        MorphToggleButtonBehavior,
        MorphTextIconButton):
    """This is a simple dropdown select button that can be used to 
    trigger a dropdown menu.

    This button displays an icon that changes depending on whether
    the dropdown menu is open or closed. It is designed to work with
    :class:`~morphui.uix.dropdown.MorphDropdownMenu`.

    Examples
    --------
    Basic usage with a simple list of items:

    ```python
    from morphui.app import MorphApp
    from morphui.uix.floatlayout import MorphFloatLayout
    from morphui.uix.dropdown import MorphDropdownSelect

    class MyApp(MorphApp):
    
        def build(self) -> MorphFloatLayout:
            self.theme_manager.theme_mode = 'Dark'
            self.theme_manager.seed_color = 'morphui_teal'
            layout = MorphFloatLayout(
                MorphDropdownSelect(
                    identity='dropdown_button',
                    items=[
                        {'label_text': f'Item {i}'} for i in range(10)],
                    pos_hint={'center_x': 0.5, 'center_y': 0.9},))
            self.dropdown_button = layout.identities.dropdown_button
            return layout

    if __name__ == '__main__':
        MyApp().run()
    ```
    """

    normal_icon: str = StringProperty('menu-down')
    """Icon for the normal (closed) state of the dropdown filter field.

    This property holds the icon name used when the dropdown is in its
    normal (closed) state.

    :attr:`normal_icon` is a
    :class:`~kivy.properties.StringProperty` and defaults to
    `'menu-down'`.
    """

    active_icon: str | None  = StringProperty('menu-up')
    """Icon for the focused (open) state of the dropdown filter field.

    This property holds the icon name used when the dropdown is in its
    focused (open) state.
    
    :attr:`active_icon` is a
    :class:`~kivy.properties.StringProperty` and defaults to
    `'menu-up'`.
    """

    dropdown_menu: MorphDropdownMenu = ObjectProperty(None)
    """The dropdown menu associated with this filter field.

    This property holds a reference to the :class:`MorphDropdownMenu`
    instance that is linked to this filter field.

    :attr:`dropdown_menu` is a :class:`~kivy.properties.ObjectProperty` and
    defaults to `None`.
    """

    default_config = (
        MorphTextIconButton.default_config.copy() | dict(
        auto_size=(False, True),
        size_hint_x=None,
        width=dp(200),))

    def __init__(self, kw_dropdown: Dict[str, Any] = {}, **kwargs) -> None:
        self.register_event_type('on_item_release')
        kw_dropdown = dict(
            caller=self,
            items=kwargs.pop('items', []),
            item_release_callback=kwargs.pop(
                'item_release_callback',
                lambda item, index: self.dispatch('on_item_release', item, index))
                ) | kw_dropdown
        self.dropdown_menu = MorphDropdownMenu(**kw_dropdown)
        super().__init__(**kwargs)
        self.label_widget.auto_width = False
        self.dropdown_menu.bind(is_open=self.setter('active'))
        self.bind(active=self._toggle_menu_on_active)

    def _toggle_menu_on_active(self, *args) -> None:
        """Toggle the dropdown menu when the button's active state 
        changes.
        
        This method is called whenever the `active` property of the
        button changes. If the button becomes active, it opens the
        dropdown menu. If the button becomes inactive, it dismisses the
        dropdown menu."""
        if self.active:
            self.dropdown_menu.open()
            self.dropdown_menu.dismiss_allowed = True
        else:
            self.dropdown_menu.dismiss()

    def on_item_release(
            self,
            item: Any,
            index: int) -> None:
        """Event handler for item release events.

        This method is called when an item in the dropdown list is
        released. It can be overridden to provide custom behavior when
        an item is selected.

        Parameters
        ----------
        item : Any
            The item that was released.
        index : int
            The index of the released item in the dropdown list.
        
        Notes
        -----
        This method is not called if an `item_release_callback` is 
        provided during initialization.
        """
        self.label_text = getattr(
            item, 'label_text', getattr(item, 'text', str(item)))
        self.trigger_action()


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
    from morphui.uix.floatlayout import MorphFloatLayout
    from morphui.uix.dropdown import MorphDropdownFilterField

    class MyApp(MorphApp):
        def build(self) -> MorphFloatLayout:
            self.theme_manager.theme_mode = 'Dark'
            self.theme_manager.seed_color = 'morphui_teal'
            icon_items = [
                {
                    'label_text': icon_name,
                    'leading_icon': icon_name,}
                for icon_name in sorted(self.typography.icon_map.keys())]
            layout = MorphFloatLayout(
                MorphDropdownFilterField(
                    identity='icon_picker',
                    items=icon_items,
                    item_release_callback=self.icon_selected_callback,
                    label_text='Search icons...',
                    leading_icon='magnify',
                    pos_hint={'center_x': 0.5, 'center_y': 0.9},
                    size_hint=(0.8, None),))
            self.icon_picker = layout.identities.icon_picker
            return layout

        def icon_selected_callback(self, item, index):
            self.icon_picker.text = item.label_text
            self.icon_picker.leading_icon = item.label_text

    if __name__ == '__main__':
        MyApp().run()
    ```

    Advanced example - Icon picker with all available icons:

    ```python
    from morphui.app import MorphApp
    from morphui.uix.floatlayout import MorphFloatLayout
    from morphui.uix.dropdown import MorphDropdownFilterField

    class MyApp(MorphApp):
        def build(self) -> MorphFloatLayout:
            self.theme_manager.theme_mode = 'Dark'
            self.theme_manager.seed_color = 'morphui_teal'
            icon_items = [
                {
                    'label_text': icon_name,
                    'leading_icon': icon_name,}
                for icon_name in sorted(self.typography.icon_map.keys())]
            layout = MorphFloatLayout(
                MorphDropdownFilterField(
                    identity='icon_picker',
                    items=icon_items,
                    item_release_callback=self.icon_selected_callback,
                    label_text='Search icons...',
                    trailing_icon='magnify',
                    pos_hint={'center_x': 0.5, 'center_y': 0.9},
                    size_hint=(0.8, None),))
            self.icon_picker = layout.identities.icon_picker
            return layout

        def icon_selected_callback(self, item, index):
            self.icon_picker.text = item.label_text
            self.icon_picker.leading_icon = item.label_text
            self.icon_picker.dropdown.dismiss()

    if __name__ == '__main__':
        MyApp().run()
    ```
    """

    normal_trailing_icon: str = StringProperty('menu-down')
    """Icon for the normal (closed) state of the dropdown filter field.

    This property holds the icon name used when the dropdown is in its
    normal (closed) state.

    :attr:`normal_trailing_icon` is a
    :class:`~kivy.properties.StringProperty` and defaults to
    `'menu-down'`.
    """

    focus_trailing_icon: str = StringProperty('menu-up')
    """Icon for the focused (open) state of the dropdown filter field.

    This property holds the icon name used when the dropdown is in its
    focused (open) state.

    :attr:`focus_trailing_icon` is a
    :class:`~kivy.properties.StringProperty` and defaults to
    `'menu-up'`.
    """

    dropdown_menu: MorphDropdownMenu = ObjectProperty(None)
    """The dropdown menu associated with this filter field.

    This property holds a reference to the :class:`MorphDropdownMenu`
    instance that is linked to this filter field.

    :attr:`dropdown_menu` is a :class:`~kivy.properties.ObjectProperty` and
    defaults to `None`.
    """

    default_config: Dict[str, Any] = (
        MorphTextField.default_config.copy() | dict())
    """Default configuration for the MorphDropdownFilterField."""

    def __init__(self, kw_dropdown: Dict[str, Any] = {}, **kwargs) -> None:
        self.register_event_type('on_item_release')
        kw_dropdown = dict(
            caller=self,
            items=kwargs.pop('items', []),
            item_release_callback=kwargs.pop(
                'item_release_callback',
                lambda item, index: self.dispatch('on_item_release', item, index))
                ) | kw_dropdown
        self.dropdown_menu = MorphDropdownMenu(**kw_dropdown)
        kwargs['trailing_icon'] = kwargs.get(
            'trailing_icon', self.normal_trailing_icon)
        super().__init__(**kwargs)
        self.bind(
            text=self._on_text_changed,
            focus=self._on_focus_changed,
            width=self.dropdown_menu.setter('width'),
            normal_trailing_icon=self.trailing_widget.setter('normal_icon'),
            focus_trailing_icon=self.trailing_widget.setter('focus_icon'),)
        self.trailing_widget.normal_icon = self.normal_trailing_icon
        self.trailing_widget.focus_icon = self.focus_trailing_icon
        self.trailing_widget.bind(
            on_release=self._on_trailing_release)
        self._on_text_changed(self, self.text)
        self._on_focus_changed(self, self.focus)
        
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
        items = self.dropdown_menu.dropdown_list._source_items
        full_texts = [item['label_text'] for item in items]
        filter_value = '' if text in full_texts else text.strip()
        self.dropdown_menu.dropdown_list.filter_value = filter_value
    
    def _on_focus_changed(
            self,
            instance: 'MorphDropdownFilterField',
            focus: bool
            ) -> None:
        """Handle changes to the focus property.

        This method is called whenever the focus state of the filter
        field changes. It opens or closes the associated dropdown list
        based on the focus state.
-
        Parameters
        ----------
        instance : MorphDropdownFilterField
            The instance of the filter field where the change occurred.
        focus : bool
            The new focus state of the filter field.
        """
        self.trailing_widget.focus = focus
        if focus:
            self.dropdown_menu.open()
        else:
            self.dropdown_menu.dismiss()
    
    def _on_trailing_release(self, *args) -> None:
        """Handle the release event of the trailing widget.

        This method is called when the trailing widget (typically an
        icon button) is released. If the dropdown is not open, it sets
        focus to the filter field, thereby opening the dropdown.
        Otherwise, it does nothing.
        """
        if not self.dropdown_menu.is_open:
            self.focus = True

    def on_item_release(
            self,
            item: Any,
            index: int) -> None:
        """Event handler for item release events.

        This method is called when an item in the dropdown list is
        released. It can be overridden to provide custom behavior when
        an item is selected.

        Parameters
        ----------
        item : Any
            The item that was released.
        index : int
            The index of the released item in the dropdown list.
        
        Notes
        -----
        This method is not called if an `item_release_callback` is 
        provided during initialization.
        """
        pass


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
        MorphRoundSidesBehavior,
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
