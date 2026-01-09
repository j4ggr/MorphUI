from kivy.properties import StringProperty

from morphui.uix.textfield import MorphTextField


class MorphDockedDatePickerField(MorphTextField):
    """A date picker text field designed to be used with a docked
    layout such as MorphDockedDatePicker.

    This text field integrates with a docked date picker layout to
    provide date selection functionality.
    """

    normal_trailing_icon: str = StringProperty('calendar')
    """Icon for the normal (closed) state of the dropdown filter field.

    This property holds the icon name used when the dropdown is in its
    normal (closed) state. Other possible values could be 'menu-down',
    'chevron-down', etc.

    :attr:`normal_trailing_icon` is a
    :class:`~kivy.properties.StringProperty` and defaults to
    `'chevron-down'`.
    """

    focus_trailing_icon: str = StringProperty('')
    """Icon for the focused (open) state of the dropdown filter field.

    This property holds the icon name used when the dropdown is in its
    focused (open) state. Other possible values could be 'menu-up',
    'chevron-up', etc.

    :attr:`focus_trailing_icon` is a
    :class:`~kivy.properties.StringProperty` and defaults to
    `''`.
    """

    def __init__(self, **kwargs) -> None:
        kwargs['trailing_icon'] = kwargs.get(
            'trailing_icon', self.normal_trailing_icon)
        super().__init__(**kwargs)
        self.bind(
            text=self._on_text_changed,
            focus=self._on_focus_changed,
            normal_trailing_icon=self.trailing_widget.setter('normal_icon'),
            focus_trailing_icon=self.trailing_widget.setter('focus_icon'),)
        self.trailing_widget.normal_icon = self.normal_trailing_icon
        self.trailing_widget.focus_icon = self.focus_trailing_icon
        self.trailing_widget.bind(
            on_release=self._on_trailing_release)
        self._on_text_changed(self, self.text)
        self._on_focus_changed(self, self.focus)

    def _on_text_changed(self, instance, value) -> None:
        """Handle changes to the text property.

        This method is called whenever the text in the text field
        changes. It can be used to validate or format the date input.
        """
        pass  # Implement date validation/formatting as needed

    def _on_focus_changed(self, instance, value) -> None:
        """Handle changes to the focus property.

        This method is called whenever the focus state of the text
        field changes. It can be used to open or close the date picker
        when the field gains or loses focus.
        """
        pass  # Implement focus handling as needed
