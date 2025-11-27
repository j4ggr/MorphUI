from typing import List

from kivy.metrics import dp
from kivy.event import EventDispatcher
from kivy.graphics import Scale
from kivy.graphics import PopMatrix
from kivy.graphics import PushMatrix
from kivy.animation import Animation
from kivy.properties import ListProperty
from kivy.properties import StringProperty
from kivy.properties import BooleanProperty
from kivy.properties import NumericProperty
from kivy.properties import VariableListProperty
from kivy.properties import BoundedNumericProperty


__all__ = [
    'MorphRoundSidesBehavior',
    'MorphScaleBehavior',]


class MorphRoundSidesBehavior(EventDispatcher):
    """Behavior to enable automatic rounding of left and right sides.

    This behavior provides a `round_sides` property that, when enabled,
    automatically adjusts the widget's `radius` property to half of its
    height. This creates perfectly rounded left and right sides, useful
    for pill-shaped buttons, badges, or labels.

    When `round_sides` is set to True, the `radius` property is updated
    whenever the widget's size changes. The radius is calculated as half
    of the smaller dimension (width or height).

    If `height` is greater than `width`, the radius will be set to
    half of the `width`, resulting in a fully rounded shape. Otherwise,
    the radius will be half of the `height`, creating rounded sides.
    This ensures that the widget maintains a visually appealing shape
    regardless of its dimensions.

    For widgets that support an active state (e.g., navigation bars),
    the `active_radius` property can be used to define a different
    radius for the active state. When `active_radius_enabled` is set to
    True, the widget will smoothly animate between the rounded sides
    and the `active_radius` when transitioning to and from the active
    state. This creates a dynamic and engaging user experience.

    Examples
    --------
    ```python
    from morphui.app import MorphApp
    from morphui.uix.label import MorphIconLabel
    from morphui.uix.behaviors import MorphToggleButtonBehavior
    from morphui.uix.floatlayout import MorphFloatLayout

    class MyWidget(
            MorphToggleButtonBehavior,
            MorphIconLabel,):

        default_config = (
            MorphIconLabel.default_config.copy() | dict(
            theme_color_bindings=dict(
                normal_surface_color='transparent_color',
                content_color='content_surface_variant_color',
                normal_border_color='outline_color',
                active_surface_color='primary_color',
                active_content_color='content_primary_color',),
            round_sides=True,
            active_radius_enabled=True,))

    class MyApp(MorphApp):
        def build(self) -> MorphFloatLayout:
            self.theme_manager.switch_to_dark()
            return MorphFloatLayout(
                MyWidget(
                    identity='my_widget',
                    icon='language-python',
                    pos_hint={'center_x': 0.5, 'center_y': 0.5},),
                normal_surface_color=self.theme_manager.surface_color,)

    if __name__ == '__main__':
        MyApp().run()
    """
    active: bool = BooleanProperty(False)
    """Indicates whether the widget is in an active state.

    This property is used to determine if the widget should apply the
    `active_radius` when `active_radius_enabled` is set to True.

    :attr:`active` is a :class:`~kivy.properties.BooleanProperty` and
    defaults to False.
    """
    
    round_sides: bool = BooleanProperty(False)
    """Enable automatic rounding of left and right sides.
    
    When True, the radius property is automatically bound to half of the
    widget's height, creating perfectly rounded left and right sides
    regardless of the widget's height. This is useful for creating
    pill-shaped buttons, badges, or labels.
    
    When False, the radius property behaves normally and can be set
    independently.

    :attr:`round_sides` is a :class:`~kivy.properties.BooleanProperty` 
    and defaults to False.
    """

    active_radius: List[float] = VariableListProperty([dp(8)], length=4)
    """Radius to apply when the widget is in an active state.

    This property defines the radius values to be used when the widget
    is in an active state (e.g., a bar widget in a navigation bar).
    These values will be applied in addition to the round sides, 
    creating a visually appealing effect.

    :attr:`active_radius` is a 
    :class:`~kivy.properties.VariableListProperty` and defaults to
    `[dp(8), dp(8), dp(8), dp(8)]`.
    """

    active_radius_enabled: bool = BooleanProperty(False)
    """Enable or disable animation between round sides and active radius.

    When True, the animation will smoothly transition between the
    round sides and the active radius when the widget is in an active
    state. This creates a visually appealing effect that enhances the 
    user experience.

    When False, the active radius won't be applied at all.

    :attr:`active_radius_enabled` is a :class:`~kivy.properties.BooleanProperty`
    and defaults to False.
    """

    round_sides_animation_duration: float = NumericProperty(0.15)
    """Duration of the animation when transitioning between round sides
    and active radius.

    This property defines the duration (in seconds) of the animation
    that occurs when the widget transitions between the round sides
    and the active radius. A shorter duration results in a quicker
    transition, while a longer duration creates a smoother effect.

    :attr:`round_sides_animation_duration` is a
    :class:`~kivy.properties.NumericProperty` and defaults to 0.15 
    seconds."""

    round_sides_animation_transition: str = StringProperty('out_sine')
    """Transition type for the round sides animation.

    This property defines the type of transition used for the animation
    when the widget transitions between the round sides and the active
    radius. Different transition types create different visual effects,
    allowing for customization of the animation's feel.

    :attr:`round_sides_animation_transition` is a
    :class:`~kivy.properties.StringProperty` and defaults to 'out_sine'.
    """

    _original_radius: List[float] | None
    """Store original radius value when round_sides is enabled."""

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self._original_radius = getattr(self, 'radius', None)
        self.bind(
            size=self._update_round_sides,
            round_sides=self._update_round_sides,
            active_radius_enabled=self._update_round_sides,
            active=self.animate_active_radius,)
        self._update_round_sides(self, self.round_sides)

    def _resolve_radius(self) -> List[float]:
        """Determine the appropriate radius based on current state.
        
        This method calculates the radius to be applied based on whether
        the :attr:`round_sides` and :attr:`active_radius_enabled`
        properties are set. If :attr:`active_radius_enabled` is True,
        the :attr:`active_radius` is returned. If :attr:`round_sides`
        is True, the radius is calculated as half of the smaller
        dimension (width or height). If neither property is set,
        the original radius value is returned."""
        if self.active and self.active_radius_enabled:
            return self.active_radius
        
        if self.round_sides:
            radius_value = min(self.size) / 2
            return [radius_value] * 4
        
        if self._original_radius is not None:
            return self._original_radius

        return getattr(self, 'radius', [0.0] * 4)

    def _update_round_sides(self, *args) -> None:
        """Update the radius based on the current round sides setting.
        
        This method is called whenever the size of the widget changes or
        when the :attr:`round_sides` property is toggled. It recalculates
        the radius based on the current state.
        If :attr:`round_sides` is enabled, the radius is set to half of
        the smaller dimension (width or height). If disabled, the radius
        is restored to its original value.
        """
        self.radius = self._resolve_radius()

    def animate_active_radius(self, *args) -> None:
        """Animate to the active radius if enabled.
        
        This method initiates an animation to transition the widget's
        radius to the :attr:`active_radius` if 
        :attr:`active_radius_enabled` is set to True. The animation uses
        the specified duration and transition type for a smooth effect.
        """
        if not self.active_radius_enabled:
            return
        
        Animation.stop_all(self, 'radius')
        
        animation = Animation(
            radius=self._resolve_radius(),
            d=self.round_sides_animation_duration,
            t=self.round_sides_animation_transition,
        )
        animation.bind(on_complete=self.round_sides_animation_complete)
        animation.start(self)
    
    def round_sides_animation_complete(self, *args) -> None:
        """Callback for when the round sides animation completes.
        
        This method is called when the animation transitioning to the
        active radius completes. Override this method to perform any
        additional actions upon completion of the animation.
        """


