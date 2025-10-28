from typing import Any
from typing import Dict

from kivy.metrics import dp
from kivy.animation import Animation
from kivy.properties import StringProperty
from kivy.properties import ObjectProperty
from kivy.properties import NumericProperty

from .label import MorphIconLabel

from .behaviors import MorphScaleBehavior
from .behaviors import MorphRippleBehavior
from .behaviors import MorphToggleButtonBehavior


__all__ = [
    'MorphCheckbox',]


class MorphCheckbox(
        MorphRippleBehavior,
        MorphToggleButtonBehavior,
        MorphScaleBehavior,
        MorphIconLabel,):

    active_icon = StringProperty("checkbox-marked")
    """Icon name for the 'active' state of the checkbox.

    The icon is displayed when the checkbox is in the 'active' state
    (i.e., checked). The icon name should correspond to a valid icon in
    the Material Design Icons library.

    :attr:`active_icon` is a :class:`~kivy.properties.StringProperty` 
    and defaults to `"checkbox-marked"`.
    """

    normal_icon = StringProperty("checkbox-blank-outline")
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
