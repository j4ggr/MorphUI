import sys
import pytest
from unittest.mock import Mock, patch
from pathlib import Path

sys.path.append(str(Path(__file__).parent.resolve()))

from kivy.uix.widget import Widget

from morphui.uix.behaviors.declarative import MorphDeclarativeBehavior
from morphui.uix.behaviors.hover import MorphHoverBehavior
from morphui.uix.behaviors.keypress import MorphKeyPressBehavior
from morphui.uix.behaviors.dropdown import MorphDropdownBehavior
from morphui.uix.behaviors.mcvreference import MorphMCVReferenceBehavior
from morphui.utils.dotdict import DotDict


class TestMorphDeclarativeBehavior:
    """Test suite for MorphDeclarativeBehavior class."""

    class TestWidget(MorphDeclarativeBehavior, Widget):
        """Test widget that combines Widget with MorphDeclarativeBehavior."""
        
        def __init__(self, *args, **kwargs):
            Widget.__init__(self, **kwargs)
            MorphDeclarativeBehavior.__init__(self, *args, **kwargs)

    class ChildWidget(MorphDeclarativeBehavior, Widget):
        """Child widget class for testing."""
        
        def __init__(self, **kwargs):
            Widget.__init__(self, **kwargs)
            MorphDeclarativeBehavior.__init__(self, **kwargs)

    def test_initialization(self):
        """Test basic initialization of MorphDeclarativeBehavior."""
        widget = self.TestWidget()
        assert widget.id == ''
        assert widget.declarative_children == []
        assert isinstance(widget.identities, DotDict)

    def test_initialization_with_children(self):
        """Test initialization with child widgets passed as args."""
        child1 = Widget()
        child2 = Widget()
        widget = self.TestWidget(child1, child2)
        assert len(widget.declarative_children) == 2
        assert child1 in widget.declarative_children
        assert child2 in widget.declarative_children

    def test_id_property(self):
        """Test the id property functionality."""
        widget = self.TestWidget()
        widget.id = 'test_widget'
        assert widget.id == 'test_widget'

    def test_identities_property(self):
        """Test the identities property returns DotDict."""
        widget = self.TestWidget()
        identities = widget.identities
        assert isinstance(identities, DotDict)
        assert identities is widget._identities

    def test_add_widget_with_id(self):
        """Test adding a widget with an id updates identities."""
        parent = self.TestWidget()
        child = self.ChildWidget()
        child.id = 'test_child'
        
        parent.add_widget(child)
        
        assert child in parent.declarative_children
        assert parent.identities.test_child is child

    def test_add_widget_without_id(self):
        """Test adding a widget without id still adds to declarative_children."""
        parent = self.TestWidget()
        child = Widget()
        
        parent.add_widget(child)
        
        assert child in parent.declarative_children
        assert len(parent.identities) == 0

    def test_remove_widget(self):
        """Test removing a widget updates declarative_children and identities."""
        parent = self.TestWidget()
        child = self.ChildWidget()
        child.id = 'test_child'
        
        parent.add_widget(child)
        assert child in parent.declarative_children
        assert hasattr(parent.identities, 'test_child')
        
        parent.remove_widget(child)
        assert child not in parent.declarative_children

    def test_register_declarative_child(self):
        """Test the _register_declarative_child method."""
        parent = self.TestWidget()
        child = self.ChildWidget()
        child.id = 'test_child'
        
        parent._register_declarative_child(child)
        
        assert child not in parent.declarative_children
        assert parent.identities.test_child is child

    def test_unregister_declarative_child(self):
        """Test the _unregister_declarative_child method."""
        parent = self.TestWidget()
        child = self.ChildWidget()
        child.id = 'test_child'  # Use id instead of identity
        
        parent._register_declarative_child(child)
        parent._unregister_declarative_child(child)
        
        assert child not in parent.declarative_children


