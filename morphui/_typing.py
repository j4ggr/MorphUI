from typing import Literal
from typing import TypeAlias

from material_color_utilities import DynamicScheme


__all__ = [
    'MaterialDynamicScheme',
    'State',
    'SurfaceState',
    'InteractionState',
    'ContentState',
    'OverlayState',]

#TODO: Remove MaterialDynamicScheme if not needed after refactor
MaterialDynamicScheme: TypeAlias = DynamicScheme
"""TypeAlias for all supported Material You dynamic color schemes."""

State: TypeAlias = Literal[
    'disabled',
    'error',
    'pressed',
    'hovered',
    'focus',
    'active',
    'resizing',
    'dragging',
    'normal',]
"""TypeAlias for all possible states.

These states represent various interaction and visual states
that a widget can have. They are used to manage the appearance
and behavior of widgets based on user interactions and other
conditions.
"""

SurfaceState: TypeAlias = Literal[
    'disabled',
    'error',
    'focus',
    'active',
    'normal',]
"""TypeAlias for surface-related states.

These states typically affect the background or surface
appearance of a widget. They are used to indicate the widget's
interaction state, such as whether it is disabled, active, or
focused. The 'normal' state represents the default state
when no other states are active.

Notes
-----
These states are ordered by precedence, with 'disabled' having the
highest precedence and 'normal' the lowest."""

InteractionState: TypeAlias = Literal[
    'disabled',
    'pressed',
    'focus',
    'hovered',
    'normal',]
"""TypeAlias for interaction-related states.

These states typically affect how a widget responds to user
interactions, such as mouse clicks or keyboard focus. They are
used to manage the widget's response to user input and
interactions.

Notes
-----
These states are ordered by precedence, with 'disabled' having the
highest precedence and 'normal' the lowest.
"""

ContentState: TypeAlias = Literal[
    'disabled',
    'error',
    'focus',
    'hovered',
    'active',
    'normal',]
"""TypeAlias for content-related states.

These states typically affect the content or foreground
appearance of a widget. They are used to indicate the widget's
interaction state, such as whether it is disabled, active, or focused. 
The 'normal' state represents the default state when no other states 
are active.

Notes
-----
These states are ordered by precedence, with 'disabled' having the
highest precedence and 'normal' the lowest.
"""

OverlayState: TypeAlias = Literal[
    'disabled',
    'resizing',
    'dragging',
    'normal',]
"""TypeAlias for overlay-related states.

These states typically affect overlay elements, such as resizing and 
dragging. They are used to manage the appearance and behavior of overlay
elements based on user interactions and other conditions.

Notes
-----
These states are ordered by precedence, with 'disabled' having the
highest precedence and 'normal' the lowest.
"""
