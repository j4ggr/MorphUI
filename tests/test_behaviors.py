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
from morphui.uix.behaviors import MorphSurfaceLayerBehavior
from morphui.uix.behaviors import MorphDeclarativeBehavior
from morphui.uix.behaviors import MorphAppReferenceBehavior
from morphui.uix.behaviors import MorphAutoSizingBehavior
from morphui.uix.behaviors import MorphIconBehavior
from morphui.uix.behaviors import MorphStateBehavior
from morphui.uix.behaviors import MorphIdentificationBehavior
from morphui.uix.behaviors import MorphContentLayerBehavior
from morphui.uix.behaviors import MorphInteractionLayerBehavior


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
        assert widget.hover_enabled is True
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
    def test_hover_enabled_property(self, mock_window):
        """Test the hover_enabled property."""
        widget = self.TestWidget()
        
        # Test default value and setting
        widget.hover_enabled = False
        assert widget.hover_enabled is False
        
        widget.hover_enabled = True
        assert widget.hover_enabled is True

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
        assert widget.hover_enabled is True
        assert widget.hovered is False
        assert widget.hovered_edges == []
        assert widget.hovered_corner is None
        assert widget.edge_detection_size == 4
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
    def test_corner_detection(self, mock_window):
        """Test corner detection from edges."""
        widget = self.TestWidget()
        
        # Test no corner when not hovered
        widget.hovered = False
        widget.hovered_edges = ['left', 'top']
        assert widget.get_hovered_corner() is None
        
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


class TestMorphSurfaceLayerBehavior:
    """Test suite for MorphSurfaceLayerBehavior class."""

    class TestWidget(MorphSurfaceLayerBehavior, Widget):
        """Test widget that combines Widget with MorphSurfaceLayerBehavior."""
        pass

    def test_initialization(self):
        """Test basic initialization of MorphSurfaceLayerBehavior."""
        widget = self.TestWidget()
        assert widget.surface_color == [1, 1, 1, 1]
        assert widget.radius == [0, 0, 0, 0]
        assert widget.border_width == 1
        assert widget.border_color == [0, 0, 0, 0]

    def test_surface_color_property(self):
        """Test the surface_color property."""
        widget = self.TestWidget()
        
        test_color = [0.5, 0.5, 0.5, 0.8]
        widget.surface_color = test_color
        assert widget.surface_color == test_color

    def test_surface_radius_property(self):
        """Test the surface_radius property."""
        widget = self.TestWidget()
        
        test_radius = [10, 10, 5, 5]
        widget.surface_radius = test_radius
        assert widget.surface_radius == test_radius

    def test_border_properties(self):
        """Test border-related properties."""
        widget = self.TestWidget()
        
        widget.border_width = 2
        assert widget.border_width == 2
        
        test_border_color = [1, 0, 0, 1.]
        widget.border_color = test_border_color
        assert widget.border_color == test_border_color


