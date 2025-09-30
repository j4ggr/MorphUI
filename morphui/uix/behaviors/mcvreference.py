from typing import Any

from ...app import MorphApp


__all__ = ['MorphMCVReferenceBehavior']


class MorphMCVReferenceBehavior:
    """Base class for widgets that need a reference to the main app,
    model, controller, and view instances."""

    _app: Any = None
    """Reference to the running app instance"""

    @property
    def app(self) -> Any:
        """Get the reference to the running app instance
        (read-only)."""
        if self._app is None:
            self._app = MorphApp.get_running_app()
        return self._app
    
    @property
    def model(self) -> Any:
        """Reference to the model instance"""
        return getattr(self.app, 'model', None)
    
    @property
    def controller(self) -> Any:
        """Reference to the controller instance"""
        return getattr(self.app, 'controller', None)
    
    @property
    def view(self) -> Any:
        """Reference to the view instance"""
        return getattr(self.app, 'view', None)