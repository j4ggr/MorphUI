from typing import Any
from typing import List
from typing import Dict

from kivy.metrics import dp
from kivy.properties import ListProperty

from morphui.utils import clean_config
from morphui.uix.label import MorphSimpleLabel
from morphui.uix.button import MorphIconButton
from morphui.uix.behaviors import MorphMenuMotionBehavior
from morphui.uix.behaviors import MorphToggleButtonBehavior
from morphui.uix.gridlayout import MorphGridLayout


class MorphChartInfoLabel(MorphSimpleLabel):
    """Label to show chart information in a MorphChartCard
    
    Parameters
    ----------
    text : str
        Text to display in the label.
    """
    default_config: Dict[str, Any] = dict(
        theme_color_bindings=dict(
            content_color='content_surface_color',),
        typography_role='Label',
        typography_size='medium',
        typography_weight='Regular',
        halign='left',
        valign='center',
        auto_size=True,)


class MorphChartNavigationButton(MorphIconButton):
    """Button for chart navigation in a MorphChartCard
    """
    default_config: Dict[str, Any] = dict(
        font_name=MorphIconButton.default_config['font_name'],
        halign='center',
        valign='center',
        theme_color_bindings={
            'surface_color': 'transparent_color',
            'content_color': 'content_surface_color',
            'hovered_content_color': 'content_surface_variant_color',
            'border_color': 'outline_color',},
        typography_role=MorphIconButton.default_config['typography_role'],
        typography_size=MorphIconButton.default_config['typography_size'],
        ripple_enabled=True,
        ripple_color=None,
        ripple_layer='interaction',
        auto_size=True,
        round_sides=True,
        padding=dp(8),)


class MorphChartNavigationToggleButton(
        MorphToggleButtonBehavior,
        MorphChartNavigationButton):
    """Toggle button for chart navigation in a MorphChartCard.
    """
    default_config: Dict[str, Any] = (
        MorphChartNavigationButton.default_config.copy() | dict(
        theme_color_bindings={
            'surface_color': 'transparent_color',
            'active_surface_color': 'primary_color',
            'content_color': 'content_surface_color',
            'active_content_color': 'content_primary_color',
            'hovered_content_color': 'content_surface_variant_color',
            'border_color': 'outline_color',},
        active_radius_enabled=True,))


class MorphChartToolbarMenu(
        MorphMenuMotionBehavior,
        MorphGridLayout):
    """Toolbar menu container for MorphChartCard.
    """
    default_config: Dict[str, Any] = dict(
        theme_color_bindings={
            'surface_color': 'transparent_color',},
        cols=1,
        spacing=dp(4),
        padding=[dp(0), dp(0), dp(0), dp(0)],)
    """Container for toolbar menu items in MorphChartCard."""

    def __init__(self, *args, caller: MorphChartNavigationButton, **kwargs) -> None:
        config = clean_config(self.default_config, kwargs)
        super().__init__(*args, caller=caller, **config)


class MorphChart:
    pass