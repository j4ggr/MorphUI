"""Widget composition behaviors for MorphUI.

This module provides behaviors for managing child widget delegation,
allowing parent widgets to expose and control properties of their child
widgets through aliased properties.
"""

from kivy.properties import AliasProperty
from kivy.properties import StringProperty
from kivy.properties import ObjectProperty

from morphui.uix.label import MorphTextLabel
from morphui.uix.label import MorphLeadingIconLabel
from morphui.uix.label import MorphTrailingIconLabel


__all__ = [
    'MorphLeadingWidgetBehavior',
    'MorphLabelWidgetBehavior',
    'MorphTrailingWidgetBehavior',]


class MorphLeadingWidgetBehavior:
    """Behavior for managing a leading icon widget.
    
    This behavior provides properties and methods for delegating icon
    management to a child `leading_widget`. It handles both simple icon
    changes and stateful icons (normal/active) for toggle-able widgets.
    
    The behavior creates aliased properties that automatically sync with
    the child widget's properties, providing a clean API for parent
    widgets.
    
    Attributes
    ----------
    leading_widget : MorphLeadingIconLabel
        The child widget displaying the leading icon
    leading_icon : str
        Alias to the child's icon property
    normal_leading_icon : str
        Alias to the child's normal_icon property
    active_leading_icon : str
        Alias to the child's active_icon property
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
        """Get the normal icon from the leading widget.

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
        """Set the normal icon on the leading widget.

        This method sets the normal icon on the `leading_widget`. It
        also updates the internal stored leading icon name.

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
        """Get the active icon from the leading widget.

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
        """Set the active icon on the leading widget.

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
    """The icon name in active state of the leading icon displayed to 
    the left.

    This property gets/sets the `active_icon` property of the 
    `leading_widget`.

    :attr:`active_leading_icon` is a 
    :class:`~kivy.properties.AliasProperty` and is bound to changes in
    the `leading_widget`.
    """

    leading_widget: MorphLeadingIconLabel = ObjectProperty(None)
    """The leading icon widget displayed to the left.

    :attr:`leading_widget` is by default an instance of
    :class:`~morphui.uix.label.MorphLeadingIconLabel`.
    """


class MorphLabelWidgetBehavior:
    """Behavior for managing a text label widget.
    
    This behavior provides properties and methods for delegating text
    content management to a child `label_widget`. It creates an aliased
    property that automatically syncs with the child widget's text
    property.
    
    Attributes
    ----------
    label_widget : MorphTextLabel
        The child widget displaying the text label
    label_text : str
        Alias to the child's text property
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

    label_widget: MorphTextLabel = ObjectProperty(None)
    """The text label widget displayed in the center.

    :attr:`label_widget` is by default an instance of
    :class:`~morphui.uix.label.MorphTextLabel`.
    """


class MorphTrailingWidgetBehavior:
    """Behavior for managing a trailing icon widget.
    
    This behavior provides properties and methods for delegating icon
    management to a child `trailing_widget`. It handles both simple icon
    changes and stateful icons (normal/active) for toggle-able widgets.
    
    The behavior creates aliased properties that automatically sync with
    the child widget's properties, providing a clean API for parent
    widgets.
    
    Attributes
    ----------
    trailing_widget : MorphTrailingIconLabel
        The child widget displaying the trailing icon
    trailing_icon : str
        Alias to the child's icon property
    normal_trailing_icon : str
        Alias to the child's normal_icon property
    active_trailing_icon : str
        Alias to the child's active_icon property
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
        """Get the normal icon from the trailing widget.

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
        """Set the normal icon on the trailing widget.

        This method sets the normal icon on the `trailing_widget`. It
        also updates the internal stored trailing icon name.

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
        bind=['trailing_widget',])
    """The icon name in normal state of the trailing icon displayed to
    the right.

    This property gets/sets the `normal_icon` property of the 
    `trailing_widget`.

    :attr:`normal_trailing_icon` is a 
    :class:`~kivy.properties.AliasProperty` and is bound to changes in
    the `trailing_widget`.
    """

    def _get_active_trailing_icon(self) -> str:
        """Get the active icon from the trailing widget.

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
        """Set the active icon on the trailing widget.

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
        bind=['trailing_widget',])
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
