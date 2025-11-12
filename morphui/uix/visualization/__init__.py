"""
MorphUI Visualization Components

Optional matplotlib integration for data visualization within MorphUI applications.

Installation:
    pip install morphui[visualization]

Usage:
    from morphui.uix.visualization import MorphPlotWidget
"""

from typing import NoReturn


try:
    import matplotlib  # noqa: F401
    import numpy  # noqa: F401
    VISUALIZATION_AVAILABLE = True
    
    from .plotting import MorphPlotWidget
    from .chart import MorphChart
    
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
    
    class MorphChart:
        def __init__(self, *args, **kwargs) -> None:
            _missing_dependencies()
    
    __all__ = [
        'MorphPlotWidget', 
        'MorphChart',
        'VISUALIZATION_AVAILABLE'
    ]