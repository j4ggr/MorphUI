import sys
import pytest
from unittest.mock import Mock, patch
from pathlib import Path

sys.path.append(str(Path(__file__).parent.resolve()))

from kivy.uix.widget import Widget
from kivy.uix.behaviors import FocusBehavior

from morphui.utils.dotdict import DotDict
from morphui.uix.behaviors import MorphHoverBehavior
from morphui.uix.behaviors import MorphHoverEnhancedBehavior
from morphui.uix.behaviors import MorphColorThemeBehavior
from morphui.uix.behaviors import MorphTypographyBehavior
from morphui.uix.behaviors import MorphThemeBehavior
from morphui.uix.behaviors import MorphKeyPressBehavior
from morphui.uix.behaviors import MorphDropdownBehavior
from morphui.uix.behaviors import MorphBackgroundBehavior
from morphui.uix.behaviors import MorphDeclarativeBehavior
from morphui.uix.behaviors import MorphMCVReferenceBehavior
from morphui.uix.behaviors import MorphAutoSizingBehavior


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
        assert widget.identity == ''
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
        widget.identity = 'test_widget'
        assert widget.identity == 'test_widget'

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
        child.identity = 'test_child'
        
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
        child.identity = 'test_child'
        
        parent.add_widget(child)
        assert child in parent.declarative_children
        assert hasattr(parent.identities, 'test_child')
        
        parent.remove_widget(child)
        assert child not in parent.declarative_children

    def test_register_declarative_child(self):
        """Test the _register_declarative_child method."""
        parent = self.TestWidget()
        child = self.ChildWidget()
        child.identity = 'test_child'
        
        parent._register_declarative_child(child)
        
        assert child not in parent.declarative_children
        assert parent.identities.test_child is child

    def test_unregister_declarative_child(self):
        """Test the _unregister_declarative_child method."""
        parent = self.TestWidget()
        child = self.ChildWidget()
        child.identity = 'test_child'  # Use id instead of identity
        
        parent._register_declarative_child(child)
        parent._unregister_declarative_child(child)
        
        assert child not in parent.declarative_children


class TestMorphHoverBehavior:
    """Test suite for MorphHoverBehavior class (basic hover)."""

    class TestWidget(MorphHoverBehavior, Widget):
        """Test widget that combines Widget with MorphHoverBehavior."""
        pass

    @patch('kivy.core.window.Window')
    def test_initialization(self, mock_window):
        """Test basic initialization of MorphHoverBehavior."""
        widget = self.TestWidget()
        assert widget.allow_hover is True
        assert widget.hovered is False
        assert widget.enter_pos == (0, 0)
        assert widget.leave_pos == (0, 0)
        assert widget.current_pos == (0, 0)

    @patch('kivy.core.window.Window')
    def test_basic_hover_events_exist(self, mock_window):
        """Test that basic hover events are properly defined."""
        widget = self.TestWidget()
        
        # Check that basic event methods exist
        assert hasattr(widget, 'on_enter')
        assert hasattr(widget, 'on_leave')
        assert callable(widget.on_enter)
        assert callable(widget.on_leave)

    @patch('kivy.core.window.Window')
    def test_allow_hover_property(self, mock_window):
        """Test the allow_hover property."""
        widget = self.TestWidget()
        
        # Test default value and setting
        widget.allow_hover = False
        assert widget.allow_hover is False
        
        widget.allow_hover = True
        assert widget.allow_hover is True

    @patch('kivy.core.window.Window')
    def test_is_displayed_property(self, mock_window):
        """Test the is_displayed property."""
        widget = self.TestWidget()
        
        # Mock get_root_window to return None (not displayed)
        widget.get_root_window = Mock(return_value=None)
        assert widget.is_displayed is False
        
        # Mock get_root_window to return a window (displayed)
        mock_root_window = Mock()
        widget.get_root_window = Mock(return_value=mock_root_window)
        assert widget.is_displayed is True


