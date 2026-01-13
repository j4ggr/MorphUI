from typing import Any
from typing import Dict
from typing import List
from typing import Tuple
from datetime import date
from warnings import warn

from kivy.metrics import dp
from kivy.uix.label import Label
from kivy.properties import ColorProperty
from kivy.properties import ObjectProperty
from kivy.properties import BooleanProperty

from morphui.utils import clean_config
from morphui.uix.label import MorphIconLabel
from morphui.uix.label import MorphSimpleIconLabel
from morphui.uix.label import MorphButtonTextLabel
from morphui.uix.label import MorphButtonLeadingIconLabel
from morphui.uix.label import MorphButtonTrailingIconLabel
from morphui.uix.behaviors import MorphIconBehavior
from morphui.uix.behaviors import MorphScaleBehavior
from morphui.uix.behaviors import MorphHoverBehavior
from morphui.uix.behaviors import MorphThemeBehavior
from morphui.uix.behaviors import MorphButtonBehavior
from morphui.uix.behaviors import MorphRippleBehavior
from morphui.uix.behaviors import MorphTooltipBehavior
from morphui.uix.behaviors import MorphElevationBehavior
from morphui.uix.behaviors import MorphAutoSizingBehavior
from morphui.uix.behaviors import MorphRoundSidesBehavior
from morphui.uix.behaviors import MorphToggleButtonBehavior
from morphui.uix.behaviors import MorphSurfaceLayerBehavior
from morphui.uix.behaviors import MorphContentLayerBehavior
from morphui.uix.behaviors import MorphCompleteLayerBehavior
from morphui.uix.behaviors import MorphHighlightLayerBehavior
from morphui.uix.behaviors import MorphDelegatedThemeBehavior
from morphui.uix.behaviors import MorphIdentificationBehavior
from morphui.uix.behaviors import MorphInteractionLayerBehavior
from morphui.uix.container import MorphIconLabelContainer
from morphui.uix.container import MorphLabelIconContainer


__all__ = [
    'MorphSimpleIconButton',
    'MorphButton',
    'MorphIconButton',
    'MorphTrailingIconButton',
    'MorphIconTextButton',
    'MorphTextIconButton',
    'MorphTextIconToggleButton',
    'MorphChipTrailingIconButton',
    'MorphTextFieldTrailingIconButton',
    'MorphDatePickerDayButton',]


class MorphSimpleIconButton(
        MorphIconBehavior,
        MorphAutoSizingBehavior,
        MorphThemeBehavior,
        MorphHoverBehavior,
        MorphRippleBehavior,
        MorphInteractionLayerBehavior,
        MorphContentLayerBehavior,
        MorphButtonBehavior,
        MorphTooltipBehavior,
        Label):
    """A simple icon button widget with ripple effect and MorphUI
    theming.

    This class is a lightweight button designed for displaying icons
    with ripple effects and theming support. It is useful for scenarios
    where a full-featured button is not required but icon interaction is
    needed (e.g., toolbar buttons, or within a chip).
    """

    default_config: Dict[str, Any] = dict(
        theme_color_bindings=dict(
            normal_surface_color='transparent_color',
            disabled_border_color='outline_variant_color',
            normal_content_color='content_surface_color',
            hovered_content_color='content_surface_variant_color'),
        typography_role=MorphIconLabel.default_config['typography_role'],
        typography_size=MorphIconLabel.default_config['typography_size'],
        font_name=MorphIconLabel.default_config['font_name'],
        halign='center',
        valign='center',
        ripple_enabled=True,
        ripple_color=None,
        ripple_layer='interaction',
        padding=dp(8),
        auto_size=True,)
    """Default configuration values for MorphSimpleIconButton.
    
    Provides standard icon button appearance and behavior settings:
    - Center alignment for icon visibility
    - Middle vertical alignment for centered appearance
    - Bounded colors for theme integration
    - Ripple effect for touch feedback
    - Auto-sizing to fit content
    These values can be overridden by subclasses or during 
    instantiation.
    """

    def __init__(self, **kwargs) -> None:
        config = clean_config(self.default_config, kwargs)
        super().__init__(**config)