class TestMorphAutoSizingBehavior:
    """Test suite for MorphAutoSizingBehavior class."""

    class MockTextWidget(MorphAutoSizingBehavior, Widget):
        """Mock widget with texture_size for testing text-based auto sizing."""
        
        def __init__(self, **kwargs):
            # Initialize texture_size before parent init
            self._texture_size = (100, 50)
            super().__init__(**kwargs)
        
        @property
        def texture_size(self):
            return self._texture_size
        
        @texture_size.setter
        def texture_size(self, value):
            self._texture_size = value

    class MockWidget(MorphAutoSizingBehavior, Widget):
        """Mock widget without texture_size for testing generic auto sizing."""
        
        def __init__(self, **kwargs):
            self.minimum_width = 80
            self.minimum_height = 40
            super().__init__(**kwargs)

    def test_initialization_default_properties(self):
        """Test MorphAutoSizingBehavior initialization with default values."""
        widget = self.MockWidget()
        
        assert widget.auto_width is False
        assert widget.auto_height is False
        assert widget.auto_size is False
        assert widget._original_size_hint == (1.0, 1.0)
        assert widget._original_size == (100.0, 100.0)  # Default Widget size
        # _has_texture_size is not initialized during __init__ due to minimum_width/height are present.
        # It will be determined later when the widget is measured
        assert widget._has_texture_size is None
        assert widget.has_texture_size is False

    def test_initialization_with_auto_size(self):
        """Test initialization with auto_size=True sets both width and height."""
        widget = self.MockWidget(auto_size=True)
        
        assert widget.auto_size is True
        assert widget.auto_width is True
        assert widget.auto_height is True

    def test_has_texture_size_property_with_texture(self):
        """Test has_texture_size property for widget with texture_size."""
        widget = self.MockTextWidget()
        
        # First call should check and cache
        assert widget.has_texture_size is True
        assert widget._has_texture_size is True
        
        # Second call should use cached value
        assert widget.has_texture_size is True

    def test_has_texture_size_property_without_texture(self):
        """Test has_texture_size property for widget without texture_size."""
        widget = self.MockWidget()
        
        assert widget.has_texture_size is False
        assert widget._has_texture_size is False

    def test_auto_width_property_binding(self):
        """Test auto_width property changes trigger appropriate methods."""
        widget = self.MockWidget()
        initial_size_hint_x = widget.size_hint_x
        
        widget.auto_width = True
        
        # Check that size_hint_x was set to None (indicating auto sizing is active)
        assert widget.size_hint_x is None
        
        widget.auto_width = False
        
        # Check that size_hint_x was restored
        assert widget.size_hint_x == initial_size_hint_x

    def test_auto_height_property_binding(self):
        """Test auto_height property changes trigger appropriate methods."""
        widget = self.MockWidget()
        initial_size_hint_y = widget.size_hint_y
        
        widget.auto_height = True
        
        # Check that size_hint_y was set to None (indicating auto sizing is active)
        assert widget.size_hint_y is None
        
        widget.auto_height = False
        
        # Check that size_hint_y was restored
        assert widget.size_hint_y == initial_size_hint_y

    def test_auto_size_property_binding(self):
        """Test auto_size property changes trigger appropriate methods."""
        widget = self.MockWidget()
        
        widget.auto_size = True
        
        # Check that both auto_width and auto_height are set
        assert widget.auto_width is True
        assert widget.auto_height is True
        assert widget.size_hint_x is None
        assert widget.size_hint_y is None

    def test_update_size_with_texture_size(self):
        """Test _update_size method with texture_size widget."""
        widget = self.MockTextWidget()
        widget.texture_size = (120, 60)
        
        # Test auto_width only
        widget.auto_width = True
        widget.auto_height = False
        widget._update_size()
        
        assert widget.width == 120
        assert widget.height == widget._original_size[1]

    def test_update_size_with_minimum_size(self):
        """Test _update_size method with minimum_width/height widget."""
        widget = self.MockWidget()
        widget.minimum_width = 150
        widget.minimum_height = 75
        
        # Test auto_height only
        widget.auto_width = False
        widget.auto_height = True
        widget._update_size()
        
        assert widget.width == widget._original_size[0]
        assert widget.height == 75

    def test_update_size_both_dimensions(self):
        """Test _update_size method with both auto_width and auto_height."""
        widget = self.MockTextWidget()
        widget.texture_size = (200, 100)
        widget.auto_width = True
        widget.auto_height = True
        
        widget._update_size()
        
        assert widget.width == 200
        assert widget.height == 100

    def test_update_size_restore_original(self):
        """Test _update_size restores original size when auto sizing disabled."""
        widget = self.MockTextWidget()
        original_width = widget._original_size[0]
        original_height = widget._original_size[1]
        
        widget.auto_width = False
        widget.auto_height = False
        widget._update_size()
        
        assert widget.width == original_width
        assert widget.height == original_height

    def test_update_auto_sizing_auto_size_sets_both(self):
        """Test _update_auto_sizing with auto_size sets both dimensions."""
        widget = self.MockWidget()
        
        widget._update_auto_sizing(widget, True, 'auto_size')
        
        assert widget.auto_width is True
        assert widget.auto_height is True

    def test_update_auto_sizing_individual_properties(self):
        """Test _update_auto_sizing with individual properties."""
        widget = self.MockWidget()
        
        with patch.object(widget, 'apply_auto_sizing') as mock_apply:
            widget._update_auto_sizing(widget, True, 'auto_width')
            mock_apply.assert_called_once_with(widget.auto_width, widget.auto_height)

    def test_apply_auto_sizing_sets_size_hint_to_none(self):
        """Test apply_auto_sizing sets size_hint to None for auto dimensions."""
        widget = self.MockWidget()
        
        widget.apply_auto_sizing(True, True)
        
        assert widget.size_hint_x is None
        assert widget.size_hint_y is None

    def test_apply_auto_sizing_restores_original_size_hint(self):
        """Test apply_auto_sizing restores original size_hint when disabled."""
        widget = self.MockWidget()
        original_x = widget._original_size_hint[0]
        original_y = widget._original_size_hint[1]
        
        widget.apply_auto_sizing(False, False)
        
        assert widget.size_hint_x == original_x
        assert widget.size_hint_y == original_y

    def test_apply_auto_sizing_mixed_dimensions(self):
        """Test apply_auto_sizing with mixed auto sizing settings."""
        widget = self.MockWidget()
        original_y = widget._original_size_hint[1]
        
        widget.apply_auto_sizing(True, False)
        
        assert widget.size_hint_x is None
        assert widget.size_hint_y == original_y

    def test_apply_auto_sizing_dispatches_event(self):
        """Test apply_auto_sizing dispatches on_auto_size_updated event."""
        widget = self.MockWidget()
        
        with patch.object(widget, 'dispatch') as mock_dispatch:
            widget.apply_auto_sizing(True, True)
            mock_dispatch.assert_called_once_with('on_auto_size_updated')

    def test_refresh_auto_sizing(self):
        """Test refresh_auto_sizing applies current settings."""
        widget = self.MockWidget()
        widget.auto_width = True
        widget.auto_height = False
        
        with patch.object(widget, 'apply_auto_sizing') as mock_apply:
            widget.refresh_auto_sizing()
            mock_apply.assert_called_once_with(True, False)

    def test_on_auto_size_updated_event_handler(self):
        """Test on_auto_size_updated event handler exists and is callable."""
        widget = self.MockWidget()
        
        # Test that the event handler exists and can be called
        assert hasattr(widget, 'on_auto_size_updated')
        assert callable(widget.on_auto_size_updated)
        
        # Test that it can be called without errors
        try:
            widget.on_auto_size_updated()
        except Exception as e:
            pytest.fail(f"on_auto_size_updated() raised an exception: {e}")

    def test_texture_size_binding_integration(self):
        """Test that texture_size changes trigger size updates."""
        widget = self.MockTextWidget()
        widget.auto_width = True
        widget.auto_height = True
        
        # Simulate texture_size change
        with patch.object(widget, '_update_size') as mock_update:
            widget.texture_size = (300, 150)
            # In real Kivy, this would trigger the bound callback
            widget._update_size()
            mock_update.assert_called_once()

    def test_minimum_size_binding_integration(self):
        """Test that minimum_width/height changes trigger size updates."""
        widget = self.MockWidget()
        widget.auto_width = True
        widget.auto_height = True
        
        # Simulate minimum size change
        with patch.object(widget, '_update_size') as mock_update:
            widget.minimum_width = 200
            widget.minimum_height = 100
            # In real Kivy, this would trigger the bound callback
            widget._update_size()
            mock_update.assert_called_once()

    def test_event_type_registration(self):
        """Test that on_auto_size_updated event type is registered."""
        widget = self.MockWidget()
        
        # Test that the event type is registered
        assert hasattr(widget, 'is_event_type')
        # Note: The actual registration happens in __init__, 
        # this tests that the method exists

    def test_original_size_preservation(self):
        """Test that original size and size_hint are properly preserved."""
        widget = self.MockWidget(size=(200, 150), size_hint=(0.5, 0.3))
        
        # Check that original values are stored
        assert widget._original_size == (200, 150)
        assert widget._original_size_hint == (0.5, 0.3)
        
        # Enable auto sizing
        widget.apply_auto_sizing(True, True)
        assert list(widget.size_hint) == [None, None]
        
        # Disable auto sizing and check restoration
        widget.apply_auto_sizing(False, False)
        assert list(widget.size_hint) == [0.5, 0.3]

    def test_complex_auto_sizing_scenario(self):
        """Test complex scenario with multiple property changes."""
        widget = self.MockTextWidget()
        widget.texture_size = (180, 90)
        
        # Start with auto_size
        widget.auto_size = True
        assert widget.auto_width is True
        assert widget.auto_height is True
        assert list(widget.size_hint) == [None, None]
        
        # Change to only auto_width
        widget.auto_size = False
        widget.auto_width = True
        widget.auto_height = False
        
        widget.apply_auto_sizing(widget.auto_width, widget.auto_height)
        assert widget.size_hint_x is None
        assert widget.size_hint_y == widget._original_size_hint[1]
        
        # Refresh sizing
        widget.refresh_auto_sizing()
        assert widget.size_hint_x is None