class TestMorphHoverEnhancedBehavior:
    """Test suite for MorphHoverEnhancedBehavior class (enhanced hover with edges/corners)."""

    class TestWidget(MorphHoverEnhancedBehavior, Widget):
        """Test widget that combines Widget with MorphHoverEnhancedBehavior."""
        pass

    @patch('kivy.core.window.Window')
    def test_enhanced_initialization(self, mock_window):
        """Test basic initialization of MorphHoverEnhancedBehavior."""
        widget = self.TestWidget()
        assert widget.allow_hover is True
        assert widget.hovered is False
        assert widget.hovered_edges == []
        assert widget.hovered_corner == 'none'
        assert widget.edge_size == 4
        assert widget.left_edge_hovered is False
        assert widget.right_edge_hovered is False
        assert widget.top_edge_hovered is False
        assert widget.bottom_edge_hovered is False

    @patch('kivy.core.window.Window')
    def test_enhanced_hover_events_exist(self, mock_window):
        """Test that enhanced hover events are properly defined."""
        widget = self.TestWidget()
        
        # Check that all event methods exist
        assert hasattr(widget, 'on_enter')
        assert hasattr(widget, 'on_leave')
        assert hasattr(widget, 'on_enter_edge')
        assert hasattr(widget, 'on_leave_edge')
        assert hasattr(widget, 'on_enter_corner')
        assert hasattr(widget, 'on_leave_corner')

    @patch('kivy.core.window.Window')
    def test_edge_constants(self, mock_window):
        """Test edge and corner constants."""
        widget = self.TestWidget()
        assert widget.EDGES == ('left', 'right', 'top', 'bottom')
        assert widget.CORNERS == ('top-left', 'top-right', 'bottom-left', 'bottom-right')

    @patch('kivy.core.window.Window')
    def test_corner_detection(self, mock_window):
        """Test corner detection from edges."""
        widget = self.TestWidget()
        
        # Test no corner when not hovered
        widget.hovered = False
        widget.hovered_edges = ['left', 'top']
        assert widget.get_hovered_corner() == 'none'
        
        # Test corner detection
        widget.hovered = True
        widget.hovered_edges = ['left', 'top']
        assert widget.get_hovered_corner() == 'top-left'
        
        widget.hovered_edges = ['right', 'top']
        assert widget.get_hovered_corner() == 'top-right'
        
        widget.hovered_edges = ['left', 'bottom']
        assert widget.get_hovered_corner() == 'bottom-left'
        
        widget.hovered_edges = ['right', 'bottom']
        assert widget.get_hovered_corner() == 'bottom-right'

    @patch('kivy.core.window.Window')
    def test_edge_size_property(self, mock_window):
        """Test the edge_size property."""
        widget = self.TestWidget()
        
        widget.edge_size = 10
        assert widget.edge_size == 10
        
        widget.edge_size = 2
        assert widget.edge_size == 2


class TestMorphBackgroundBehavior:
    """Test suite for MorphBackgroundBehavior class."""

    class TestWidget(MorphBackgroundBehavior, Widget):
        """Test widget that combines Widget with MorphBackgroundBehavior."""
        pass

    def test_initialization(self):
        """Test basic initialization of MorphBackgroundBehavior."""
        widget = self.TestWidget()
        assert widget.background_color == [1, 1, 1, 1]
        assert widget.radius == [0, 0, 0, 0]
        assert widget.border_width == 0
        assert widget.border_color == [0, 0, 0, 0]

    def test_background_color_property(self):
        """Test the background_color property."""
        widget = self.TestWidget()
        
        test_color = [0.5, 0.5, 0.5, 0.8]
        widget.background_color = test_color
        assert widget.background_color == test_color

    def test_background_radius_property(self):
        """Test the background_radius property."""
        widget = self.TestWidget()
        
        test_radius = [10, 10, 5, 5]
        widget.background_radius = test_radius
        assert widget.background_radius == test_radius

    def test_border_properties(self):
        """Test border-related properties."""
        widget = self.TestWidget()
        
        widget.border_width = 2
        assert widget.border_width == 2
        
        test_border_color = [1, 0, 0, 1]
        widget.border_color = test_border_color
        assert widget.border_color == test_border_color


