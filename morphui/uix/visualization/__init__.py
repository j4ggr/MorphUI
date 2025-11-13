"""
MorphUI Visualization Components

Optional matplotlib integration for data visualization within MorphUI applications.

Installation:
    pip install morphui[visualization]

Usage:
    from morphui.uix.visualization import MorphPlotWidget
"""

from typing import NoReturn, Any


try:
    import matplotlib as mpl
    VISUALIZATION_AVAILABLE = True
    
    from .backend import Navigation
    from .backend import FigureCanvas
    from .plotting import MorphPlotWidget
    from .chart import MorphChart

    import logging

    mpl.use('Agg') # Switch matplotlib backend to non-interactive.
    logging.getLogger('matplotlib.font_manager').disabled = True # Disable annoying font warnings from matplotlib.
    
    __all__ = [
        'MorphPlotWidget',
        'MorphChart',
        'VISUALIZATION_AVAILABLE'
    ]
    
except ImportError:
    VISUALIZATION_AVAILABLE = False
    
    def _missing_dependencies(*args, **kwargs) -> NoReturn:
        raise ImportError(
            'Visualization components require matplotlib and numpy. '
            'Install with: pip install morphui[visualization]')
    
    # Create placeholder classes that raise helpful errors
    class MorphPlotWidget:
        def __init__(self, *args, **kwargs) -> None:
            _missing_dependencies()
    
    # Use a dynamic placeholder typed as Any to avoid static type conflicts
    MorphChart: Any = type(
        'MorphChart',
        (),
        {'__init__': lambda self, *args, **kwargs: _missing_dependencies()})
    
    __all__ = [
        'MorphPlotWidget', 
        'MorphChart',
        'VISUALIZATION_AVAILABLE']