class TestMorphHoverBehavior:
    """Test suite for MorphHoverBehavior class."""

    class TestWidget(Widget, MorphHoverBehavior):
        """Test widget that combines Widget with MorphHoverBehavior."""
        pass

    def test_initialization(self):
        """Test basic initialization of MorphHoverBehavior."""
        widget = self.TestWidget()
        assert hasattr(widget, 'allow_hover')
        assert hasattr(widget, 'hovered')
        assert hasattr(widget, 'edge_hovered')
        assert hasattr(widget, 'corner_hovered')

    def test_hover_events_exist(self):
        """Test that hover events are properly defined."""
        widget = self.TestWidget()
        
        # Check that event methods exist
        assert hasattr(widget, 'on_enter')
        assert hasattr(widget, 'on_leave')
        assert hasattr(widget, 'on_enter_edge')
        assert hasattr(widget, 'on_leave_edge')
        assert hasattr(widget, 'on_enter_corner')
        assert hasattr(widget, 'on_leave_corner')

    @patch('kivy.core.window.Window')
    def test_window_mouse_binding(self, mock_window):
        """Test that the widget binds to window mouse events."""
        self.TestWidget()
        # The widget should bind to window mouse events
        assert mock_window.bind.called

    def test_allow_hover_property(self):
        """Test the allow_hover property."""
        widget = self.TestWidget()
        
        # Test default value and setting
        widget.allow_hover = False
        assert widget.allow_hover is False
        
        widget.allow_hover = True
        assert widget.allow_hover is True


class TestMorphKeyPressBehavior:
    """Test suite for MorphKeyPressBehavior class."""

    class TestWidget(Widget, MorphKeyPressBehavior):
        """Test widget that combines Widget with MorphKeyPressBehavior."""
        pass

    def test_initialization(self):
        """Test basic initialization of MorphKeyPressBehavior."""
        widget = self.TestWidget()
        assert widget.disable_key_press is False
        assert widget.tab_widgets == []
        assert widget.index_last_focus == -1
        assert widget.index_next_focus == 0
        assert widget.keyboard == 0
        assert widget.key_text == ''
        assert widget.keycode == -1

    def test_disable_key_press_property(self):
        """Test the disable_key_press property."""
        widget = self.TestWidget()
        
        widget.disable_key_press = True
        assert widget.disable_key_press is True
        
        widget.disable_key_press = False
        assert widget.disable_key_press is False

    def test_tab_widgets_property(self):
        """Test the tab_widgets property."""
        widget = self.TestWidget()
        test_widgets = [Widget(), Widget(), Widget()]
        
        widget.tab_widgets = test_widgets
        assert widget.tab_widgets == test_widgets
        assert len(widget.tab_widgets) == 3

    def test_focus_index_properties(self):
        """Test focus index properties."""
        widget = self.TestWidget()
        
        widget.index_last_focus = 2
        assert widget.index_last_focus == 2
        
        widget.index_next_focus = 1
        assert widget.index_next_focus == 1

    def test_key_properties(self):
        """Test key-related properties."""
        widget = self.TestWidget()
        
        widget.key_text = 'a'
        assert widget.key_text == 'a'
        
        widget.keycode = 97  # ASCII for 'a'
        assert widget.keycode == 97
        
        widget.keyboard = 1
        assert widget.keyboard == 1

    @patch('kivy.core.window.Window')
    def test_window_keyboard_binding(self, mock_window):
        """Test that the widget binds to window keyboard events."""
        self.TestWidget()
        # The widget should bind to window keyboard events
        assert mock_window.bind.called


