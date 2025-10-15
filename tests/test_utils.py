import sys
import pytest

from pathlib import Path
from unittest.mock import Mock, patch

sys.path.append(str(Path(__file__).parent.resolve()))

from morphui.utils.dotdict import DotDict
from morphui.utils.helpers import clamp
from morphui.utils.helpers import FrozenGeometry
from morphui.utils.helpers import calculate_text_size
from morphui.utils.helpers import clean_config


class TestDotDict:

    def test_dotdict_basic(self) -> None:
        data = DotDict({'name': 'John', 'age': 30})
        assert data.name == 'John'
        assert data.age == 30
        data.city = 'New York'
        assert data['city'] == 'New York'

    def test_dotdict_nested(self) -> None:
        nested = DotDict({
            'user': {'name': 'Alice', 'profile': {'role': 'admin'}}
        })
        assert nested.user.name == 'Alice'
        assert nested.user.profile.role == 'admin'
    
    def test_dotdict_keyerror(self) -> None:
        data = DotDict({'name': 'John'})
        with pytest.raises(AttributeError):
            _ = data.age
    
    def test_dotdict_dict_methods(self) -> None:
        regular_dict = {'name': 'John', 'age': 30}
        data = DotDict(regular_dict)
        assert data.keys() == regular_dict.keys()
        assert data.items() == regular_dict.items()
        assert data.get('name') == 'John'
        assert data.get('nonexistent', 'default') == 'default'
        data.update({'city': 'New York'})
        assert data.city == 'New York'


class TestCleanDefaultConfig:
    """Test cases for the clean_config function."""

    def test_no_theme_bindings(self) -> None:
        """Test config without theme_color_bindings."""
        config = {'width': 100, 'height': 50}
        result = clean_config(config, {})
        assert result == config
        assert result is not config  # Should return a copy

    def test_theme_bindings_filtered_by_explicit_config(self) -> None:
        """Test that explicit config removes items from theme_color_bindings."""
        config = {
            'theme_color_bindings': {'color': 'primary', 'background': 'surface'},
            'color': 'red',  # Explicit override
            'width': 100
        }
        result = clean_config(config, {})
        expected = {
            'theme_color_bindings': {'background': 'surface'},
            'color': 'red',
            'width': 100
        }
        assert result == expected

    def test_empty_theme_bindings(self) -> None:
        """Test with empty theme_color_bindings."""
        config = {
            'theme_color_bindings': {},
            'width': 100
        }
        result = clean_config(config, {})
        expected = {'theme_color_bindings': {}, 'width': 100}
        assert result == expected

    def test_all_bindings_overridden(self) -> None:
        """Test when all theme bindings are explicitly overridden."""
        config = {
            'theme_color_bindings': {'color': 'primary', 'background': 'surface'},
            'color': 'red',
            'background': 'blue'
        }
        result = clean_config(config, {})
        expected = {
            'theme_color_bindings': {},
            'color': 'red',
            'background': 'blue'
        }
        assert result == expected


