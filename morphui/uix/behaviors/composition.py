"""Widget composition behaviors for MorphUI.

This module provides behaviors for managing child widget delegation,
allowing parent widgets to expose and control properties of their child
widgets through aliased properties.
"""
from typing import Any

from kivy.properties import AliasProperty
from kivy.properties import StringProperty
from kivy.properties import ObjectProperty
from kivy.properties import BooleanProperty

from morphui.utils import refresh_widget
from morphui.uix.label import MorphTextLabel
from morphui.uix.label import MorphLeadingIconLabel
from morphui.uix.label import MorphTrailingIconLabel


__all__ = [
    'MorphLeadingWidgetBehavior',
    'MorphLabelWidgetBehavior',
    'MorphTripleLabelBehavior',
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
        
        if self.leading_widget.icon and not self._leading_icon:
            self._leading_icon = self.leading_widget.icon
    
        return self._leading_icon
    
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
        
        if self.leading_widget.normal_icon and not self._normal_leading_icon:
            self._normal_leading_icon = self.leading_widget.normal_icon
        
        return self._normal_leading_icon
    
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
        self._normal_leading_icon = icon_name
        if self.leading_widget is not None:
            self.leading_widget.normal_icon = icon_name

    _normal_leading_icon: str = StringProperty('')
    """Internal stored name of the normal leading icon displayed to the
    left."""

    normal_leading_icon: str = AliasProperty(
        _get_normal_leading_icon,
        _set_normal_leading_icon,
        bind=['leading_widget', '_normal_leading_icon',])
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
        
        if self.leading_widget.active_icon and not self._active_leading_icon:
            self._active_leading_icon = self.leading_widget.active_icon
        
        return self._active_leading_icon
    
    def _set_active_leading_icon(self, icon_name: str) -> None:
        """Set the active icon on the leading widget.

        This method sets the active icon on the `leading_widget`. 

        Parameters
        ----------
        icon_name : str
            The icon name to set on the leading widget in its active 
            state.
        """
        self._active_leading_icon = icon_name
        if self.leading_widget is not None:
            self.leading_widget.active_icon = icon_name
    
    _active_leading_icon: str = StringProperty('')
    """Internal stored name of the active leading icon displayed to the
    left."""
    
    active_leading_icon: str = AliasProperty(
        _get_active_leading_icon,
        _set_active_leading_icon,
        bind=['leading_widget', '_active_leading_icon',])
    """The icon name in active state of the leading icon displayed to 
    the left.

    This property gets/sets the `active_icon` property of the 
    `leading_widget`.

    :attr:`active_leading_icon` is a 
    :class:`~kivy.properties.AliasProperty` and is bound to changes in
    the `leading_widget`.
    """

    leading_scale_enabled: bool = BooleanProperty(False)
    """Whether scale animations are enabled for the leading widget.

    If True, changes to the leading icon will be animated with a scale
    effect. If False, icon changes will happen instantly without 
    animation.

    :attr:`leading_scale_enabled` is a 
    :class:`~kivy.properties.BooleanProperty` that controls whether 
    scale animations are enabled for the leading icon.
    """

    leading_widget: MorphLeadingIconLabel = ObjectProperty(None)
    """The leading icon widget displayed to the left.

    :attr:`leading_widget` is by default an instance of
    :class:`~morphui.uix.label.MorphLeadingIconLabel`.
    """

    def on_leading_widget(self, instance: Any, leading_widget: Any) -> None:
        """Called when the leading widget is changed.

        This method updates the `leading_widget` to ensure it reflects
        the current state of the parent widget, including icon names
        and any other relevant properties.
        """
        if self.leading_widget is None:
            return
        
        self.leading_widget.scale_enabled = self.leading_scale_enabled
        self.leading_widget.normal_icon = self.normal_leading_icon
        self.leading_widget.active_icon = self.active_leading_icon
        self.leading_widget._update_icon()
    
    def refresh_leading_widget(self) -> None:
        """Refresh the leading widget to reflect current properties.

        This method updates the `leading_widget` to ensure it reflects
        the current state of the parent widget, including icon names
        and any other relevant properties.
        """
        self.on_leading_widget(self, self.leading_widget)
        refresh_widget(self.leading_widget)


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
        
        if self.label_widget.text and not self._label_text:
            self._label_text = self.label_widget.text
        
        return self._label_text
    
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
        bind=['label_widget', '_label_text'])
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
    def on_label_widget(self, instance: Any, label_widget: Any) -> None:
        """Called when the label widget is changed.

        This method updates the `label_widget` to ensure it reflects
        the current state of the parent widget, including text content
        and any other relevant properties.
        """
        if self.label_widget is None:
            return
        
        self.label_widget.text = self.label_text

    def refresh_label_widget(self) -> None:
        """Refresh the label widget to reflect current properties.

        This method updates the `label_widget` to ensure it reflects
        the current state of the parent widget, including text content
        and any other relevant properties.
        """
        self.on_label_widget(self, self.label_widget)
        refresh_widget(self.label_widget)


