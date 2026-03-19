from typing import Any

from kivy.event import EventDispatcher
from kivy.properties import StringProperty
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

    tooltip_text: str = StringProperty('')
    """The tooltip text for the navigation rail item.

    This text is displayed when the user hovers over the item,
    providing additional information about its function. The text can be 
    updated dynamically after the widget is created by setting the
    :attr:`tooltip_text` property.

    :attr:`tooltip_text` is a :class:`~kivy.properties.StringProperty`
    and defaults to an empty string.

    Notes
    -----
    - The actual display of the tooltip text is handled by the tooltip
      widget itself, which should be set as the `tooltip` property.
    - When the `tooltip_text` property changes, the behavior 
      automatically updates the tooltip's text to match.
    - :class:`morphui.uix.tooltip.MorphSimpleTooltip` updates the text 
      of a single label, while 
      :class:`morphui.uix.tooltip.MorphRichTooltip` updates the 
      supporting text label, allowing the heading to remain unchanged.
      Both of these tooltip classes implement the `update_tooltip_text` 
      method to handle text updates appropriately.
    """

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.bind(
            tooltip=self._on_tooltip_changed,
            tooltip_text=self.update_tooltip_text)
        self._on_tooltip_changed(self, self.tooltip)

    def _on_tooltip_changed(self, *args) -> None:
        """Handle changes to the tooltip property.

        This method is called whenever the `tooltip` property changes.
        It updates the `caller` property of the tooltip to reference
        the widget using this behavior. If the tooltip is set to `None`, 
        it does nothing. Finally, it calls `update_tooltip_text` to 
        ensure the tooltip text is updated to match the current 
        `tooltip_text` property.
        """
        if self.tooltip is None:
            return
        
        self.tooltip.caller = self
        self.update_tooltip_text(self, self.tooltip_text)

    def update_tooltip_text(self, instance: Any, tooltip_text: str) -> None:
        """Update the tooltip text.

        This method is called whenever the `tooltip_text` property
        changes. It delegates to
        :meth:`~morphui.uix.tooltip.MorphTooltip.update_tooltip_text`
        on the tooltip widget, which each tooltip subclass implements
        to update the correct label.
        """
        if self.tooltip is None:
            return

        self.tooltip.update_tooltip_text(tooltip_text)