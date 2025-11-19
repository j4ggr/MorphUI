import weakref

from typing import Any
from typing import Self
from typing import List
from typing import Dict
from typing import Tuple
from typing import Literal
from numpy.typing import ArrayLike

from matplotlib.axes import Axes
from matplotlib.figure import Figure
from matplotlib.backend_bases import MouseEvent
from matplotlib.backend_bases import MouseButton
from matplotlib.backends.backend_agg import RendererAgg

from kivy.base import EventLoop
from kivy.metrics import dp
from kivy.graphics import Color
from kivy.graphics import Line
from kivy.graphics import Rectangle
from kivy.graphics import BorderImage
from kivy.uix.widget import Widget
from kivy.properties import ListProperty
from kivy.properties import ColorProperty
from kivy.properties import ObjectProperty
from kivy.properties import BooleanProperty
from kivy.properties import VariableListProperty
from kivy.graphics.texture import Texture
from kivy.input.motionevent import MotionEvent
from kivy.core.window.window_sdl2 import WindowSDL

from morphui.utils import clean_config
from morphui.uix.behaviors import MorphThemeBehavior
from morphui.uix.behaviors import MorphSurfaceLayerBehavior
from morphui.uix.behaviors import MorphIdentificationBehavior

from .backend import FigureCanvas


__all__ = [
    'MorphPlotWidget',
]