class TestMorphAutoSizingBehavior:
    """Test suite for MorphAutoSizingBehavior class.
    
    Note: This behavior is complex and requires testing with actual Kivy
    widgets that have texture_size properties (like Label) or 
    size-related behavior. These tests would need a full Kivy 
    environment to be meaningful.
    
    The behavior provides auto_width, auto_height, and auto_size 
    properties that dynamically adjust widget sizes based on content, 
    which is difficult to test properly without real widget rendering.
    
    For now, this test class is commented out as the previous tests were
    testing non-existent properties (auto_size_x, min_width, etc.) that
    don't exist in the actual MorphAutoSizingBehavior implementation.
    """
    pass

    # TODO: Implement proper tests when Kivy environment is available
    # The tests should cover:
    # - auto_width property and _fit_width_to_content()
    # - auto_height property and _fit_height_to_content() 
    # - auto_size property and combined sizing
    # - texture_size binding for Label-like widgets
    # - size_hint management during auto-sizing
    # - _original_size and _original_size_hint storage/restoration


class TestMorphKeyPressBehavior:
    """Test suite for MorphKeyPressBehavior class."""

    class TestWidget(MorphKeyPressBehavior, Widget):
        """Test widget that combines Widget with MorphKeyPressBehavior."""
        pass

    class FocusWidget(FocusBehavior, Widget):
        """Test widget that combines Widget with FocusBehavior."""
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
        test_widgets = [
            self.FocusWidget(), self.FocusWidget(), self.FocusWidget()]
        
        widget.tab_widgets = test_widgets
        assert widget.tab_widgets == test_widgets
        assert len(widget.tab_widgets) == 3
        assert not any(w.focus for w in widget.tab_widgets)

        widget.on_key_press(
            instance=self, keyboard=9, keycode=43, text=None, modifiers=[])
        widget.on_key_release(instance=self, keyboard=9, keycode=43)
        assert list(w.focus for w in widget.tab_widgets).count(True) == 1
        assert widget.index_last_focus == -1
        assert widget.index_next_focus == 0
        assert widget.tab_widgets[0].focus is True

        widget.on_key_press(
            instance=self, keyboard=9, keycode=43, text=None, modifiers=[])
        widget.on_key_release(instance=self, keyboard=9, keycode=43)
        assert list(w.focus for w in widget.tab_widgets).count(True) == 1
        assert widget.index_last_focus == 0
        assert widget.index_next_focus == 1
        assert widget.tab_widgets[1].focus is True

        widget.on_key_press(
            instance=self, keyboard=9, keycode=43, text=None, modifiers=[])
        widget.on_key_release(instance=self, keyboard=9, keycode=43)
        assert list(w.focus for w in widget.tab_widgets).count(True) == 1
        assert widget.index_last_focus == 1
        assert widget.index_next_focus == 2
        assert widget.tab_widgets[2].focus is True

        widget.on_key_press(
            instance=self, keyboard=9, keycode=43, text=None, modifiers=[])
        widget.on_key_release(instance=self, keyboard=9, keycode=43)
        assert list(w.focus for w in widget.tab_widgets).count(True) == 1
        assert widget.index_last_focus == 2
        assert widget.index_next_focus == 0
        assert widget.tab_widgets[0].focus is True

    def test_key_properties(self):
        """Test key-related properties."""
        widget = self.TestWidget()
        widget.key_map = {97: 'a', 98: 'b'}
        widget.on_key_press(
            instance=self, keyboard=9, keycode=97, text='a', modifiers=[])
        assert widget.key_text == 'a'
        assert widget.keycode == 97
        assert widget.keyboard == 9
        widget.on_key_press(
            instance=self, keyboard=9, keycode=98, text='b', modifiers=[])
        assert widget.key_text == 'b'
        assert widget.keycode == 98
        assert widget.keyboard == 9


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


