from typing import Any
from typing import Dict

from matplotlib.backend_bases import _Mode

from kivy.metrics import dp
from kivy.properties import ObjectProperty

from morphui.utils import clean_config
from morphui.uix.label import MorphSimpleLabel
from morphui.uix.button import MorphIconButton
from morphui.uix.boxlayout import MorphBoxLayout
from morphui.uix.behaviors import MorphMenuMotionBehavior
from morphui.uix.behaviors import MorphToggleButtonBehavior
from morphui.uix.visualization import MorphPlotWidget
from morphui.uix.visualization.backend import Navigation
from morphui.uix.visualization.backend import FigureCanvas

__all__ = [
    'MorphChartInfoLabel',
    'MorphChartNavigationButton',
    'MorphChartNavigationToggleButton',
    'MorphChartToolbarMenu',
    'MorphChartToolbar',
    'MorphChart',]


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
        MorphBoxLayout):
    """Toolbar menu container for MorphChartCard.
    """
    default_config: Dict[str, Any] = dict(
        theme_color_bindings={
            'surface_color': 'transparent_color',},
        orientation='vertical',
        spacing=dp(4),
        padding=[dp(0), dp(0), dp(0), dp(0)],)
    """Container for toolbar menu items in MorphChartCard."""

    def __init__(self, *args, caller: MorphChartNavigationButton, **kwargs) -> None:
        config = clean_config(self.default_config, kwargs)
        super().__init__(*args, caller=caller, **config)


class MorphChartToolbar(MorphChartNavigationButton):
    """Toolbar button for MorphChartCard that opens a menu.
    """

    plot_widget: MorphPlotWidget = ObjectProperty(None)
    """Reference to the associated MorphPlotWidget.

    This property must be set to link the toolbar to its corresponding
    MorphPlotWidget for chart interactions.

    :attr:`plot_widget` is a :class:`~kivy.properties.ObjectProperty`
    and defaults to `None`."""

    menu: MorphChartToolbarMenu = ObjectProperty(None)
    """Reference to the toolbar menu.

    This property holds the menu associated with the toolbar button.

    :attr:`menu` is a :class:`~kivy.properties.ObjectProperty`
    and defaults to `None`."""

    navigation: Navigation = ObjectProperty(None)
    """Reference to the Navigation instance.

    This property holds the 
    :class:`~morphui.uix.visualization.backend.Navigation` instance
    for managing chart navigation actions.

    :attr:`navigation` is a :class:`~kivy.properties.ObjectProperty`
    and defaults to `None`."""

    default_config: Dict[str, Any] = (
        MorphChartNavigationButton.default_config.copy() | dict(
            icon='menu',))

    def __init__(self, **kwargs) -> None:
        self.menu = kwargs.pop('menu', MorphChartToolbarMenu(
            MorphChartNavigationButton(
                identity='chart_toolbar_home_button',
                icon='home-outline',),
            MorphChartNavigationButton(
                identity='chart_toolbar_undo_button',
                icon='undo-variant',),
            MorphChartNavigationButton(
                identity='chart_toolbar_redo_button',
                icon='redo-variant',),
            MorphChartNavigationToggleButton(
                identity='chart_toolbar_coordinate_button',
                group='chart_toolbar_navigation_tools',
                icon='map-marker-radius-outline',
                on_release=self.show_coordinates,),
            MorphChartNavigationToggleButton(
                identity='chart_toolbar_pan_button',
                group='chart_toolbar_navigation_tools',
                icon='arrow-all',),
            MorphChartNavigationToggleButton(
                identity='chart_toolbar_zoom_button',
                group='chart_toolbar_navigation_tools',
                icon='selection-drag',),
            MorphChartNavigationButton(
                identity='chart_toolbar_save_button',
                icon='content-save-outline',),
            identity='chart_toolbar_menu',
            caller=self))
        super().__init__(
            on_release=kwargs.pop('on_release', self.menu.toggle),
            **kwargs)
    
    def on_plot_widget(self, instance: Any, plot_widget: MorphPlotWidget) -> None:
        """Bind the toolbar buttons to the plot widget actions.

        This method sets up the necessary bindings between the toolbar
        buttons and the corresponding actions on the associated
        MorphPlotWidget.

        Parameters
        ----------
        instance : Any
            The instance of the toolbar.
        plot_widget : MorphPlotWidget
            The associated MorphPlotWidget.
        """
        self.plot_widget.bind(figure_canvas=self._figure_canvas_updated_)
        self.menu.identities.chart_toolbar_coordinate_button.bind(
            active=plot_widget.setter('show_info'))

    def _figure_canvas_updated_(self, instance: Any, figure_canvas: Any) -> None:
        """Update toolbar button states based on the figure canvas.

        This method initializes the Navigation instance and binds
        the toolbar buttons to their respective navigation actions
        whenever the `figure_canvas` property of the associated
        `MorphPlotWidget` is updated.

        Parameters
        ----------
        instance : Any
            The instance of the toolbar. Unless triggered manually, this
            will be the `MorphPlotWidget`. Because this method is bound 
            to the `figure_canvas` property, the instance is passed
            automatically.
        figure_canvas : Any
            The current figure canvas.

        Notes
        -----
        This method is bound to the `figure_canvas` property of the
        associated `MorphPlotWidget` and is triggered on changes to
        that property.
        """
        self.navigation = Navigation(figure_canvas, self)
        self.navigation.plot_widget = self.plot_widget
        self.menu.identities.chart_toolbar_home_button.bind(
            on_release=self.navigation.home)
        self.menu.identities.chart_toolbar_undo_button.bind(
            on_release=self.navigation.back)
        self.menu.identities.chart_toolbar_redo_button.bind(
            on_release=self.navigation.forward)
        self.menu.identities.chart_toolbar_pan_button.bind(
            on_release=self.navigation.pan)
        self.menu.identities.chart_toolbar_zoom_button.bind(
            on_release=self.navigation.zoom)
    
    def show_coordinates(self, *args) -> None:
        """Toggle the display of coordinates on the plot widget.

        This method is called when the coordinate button in the
        toolbar is toggled. It updates the `show_info` property
        of the associated `MorphPlotWidget` to show or hide
        coordinate information.

        Parameters
        ----------
        *args
            Additional arguments passed by the button event.
        """
        if self.plot_widget is None:
            return
        
        if self.menu.identities.chart_toolbar_coordinate_button.active:
            self._update_navigation_mode_()
    
    def _update_navigation_mode_(self) -> None:
        """Update the navigation mode based on the active toolbar button.

        This method checks which navigation toggle button is currently
        active in the toolbar and sets the corresponding navigation
        mode in the `Navigation` instance.

        Raises
        ------
        ValueError
            If an unknown navigation mode is encountered.
        """
        if self.navigation is None:
            return
    
        mode = getattr(self.navigation, 'mode', None)
        if mode == _Mode.NONE or mode is None:
            return
    
        if mode == _Mode.ZOOM:
            self.navigation.zoom()
        elif mode == _Mode.PAN:
            self.navigation.pan()

class MorphChart:
    pass