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

    _has_texture_size: bool | None = None
    """Cache whether the widget has a texture_size attribute. This is
    used to optimize checks for text-based widgets that can use
    texture_size for auto sizing.
    """

    def __init__(self, **kwargs) -> None:
        self.register_event_type('on_auto_size_updated')
        super().__init__(**kwargs)

        self._original_size = (self.size[0], self.size[1])
        self._original_size_hint = (self.size_hint[0], self.size_hint[1])
        if kwargs.get('auto_size'):
            self.auto_width = True
            self.auto_height = True

        if self.has_texture_size:
            self.fbind('texture_size', self._update_size)
        else:
            self.fbind('minimum_width', self._update_size)
            self.fbind('minimum_height', self._update_size)
        for prop in ('auto_size', 'auto_width', 'auto_height'):
            self.fbind(prop, self._update_auto_sizing, prop=prop)

        self.refresh_auto_sizing()
    
    @property
    def has_texture_size(self) -> bool:
        """Check if the widget has a texture_size attribute.

        This property is used to determine if the widget can use
        texture_size for auto sizing. It returns True if the widget
        has a texture_size attribute, which is common for text-based
        widgets like Label.
        """
        if self._has_texture_size is None:
            self._has_texture_size = hasattr(self, 'texture_size')
        return self._has_texture_size

    def _update_size(self, *args) -> None:
        """Update size based on current auto sizing settings.

        This method adjusts the widget's width and/or height based on
        the current values of :attr:`auto_width` and :attr:`auto_height`.
        It uses texture_size if available, otherwise falls back to
        minimum_width and minimum_height.

        This method is called whenever the relevant size properties
        change, ensuring that the widget's size remains consistent with
        its content.
        """
        if self.auto_width:
            if self.has_texture_size:
                self.width = self.texture_size[0]
            else:
                self.width = self.minimum_width
        else:
            self.width = self._original_size[0]

        if self.auto_height:
            if self.has_texture_size:
                self.height = self.texture_size[1]
            else:
                self.height = self.minimum_height
        else:
            self.height = self._original_size[1]

    def _update_auto_sizing(
            self, instance: Any, value: bool, prop: str) -> None:
        """Update auto sizing based on property changes.

        This method is called whenever one of the auto sizing properties
        changes. It ensures that the appropriate sizing adjustments are
        made to the widget. If :attr:`auto_size` is changed, it sets
        both :attr:`auto_width` and :attr:`auto_height` to the same
        value, triggering their respective handlers.

        Parameters
        ----------
        instance : Any
            The widget instance that triggered the event.
        value : bool
            The new value of the property that changed.
        prop : str
            The name of the property that changed. One of 'auto_size',
            'auto_width', 'auto_height'.
        """
        if prop == 'auto_size':
            self.auto_height = value
            self.auto_width = value
            return

        self.apply_auto_sizing(self.auto_width, self.auto_height)

    def apply_auto_sizing(self, auto_width: bool, auto_height: bool) -> None:
        """Enforce auto sizing based on provided flags. This will
        not change the property values, but will apply the sizing
        adjustments as if the properties were set.

        This method is responsible for applying the appropriate sizing
        adjustments to the widget based on the provided flags. It stores
        the original size and size_hint before making any changes,
        allowing for restoration when auto sizing is disabled.

        Parameters
        ----------
        auto_width : bool
            Whether to apply auto width sizing.
        auto_height : bool
            Whether to apply auto height sizing.
        """
        if auto_width:
            self.size_hint_x = None
        else:
            self.size_hint_x = self._original_size_hint[0]

        if auto_height:
            self.size_hint_y = None
        else:
            self.size_hint_y = self._original_size_hint[1]
        
        self._update_size()
        self.dispatch('on_auto_size_updated')

    def refresh_auto_sizing(self) -> None:
        """Re-apply the current auto sizing settings.

        This method can be called to refresh the auto sizing behavior,
        for example after dynamic changes to the widget that may affect
        sizing. It re-applies the sizing adjustments based on the current
        values of :attr:`auto_width` and :attr:`auto_height`.

        This method preserves the original size and size_hint
        before re-applying the sizing adjustments, ensuring that the
        widget can return to its original size if needed.
        """
        self.apply_auto_sizing(self.auto_width, self.auto_height)

    def on_auto_size_updated(self, *args) -> None:
        """Event fired after auto sizing has been applied or refreshed.

        This event can be used to perform additional actions after the
        widget's size has been adjusted based on its content. It is
        triggered at the end of the :meth:`apply_auto_sizing` method.
        """
        pass

