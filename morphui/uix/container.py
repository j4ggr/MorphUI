"""Reusable container widgets for MorphUI.

This module provides base container classes that implement common layout
patterns used across multiple components.
"""

from typing import Any
from typing import Dict

from kivy.metrics import dp
from kivy.properties import BooleanProperty

from morphui.utils import clean_config
from morphui.uix.label import MorphTextLabel
from morphui.uix.label import MorphLeadingIconLabel
from morphui.uix.label import MorphTrailingIconLabel
from morphui.uix.boxlayout import MorphSimpleBoxLayout
from morphui.uix.behaviors import MorphLeadingWidgetBehavior
from morphui.uix.behaviors import MorphLabelWidgetBehavior
from morphui.uix.behaviors import MorphTrailingWidgetBehavior


__all__ = [
    'MorphIconLabelContainer',
    'MorphIconLabelIconContainer',
    'MorphLabelIconContainer',]


class _MorphBaseContainer(MorphSimpleBoxLayout):
    """Base container class with shared configuration and initialization.
    
    This internal base class consolidates common functionality across
    all container widgets to eliminate code duplication.
    """
    
    disabled: bool = BooleanProperty(False)
    """Whether the container is disabled.
    
    This property can be used to control the disabled state of the
    container and its child widgets. When set to True, the container and
    its children will appear disabled and will not respond to user
    interactions.

    :attr:`disabled` is a :class:`~kivy.properties.BooleanProperty` and 
    defaults to False.
    """

    default_child_classes: Dict[str, Any] = {}
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
        config = self._prepare_config(**kwargs)
        super().__init__(**config)
        self._initialize_child_widgets()
    
    def _prepare_config(self, **kwargs) -> Dict[str, Any]:
        """Prepare configuration by merging defaults and instantiating
        child widgets.

        This method combines the default configuration with any
        overrides provided during instantiation. It also ensures that
        default child widgets are created if not explicitly provided.

        Parameters
        ----------
        **kwargs : Any
            Configuration overrides provided during instantiation.

        Returns
        -------
        Dict[str, Any]
            The final configuration dictionary with defaults applied
            and child widgets instantiated.
        """
        config = clean_config(self.default_config, kwargs)
        for key, widget_cls in self.default_child_classes.items():
            if key not in config and widget_cls is not None:
                config[key] = widget_cls()
        return config
    
    def _initialize_child_widgets(self) -> None:
        """Initialize child widgets. Override in subclasses.
        
        This method adds the child widgets to the container based on
        the `default_child_classes` mapping. Subclasses can override
        this method to customize the initialization process.
        """
        for key in self.default_child_classes.keys():
            widget = getattr(self, key, None)
            if widget is not None:
                self.add_widget(widget)
                getattr(self, f'refresh_{key}', lambda: None)()


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

    default_child_classes = {
        'leading_widget': MorphLeadingIconLabel,
        'label_widget': MorphTextLabel,}


class MorphIconLabelIconContainer(
        MorphLeadingWidgetBehavior,
        MorphLabelWidgetBehavior,
        MorphTrailingWidgetBehavior,
        _MorphBaseContainer):
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

    default_child_classes = {
        'leading_widget': MorphLeadingIconLabel,
        'label_widget': MorphTextLabel,
        'trailing_widget': MorphTrailingIconLabel,}


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

    default_child_classes = {
        'label_widget': MorphTextLabel,
        'trailing_widget': MorphTrailingIconLabel,}
