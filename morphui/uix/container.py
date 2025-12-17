"""Reusable container widgets for MorphUI.

This module provides base container classes that implement common layout
patterns used across multiple components.
"""

from typing import Any
from typing import Dict

from kivy.metrics import dp
from kivy.metrics import AliasProperty
from kivy.properties import ObjectProperty
from kivy.properties import StringProperty
from kivy.properties import BooleanProperty
from kivy.uix.boxlayout import BoxLayout

from morphui.utils import clean_config
from morphui.constants import NAME
from morphui.uix.label import MorphSimpleLabel
from morphui.uix.label import MorphSimpleIconLabel
from morphui.uix.button import MorphSimpleIconButton
from morphui.uix.behaviors import MorphScaleBehavior
from morphui.uix.behaviors import MorphAutoSizingBehavior
from morphui.uix.behaviors import MorphIdentificationBehavior


__all__ = [
    'LeadingIconLabel',
    'TextLabel',
    'TrailingIconLabel',
    'TrailingIconButton',
    'LeadingTextTrailingContainer',]


class LeadingIconLabel(
        MorphScaleBehavior,
        MorphSimpleIconLabel):
    """Leading icon label for containers.
    
    This widget displays an icon on the left side of a container,
    with support for scale animations.
    """
    
    default_config: Dict[str, Any] = (
        MorphSimpleIconLabel.default_config.copy() | dict(
        padding=dp(0),
        pos_hint={'center_y': 0.5},))


class TextLabel(MorphSimpleLabel):
    """Text label for containers.
    
    This widget displays text mostly used in between leading and 
    trailing icons or other widgets.
    """
    
    default_config: Dict[str, Any] = (
        MorphSimpleLabel.default_config.copy() | dict(
        auto_size=(False, True),
        size_hint=(1, None),
        padding=dp(0),
        pos_hint={'center_y': 0.5},))


class TrailingIconLabel(
        MorphScaleBehavior,
        MorphSimpleIconLabel):
    """Trailing icon label for containers.
    
    This widget displays an icon on the right side of a container,
    with support for scale animations.
    """
    
    default_config: Dict[str, Any] = (
        MorphSimpleIconLabel.default_config.copy() | dict(
        padding=dp(0),
        pos_hint={'center_y': 0.5},))


class TrailingIconButton(
        MorphScaleBehavior,
        MorphSimpleIconButton):
    """Trailing icon button for containers.
    
    This widget displays an interactive icon button on the right side
    of a container, with support for scale animations. Used primarily
    for chips where the trailing icon needs button behavior.
    """
    
    default_config: Dict[str, Any] = (
        MorphSimpleIconLabel.default_config.copy() | dict(
        padding=dp(0),
        pos_hint={'center_y': 0.5},))


