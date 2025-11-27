from typing import Any
from typing import Dict
from typing import Tuple

from kivy.metrics import dp
from kivy.animation import Animation
from kivy.properties import StringProperty
from kivy.properties import NumericProperty
from kivy.properties import BooleanProperty
from kivy.uix.floatlayout import FloatLayout

from morphui.uix.label import MorphIconLabel

from morphui.uix.behaviors import MorphIconBehavior
from morphui.uix.behaviors import MorphHoverBehavior
from morphui.uix.behaviors import MorphScaleBehavior
from morphui.uix.behaviors import MorphRippleBehavior
from morphui.uix.behaviors import MorphColorThemeBehavior
from morphui.uix.behaviors import MorphRoundSidesBehavior
from morphui.uix.behaviors import MorphSurfaceLayerBehavior
from morphui.uix.behaviors import MorphContentLayerBehavior
from morphui.uix.behaviors import MorphToggleButtonBehavior
from morphui.uix.behaviors import MorphIdentificationBehavior
from morphui.uix.behaviors import MorphInteractionLayerBehavior

from morphui.utils import clean_config


__all__ = [
    'MorphCheckbox',
    'MorphRadioButton',
    'MorphSwitch',]


class MorphCheckbox(
        MorphRippleBehavior,
        MorphToggleButtonBehavior,
        MorphScaleBehavior,
        MorphIconLabel,):

    default_config: Dict[str, Any] = (
        MorphIconLabel.default_config.copy() | dict(
        theme_color_bindings=dict(
            normal_surface_color='transparent_color',
            normal_content_color='content_surface_color',
            active_content_color='primary_color',
            disabled_content_color='outline_color',),
        normal_icon='checkbox-blank-outline',
        active_icon='checkbox-marked',
        auto_size=True,
        round_sides=True,
        padding=dp(1),
        scale_animation_duration=0.1,))

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        self.bind(active=self._update_icon,)
        
        self._update_icon()

    def on_active(self, instance: Any, active: bool) -> None:
        """Handle the `active` property change. 
        
        Triggers the check animations and updates the icon based on
        the new state. The `active` property is inherited from
        MorphToggleButtonBehavior.
        
        Parameters
        ----------
        instance : Any
            The instance of the widget where the property changed.
        active : bool
            The new value of the `active` property.
        """
        def on_scale_out_complete(anim, widget):
            """Called when scale out animation completes."""
            self._update_icon()
            self.animate_scale_in()
            
        self.animate_scale_out(callback=on_scale_out_complete)


class MorphRadioButton(MorphCheckbox):
    """A radio button widget that allows selection within a group.

    This widget extends the MorphCheckbox to provide radio button
    functionality, where only one button in a group can be active at
    a time.

    Inherits from
    -------------
    :class:`~morphui.uix.selection.MorphCheckbox`
    """

    default_config: Dict[str, Any] = (
        MorphCheckbox.default_config.copy() | dict(
        normal_icon='radiobox-blank',
        active_icon='radiobox-marked',
        ripple_enabled=False,
        allow_no_selection=False,))


class ThumbSwitch(
        MorphIconLabel):
    """The thumb icon for the MorphSwitch widget.

    This class represents the thumb component of a switch, which
    moves between 'on' and 'off' positions when the switch is toggled.
    """

    active: bool = BooleanProperty(False)
    """Indicates whether the thumb switch is in the 'active' state.

    :attr:`active` is a :class:`~kivy.properties.BooleanProperty` and
    defaults to `False`."""

    default_config: Dict[str, Any] = dict(
        theme_color_bindings=dict(
            normal_surface_color='content_surface_color',
            active_surface_color='content_primary_color',
            disabled_surface_color='outline_color',
            normal_content_color='surface_dim_color',
            active_content_color='primary_color',),
        font_name='MaterialIcons',
        typography_role='Label',
        typography_size='large',
        size_hint=(None, None),
        round_sides=True,
        auto_size=False,
        padding=dp(0),
        halign='center',
        valign='center',)
    
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)