class MorphScaleBehavior(EventDispatcher):
    """Behavior that adds scaling capabilities to widgets.

    This behavior provides properties to control scaling factors along
    the X, Y, and Z axes, as well as the origin point for scaling
    transformations. It utilizes Kivy's graphics instructions to apply
    scaling effects to the widget.

    The behavior also includes built-in animation methods to create
    scale in and scale out effects, allowing for smooth transitions
    between scaled states.

    Examples
    --------
    ```python
    from morphui.app import MorphApp
    from morphui.uix.button import MorphButton
    from morphui.uix.behaviors import MorphScaleBehavior
    from morphui.uix.floatlayout import MorphFloatLayout

    class MyWidget(MorphScaleBehavior, MorphButton):
        
        def on_release(self) -> None:
            self.animate_scale_out(
                callback=lambda *args: self.animate_scale_in(
                    callback=self.theme_manager.toggle_theme_mode))

    class MyApp(MorphApp):
        def build(self) -> MorphFloatLayout:
            layout = MorphFloatLayout(
                MyWidget(
                    text="Click Me",
                    pos_hint={'center_x': 0.5, 'center_y': 0.5},),
                theme_style='surface',)
            return layout

    if __name__ == '__main__':
        MyApp().run()
    """

    scale_factor_x: float = BoundedNumericProperty(
        1.0, min=0.0, errorvalue=0.0)
    """Scaling factor along the X-axis.

    Defines the scaling factor applied to the widget along the X-axis.
    A value of `1.0` means no scaling, values greater than `1.0` will
    enlarge the widget, and values between `0.0` and `1.0` will shrink 
    it. The value is clamped to be at least `0.0`.

    :attr:`scale_factor_x` is a
    :class:`~kivy.properties.BoundedNumericProperty` and defaults to 
    `1.0`.
    """

    scale_factor_y: float = BoundedNumericProperty(
        1.0, min=0.0, errorvalue=0.0)
    """Scaling factor along the Y-axis.

    Defines the scaling factor applied to the widget along the Y-axis.
    A value of `1.0` means no scaling, values greater than `1.0` will
    enlarge the widget, and values between `0.0` and `1.0` will shrink
    it. The value is clamped to be at least `0.0`.

    :attr:`scale_factor_y` is a
    :class:`~kivy.properties.BoundedNumericProperty` and defaults to
    `1.0`.
    """

    scale_factor_z: float = BoundedNumericProperty(
        1.0, min=0.0, errorvalue=0.0)
    """Scaling factor along the Z-axis.

    Defines the scaling factor applied to the widget along the Z-axis.
    A value of `1.0` means no scaling, values greater than `1.0` will
    enlarge the widget, and values between `0.0` and `1.0` will shrink
    it. The value is clamped to be at least `0.0`.

    :attr:`scale_factor_z` is a
    :class:`~kivy.properties.BoundedNumericProperty` and defaults to
    `1.0`.
    """

    scale_origin: List[float] = ListProperty([])
    """Origin point for scaling transformations.
    
    This property defines the point around which the scaling occurs.
    It is a 3D point represented by a list of two (x, y) or three floats 
    (x, y, z).

    :attr:`scale_origin` is a :class:`~kivy.properties.ListProperty`
    and defaults to `[]`.
    """

    scale_animation_duration: float = NumericProperty(0.2)
    """Duration for scale animations in seconds.
    
    This property defines the duration of scale animations when using
    the built-in animation methods like `animate_scale_in()` and
    `animate_scale_out()`.
    
    :attr:`scale_animation_duration` is a 
    :class:`~kivy.properties.NumericProperty` and defaults to `0.2`."""

    scale_animation_transition: str = StringProperty('in_out_back')
    """Transition type for scale animations.
    
    This property defines the easing transition used for scale animations.
    Common values include 'linear', 'in_out_sine', 'out_bounce', etc.
    See Kivy's Animation documentation for all available transitions.
    
    :attr:`scale_animation_transition` is a 
    :class:`~kivy.properties.StringProperty` and defaults to `'out_quart'`."""

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        with self.canvas.before:
            PushMatrix()
            self._scale_instruction = Scale(
                x=self.scale_factor_x,
                y=self.scale_factor_y,
                z=self.scale_factor_z,
                origin=self.resolved_scale_origin,)
        with self.canvas.after:
            PopMatrix()

        self.bind(
            scale_factor_x=self._update_scale,
            scale_factor_y=self._update_scale,
            scale_factor_z=self._update_scale,
            scale_origin=self._update_scale)
        
    @property
    def resolved_scale_origin(self) -> List[float]:
        """Get the resolved scale origin as a 3D point.

        This property returns the `scale_origin` property ensured to be
        a list of three floats (x, y, z). If only two values are 
        provided, it appends a `0.0` for the z-coordinate.

        Returns
        -------
        List[float]
            The resolved scale origin as a list of three floats.
        """
        if len(self.scale_origin) < 2:
            return [self.center_x, self.center_y, 0.0]
        return self.scale_origin

    def _update_scale(self, *args) -> None:
        """Update the scale transformation based on the current 
        properties.
        
        This method updates the Scale instruction with the current
        scaling factors and origin point whenever any of the related
        properties change.
        """
        self._scale_instruction.x = self.scale_factor_x
        self._scale_instruction.y = self.scale_factor_y
        self._scale_instruction.z = self.scale_factor_z
        self._scale_instruction.origin = self.resolved_scale_origin

    def animate_scale_in(self, callback=None) -> Animation:
        """Animate scale from 0 to 1 (scale in effect).
        
        This method animates the widget from completely scaled down (0)
        to normal size (1), creating a "scale in" or "zoom in" effect.
        It's commonly used for entrance animations or showing elements.
        
        Parameters
        ----------
        callback : callable, optional
            A function to call when the animation completes. The 
            callback will receive the Animation instance and the widget
            as arguments.
            
        Returns
        -------
        Animation
            The Animation instance that was started.
            
        Examples
        --------
        ```python
        # Simple scale in
        widget.animate_scale_in()
        
        # Scale in with callback
        def on_scale_complete(anim, widget):
            print("Scale in complete!")
            
        widget.animate_scale_in(callback=on_scale_complete)
        ```
        """
        Animation.stop_all(
            self, 'scale_factor_x', 'scale_factor_y', 'scale_factor_z')
        
        self.scale_factor_x = 0.0
        self.scale_factor_y = 0.0
        self.scale_factor_z = 0.0
        
        anim = Animation(
            scale_factor_x=1.0,
            scale_factor_y=1.0,
            scale_factor_z=1.0,
            duration=self.scale_animation_duration,
            transition=self.scale_animation_transition)
        
        if callback:
            anim.bind(on_complete=callback)
            
        anim.start(self)
        return anim

    def animate_scale_out(self, callback=None) -> Animation:
        """Animate scale from 1 to 0 (scale out effect).
        
        This method animates the widget from normal size (1) to
        completely scaled down (0), creating a "scale out" or 
        "zoom out" effect. It's commonly used for exit animations or 
        hiding elements.
        
        Parameters
        ----------
        callback : callable, optional
            A function to call when the animation completes. The 
            callback will receive the Animation instance and the widget
            as arguments.
            
        Returns
        -------
        Animation
            The Animation instance that was started.
            
        Examples
        --------
        ```python
        # Simple scale out
        widget.animate_scale_out()
        
        # Scale out with callback to hide widget
        def on_scale_complete(anim, widget):
            widget.opacity = 0  # Hide after scaling out
            
        widget.animate_scale_out(callback=on_scale_complete)
        ```
        """
        Animation.stop_all(
            self, 'scale_factor_x', 'scale_factor_y', 'scale_factor_z')
        
        self.scale_factor_x = 1.0
        self.scale_factor_y = 1.0
        self.scale_factor_z = 1.0
        
        anim = Animation(
            scale_factor_x=0.0,
            scale_factor_y=0.0,
            scale_factor_z=0.0,
            duration=self.scale_animation_duration,
            transition=self.scale_animation_transition)
        
        if callback:
            anim.bind(on_complete=callback)
            
        anim.start(self)
        return anim
