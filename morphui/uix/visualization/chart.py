import warnings

from typing import Any
from typing import Dict

from pathlib import Path

from matplotlib.figure import Figure
from matplotlib.backend_bases import _Mode

from kivy.metrics import dp
from kivy.properties import ObjectProperty
from kivy.properties import VariableListProperty

from morphui.uix.label import MorphSimpleLabel
from morphui.uix.button import MorphIconButton
from morphui.uix.boxlayout import MorphBoxLayout
from morphui.uix.behaviors import MorphMenuMotionBehavior
from morphui.uix.behaviors import MorphToggleButtonBehavior
from morphui.uix.floatlayout import MorphFloatLayout
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
            normal_content_color='content_primary_fixed_variant_color',),
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
            'normal_surface_color': 'transparent_color',
            'normal_content_color': 'content_primary_fixed_variant_color',
            'hovered_content_color': 'content_primary_fixed_color',},
        typography_role=MorphIconButton.default_config['typography_role'],
        typography_size=MorphIconButton.default_config['typography_size'],
        interaction_gray_value=0.0,
        ripple_enabled=True,
        ripple_layer='interaction',
        hover_enabled=True,
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
            'normal_surface_color': 'transparent_color',
            'active_surface_color': 'primary_fixed_color',
            'normal_content_color': 'content_primary_fixed_variant_color',
            'hovered_content_color': 'content_primary_fixed_color',
            'active_content_color': 'content_primary_fixed_color',},
        active_radius_enabled=True,))


class MorphChartToolbarMenu(
        MorphMenuMotionBehavior,
        MorphBoxLayout):
    """Toolbar menu container for MorphChartCard.
    """
    default_config: Dict[str, Any] = dict(
        theme_color_bindings={
            'normal_surface_color': 'transparent_color',},
        orientation='vertical',
        auto_size=True,
        spacing=dp(4),
        padding=[dp(0), dp(4)],)
    """Container for toolbar menu items in MorphChartCard."""

    def __init__(self, *args, caller: MorphChartNavigationButton, **kwargs) -> None:
        config = self.default_config.copy() | kwargs
        super().__init__(caller=caller, **config)
        for child in args:
            self.add_widget(child)
    
    def on_pre_open(self, *args) -> None:
        """Called before the menu is opened.
        
        This method is used to prepare the menu for opening, such as
        allowing it to be dismissed when clicking outside the menu area.
        """
        self.dismiss_allowed = True

    def on_dismiss(self, *args) -> None:
        """Handle actions after the dropdown menu is dismissed.

        If the caller button has an `active` property and is not in the 
        middle of a ripple animation, it sets `active` to `False` to 
        indicate that the dropdown is no longer active.
        """
        if (hasattr(self.caller, 'active') 
                and not getattr(self.caller, '_ripple_in_progress', False)):
            self.caller.active = False


