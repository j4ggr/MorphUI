import warnings

from typing import Any
from typing import List
from typing import Tuple
from typing import Literal
from typing import NamedTuple

from matplotlib.axes import Axes
from matplotlib.figure import Figure
from matplotlib.backend_bases import Event
from matplotlib.backend_bases import KeyEvent
from matplotlib.backend_bases import MouseEvent
from matplotlib.backend_bases import ResizeEvent
from matplotlib.backend_bases import NavigationToolbar2
from matplotlib.backends.backend_agg import FigureCanvasAgg


__all__ = [
    'FigureCanvas',
    'Navigation'
]


ZoomInfo = NamedTuple('ZoomInfo',[
    ('direction', Literal['in', 'out']),
    ('start_xy', Tuple[int, int]),
    ('axes', List[Axes]),
    ('cid', int),
    ('cbar', Literal['vertical', 'horizontal', None])])


class FigureCanvas(FigureCanvasAgg):
    """Internal AGG canvas the figure renders into.

    Parameters
    ----------
    figure : `~matplotlib.figure.Figure`
        A high-level figure instance.
    figure_widget : `~kivymd.uix.widget.MDWidget`
        Graphical representation of the figure in the application.
    """
    def __init__(
            self,
            figure: Figure,
            figure_widget: Any,
            *args,
            **kwargs) -> None:
        self.is_drawn = False
        self.figure_widget = figure_widget
        super().__init__(figure, *args, **kwargs)

    def draw(self) -> None:
        """Render the figure using agg."""
        try:
            super().draw()
            self.is_drawn = True
            self.blit()
        except IndexError as e:
            warnings.warn(f'Could not redraw canvas: {e}')

    def blit(self, bbox=None) -> None:
        """Render the figure using agg (blit method)."""
        self.figure_widget._draw_bitmap_(self.get_renderer())
    
    def enter_notify_event(self, gui_event=None) -> None: # pyright: ignore[reportIncompatibleMethodOverride]
        name = 'figure_enter_event'
        figure_enter_event = Event(name, self, gui_event)
        self.callbacks.process(name, figure_enter_event)

    def leave_notify_event(self, gui_event=None) -> None: # pyright: ignore[reportIncompatibleMethodOverride]
        name = 'figure_leave_event'
        figure_leave_event = Event(name, self, gui_event)
        self.callbacks.process(name, figure_leave_event)

    def resize_event(self) -> None:
        name = 'resize_event'
        resize_event = ResizeEvent(name, self)
        self.callbacks.process(name, resize_event)

    def motion_notify_event(self, x, y, gui_event=None) -> None: # pyright: ignore[reportIncompatibleMethodOverride]
        name = 'motion_notify_event'
        self.callbacks.process(
            name, MouseEvent(name, self, x, y, guiEvent=gui_event))

    def button_press_event( # pyright: ignore[reportIncompatibleMethodOverride]
            self, x, y, button, dblclick=False, gui_event=None) -> None:
        name = 'button_press_event'
        button_press_event = MouseEvent(
            name, self, x, y, button=button, dblclick=dblclick,
            guiEvent=gui_event)
        self.callbacks.process(name, button_press_event)

    def button_release_event( # pyright: ignore[reportIncompatibleMethodOverride]
            self, x, y, button, dblclick=False, gui_event=None) -> None:
        name = 'button_release_event'
        button_release_event = MouseEvent(
            name, self, x, y, button=button, dblclick=dblclick,
            guiEvent=gui_event)
        self.callbacks.process(name, button_release_event)

    def scroll_event(self, x, y, step, gui_event=None) -> None: # pyright: ignore[reportIncompatibleMethodOverride]
        name = 'scroll_event'
        scroll_event = MouseEvent(
            name, self, x, y, step=step, guiEvent=gui_event)
        self.callbacks.process(name, scroll_event)

    def key_press_event(self, key, gui_event=None) -> None: # pyright: ignore[reportIncompatibleMethodOverride]
        name = 'key_press_event'
        key_press_event = KeyEvent(name, self, key=key, guiEvent=gui_event)
        self.callbacks.process(name, key_press_event)

    def key_release_event(self, key, gui_event=None) -> None: # pyright: ignore[reportIncompatibleMethodOverride]
        name = 'key_release_event'
        key_release_event = KeyEvent(name, self, key=key, guiEvent=gui_event)
        self.callbacks.process(name, key_release_event)


class Navigation(NavigationToolbar2):
    """Navigation for the toolbar buttons
    
    Parameters
    ----------
    canvas : FigureCanvas
        Internal AGG canvas the figure renders into.
    toolbar : `~kivy.uix.layout.Layout`
        Toolbar widget connected with the figure widget
    """

    figure_widget: Any
    """MatplotFigure widget set in `widgets.kv` file"""

    _zoom_info: ZoomInfo
    """Zoom info set in parent class"""

    zoom_y_only: bool = False
    """Flag to zoom in Y axis only."""

    zoom_x_only: bool = False
    """Flag to zoom in X axis only."""

    canvas: FigureCanvas
    """Internal AGG canvas the figure renders into."""

    def __init__(self, canvas: FigureCanvas, toolbar: Any) -> None:
        self.toolbar = toolbar
        super().__init__(canvas)
    
    def release_zoom(self, event: MouseEvent) -> None: # type: ignore
        """Callback for mouse button release in zoom to rect mode."""
        if self._zoom_info is not None:
            ax = self._zoom_info.axes[0]
            start_xy = self._zoom_info.start_xy
            bbox = getattr(ax, 'bbox', None)
            if bbox is None:
                warnings.warn('Axis bbox not found, cannot perform zoom.')
                return
            
            y_beg, y_end = bbox.intervaly
            x_beg, x_end = bbox.intervalx

            if self.zoom_y_only:
                self._zoom_info = self._zoom_info._replace(
                    start_xy=(x_beg, start_xy[1]))
                event.x = int(x_end)
            elif self.zoom_x_only:
                self._zoom_info = self._zoom_info._replace(
                    start_xy=(start_xy[0], y_beg))
                event.y = int(y_end)
                
        super().release_zoom(event)

    def dynamic_update(self) -> None:
        self.canvas.draw()
        
    def draw_rubberband(self, event, x0, y0, x1, y1) -> None:
        """Draw rubberband for zoom."""
        self.figure_widget.draw_rubberband(event, x0, y0, x1, y1)
    
    def remove_rubberband(self) -> None:
        """Remove rubberband for zoom."""
        self.figure_widget.remove_rubberband()
    
    def set_message(self, s: str) -> None:
        if self.toolbar.figure_widget.show_info:
            self.toolbar.info_label.text = s
    
    def mouse_move(self, event) -> None:
        self._update_cursor(event) # type: ignore
        self.set_message(self._mouse_event_to_message(event)) # type: ignore