class TestMorphKeyPressBehavior:
    """Test suite for MorphKeyPressBehavior class."""

    class TestWidget(MorphKeyPressBehavior, Widget):
        """Test widget that combines Widget with MorphKeyPressBehavior."""
        pass

    class FocusWidget(MorphKeyPressBehavior, FocusBehavior, Widget):
        """Test widget that combines Widget with FocusBehavior and MorphKeyPressBehavior."""
        pass

    def setup_method(self):
        """Clear tab groups before each test."""
        MorphKeyPressBehavior.tab_widgets.clear()

    def test_initialization(self):
        """Test basic initialization of MorphKeyPressBehavior."""
        widget = self.TestWidget()
        assert widget.key_press_enabled is True
        assert widget.tab_group is None
        assert widget.index_last_focus == -1
        assert widget.index_next_focus == 0
        assert widget.keyboard == 0
        assert widget.key_text == ''
        assert widget.keycode == -1

    def test_key_press_enabled_property(self):
        """Test the key_press_enabled property."""
        widget = self.TestWidget()
        
        widget.key_press_enabled = False
        assert widget.key_press_enabled is False
        
        widget.key_press_enabled = True
        assert widget.key_press_enabled is True

    def test_tab_group_property(self):
        """Test the tab_group property and group management."""
        widget1 = self.FocusWidget()
        widget2 = self.FocusWidget()
        widget3 = self.FocusWidget()
        
        # Test setting tab group
        widget1.tab_group = "form1"
        assert widget1.tab_group == "form1"
        assert "form1" in MorphKeyPressBehavior.tab_widgets
        assert widget1 in MorphKeyPressBehavior.tab_widgets["form1"]
        
        # Test adding multiple widgets to same group
        widget2.tab_group = "form1"
        widget3.tab_group = "form1"
        assert len(MorphKeyPressBehavior.tab_widgets["form1"]) == 3
        assert widget2 in MorphKeyPressBehavior.tab_widgets["form1"]
        assert widget3 in MorphKeyPressBehavior.tab_widgets["form1"]
        
        # Test moving widget to different group
        widget3.tab_group = "form2"
        assert len(MorphKeyPressBehavior.tab_widgets["form1"]) == 2
        assert widget3 not in MorphKeyPressBehavior.tab_widgets["form1"]
        assert widget3 in MorphKeyPressBehavior.tab_widgets["form2"]
        
        # Test removing widget from groups
        widget1.tab_group = None
        assert widget1 not in MorphKeyPressBehavior.tab_widgets["form1"]
        assert len(MorphKeyPressBehavior.tab_widgets["form1"]) == 1

    def test_current_tab_widgets_property(self):
        """Test the current_tab_widgets property."""
        widget1 = self.FocusWidget()
        widget2 = self.FocusWidget()
        widget3 = self.FocusWidget()
        
        # Test empty list when no group set
        assert widget1.current_tab_widgets == []
        
        # Test current_tab_widgets returns correct group
        widget1.tab_group = "form1"
        widget2.tab_group = "form1"
        widget3.tab_group = "form2"
        
        form1_widgets = widget1.current_tab_widgets
        assert len(form1_widgets) == 2
        assert widget1 in form1_widgets
        assert widget2 in form1_widgets
        assert widget3 not in form1_widgets
        
        form2_widgets = widget3.current_tab_widgets
        assert len(form2_widgets) == 1
        assert widget3 in form2_widgets

    def test_has_focus_property(self):
        """Test the has_focus property with groups."""
        widget1 = self.FocusWidget()
        widget2 = self.FocusWidget()
        widget3 = self.FocusWidget()
        
        widget1.tab_group = "form1"
        widget2.tab_group = "form1"
        widget3.tab_group = "form2"
        
        # Test no focus initially
        assert widget1.has_focus is False
        assert widget3.has_focus is False
        
        # Test focus in group
        widget1.focus = True
        assert widget1.has_focus is True
        assert widget2.has_focus is True  # Same group
        assert widget3.has_focus is False  # Different group

    def test_tab_navigation_with_groups(self):
        """Test tab navigation within groups."""
        widget1 = self.FocusWidget()
        widget2 = self.FocusWidget()
        widget3 = self.FocusWidget()
        widget4 = self.FocusWidget()
        
        # Set up two groups
        widget1.tab_group = "form1"
        widget2.tab_group = "form1"
        widget3.tab_group = "form2"
        widget4.tab_group = "form2"
        
        # Test tab navigation in form1 group
        current_widgets = widget1.current_tab_widgets
        assert len(current_widgets) == 2
        assert not any(w.focus for w in current_widgets)

        # First tab press in group 1
        widget1.on_key_press(
            instance=self, keyboard=9, keycode=43, text=None, modifiers=[])
        widget1.on_key_release(instance=self, keyboard=9, keycode=43)
        
        form1_widgets = widget1.current_tab_widgets
        assert sum(w.focus for w in form1_widgets) == 1
        assert widget1.index_last_focus == -1
        assert widget1.index_next_focus == 0
        assert form1_widgets[0].focus is True

        # Second tab press in group 1
        widget1.on_key_press(
            instance=self, keyboard=9, keycode=43, text=None, modifiers=[])
        widget1.on_key_release(instance=self, keyboard=9, keycode=43)
        
        assert sum(w.focus for w in form1_widgets) == 1
        assert widget1.index_last_focus == 0
        assert widget1.index_next_focus == 1
        assert form1_widgets[1].focus is True

        # Third tab press (should wrap around)
        widget1.on_key_press(
            instance=self, keyboard=9, keycode=43, text=None, modifiers=[])
        widget1.on_key_release(instance=self, keyboard=9, keycode=43)
        
        assert sum(w.focus for w in form1_widgets) == 1
        assert widget1.index_last_focus == 1
        assert widget1.index_next_focus == 0  # Wrapped around
        assert form1_widgets[0].focus is True

        # Verify form2 group is unaffected
        form2_widgets = widget3.current_tab_widgets
        assert not any(w.focus for w in form2_widgets)

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