class TestMorphThemeBehavior:
    """Test suite for MorphThemeBehavior class."""

    def setup_method(self):
        """Set up test fixtures before each test method."""
        from morphui.theme.manager import ThemeManager
        self.mock_theme_manager = Mock(spec=ThemeManager)
        self.mock_theme_manager.primary_color = [1.0, 0.0, 0.0, 1.0]
        self.mock_theme_manager.on_primary_color = [1.0, 1.0, 1.0, 1.0]
        self.mock_theme_manager.surface_color = [0.9, 0.9, 0.9, 1.0]
        self.mock_theme_manager.outline_color = [0.5, 0.5, 0.5, 1.0]

    class TestWidget(MorphThemeBehavior, Widget):
        """Test widget that combines Widget with MorphThemeBehavior."""
        
        def __init__(self, **kwargs):
            # Mock properties to avoid Kivy property issues
            self.background_color = None
            self.color = None
            self.border_color = None
            Widget.__init__(self, **kwargs)
            MorphThemeBehavior.__init__(self, **kwargs)

    @patch('morphui.uix.behaviors.theming.MorphApp._theme_manager')
    def test_init_default_properties(self, mock_app_theme_manager):
        """Test MorphThemeBehavior initialization with default values."""
        
        with patch.object(self.TestWidget, 'bind'), \
             patch.object(self.TestWidget, 'register_event_type'):
            
            widget = self.TestWidget()
            
            assert widget.auto_theme is True
            assert widget.theme_color_bindings == {}
            assert widget.theme_style == ''
            assert widget._theme_bound is False

    @patch('morphui.uix.behaviors.theming.MorphApp._theme_manager')
    def test_theme_style_mappings_class_attribute(self, mock_app_theme_manager):
        """Test that theme_style_mappings is properly set from constants."""
        
        with patch.object(self.TestWidget, 'bind'), \
             patch.object(self.TestWidget, 'register_event_type'):
            
            widget = self.TestWidget()
            
            # Check that default styles are available
            from morphui.constants import THEME
            assert 'primary' in widget.theme_style_mappings
            assert 'secondary' in widget.theme_style_mappings
            assert 'surface' in widget.theme_style_mappings
            assert 'error' in widget.theme_style_mappings
            assert 'outline' in widget.theme_style_mappings
            
            # Check that it references THEME.STYLES
            assert widget.theme_style_mappings == THEME.STYLES

    @patch('morphui.uix.behaviors.theming.MorphApp._theme_manager')
    def test_apply_theme_color_success(self, mock_app_theme_manager):
        """Test successful theme color application."""
        
        with patch.object(self.TestWidget, 'bind'), \
             patch.object(self.TestWidget, 'register_event_type'):
            
            widget = self.TestWidget()
            widget._theme_manager = self.mock_theme_manager
            
            # Test successful color application
            result = widget.apply_theme_color('background_color', 'primary_color')
            
            assert result is True
            assert widget.background_color == [1.0, 0.0, 0.0, 1.0]

    @patch('morphui.uix.behaviors.theming.MorphApp._theme_manager')
    def test_apply_theme_color_failure_cases(self, mock_app_theme_manager):
        """Test theme color application failure cases."""
        
        with patch.object(self.TestWidget, 'bind'), \
             patch.object(self.TestWidget, 'register_event_type'):
            
            widget = self.TestWidget()
            widget._theme_manager = self.mock_theme_manager
            
            # Test with non-existent theme color
            result = widget.apply_theme_color('background_color', 'nonexistent_color')
            assert result is False
            
            # Test with non-existent widget property
            result = widget.apply_theme_color('nonexistent_property', 'primary_color')
            assert result is False
            
            # Test with None color value
            self.mock_theme_manager.primary_color = None
            result = widget.apply_theme_color('background_color', 'primary_color')
            assert result is False

    @patch('morphui.uix.behaviors.theming.MorphApp._theme_manager')
    def test_on_theme_style_with_valid_style(self, mock_app_theme_manager):
        """Test on_theme_style method with valid predefined styles."""
        
        with patch.object(self.TestWidget, 'bind'), \
             patch.object(self.TestWidget, 'register_event_type'), \
             patch.object(self.TestWidget, 'dispatch'):
            
            widget = self.TestWidget()
            
            # Test setting primary style
            widget.on_theme_style(widget, 'primary')
            
            # Should update theme_color_bindings with the primary style mappings
            from morphui.constants import THEME
            primary_style = THEME.STYLES['primary']
            
            # Check that all primary style bindings were added
            for widget_prop, theme_color in primary_style.items():
                assert widget_prop in widget.theme_color_bindings
                assert widget.theme_color_bindings[widget_prop] == theme_color

    @patch('morphui.uix.behaviors.theming.MorphApp._theme_manager')
    def test_on_theme_style_with_invalid_style(self, mock_app_theme_manager):
        """Test on_theme_style with invalid style name."""
        
        with patch.object(self.TestWidget, 'bind'), \
             patch.object(self.TestWidget, 'register_event_type'):
            
            widget = self.TestWidget()
            
            # Store initial bindings
            initial_bindings = widget.theme_color_bindings.copy()
            
            # Test with invalid style name - should not change bindings
            widget.on_theme_style(widget, 'invalid_style')
            
            # Bindings should remain unchanged
            assert widget.theme_color_bindings == initial_bindings

    @patch('morphui.uix.behaviors.theming.MorphApp._theme_manager')
    def test_add_custom_style(self, mock_app_theme_manager):
        """Test add_custom_style method."""
        
        with patch.object(self.TestWidget, 'bind'), \
             patch.object(self.TestWidget, 'register_event_type'):
            
            widget = self.TestWidget()
            
            # Add a custom style
            custom_mappings = {
                'background_color': 'tertiary_color',
                'text_color': 'on_tertiary_color'
            }
            
            widget.add_custom_style('custom', custom_mappings)
            
            # Check that custom style was added
            assert 'custom' in widget.theme_style_mappings
            assert widget.theme_style_mappings['custom'] == custom_mappings
            
            # Check that original styles are still there
            assert 'primary' in widget.theme_style_mappings

    @patch('morphui.uix.behaviors.theming.MorphApp._theme_manager')
    def test_add_custom_style_copy_on_write(self, mock_app_theme_manager):
        """Test that adding custom style creates instance copy."""
        
        with patch.object(self.TestWidget, 'bind'), \
             patch.object(self.TestWidget, 'register_event_type'):
            
            widget1 = self.TestWidget()
            widget2 = self.TestWidget()
            
            # Initially both widgets should reference the same class attribute
            assert widget1.theme_style_mappings is widget2.theme_style_mappings
            assert widget1.theme_style_mappings is self.TestWidget.theme_style_mappings
            
            # Add custom style to widget1
            widget1.add_custom_style('custom1', {'background_color': 'primary_color'})
            
            # Now widget1 should have its own copy
            assert widget1.theme_style_mappings is not widget2.theme_style_mappings
            assert widget1.theme_style_mappings is not self.TestWidget.theme_style_mappings
            
            # widget2 should still reference the class attribute
            assert widget2.theme_style_mappings is self.TestWidget.theme_style_mappings
            
            # Only widget1 should have the custom style
            assert 'custom1' in widget1.theme_style_mappings
            assert 'custom1' not in widget2.theme_style_mappings

    @patch('morphui.uix.behaviors.theming.MorphApp._theme_manager')
    def test_refresh_theme_colors(self, mock_app_theme_manager):
        """Test refresh_theme_colors method."""
        
        with patch.object(self.TestWidget, 'bind'), \
             patch.object(self.TestWidget, 'register_event_type'), \
             patch.object(self.TestWidget, 'dispatch'):
            
            widget = self.TestWidget()
            
            # Test manual refresh
            with patch.object(widget, '_update_colors') as mock_update:
                widget.refresh_theme_colors()
                mock_update.assert_called_once()

    def test_on_colors_updated_default_implementation(self):
        """Test that on_colors_updated has a default no-op implementation."""
        with patch.object(self.TestWidget, 'bind'), \
             patch.object(self.TestWidget, 'register_event_type'):
            
            widget = self.TestWidget()
            
            # Should not raise any exception
            result = widget.on_colors_updated()
            assert result is None