class MorphButton(
        MorphTooltipBehavior,
        MorphRoundSidesBehavior,
        MorphIdentificationBehavior,
        MorphHoverBehavior,
        MorphThemeBehavior,
        MorphRippleBehavior,
        MorphCompleteLayerBehavior,
        MorphButtonBehavior,
        MorphAutoSizingBehavior,
        MorphElevationBehavior,
        Label):
    """A button widget with ripple effect and MorphUI theming.
    
    This class combines Kivy's TouchRippleButtonBehavior with MorphUI's
    MorphLabel to create a button that supports ripple effects and 
    theming.
    """
    default_config: Dict[str, Any] = dict(
        halign='center',
        valign='center',
        theme_color_bindings={
            'normal_surface_color': 'surface_container_color',
            'normal_border_color': 'outline_color',
            'disabled_border_color': 'outline_variant_color',
            'normal_content_color': 'content_surface_color',
            'hovered_content_color': 'content_surface_variant_color',},
        ripple_enabled=True,
        ripple_color=None,
        ripple_layer='interaction',
        padding=dp(8),
        auto_size=True,)
    """Default configuration values for MorphButton.

    Provides standard button appearance and behavior settings:
    - Center alignment for text readability
    - Middle vertical alignment for centered appearance
    - Bounded colors for theme integration
    - Ripple effect for touch feedback
    - Auto-sizing to fit content
    
    These values can be overridden by subclasses or during 
    instantiation."""

    def __init__(self, **kwargs) -> None:
        config = clean_config(self.default_config, kwargs)
        super().__init__(**config)


class MorphIconButton(
        MorphIconBehavior,
        MorphButton):
    """A button widget designed for icon display with ripple effect 
    and MorphUI theming.
    
    This class is similar to MorphButton but is intended for use with
    icon fonts or images, providing a button that supports ripple 
    effects and theming.
    """

    default_config: Dict[str, Any] = dict(
        font_name=MorphIconLabel.default_config['font_name'],
        halign='center',
        valign='center',
        theme_color_bindings={
            'normal_surface_color': 'surface_container_color',
            'normal_content_color': 'content_surface_color',
            'hovered_content_color': 'content_surface_variant_color',
            'normal_border_color': 'outline_color',},
        typography_role=MorphIconLabel.default_config['typography_role'],
        typography_size=MorphIconLabel.default_config['typography_size'],
        ripple_enabled=True,
        ripple_color=None,
        ripple_layer='interaction',
        auto_size=True,
        padding=dp(8),
        radius=[5] * 4,
        )
    """Default configuration values for MorphIconButton.

    Provides standard icon button appearance and behavior settings:
    - Center alignment for icon visibility
    - Middle vertical alignment for centered appearance
    - Bounded colors for theme integration
    - Ripple effect for touch feedback
    - Auto-sizing to fit content
    - Rounded corners for a modern look

    These values can be overridden by subclasses or during 
    instantiation.
    """


