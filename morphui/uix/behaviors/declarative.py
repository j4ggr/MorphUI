from kivy.uix.widget import Widget
from kivy.properties import ListProperty
from kivy.properties import StringProperty

from ...utils.dotdict import DotDict

__all__ = [
    'MorphDeclarativeBehavior',]


# TODO: Add example usage in docstring
class MorphDeclarativeBehavior:
    """A mixin class that adds declarative behavior to Kivy widgets.
    
    This allows you to define child widgets declaratively by adding them
    to the :attr:`declarative_children` list. Child widgets added to 
    this list will be automatically added as children of this widget.
    The identity of the child widgets will be added to the parent's 
    :attr:`identities` dictionary.

    This class assumes that the widget it is mixed into has an
    :attr:`add_widget` and :attr:`remove_widget` method, as well as
    a :attr:`children` attribute, as is the case with most Kivy widgets.

    If all the child widgets are a subclass of 
    :class:`DeclarativeBehavior`, you can nest declarative widgets
    inside each other. So you can see the widget tree structure in the
    code itself, similar to how it is done in kv language.
    """

    id = StringProperty('')
    """The identity of the widget similar to the id in kv language.
    It can be used to reference the widget in the parent widget's 
    :attr:`identities` dictionary if the parent widget is also a
    :class:`DeclarativeBehavior`.

    :attr:`id` is a :class:`~kivy.properties.StringProperty` and
    defaults to ''."""

    declarative_children = ListProperty([])
    """List of child widgets that are added declaratively to this widget.
    This is similar to adding child widgets in kv language. Child 
    widgets added to this list will be automatically added as children
    of this widget. The identity of the child widgets will be added to
    the parent's :attr:`identities` dictionary.
    
    :attr:`declarative_children` is a 
    :class:`~kivy.properties.ListProperty` and defaults to []."""

    _identities = DotDict()
    """A dictionary mapping identities to widgets. This is similar to
    the :attr:`identities` dictionary in kv language, allowing for easy
    access to child widgets by their identity.
    """

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(**kwargs)
        self.declarative_children = list(args)

    @property
    def identities(self) -> DotDict:
        """A dictionary mapping identities to widgets. This is similar to
        the :attr:`identities` dictionary in kv language, allowing for easy
        access to child widgets by their identity.
        
        Returns
        -------
        DotDict
            A dictionary mapping identities to widgets.
        """
        return self._identities
    
    def add_widget(self, widget: Widget, *args, **kwargs) -> None:
        """Override the add_widget method to add the widget to the
        :attr:`declarative_children` list and update the 
        :attr:`identities` dictionary if the widget has an identity.
        
        Parameters
        ----------
        widget : Widget
            The widget to add.
        *args : Any
            Additional arguments to pass to the super method.
        **kwargs : Any
            Additional keyword arguments to pass to the super method.
        """
        if widget not in self.declarative_children:
            self.declarative_children = (
                list(self.declarative_children) + [widget])
            return # changing declarative_children will call add_widget again
        
        super().add_widget(widget, *args, **kwargs) # type: ignore
        self._register_declarative_child(widget)
    
    def remove_widget(self, widget: Widget, *args, **kwargs) -> None:
        """Override the remove_widget method to remove the widget from
        the :attr:`declarative_children` list and update the 
        :attr:`identities` dictionary if the widget has an identity.
        
        Parameters
        ----------
        widget : Widget
            The widget to remove.
        *args : Any
            Additional arguments to pass to the super method.
        **kwargs : Any
            Additional keyword arguments to pass to the super method.
        """
        if widget in self.declarative_children:
            self.declarative_children = [
                w for w in self.declarative_children if w != widget]
            return # changing declarative_children will call remove_widget again
        
        super().remove_widget(widget, *args, **kwargs) # type: ignore
        self._unregister_declarative_child(widget)
    
    def _register_declarative_child(self, widget: Widget) -> None:
        """Register a declarative child widget. This method is called
        when a widget is added to the :attr:`declarative_children` list
        or when a widget is added using the :meth:`add_widget` method.
        
        Parameters
        ----------
        widget : Widget
            The widget to register.
        """
        identity = getattr(widget, 'id', None)
        if identity:
            self._identities = DotDict(
                {identity: widget} | {**self._identities})
            # Do not overwrite existing identities because of class attributes
            # in case of multiple inheritance.
    
    def _unregister_declarative_child(self, widget: Widget) -> None:
        """Unregister a declarative child widget. This method is called
        when a widget is removed from the :attr:`declarative_children`
        list or when a widget is removed using the :meth:`remove_widget` 
        method.

        Parameters
        ----------
        widget : Widget
            The widget to unregister.
        """
        identity = getattr(widget, 'identity', None)
        if identity and identity in self._identities:
            self._identities = DotDict(
                {k: v for k, v in self._identities.items() if k != identity})
            # Do not overwrite existing identities because of class attributes
            # in case of multiple inheritance.

    def on_declarative_children(
            self, instance: Widget, children: list[Widget]) -> None:
        """Called when the :attr:`declarative_children` list is changed.
        This method ensures that all widgets in the list are added as
        children of this widget and updates the :attr:`identities`
        dictionary.
        
        Parameters
        ----------
        instance : Widget
            The instance of the widget.
        children : list[Widget]
            The new list of declarative children.
        """
        current_children = list(getattr(self, 'children', []))

        for child in current_children:
            if child not in children:
                self.remove_widget(child)
        
        for child in children:
            if child not in current_children:
                self.add_widget(child)