class MorphChartToolbar(
        MorphToggleButtonBehavior,
        MorphChartNavigationButton):
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

    info_label: MorphChartInfoLabel = ObjectProperty(None)
    """Reference to the chart info label.

    This property holds the info label associated with the toolbar.

    :attr:`info_label` is a :class:`~kivy.properties.ObjectProperty`
    and defaults to `None`."""

    default_config: Dict[str, Any] = (
        MorphChartNavigationButton.default_config.copy() | dict(
            icon='menu',))

    def __init__(self, **kwargs) -> None:
        self.menu = kwargs.pop('menu', 
            MorphChartToolbarMenu(
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
        super().__init__(**kwargs)
        self.bind(active=self._toggle_menu_on_active)

    def _toggle_menu_on_active(self, *args) -> None:
        """Toggle the dropdown menu when the button's active state 
        changes.
        
        This method is called whenever the `active` property of the
        button changes. If the button becomes active, it opens the
        dropdown menu. If the button becomes inactive, it dismisses the
        dropdown menu."""
        if self.active:
            self.menu.open()
        else:
            self.menu.dismiss()
    
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

    def _figure_canvas_updated_(
            self,
            instance: Any,
            figure_canvas: FigureCanvas) -> None:
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


class MorphChart(MorphFloatLayout):
    """Chart component for data visualization within MorphUI.

    This class integrates a `MorphPlotWidget` with a toolbar for
    interactive chart navigation and manipulation. 
    
    Usage
    -----
    To use MorphChart, simply create an instance and set the 
    :attr:`figure` attribute to a matplotlib Figure. Everything else is 
    handled automatically:
    
    ```python
    import matplotlib.pyplot as plt
    from morphui.uix.visualization import MorphChart
    
    # Create your matplotlib figure
    fig, ax = plt.subplots()
    ax.plot([1, 2, 3], [4, 5, 6])
    
    # Create chart and set figure - that's it!
    chart = MorphChart()
    chart.figure = fig  # This automatically sets up all navigation
    ```
    
    When you set `chart.figure = fig`, the following happens 
    automatically:
    1. The figure is passed to the internal plot widget
    2. A figure canvas is created for rendering
    3. Navigation tools are initialized and bound to toolbar buttons
    4. All interactive features (zoom, pan, save, etc.) become 
       available
    
    No additional setup is required - the chart is immediately
    interactive and ready for user interaction.
    
    Customizing Save Behavior
    -------------------------
    To customize where chart images are saved, override the 
    :meth:`get_save_dir` method. This is the ideal place to implement
    a custom save directory dialog:
    
    ```python
    class CustomChart(MorphChart):
        def get_save_dir(self) -> Path:
            # Your custom logic here - e.g., open a directory dialog
            # Return the selected directory as a Path object
            return Path('/your/custom/directory')
    ```
    """

    plot_widget: MorphPlotWidget = ObjectProperty(None)
    """The plot widget used for rendering the chart.
    
    This property holds the `MorphPlotWidget` instance responsible for
    displaying the chart data.

    :attr:`plot_widget` is a :class:`~kivy.properties.ObjectProperty`
    and defaults to `None`.
    """

    toolbar: MorphChartToolbar = ObjectProperty(None)
    """The toolbar for chart navigation and actions.
    
    This property holds the `MorphChartToolbar` instance that provides
    interactive buttons for chart navigation, zooming, panning, and
    other actions.

    :attr:`toolbar` is a :class:`~kivy.properties.ObjectProperty`
    and defaults to `None`.
    """

    figure: Figure = ObjectProperty(None)
    """The matplotlib Figure associated with the chart.

    This property holds the `Figure` instance from matplotlib that
    contains the chart data and visual elements.

    :attr:`figure` is a :class:`~kivy.properties.ObjectProperty`
    and defaults to `None`.
    """

    padding: VariableListProperty = VariableListProperty(
        [dp(0)], length=4)
    """Padding around the chart components.

    This property defines the padding around the chart components
    (plot widget, toolbar, info label) within the `MorphChart`. It is a
    list of four values representing the padding on the left, top,
    right, and bottom sides, respectively.

    :attr:`padding` is a :class:`~kivy.properties.VariableListProperty`
    and defaults to `[dp(0), dp(0), dp(0), dp(0)]`.
    """

    kw_savefig: Dict[str, Any]
    """Keyword arguments for saving the figure.

    This dictionary holds any additional keyword arguments that should
    be passed to the :meth:`savefig` method of the matplotlib Figure
    when saving the chart to a file.
    """

    default_save_dir: Path | str = Path.home()/'Downloads'
    """Default directory for saving chart images.

    This attribute specifies the default directory where chart images
    will be saved when using the save functionality.
    """

    filename: str = 'morphui_chart.png'
    """Default filename for saved chart images.

    This attribute specifies the default filename used when saving
    chart images to a file.
    """

    initial_save_dir: Path | str = Path.home()/'Downloads'
    """Initial directory for the save dialog.

    This attribute specifies the initial directory that the save dialog
    will open to when saving chart images. This attribute is
    automatically updated to the last used directory after each save
    operation.

    Set this attribute to customize the initial directory for saving
    chart images. Especially useful for guiding users to a preferred
    save location.
    """

    default_config: Dict[str, Any] = dict(
        theme_color_bindings=dict(
            normal_surface_color='transparent_color',),
        size_hint=(1, 1),)
    """Default configuration for the MorphChart."""

    def __init__(
            self,
            kw_savefig: Dict[str, Any] = {},
            **kwargs) -> None:
        config = self.default_config.copy() | kwargs

        self.kw_savefig = kw_savefig
        super().__init__(**config)
        self.info_label = MorphChartInfoLabel()
        self.toolbar = MorphChartToolbar(info_label=self.info_label)
        self.plot_widget = MorphPlotWidget(toolbar=self.toolbar)
        self.toolbar.plot_widget = self.plot_widget

        self.add_widget(self.plot_widget)
        self.add_widget(self.toolbar)
        self.add_widget(self.info_label)
        
        self.bind(
            pos=self._update_layout,
            size=self._update_layout,)
        self.toolbar.menu.identities.chart_toolbar_save_button.bind(
            on_release=self.save_figure)

        self._update_layout()

    def on_touch_down(self, touch) -> None:
        """Callback function, called on mouse button press or touch.

        This method dismisses the toolbar menu if a touch occurs
        outside the chart area.
        """
        if not self.plot_widget.collide_point(*touch.pos):
            self.toolbar.menu.dismiss()
        return super().on_touch_down(touch)
        
    def on_figure(self, instance: Any, figure: Figure) -> None:
        """Callback function, called when `figure` attribute changes.
        
        This method updates the :attr:`figure` property of the 
        associated :class:`MorphPlotWidget` whenever the :attr:`figure` 
        property of the :class:`MorphChart` changes. This triggers the 
        following automatic chain:
        
        1. `self.plot_widget.figure = figure` - passes figure to plot.
        2. Plot widget's :meth:`on_figure()` method creates/updates 
           :attr:`figure_canvas`.
        3. Toolbar's :meth:`_figure_canvas_updated_()` method is 
           triggered.
        4. Navigation instance is created and all toolbar buttons are 
           bound.
        
        After this chain completes, the chart is fully interactive with
        working navigation, zoom, pan, save functionality, etc.
        """
        self.plot_widget.figure = figure

    def get_save_dir(self) -> Path:
        """Get the directory to save the current chart image.

        This method determines the directory where the chart image
        should be saved. It first checks the :attr:`initial_save_dir` 
        attribute, then falls back to :attr:`default_save_dir`, and
        finally defaults to the user's Downloads folder if neither
        directory is valid.

        Override this method to implement custom save directory 
        selection, such as opening a directory picker dialog. This is 
        the recommended approach for providing users with interactive 
        directory selection.
        
        Returns
        -------
        Path
            The directory path where the chart should be saved.
            
        Examples
        --------
        Override to implement a custom directory dialog:
        
        ```python
        class CustomChart(MorphChart):
            def get_save_dir(self) -> Path:
                # Open your preferred directory dialog here
                # Return the selected directory
                return selected_directory_path
        ```
        """
        directory = Path(self.initial_save_dir)
        if not directory.is_dir():
            directory = Path(self.default_save_dir)
        if not directory.is_dir():
            directory = Path.home()/'Downloads'
        return directory

    def save_figure(self, *args) -> None:
        """Save the current chart figure to a file.

        This method saves the current chart figure to a file in the
        directory returned by :meth:`get_save_dir`. The filename is
        determined by the :attr:`filename` attribute if not provided in
        :attr:`kw_savefig`. Any additional keyword arguments specified 
        in :attr:`kw_savefig` are passed to the :meth:`savefig` method 
        of the matplotlib Figure.

        Raises
        ------
        FileNotFoundError
            If the save directory is not valid.
        
        Warnings
        --------
        UserWarning
            If no figure is set or :meth:`get_save_dir` returns None.
        """
        if self.figure is None:
            warnings.warn('No figure set, cannot save figure.')
            return
        
        save_dir = self.get_save_dir()
        if save_dir is None:
            warnings.warn(
                'None returned by get_save_dir, cannot save figure.')
            return
        
        save_dir = Path(save_dir)
        if not save_dir.is_dir():
            raise FileNotFoundError(
                f'Save directory {save_dir} is not valid.')
        
        self.initial_save_dir = save_dir
        filename = (
            self.kw_savefig.get('fname', self.filename)
            or self.figure.canvas.get_default_filename())
        suffix = self.kw_savefig.get(
            'format', Path(filename).suffix.lstrip('.'))
        if suffix and not filename.endswith(f'.{suffix}'):
            filename = f'{filename}.{suffix}'
        
        kwargs = {k: v for k, v in self.kw_savefig.items() if k != 'fname'}
        self.figure.savefig(str(save_dir/filename), **kwargs)

    def _update_layout(self, *args) -> None:
        """Update the layout of the chart components."""
        self.plot_widget.pos = (
            self.pos[0] + self.padding[0],
            self.pos[1] + self.padding[1])
        self.plot_widget.size = (
            self.size[0] - self.padding[0] - self.padding[2],
            self.size[1] - self.padding[1] - self.padding[3])

        self.toolbar.x = (
            self.plot_widget.x
            + self.plot_widget.width
            - self.toolbar.width
            - dp(4))
        self.toolbar.y = (
            self.plot_widget.y
            + self.plot_widget.height
            - self.toolbar.height
            - dp(4))
