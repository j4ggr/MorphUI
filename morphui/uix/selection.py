from typing import Any
from typing import List
from typing import Dict

from kivy.metrics import dp
from kivy.metrics import sp
from kivy.animation import Animation
from kivy.properties import StringProperty
from kivy.properties import ObjectProperty
from kivy.properties import NumericProperty
from kivy.properties import VariableListProperty
from kivy.uix.floatlayout import FloatLayout

from .label import MorphIconLabel
from .label import MorphSimpleIconLabel

from .behaviors import MorphScaleBehavior
from .behaviors import MorphRippleBehavior
from .behaviors import MorphTextLayerBehavior
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
        # MorphRippleBehavior,
        MorphRoundSidesBehavior,
        MorphSimpleIconLabel):
    """The thumb icon for the MorphSwitch widget.

    This class represents the thumb component of a switch, which
    moves between 'on' and 'off' positions when the switch is toggled.
    """

    active: bool = StringProperty(False)
    """Indicates whether the thumb switch is in the 'active' state.

    :attr:`active` is a :class:`~kivy.properties.BooleanProperty` and
    defaults to `False`."""

    default_config: Dict[str, Any] = (
        MorphSimpleIconLabel.default_config.copy() | dict(
        # auto_size=True,
        size_hint=(None, None),
        round_sides=True,
        padding=dp(1),
        halign='center',
        valign='center',))
    
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.bind(size=self.setter('text_size'))


class MorphSwitch(
        MorphRoundSidesBehavior,
        MorphToggleButtonBehavior,
        MorphColorThemeBehavior,
        MorphTextLayerBehavior,
        FloatLayout,):
    """A switch widget that allows toggling between 'on' and 'off' 
    states.
    """

    active_icon: StringProperty = StringProperty('checkbox-marked-circle')
    """Icon name for the 'active' state of the switch thumb.

    The icon is displayed on the thumb when the switch is in the
    'active' state (i.e., switched on). The icon name should correspond
    to a valid icon in the Material Design Icons library.

    :attr:`active_icon` is a :class:`~kivy.properties.StringProperty` and
    defaults to `"checkbox-marked-circle"`.
    """

    normal_icon: StringProperty = StringProperty('checkbox-blank-circle')
    """Icon name for the 'normal' state of the switch thumb.

    The icon is displayed on the thumb when the switch is in the
    'normal' state (i.e., switched off). The icon name should correspond
    to a valid icon in the Material Design Icons library.

    :attr:`normal_icon` is a :class:`~kivy.properties.StringProperty` and
    defaults to `"checkbox-blank-circle"`.
    """
    padding: List[float] = VariableListProperty([dp(2)], length=4)
    """Padding around the switch thumb.

    :attr:`padding` is a :class:`~kivy.properties.VariableListProperty`
    of length 4 and defaults to `[dp(2), dp(2), dp(2), dp(2)]`.
    """

    default_config: Dict[str, Any] = dict(
        theme_color_bindings=dict(
            surface_color='secondary_color',
            active_surface_color='primary_color',
            content_color='content_surface_color',
            active_content_color='primary_color',
            disabled_content_color='outline_color',),
        round_sides=True,
        size_hint=(None, None),
        width=dp(52),
        height=dp(32),)
    
    def __init__(self, **kwargs) -> None:
        self.thumb = ThumbSwitch()
        config = clean_config(self.default_config, kwargs)
        super().__init__(**config)
        self.add_widget(self.thumb)

        self.bind(
            pos=self._update_thumb_appearance,
            size=self._update_thumb_appearance,
            active=self._update_thumb_appearance,
            content_color=self.thumb.setter('content_color'),
            active_content_color=self.thumb.setter('active_content_color'),
            disabled_content_color=self.thumb.setter('disabled_content_color'),)
        
        self.thumb.refresh_theme_colors()
        self._update_thumb_appearance()

    def on_pressed(self, instance: Any, pressed: bool) -> None:
        """Handle the `pressed` event to toggle the switch state.

        This method is called when the switch is pressed, toggling
        its `active` state.

        Parameters
        ----------
        instance : Any
            The instance of the widget that was pressed.
        """
        if pressed:
            pass
            # self.thumb.show_ripple_effect(self.thumb.center)

    def _update_thumb_appearance(self, *args) -> None:
        """Update the position, icon, and font size of the thumb based 
        on the `active` state.
        """
        Animation.stop_all(self.thumb)
        height = self.height - self.padding[1] - self.padding[3]
        self.thumb.size = (height, height)
        if self.active:
            self.thumb.icon = self.active_icon
            thumb_pos = (
                self.x + self.width - self.thumb.width - self.padding[2],
                self.y + self.height / 2 - self.thumb.height / 2,)
            font_size = sp(22)
        else:
            self.thumb.icon = self.normal_icon
            thumb_pos = (
                self.x + self.padding[0],
                self.y + self.padding[1],)
            font_size = sp(20)

        Animation(
            pos=thumb_pos,
            font_size=font_size,
            duration=0.2,
        ).start(self.thumb)