class MorphSwitch(
        MorphIconBehavior,
        MorphIdentificationBehavior,
        MorphRoundSidesBehavior,
        MorphToggleButtonBehavior,
        MorphColorThemeBehavior,
        MorphHoverBehavior,
        MorphContentLayerBehavior,
        MorphInteractionLayerBehavior,
        MorphSurfaceLayerBehavior,
        FloatLayout,):
    """A switch widget that allows toggling between 'on' and 'off' 
    states.
    """

    active_icon: StringProperty = StringProperty('check')
    """Icon name for the 'active' state of the switch thumb.

    The icon is displayed on the thumb when the switch is in the
    'active' state (i.e., switched on). The icon name should correspond
    to a valid icon in the Material Design Icons library.

    :attr:`active_icon` is a :class:`~kivy.properties.StringProperty` and
    defaults to `"checkbox-marked-circle"`.
    """

    normal_icon: StringProperty = StringProperty('')
    """Icon name for the 'normal' state of the switch thumb.

    The icon is displayed on the thumb when the switch is in the
    'normal' state (i.e., switched off). The icon name should correspond
    to a valid icon in the Material Design Icons library. If no icon is
    specified, no icon will be shown in the 'normal' state and the
    thumb will be smaller. A common choice for a switch in the 'off'
    state is `"close"`.

    :attr:`normal_icon` is a :class:`~kivy.properties.StringProperty` and
    defaults to `"checkbox-blank-circle"`.
    """
    
    minimum_padding: float = NumericProperty(dp(4))
    """The minimum padding around the switch thumb.
    
    This property defines the minimum padding applied to the switch
    thumb, ensuring that it has enough space to be visually distinct
    and not overlap with the switch's edges.

    :attr:`minimum_padding` is a 
    :class:`~kivy.properties.NumericProperty` and defaults to `dp(2)`.
    """

    switch_animation_duration: float = NumericProperty(0.15)
    """Duration of the switch toggle animation in seconds.

    Specifies the duration of the animation that plays when the switch
    is toggled between the 'on' and 'off' states.

    :attr:`switch_animation_duration` is a
    :class:`~kivy.properties.NumberProperty` and defaults to `0.15`.
    """

    switch_animation_transition: str = StringProperty('out_sine')
    """Transition type for the switch toggle animation.

    :attr:`switch_animation_transition` is a
    :class:`~kivy.properties.StringProperty` and defaults to `'out_sine'`.
    """

    default_config: Dict[str, Any] = dict(
        theme_color_bindings=dict(
            normal_surface_color='surface_dim_color',
            active_surface_color='primary_color',
            normal_border_color='outline_color',
            active_border_color='primary_color',),
        round_sides=True,
        size_hint=(None, None),
        width=dp(39),
        height=dp(24),)
    """Default configuration for the MorphSwitch widget."""

    def __init__(self, kw_thumb: Dict[str, Any] = {}, **kwargs) -> None:
        config = clean_config(self.default_config, kwargs)
        self.thumb = ThumbSwitch(**kw_thumb)
        super().__init__(**config)
        self.add_widget(self.thumb)

        self.bind(
            pos=self._update_thumb,
            size=self._update_thumb,)
        self._update_thumb()

    def _do_press(self, *args) -> None:
        """Handle the `pressed` event to toggle the switch state.

        This method is called when the switch is pressed, toggling
        its `active` state.

        Parameters
        ----------
        instance : Any
            The instance of the widget that was pressed.
        """
        super()._do_press(*args)
        self._update_thumb()

    def _resolve_thumb_diameter(self) -> float:
        """Calculate the diameter of the thumb based on the current 
        state.

        This method determines the appropriate diameter for the thumb
        based on whether the switch is pressed or active. If the switch
        is pressed, the thumb diameter is slightly increased. If the
        switch is active, the thumb takes the available size. If neither
        condition is met but a normal icon is set, the thumb diameter is
        reduced to two-thirds of the available size.

        Returns
        -------
        float
            The calculated diameter of the thumb.
        """
        if self.pressed:
            return self.height - dp(4)
        
        diameter = self.height - 2 * self.minimum_padding
        if self.active:
            return diameter
        
        if not self.normal_icon:
            return diameter * 2 / 3
        return diameter

    def _resolve_thumb_position(self) -> Tuple[float, float]:
        """Calculate the position of the thumb based on the current 
        state.

        This method determines the appropriate position for the thumb
        based on whether the switch is active or not.

        Returns
        -------
        Tuple[float, float]
            The calculated (x, y) position of the thumb.
        """
        diameter = self._resolve_thumb_diameter()
        y = self.y + self.height / 2 - diameter / 2
        delta = y - self.y
        if self.active:
            x = self.x + self.width - delta - diameter
        else:
            x = self.x + delta
        return (x, y)

    def _update_thumb(self, *args) -> None:
        """Update the layout of the thumb based on the current state.

        This method adjusts the size and position of the thumb
        according to the resolved diameter and position.
        """
        diameter = self._resolve_thumb_diameter()
        self.thumb.size = (diameter, diameter)
        self.thumb.pos = self._resolve_thumb_position()
        self._update_icon()
        self.thumb.active = self.active

    def _apply_icon(self, instance: Any, icon: str) -> None:
        """Apply the icon to the thumb based on the current state.

        This method overrides the base method to delegate icon
        application to the thumb."""
        return self.thumb._apply_icon(instance, icon)

    def _toggle_active(self, *args) -> None:
        """Toggle the `active` state of the switch."""
        self.active = not self.active

    def _do_release(self, *args) -> None:
        """Release the switch, toggling its `active` state."""
        super()._do_release(*args)

        Animation.cancel_all(self.thumb)
        pos = self._resolve_thumb_position()
        diameter = self._resolve_thumb_diameter()
        animation = Animation(
            pos=pos,
            size=(diameter, diameter),
            t=self.switch_animation_transition,
            d=self.switch_animation_duration,)
        animation.bind(on_complete=self._update_thumb)
        animation.start(self.thumb)
        
