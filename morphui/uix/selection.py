from typing import Any
from typing import Dict
from typing import Tuple

from kivy.clock import Clock
from kivy.metrics import dp
from kivy.animation import Animation
from kivy.properties import StringProperty
from kivy.properties import ObjectProperty
from kivy.properties import NumericProperty
from kivy.properties import BooleanProperty
from kivy.uix.floatlayout import FloatLayout

from .label import MorphIconLabel

from .behaviors import MorphHoverBehavior
from .behaviors import MorphScaleBehavior
from .behaviors import MorphRippleBehavior
from .behaviors import MorphSurfaceLayerBehavior
from .behaviors import MorphContentLayerBehavior
from .behaviors import MorphInteractionLayerBehavior
from .behaviors import MorphColorThemeBehavior
from .behaviors import MorphRoundSidesBehavior
from .behaviors import MorphToggleButtonBehavior

from ..utils import clean_config


__all__ = [
    'MorphCheckbox',
    'MorphRadioButton',
    'MorphSwitch',]


class MorphCheckbox(
        MorphRippleBehavior,
        MorphToggleButtonBehavior,
        MorphScaleBehavior,
        MorphIconLabel,):

    active_icon = StringProperty('checkbox-marked')
    """Icon name for the 'active' state of the checkbox.

    The icon is displayed when the checkbox is in the 'active' state
    (i.e., checked). The icon name should correspond to a valid icon in
    the Material Design Icons library.

    :attr:`active_icon` is a :class:`~kivy.properties.StringProperty` 
    and defaults to `"checkbox-marked"`.
    """

    normal_icon = StringProperty('checkbox-blank-outline')
    """Icon name for the 'normal' state of the checkbox.

    The icon is displayed when the checkbox is in the 'normal' state
    (i.e., unchecked). The icon name should correspond to a valid icon in
    the Material Design Icons library.

    :attr:`normal_icon` is a :class:`~kivy.properties.StringProperty` and
    defaults to `"checkbox-blank-outline"`.
    """

    check_animation_duration: float = NumericProperty(0.15)
    """Duration of the check animation in seconds.
    
    Specifies the duration of the animation that plays when the checkbox
    transitions between the 'normal' and 'active' states.

    :attr:`check_animation_duration` is a
    :class:`~kivy.properties.NumberProperty` and defaults to `0.15`.
    """

    check_animation_transition: str = StringProperty('out_sine')
    """Transition type for the check animation.

    This property defines the type of transition to use for the check
    animation. It should correspond to a valid transition type in Kivy's
    animation system.

    :attr:`check_animation_transition` is a
    :class:`~kivy.properties.StringProperty` and defaults to `'out_sine'`.
    """

    check_animation_out: Animation = ObjectProperty()
    """Animation played when the checkbox check flag changes.

    This animation is triggered when the checkbox transitions from
    full scale to a zero scale.

    :attr:`check_animation_out` is a
    :class:`~kivy.animation.Animation` and defaults to an animation that
    scales the checkbox down."""

    check_animation_in: Animation = ObjectProperty()
    """Animation played when the :attr:`check_animation_out`
    completes.

    This animation is triggered after the checkbox has been scaled down
    to zero, scaling it back up to full size.

    :attr:`check_animation_in` is a
    :class:`~kivy.animation.Animation` and defaults to an animation that
    scales the checkbox back up.
    """
    default_config: Dict[str, Any] = (
        MorphIconLabel.default_config.copy() | dict(
        theme_color_bindings=dict(
            surface_color='transparent_color',
            content_color='content_surface_color',
            active_content_color='primary_color',
            disabled_content_color='outline_color',),
        auto_size=True,
        round_sides=True,
        padding=dp(1),))

    def __init__(self, **kwargs) -> None:
        self.check_animation_out = Animation(
            scale_factor_x=0.0,
            scale_factor_y=0.0,
            transition=self.check_animation_transition,
            duration=self.check_animation_duration / 2,)
        self.check_animation_in = Animation(
            scale_factor_x=1.0,
            scale_factor_y=1.0,
            transition=self.check_animation_transition,
            duration=self.check_animation_duration / 2,)
        super().__init__(**kwargs)

        self.check_animation_out.bind(
            on_complete=lambda *_: self.check_animation_in.start(self))

        self.bind(
            normal_icon=self._update_icon,
            active_icon=self._update_icon,
            active=self._update_icon,)
        
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
        self.check_animation_in.cancel(self)
        self.check_animation_out.start(self)
    
    def _update_icon(self, *args) -> None:
        """Update the displayed icon based on the `active` state."""
        self.icon = (
            self.active_icon if self.active else self.normal_icon)


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
        normal_icon='checkbox-blank-circle-outline',
        active_icon='checkbox-marked-circle',
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
            surface_color='content_surface_color',
            active_surface_color='content_primary_color',
            disabled_surface_color='outline_color',
            content_color='surface_dim_color',
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
    to a valid icon in the Material Design Icons library.

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
            surface_color='surface_dim_color',
            active_surface_color='primary_color',
            border_color='outline_color',
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
        self._set_icon()
        self.thumb.active = self.active
            
    def _set_icon(self, *args) -> None:
        """Set the icon of the thumb based on the `active` state."""
        self.thumb.icon = self.active_icon if self.active else self.normal_icon

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
            duration=self.switch_animation_duration,
            transition=self.switch_animation_transition,
            )
        animation.bind(on_complete=self._update_thumb)
        animation.start(self.thumb)
        
