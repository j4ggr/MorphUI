"""Reusable container widgets for MorphUI.

This module provides base container classes that implement common layout
patterns used across multiple components.
"""

from typing import Any
from typing import Dict

from kivy.metrics import dp
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

    leading_icon: str = StringProperty('')
    """The name of the leading icon displayed to the left.

    :attr:`leading_icon` is a :class:`~kivy.properties.StringProperty`
    and defaults to an empty string.
    """

    label_text: str = StringProperty('')
    """The text displayed in the center.

    :attr:`label_text` is a :class:`~kivy.properties.StringProperty`
    and defaults to an empty string.
    """

    trailing_icon: str = StringProperty('')
    """The name of the trailing icon displayed to the right.

    :attr:`trailing_icon` is a :class:`~kivy.properties.StringProperty`
    and defaults to an empty string.
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
        self.refresh_container_content()

    def _update_child_widget(
            self, instance: Any, text: str, identity: str) -> None:
        """Update the child widget based on the provided text and identity.
        
        This method handles updating the content of child widgets with
        smooth scale animations when icons are added or removed.
        
        Parameters
        ----------
        instance : Any
            The instance that triggered the update
        text : str
            The new text or icon name
        identity : str
            The identity of the widget to update (LEADING_WIDGET,
            LABEL_WIDGET, or TRAILING_WIDGET)
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
                if widget.icon == text:
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

    def _remove_child_content_bindings(self, *args) -> None:
        """Remove content color bindings from child widgets.
        
        This method removes content color bindings from child widgets
        when delegate_content_color is True, allowing the container
        to manage the content color of its children.
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

    def refresh_container_content(self, *args) -> None:
        """Refresh the content of the container.

        This method updates the leading icon, label text, and trailing
        icon based on their respective properties. It ensures that all
        child widgets are in sync with the current property values.
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
