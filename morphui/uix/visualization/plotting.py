import math
import warnings

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
    
    mouse_pos: List[float] = VariableListProperty([0, 0], length=2)
    """Current mouse position relative to the parent widget.
    
    This property stores the [x, y] coordinates of the mouse cursor
    position relative to the parent widget's coordinate system. It is
    automatically updated during mouse movement events and used for
    determining which matplotlib axes the cursor is hovering over.
    
    :attr:`mouse_pos` is a
    :class:`~kivy.properties.VariableListProperty` and defaults to 
    `[0, 0]`."""
    
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
        size_hint=(1, 1),
        pos_hint={'center_x': 0.5, 'center_y': 0.5},)
    """Default configuration for the plot widget."""

    def __init__(self, *args, **kwargs) -> None:
        config = clean_config(self.default_config, kwargs)
        super().__init__(*args, **config)
        
        # Rubberband rendering
        with self.canvas.after:
            self._texture_rectangle_instruction = Rectangle(
                pos=self.pos,
                size=self.size,
                texture=self.texture)
            
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
        
        EventLoop.window.bind(mouse_pos=self.on_mouse_move) # type: ignore
        self.bind(
            pos=self._update_texture_rectangle,
            size=self._update_figure_size,
            texture=self._update_texture_rectangle,
            rubberband_pos=self._update_rubberband_area,
            rubberband_size=self._update_rubberband_area,
            rubberband_corners=self._update_rubberband_edge,
            rubberband_color=self._update_rubberband_colors,
            rubberband_edge_color=self._update_rubberband_colors,)
        self._update_figure_size(self, self.size)
        self._update_texture_rectangle(self, self.texture)
    
    def _update_texture_rectangle(self, *args) -> None:
        """Update the main texture rectangle graphics instructions."""
        self._texture_rectangle_instruction.pos = self.pos
        self._texture_rectangle_instruction.size = self.size
        self._texture_rectangle_instruction.texture = self.texture

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

    @property
    def rubberband_drawn(self) -> bool:
        """True if a rubberband is drawn (read-only)"""
        return self.rubberband_size[0] > 1 or self.rubberband_size[1] > 1
    
    def on_mouse_pos(
            self, caller: Self, mouse_pos: Tuple[float, float]) -> None:
        """Callback function, called when `mouse_pos` attribute changes."""
        if self.figure_canvas is None:
            self.inaxes = None
        else:
            self.inaxes = self.figure_canvas.inaxes(mouse_pos)
    
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
            x = touch.x,
            y = touch.y - self.pos[1],
            button = self._button_(touch),
            gui_event = touch)
    
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
            x = touch.x,
            y = touch.y - self.pos[1],
            button = self._button_(touch),
            gui_event = touch)
    
    def on_mouse_move(
            self, window: WindowSDL, mouse_pos: Tuple[float, float]) -> None:
        """Callback function, called on mouse movement event"""
        self.mouse_pos = [
            mouse_pos[0] - self.parent.x,
            mouse_pos[1] - self.parent.y]
        if self.collide_point(*self.mouse_pos) and not self.is_pressed:
            if self.figure_canvas is None:
                return
            
            self.figure_canvas.motion_notify_event(
                x = self.mouse_pos[0],
                y = self.mouse_pos[1] - self.pos[1],
                gui_event = None)
            self.adjust_toolbar_info_pos()
        else:
            self.clear_toolbar_info()

    def on_touch_move(self, touch: MotionEvent) -> None:
        """Callback function, called on mouse movement event while mouse
        button pressed or touch."""
        if not self.collide_point(touch.x, touch.y):
            return
        
        if self.figure_canvas is None:
            return
        
        self.figure_canvas.motion_notify_event(
            x = touch.x,
            y = touch.y - self.pos[1],
            gui_event = touch)

    def on_figure(self, caller: Self, figure: Figure) -> None:
        """Callback function, called when `figure` attribute changes."""
        # self.figure.set_layout_engine('constrained')
        self.figure_canvas = FigureCanvas(figure, plot_widget=self)
        bbox = getattr(figure, 'bbox', None)
        if bbox is None:
            warnings.warn('Figure bbox not found, cannot set size.')
            return
        
        self.size = (math.ceil(bbox.width), math.ceil(bbox.height))
        self.texture = Texture.create(size=self.size)

    def _update_figure_size(
            self, caller: Self, size: Tuple[float, float]) -> None:
        """Creat a new, correctly sized bitmap"""
        if self.figure is None or size[0] <= 1 or size[1] <= 1:
            return
        
        self.figure.set_size_inches(
            size[0] / self.figure.dpi,
            size[1] / self.figure.dpi)
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

        if x0 > x1: 
            x0, x1 = x1, x0
        if y0 > y1: 
            y0, y1 = y1, y0
        y0 += self.pos[1]
        y1 += self.pos[1]

        x0, x1, y0, y1 = float(x0), float(x1), float(y0), float(y1)
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
    
    def adjust_toolbar_info_pos(self, *args) -> None:
        """Adjust position of toolbar label if available"""
        if self.toolbar is None or self.toolbar.info_label.text == '':
            return
        self.toolbar.info_label.pos = (
            self.mouse_pos[0] - self.toolbar.info_label.width/2,
            self.mouse_pos[1])

    def _draw_bitmap_(self, renderer: RendererAgg) -> None:
        """Draw the bitmap from the given renderer into the texture."""
        size = renderer.get_canvas_width_height()
        bitmap = renderer.tostring_argb()
        self.texture = Texture.create(size=size)
        self.texture.blit_buffer(bitmap, colorfmt='argb', bufferfmt='ubyte')
        self.texture.flip_vertical()
    
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
