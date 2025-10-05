from typing import Any
from typing import Tuple

from kivy.event import EventDispatcher
from kivy.properties import BooleanProperty


__all__ = [
    'MorphAutoSizingBehavior']


class MorphAutoSizingBehavior(EventDispatcher):
    """Behavior for automatic widget sizing based on content.
    
    This behavior provides three boolean properties that enable automatic 
    sizing of widgets based on their content and children. It can 
    automatically adjust width, height, or both dimensions to fit the 
    minimum required size.
    """

    auto_width = BooleanProperty(False)
    """Automatically adjust widget width to minimum required size.
    
    When True, the widget's width will be automatically calculated and 
    set to the minimum size required to accommodate all its content and 
    children. This is useful for creating widgets that adapt their width 
    based on their packed content, such as buttons that resize based on 
    text length or containers that fit their child widgets.
    
    :attr:`auto_width` is a :class:`~kivy.properties.BooleanProperty` 
    and defaults to False.
    """

    auto_height = BooleanProperty(False)
    """Automatically adjust widget height to minimum required size.
    
    When True, the widget's height will be automatically calculated and 
    set to the minimum size required to accommodate all its content and 
    children. This is useful for creating widgets that adapt their 
    height based on their packed content, such as labels that resize 
    based on text height or containers that fit their child widgets 
    vertically.
    
    :attr:`auto_height` is a :class:`~kivy.properties.BooleanProperty` 
    and defaults to False.
    """

    auto_size = BooleanProperty(False)
    """Automatically adjust both width and height to minimum required 
    size.
    
    When True, both the widget's width and height will be automatically 
    calculated and set to the minimum size required to accommodate all 
    its content and children. This property acts as a convenience 
    shortcut for setting both :attr:`auto_width` and :attr:`auto_height` 
    to True.
    
    Note: When :attr:`auto_size` is True, it takes precedence over 
    individual :attr:`auto_width` and :attr:`auto_height` settings.
    
    :attr:`auto_size` is a :class:`~kivy.properties.BooleanProperty` 
    and defaults to False.
    """

    _original_size_hint : Tuple[float | None, float | None] = (1.0, 1.0)
    """Internal storage for the original size_hint before auto sizing.
    This is used to restore the size_hint when auto sizing is disabled.
    """

    _original_size : Tuple[float, float] = (0, 0)
    """Internal storage for the original size before auto sizing.
    This is used to restore the size when auto sizing is disabled.
    """

    def on_auto_size(self, instance: Any, auto_size: bool) -> None:
        """Handle auto_size property changes.
        
        Parameters
        ----------
        instance : Any
            The widget instance that triggered the event.
        auto_size : bool
            The new value of the auto_size property.
            
        Notes
        -----
        When auto_size is enabled, stores original size_hint and size,
        then sets size_hint to (None, None) and adjusts width to content.
        When disabled, restores the original size_hint and size values.
        """
        if auto_size:
            self._original_size_hint = self.size_hint
            self._original_size = self.size
            self.size_hint = (None, None)
            self._fit_width_to_content()
        else:
            self.size_hint = self._original_size_hint
            self.width, self.height = self._original_size
    
    def on_auto_width(self, instance: Any, auto_width: bool) -> None:
        """Handle auto_width property changes.
        
        Parameters
        ----------
        instance : Any
            The widget instance that triggered the event.
        auto_width : bool
            The new value of the auto_width property.
            
        Notes
        -----
        When auto_width is enabled, stores original size_hint_x and width,
        then sets size_hint_x to None and adjusts width to content.
        When disabled, restores the original size_hint_x and width values.
        """
        if auto_width:
            self._original_size_hint = (self.size_hint_x, self.size_hint[1])
            self._original_size = (self.width, self.size[1])
            self.size_hint_x = None
            self._fit_width_to_content()
        else:
            self.size_hint_x = self._original_size_hint[0]
            self.width = self._original_size[0]

    def on_auto_height(self, instance: Any, auto_height: bool) -> None:
        """Handle auto_height property changes.
        
        Parameters
        ----------
        instance : Any
            The widget instance that triggered the event.
        auto_height : bool
            The new value of the auto_height property.
            
        Notes
        -----
        When auto_height is enabled, stores original size_hint_y and height,
        then sets size_hint_y to None and adjusts height to content.
        When disabled, restores the original size_hint_y and height values.
        """
        if auto_height:
            self._original_size_hint = (self.size_hint[0], self.size_hint_y)
            self._original_size = (self.size[0], self.height)
            self.size_hint_y = None
            self._fit_height_to_content()
        else:
            self.size_hint_y = self._original_size_hint[1]
            self.height = self._original_size[1]
    
    def _fit_width_to_content(self) -> None:
        """Calculate and set the minimum required width based on content.
        
        Notes
        -----
        For widgets with texture_size (like Label), binds to texture_size
        changes and sets width to texture width. For other widgets, binds
        to minimum_width property to automatically update width.
        """
        if hasattr(self, 'texture_size'):
            self.bind(texture_size=self._fit_width_on_texture_change)
            self._fit_width_on_texture_change(self, self.texture_size)
        else:
            self.bind(minimum_width=self.setter('width'))

    def _fit_width_on_texture_change(
            self, instance: Any, texture_size: Tuple[float, float]) -> None:
        """Update width when the texture size changes.
        
        Parameters
        ----------
        instance : Any
            The widget instance that triggered the texture size change.
        texture_size : Tuple[float, float]
            The new texture size as (width, height).
            
        Notes
        -----
        Sets the widget width to match the texture width, ensuring the
        widget is sized to fit its rendered content.
        """
        self.width = texture_size[0]

    def _fit_height_to_content(self) -> None:
        """Calculate and set the minimum required height based on content.
        
        Notes
        -----
        For widgets with texture_size (like Label), binds to texture_size
        changes and sets height to texture height. For other widgets, binds
        to minimum_height property to automatically update height.
        """
        if hasattr(self, 'texture_size'):
            self.bind(texture_size=self._fit_height_on_texture_change)
            self._fit_height_on_texture_change(self, self.texture_size)
        else:
            self.bind(minimum_height=self.setter('height'))

    def _fit_height_on_texture_change(
            self, instance: Any, texture_size: Tuple[float, float]) -> None:
        """Update height when the texture size changes.
        
        Parameters
        ----------
        instance : Any
            The widget instance that triggered the texture size change.
        texture_size : Tuple[float, float]
            The new texture size as (width, height).
            
        Notes
        -----
        Sets the widget height to match the texture height, ensuring the
        widget is sized to fit its rendered content.
        """
        self.height = texture_size[1]