class TestMorphDropdownBehavior:
    """Test suite for MorphDropdownBehavior class."""

    class TestWidget(Widget, MorphDropdownBehavior):
        """Test widget that combines Widget with MorphDropdownBehavior."""
        pass

    def test_initialization(self):
        """Test basic initialization of MorphDropdownBehavior."""
        widget = self.TestWidget()
        assert widget.items == []
        assert widget.menu is None
        assert widget.dropdown_position == 'bottom'
        assert widget.menu_open_delay == 0.1
        assert widget.item_viewclass == 'OneLineListItem'

    def test_items_property(self):
        """Test the items property."""
        widget = self.TestWidget()
        test_items = ['Item 1', 'Item 2', 'Item 3']
        
        widget.items = test_items
        assert widget.items == test_items
        assert len(widget.items) == 3

    def test_dropdown_position_property(self):
        """Test the dropdown_position property."""
        widget = self.TestWidget()
        
        for position in ['top', 'bottom', 'center', 'auto']:
            widget.dropdown_position = position
            assert widget.dropdown_position == position

    def test_menu_open_delay_property(self):
        """Test the menu_open_delay property."""
        widget = self.TestWidget()
        
        widget.menu_open_delay = 0.5
        assert widget.menu_open_delay == 0.5

    def test_item_viewclass_property(self):
        """Test the item_viewclass property."""
        widget = self.TestWidget()
        
        widget.item_viewclass = 'TwoLineListItem'
        assert widget.item_viewclass == 'TwoLineListItem'

    def test_current_icon_property(self):
        """Test the current_icon property."""
        widget = self.TestWidget()
        
        # Test that current_icon has a default value from constants
        assert widget.current_icon is not None
        
        widget.current_icon = 'custom-icon'
        assert widget.current_icon == 'custom-icon'

    def test_menu_state_icon_mapping(self):
        """Test the internal menu state icon mapping."""
        widget = self.TestWidget()
        
        # Test that the mapping exists and is a dictionary
        assert hasattr(widget, '_menu_state_icon')
        assert isinstance(widget._menu_state_icon, dict)


class TestMorphMCVReferenceBehavior:
    """Test suite for MorphMCVReferenceBehavior class."""

    class TestWidget(Widget, MorphMCVReferenceBehavior):
        """Test widget that combines Widget with MorphMCVReferenceBehavior."""
        pass

    def test_initialization(self):
        """Test basic initialization of MorphMCVReferenceBehavior."""
        widget = self.TestWidget()
        assert widget._app is None

    @patch('morphui.app.MorphApp.get_running_app')
    def test_app_property(self, mock_get_running_app):
        """Test the app property."""
        mock_app = Mock()
        mock_get_running_app.return_value = mock_app
        
        widget = self.TestWidget()
        app = widget.app
        
        assert app is mock_app
        assert widget._app is mock_app
        mock_get_running_app.assert_called_once()

    @patch('morphui.app.MorphApp.get_running_app')
    def test_app_property_cached(self, mock_get_running_app):
        """Test that the app property is cached after first access."""
        mock_app = Mock()
        mock_get_running_app.return_value = mock_app
        
        widget = self.TestWidget()
        
        # Access app property twice
        app1 = widget.app
        app2 = widget.app
        
        assert app1 is app2
        assert app1 is mock_app
        # Should only call get_running_app once due to caching
        mock_get_running_app.assert_called_once()

    @patch('morphui.app.MorphApp.get_running_app')
    def test_model_property(self, mock_get_running_app):
        """Test the model property."""
        mock_model = Mock()
        mock_app = Mock()
        mock_app.model = mock_model
        mock_get_running_app.return_value = mock_app
        
        widget = self.TestWidget()
        model = widget.model
        
        assert model is mock_model

    @patch('morphui.app.MorphApp.get_running_app')
    def test_model_property_none(self, mock_get_running_app):
        """Test the model property when app has no model."""
        mock_app = Mock()
        del mock_app.model  # Remove model attribute
        mock_get_running_app.return_value = mock_app
        
        widget = self.TestWidget()
        model = widget.model
        
        assert model is None

    @patch('morphui.app.MorphApp.get_running_app')
    def test_controller_property(self, mock_get_running_app):
        """Test the controller property."""
        mock_controller = Mock()
        mock_app = Mock()
        mock_app.controller = mock_controller
        mock_get_running_app.return_value = mock_app
        
        widget = self.TestWidget()
        controller = widget.controller
        
        assert controller is mock_controller

    @patch('morphui.app.MorphApp.get_running_app')
    def test_controller_property_none(self, mock_get_running_app):
        """Test the controller property when app has no controller."""
        mock_app = Mock()
        del mock_app.controller  # Remove controller attribute
        mock_get_running_app.return_value = mock_app
        
        widget = self.TestWidget()
        controller = widget.controller
        
        assert controller is None


if __name__ == '__main__':
    pytest.main([__file__])