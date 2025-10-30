from typing import Any

from kivy.uix.widget import Widget
from kivy.properties import ListProperty
from kivy.properties import StringProperty

from ...utils.dotdict import DotDict

__all__ = [
    'MorphIdentificationBehavior',
    'MorphDeclarativeBehavior',]


class MorphIdentificationBehavior:
    """
    A behavior that provides identity-based widget identification.
    
    This behavior allows widgets to have an identity attribute that can 
    be used to identify and reference them within their parent widget. 
    This is particularly useful in declarative UI definitions where you 
    want to reference specific widgets by name.

    When a widget with this behavior has an identity set, and is added 
    to a parent widget that also uses :class:`MorphDeclarativeBehavior`, 
    the widget becomes accessible via the parent's identities dictionary 
    using dot notation.
    
    This functionality is similar to how the ``ids`` attribute works in 
    Kivy's kv language, but implemented directly in Python code.
    
    Examples
    --------
    ```python
    class MyWidget(MorphIdentificationBehavior, Widget):
        pass
    
    widget = MyWidget()
    widget.identity = 'submit_button'
    # When added to a declarative parent:
    # parent.identities.submit_button == widget
    ```
    """

    identity = StringProperty('')
    """The identity of the widget, similar to the id in kv language.
    
    This property allows widgets to be identified and referenced within 
    their parent widget's :attr:`identities` dictionary. When a widget 
    with an identity is added to a parent that uses 
    :class:`MorphDeclarativeBehavior`, it can be accessed via 
    ``parent.identities.widget_identity``.

    :attr:`identity` is a :class:`~kivy.properties.StringProperty` and
    defaults to ''.
    
    Examples
    --------
    ```python
    widget = SomeWidget()
    widget.identity = 'my_button'
    parent.add_widget(widget)
    # Access via parent.identities.my_button
    ```
    """

    _identities = DotDict()
    """Internal storage for the identities-to-widgets mapping.
    
    This private attribute stores the mapping between identity strings
    and their corresponding widget instances. It should not be accessed
    directly - use the :attr:`identities` property instead.
    """

    @property
    def identities(self) -> DotDict:
        """A mapping of child widget identities to their widget
        instances.
        
        This property provides access to child widgets that have been
        assigned identities, similar to the ``ids`` attribute in Kivy's
        kv language. Widgets can be accessed using dot notation.
        
        Returns
        -------
        DotDict
            A dictionary-like object that supports both bracket notation
            (``identities['widget_name']``) and dot notation 
            (``identities.widget_name``) for accessing widgets.
            
        Examples
        --------
        ```python
        # Assuming child widgets have been added with identities:
        button = parent.identities.submit_button
        label = parent.identities['status_label']
        
        # Check if an identity exists:
        if 'optional_widget' in parent.identities:
            widget = parent.identities.optional_widget
        ```
        """
        return self._identities
    
    def _register_declarative_child(self, widget: Any) -> None:
        """Register a child widget's identity for easy access.
        
        This internal method is called when a widget with an identity
        is added to this widget. If the child widget has an identity 
        attribute set, it will be added to the :attr:`identities` 
        mapping for easy reference.
        
        The method ensures that existing identities are preserved when
        updating the mapping to handle multiple inheritance scenarios.
        
        Parameters
        ----------
        widget : Widget
            The child widget to register. If it has an identity 
            attribute, it will be added to the identities mapping.
            
        Notes
        -----
        This is an internal method and should not be called directly.
        It's automatically called by :meth:`add_widget` and similar 
        methods.
        """
        # Always overwrite identities here to avoid class attribute
        # conflicts in multiple inheritance scenarios!
        if hasattr(widget, '_identities'):
            for sub_widget in widget._identities.values():
                self._register_declarative_child(sub_widget)

        identity = getattr(widget, 'identity', None)
        if identity is not None and identity != '':
            self._identities = DotDict(
                {identity: widget} | {**self._identities})
    
    def _unregister_declarative_child(self, widget: Any) -> None:
        """Unregister a child widget's identity from the identities 
        mapping.
        
        This internal method is called when a widget is removed from
        this widget. If the child widget has an identity that exists in
        the :attr:`identities` mapping, it will be removed.
        
        The method ensures that other identities are preserved when
        updating the mapping to handle multiple inheritance scenarios.

        Parameters
        ----------
        widget : Widget
            The child widget to unregister. If it has an identity that
            exists in the mapping, it will be removed.
            
        Notes
        -----
        This is an internal method and should not be called directly.
        It's automatically called by :meth:`remove_widget` and similar 
        methods.
        """
        # Always overwrite identities here to avoid class attribute
        # conflicts in multiple inheritance scenarios!
        if hasattr(widget, '_identities'):
            for sub_widget in widget._identities.values():
                self._unregister_declarative_child(sub_widget)

        identity = getattr(widget, 'identity', None)
        if identity and identity in self._identities:
            self._identities = DotDict(
                {k: v for k, v in self._identities.items() if k != identity})


