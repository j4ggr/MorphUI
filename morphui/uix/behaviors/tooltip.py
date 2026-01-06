from typing import Any

from kivy.event import EventDispatcher
from kivy.properties import ObjectProperty


__all__ = [
    'MorphTooltipBehavior',]


class MorphTooltipBehavior(EventDispatcher):
    """Behavior class implementing default MorphTooltip settings.
    
    This behavior can be mixed into any widget to provide tooltip
    functionality. It manages a reference to a tooltip widget and
    ensures proper linkage between the widget and its tooltip.
    
    Notes
    -----
    - If you create a custom widget that uses this behavior, ensure that
      the widget inherits also from 
      `morphui.uix.behaviors.MorphHoverBehavior` to handle hover events.
      Order of inheritance matters: the hover behavior should come 
      before this behavior.
    - The widget using this behavior should set the `tooltip` property
      to an instance of `MorphTooltip`.
    - The behavior automatically updates the `caller` property of the
      tooltip to reference the widget.
    """

    tooltip: Any = ObjectProperty(None)
    """Reference to the tooltip widget associated with this behavior.
    
    This property holds a reference to the tooltip widget that is
    associated with the widget using this behavior. It allows for
    easy access and manipulation of the tooltip from within the
    widget. The tooltip is typically shown when the user hovers over
    or focuses on the widget. Use
    :class:`morphui.uix.tooltip.MorphTooltip` for the tooltip.
    
    :attr:`tooltip` is a :class:`~kivy.properties.ObjectProperty` and
    defaults to `None`."""

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.bind(tooltip=self._on_tooltip_changed)
        self._on_tooltip_changed(self, self.tooltip)

    def _on_tooltip_changed(self, *args) -> None:
        """Handle changes to the tooltip property.

        This method is called whenever the `tooltip` property changes.
        It updates the `caller` property of the tooltip to reference
        the widget using this behavior.
        """
        if self.tooltip is None:
            return
        
        self.tooltip.caller = self
