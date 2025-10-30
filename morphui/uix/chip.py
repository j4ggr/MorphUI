from typing import Any
from typing import Dict

from kivy.metrics import dp
from kivy.properties import ObjectProperty
from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout

from morphui.utils import clean_config
from morphui.constants import NAME

from morphui.uix.behaviors import MorphHoverBehavior
from morphui.uix.behaviors import MorphRippleBehavior
from morphui.uix.behaviors import MorphButtonBehavior
from morphui.uix.behaviors import MorphElevationBehavior
from morphui.uix.behaviors import MorphAutoSizingBehavior
from morphui.uix.behaviors import MorphColorThemeBehavior
from morphui.uix.behaviors import MorphRoundSidesBehavior
from morphui.uix.behaviors import MorphSurfaceLayerBehavior
from morphui.uix.behaviors import MorphIdentificationBehavior
from morphui.uix.behaviors import MorphInteractionLayerBehavior

from morphui.uix.label import MorphSimpleLabel
from morphui.uix.label import MorphSimpleIconLabel
from morphui.uix.button import MorphSimpleIconButton


__all__ = [
    'ChipLeadingIconLabel',
    'ChipTextLabel',
    'ChipTrailingIconButton',
    'MorphChip',]


class ChipLeadingIconLabel(MorphSimpleIconLabel):
    
    default_config: Dict[str, Any] = (
        MorphSimpleIconLabel.default_config.copy() | dict(
        auto_size=True,
        padding=dp(0),))


class ChipTextLabel(MorphSimpleLabel):

    default_config: Dict[str, Any] = (
        MorphSimpleLabel.default_config.copy() | dict(
        auto_size=True,
        padding=dp(0),))


class ChipTrailingIconButton(MorphSimpleIconButton):

    default_config: Dict[str, Any] = (
        MorphSimpleIconButton.default_config.copy() | dict(
            auto_size=True,
            padding=dp(0),))


