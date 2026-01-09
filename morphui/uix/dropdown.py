from textwrap import dedent

from typing import Any
from typing import Dict

from kivy.lang import Builder
from kivy.properties import DictProperty
from kivy.properties import StringProperty
from kivy.properties import ObjectProperty

from morphui.uix.list import BaseListView
from morphui.uix.list import MorphListLayout # noqa F401
from morphui.uix.list import MorphListItemFlat
from morphui.uix.behaviors import MorphElevationBehavior
from morphui.uix.behaviors import MorphMenuMotionBehavior
from morphui.uix.behaviors import MorphSizeBoundsBehavior
from morphui.uix.textfield import MorphTextField
from morphui.uix.textfield import MorphTextFieldFilled
from morphui.uix.textfield import MorphTextFieldRounded
from morphui.uix.textfield import MorphTextFieldOutlined


class MorphDropdownList(
        MorphSizeBoundsBehavior,
        MorphElevationBehavior,
        MorphMenuMotionBehavior,
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
    
    default_config: Dict[str, Any] = (
        BaseListView.default_config.copy() | dict(
            size_lower_bound=(150, 100),
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

    normal_trailing_icon: str = StringProperty('chevron-down')
    """Icon for the normal (closed) state of the dropdown filter field.

    This property holds the icon name used when the dropdown is in its
    normal (closed) state.

    :attr:`normal_trailing_icon` is a
    :class:`~kivy.properties.StringProperty` and defaults to
    `'chevron-down'`.
    """

    focus_trailing_icon: str = StringProperty('chevron-up')
    """Icon for the focused (open) state of the dropdown filter field.

    This property holds the icon name used when the dropdown is in its
    focused (open) state.

    :attr:`focus_trailing_icon` is a
    :class:`~kivy.properties.StringProperty` and defaults to
    `'chevron-up'`.
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
        kwargs['trailing_icon'] = kwargs.get(
            'trailing_icon', self.normal_trailing_icon)
        super().__init__(dropdown=dropdown, **kwargs)
        self.bind(
            text=self._on_text_changed,
            focus=self._on_focus_changed,
            width=self.dropdown.setter('width'),
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
        full_texts = [
            item['label_text'] for item in self.dropdown._source_items]    
        self.dropdown.filter_value = '' if text in full_texts else text
    
    def _on_focus_changed(
            self,
            instance: 'MorphDropdownFilterField',
            focus: bool) -> None:
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
            self.dropdown.open()
        else:
            self.dropdown.dismiss()
    
    def _on_trailing_release(self, *args) -> None:
        """Handle the release event of the trailing widget.

        This method is called when the trailing widget (typically an
        icon button) is released. If the dropdown is not open, it sets
        focus to the filter field, thereby opening the dropdown.
        Otherwise, it does nothing.
        """
        if not self.dropdown.is_open:
            self.focus = True


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