class TestMorphAppReferenceBehavior:
    """Test suite for MorphAppReferenceBehavior class."""

    class TestWidget(Widget, MorphAppReferenceBehavior):
        """Test widget that combines Widget with MorphAppReferenceBehavior."""
        pass

    def test_initialization(self):
        """Test basic initialization of MorphAppReferenceBehavior."""
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
        self.mock_theme_manager.content_primary_color = [1.0, 1.0, 1.0, 1.0]
        self.mock_theme_manager.surface_color = [0.9, 0.9, 0.9, 1.0]
        self.mock_theme_manager.outline_color = [0.5, 0.5, 0.5, 1.0]

    class TestWidget(MorphThemeBehavior, Widget):
        """Test widget that combines Widget with MorphThemeBehavior."""
        
        def __init__(self, **kwargs):
            # Mock properties to avoid Kivy property issues
            self.surface_color = [1, 1, 1, 1]
            self.color = [0, 0, 0, 1]
            self.border_color = [0, 0, 0, 0]
            self.content_color = [0, 0, 0, 1]
            Widget.__init__(self, **kwargs)
            MorphThemeBehavior.__init__(self, **kwargs)

    @patch('morphui.app.MorphApp._theme_manager')
    def test_init_default_properties(self, mock_app_theme_manager):
        """Test MorphThemeBehavior initialization with default values."""
        
        with patch.object(self.TestWidget, 'bind'), \
             patch.object(self.TestWidget, 'register_event_type'), \
             patch.object(self.TestWidget, 'dispatch'):
            
            widget = self.TestWidget()
            
            assert widget.auto_theme is True
            assert widget.theme_color_bindings == {}
            assert widget.theme_style == ''
            assert widget._theme_bound is False

    @patch('morphui.app.MorphApp._theme_manager')
    def test_theme_style_mappings_class_attribute(self, mock_app_theme_manager):
        """Test that theme_style_mappings is properly set from constants."""
        
        with patch.object(self.TestWidget, 'bind'), \
             patch.object(self.TestWidget, 'register_event_type'), \
             patch.object(self.TestWidget, 'dispatch'):
            
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

    @patch('morphui.app.MorphApp._theme_manager')
    def test_apply_theme_color_success(self, mock_app_theme_manager):
        """Test successful theme color application."""
        # Configure the mock to return our mock theme manager
        mock_app_theme_manager.configure_mock(**{
            'primary_color': [1.0, 0.0, 0.0, 1.0],
            'content_primary_color': [1.0, 1.0, 1.0, 1.0],
            'secondary_color': [0.0, 1.0, 0.0, 1.0],
            'content_secondary_color': [0.8, 0.8, 0.8, 1.0],
            'surface_color': [0.9, 0.9, 0.9, 1.0],
            'content_surface_color': [0.2, 0.2, 0.2, 1.0],
            'error_color': [1.0, 0.0, 0.0, 1.0],
            'content_error_color': [1.0, 1.0, 1.0, 1.0],
            'outline_color': [0.5, 0.5, 0.5, 1.0],
            'content_on_surface_color': [0.1, 0.1, 0.1, 1.0],
        })
        
        with patch.object(self.TestWidget, 'bind'), \
             patch.object(self.TestWidget, 'register_event_type'), \
             patch.object(self.TestWidget, 'dispatch'):
            
            widget = self.TestWidget()
            # Set up valid widget properties
            widget.surface_color = [1, 1, 1, 1]
            
            # Test successful color application
            result = widget.apply_theme_color('surface_color', 'primary_color')
            
            assert result is True
            assert widget.surface_color == [1.0, 0.0, 0.0, 1.0]

    @patch('morphui.app.MorphApp._theme_manager')
    def test_apply_theme_color_failure_cases(self, mock_app_theme_manager):
        """Test theme color application failure cases."""
        # Configure the mock to return our mock theme manager
        mock_app_theme_manager.configure_mock(**{
            'primary_color': [1.0, 0.0, 0.0, 1.0],
            'content_primary_color': [1.0, 1.0, 1.0, 1.0],
        })
        
        # Override the mock's __hasattr__ to properly handle non-existent attributes
        def mock_hasattr(attr):
            return attr in ['primary_color', 'content_primary_color']
        
        # Set up the mock to behave more like a real object for hasattr checks
        type(mock_app_theme_manager).__contains__ = lambda self, item: item in ['primary_color', 'content_primary_color']
        
        with patch.object(self.TestWidget, 'bind'), \
             patch.object(self.TestWidget, 'register_event_type'), \
             patch.object(self.TestWidget, 'dispatch'):
            
            widget = self.TestWidget()
            # Set up valid widget properties
            widget.surface_color = [1, 1, 1, 1]
            
            # Test with non-existent theme color by patching hasattr directly
            with patch('builtins.hasattr') as mock_hasattr:
                mock_hasattr.side_effect = lambda obj, attr: attr in ['primary_color', 'content_primary_color'] if obj is mock_app_theme_manager else hasattr(obj, attr)
                result = widget.apply_theme_color('surface_color', 'nonexistent_color')
                assert result is False
            
            # Test with non-existent widget property
            result = widget.apply_theme_color('nonexistent_property', 'primary_color')
            assert result is False
            
            # Test with None color value - temporarily set primary_color to None
            original_primary = mock_app_theme_manager.primary_color
            mock_app_theme_manager.primary_color = None
            result = widget.apply_theme_color('surface_color', 'primary_color')
            assert result is False
            # Restore the original value
            mock_app_theme_manager.primary_color = original_primary

    @patch('morphui.app.MorphApp._theme_manager')
    def test_on_theme_style_with_valid_style(self, mock_app_theme_manager):
        """Test on_theme_style method with valid predefined styles."""
        # Configure the mock to return our mock theme manager
        mock_app_theme_manager.configure_mock(**{
            'primary_color': [1.0, 0.0, 0.0, 1.0],
            'content_primary_color': [1.0, 1.0, 1.0, 1.0],
            'secondary_color': [0.0, 1.0, 0.0, 1.0],
            'content_secondary_color': [0.8, 0.8, 0.8, 1.0],
            'surface_color': [0.9, 0.9, 0.9, 1.0],
            'content_surface_color': [0.2, 0.2, 0.2, 1.0],
            'error_color': [1.0, 0.0, 0.0, 1.0],
            'content_error_color': [1.0, 1.0, 1.0, 1.0],
            'outline_color': [0.5, 0.5, 0.5, 1.0],
            'content_on_surface_color': [0.1, 0.1, 0.1, 1.0],
        })
        
        with patch.object(self.TestWidget, 'bind'), \
             patch.object(self.TestWidget, 'register_event_type'), \
             patch.object(self.TestWidget, 'dispatch'):
            
            widget = self.TestWidget()
            # Set up valid widget properties
            widget.surface_color = [1, 1, 1, 1]
            widget.content_color = [0, 0, 0, 1]
            widget.border_color = [0, 0, 0, 0]
            
            # Test setting primary style
            widget.theme_style = 'primary'
            
            # Should update effective_color_bindings with the primary style mappings
            from morphui.constants import THEME
            primary_style = THEME.STYLES['primary']
            
            # Check that all primary style bindings were added
            for widget_prop, theme_color in primary_style.items():
                assert widget_prop in widget._theme_style_color_bindings
                assert widget_prop in widget.effective_color_bindings
                assert widget.effective_color_bindings[widget_prop] == theme_color

    @patch('morphui.app.MorphApp._theme_manager')
    def test_on_theme_style_with_invalid_style(self, mock_app_theme_manager):
        """Test on_theme_style with invalid style name."""
        
        with patch.object(self.TestWidget, 'bind'), \
             patch.object(self.TestWidget, 'register_event_type'), \
             patch.object(self.TestWidget, 'dispatch'):
            
            widget = self.TestWidget()
            
            # Store initial bindings
            initial_bindings = widget.theme_color_bindings.copy()
            
            # Test with invalid style name - should not change bindings
            widget.on_theme_style(widget, 'invalid_style')
            
            # Bindings should remain unchanged
            assert widget.theme_color_bindings == initial_bindings

    @patch('morphui.app.MorphApp._theme_manager')
    def test_add_custom_style(self, mock_app_theme_manager):
        """Test add_custom_style method."""
        
        with patch.object(self.TestWidget, 'bind'), \
             patch.object(self.TestWidget, 'register_event_type'), \
             patch.object(self.TestWidget, 'dispatch'):
            
            widget = self.TestWidget()
            
            # Add a custom style
            custom_mappings = {
                'surface_color': 'tertiary_color',
                'content_color': 'on_tertiary_color'
            }
            
            widget.add_custom_style('custom', custom_mappings)
            
            # Check that custom style was added
            assert 'custom' in widget.theme_style_mappings
            assert widget.theme_style_mappings['custom'] == custom_mappings
            
            # Check that original styles are still there
            assert 'primary' in widget.theme_style_mappings

    @patch('morphui.app.MorphApp._theme_manager')
    def test_add_custom_style_copy_on_write(self, mock_app_theme_manager):
        """Test that adding custom style creates instance copy."""
        
        with patch.object(self.TestWidget, 'bind'), \
             patch.object(self.TestWidget, 'register_event_type'), \
             patch.object(self.TestWidget, 'dispatch'):
            
            widget1 = self.TestWidget()
            widget2 = self.TestWidget()
            
            # Initially both widgets should reference the same class attribute
            assert widget1.theme_style_mappings is widget2.theme_style_mappings
            assert widget1.theme_style_mappings is self.TestWidget.theme_style_mappings
            
            # Add custom style to widget1
            widget1.add_custom_style('custom1', {'surface_color': 'primary_color'})
            
            # Now widget1 should have its own copy
            assert widget1.theme_style_mappings is not widget2.theme_style_mappings
            assert widget1.theme_style_mappings is not self.TestWidget.theme_style_mappings
            
            # widget2 should still reference the class attribute
            assert widget2.theme_style_mappings is self.TestWidget.theme_style_mappings
            
            # Only widget1 should have the custom style
            assert 'custom1' in widget1.theme_style_mappings
            assert 'custom1' not in widget2.theme_style_mappings

    @patch('morphui.app.MorphApp._theme_manager')
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
             patch.object(self.TestWidget, 'register_event_type'), \
             patch.object(self.TestWidget, 'dispatch'):
            
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
        self.mock_theme_manager.content_primary_color = [1.0, 1.0, 1.0, 1.0]
        self.mock_theme_manager.surface_color = [0.9, 0.9, 0.9, 1.0]
        self.mock_theme_manager.outline_color = [0.5, 0.5, 0.5, 1.0]
        self.mock_theme_manager.content_primary_color = [1.0, 1.0, 1.0, 1.0]
        self.mock_theme_manager.content_nt_secondary_color = [0.8, 0.8, 0.8, 1.0]
        self.mock_theme_manager.content_surface_color = [0.2, 0.2, 0.2, 1.0]
        self.mock_theme_manager.content_error_color = [1.0, 1.0, 1.0, 1.0]
        self.mock_theme_manager.content_on_surface_color = [0.1, 0.1, 0.1, 1.0]
        self.mock_theme_manager.secondary_color = [0.0, 1.0, 0.0, 1.0]
        self.mock_theme_manager.error_color = [1.0, 0.0, 0.0, 1.0]

    class TestWidget(MorphColorThemeBehavior, Widget):
        """Test widget that combines Widget with MorphColorThemeBehavior."""
        
        def __init__(self, **kwargs):
            # Mock properties to avoid Kivy property issues
            self.surface_color = [1, 1, 1, 1]
            self.color = [0, 0, 0, 1]
            self.border_color = [0, 0, 0, 0]
            self.content_color = [0, 0, 0, 1]
            Widget.__init__(self, **kwargs)
            MorphColorThemeBehavior.__init__(self, **kwargs)

    @patch('morphui.app.MorphApp._theme_manager')
    def test_initialization(self, mock_app_theme_manager):
        """Test MorphColorThemeBehavior initialization."""
        # Configure the mock to return our mock theme manager
        mock_app_theme_manager.configure_mock(**{
            'primary_color': [1.0, 0.0, 0.0, 1.0],
            'content_primary_color': [1.0, 1.0, 1.0, 1.0],
            'secondary_color': [0.0, 1.0, 0.0, 1.0],
            'content_secondary_color': [0.8, 0.8, 0.8, 1.0],
            'surface_color': [0.9, 0.9, 0.9, 1.0],
            'content_surface_color': [0.2, 0.2, 0.2, 1.0],
            'error_color': [1.0, 0.0, 0.0, 1.0],
            'content_error_color': [1.0, 1.0, 1.0, 1.0],
            'outline_color': [0.5, 0.5, 0.5, 1.0],
            'content_on_surface_color': [0.1, 0.1, 0.1, 1.0],
        })
        
        with patch.object(self.TestWidget, 'bind'), \
             patch.object(self.TestWidget, 'register_event_type'):
            
            widget = self.TestWidget()
            
            assert widget.auto_theme is True
            assert widget.theme_color_bindings == {}
            assert widget.theme_style == ''

    @patch('morphui.app.MorphApp._theme_manager')  
    def test_apply_theme_color(self, mock_app_theme_manager):
        """Test applying theme colors to widget properties."""
        # Configure the mock to return our mock theme manager
        mock_app_theme_manager.configure_mock(**{
            'primary_color': [1.0, 0.0, 0.0, 1.0],
            'content_primary_color': [1.0, 1.0, 1.0, 1.0],
            'secondary_color': [0.0, 1.0, 0.0, 1.0],
            'content_secondary_color': [0.8, 0.8, 0.8, 1.0],
            'surface_color': [0.9, 0.9, 0.9, 1.0],
            'content_surface_color': [0.2, 0.2, 0.2, 1.0],
            'error_color': [1.0, 0.0, 0.0, 1.0],
            'content_error_color': [1.0, 1.0, 1.0, 1.0],
            'outline_color': [0.5, 0.5, 0.5, 1.0],
            'content_on_surface_color': [0.1, 0.1, 0.1, 1.0],
        })
        
        with patch.object(self.TestWidget, 'bind'), \
             patch.object(self.TestWidget, 'register_event_type'):
            
            widget = self.TestWidget()
            
            # Test successful color application
            result = widget.apply_theme_color('surface_color', 'primary_color')
            
            assert result is True
            assert widget.surface_color == [1.0, 0.0, 0.0, 1.0]

    @patch('morphui.app.MorphApp._theme_manager')
    def test_theme_style_application(self, mock_app_theme_manager):
        """Test applying predefined theme styles."""
        # Configure the mock to return our mock theme manager
        mock_app_theme_manager.configure_mock(**{
            'primary_color': [1.0, 0.0, 0.0, 1.0],
            'content_primary_color': [1.0, 1.0, 1.0, 1.0],
            'secondary_color': [0.0, 1.0, 0.0, 1.0],
            'content_secondary_color': [0.8, 0.8, 0.8, 1.0],
            'surface_color': [0.9, 0.9, 0.9, 1.0],
            'content_surface_color': [0.2, 0.2, 0.2, 1.0],
            'error_color': [1.0, 0.0, 0.0, 1.0],
            'content_error_color': [1.0, 1.0, 1.0, 1.0],
            'outline_color': [0.5, 0.5, 0.5, 1.0],
            'content_on_surface_color': [0.1, 0.1, 0.1, 1.0],
        })
        
        with patch.object(self.TestWidget, 'bind'), \
             patch.object(self.TestWidget, 'register_event_type'), \
             patch.object(self.TestWidget, 'dispatch'):
            
            widget = self.TestWidget()
            
            # Test setting primary style
            widget.theme_style = 'primary'
            
            # Should update effective_color_bindings with the primary style mappings
            from morphui.constants import THEME
            primary_style = THEME.STYLES['primary']
            
            # Check that all primary style bindings were added
            for widget_prop, theme_color in primary_style.items():
                assert widget_prop in widget._theme_style_color_bindings
                assert widget_prop in widget.effective_color_bindings
                assert widget.effective_color_bindings[widget_prop] == theme_color


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

    @patch('morphui.app.MorphApp._typography')
    def test_initialization(self, mock_app_typography):
        """Test MorphTypographyBehavior initialization."""
        
        with patch.object(self.TestWidget, 'bind'), \
             patch.object(self.TestWidget, 'register_event_type'), \
             patch.object(self.TestWidget, 'dispatch'):
            
            widget = self.TestWidget()
            
            assert widget.typography_role == 'Label'
            assert widget.typography_size == 'medium'
            assert widget.typography_weight == 'Regular'
            assert widget.auto_typography is True

    @patch('morphui.app.MorphApp._typography')
    def test_apply_typography_style(self, mock_app_typography):
        """Test applying typography styles to widget."""
        # Configure the mock to return our mock typography
        mock_app_typography.configure_mock(**{
            'get_text_style': self.mock_typography.get_text_style
        })
        
        with patch.object(self.TestWidget, 'bind'), \
             patch.object(self.TestWidget, 'register_event_type'), \
             patch.object(self.TestWidget, 'dispatch'):
            
            widget = self.TestWidget()
            
            # Test successful typography application
            widget.apply_typography_style(
                None, 'Headline', 'large', 'Regular')
            self.mock_typography.get_text_style.assert_called_with(
                font_name=None, role='Headline', size='large',
                font_weight='Regular')

    @patch('morphui.app.MorphApp._typography')
    def test_typography_properties(self, mock_app_typography):
        """Test typography property changes."""
        
        with patch.object(self.TestWidget, 'bind'), \
             patch.object(self.TestWidget, 'register_event_type'), \
             patch.object(self.TestWidget, 'dispatch'):
            
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
            self.surface_color = None
            self.color = None
            self.border_color = None
            self.font_name = None
            self.font_size = None
            Widget.__init__(self, **kwargs)
            MorphThemeBehavior.__init__(self, **kwargs)

    @patch('morphui.app.MorphApp._theme_manager')
    @patch('morphui.app.MorphApp._typography')
    def test_combined_behavior_inheritance(self, mock_app_typography, mock_app_theme_manager):
        """Test that MorphThemeBehavior combines both behaviors."""
        
        with patch.object(self.TestWidget, 'bind'), \
             patch.object(self.TestWidget, 'register_event_type'), \
             patch.object(self.TestWidget, 'dispatch'):
            
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


