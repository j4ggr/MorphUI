from typing import Any, List
from typing import Dict

from kivy.metrics import dp
from kivy.properties import ObjectProperty
from kivy.properties import StringProperty
from kivy.properties import BooleanProperty
from kivy.uix.boxlayout import BoxLayout

from morphui.utils import clean_config
from morphui.constants import NAME

from morphui.uix.behaviors import MorphIconBehavior
from morphui.uix.behaviors import MorphHoverBehavior
from morphui.uix.behaviors import MorphScaleBehavior
from morphui.uix.behaviors import MorphRippleBehavior
from morphui.uix.behaviors import MorphButtonBehavior
from morphui.uix.behaviors import MorphElevationBehavior
from morphui.uix.behaviors import MorphAutoSizingBehavior
from morphui.uix.behaviors import MorphColorThemeBehavior
from morphui.uix.behaviors import MorphRoundSidesBehavior
from morphui.uix.behaviors import MorphToggleButtonBehavior
from morphui.uix.behaviors import MorphSurfaceLayerBehavior
from morphui.uix.behaviors import MorphContentLayerBehavior
from morphui.uix.behaviors import MorphIdentificationBehavior
from morphui.uix.behaviors import MorphInteractionLayerBehavior

from morphui.uix.label import MorphSimpleLabel
from morphui.uix.label import MorphSimpleIconLabel
from morphui.uix.button import MorphSimpleIconButton


__all__ = [
    'ChipLeadingIconLabel',
    'ChipTextLabel',
    'ChipTrailingIconButton',
    'MorphChip',
    'MorphFilterChip',
    'MorphInputChip',]


class ChipLeadingIconLabel(
        MorphScaleBehavior,
        MorphSimpleIconLabel):
    
    default_config: Dict[str, Any] = (
        MorphSimpleIconLabel.default_config.copy() | dict(
        padding=dp(0),
        pos_hint={'center_y': 0.5},))


class ChipTextLabel(MorphSimpleLabel):

    default_config: Dict[str, Any] = (
        MorphSimpleLabel.default_config.copy() | dict(
        auto_size=True,
        padding=dp(0),
        pos_hint={'center_y': 0.5},))


class ChipTrailingIconButton(
        MorphScaleBehavior,
        MorphSimpleIconButton):

    default_config: Dict[str, Any] = (
        MorphSimpleIconButton.default_config.copy() | dict(
        padding=dp(0),
        pos_hint={'center_y': 0.5},))