class TestCalculateTextSize:
    """Test cases for the calculate_text_size function."""

    @patch('morphui.utils.helpers.CoreLabel')
    def test_basic_text_size(self, mock_core_label) -> None:
        """Test basic text size calculation."""
        # Mock the CoreLabel to return a predictable content_size
        mock_label = Mock()
        mock_label.content_size = (50, 16)
        mock_core_label.return_value = mock_label
        
        result = calculate_text_size("Hello", font_size=16)
        assert result == (50, 16)
        mock_core_label.assert_called_once_with(text="Hello", font_size=16)
        mock_label.refresh.assert_called_once()

    @patch('morphui.utils.helpers.CoreLabel')
    def test_empty_text(self, mock_core_label) -> None:
        """Test with empty text."""
        mock_label = Mock()
        mock_label.content_size = (0, 16)
        mock_core_label.return_value = mock_label
        
        result = calculate_text_size("", font_size=16)
        assert result == (0, 16)

    @patch('morphui.utils.helpers.CoreLabel')
    def test_larger_font_size(self, mock_core_label) -> None:
        """Test that larger font sizes result in larger text."""
        # First call for small font
        mock_label_small = Mock()
        mock_label_small.content_size = (30, 12)
        
        # Second call for large font
        mock_label_large = Mock()
        mock_label_large.content_size = (60, 24)
        
        mock_core_label.side_effect = [mock_label_small, mock_label_large]
        
        small_result = calculate_text_size("Test", font_size=12)
        large_result = calculate_text_size("Test", font_size=24)
        
        assert large_result[0] > small_result[0]  # width
        assert large_result[1] > small_result[1]  # height

    @patch('morphui.utils.helpers.CoreLabel')
    def test_longer_text(self, mock_core_label) -> None:
        """Test that longer text results in larger width."""
        # First call for short text
        mock_label_short = Mock()
        mock_label_short.content_size = (20, 16)
        
        # Second call for long text
        mock_label_long = Mock()
        mock_label_long.content_size = (80, 16)
        
        mock_core_label.side_effect = [mock_label_short, mock_label_long]
        
        short_result = calculate_text_size("Hi", font_size=16)
        long_result = calculate_text_size("Hello World", font_size=16)
        
        assert long_result[0] > short_result[0]  # width should be larger

    @patch('morphui.utils.helpers.CoreLabel')
    def test_with_font_name(self, mock_core_label) -> None:
        """Test with custom font name."""
        mock_label = Mock()
        mock_label.content_size = (50, 16)
        mock_label.options = {}
        mock_core_label.return_value = mock_label
        
        result = calculate_text_size("Test", font_size=16, font_name="Arial")
        assert result == (50, 16)
        
        # Check that font_name was set in options
        assert mock_label.options['font_name'] == "Arial"


class TestClamp:
    """Test cases for the clamp function."""

    def test_value_within_range(self) -> None:
        """Test value that's already within the specified range."""
        assert clamp(50.0, 0.0, 100.0) == 50.0
        assert clamp(25.5, 10.0, 50.0) == 25.5

    def test_value_below_minimum(self) -> None:
        """Test value below the minimum gets clamped to minimum."""
        assert clamp(-10.0, 0.0, 100.0) == 0.0
        assert clamp(5.0, 10.0, 50.0) == 10.0

    def test_value_above_maximum(self) -> None:
        """Test value above the maximum gets clamped to maximum."""
        assert clamp(150.0, 0.0, 100.0) == 100.0
        assert clamp(75.0, 10.0, 50.0) == 50.0

    def test_no_minimum_constraint(self) -> None:
        """Test clamping with only maximum constraint."""
        assert clamp(50.0, None, 100.0) == 50.0
        assert clamp(150.0, None, 100.0) == 100.0  # Clamped to max
        assert clamp(-50.0, None, 100.0) == -50.0  # No min constraint

    def test_no_maximum_constraint(self) -> None:
        """Test clamping with only minimum constraint."""
        assert clamp(50.0, 0.0, None) == 50.0
        assert clamp(-10.0, 0.0, None) == 0.0  # Clamped to min
        assert clamp(1000.0, 0.0, None) == 1000.0  # No max constraint

    def test_no_constraints(self) -> None:
        """Test clamping with no constraints returns original value."""
        assert clamp(50.0, None, None) == 50.0
        assert clamp(-100.0, None, None) == -100.0
        assert clamp(1000.0, None, None) == 1000.0

    def test_value_at_boundaries(self) -> None:
        """Test values exactly at the boundaries."""
        assert clamp(0.0, 0.0, 100.0) == 0.0
        assert clamp(100.0, 0.0, 100.0) == 100.0

    def test_min_equals_max(self) -> None:
        """Test when minimum equals maximum."""
        assert clamp(50.0, 25.0, 25.0) == 25.0
        assert clamp(10.0, 25.0, 25.0) == 25.0
        assert clamp(30.0, 25.0, 25.0) == 25.0

    def test_invalid_range_raises_error(self) -> None:
        """Test that min > max raises a AssertionError."""
        with pytest.raises(AssertionError):
            clamp(50.0, 100.0, 50.0)

    def test_integer_input(self) -> None:
        """Test that integer inputs work correctly."""
        assert clamp(50, 0.0, 100.0) == 50.0
        assert clamp(150, 0.0, 100.0) == 100.0

    def test_negative_ranges(self) -> None:
        """Test clamping with negative ranges."""
        assert clamp(-50.0, -100.0, -10.0) == -50.0
        assert clamp(-150.0, -100.0, -10.0) == -100.0
        assert clamp(0.0, -100.0, -10.0) == -10.0