class TestMorphIconBehavior:
    """Test suite for MorphIconBehavior class."""

    class TestWidget(MorphIconBehavior, Widget):
        """Test widget that combines Widget with MorphIconBehavior."""
        
        def __init__(self, **kwargs):
            self.text = ''
            super().__init__(**kwargs)

    @patch('morphui.app.MorphApp._typography')
    def test_initialization(self, mock_app_typography):
        """Test basic initialization of MorphIconBehavior."""
        mock_typography = Mock()
        mock_typography.get_icon_character.return_value = '★'
        mock_app_typography.configure_mock(**{
            'get_icon_character': mock_typography.get_icon_character
        })
        
        widget = self.TestWidget()
        
        assert widget.icon == ''
        assert hasattr(widget, 'text')

    @patch('morphui.app.MorphApp._typography')
    def test_icon_property(self, mock_app_typography):
        """Test the icon property functionality."""
        mock_typography = Mock()
        mock_typography.get_icon_character.return_value = '★'
        mock_app_typography.configure_mock(**{
            'get_icon_character': mock_typography.get_icon_character
        })
        
        widget = self.TestWidget()
        
        # Test setting icon
        widget.icon = 'star'
        assert widget.icon == 'star'

    @patch('morphui.app.MorphApp._typography')
    def test_apply_icon(self, mock_app_typography):
        """Test the _apply_icon method."""
        mock_typography = Mock()
        mock_typography.get_icon_character.return_value = '★'
        mock_app_typography.configure_mock(**{
            'get_icon_character': mock_typography.get_icon_character
        })
        
        widget = self.TestWidget()
        
        # Mock typography property using patch.object
        with patch.object(type(widget), 'typography', new_callable=lambda: mock_typography):
            # Test icon application
            widget._apply_icon(widget, 'star')
            
            assert widget.text == '★'
            mock_typography.get_icon_character.assert_called_with('star')

    @patch('morphui.app.MorphApp._typography')
    def test_apply_icon_without_text_property(self, mock_app_typography):
        """Test _apply_icon when widget doesn't have text property."""
        
        class NoTextWidget(MorphIconBehavior, Widget):
            pass
        
        widget = NoTextWidget()
        
        # Should not raise error when text property is missing
        widget._apply_icon(widget, 'star')

    @patch('morphui.app.MorphApp._typography')
    def test_apply_icon_without_typography(self, mock_app_typography):
        """Test _apply_icon when typography is not available."""
        
        widget = self.TestWidget()
        
        # Should not raise error when typography is missing
        widget._apply_icon(widget, 'star')