class TestMorphColorThemeBehavior:
    """Test suite for MorphColorThemeBehavior class."""

    def setup_method(self):
        """Set up test fixtures before each test method."""
        from morphui.theme.manager import ThemeManager
        self.mock_theme_manager = Mock(spec=ThemeManager)
        self.mock_theme_manager.primary_color = [1.0, 0.0, 0.0, 1.0]
        self.mock_theme_manager.on_primary_color = [1.0, 1.0, 1.0, 1.0]
        self.mock_theme_manager.surface_color = [0.9, 0.9, 0.9, 1.0]
        self.mock_theme_manager.outline_color = [0.5, 0.5, 0.5, 1.0]

    class TestWidget(MorphColorThemeBehavior, Widget):
        """Test widget that combines Widget with MorphColorThemeBehavior."""
        
        def __init__(self, **kwargs):
            # Mock properties to avoid Kivy property issues
            self.background_color = None
            self.color = None
            self.border_color = None
            Widget.__init__(self, **kwargs)
            MorphColorThemeBehavior.__init__(self, **kwargs)

    @patch('morphui.uix.behaviors.theming.MorphApp._theme_manager')
    def test_initialization(self, mock_app_theme_manager):
        """Test MorphColorThemeBehavior initialization."""
        
        with patch.object(self.TestWidget, 'bind'), \
             patch.object(self.TestWidget, 'register_event_type'):
            
            widget = self.TestWidget()
            
            assert widget.auto_theme is True
            assert widget.theme_color_bindings == {}
            assert widget.theme_style == ''

    @patch('morphui.uix.behaviors.theming.MorphApp._theme_manager')
    def test_apply_theme_color(self, mock_app_theme_manager):
        """Test applying theme colors to widget properties."""
        
        with patch.object(self.TestWidget, 'bind'), \
             patch.object(self.TestWidget, 'register_event_type'):
            
            widget = self.TestWidget()
            widget._theme_manager = self.mock_theme_manager
            
            # Test successful color application
            result = widget.apply_theme_color('background_color', 'primary_color')
            
            assert result is True
            assert widget.background_color == [1.0, 0.0, 0.0, 1.0]

    @patch('morphui.uix.behaviors.theming.MorphApp._theme_manager')
    def test_theme_style_application(self, mock_app_theme_manager):
        """Test applying predefined theme styles."""
        
        with patch.object(self.TestWidget, 'bind'), \
             patch.object(self.TestWidget, 'register_event_type'), \
             patch.object(self.TestWidget, 'dispatch'):
            
            widget = self.TestWidget()
            
            # Test setting primary style
            widget.on_theme_style(widget, 'primary')
            
            # Should update theme_color_bindings with the primary style mappings
            from morphui.constants import THEME
            primary_style = THEME.STYLES['primary']
            
            # Check that all primary style bindings were added
            for widget_prop, theme_color in primary_style.items():
                assert widget_prop in widget.theme_color_bindings
                assert widget.theme_color_bindings[widget_prop] == theme_color