class MorphTripleLabelBehavior:
    """Behavior for managing three text label widgets.

    This behavior provides properties and methods for delegating text
    content management to three child label widgets: `heading_widget`,
    `supporting_widget`, and `tertiary_widget`. It creates aliased
    properties that automatically sync with the child widgets' text
    properties.
    """

    def _get_heading_text(self) -> str:
        """Get the text from the heading label widget.

        This method retrieves the text from the `heading_widget`.
        If the `heading_widget` is None, it returns the internal
        stored heading text.

        Returns
        -------
        str
            The heading text displayed at the top
        """
        if self.heading_widget is None:
            return ''
        
        if self.heading_widget.text and not self._heading_text:
            self._heading_text = self.heading_widget.text
        
        return self._heading_text
    
    def _set_heading_text(self, text: str) -> None:
        """Set the text on the heading label widget.

        This method sets the text on the `heading_widget`. It also
        updates the internal stored heading text.

        Parameters
        ----------
        text : str
            The heading text to set
        """
        self._heading_text = text
        if self.heading_widget is not None:
            self.heading_widget.text = text

    _heading_text: str = StringProperty('')
    """Internal stored text of the heading label displayed at the top."""

    heading_text: str = AliasProperty(
        _get_heading_text,
        _set_heading_text,
        bind=['heading_widget', '_heading_text'])
    """The heading text displayed at the top.

    This property gets/sets the `text` property of the `heading_widget`.

    :attr:`heading_text` is a :class:`~kivy.properties.AliasProperty`
    and is bound to changes in the `heading_widget`.
    """

    heading_widget: MorphTextLabel = ObjectProperty(None)
    """The heading label widget displayed at the top.

    This widget is typically used above the main label to provide
    a headline text.

    :attr:`heading_widget` is by default an instance of
    :class:`~morphui.uix.label.MorphTextLabel`.
    """

    def _get_supporting_text(self) -> str:
        """Get the text from the supporting label widget.

        This method retrieves the text from the `supporting_widget`.
        If the `supporting_widget` is None, it returns the internal
        stored supporting text.

        Returns
        -------
        str
            The supporting text displayed in the center
        """
        if self.supporting_widget is None:
            return ''
        
        if self.supporting_widget.text and not self._supporting_text:
            self._supporting_text = self.supporting_widget.text
        
        return self._supporting_text
    
    def _set_supporting_text(self, text: str) -> None:
        """Set the text on the supporting label widget.

        This method sets the text on the `supporting_widget`. It also
        updates the internal stored supporting text.

        Parameters
        ----------
        text : str
            The supporting text to set
        """
        self._supporting_text = text
        if self.supporting_widget is not None:
            self.supporting_widget.text = text

    _supporting_text: str = StringProperty('')
    """Internal stored text of the supporting label displayed in the
    center."""

    supporting_text: str = AliasProperty(
        _get_supporting_text,
        _set_supporting_text,
        bind=['supporting_widget', '_supporting_text'])
    """The supporting text displayed in the center.

    This property gets/sets the `text` property of the
    `supporting_widget`.

    :attr:`supporting_text` is a :class:`~kivy.properties.AliasProperty`
    and is bound to changes in the `supporting_widget`.
    """

    supporting_widget: MorphTextLabel = ObjectProperty(None)
    """The body label widget displayed in the center.

    This widget is typically used below the main label to provide
    supporting text.

    :attr:`supporting_widget` is by default an instance of
    :class:`~morphui.uix.label.MorphTextLabel`.
    """

    def _get_tertiary_text(self) -> str:
        """Get the text from the tertiary label widget.

        This method retrieves the text from the `tertiary_widget`.
        If the `tertiary_widget` is None, it returns the internal
        stored tertiary text.

        Returns
        -------
        str
            The tertiary text displayed at the bottom
        """
        if self.tertiary_widget is None:
            return ''
        
        if self.tertiary_widget.text and not self._tertiary_text:
            self._tertiary_text = self.tertiary_widget.text
        
        return self._tertiary_text
    
    def _set_tertiary_text(self, text: str) -> None:
        """Set the text on the tertiary label widget.

        This method sets the text on the `tertiary_widget`. It also
        updates the internal stored tertiary text.

        Parameters
        ----------
        text : str
            The tertiary text to set
        """
        self._tertiary_text = text
        if self.tertiary_widget is not None:
            self.tertiary_widget.text = text

    _tertiary_text: str = StringProperty('')
    """Internal stored text of the tertiary label displayed at the
    bottom."""

    tertiary_text: str = AliasProperty(
        _get_tertiary_text,
        _set_tertiary_text,
        bind=['tertiary_widget', '_tertiary_text'])
    """The tertiary text displayed at the bottom.

    This property gets/sets the `text` property of the
    `tertiary_widget`.

    :attr:`tertiary_text` is a :class:`~kivy.properties.AliasProperty`
    and is bound to changes in the `tertiary_widget`.
    """

    tertiary_widget: MorphTextLabel = ObjectProperty(None)
    """The tertiary label widget displayed at the bottom.

    This widget is typically used below the supporting label to provide
    additional tertiary text.

    :attr:`tertiary_widget` is by default an instance of
    :class:`~morphui.uix.label.MorphTextLabel`.
    """

    def on_heading_widget(
            self, instance: Any, heading_widget: Any) -> None:
        """Called when the heading widget is changed.

        This method updates the `heading_widget` to ensure it reflects
        the current state of the parent widget, including text content
        and any other relevant properties.
        """
        if self.heading_widget is None:
            return
        
        self.heading_widget.text = self.heading_text

    def on_supporting_widget(
            self, instance: Any, supporting_widget: Any) -> None:
        """Called when the supporting widget is changed.

        This method updates the `supporting_widget` to ensure it
        reflects the current state of the parent widget, including text
        content and any other relevant properties.
        """
        if self.supporting_widget is None:
            return
        
        self.supporting_widget.text = self.supporting_text

    def on_tertiary_widget(
            self, instance: Any, tertiary_widget: Any) -> None:
        """Called when the tertiary widget is changed.

        This method updates the `tertiary_widget` to ensure it reflects
        the current state of the parent widget, including text content
        and any other relevant properties.
        """
        if self.tertiary_widget is None:
            return

        self.tertiary_widget.text = self.tertiary_text

    def refresh_triple_labels(self) -> None:
        """Refresh all three label widgets to reflect current properties.

        This method updates the `heading_widget`, `supporting_widget`,
        and `tertiary_widget` to ensure they reflect the current state
        of the parent widget, including text content and any other
        relevant properties.
        """
        self.on_heading_widget(self, self.heading_widget)
        refresh_widget(self.heading_widget)

        self.on_supporting_widget(self, self.supporting_widget)
        refresh_widget(self.supporting_widget)

        self.on_tertiary_widget(self, self.tertiary_widget)
        refresh_widget(self.tertiary_widget)



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
        
        if self.trailing_widget.icon and not self._trailing_icon:
            self._trailing_icon = self.trailing_widget.icon

        return self._trailing_icon
    
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
        bind=['trailing_widget', '_trailing_icon',])
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
        
        if self.trailing_widget.normal_icon and not self._normal_trailing_icon:
            self._normal_trailing_icon = self.trailing_widget.normal_icon

        return self._normal_trailing_icon

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
        self._normal_trailing_icon = icon_name
        if self.trailing_widget is not None:
            self.trailing_widget.normal_icon = icon_name
    
    _normal_trailing_icon: str = StringProperty('')
    """Internal stored name of the normal trailing icon displayed to the
    right."""

    normal_trailing_icon: str = AliasProperty(
        _get_normal_trailing_icon,
        _set_normal_trailing_icon,
        bind=['trailing_widget', '_normal_trailing_icon',])
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
        
        if self.trailing_widget.active_icon and not self._active_trailing_icon:
            self._active_trailing_icon = self.trailing_widget.active_icon

        return self._active_trailing_icon
    
    def _set_active_trailing_icon(self, icon_name: str) -> None:
        """Set the active icon on the trailing widget.

        This method sets the active icon on the `trailing_widget`. 

        Parameters
        ----------
        icon_name : str
            The icon name to set on the trailing widget in its active 
            state.
        """
        self._active_trailing_icon = icon_name
        if self.trailing_widget is not None:
            self.trailing_widget.active_icon = icon_name
    
    _active_trailing_icon: str = StringProperty('')
    """Internal stored name of the active trailing icon displayed to the
    right."""

    active_trailing_icon: str = AliasProperty(
        _get_active_trailing_icon,
        _set_active_trailing_icon,
        bind=['trailing_widget', '_active_trailing_icon',])
    """The icon name in active state of the trailing icon displayed to
    the right.

    This property gets/sets the `active_icon` property of the 
    `trailing_widget`.

    :attr:`active_trailing_icon` is a 
    :class:`~kivy.properties.AliasProperty` and is bound to changes in
    the `trailing_widget`.
    """

    trailing_scale_enabled: bool = BooleanProperty(False)
    """Whether scale animations are enabled for the trailing widget.

    If True, changes to the trailing icon will be animated with a scale
    effect. If False, icon changes will happen instantly without animation.

    :attr:`trailing_scale_enabled` is a 
    :class:`~kivy.properties.BooleanProperty` that controls whether 
    scale animations are enabled for the trailing icon.
    """

    trailing_widget: MorphTrailingIconLabel = ObjectProperty(None)
    """The trailing icon widget displayed to the right.

    :attr:`trailing_widget` is by default an instance of
    :class:`~morphui.uix.label.MorphTrailingIconLabel`.
    """

    def on_trailing_widget(self, instance: Any, trailing_widget: Any) -> None:
        """Called when the trailing widget is changed.

        This method updates the `trailing_widget` to ensure it reflects
        the current state of the parent widget, including icon names
        and any other relevant properties.
        """
        if self.trailing_widget is None:
            return
        
        self.trailing_widget.scale_enabled = self.trailing_scale_enabled
        self.trailing_widget.icon = self.trailing_icon
        self.trailing_widget.normal_icon = self.normal_trailing_icon
        self.trailing_widget.active_icon = self.active_trailing_icon
        self.trailing_widget._update_icon()

    def refresh_trailing_widget(self) -> None:
        """Refresh the trailing widget to reflect current properties.

        This method updates the `trailing_widget` to ensure it reflects
        the current state of the parent widget, including icon names
        and any other relevant properties.
        """
        self.on_trailing_widget(self, self.trailing_widget)
        refresh_widget(self.trailing_widget)