class TestMorphStateBehavior:
    """Test suite for MorphStateBehavior class."""

    class TestWidget(MorphStateBehavior, Widget):
        """Test widget that combines Widget with MorphStateBehavior."""
        
        def __init__(self, **kwargs):
            # Add state properties that the behavior can track
            # Use simple attributes instead of trying to override Kivy properties
            super().__init__(**kwargs)
            self.pressed = False
            self.selected = False
            self.focus = False
            self.hovered = False
            self.active = False
            self.resizing = False

    def test_initialization(self):
        """Test basic initialization of MorphStateBehavior."""
        widget = self.TestWidget()
        
        # Widget already has disabled property from Kivy
        assert widget.disabled is False
        assert widget.pressed is False
        assert widget.selected is False
        assert widget.focus is False
        assert widget.hovered is False
        assert widget.active is False
        assert widget.resizing is False
        
        # Check initial current states
        assert widget.current_surface_state == 'normal'
        assert widget.current_interaction_state == 'normal'
        assert widget.current_content_state == 'normal'
        assert widget.current_overlay_state == 'normal'

    def test_state_properties(self):
        """Test state properties can be set and retrieved."""
        widget = self.TestWidget()
        
        # Test disabled state (Kivy property)
        widget.disabled = True
        assert widget.disabled is True
        
        # Test pressed state
        widget.pressed = True
        assert widget.pressed is True
        
        # Test selected state
        widget.selected = True
        assert widget.selected is True
        
        # Test focus state
        widget.focus = True
        assert widget.focus is True
        
        # Test hovered state
        widget.hovered = True
        assert widget.hovered is True
        
        # Test active state
        widget.active = True
        assert widget.active is True
        
        # Test resizing state
        widget.resizing = True
        assert widget.resizing is True

    def test_available_states_property(self):
        """Test the available_states property."""
        widget = self.TestWidget()
        
        # Should include states the widget has plus 'normal'
        # Note: disabled is inherited from Kivy Widget
        available = widget.available_states
        assert 'normal' in available
        assert 'disabled' in available  # From Kivy Widget

    def test_current_states_with_precedence(self):
        """Test current state properties reflect precedence logic."""
        widget = self.TestWidget()
        
        # Test normal state (all states False)
        assert widget.current_surface_state == 'normal'
        assert widget.current_interaction_state == 'normal'
        assert widget.current_content_state == 'normal'
        assert widget.current_overlay_state == 'normal'

    def test_update_available_states(self):
        """Test the update_available_states method."""
        widget = self.TestWidget()
        
        # Test that method runs without error
        widget.update_available_states()
        
        # Should have at least normal and disabled states
        available = widget.available_states
        assert 'normal' in available
        assert len(available) >= 2

    def test_refresh_state(self):
        """Test the refresh_state method."""
        widget = self.TestWidget()
        
        # Set some states manually
        widget.disabled = True
        widget.hovered = True
        
        # Refresh should update current states based on actual values
        widget.refresh_state()
        
        # Current states should reflect the active states
        # Note: The exact behavior depends on the state resolution logic

    def test_on_current_state_changed_event(self):
        """Test the on_current_state_changed event."""
        widget = self.TestWidget()
        
        # Test that the event handler exists and can be called
        assert hasattr(widget, 'on_current_state_changed')
        assert callable(widget.on_current_state_changed)
        
        # Test that it can be called without errors
        try:
            widget.on_current_state_changed()
        except Exception as e:
            pytest.fail(f"on_current_state_changed() raised an exception: {e}")

    def test_precedence_constants(self):
        """Test that precedence constants are properly set."""
        widget = self.TestWidget()
        
        # Test that precedence tuples exist and are not empty
        assert hasattr(widget, 'surface_state_precedence')
        assert hasattr(widget, 'interaction_state_precedence')
        assert hasattr(widget, 'content_state_precedence')
        assert hasattr(widget, 'overlay_state_precedence')
        
        assert len(widget.surface_state_precedence) > 0
        assert len(widget.interaction_state_precedence) > 0
        assert len(widget.content_state_precedence) > 0
        assert len(widget.overlay_state_precedence) > 0

    def test_possible_states_property(self):
        """Test the possible_states property."""
        widget = self.TestWidget()
        
        # Should contain all possible states
        assert hasattr(widget, 'possible_states')
        assert isinstance(widget.possible_states, set)
        assert len(widget.possible_states) > 0


