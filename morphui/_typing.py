from typing import Literal
from typing import TypeAlias

from materialyoucolor.scheme.scheme_tonal_spot import SchemeTonalSpot
from materialyoucolor.scheme.scheme_expressive import SchemeExpressive
from materialyoucolor.scheme.scheme_fruit_salad import SchemeFruitSalad
from materialyoucolor.scheme.scheme_monochrome import SchemeMonochrome
from materialyoucolor.scheme.scheme_rainbow import SchemeRainbow
from materialyoucolor.scheme.scheme_vibrant import SchemeVibrant
from materialyoucolor.scheme.scheme_neutral import SchemeNeutral
from materialyoucolor.scheme.scheme_fidelity import SchemeFidelity
from materialyoucolor.scheme.scheme_content import SchemeContent


__all__ = [
    'MaterialDynamicScheme',
    'State',
    'SurfaceState',
    'InteractionState',
    'ContentState',
    'OverlayState',]

MaterialDynamicScheme: TypeAlias = (
    SchemeTonalSpot
    | SchemeExpressive
    | SchemeFruitSalad
    | SchemeMonochrome
    | SchemeRainbow
    | SchemeVibrant
    | SchemeNeutral
    | SchemeFidelity
    | SchemeContent)
"""TypeAlias for all supported Material You dynamic color schemes."""

State: TypeAlias = Literal[
    'disabled',
    'error',
    'pressed',
    'hovered',
    'focus',
    'active',
    'selected',
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
    'selected',
    'normal',]
"""TypeAlias for surface-related states.

These states typically affect the background or surface
appearance of a widget. They are used to indicate the widget's
interaction state, such as whether it is disabled, active, or
selected. The 'normal' state represents the default state
when no other states are active.

Notes
-----
These states are ordered by precedence, with 'disabled' having the
highest precedence and 'normal' the lowest."""

InteractionState: TypeAlias = Literal[
    'disabled',
    'pressed',
    'hovered',
    'focus',
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
    'hovered',
    'active',
    'selected',
    'normal',]
"""TypeAlias for content-related states.

These states typically affect the content or foreground
appearance of a widget. They are used to indicate the widget's
interaction state, such as whether it is disabled, active, or
selected. The 'normal' state represents the default state
when no other states are active.

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