class TestMorphTypographyBehavior:
    """Test suite for MorphTypographyBehavior class."""

    def setup_method(self):
        """Set up test fixtures before each test method."""
        from morphui.theme.typography import Typography
        self.mock_typography = Mock(spec=Typography)
        self.mock_typography.get_text_style.return_value = {
            'name': 'Test Font',
            'font_size': 16
        }

    class TestWidget(MorphTypographyBehavior, Widget):
        """Test widget that combines Widget with MorphTypographyBehavior."""
        
        def __init__(self, **kwargs):
            # Mock properties to avoid Kivy property issues
            self.font_name = None
            self.font_size = None
            Widget.__init__(self, **kwargs)
            MorphTypographyBehavior.__init__(self, **kwargs)

    @patch('morphui.uix.behaviors.theming.MorphApp._typography')
    def test_initialization(self, mock_app_typography):
        """Test MorphTypographyBehavior initialization."""
        
        with patch.object(self.TestWidget, 'bind'), \
             patch.object(self.TestWidget, 'register_event_type'):
            
            widget = self.TestWidget()
            
            assert widget.typography_role == 'Label'
            assert widget.typography_size == 'medium'
            assert widget.typography_weight == 'Regular'
            assert widget.auto_typography is True

    @patch('morphui.uix.behaviors.theming.MorphApp._typography')
    def test_apply_typography_style(self, mock_app_typography):
        """Test applying typography styles to widget."""
        
        with patch.object(self.TestWidget, 'bind'), \
             patch.object(self.TestWidget, 'register_event_type'):
            
            widget = self.TestWidget()
            widget._typography = self.mock_typography
            
            # Test successful typography application
            widget.apply_typography_style('Headline', 'large', 'Regular')
            self.mock_typography.get_text_style.assert_called_with(
                role='Headline', size='large', font_weight='Regular')

    @patch('morphui.uix.behaviors.theming.MorphApp._typography')
    def test_typography_properties(self, mock_app_typography):
        """Test typography property changes."""
        
        with patch.object(self.TestWidget, 'bind'), \
             patch.object(self.TestWidget, 'register_event_type'):
            
            widget = self.TestWidget()
            
            # Test changing typography properties
            widget.typography_role = 'Headline'
            assert widget.typography_role == 'Headline'
            
            widget.typography_size = 'large'
            assert widget.typography_size == 'large'
            
            widget.typography_weight = 'Heavy'
            assert widget.typography_weight == 'Heavy'