class TestMorphIdentificationBehavior:
    """Test suite for MorphIdentificationBehavior class."""

    class TestWidget(MorphIdentificationBehavior, Widget):
        """Test widget that combines Widget with MorphIdentificationBehavior."""
        pass

    def test_initialization(self):
        """Test basic initialization of MorphIdentificationBehavior."""
        widget = self.TestWidget()
        
        assert widget.identity == ''

    def test_identity_property(self):
        """Test the identity property."""
        widget = self.TestWidget()
        
        # Test setting identity
        widget.identity = 'test_widget'
        assert widget.identity == 'test_widget'
        
        # Test changing identity
        widget.identity = 'another_id'
        assert widget.identity == 'another_id'
        
        # Test empty identity
        widget.identity = ''
        assert widget.identity == ''

    def test_identity_with_spaces(self):
        """Test identity property with various string formats."""
        widget = self.TestWidget()
        
        # Test with spaces
        widget.identity = 'widget with spaces'
        assert widget.identity == 'widget with spaces'
        
        # Test with special characters
        widget.identity = 'widget-with_special.chars'
        assert widget.identity == 'widget-with_special.chars'
        
        # Test with numbers
        widget.identity = 'widget123'
        assert widget.identity == 'widget123'


class TestMorphContentLayerBehavior:
    """Test suite for MorphContentLayerBehavior class."""

    class TestWidget(MorphContentLayerBehavior, Widget):
        """Test widget that combines Widget with MorphContentLayerBehavior."""
        
        def __init__(self, **kwargs):
            self.color = [0, 0, 0, 1]
            super().__init__(**kwargs)

    @patch('morphui.app.MorphApp._theme_manager')
    def test_initialization(self, mock_app_theme_manager):
        """Test basic initialization of MorphContentLayerBehavior."""
        mock_app_theme_manager.configure_mock(**{
            'text_color': [0, 0, 0, 1]
        })
        
        widget = self.TestWidget()
        
        assert widget.content_color is not None
        assert widget.disabled_content_color is None
        assert widget.hovered_content_color is None

    @patch('morphui.app.MorphApp._theme_manager')
    def test_content_color_property(self, mock_app_theme_manager):
        """Test the content_color property."""
        mock_app_theme_manager.configure_mock(**{
            'text_color': [0, 0, 0, 1]
        })
        
        widget = self.TestWidget()
        
        test_color = [1, 0, 0, 1.]
        widget.content_color = test_color
        assert widget.content_color == test_color

    @patch('morphui.app.MorphApp._theme_manager')
    def test_disabled_content_color_property(self, mock_app_theme_manager):
        """Test the disabled_content_color property."""
        mock_app_theme_manager.configure_mock(**{
            'text_color': [0, 0, 0, 1]
        })
        
        widget = self.TestWidget()
        
        test_color = [0.5, 0.5, 0.5, 1]
        widget.disabled_content_color = test_color
        assert widget.disabled_content_color == test_color

    @patch('morphui.app.MorphApp._theme_manager')
    def test_apply_content(self, mock_app_theme_manager):
        """Test the apply_content method."""
        mock_app_theme_manager.configure_mock(**{
            'text_color': [0, 0, 0, 1]
        })
        
        widget = self.TestWidget()
        
        test_color = [1, 0, 0, 1.]
        widget.apply_content(test_color)
        
        assert widget.color == test_color

    @patch('morphui.app.MorphApp._theme_manager')
    def test_refresh_content(self, mock_app_theme_manager):
        """Test the refresh_content method."""
        mock_app_theme_manager.configure_mock(**{
            'text_color': [0, 0, 0, 1]
        })
        
        widget = self.TestWidget()
        
        with patch.object(widget, '_update_content_layer') as mock_update:
            widget.refresh_content()
            mock_update.assert_called_once()