class MorphChip(
        MorphIdentificationBehavior,
        MorphAutoSizingBehavior,
        MorphHoverBehavior,
        MorphRippleBehavior,
        MorphButtonBehavior,
        MorphColorThemeBehavior,
        MorphRoundSidesBehavior,
        MorphInteractionLayerBehavior,
        MorphSurfaceLayerBehavior,
        MorphElevationBehavior,
        BoxLayout,):
    """Morph Chip component.

    A chip is a compact element that represents an input, attribute, 
    or action. Chips can contain a leading icon, text, and a trailing 
    icon. They are typically used for filtering, assisting, input and
    suggestions.

    Use the `leading_icon` and `trailing_icon` properties to add
    icons to the chip. The `text` property is used to set the text
    of the chip.

    Example
    -------
    ````python
    from morphui.app import MorphApp
    from morphui.uix.chip import MorphChip
    from morphui.uix.floatlayout import MorphFloatLayout

    class MyApp(MorphApp):
        def build(self) -> MorphFloatLayout:
            self.theme_manager.switch_to_dark()
            return MorphFloatLayout(
                MorphChip(
                    identity='my_widget',
                    leading_icon='language-python',),
                surface_color=self.theme_manager.surface_color,)

    if __name__ == '__main__':
        MyApp().run()
    """

    leading_icon: str = StringProperty('')
    """The name of the leading icon displayed to the left of the chip 
    text.

    This property represents the leading icon of the chip. If set,
    the `leading_widget` will display the specified icon.

    :attr:`leading_icon` is a :class:`~kivy.properties.StringProperty`
    and defaults to an empty string.
    """

    label_text: str = StringProperty('')
    """The text displayed in the center of the chip.

    This property represents the text label of the chip.

    :attr:`label_text` is a :class:`~kivy.properties.StringProperty`
    and defaults to an empty string.
    """

    trailing_icon: str = StringProperty('')
    """The name of the trailing icon displayed to the right of the chip
    text.

    This property represents the trailing icon of the chip. If set,
    the `trailing_widget` will display the specified icon.

    :attr:`trailing_icon` is a :class:`~kivy.properties.StringProperty`
    and defaults to an empty string.
    """

    leading_widget: ChipLeadingIconLabel = ObjectProperty()
    """The leading icon widget displayed to the left of the chip text.
    
    This widget represents the leading icon of the chip. If not
    provided, it is automatically created based on the `leading_icon`
    property.

    :attr:`leading_widget` is by default an instance of
    :class:`~morphui.uix.chip.ChipLeadingIconLabel`."""

    label_widget: ChipTextLabel = ObjectProperty(None)
    """The text label widget displayed in the center of the chip.

    This widget represents the text label of the chip. If not
    provided, it is automatically created.

    :attr:`label_widget` is by default an instance of
    :class:`~morphui.uix.chip.ChipTextLabel`."""

    trailing_widget: ChipTrailingIconButton = ObjectProperty(None)
    """The trailing icon button widget displayed to the right of the
    chip text.

    This widget represents the trailing icon button of the chip. If not
    provided, it is automatically created based on the `trailing_icon`
    property.

    :attr:`trailing_widget` is by default an instance of
    :class:`~morphui.uix.chip.ChipTrailingIconButton`."""

    default_config: Dict[str, Any] = dict(
        theme_color_bindings=dict(
            surface_color='transparent_color',
            border_color='outline_variant_color',),
        orientation='horizontal',
        auto_size=True,
        padding=dp(8),
        spacing=dp(8),
        radius=dp(8),
        round_sides=False,)
    """Default configuration for the :class:`MorphChip` component."""
    
    def __init__(self, **kwargs) -> None:
        child_classes = dict(
            leading_widget=ChipLeadingIconLabel,
            label_widget=ChipTextLabel,
            trailing_widget=ChipTrailingIconButton,)
        
        config = clean_config(self.default_config, kwargs)
        for attr, cls in child_classes.items():
            if attr not in config:
                config[attr] = cls()

        super().__init__(**config)
        self.add_widget(self.leading_widget)
        self.add_widget(self.label_widget)
        self.add_widget(self.trailing_widget)

        self.fbind(
            'leading_icon',
            self._update_child_widget,
            identity=NAME.LEADING_WIDGET)
        self.fbind(
            'label_text',
            self._update_child_widget,
            identity=NAME.LABEL_WIDGET)
        self.fbind(
            'trailing_icon',
            self._update_child_widget,
            identity=NAME.TRAILING_WIDGET)
        
        self.refresh_chip_content()

    # TODO: Refactor to reduce code duplication with other components (e.g. TextField)
    def _update_child_widget(
            self, instance: Any, text: str, identity: str) -> None:
        """Update the child widget based on the provided text and identity.

        This method is responsible for updating the content of the
        child widget identified by the `identity` parameter with the
        new `text` value.

        Parameters
        ----------
        instance : Any
            The instance of the child widget to update.
        text : str
            The new text content to set for the child widget.
        identity : str
            The identity of the child widget to update (e.g., "label",
            "leading_icon", "trailing_icon").
        """
        match identity:
            case NAME.LABEL_WIDGET:
                widget = self.label_widget
            case NAME.LEADING_WIDGET:
                widget = self.leading_widget
            case NAME.TRAILING_WIDGET:
                widget = self.trailing_widget
            case _:
                raise ValueError(
                    f'Widget not found for identity: {identity!r}')

        if hasattr(widget, 'icon'): # TODO: animate
            widget.icon = text
            print(f'Set icon of {identity} to {text!r}')
        else:
            widget.text = text
    
    def refresh_chip_content(self, *args) -> None:
        """Refresh the content of the chip.

        This method updates the leading icon, label text, and
        trailing icon of the chip based on their respective properties.
        It ensures that the displayed content is in sync with the
        current property values.
        """
        self._update_child_widget(
            self,
            self.leading_icon,
            identity=NAME.LEADING_WIDGET)
        self._update_child_widget(
            self,
            self.label_text,
            identity=NAME.LABEL_WIDGET)
        self._update_child_widget(
            self,
            self.trailing_icon,
            identity=NAME.TRAILING_WIDGET)
        