"""Reusable container widgets for MorphUI.

This module provides base container classes that implement common layout
patterns used across multiple components.
"""

from typing import Any
from typing import Dict

from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout

from morphui.utils import clean_config
from morphui.uix.label import MorphTextLabel
from morphui.uix.label import MorphLeadingIconLabel
from morphui.uix.label import MorphTrailingIconLabel
from morphui.uix.behaviors import MorphAutoSizingBehavior
from morphui.uix.behaviors import MorphIdentificationBehavior
from morphui.uix.behaviors import MorphLeadingWidgetBehavior
from morphui.uix.behaviors import MorphLabelWidgetBehavior
from morphui.uix.behaviors import MorphTrailingWidgetBehavior


__all__ = [
    'MorphIconLabelContainer',
    'MorphIconLabelIconContainer',
    'MorphLabelIconContainer',]


class _MorphBaseContainer(
        MorphIdentificationBehavior,
        MorphAutoSizingBehavior,
        BoxLayout):
    """Base container class with shared configuration and initialization.
    
    This internal base class consolidates common functionality across
    all container widgets to eliminate code duplication.
    """

    _default_child_widgets: Dict[str, Any] = {}
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

    This dictionary contains default property values. These defaults 
    can be overridden by subclasses or during instantiation.
    """

    def __init__(self, **kwargs) -> None:
        config = clean_config(self.default_config, kwargs)
        
        # Create default child widgets if not provided
        for key, widget_cls in self._default_child_widgets.items():
            if key not in config and widget_cls is not None:
                config[key] = widget_cls()
        
        super().__init__(**config)
        
        # Initialize child widgets with stored values
        self._initialize_child_widgets()
    
    def _initialize_child_widgets(self) -> None:
        """Initialize child widgets. Override in subclasses."""
        pass


class MorphIconLabelContainer(
        MorphLeadingWidgetBehavior,
        MorphLabelWidgetBehavior,
        _MorphBaseContainer):
    """Container with leading icon and text label.
    
    This container provides a horizontal layout with two child widgets:
    a leading icon and a text label. It is designed to be inherited by
    components that need this layout pattern (e.g., icon buttons, list
    items with icons).
    
    This class only provides the core layout and widget management.
    Subclasses should add additional behaviors like:
    - :class:`~morphui.uix.behaviors.MorphColorThemeBehavior`
    - :class:`~morphui.uix.behaviors.MorphInteractionLayerBehavior`
    - :class:`~morphui.uix.behaviors.MorphSurfaceLayerBehavior`
    
    Attributes
    ----------
    leading_icon : str
        Icon name for the leading widget
    label_text : str
        Text content for the label widget
        
    Examples
    --------
    ```python
    from morphui.uix.container import MorphIconLabelContainer
    
    class MyButton(MorphIconLabelContainer):
        default_config = MorphIconLabelContainer.default_config.copy()
        
    button = MyButton(
        leading_icon='home',
        label_text='Home')
    ```
    """

    _default_child_widgets = {
        'leading_widget': MorphLeadingIconLabel,
        'label_widget': MorphTextLabel,}

    def _initialize_child_widgets(self) -> None:
        if self.leading_widget is not None:
            self.add_widget(self.leading_widget)
            self.leading_widget.icon = self.leading_icon

        if self.label_widget is not None:
            self.add_widget(self.label_widget)
            self.label_widget.text = self.label_text


class MorphIconLabelIconContainer(
        MorphTrailingWidgetBehavior,
        MorphIconLabelContainer):
    """Container with leading icon, text label, and trailing icon.
    
    This container provides a horizontal layout with three child widgets:
    a leading icon, a text label, and a trailing icon. It is designed
    to be inherited by components that need this layout pattern (e.g.,
    menu items, list items, chips).
    
    This class only provides the core layout and widget management.
    Subclasses should add additional behaviors like:
    - :class:`~morphui.uix.behaviors.MorphColorThemeBehavior`
    - :class:`~morphui.uix.behaviors.MorphInteractionLayerBehavior`
    - :class:`~morphui.uix.behaviors.MorphSurfaceLayerBehavior`
    
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
    from morphui.uix.container import MorphIconLabelIconContainer
    
    class MyMenuItem(MorphIconLabelIconContainer):
        default_config = MorphIconLabelIconContainer.default_config.copy()
        
    item = MyMenuItem(
        leading_icon='home',
        label_text='Home',
        trailing_icon='chevron-right')
    ```
    """

    _default_child_widgets = {
        'leading_widget': MorphLeadingIconLabel,
        'label_widget': MorphTextLabel,
        'trailing_widget': MorphTrailingIconLabel,}

    def _initialize_child_widgets(self) -> None:
        super()._initialize_child_widgets()
        
        if self.trailing_widget is not None:
            self.add_widget(self.trailing_widget)
            self.trailing_widget.icon = self.trailing_icon


class MorphLabelIconContainer(
        MorphTrailingWidgetBehavior,
        MorphLabelWidgetBehavior,
        _MorphBaseContainer):
    """Container with text label and trailing icon.
    
    This container provides a horizontal layout with two child widgets:
    a text label and a trailing icon. It is designed to be inherited by
    components that need this layout pattern (e.g., buttons with trailing
    icons, list items).
    
    This class only provides the core layout and widget management.
    Subclasses should add additional behaviors like:
    - :class:`~morphui.uix.behaviors.MorphColorThemeBehavior`
    - :class:`~morphui.uix.behaviors.MorphInteractionLayerBehavior`
    - :class:`~morphui.uix.behaviors.MorphSurfaceLayerBehavior`
    
    Attributes
    ----------
    label_text : str
        Text content for the label widget
    trailing_icon : str
        Icon name for the trailing widget
        
    Examples
    --------
    ```python
    from morphui.uix.container import MorphLabelIconContainer
    
    class MyButton(MorphLabelIconContainer):
        default_config = MorphLabelIconContainer.default_config.copy()

    button = MyButton(
        label_text='Settings',
        trailing_icon='chevron-right')
    ```
    """

    _default_child_widgets = {
        'label_widget': MorphTextLabel,
        'trailing_widget': MorphTrailingIconLabel,}

    def _initialize_child_widgets(self) -> None:
        if self.label_widget is not None:
            self.add_widget(self.label_widget)
            self.label_widget.text = self.label_text

        if self.trailing_widget is not None:
            self.add_widget(self.trailing_widget)
            self.trailing_widget.icon = self.trailing_icon
