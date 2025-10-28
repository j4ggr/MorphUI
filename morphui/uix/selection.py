from typing import Any
from typing import Dict

from kivy.metrics import dp
from kivy.animation import Animation
from kivy.properties import StringProperty
from kivy.properties import ObjectProperty
from kivy.properties import BooleanProperty
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
    
    selected = BooleanProperty(False)
    """Indicates whether the checkbox is selected (checked) or not.

    When set to `True`, the checkbox is in the 'selected' state 
    (checked). When set to `False`, it is in the 'normal' state 
    (unchecked).

    :attr:`selected` is a :class:`~kivy.properties.BooleanProperty` and
    defaults to `False`.
    """
    
    selected_icon = StringProperty("checkbox-marked")
    """Icon name for the 'selected' state of the checkbox.

    The icon is displayed when the checkbox is in the 'selected' state
    (i.e., checked). The icon name should correspond to a valid icon in
    the Material Design Icons library.

    :attr:`selected_icon` is a :class:`~kivy.properties.StringProperty` 
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

    selection_animation_duration: float = NumericProperty(0.2)
    """Duration of the selection animation in seconds."
    
    Specifies the duration of the animation that plays when the checkbox
    transitions between the 'normal' and 'active' states.

    :attr:`selection_animation_duration` is a
    :class:`~kivy.properties.NumberProperty` and defaults to `0.2`.
    """

    selection_animation_out: Animation = ObjectProperty()
    """Animation played when the checkbox selection flag changes.

    This animation is triggered when the checkbox transitions from 
    full scale to a zero scale.
    
    :attr:`selection_animation_out` is a 
    :class:`~kivy.animation.Animation` and defaults to an animation that
    scales the checkbox down."""

    selection_animation_in: Animation = ObjectProperty()
    """Animation played when the :attr:`selection_animation_out`
    completes.

    This animation is triggered after the checkbox has been scaled down
    to zero, scaling it back up to full size.

    :attr:`selection_animation_in` is a 
    :class:`~kivy.animation.Animation` and defaults to an animation that
    scales the checkbox back up.
    """
    default_config: Dict[str, Any] = (
        MorphIconLabel.default_config.copy() | dict(
        theme_color_bindings=dict(
            surface_color='transparent_color',
            content_color='content_surface_color',
            selected_content_color='primary_color',
            disabled_content_color='outline_color',),
        auto_size=False,
        round_sides=True,
        size_hint=(None, None),
        size=(dp(24), dp(24)),))

    def __init__(self, **kwargs) -> None:
        self.selection_animation_out = Animation(
            scale_factor_x=0.0,
            scale_factor_y=0.0,
            duration=self.selection_animation_duration / 2,)
        self.selection_animation_in = Animation(
            scale_factor_x=1.0,
            scale_factor_y=1.0,
            duration=self.selection_animation_duration / 2,)
        super().__init__(**kwargs)

        self.selection_animation_out.bind(
            on_complete=lambda *_: self.selection_animation_in.start(self))
        
        self.bind(
            normal_icon=self._update_icon,
            selected_icon=self._update_icon,
            selected=self._update_icon,)
        
        self._update_icon()

    def on_active(self, instance: Any, active: bool) -> None:
        """Handle the `active` property change. 
        
        Triggers the selection animations and updates the icon based on
        the new state. The `active` property is inherited from
        MorphToggleButtonBehavior.
        
        Parameters
        ----------
        instance : Any
            The instance of the widget where the property changed.
        active : bool
            The new value of the `active` property.
        """
        self.selection_animation_in.cancel(self)
        self.selection_animation_out.start(self)
        self.selected = active
    
    def _update_icon(self, *args) -> None:
        """Update the displayed icon based on the `selected` state."""
        # target_icon = self.active_icon if self.selected else self.normal_icon
        # anim = Animation(duration=0.1)
        # anim += Animation(opacity=0, duration=0.1)
        # anim.bind(on_complete=lambda *args: setattr(self, 'icon', target_icon))
        # anim += Animation(opacity=1, duration=0.1)
        # anim.start(self)
        self.icon = (
            self.selected_icon if self.selected else self.normal_icon)