class MorphPlotWidget(
        MorphIdentificationBehavior,
        MorphThemeBehavior, 
        MorphSurfaceLayerBehavior,
        Widget):
    """Kivy Widget to show a matplotlib figure in kivy.
    The figure is rendered internally in an AGG backend then
    the rgb data is obtained and blitted into a kivy texture.
    
    This widget uses only the essential MorphUI behaviors for lightweight operation:
    - MorphIdentificationBehavior: For widget identification and identity-based styling
    - MorphThemeBehavior: For theme integration and color binding
    - MorphSurfaceLayerBehavior: For background color, borders, and radius styling
    
    This focused approach provides theming and styling capabilities while avoiding
    unnecessary behaviors like interaction layers, content layers, or auto-sizing.
    
    Parameters
    ----------
    figure : `~matplotlib.figure.Figure`
        The top level container for all the plot elements.
    surface_color : list or tuple, optional
        Background color for the plot. Defaults to white (1.0, 1.0, 1.0, 1.0).
        Can be customized for different themes or transparent overlays.
    """
    
    figure: Figure = ObjectProperty(None)
    """The matplotlib figure object as the top level container for all 
    the plot elements. If this property changes, a new FigureCanvas is
    created, see method `on_figure` (callback)."""
    
    figure_canvas: FigureCanvas = ObjectProperty(None)
    """Canvas to render the plots into. Is set in method `on_figure` 
    (callback)."""
    
    texture: Texture = ObjectProperty(None)
    """Texture to blit the figure into."""

    rubberband_pos: List[float] = VariableListProperty([0, 0], length=2)
    """Position of the rubberband when using the zoom tool.
    
    This property stores the [x, y] coordinates of the top-left corner
    of the rubberband rectangle during zoom operations. The coordinates
    are in widget space.
    
    :attr:`rubberband_pos` is a
    :class:`~kivy.properties.VariableListProperty` and defaults to 
    `[0, 0]`."""
    
    rubberband_size: List[float] = VariableListProperty([0, 0], length=2)
    """Size of the rubberband when using the zoom tool.
    
    This property stores the [width, height] dimensions of the 
    rubberband rectangle during zoom operations. Values of 0 indicate no
    rubberband is currently displayed.
    
    :attr:`rubberband_size` is a
    :class:`~kivy.properties.VariableListProperty` and defaults to 
    `[0, 0]`."""
    
    rubberband_corners: List[float] = ListProperty(
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    """Corner points of the rubberband when using the zoom tool.
    
    This property stores a flat list of [x, y] coordinates representing
    the corners of the rubberband rectangle in order: top-left, 
    top-right, bottom-right, bottom-left, and back to top-left to close
    the path. Used for drawing the rubberband border as a line.
    
    :attr:`rubberband_corners` is a 
    :class:`~kivy.properties.ListProperty` and defaults to 
    `[0, 0, 0, 0, 0, 0, 0, 0, 0, 0]`."""
    
    rubberband_threshold: float = dp(20)
    """Threshold at which it will switch between axis-wise zoom or 
    rectangle zoom"""
    
    rubberband_color: ColorProperty = ColorProperty([0, 0, 0, 0.2])
    """Color of the rubberband area when using the zoom tool.
    
    The color should be provided as a list of RGBA values between 0 and 
    1. Example: `[0, 0, 0, 0.2]` for semi-transparent black.
    
    :attr:`rubberband_color` is a 
    :class:`~kivy.properties.ColorProperty` and defaults to 
    `[0, 0, 0, 0.2]`."""
    
    rubberband_edge_color: ColorProperty = ColorProperty([0, 0, 0, 0.6])
    """Color of the rubberband edges when using the zoom tool.
    
    The color should be provided as a list of RGBA values between 0 and 
    1. Example: `[0, 0, 0, 0.6]` for semi-transparent black.
    
    :attr:`rubberband_edge_color` is a
    :class:`~kivy.properties.ColorProperty` and defaults to 
    `[0, 0, 0, 0.6]`."""
    
    toolbar: Any = ObjectProperty(None)
    """Toolbar widget to display the toolbar.
    
    This property holds a reference to the toolbar widget associated
    with this plot widget. It is used to coordinate interactions
    between the plot and the toolbar."""
    
    is_pressed: bool = False
    """Flag to distinguish whether the mouse is moved with the key 
    pressed or not."""
    
    inaxes: Axes | None = None
    """Current axis on which the mouse is hovering, is automatically 
    set in `on_mouse_pos` callback"""

    show_info: bool = BooleanProperty(False)
    """Flag to show the info label"""

    _rubberband_color_instruction: Color
    """Kivy Color instruction for the rubberband area color."""

    _rubberband_instruction: BorderImage
    """Kivy BorderImage instruction for the rubberband area."""

    _rubberband_edge_color_instruction: Color
    """Kivy Color instruction for the rubberband edge color."""

    _rubberband_edge_instruction: Line
    """Kivy Line instruction for the rubberband edge."""

    _texture_rectangle_instruction: Rectangle
    """Kivy Rectangle instruction for rendering the matplotlib texture."""

    default_config: Dict[str, Any] = dict(
        surface_color=(1.0, 1.0, 1.0, 1.0),  # White background for charts
        size_hint=(None, None),)
    """Default configuration for the plot widget."""

    def __init__(self, *args, **kwargs) -> None:
        config = clean_config(self.default_config, kwargs)
        super().__init__(*args, **config)
        
        self._flipped_textures = weakref.WeakSet()
        
        with self.canvas.before:
            self._texture_rectangle_color_instruction = Color(
                rgba=self.get_resolved_surface_colors()[0])
            self._texture_rectangle_instruction = Rectangle(
                pos=self.pos,
                size=self.size,
                texture=self.texture)
    
        with self.canvas.after:
            self._rubberband_color_instruction = Color(rgba=self.rubberband_color)
            self._rubberband_instruction = BorderImage(
                source='border.png',
                pos=self.rubberband_pos,
                size=self.rubberband_size,
                border=(1, 1, 1, 1))

            self._rubberband_edge_color_instruction = Color(rgba=self.rubberband_edge_color)
            self._rubberband_edge_instruction = Line(
                points=self.rubberband_corners,
                width=1,
                dash_offset=4,
                dash_length=6)
        
        EventLoop.window.bind( # type: ignore
            mouse_pos=self.on_mouse_move)
        
        self.bind(
            size=self._update_figure_size,
            pos=self._update_surface_layer,
            texture=self._update_surface_layer,
            rubberband_pos=self._update_rubberband_area,
            rubberband_size=self._update_rubberband_area,
            rubberband_corners=self._update_rubberband_edge,
            rubberband_color=self._update_rubberband_colors,
            rubberband_edge_color=self._update_rubberband_colors,)
       
        self._update_figure_size(self, self.size)
        self._update_surface_layer(self, self.texture)

    @property
    def rubberband_drawn(self) -> bool:
        """True if a rubberband is drawn (read-only)"""
        return self.rubberband_size[0] > 1 or self.rubberband_size[1] > 1

    def _update_rubberband_area(self, *args) -> None:
        """Update the rubberband area graphics instructions."""
        self._rubberband_instruction.pos = self.rubberband_pos
        self._rubberband_instruction.size = self.rubberband_size

    def _update_rubberband_edge(self, *args) -> None:
        """Update the rubberband edge graphics instructions."""
        self._rubberband_edge_instruction.points = self.rubberband_corners

    def _update_rubberband_colors(self, *args) -> None:
        """Update the rubberband color graphics instructions."""
        self._rubberband_color_instruction.rgba = self.rubberband_color
        self._rubberband_edge_color_instruction.rgba = self.rubberband_edge_color

    def get_resolved_surface_colors(self) -> Tuple[List[float], List[float]]:
        """Get the resolved surface and border colors based on the
        current theme and surface color settings.

        Returns
        -------
        Tuple[List[float], List[float]]
            A tuple containing two lists:
            - The resolved surface color as an RGBA list.
            - The resolved border color as an RGBA list.

        Raises
        ------
        ValueError
            If the resolved surface color is fully transparent.
        """
        surface_color, border_color = super().get_resolved_surface_colors()
        assert surface_color[3] > 0, (
            'MorphPlotWidget requires a non-transparent surface color '
            'to render the matplotlib figure correctly.')
        return surface_color, border_color
    
    def _safe_flip_texture_vertical(self, texture: Texture | None) -> None:
        """Safely flip the given texture vertically if it hasn't been
        flipped yet, using weak references to track flipped textures.

        Parameters
        ----------
        texture : Texture | None
            The texture to flip vertically if it hasn't been flipped yet.
        """
        if texture is None:
            return
        
        if texture not in self._flipped_textures:
            texture.flip_vertical()
            self._flipped_textures.add(texture)
        
    def _update_surface_layer(self, *args) -> None:
        """Update the surface when any relevant property changes.
        
        This method overrides the base implementation to also update
        the texture rectangle instruction with the current texture
        and size. It ensures that the background surface reflects the
        current state of the plot widget.

        The method checks if the texture has been created and flips it
        vertically only once per texture instance to ensure correct
        rendering.
        """
        super()._update_surface_layer(*args)
        if not hasattr(self, '_texture_rectangle_color_instruction'):
            self._surface_color_instruction.rgba = (
                self.theme_manager.transparent_color)
            return
        
        surface_color, border_color = self.get_resolved_surface_colors()

        self._border_instruction.width = dp(self.border_width)
        self._border_instruction.points = self._generate_border_path()
        self._border_instruction.close = self.border_closed
        self._border_color_instruction.rgba = border_color
        
        self._safe_flip_texture_vertical(self.texture)
        self._texture_rectangle_color_instruction.rgba = surface_color
        self._texture_rectangle_instruction.pos = self.pos
        self._texture_rectangle_instruction.size = self.size
        self._texture_rectangle_instruction.texture = self.texture

        self.dispatch('on_surface_updated')

    def window_to_figure_canvas(self, x: float, y: float) -> Tuple[float, float]:
        """Convert window coordinates to figure canvas coordinates.

        This method transforms the given (x, y) coordinates from window
        space to figure canvas space.
        """
        x_offset, y_offset = self.to_window(*self.pos)
        return x - x_offset, y - y_offset

    def touch_to_figure_canvas(self, touch: MotionEvent) -> Tuple[float, float]:
        """Convert touch coordinates to figure canvas coordinates.

        This method transforms the given touch event's (x, y)
        coordinates from window space to figure canvas space.
        """
        return self.window_to_figure_canvas(*self.to_window(touch.x, touch.y))
    
    def figure_canvas_to_widget(self, x: float, y: float) -> Tuple[float, float]:
        """Convert figure canvas coordinates to widget coordinates.

        This method transforms the given (x, y) coordinates from figure
        canvas space to widget space.
        """
        x_offset, y_offset = self.to_window(*self.pos)
        x, y = x + x_offset, y + y_offset
        return self.to_widget(x, y)
    
    def on_touch_down(self, touch: MotionEvent) -> None:
        """Callback function, called on mouse button press or touch 
        event."""
        if not self.collide_point(touch.x, touch.y):
            return
        
        if touch.is_mouse_scrolling:
            return
        
        if touch.is_double_tap:
            self.toolbar.navigation.home()
            return
        
        if self.figure_canvas is None:
            return
        
        self.is_pressed = True
        self.figure_canvas.button_press_event(
            *self.touch_to_figure_canvas(touch),
            button=self._button_(touch),
            gui_event=touch)

    def on_touch_move(self, touch: MotionEvent) -> None:
        """Callback function, called on mouse movement event while mouse
        button pressed or touch."""
        if not self.collide_point(*touch.pos) or self.figure_canvas is None:
            return

        self.figure_canvas.motion_notify_event(
            *self.touch_to_figure_canvas(touch),
            gui_event=touch)
    
    def on_touch_up(self, touch: MotionEvent) -> None:
        """Callback function, called on mouse button release or touch up
        event."""
        # self.reset_rubberband()
        if not self.collide_point(touch.x, touch.y):
            return
        
        if self.figure_canvas is None:
            return
        
        self.is_pressed = False
        self.figure_canvas.button_release_event(
            *self.touch_to_figure_canvas(touch),
            button=self._button_(touch),
            gui_event=touch)
    
    def on_mouse_move(
            self, window: WindowSDL, mouse_pos: Tuple[float, float]) -> None:
        """Callback function, called on mouse movement event"""
        if any((
                not self.collide_point(*mouse_pos),
                self.is_pressed,
                self.figure_canvas is None)):
            self.clear_toolbar_info()
            self.inaxes = None
            return

        transformed_pos = self.window_to_figure_canvas(*mouse_pos)
        self.inaxes = self.figure_canvas.inaxes(transformed_pos)
        self.figure_canvas.motion_notify_event(
            *transformed_pos,
            gui_event = None)
        self.adjust_toolbar_info_pos(self.to_widget(*mouse_pos))

    def on_figure(self, caller: Self, figure: Figure) -> None:
        """Callback function, called when `figure` attribute changes."""
        self.texture = None
        self.figure_canvas = FigureCanvas(figure, plot_widget=self)
        self.figure_canvas.draw()
        self.size = list(map(float, self.figure.bbox.size))
        self._update_figure_size(self, self.size)

    def _update_figure_size(self, caller: Self, size: List[float]) -> None:
        """Creat a new, correctly sized bitmap"""
        if self.figure is None or size[0] <= 1 or size[1] <= 1:
            return
        
        fig_size = (size[0] / self.figure.dpi, size[1] / self.figure.dpi)
        if tuple(self.figure.get_size_inches()) == fig_size:
            return

        self.figure.set_size_inches(*fig_size, forward=True)
        self.figure_canvas.resize_event()
        self.figure_canvas.draw()
    
    def data_to_axes(self, points: ArrayLike) -> ArrayLike:
        """Transform points from the data coordinate system to the 
        axes coordinate system. Given points should be an array with
        shape (N, 2) or a single point as a tuple containing 2 floats
        """
        if self.inaxes is None:
            return points
        
        points = (
            self.inaxes.transData
            + self.inaxes.transAxes.inverted()
            ).transform(points)
        return points
    
    def display_to_data(self, points: ArrayLike) -> ArrayLike:
        """Transform points from the display coordinate system to the 
        data coordinate system. Given points should be an array with
        shape (N, 2) or a single point as a tuple containing 2 floats.
        """
        if self.inaxes is None:
            return points
        
        return self.inaxes.transData.inverted().transform(points)
    
    def data_to_display(self, points: ArrayLike) -> ArrayLike:
        """Transform points from the data coordinate system to the 
        display coordinate system. Given points should be an array with
        shape (N, 2) or a single point as a tuple containing 2 floats.
        """
        if self.inaxes is None:
            return points

        return self.inaxes.transData.transform(points)
    
    def display_to_axes(self, points: ArrayLike) -> ArrayLike:
        """Transform points from the display coordinate system to the 
        data coordinate system. Given points should be an array with
        shape (N, 2) or a single point as a tuple containing 2 floats.
        """
        if self.inaxes is None:
            return points
        return self.inaxes.transAxes.inverted().transform(points)
    
    def draw_rubberband(
            self, touch: MouseEvent, x0: float, y0: float, x1: float, y1: float
            ) -> None:
        """Draw a rectangle rubberband to indicate zoom limits.
    
        Parameters
        ----------
        touch : `~matplotlib.backend_bases.MouseEvent`
            Touch event
        x0 : float
            x coordonnate init
        x1 : float
            y coordonnate of move touch
        y0 : float
            y coordonnate init
        y1 : float
            x coordonnate of move touch"""
        if self.toolbar is not None:
            self.toolbar.navigation.zoom_x_only = False
            self.toolbar.navigation.zoom_y_only = False
            ax = self.toolbar.navigation._zoom_info.axes[0]
            width = abs(x1 - x0)
            height = abs(y1 - y0)
            if width < self.rubberband_threshold < height:
                x0, x1 = ax.bbox.intervalx
                self.toolbar.navigation.zoom_y_only = True
            elif height < self.rubberband_threshold < width:
                y0, y1 = ax.bbox.intervaly
                self.toolbar.navigation.zoom_x_only = True

        x0, x1, y0, y1 = map(float, (*sorted((x0, x1)), *sorted((y0, y1))))
        x0, y0 = self.figure_canvas_to_widget(x0, y0)
        x1, y1 = self.figure_canvas_to_widget(x1, y1)

        self.rubberband_pos = [x0, y0]
        self.rubberband_size = [x1 - x0, y1 - y0]
        self.rubberband_corners = [x0, y0, x1, y0, x1, y1, x0, y1, x0, y0]
    
    def remove_rubberband(self) -> None:
        """Remove rubberband if is drawn."""
        if not self.rubberband_drawn:
            return
        
        self.rubberband_pos = [0, 0]
        self.rubberband_size = [0, 0]
        self.rubberband_corners = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    def on_show_info(self, caller: Any, show_info: bool) -> None:
        """Callback function, called when `show_info` attribute changes.
        Clear toolbar label if show_info is False."""
        if not show_info:
            self.clear_toolbar_info()
    
    def clear_toolbar_info(self) -> None:
        """Clear text of toolbar label if available"""
        if self.toolbar is None:
            return
        
        self.toolbar.info_label.text = ''
    
    def adjust_toolbar_info_pos(
            self,
            pos: Tuple[float, float],
            center_x: bool = True
            ) -> None:
        """Adjust position of toolbar label if available
        
        This method repositions the toolbar's info label to the given
        position. It is typically called during mouse movement events
        to keep the info label near the cursor.
        
        Parameters
        ----------
        pos : Tuple[float, float]
            The position (x, y) to align the info label to.
        center_x : bool, optional
            Whether to center the label horizontally at the given x
            position. Defaults to True.

        Notes
        -----
        If the toolbar or info label is not available, the method
        exits without making any changes.
        """
        if self.toolbar is None or self.toolbar.info_label.text == '':
            return
        
        x_offset = -self.toolbar.info_label.width / 2 if center_x else 0
        self.toolbar.info_label.pos = (pos[0] + x_offset, pos[1] + dp(4))

    def _draw_bitmap_(self, renderer: RendererAgg) -> None:
        """Draw the bitmap from the given renderer into the texture."""
        self.texture = Texture.create(size=self.size,)
        self.texture.blit_buffer(
            renderer.tostring_argb(),
            colorfmt='argb',
            bufferfmt='ubyte')
    
    def _button_(
            self,
            event: MotionEvent
            ) -> MouseButton | Literal['up', 'down'] | None:
        """If possible, connvert `button` attribute of given event to a
        number using enum `~matplotlib.backend_bases.MouseButton`. If it
        is a scroll event, return "up" or "down" as appropriate."""
        name = getattr(event, 'button', None)
        if name is None:
            return None
        
        if hasattr(MouseButton, name.upper()):
            button = MouseButton[name.upper()]
        elif 'scroll' in name:
            button = 'up' if 'up' in name else 'down'
        else:
            button = None
        return button