class MorphTrailingIconButton(
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


class MorphIconTextButton(
        MorphIconBehavior,
        MorphTooltipBehavior,
        MorphRoundSidesBehavior,
        MorphDelegatedThemeBehavior,
        MorphHoverBehavior,
        MorphThemeBehavior,
        MorphRippleBehavior,
        MorphCompleteLayerBehavior,
        MorphButtonBehavior,
        MorphElevationBehavior,
        MorphIconLabelContainer,):
    """A button widget that combines icon and text display with ripple
    effect and MorphUI theming.

    This class extends MorphIconLabelContainer to create a button
    that supports both icon and text content, along with ripple effects
    and theming.

    Examples
    --------
    Simple usage of MorphIconTextButton in a MorphApp:
    ```python
    from morphui.app import MorphApp
    from morphui.uix.button import MorphIconTextButton
    from morphui.uix.floatlayout import MorphFloatLayout

    class MyApp(MorphApp):
        def build(self) -> MorphFloatLayout:
            self.theme_manager.seed_color = 'morphui_teal'
            self.theme_manager.switch_to_dark()
            return MorphFloatLayout(
                MorphIconTextButton(
                    identity='icon_text_button',
                    normal_icon='language-python',
                    label_text='Icon Text Button',
                    pos_hint={'center_x': 0.5, 'center_y': 0.5},),)
    
    if __name__ == '__main__':
        MyApp().run()
    ```

    Toggle behavior with MorphToggleButtonBehavior:
    ```python
    from morphui.app import MorphApp
    from morphui.uix.button import MorphIconTextButton
    from morphui.uix.floatlayout import MorphFloatLayout
    from morphui.uix.behaviors import MorphToggleButtonBehavior

    class ToggleIconTextButton(
            MorphIconTextButton,
            MorphToggleButtonBehavior):
        pass

    class MyApp(MorphApp):
        def build(self) -> MorphFloatLayout:
            self.theme_manager.seed_color = 'morphui_teal'
            self.theme_manager.switch_to_dark()
            return MorphFloatLayout(
                ToggleIconTextButton(
                    identity='icon_text_button',
                    normal_icon='language-python',
                    active_icon='language-java',
                    label_text='Icon Text Button',
                    pos_hint={'center_x': 0.5, 'center_y': 0.5},),)
        
    if __name__ == '__main__':
        MyApp().run()
    """ 

    _default_child_widgets = {
        'leading_widget': MorphButtonLeadingIconLabel,
        'label_widget': MorphButtonTextLabel,}
    """Default child widgets for MorphIconTextButton.

    - `leading_widget`: An instance of :class:`~morphui.uix.label.
      MorphButtonLeadingIconLabel` for displaying the leading icon.
    - `label_widget`: An instance of :class:`~morphui.uix.label.
      MorphButtonTextLabel` for displaying the button text.
    """

    default_config: Dict[str, Any] = dict(
        theme_color_bindings={
            'normal_surface_color': 'surface_container_color',
            'normal_border_color': 'outline_color',
            'disabled_border_color': 'outline_variant_color',
            'normal_content_color': 'content_surface_color',
            'hovered_content_color': 'content_surface_variant_color',},
        orientation='horizontal',
        ripple_enabled=True,
        ripple_color=None,
        ripple_layer='interaction',
        padding=dp(8),
        spacing=dp(4),
        radius=dp(4),
        auto_size=True,
        delegate_content_color=True,)
    """Default configuration values for MorphIconTextButton.

    Provides standard button appearance and behavior settings:
    - Bounded colors for theme integration
    - Ripple effect for touch feedback
    - Auto-sizing to fit content
    - Delegation of content color theming to child widgets
    These values can be overridden by subclasses or during 
    instantiation.
    """

    def __init__(self, **kwargs) -> None:
        config = clean_config(self.default_config, kwargs)
        if 'leading_icon' in kwargs:
            warn(
                "`leading_icon` is not supported. Use `normal_icon` instead.",
                UserWarning,)
            config['normal_icon'] = kwargs.pop('leading_icon')

        super().__init__(**config)
        self.delegate_to_children = [
            self.leading_widget,
            self.label_widget,]
    
    def _update_icon(self, *args) -> None:
        """Update the leading icon based on the toggle state.

        This method switches the leading icon between `normal_icon` and
        `active_icon` depending on whether the chip is active or not.
        """
        self.leading_icon = self.icon


class MorphTextIconButton(
        MorphIconBehavior,
        MorphTooltipBehavior,
        MorphRoundSidesBehavior,
        MorphDelegatedThemeBehavior,
        MorphHoverBehavior,
        MorphThemeBehavior,
        MorphRippleBehavior,
        MorphCompleteLayerBehavior,
        MorphButtonBehavior,
        MorphElevationBehavior,
        MorphLabelIconContainer,):
    """A button widget that combines text and icon display with ripple
    effect and MorphUI theming.

    This class extends MorphIconTextButton to create a button that
    primarily displays text with an optional trailing icon, along with
    ripple effects and theming.
    """

    _default_child_widgets = {
        'label_widget': MorphButtonTextLabel,
        'trailing_widget': MorphButtonTrailingIconLabel,}
    """Default child widgets for MorphTextIconButton.

    - `label_widget`: An instance of :class:`~morphui.uix.label.
      MorphButtonTextLabel` for displaying the button text.
    - `trailing_widget`: An instance of :class:`~morphui.uix.label.
      MorphButtonTrailingIconLabel` for displaying the trailing icon.
    """

    default_config: Dict[str, Any] = dict(
        theme_color_bindings={
            'normal_surface_color': 'transparent_color',
            'normal_content_color': 'content_surface_color',
            'disabled_content_color': 'content_surface_variant_color',},
        orientation='horizontal',
        ripple_enabled=True,
        ripple_color=None,
        ripple_layer='interaction',
        padding=dp(8),
        spacing=dp(4),
        radius=dp(4),
        auto_size=True,
        delegate_content_color=True,)

    def __init__(self, **kwargs) -> None:
        config = clean_config(self.default_config, kwargs)
        if 'trailing_icon' in kwargs:
            warn(
                "`trailing_icon` is not supported. Use `normal_icon` instead.",
                UserWarning,)
            config['normal_icon'] = kwargs.pop('trailing_icon')
        super().__init__(**config)
        self.delegate_to_children = [
            self.label_widget,
            self.trailing_widget,]
        
    def _update_icon(self, *args) -> None:
        """Update the leading icon based on the toggle state.

        This method switches the leading icon between `normal_icon` and
        `active_icon` depending on whether the chip is active or not.
        """
        self.trailing_icon = self.icon


class MorphTextIconToggleButton(
        MorphToggleButtonBehavior,
        MorphTextIconButton,):
    """A toggle button widget that combines text and icon display with
    ripple effect and MorphUI theming.

    This class extends MorphTextIconButton and adds toggle behavior,
    allowing the button to switch between active and inactive states.
    By default, it uses 'menu-down' and 'menu-up' icons to indicate
    the toggle state.
    """
    default_config: Dict[str, Any] = (
        MorphTextIconButton.default_config.copy() | dict(
        normal_icon='menu-down',
        active_icon='menu-up',))


class MorphChipTrailingIconButton(
        MorphTrailingIconButton):
    """Trailing icon button for chips.
    
    Inherits from :class:`~morphui.uix.button.MorphTrailingIconButton`.
    """
    pass


class MorphTextFieldTrailingIconButton(MorphIconButton):
    """Trailing icon button for text fields.

    Used primarily in text fields where the trailing icon needs button
    behavior (e.g., clear text button).
    """

    disabled: bool = BooleanProperty(False)
    """Indicates whether the button is disabled.

    When True, the label is rendered in a disabled state, typically with
    a different color or style to indicate it is not interactive.

    :attr:`disabled` is a :class:`kivy.properties.BooleanProperty` and
    defaults to False.
    """

    focus: bool = BooleanProperty(False)
    """Indicates whether the button is focused.

    When set to True, the button is considered focused, which may
    affect its visual appearance and behavior.
    
    :attr:`focus` is a :class:`kivy.properties.BooleanProperty` and
    defaults to False."""

    error: bool = BooleanProperty(False)
    """Indicates whether the button is in an error state.

    When set to True, the button is considered to be in an error state,
    which may affect its visual appearance and behavior.

    :attr:`error` is a :class:`kivy.properties.BooleanProperty` and
    defaults to False.
    """

    default_config: Dict[str, Any] = dict(
        theme_color_bindings=dict(
            normal_content_color='primary_color',
            normal_surface_color='transparent_color',
            hovered_content_color='content_surface_variant_color',),
        font_name=MorphIconButton.default_config['font_name'],
        typography_role=MorphIconButton.default_config['typography_role'],
        typography_size=MorphIconButton.default_config['typography_size'],
        focus_state_opacity=0.0,
        halign='center',
        valign='center',
        round_sides=True,
        ripple_enabled=False,
        size_hint=(None, None),
        size=(dp(24), dp(24)),
        padding=dp(0),)


class MorphDatePickerDayButton(
        MorphRoundSidesBehavior,
        MorphIdentificationBehavior,
        MorphToggleButtonBehavior,
        MorphThemeBehavior,
        MorphContentLayerBehavior,
        MorphSurfaceLayerBehavior,
        MorphHighlightLayerBehavior,
        Label):
    """A button widget representing a day in a date picker.

    This class combines various MorphUI behaviors to create a button
    that represents a day in a date picker, with support for ripple
    effects, theming, and toggle behavior.
    """

    date_value: date = ObjectProperty(None)
    """The date value represented by the button.

    This property holds the date value that the button represents.

    :attr:`date_value` is a :class:`kivy.properties.ObjectProperty` and
    defaults to None.
    """

    is_start_day: bool = BooleanProperty(False)
    """Indicates whether the button represents the start day of a
    selected date range.

    When True, the button is styled to indicate it is the start day of a
    selected date range.

    :attr:`is_start_day` is a :class:`kivy.properties.BooleanProperty`
    and defaults to False.
    """

    is_end_day: bool = BooleanProperty(False)
    """Indicates whether the button represents the end day of a
    selected date range.

    When True, the button is styled to indicate it is the end day of a
    selected date range.

    :attr:`is_end_day` is a :class:`kivy.properties.BooleanProperty` and
    defaults to False.
    """

    is_in_range: bool = BooleanProperty(False)
    """Indicates whether the button is between the start and end days of
    a selected date range.

    When True, the button is styled to indicate it is between the start
    and end days of a selected date range.

    :attr:`is_in_range` is a :class:`kivy.properties.BooleanProperty`
    and defaults to False.
    """

    is_today: bool = BooleanProperty(False)
    """Indicates whether the button represents today's date.

    When True, the button is styled to indicate it represents today's
    date.

    :attr:`is_today` is a :class:`kivy.properties.BooleanProperty` and
    defaults to False.
    """

    today_border_color: List[float] = ColorProperty([0, 0, 0, 0])
    """Border color for today's date button.

    This property holds the RGBA color value used for the border of
    the button when it represents today's date.

    :attr:`today_border_color` is a
    :class:`~kivy.properties.ColorProperty` and defaults to
    `[0, 0, 0, 0]`.
    """

    default_config: Dict[str, Any] = dict(
        halign='center',
        valign='center',
        theme_color_bindings={
            'normal_surface_color': 'transparent_color',
            'active_surface_color': 'primary_container_color',
            'normal_content_color': 'content_surface_color',
            'active_content_color': 'on_primary_container_color',
            'normal_border_color': 'transparent_color',
            'today_border_color': 'tertiary_color',
            'normal_highlight_color': 'primary_container_color',},
        highlight_opacity=0.3,
        size_hint=(None, None),
        size=(dp(42), dp(42)),
        round_sides=True,)

    def __init__(self, **kwargs) -> None:
        config = clean_config(self.default_config, kwargs)
        super().__init__(**config)
            
        self.bind(
            is_today=self._set_border_color,
            is_in_range=self._update_highlight_flag,
            is_start_day=self._update_highlight_flag,
            is_end_day=self._update_highlight_flag,)
        self._update_highlight_flag()
        self._set_border_color()

    def on_date_value(self, instance: Any, date_value: date) -> None:
        """Handle changes to the date_value property.

        This method is called whenever the date_value property changes.
        It can be used to update the button's appearance or behavior
        based on the new date value.
        """
        self.text = str(date_value.day) if date_value else ''

    def _update_highlight_flag(self, *args) -> None:
        """Update the highlight layer based on range flags.

        This method updates the highlight layer whenever the
        `is_in_range`, `is_start_day`, or `is_end_day` properties
        change.
        """
        self.highlight = any([
            self.is_in_range,
            self.is_start_day,
            self.is_end_day,])

    def _get_highlight_layer_pos(self) -> Tuple[float, float]:
        """Get the position of the highlight layer.

        This method returns the position of the highlight layer based
        on the button's position and whether it is a start or end day.

        Returns
        -------
        List[float]
            The (x, y) position of the highlight layer.
        """
        x, y = super()._get_highlight_layer_pos()
        y = y + dp(4)

        if self.is_start_day:
            x += self.width / 2

        return x, y

    def _get_highlight_layer_size(self) -> Tuple[float, float]:
        """Get the size of the highlight layer.

        This method returns the size of the highlight layer based on
        the button's size and whether it is a start or end day.

        Returns
        -------
        List[float]
            The (width, height) size of the highlight layer.
        """
        width, height = super()._get_highlight_layer_size()
        height = height - dp(8)

        if self.is_start_day or self.is_end_day:
            width = width / 2

        return width, height

    def _get_border_color(self, *args) -> List[float]:
        """Get the border color based on the button state.

        This method returns the appropriate border color depending on
        whether the button represents today's date or is focused.

        Returns
        -------
        List[float]
            The RGBA color value for the border.
        """
        if self.is_today:
            return self.today_border_color
        return super()._get_border_color()