class MorphChip(
        MorphIdentificationBehavior,
        MorphAutoSizingBehavior,
        MorphHoverBehavior,
        MorphRippleBehavior,
        MorphButtonBehavior,
        MorphColorThemeBehavior,
        MorphRoundSidesBehavior,
        MorphContentLayerBehavior,
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

    delegate_content_color: bool = BooleanProperty(True)
    """Whether to delegate content color application to child widgets.

    If set to `True`, the chip will delegate the application of content
    color to its child widgets (leading icon, label, trailing icon).
    If set to `False`, the chip will not delegate content color
    application.

    :attr:`delegate_content_color` is a
    :class:`~kivy.properties.BooleanProperty` and defaults to `True`.
    """

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

        self.bind(
            pos=self._update_layout,
            size=self._update_layout,
            spacing=self._update_layout,
            padding=self._update_layout,
            radius=self._update_layout,)

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

        if hasattr(widget, 'icon'):
            def set_icon(*args):
                widget.icon = text

            if issubclass(type(widget), MorphScaleBehavior):
                if bool(widget.icon) == bool(text):
                    pass
                elif text:
                    set_icon()
                    widget.animate_scale_in()
                else:
                    widget.animate_scale_out(callback=set_icon)
            else:
                set_icon()
        else:
            widget.text = text
        self._update_layout()
    
    def _remove_child_content_bindings(self, *args) -> None:
        """Remove content color bindings from child widgets.

        This method removes any content color bindings from the
        leading, label, and trailing widgets to prevent them from
        being affected by changes in the chip's content color.
        """
        if not self.delegate_content_color:
            return None
        
        def new_bindings(original: Dict[str, str]) -> Dict[str, str]:
            return dict(
                (k, v) for k, v in original.items()
                if 'content' not in k)
        self.leading_widget.theme_color_bindings = new_bindings(
            self.leading_widget.theme_color_bindings)
        self.label_widget.theme_color_bindings = new_bindings(
            self.label_widget.theme_color_bindings)
        self.trailing_widget.theme_color_bindings = new_bindings(
            self.trailing_widget.theme_color_bindings)

    def _update_layout(self, *args) -> None:
        """Update the layout of the chip and its child widgets.
        
        This method recalculates and updates the layout of the chip
        and its child widgets based on the current properties such as
        size, padding, spacing, and radius.
        """
        if self.trailing_widget.icon:
            trailing_radius = [0, *self.clamped_radius[1:3], 0]
            expansion = [self.spacing / 2, *self.padding[1:]]
        else:
            trailing_radius = [0, 0, 0, 0]
            expansion = [0, 0, 0, 0]
        self.trailing_widget.radius = trailing_radius
        self.trailing_widget.interaction_layer_expansion = expansion
    
    def apply_content(self, color: List[float]) -> None:
        """Apply content color based on the current state.

        This method overrides the base method to delegate content
        color application to the leading and label widgets.
        """
        if not self.delegate_content_color:
            return super().apply_content(color)

        for widget in (
                self.leading_widget,
                self.label_widget,
                self.trailing_widget,):
            if hasattr(widget, 'apply_content'):
                widget.apply_content(color)

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
        self._remove_child_content_bindings()


class MorphFilterChip(
        MorphIconBehavior,
        MorphToggleButtonBehavior,
        MorphChip):
    """Morph Filter Chip component.

    A filter chip represents a filter option that can be toggled on
    or off. It is used to apply filters to content or data sets.

    Example
    -------
    ````python
    from morphui.app import MorphApp
    from morphui.uix.chip import MorphFilterChip
    from morphui.uix.floatlayout import MorphFloatLayout

    class MyApp(MorphApp):
        def build(self) -> MorphFloatLayout:
            self.theme_manager.switch_to_dark()
            return MorphFloatLayout(
                MorphFilterChip(
                    identity='my_widget',
                    leading_icon='filter',),
                surface_color=self.theme_manager.surface_color,)
    
    if __name__ == '__main__':
        MyApp().run()
    """

    default_config: Dict[str, Any] = (
        MorphChip.default_config.copy() | dict(
        theme_color_bindings=dict(
            surface_color='transparent_color',
            content_color='content_surface_color',
            border_color='outline_variant_color',
            active_surface_color='secondary_container_color',
            active_content_color='content_secondary_container_color',
            active_border_color='transparent_color',
            disabled_surface_color='transparent_color',
            disabled_content_color='outline_color',),
        normal_icon='',
        active_icon='check',))
    """Default configuration for the :class:`MorphFilterChip` component."""

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.bind(active=self._update_icon)
    
    def _apply_icon(self, instance: Any, icon: str) -> None:
        """Apply the icon to the leading widget based on the current 
        state.

        This method overrides the base method to delegate icon
        application to the leading widget.
        """
        self.leading_icon = icon


class MorphInputChip(
        MorphChip):
    """Morph Input Chip component.

    An input chip represents a user input or selection that can be
    removed. It typically includes   a trailing icon button for removal.

    Example
    -------
    ````python
    from morphui.app import MorphApp
    from morphui.uix.chip import MorphInputChip
    from morphui.uix.floatlayout import MorphFloatLayout

    class MyApp(MorphApp):
        def build(self) -> MorphFloatLayout:
            self.theme_manager.switch_to_dark()
            return MorphFloatLayout(
                MorphInputChip(
                    identity='my_widget',
                    label_text='Input Chip',
                    trailing_icon='close',),
                surface_color=self.theme_manager.surface_color,)
    if __name__ == '__main__':
        MyApp().run()
    """
    default_config: Dict[str, Any] = (
        MorphChip.default_config.copy() | dict(
            trailing_icon='close',))
    """Default configuration for the :class:`MorphInputChip` component."""

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.trailing_widget.bind(
            on_press=self.on_trailing_widget_release,
            on_release=self.on_trailing_widget_release)
    
    def on_trailing_widget_press(self, *args) -> None:
        """Handle the press event of the trailing icon button.

        This method is called when the trailing icon button is
        pressed. It can be used to provide visual feedback or
        initiate actions before the chip is removed.
        """
        pass

    def on_trailing_widget_release(self, *args) -> None:
        """Handle the release event of the trailing icon button.

        This method is called when the trailing icon button is
        released. It removes the chip from its parent layout.
        """
        if self.parent:
            self.parent.remove_widget(self)
