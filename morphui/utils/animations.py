"""
Animation utilities for MorphUI components
"""

from kivy.animation import Animation
from kivy.clock import Clock


def create_fade_animation(widget, fade_in=True, duration=0.3, callback=None):
    """Create a fade in/out animation for a widget"""
    if fade_in:
        widget.opacity = 0
        anim = Animation(opacity=1, duration=duration)
    else:
        anim = Animation(opacity=0, duration=duration)
    
    if callback:
        anim.bind(on_complete=callback)
    
    anim.start(widget)
    return anim


def create_slide_animation(widget, direction="up", distance=100, duration=0.3, callback=None):
    """Create a slide animation for a widget"""
    original_pos = widget.pos[:]
    
    # Set starting position based on direction
    if direction == "up":
        widget.y -= distance
        anim = Animation(y=original_pos[1], duration=duration)
    elif direction == "down":
        widget.y += distance
        anim = Animation(y=original_pos[1], duration=duration)
    elif direction == "left":
        widget.x += distance
        anim = Animation(x=original_pos[0], duration=duration)
    elif direction == "right":
        widget.x -= distance
        anim = Animation(x=original_pos[0], duration=duration)
    else:
        raise ValueError("Direction must be 'up', 'down', 'left', or 'right'")
    
    if callback:
        anim.bind(on_complete=callback)
    
    anim.start(widget)
    return anim


def create_scale_animation(widget, scale_from=0.8, scale_to=1.0, duration=0.3, callback=None):
    """Create a scale animation for a widget"""
    # Note: Kivy doesn't have built-in scale properties, so this would need custom implementation
    # or use of transforms. For now, we'll use size animation as an alternative
    original_size = widget.size[:]
    
    start_width = original_size[0] * scale_from
    start_height = original_size[1] * scale_from
    
    widget.size = (start_width, start_height)
    
    anim = Animation(
        size=(original_size[0] * scale_to, original_size[1] * scale_to),
        duration=duration
    )
    
    if callback:
        anim.bind(on_complete=callback)
    
    anim.start(widget)
    return anim


def create_color_animation(widget, color_property="color", target_color=None, duration=0.3, callback=None):
    """Create a color transition animation for a widget"""
    if target_color is None:
        return None
    
    anim_props = {color_property: target_color}
    anim = Animation(duration=duration, **anim_props)
    
    if callback:
        anim.bind(on_complete=callback)
    
    anim.start(widget)
    return anim


def delayed_call(callback, delay=1.0):
    """Execute a callback after a delay"""
    def wrapper(dt):
        callback()
    
    Clock.schedule_once(wrapper, delay)