class LeadingTextTrailingContainer(
        MorphIdentificationBehavior,
        MorphAutoSizingBehavior,
        BoxLayout):
    """Base container with leading icon, text label, and trailing icon.
    
    This is a minimal base class that provides a horizontal layout structure
    with three child widgets: a leading icon, a text label, and a
    trailing icon. It is designed to be inherited by other components
    that need this layout pattern, such as menu items, list items,
    chips, etc.
    
    This class only provides the core layout and widget management.
    Subclasses should add additional behaviors like MorphColorThemeBehavior,
    MorphInteractionLayerBehavior, MorphSurfaceLayerBehavior as needed.
    
    The container automatically manages the visibility and animation of
    child widgets based on their content. When icons are set or cleared,
    the widgets smoothly animate in or out using scale animations.
    
    Attributes
    ----------
    leading_icon : str
        Icon name for the leading widget
    label_text : str
        Text content for the label widget
    trailing_icon : str
        Icon name for the trailing widget
    delegate_content_color : bool
        Whether to delegate content color to child widgets
        
    Examples
    --------
    ```python
    from morphui.uix.container import LeadingTextTrailingContainer
    
    class MyMenuItem(LeadingTextTrailingContainer):
        default_config = LeadingTextTrailingContainer.default_config.copy()
        
    item = MyMenuItem(
        leading_icon='home',
        label_text='Home',
        trailing_icon='chevron-right')
    ```
    """
    @staticmethod
    def _get_icon(widget: Any) -> str:
        """Get the icon name from a widget.
        
        This method retrieves the icon name from the provided widget.
        If the widget is None or does not have an icon attribute,
        it returns an empty string.

        Parameters
        ----------
        widget : Any
            The widget to get the icon from

        Returns
        -------
        str
            The name of the icon, or an empty string if not available
        """
        if widget is None or not hasattr(widget, 'icon'):
            return ''
        
        return widget.icon

    @staticmethod
    def _set_icon(widget: Any, icon_name: str) -> None:
        """Set the icon of a widget with scale animation if applicable.
        
        This method sets the icon of the provided widget. If the widget
        supports scale animations (i.e., is a subclass of 
        :class:`~morphui.uix.behaviors.MorphScaleBehavior`), it will 
        animate the icon change smoothly.

        Parameters
        ----------
        widget : Any
            The widget to set the icon on
        icon_name : str
            The name of the icon to set
        """
        if widget is None or not hasattr(widget, 'icon'):
            return None
        
        def set_widget_icon(*args) -> None:
            widget.icon = icon_name

        if issubclass(type(widget), MorphScaleBehavior):
            if widget.icon == icon_name:
                pass
            elif icon_name:
                set_widget_icon()
                widget.animate_scale_in()
            else:
                widget.animate_scale_out(callback=set_widget_icon)
        else:
            set_widget_icon()

    leading_icon: str = AliasProperty(
        lambda self: self._get_icon(self.leading_widget),
        lambda self, icon_name: self._set_icon(self.leading_widget, icon_name),
        bind=['leading_widget',])
    """The name of the leading icon displayed to the left.

    This property gets/sets the `icon` property of the `leading_widget`.
    If the `leading_widget` supports scale animations, the icon change
    will be animated smoothly.

    :attr:`leading_icon` is a :class:`~kivy.properties.AliasProperty`
    and is bound to changes in the `leading_widget`.
    """

    def _get_label_text(self) -> str:
        if self.label_widget is None:
            return ''
        
        return self.label_widget.text
    
    def _set_label_text(self, text: str) -> None:
        if self.label_widget is not None:
            self.label_widget.text = text

    label_text: str = AliasProperty(
        _get_label_text,
        _set_label_text,
        bind=['label_widget',])
    """The text displayed in the center.

    This property gets/sets the `text` property of the `label_widget`.

    :attr:`label_text` is a :class:`~kivy.properties.AliasProperty`
    and is bound to changes in the `label_widget`.
    """

    text: str = AliasProperty(
        _get_label_text,
        _set_label_text,
        bind=['label_text',])
    """Alias for label_text for convenience.

    This property is an alias for `label_text`, allowing direct access
    to the text content of the label widget.

    :attr:`text` is a :class:`~kivy.properties.AliasProperty`
    and is bound to changes in the `label_text`.
    """

    trailing_icon: str = AliasProperty(
        lambda self: self._get_icon(self.trailing_widget),
        lambda self, icon_name: self._set_icon(self.trailing_widget, icon_name),
        bind=['trailing_widget',])
    """The name of the trailing icon displayed to the right.

    This property gets/sets the `icon` property of the `trailing_widget`.
    If the `trailing_widget` supports scale animations, the icon change
    will be animated smoothly.

    :attr:`trailing_icon` is a :class:`~kivy.properties.AliasProperty`
    and is bound to changes in the `trailing_widget`.
    """

    leading_widget: LeadingIconLabel = ObjectProperty()
    """The leading icon widget displayed to the left.

    :attr:`leading_widget` is by default an instance of
    :class:`~morphui.uix.container.LeadingIconLabel`.
    """

    label_widget: TextLabel = ObjectProperty(None)
    """The text label widget displayed in the center.

    :attr:`label_widget` is by default an instance of
    :class:`~morphui.uix.container.TextLabel`.
    """

    trailing_widget: TrailingIconLabel = ObjectProperty(None)
    """The trailing icon widget displayed to the right.

    :attr:`trailing_widget` is by default an instance of
    :class:`~morphui.uix.container.TrailingIconLabel`.
    """

    delegate_content_color: bool = BooleanProperty(True)
    """Whether to delegate content color application to child widgets.

    :attr:`delegate_content_color` is a
    :class:`~kivy.properties.BooleanProperty` and defaults to `True`.
    """

    _default_child_widgets = {
        'leading_widget': LeadingIconLabel,
        'label_widget': TextLabel,
        'trailing_widget': TrailingIconLabel,}
    """Default child widgets for the container.
    
    This dictionary maps widget identities to their default classes.
    Override in subclasses to change default child widgets.
    """

    default_config: Dict[str, Any] = dict(
        orientation='horizontal',
        auto_size=True,
        padding=dp(8),
        spacing=dp(8),)

    def __init__(self, **kwargs) -> None:
        config = clean_config(self.default_config, kwargs)
        for key, widget_cls in self._default_child_widgets.items():
            if key not in config:
                config[key] = widget_cls()

        super().__init__(**config)
        self.add_widget(self.leading_widget)
        self.add_widget(self.label_widget)
        self.add_widget(self.trailing_widget)

    def on_leading_widget(
            self,
            instance: Any,
            widget: LeadingIconLabel) -> None:
        """Callback when the leading widget changes.

        Parameters
        ----------
        instance : Any
            The instance that triggered the change
        widget : LeadingIconLabel
            The new leading widget
        """
        if widget is None or not hasattr(widget, 'icon'):
            return
        self.leading_widget.bind(icon=self.setter('leading_icon'))
        self._remove_child_content_bindings(self.leading_widget)

    def on_label_widget(
            self,
            instance: Any,
            widget: TextLabel) -> None:
        """Callback when the label widget changes.

        Parameters
        ----------
        instance : Any
            The instance that triggered the change
        widget : TextLabel
            The new label widget
        """
        if widget is None:
            return
        self.label_widget.bind(text=self.setter('label_text'))
        self._remove_child_content_bindings(self.label_widget)

    def on_trailing_widget(
            self,
            instance: Any,
            widget: TrailingIconLabel) -> None:
        """Callback when the trailing widget changes.

        Parameters
        ----------
        instance : Any
            The instance that triggered the change
        widget : TrailingIconLabel
            The new trailing widget
        """
        if widget is None or not hasattr(widget, 'icon'):
            return
        self.trailing_widget.bind(icon=self.setter('trailing_icon'))
        self._remove_child_content_bindings(self.trailing_widget)

    def _remove_child_content_bindings(self, widget: Any) -> None:
        """Remove content color bindings from child widget.
        
        This method removes content color bindings from child widget
        when :attr:`delegate_content_color` is `True`, allowing the
        container to manage the content color of its children.
        """
        if not self.delegate_content_color:
            return None
        
        widget.theme_color_bindings = dict(
            (k, v) for k, v in widget.theme_color_bindings.items()
            if 'content' not in k)
    
    def apply_content(self, color: list[float]) -> None:
        """Apply content color based on the current state.

        This method delegates content color application to child widgets
        when delegate_content_color is True.
        
        Parameters
        ----------
        color : list[float]
            RGBA color values to apply
        """
        if not self.delegate_content_color:
            return super().apply_content(color)

        for widget in (
                self.leading_widget,
                self.label_widget,
                self.trailing_widget,):
            if hasattr(widget, 'apply_content'):
                widget.apply_content(color)