class TestMorphThemeBehaviorSplit:
    """Test suite for the combined MorphThemeBehavior class after split."""

    class TestWidget(MorphThemeBehavior, Widget):
        """Test widget that combines Widget with MorphThemeBehavior."""
        
        def __init__(self, **kwargs):
            # Mock properties to avoid Kivy property issues
            self.background_color = None
            self.color = None
            self.border_color = None
            self.font_name = None
            self.font_size = None
            Widget.__init__(self, **kwargs)
            MorphThemeBehavior.__init__(self, **kwargs)

    @patch('morphui.uix.behaviors.theming.MorphApp._theme_manager')
    @patch('morphui.uix.behaviors.theming.MorphApp._typography')
    def test_combined_behavior_inheritance(self, mock_app_typography, mock_app_theme_manager):
        """Test that MorphThemeBehavior combines both behaviors."""
        
        with patch.object(self.TestWidget, 'bind'), \
             patch.object(self.TestWidget, 'register_event_type'):
            
            widget = self.TestWidget()
            
            # Should have color theming properties
            assert hasattr(widget, 'auto_theme')
            assert hasattr(widget, 'theme_color_bindings')
            assert hasattr(widget, 'theme_style')
            assert hasattr(widget, 'apply_theme_color')
            
            # Should have typography properties
            assert hasattr(widget, 'typography_role')
            assert hasattr(widget, 'typography_size')
            assert hasattr(widget, 'typography_weight')
            assert hasattr(widget, 'auto_typography')
            assert hasattr(widget, 'apply_typography_style')

    def test_inheritance_chain(self):
        """Test that MorphThemeBehavior inherits from both specialized behaviors."""
        assert issubclass(MorphThemeBehavior, MorphColorThemeBehavior)
        assert issubclass(MorphThemeBehavior, MorphTypographyBehavior)
        
        # Check MRO includes both behaviors
        mro_names = [cls.__name__ for cls in MorphThemeBehavior.__mro__]
        assert 'MorphColorThemeBehavior' in mro_names
        assert 'MorphTypographyBehavior' in mro_names


if __name__ == '__main__':
    pytest.main([__file__])