class TestFrozenGeometry:
    """Test cases for the FrozenGeometry class."""

    def test_default_initialization(self) -> None:
        """Test creating FrozenGeometry with default values."""
        geo = FrozenGeometry()
        assert geo.x == 0.0
        assert geo.y == 0.0
        assert geo.width == 0.0
        assert geo.height == 0.0

    def test_custom_initialization(self) -> None:
        """Test creating FrozenGeometry with custom values."""
        geo = FrozenGeometry(x=10.0, y=20.0, width=100.0, height=50.0)
        assert geo.x == 10.0
        assert geo.y == 20.0
        assert geo.width == 100.0
        assert geo.height == 50.0

    def test_immutability(self) -> None:
        """Test that FrozenGeometry is immutable."""
        geo = FrozenGeometry(x=10.0, y=20.0, width=100.0, height=50.0)
        with pytest.raises(AttributeError):
            geo.x = 15.0  # Should raise error due to frozen dataclass

    def test_pos_property(self) -> None:
        """Test the pos property returns correct tuple."""
        geo = FrozenGeometry(x=10.0, y=20.0, width=100.0, height=50.0)
        assert geo.pos == (10.0, 20.0)

    def test_size_property(self) -> None:
        """Test the size property returns correct tuple."""
        geo = FrozenGeometry(x=10.0, y=20.0, width=100.0, height=50.0)
        assert geo.size == (100.0, 50.0)

    def test_center_property(self) -> None:
        """Test the center property calculates correctly."""
        geo = FrozenGeometry(x=10.0, y=20.0, width=100.0, height=50.0)
        expected_center = (10.0 + 100.0/2, 20.0 + 50.0/2)
        assert geo.center == expected_center
        assert geo.center == (60.0, 45.0)

    def test_right_property(self) -> None:
        """Test the right property calculates correctly."""
        geo = FrozenGeometry(x=10.0, y=20.0, width=100.0, height=50.0)
        assert geo.right == 110.0  # x + width

    def test_top_property(self) -> None:
        """Test the top property calculates correctly."""
        geo = FrozenGeometry(x=10.0, y=20.0, width=100.0, height=50.0)
        assert geo.top == 70.0  # y + height

    def test_area_property(self) -> None:
        """Test the area property calculates correctly."""
        geo = FrozenGeometry(x=10.0, y=20.0, width=100.0, height=50.0)
        assert geo.area == 5000.0  # width * height

    def test_aspect_ratio_property(self) -> None:
        """Test the aspect_ratio property calculates correctly."""
        geo = FrozenGeometry(x=0.0, y=0.0, width=100.0, height=50.0)
        assert geo.aspect_ratio == 2.0  # width / height

    def test_aspect_ratio_zero_height(self) -> None:
        """Test aspect_ratio returns 1.0 when height is zero."""
        geo = FrozenGeometry(x=0.0, y=0.0, width=100.0, height=0.0)
        assert geo.aspect_ratio == 1.0

    def test_point_delta(self) -> None:
        """Test the point_delta method calculates correctly."""
        geo = FrozenGeometry(x=10.0, y=20.0, width=100.0, height=50.0)
        dx, dy = geo.point_delta(15.0, 25.0)
        assert dx == 5.0  # 15 - 10
        assert dy == 5.0  # 25 - 20

    def test_scaled(self) -> None:
        """Test the scaled method creates correctly scaled geometry."""
        geo = FrozenGeometry(x=10.0, y=20.0, width=100.0, height=50.0)
        scaled = geo.scaled(2.0)
        
        assert scaled.x == 10.0  # Position unchanged
        assert scaled.y == 20.0  # Position unchanged
        assert scaled.width == 200.0  # Scaled by 2
        assert scaled.height == 100.0  # Scaled by 2
        assert scaled is not geo  # Different instance

    def test_translated(self) -> None:
        """Test the translated method creates correctly moved geometry."""
        geo = FrozenGeometry(x=10.0, y=20.0, width=100.0, height=50.0)
        translated = geo.translated(5.0, -10.0)
        
        assert translated.x == 15.0  # Moved by dx
        assert translated.y == 10.0  # Moved by dy
        assert translated.width == 100.0  # Size unchanged
        assert translated.height == 50.0  # Size unchanged
        assert translated is not geo  # Different instance

    def test_resized(self) -> None:
        """Test the resized method creates correctly resized geometry."""
        geo = FrozenGeometry(x=10.0, y=20.0, width=100.0, height=50.0)
        resized = geo.resized(200.0, 75.0)
        
        assert resized.x == 10.0  # Position unchanged
        assert resized.y == 20.0  # Position unchanged
        assert resized.width == 200.0  # New width
        assert resized.height == 75.0  # New height
        assert resized is not geo  # Different instance

    def test_collide_point_inside(self) -> None:
        """Test collide_point returns True for points inside geometry."""
        geo = FrozenGeometry(x=10.0, y=20.0, width=100.0, height=50.0)
        
        # Points inside
        assert geo.collide_point(50.0, 40.0) is True
        assert geo.collide_point(10.0, 20.0) is True  # Bottom-left corner
        assert geo.collide_point(110.0, 70.0) is True  # Top-right corner

    def test_collide_point_outside(self) -> None:
        """Test collide_point returns False for points outside geometry."""
        geo = FrozenGeometry(x=10.0, y=20.0, width=100.0, height=50.0)
        
        # Points outside
        assert geo.collide_point(5.0, 40.0) is False  # Left of geometry
        assert geo.collide_point(115.0, 40.0) is False  # Right of geometry
        assert geo.collide_point(50.0, 15.0) is False  # Below geometry
        assert geo.collide_point(50.0, 75.0) is False  # Above geometry

    def test_distance_to_point_inside(self) -> None:
        """Test distance_to_point returns 0 for points inside geometry."""
        geo = FrozenGeometry(x=10.0, y=20.0, width=100.0, height=50.0)
        assert geo.distance_to_point(50.0, 40.0) == 0.0

    def test_distance_to_point_outside(self) -> None:
        """Test distance_to_point calculates correctly for points outside."""
        geo = FrozenGeometry(x=10.0, y=20.0, width=100.0, height=50.0)
        
        # Point directly left
        distance = geo.distance_to_point(5.0, 40.0)
        assert distance == 5.0  # 5 pixels to the left
        
        # Point diagonally away
        distance = geo.distance_to_point(5.0, 15.0)
        expected = ((5.0)**2 + (5.0)**2)**0.5  # Pythagorean theorem
        assert abs(distance - expected) < 0.001

    def test_from_widget_classmethod(self) -> None:
        """Test creating FrozenGeometry from a widget-like object."""
        # Mock widget object
        class MockWidget:
            def __init__(self):
                self.x = 15
                self.y = 25  
                self.width = 80
                self.height = 60
        
        widget = MockWidget()
        geo = FrozenGeometry.from_widget(widget)
        
        assert geo.x == 15.0
        assert geo.y == 25.0
        assert geo.width == 80.0
        assert geo.height == 60.0

    def test_str_representation(self) -> None:
        """Test string representation is readable."""
        geo = FrozenGeometry(x=10.0, y=20.0, width=100.0, height=50.0)
        str_repr = str(geo)
        assert "FrozenGeometry" in str_repr
        assert "pos=(10.0, 20.0)" in str_repr
        assert "size=(100.0, 50.0)" in str_repr

    def test_repr_representation(self) -> None:
        """Test repr representation is detailed."""
        geo = FrozenGeometry(x=10.0, y=20.0, width=100.0, height=50.0)
        repr_str = repr(geo)
        assert "FrozenGeometry" in repr_str
        assert "x=10.0" in repr_str
        assert "y=20.0" in repr_str
        assert "width=100.0" in repr_str
        assert "height=50.0" in repr_str

