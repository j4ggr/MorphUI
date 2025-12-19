"""Reusable container widgets for MorphUI.

This module provides base container classes that implement common layout
patterns used across multiple components.
"""

from typing import Any
from typing import Dict

from kivy.metrics import dp
from kivy.properties import AliasProperty
from kivy.properties import StringProperty
from kivy.properties import ObjectProperty
from kivy.properties import BooleanProperty
from kivy.uix.boxlayout import BoxLayout

from morphui.utils import clean_config
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


class LeadingIconLabel( # TODO: move to Labels module?
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


class TextLabel(MorphSimpleLabel): # TODO: move to Labels module?
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


class TrailingIconLabel( # TODO: move to Labels module?
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


class TrailingIconButton( # TODO: move to Buttons module?
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

    def _get_leading_icon(self) -> str:
        """Get the leading icon name from the leading widget.

        This method retrieves the icon name from the `leading_widget`.
        If the `leading_widget` is None, it returns the internal
        stored leading icon name.

        Returns
        -------
        str
            The name of the leading icon
        """
        if self.leading_widget is None:
            return ''
        return self.leading_widget.icon or self._leading_icon
    
    def _set_leading_icon(self, icon_name: str) -> None:
        """Set the leading icon name on the leading widget.

        This method sets the icon name on the `leading_widget`.
        It also updates the internal stored leading icon name.
        
        Parameters
        ----------
        icon_name : str
            The name of the leading icon to set
        """
        self._leading_icon = icon_name
        if self.leading_widget is not None:
            self.leading_widget.icon = icon_name

    _leading_icon: str = StringProperty('')
    """Internal stored name of the leading icon displayed to the left."""

    leading_icon: str = AliasProperty(
        _get_leading_icon,
        _set_leading_icon,
        bind=['leading_widget', '_leading_icon',])
    """The name of the leading icon displayed to the left.

    This property gets/sets the `icon` property of the `leading_widget`.
    If the `leading_widget` supports scale animations, the icon change
    will be animated smoothly.

    :attr:`leading_icon` is a :class:`~kivy.properties.AliasProperty`
    and is bound to changes in the `leading_widget`.
    """

    def _get_label_text(self) -> str:
        """Get the text from the label widget.

        This method retrieves the text from the `label_widget`.
        If the `label_widget` is None, it returns the internal
        stored label text.

        Returns
        -------
        str
            The text displayed in the center
        """
        if self.label_widget is None:
            return ''
        
        return self.label_widget.text or self._label_text
    
    def _set_label_text(self, text: str) -> None:
        """Set the text on the label widget.

        This method sets the text on the `label_widget`. It also updates
        the internal stored label text.

        Parameters
        ----------
        text : str
            The text to set on the label
        """
        self._label_text = text
        if self.label_widget is not None:
            self.label_widget.text = text

    _label_text: str = StringProperty('')
    """Internal stored text of the label displayed in the center."""

    label_text: str = AliasProperty(
        _get_label_text,
        _set_label_text,
        bind=['label_widget',])
    """The text displayed in the center.

    This property gets/sets the `text` property of the `label_widget`.

    :attr:`label_text` is a :class:`~kivy.properties.AliasProperty`
    and is bound to changes in the `label_widget`.
    """

    def _get_trailing_icon(self) -> str:
        """Get the trailing icon name from the trailing widget.

        This method retrieves the icon name from the `trailing_widget`.
        If the `trailing_widget` is None, it returns the internal
        stored trailing icon name.

        Returns
        -------
        str
            The name of the trailing icon
        """
        if self.trailing_widget is None:
            return ''
        return self.trailing_widget.icon or self._trailing_icon
    
    def _set_trailing_icon(self, icon_name: str) -> None:
        """Set the trailing icon name on the trailing widget.

        This method sets the icon name on the `trailing_widget`.
        It also updates the internal stored trailing icon name.
        
        Parameters
        ----------
        icon_name : str
            The name of the trailing icon to set
        """
        self._trailing_icon = icon_name
        if self.trailing_widget is not None:
            self.trailing_widget.icon = icon_name

    _trailing_icon: str = StringProperty('')
    """Internal stored name of the trailing icon displayed to the right."""

    trailing_icon: str = AliasProperty(
        _get_trailing_icon,
        _set_trailing_icon,
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
        
        if self.leading_widget is not None:
            self.add_widget(self.leading_widget)
            self.leading_widget.icon = config.get('leading_icon', '')

        if self.label_widget is not None:
            self.add_widget(self.label_widget)
            self.label_widget.text = config.get('label_text', '')

        if self.trailing_widget is not None:
            self.add_widget(self.trailing_widget)
            self.trailing_widget.icon = config.get('trailing_icon', '')

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
