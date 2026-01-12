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
from kivy.uix.boxlayout import BoxLayout

from morphui.utils import clean_config
from morphui.uix.label import MorphTextLabel
from morphui.uix.label import MorphLeadingIconLabel
from morphui.uix.label import MorphTrailingIconLabel
from morphui.uix.behaviors import MorphAutoSizingBehavior
from morphui.uix.behaviors import MorphIdentificationBehavior


__all__ = [
    'MorphLeadingTextContainer',
    'MorphLeadingTextTrailingContainer',]


class MorphLeadingTextContainer(
        MorphIdentificationBehavior,
        MorphAutoSizingBehavior,
        BoxLayout):
    """Base container with leading icon and text label.
    
    This is a minimal base class that provides a horizontal layout 
    structure with two child widgets: a leading icon and a text label.
    It is designed to be inherited by other components that need this
    layout pattern e.g. button with leading icon, list item with
    leading icon, etc.
    
    This class only provides the core layout and widget management.
    Subclasses should add additional behaviors like:
    - :class:`~morphui.uix.behaviors.MorphColorThemeBehavior`,
    - :class:`~morphui.uix.behaviors.MorphInteractionLayerBehavior`,
    - :class:`~morphui.uix.behaviors.MorphSurfaceLayerBehavior`.
    
    The container automatically manages the visibility and animation of
    child widgets based on their content. When icons are set or cleared,
    the widgets smoothly animate in or out using scale animations.
    
    Attributes
    ----------
    leading_icon : str
        Icon name for the leading widget
    label_text : str
        Text content for the label widget
        
    Examples
    --------
    ```python
    from morphui.uix.container import MorphLeadingTextTrailingContainer
    
    class MyMenuItem(MorphLeadingTextTrailingContainer):
        default_config = MorphLeadingTextTrailingContainer.default_config.copy()
        
    item = MyMenuItem(
        leading_icon='home',
        label_text='Home',)
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

    def _get_normal_leading_icon(self) -> str:
        """Get the text from the label widget.

        This method retrieves the normal icon from the `leading_widget`.
        If the `leading_widget` is None, it returns an empty string.

        Returns
        -------
        str
            The normal icon name of the leading widget
        """
        if self.leading_widget is None:
            return ''
        
        return self.leading_widget.normal_icon
    
    def _set_normal_leading_icon(self, icon_name: str) -> None:
        """Set the text on the label widget.

        This method sets the normal icon on the `leading_widget`. It
        also updates  the internal stored leading icon name.

        Parameters
        ----------
        icon_name : str
            The icon name to set on the leading widget in its normal 
            state.
        """
        self._leading_icon = icon_name
        if self.leading_widget is not None:
            self.leading_widget.normal_icon = icon_name

    normal_leading_icon: str = AliasProperty(
        _get_normal_leading_icon,
        _set_normal_leading_icon,
        bind=['leading_widget',])
    """The icon name in normal state of the leading icon displayed to 
    the left.

    This property gets/sets the `normal_icon` property of the 
    `leading_widget`.

    :attr:`normal_leading_icon` is a 
    :class:`~kivy.properties.AliasProperty` and is bound to changes in
    the `leading_widget`.
    """

    def _get_active_leading_icon(self) -> str:
        """Get the text from the label widget.

        This method retrieves the active icon from the `leading_widget`.
        If the `leading_widget` is None, it returns an empty string.

        Returns
        -------
        str
            The active icon name of the leading widget
        """
        if self.leading_widget is None:
            return ''
        
        return self.leading_widget.active_icon
    
    def _set_active_leading_icon(self, icon_name: str) -> None:
        """Set the text on the label widget.

        This method sets the active icon on the `leading_widget`. 

        Parameters
        ----------
        icon_name : str
            The icon name to set on the leading widget in its active 
            state.
        """
        if self.leading_widget is not None:
            self.leading_widget.active_icon = icon_name
    
    active_leading_icon: str = AliasProperty(
        _get_active_leading_icon,
        _set_active_leading_icon,
        bind=['leading_widget',])

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

    leading_widget: MorphLeadingIconLabel = ObjectProperty(None)
    """The leading icon widget displayed to the left.

    :attr:`leading_widget` is by default an instance of
    :class:`~morphui.uix.label.MorphLeadingIconLabel`.
    """

    label_widget: MorphTextLabel = ObjectProperty(None)
    """The text label widget displayed in the center.

    :attr:`label_widget` is by default an instance of
    :class:`~morphui.uix.label.MorphTextLabel`.
    """

    _default_child_widgets = {
        'leading_widget': MorphLeadingIconLabel,
        'label_widget': MorphTextLabel,}
    """Default child widgets for the container.
    
    This dictionary maps widget identities to their default classes.
    Override in subclasses to change default child widgets.
    """

    default_config: Dict[str, Any] = dict(
        orientation='horizontal',
        auto_size=True,
        padding=dp(8),
        spacing=dp(8),)
    """Default configuration for the container.

    This dictionary contains default property values for the
    :class:`MorphLeadingTextContainer`. These defaults can be overridden
    by subclasses or during instantiation.
    """

    def __init__(self, **kwargs) -> None:
        config = clean_config(self.default_config, kwargs)
        for key, widget_cls in self._default_child_widgets.items():
            if key not in config and widget_cls is not None:
                config[key] = widget_cls()
        super().__init__(**config)
        
        if self.leading_widget is not None:
            self.add_widget(self.leading_widget)
            self.leading_widget.icon = self._leading_icon

        if self.label_widget is not None:
            self.add_widget(self.label_widget)
            self.label_widget.text = self._label_text


class MorphLeadingTextTrailingContainer(
        MorphLeadingTextContainer):
    """Base container with leading icon, text label, and trailing icon.
    
    This is a minimal base class that provides a horizontal layout 
    structure with three child widgets: a leading icon, a text label,
    and a trailing icon. It is designed to be inherited by other 
    components that need this layout pattern, such as menu items, list
    items, chips, etc.
    
    This class only provides the core layout and widget management.
    Subclasses should add additional behaviors like:
    - :class:`~morphui.uix.behaviors.MorphColorThemeBehavior`
    - :class:`~morphui.uix.behaviors.MorphInteractionLayerBehavior`
    - :class:`~morphui.uix.behaviors.MorphSurfaceLayerBehavior`
    
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
        
    Examples
    --------
    ```python
    from morphui.uix.container import MorphLeadingTextTrailingContainer
    
    class MyMenuItem(MorphLeadingTextTrailingContainer):
        default_config = MorphLeadingTextTrailingContainer.default_config.copy()
        
    item = MyMenuItem(
        leading_icon='home',
        label_text='Home',
        trailing_icon='chevron-right')
    ```
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

    def _get_normal_trailing_icon(self) -> str:
        """Get the text from the label widget.

        This method retrieves the normal icon from the `trailing_widget`.
        If the `trailing_widget` is None, it returns an empty string.

        Returns
        -------
        str
            The normal icon name of the trailing widget
        """

        if self.trailing_widget is None:
            return ''
        
        return self.trailing_widget.normal_icon

    def _set_normal_trailing_icon(self, icon_name: str) -> None:
        """Set the text on the label widget.

        This method sets the normal icon on the `trailing_widget`. It
        also updates  the internal stored trailing icon name.

        Parameters
        ----------
        icon_name : str
            The icon name to set on the trailing widget in its normal 
            state.
        """
        self._trailing_icon = icon_name
        if self.trailing_widget is not None:
            self.trailing_widget.normal_icon = icon_name

    normal_trailing_icon: str = AliasProperty(
        _get_normal_trailing_icon,
        _set_normal_trailing_icon,
        bind=['label_widget',])
    """The icon name in normal state of the trailing icon displayed to
    the right.

    This property gets/sets the `normal_icon` property of the 
    `trailing_widget`.

    :attr:`normal_trailing_icon` is a 
    :class:`~kivy.properties.AliasProperty` and is bound to changes in
    the `trailing_widget`.
    """

    def _get_active_trailing_icon(self) -> str:
        """Get the text from the label widget.

        This method retrieves the active icon from the `trailing_widget`.
        If the `trailing_widget` is None, it returns an empty string.

        Returns
        -------
        str
            The active icon name of the trailing widget
        """
        if self.trailing_widget is None:
            return ''
        
        return self.trailing_widget.active_icon
    
    def _set_active_trailing_icon(self, icon_name: str) -> None:
        """Set the text on the label widget.

        This method sets the active icon on the `trailing_widget`. 

        Parameters
        ----------
        icon_name : str
            The icon name to set on the trailing widget in its active 
            state.
        """
        if self.trailing_widget is not None:
            self.trailing_widget.active_icon = icon_name

    active_trailing_icon: str = AliasProperty(
        _get_active_trailing_icon,
        _set_active_trailing_icon,
        bind=['label_widget',])
    """The icon name in active state of the trailing icon displayed to
    the right.

    This property gets/sets the `active_icon` property of the 
    `trailing_widget`.

    :attr:`active_trailing_icon` is a 
    :class:`~kivy.properties.AliasProperty` and is bound to changes in
    the `trailing_widget`.
    """

    trailing_widget: MorphTrailingIconLabel = ObjectProperty(None)
    """The trailing icon widget displayed to the right.

    :attr:`trailing_widget` is by default an instance of
    :class:`~morphui.uix.label.MorphTrailingIconLabel`.
    """

    _default_child_widgets = {
        'leading_widget': MorphLeadingIconLabel,
        'label_widget': MorphTextLabel,
        'trailing_widget': MorphTrailingIconLabel,}
    """Default child widgets for the container.
    
    This dictionary maps widget identities to their default classes.
    Override in subclasses to change default child widgets.
    """

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        if self.trailing_widget is not None:
            self.add_widget(self.trailing_widget)
            self.trailing_widget.icon = self._trailing_icon