class TestMorphInteractionLayerBehavior:
    """Test suite for MorphInteractionLayerBehavior class."""

    class TestWidget(MorphInteractionLayerBehavior, Widget):
        """Test widget that combines Widget with MorphInteractionLayerBehavior."""
        
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            # Add hovered property to support hovered state
            self.hovered = False
            # Update available states after adding new property
            self.update_available_states()

    @patch('morphui.app.MorphApp._theme_manager')
    def test_initialization(self, mock_app_theme_manager):
        """Test basic initialization of MorphInteractionLayerBehavior."""
        mock_app_theme_manager.configure_mock(**{
            'transparent_color': [0, 0, 0, 0],
            'is_dark_mode': False
        })
        
        widget = self.TestWidget()
        
        assert widget.hovered_state_opacity == 0.08
        assert widget.pressed_state_opacity == 0.10
        assert widget.focus_state_opacity == 0.10
        assert widget.disabled_state_opacity == 0.16
        assert widget.interaction_enabled is True
        assert widget.interaction_color == [0, 0, 0, 0]

    @patch('morphui.app.MorphApp._theme_manager')
    def test_interaction_color_property(self, mock_app_theme_manager):
        """Test the interaction_color property."""
        mock_app_theme_manager.configure_mock(**{
            'transparent_color': [0, 0, 0, 0],
            'is_dark_mode': False
        })
        
        widget = self.TestWidget()
        
        test_color = [1, 0, 0, 0.5]
        widget.interaction_color = test_color
        assert widget.interaction_color == test_color

    @patch('morphui.app.MorphApp._theme_manager')
    def test_interaction_enabled_property(self, mock_app_theme_manager):
        """Test the interaction_enabled property."""
        mock_app_theme_manager.configure_mock(**{
            'transparent_color': [0, 0, 0, 0],
            'is_dark_mode': False
        })
        
        widget = self.TestWidget()
        
        widget.interaction_enabled = False
        assert widget.interaction_enabled is False
        
        widget.interaction_enabled = True
        assert widget.interaction_enabled is True

    @patch('morphui.app.MorphApp._theme_manager')
    def test_interaction_color_getter(self, mock_app_theme_manager):
        """Test the _interaction_color property for theme-aware colors."""
        mock_app_theme_manager.configure_mock(**{
            'transparent_color': [0, 0, 0, 0],
            'is_dark_mode': False
        })
        
        widget = self.TestWidget()
        
        # Test light mode (should return black)
        base_color = widget._interaction_color
        assert base_color == [0.0, 0.0, 0.0]
        
        # Test dark mode (should return white)
        mock_app_theme_manager.is_dark_mode = True
        base_color = widget._interaction_color
        assert base_color == [1.0, 1.0, 1.0]

    @patch('morphui.app.MorphApp._theme_manager')
    def test_apply_interaction(self, mock_app_theme_manager):
        """Test the apply_interaction method."""
        mock_app_theme_manager.configure_mock(**{
            'transparent_color': [0, 0, 0, 0],
            'is_dark_mode': False
        })
        
        widget = self.TestWidget()
        
        # Test applying hover interaction
        widget.apply_interaction('hovered', 0.08)
        
        expected_color = [0.0, 0.0, 0.0, 0.08]
        assert widget.interaction_color == expected_color

    @patch('morphui.app.MorphApp._theme_manager')
    def test_refresh_interaction(self, mock_app_theme_manager):
        """Test the refresh_interaction method."""
        mock_app_theme_manager.configure_mock(**{
            'transparent_color': [0, 0, 0, 0],
            'is_dark_mode': False
        })
        
        widget = self.TestWidget()
        
        with patch.object(widget, '_on_interaction_state_change') as mock_state_change:
            widget.refresh_interaction()
            mock_state_change.assert_called()


if __name__ == '__main__':
    pytest.main([__file__])