class MorphDeclarativeBehavior(MorphIdentificationBehavior):
    """A mixin that enables declarative widget composition.
    
    This behavior allows you to define and manage child widgets 
    declaratively using the :attr:`declarative_children` list or by
    passing widgets as constructor arguments. Child widgets are 
    automatically added to the widget tree, and those with identities
    become accessible via the :attr:`identities` mapping.
    
    This provides a Python-based approach to widget composition that's
    similar to Kivy's kv language but more programmatic and flexible.

    Requirements
    ------------
    This behavior requires that the target widget class has:
    
    - :meth:`add_widget` and :meth:`remove_widget` methods
    - A :attr:`children` attribute
    
    Most Kivy widgets satisfy these requirements.
    
    Key Features
    ------------
    - Declarative child widget definition
    - Automatic widget tree management
    - Identity-based widget access
    - Constructor-based widget composition
    - Nested declarative structures
    
    Examples
    --------
    Basic declarative usage:
    
    ```python
    from kivy.uix.label import Label
    from kivy.uix.button import Button
    from kivy.uix.boxlayout import BoxLayout
    from morphui.uix.behaviors import MorphDeclarativeBehavior

    class MyLabel(MorphIdentificationBehavior, Label):
        pass
        
    class MyButton(MorphIdentificationBehavior, Button):
        pass

    class MyLayout(MorphDeclarativeBehavior, BoxLayout):
        pass
        
    layout = MyLayout(
        MyLabel(text='Title', identity='title'),
        MyButton(text='OK', identity='ok_button'))
    
    # Access children by identity
    title = layout.identities.title
    ok_button = layout.identities.ok_button
    ```
    """

    declarative_children = ListProperty([])
    """List of child widgets managed declaratively by this widget.
    
    This property contains the widgets that are added as children to
    this widget through declarative composition. When widgets are added
    to this list, they are automatically added to the widget tree.
    Widgets with identities become accessible via the 
    :attr:`identities` mapping.
    
    The list can be modified directly, and changes will automatically
    trigger the appropriate add/remove operations on the widget tree.
    
    :attr:`declarative_children` is a 
    :class:`~kivy.properties.ListProperty` and defaults to [].
    
    Examples
    --------
    Adding children declaratively:
    
    ```python
    widget.declarative_children = [
        Label(text='First child', identity='label1'),
        Button(text='Second child', identity='btn1')
    ]
    ```
    
    Adding children incrementally:
    
    ```python
    widget.declarative_children.append(
        Label(text='New child', identity='label2')
    )
    ```
    
    Removing children:
    
    ```python
    # Remove by reference
    widget.declarative_children.remove(some_widget)
    
    # Or replace the entire list
    widget.declarative_children = [new_widget1, new_widget2]
    ```
    """

    def __init__(self, *args, **kwargs) -> None:
        """Initialize the declarative behavior.
        
        This constructor allows widgets to be passed as positional
        arguments, which will be automatically added to 
        :attr:`declarative_children`. This provides a convenient way to 
        compose widgets at construction time.
        
        Parameters
        ----------
        *args : Widget
            Child widgets to add to :attr:`declarative_children`.
            These will be automatically added to the widget tree.
        **kwargs : Any
            Additional keyword arguments passed to the parent
            constructor.
            
        Examples
        --------
        ```python
        # Pass children as constructor arguments
        layout = MyDeclarativeWidget(
            Label(text='Child 1', identity='label1'),
            Button(text='Child 2', identity='button1')
        )
        ```
        """
        super().__init__(**kwargs)
        self.declarative_children = list(args)
    
    def add_widget(self, widget: Widget, *args, **kwargs) -> None:
        """Add a widget as a child and register it declaratively.
        
        This method overrides the standard Kivy :meth:`add_widget` to 
        integrate with the declarative behavior system. When a widget is
        added, it's automatically included in 
        :attr:`declarative_children` and registered in the 
        :attr:`identities` mapping if it has an identity.
        
        The method prevents duplicate additions and ensures proper
        synchronization between the declarative children list and the
        actual widget tree.
        
        Parameters
        ----------
        widget : Widget
            The widget to add as a child.
        *args : Any
            Additional positional arguments passed to the parent's
            :meth:`add_widget` method.
        **kwargs : Any
            Additional keyword arguments passed to the parent's
            :meth:`add_widget` method.
            
        Notes
        -----
        If the widget is not already in :attr:`declarative_children`,
        it will be added to the list, which will trigger another call
        to this method to actually add it to the widget tree.
        """
        if widget not in self.declarative_children:
            self.declarative_children = (
                list(self.declarative_children) + [widget])
            return # changing declarative_children will call add_widget again, so return here
        
        super().add_widget(widget, *args, **kwargs) # type: ignore
        self._register_declarative_child(widget)
    
    def remove_widget(self, widget: Widget, *args, **kwargs) -> None:
        """Remove a child widget and unregister it from declarative
        management.
        
        This method overrides the standard Kivy :meth:`remove_widget`
        to integrate with the declarative behavior system. When a widget
        is removed, it's automatically removed from
        :attr:`declarative_children` and unregistered from the
        :attr:`identities` mapping.
        
        The method ensures proper synchronization between the
        declarative children list and the actual widget tree.
        
        Parameters
        ----------
        widget : Widget
            The widget to remove.
        *args : Any
            Additional positional arguments passed to the parent's
            :meth:`remove_widget` method.
        **kwargs : Any
            Additional keyword arguments passed to the parent's
            :meth:`remove_widget` method.
            
        Notes
        -----
        If the widget is in :attr:`declarative_children`, it will be
        removed from the list, which will trigger another call to this
        method to actually remove it from the widget tree.
        """
        if widget in self.declarative_children:
            self.declarative_children = [
                w for w in self.declarative_children if w != widget]
            return # changing declarative_children will call remove_widget again, so return here
        
        super().remove_widget(widget, *args, **kwargs) # type: ignore
        self._unregister_declarative_child(widget)

    def on_declarative_children(
            self, instance: Widget, children: list[Widget]) -> None:
        """Handle changes to the declarative children list.
        
        This method is automatically called when
        :attr:`declarative_children` is modified. It ensures that the 
        actual widget tree stays synchronized with the declarative
        children list by adding new widgets and removing widgets that 
        are no longer in the list.
        
        The synchronization process:
        1. Remove widgets that are in the current children but not in
           the new list
        2. Add widgets that are in the new list but not in the current 
           children
        
        This ensures that the widget tree always reflects the current
        state of :attr:`declarative_children`.
        
        Parameters
        ----------
        instance : Widget
            The widget instance (self) that triggered the property 
            change.
        children : list[Widget]
            The new list of declarative children.
            
        Notes
        -----
        This method is called automatically by Kivy's property system
        when :attr:`declarative_children` changes. You typically don't 
        need to call this method directly.
        """
        current_children = list(getattr(self, 'children', []))

        for child in current_children:
            if child not in children:
                self.remove_widget(child)
        
        for child in children:
            if child not in current_children:
                self.add_widget(child)
