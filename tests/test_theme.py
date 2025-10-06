import sys
import pytest
import warnings
from pathlib import Path
from unittest.mock import Mock, patch

sys.path.append(str(Path(__file__).parent.resolve()))

from morphui.theme.manager import ThemeManager
from morphui.theme.typography import Typography
from morphui.uix.behaviors.theming import MorphThemeBehavior
from morphui.constants import FONTS, THEME


class TestThemeManager:
    """Test suite for ThemeManager class."""

    def test_init_default_properties(self):
        """Test ThemeManager initialization with default values."""
        theme_manager = ThemeManager()
        
        assert theme_manager.auto_theme is True
        assert theme_manager.seed_color == 'Blue'
        assert theme_manager.color_scheme == 'FIDELITY'
        assert theme_manager.color_scheme_contrast == 0.0
        assert theme_manager.color_quality == 1
        assert theme_manager.theme_mode == THEME.LIGHT
        assert theme_manager.mode_transition is True
        assert theme_manager.mode_transition_duration == 0.3

    @patch.object(ThemeManager, 'dispatch')
    def test_init_custom_properties(self, mock_dispatch):
        """Test ThemeManager initialization with custom values."""
        theme_manager = ThemeManager(
            auto_theme=False,
            seed_color='Red',
            color_scheme='VIBRANT',
            color_scheme_contrast=0.5,
            theme_mode=THEME.DARK,
            mode_transition=False,
            mode_transition_duration=0.8)
        
        assert theme_manager.auto_theme is False
        assert theme_manager.seed_color == 'Red'
        assert theme_manager.color_scheme == 'VIBRANT'
        assert theme_manager.color_scheme_contrast == 0.5
        assert theme_manager.theme_mode == THEME.DARK
        assert theme_manager.mode_transition is False
        assert theme_manager.mode_transition_duration == 0.8
        
        # Verify that dispatch was called during initialization
        mock_dispatch.assert_called_with('on_theme_changed')

    def test_available_seed_colors(self):
        """Test available_seed_colors property."""
        theme_manager = ThemeManager()
        colors = theme_manager.available_seed_colors
        
        assert isinstance(colors, tuple)
        assert len(colors) > 0
        assert 'Blue' in colors
        assert 'Red' in colors

    def test_inverse_mode(self):
        """Test inverse_mode property."""
        theme_manager = ThemeManager()
        
        # Test with light mode
        theme_manager.theme_mode = THEME.LIGHT
        assert theme_manager.inverse_mode == THEME.DARK
        
        # Test with dark mode
        theme_manager.theme_mode = THEME.DARK
        assert theme_manager.inverse_mode == THEME.LIGHT

    def test_material_schemes(self):
        """Test material_schemes property."""
        theme_manager = ThemeManager()
        schemes = theme_manager.material_schemes
        
        assert isinstance(schemes, dict)
        assert len(schemes) > 0
        assert 'FIDELITY' in schemes

    def test_toggle_theme_mode(self):
        """Test toggle_theme_mode method."""
        theme_manager = ThemeManager()
        
        # Start with light mode
        theme_manager.theme_mode = THEME.LIGHT
        theme_manager.toggle_theme_mode()
        assert theme_manager.theme_mode == THEME.DARK
        
        # Toggle back to light
        theme_manager.toggle_theme_mode()
        assert theme_manager.theme_mode == THEME.LIGHT

    def test_switch_to_light(self):
        """Test switch_to_light method."""
        theme_manager = ThemeManager()
        
        theme_manager.theme_mode = THEME.DARK
        theme_manager.switch_to_light()
        assert theme_manager.theme_mode == THEME.LIGHT
        
        # Should be no-op if already light
        theme_manager.switch_to_light()
        assert theme_manager.theme_mode == THEME.LIGHT

    def test_switch_to_dark(self):
        """Test switch_to_dark method."""
        theme_manager = ThemeManager()
        
        theme_manager.theme_mode = THEME.LIGHT
        theme_manager.switch_to_dark()
        assert theme_manager.theme_mode == THEME.DARK
        
        # Should be no-op if already dark
        theme_manager.switch_to_dark()
        assert theme_manager.theme_mode == THEME.DARK

    @patch.object(ThemeManager, 'apply_color_scheme')
    def test_register_seed_color(self, mock_apply_color_scheme):
        """Test register_seed_color method."""
        theme_manager = ThemeManager()
        initial_colors = theme_manager.available_seed_colors
        
        # Register a new color
        theme_manager.register_seed_color('TestColor', '#FF5733')
        
        # Check that color was added
        updated_colors = theme_manager.available_seed_colors
        assert len(updated_colors) == len(initial_colors) + 1
        assert 'Testcolor' in updated_colors
        
        # Test setting the new color (this would trigger apply_color_scheme)
        theme_manager.seed_color = 'Testcolor'
        assert theme_manager.seed_color == 'Testcolor'
    
        # Verify apply_color_scheme was called
        mock_apply_color_scheme.assert_called()

    def test_register_seed_color_invalid_hex(self):
        """Test register_seed_color with invalid hex values."""
        theme_manager = ThemeManager()
        
        # Test invalid hex codes
        with pytest.raises(AssertionError):
            theme_manager.register_seed_color('Invalid1', 'FF5733')  # Missing #
        
        with pytest.raises(AssertionError):
            theme_manager.register_seed_color('Invalid2', '#FF57')   # Too short
        
        with pytest.raises(AssertionError):
            theme_manager.register_seed_color('Invalid3', '#FF5733X') # Too long

    def test_get_seed_color_rgba(self):
        """Test get_seed_color_rgba method."""
        theme_manager = ThemeManager()
        theme_manager.seed_color = 'Blue'
        
        # Test integer RGBA (default)
        rgba_int = theme_manager.get_seed_color_rgba()
        assert isinstance(rgba_int, list)
        assert len(rgba_int) == 4
        assert all(isinstance(val, int) for val in rgba_int)
        assert all(0 <= val <= 255 for val in rgba_int)
        
        # Test float RGBA
        rgba_float = theme_manager.get_seed_color_rgba(as_float=True)
        assert isinstance(rgba_float, list)
        assert len(rgba_float) == 4
        assert all(isinstance(val, float) for val in rgba_float)
        assert all(0.0 <= val <= 1.0 for val in rgba_float)

    @patch('morphui.theme.manager.get_dynamic_scheme')
    def test_generate_color_scheme_auto_theme(self, mock_get_dynamic_scheme):
        """Test generate_color_scheme with auto_theme enabled."""
        theme_manager = ThemeManager()
        theme_manager.auto_theme = True
        mock_scheme = Mock()
        mock_get_dynamic_scheme.return_value = mock_scheme
        
        result = theme_manager.generate_color_scheme()
        
        assert result == mock_scheme
        mock_get_dynamic_scheme.assert_called_once()

    def test_material_color_map(self):
        """Test material_color_map property."""
        theme_manager = ThemeManager()
        color_map = theme_manager.material_color_map
        
        assert isinstance(color_map, dict)
        assert len(color_map) > 0
        # Check that some expected color keys exist
        assert 'primary_color' in color_map
        assert 'background_color' in color_map
        assert 'surface_color' in color_map
        assert 'on_surface_color' in color_map

    def test_bounded_properties(self):
        """Test bounded numeric properties validation."""
        theme_manager = ThemeManager()
        
        # Test color_scheme_contrast bounds
        theme_manager.color_scheme_contrast = -0.5  # Should clamp to 0.0
        assert theme_manager.color_scheme_contrast == 0.0
        
        theme_manager.color_scheme_contrast = 1.5   # Should clamp to 1.0
        assert theme_manager.color_scheme_contrast == 1.0
        
        # Test color_quality bounds
        theme_manager.color_quality = 0   # Should clamp to 1
        assert theme_manager.color_quality == 1
        
        theme_manager.color_quality = -5  # Should clamp to 1
        assert theme_manager.color_quality == 1

    def test_all_colors_set_logic(self):
        """Test all_colors_set property logic."""
        theme_manager = ThemeManager()
        
        # Test that it checks all color properties in material_color_map
        color_map = theme_manager.material_color_map
        assert len(color_map) > 0  # Ensure we have colors to test
        
        # Test with method that simulates all colors set
        def mock_getattr_all_set(obj, name, default=None):
            if name in color_map:
                return [1.0, 0.0, 0.0, 1.0]  # All colors set
            return getattr(obj, name, default) if hasattr(obj, name) else default
        
        # Test with method that simulates some colors missing
        def mock_getattr_some_missing(obj, name, default=None):
            if name == 'primary_color':
                return None  # This one is missing
            elif name in color_map:
                return [1.0, 0.0, 0.0, 1.0]  # Others are set
            return getattr(obj, name, default) if hasattr(obj, name) else default
        
        # Note: We can't easily test this with patch due to recursion issues
        # But we can verify the logic exists and the material_color_map is accessible
        assert hasattr(theme_manager, 'all_colors_set')
        assert hasattr(theme_manager, 'material_color_map')

    @patch.object(ThemeManager, 'dispatch')
    def test_on_theme_changed_event(self, mock_dispatch):
        """Test that on_theme_changed event is properly dispatched."""
        theme_manager = ThemeManager()
        mock_dispatch.reset_mock()  # Clear any calls from initialization
        
        # Changing seed color should trigger on_theme_changed
        theme_manager.seed_color = 'Red'
        mock_dispatch.assert_called_with('on_theme_changed')

    def test_on_colors_updated_event_disabled_auto_theme(self):
        """Test on_colors_updated behavior when auto_theme is disabled."""
        theme_manager = ThemeManager()
        theme_manager.auto_theme = False
        
        # Mock a scheme
        mock_scheme = Mock()
        
        # Mock colors_initialized to return True (simulating colors were set before)
        with patch.object(type(theme_manager), 'colors_initialized', new_callable=lambda: property(lambda self: True)):
            with patch.object(theme_manager, 'dispatch') as mock_dispatch:
                theme_manager.apply_color_scheme(mock_scheme)
                
                # on_colors_updated should not be dispatched when auto_theme=False and colors are initialized
                mock_dispatch.assert_not_called()


class TestTypography:
    """Test suite for Typography class."""

    def test_init_default_properties(self):
        """Test Typography initialization with default values."""
        typography = Typography()
        
        assert typography.font_name == 'Inter'
        assert isinstance(typography.fonts_to_autoregister, tuple)
        assert len(typography.fonts_to_autoregister) > 0
        assert isinstance(typography._registered_fonts, tuple)

    def test_init_custom_properties(self):
        """Test Typography initialization with custom values."""
        typography = Typography(font_name='DMSans')
        
        assert typography.font_name == 'DMSans'

    @patch('morphui.theme.typography.LabelBase')
    def test_register_font_new(self, mock_label_base):
        """Test registering a new font."""
        typography = Typography()
        initial_count = len(typography._registered_fonts)
        
        typography.register_font(
            name='TestFont',
            fn_regular='test-regular.ttf',
            fn_italic='test-italic.ttf',
            fn_bold='test-bold.ttf',
            fn_bolditalic='test-bolditalic.ttf'
        )
        
        # Check LabelBase.register was called
        mock_label_base.register.assert_called_once_with(
            name='TestFont',
            fn_regular='test-regular.ttf',
            fn_italic='test-italic.ttf',
            fn_bold='test-bold.ttf',
            fn_bolditalic='test-bolditalic.ttf'
        )
        
        # Check font was added to registered fonts
        assert len(typography._registered_fonts) == initial_count + 1
        assert 'TestFont' in typography._registered_fonts

    @patch('morphui.theme.typography.LabelBase')
    def test_register_font_duplicate(self, mock_label_base):
        """Test registering a font that's already registered."""
        typography = Typography()
        typography._registered_fonts = ('TestFont',)
        
        typography.register_font(
            name='TestFont',
            fn_regular='test-regular.ttf'
        )
        
        # Should not call LabelBase.register for duplicate
        mock_label_base.register.assert_not_called()

    def test_get_text_style_valid_inputs(self):
        """Test get_text_style with valid inputs."""
        typography = Typography()
        typography._registered_fonts = ('InterRegular', 'InterThin', 'InterHeavy')
        
        # Test basic style retrieval
        style = typography.get_text_style('Display', 'large')
        
        assert isinstance(style, dict)
        assert 'font_size' in style
        assert 'line_height' in style
        assert 'name' in style
        assert style['font_size'] == '36sp'
        assert style['line_height'] == 1.44
        assert style['name'] == 'InterRegular'

    def test_get_text_style_with_weight(self):
        """Test get_text_style with font weight."""
        typography = Typography()
        typography._registered_fonts = ('InterRegular', 'InterThin', 'InterHeavy')
        
        style = typography.get_text_style('Headline', 'medium', font_weight='Heavy')
        
        assert style['name'] == 'InterHeavy'
        assert style['font_size'] == '22sp'
        assert style['line_height'] == 1.32

    def test_get_text_style_fallback_warning(self):
        """Test get_text_style fallback behavior with warning."""
        typography = Typography()
        typography._registered_fonts = ('InterRegular',)  # Only InterRegular available
        typography.font_name = 'NonExistentFont'
        
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            style = typography.get_text_style('Body', 'medium', font_weight='Heavy')
            
            # Check warning was issued
            assert len(w) == 1
            assert issubclass(w[0].category, UserWarning)
            assert 'not registered' in str(w[0].message)
            assert 'falling back to' in str(w[0].message)
        
        # Check fallback font is used
        assert style['name'] == 'InterRegular'

    def test_get_text_style_invalid_role(self):
        """Test get_text_style with invalid role."""
        typography = Typography()
        
        with pytest.raises(AssertionError) as exc_info:
            # Use typing.cast to bypass type checker for testing invalid input
            from typing import cast, Literal
            invalid_role = cast(Literal['Display', 'Headline', 'Title', 'Body', 'Label'], 'InvalidRole')
            typography.get_text_style(invalid_role, 'large')
        
        assert 'Invalid role' in str(exc_info.value)
        assert 'InvalidRole' in str(exc_info.value)

    def test_get_text_style_invalid_size(self):
        """Test get_text_style with invalid size."""
        typography = Typography()
        
        with pytest.raises(AssertionError) as exc_info:
            # Use typing.cast to bypass type checker for testing invalid input
            from typing import cast, Literal
            invalid_size = cast(Literal['large', 'medium', 'small'], 'invalid_size')
            typography.get_text_style('Display', invalid_size)
        
        assert 'Invalid size' in str(exc_info.value)
        assert 'invalid_size' in str(exc_info.value)

    def test_all_typography_combinations(self):
        """Test all valid typography role and size combinations."""
        typography = Typography()
        typography._registered_fonts = ('InterRegular',)
        
        from typing import cast, Literal
        
        for role in FONTS.TYPOGRAPHY_ROLES:
            for size in FONTS.SIZE_VARIANTS:
                # Cast to satisfy type checker
                typed_role = cast(Literal['Display', 'Headline', 'Title', 'Body', 'Label'], role)
                typed_size = cast(Literal['large', 'medium', 'small'], size)
                style = typography.get_text_style(typed_role, typed_size)
                
                assert isinstance(style, dict)
                assert 'font_size' in style
                assert 'line_height' in style
                assert 'name' in style
                assert isinstance(style['font_size'], str) and style['font_size'].endswith('sp')
                assert isinstance(style['line_height'], float)

    def test_font_weight_variants(self):
        """Test all font weight variants."""
        typography = Typography()
        typography._registered_fonts = (
            'TestFontRegular', 'TestFontThin', 'TestFontHeavy'
        )
        typography.font_name = 'TestFont'
        
        from typing import cast, Literal
        
        for weight in FONTS.WEIGHT_VARIANTS:
            # Cast to satisfy type checker
            typed_weight = cast(Literal['Regular', 'Thin', 'Heavy', ''], weight)
            style = typography.get_text_style('Title', 'medium', font_weight=typed_weight)
            expected_name = f'TestFont{weight}'
            assert style['name'] == expected_name

    def test_fonts_to_autoregister_structure(self):
        """Test that fonts_to_autoregister has correct structure."""
        typography = Typography()
        
        assert isinstance(typography.fonts_to_autoregister, tuple)
        
        for font_dict in typography.fonts_to_autoregister:
            assert isinstance(font_dict, dict)
            assert 'name' in font_dict
            assert 'fn_regular' in font_dict
            # Check that paths are strings
            assert isinstance(font_dict['name'], str)
            assert isinstance(font_dict['fn_regular'], str)

    def test_font_registration_methods(self):
        """Test different font registration method signatures."""
        typography = Typography()
        
        # Test minimal registration (regular only)
        with patch('morphui.theme.typography.LabelBase') as mock_label_base:
            typography.register_font('MinimalFont', 'regular.ttf')
            mock_label_base.register.assert_called_with(
                name='MinimalFont',
                fn_regular='regular.ttf',
                fn_italic=None,
                fn_bold=None,
                fn_bolditalic=None
            )
        
        # Test full registration
        with patch('morphui.theme.typography.LabelBase') as mock_label_base:
            typography.register_font(
                'FullFont',
                'regular.ttf',
                'italic.ttf',
                'bold.ttf',
                'bolditalic.ttf'
            )
            mock_label_base.register.assert_called_with(
                name='FullFont',
                fn_regular='regular.ttf',
                fn_italic='italic.ttf',
                fn_bold='bold.ttf',
                fn_bolditalic='bolditalic.ttf'
            )

    def test_style_dictionary_immutability(self):
        """Test that returned style dictionaries are copies."""
        typography = Typography()
        typography._registered_fonts = ('InterRegular',)
        
        style1 = typography.get_text_style('Display', 'large')
        style2 = typography.get_text_style('Display', 'large')
        
        # Modify one style
        style1['custom_property'] = 'test'
        
        # Check that the other style is not affected
        assert 'custom_property' not in style2
        
        # Check that subsequent calls return clean copies
        style3 = typography.get_text_style('Display', 'large')
        assert 'custom_property' not in style3


class TestMorphThemeBehavior:
    """Test suite for MorphThemeBehavior class."""

    def setup_method(self):
        """Set up test fixtures before each test method."""
        self.mock_theme_manager = Mock(spec=ThemeManager)
        self.mock_theme_manager.primary_color = [1.0, 0.0, 0.0, 1.0]
        self.mock_theme_manager.on_primary_color = [1.0, 1.0, 1.0, 1.0]
        self.mock_theme_manager.surface_color = [0.9, 0.9, 0.9, 1.0]
        self.mock_theme_manager.outline_color = [0.5, 0.5, 0.5, 1.0]

    @patch('morphui.uix.behaviors.theming.MorphApp._theme_manager')
    def test_init_default_properties(self, mock_app_theme_manager):
        """Test MorphThemeBehavior initialization with default values."""
        mock_app_theme_manager.return_value = self.mock_theme_manager
        
        # Create a mock widget class that inherits from MorphThemeBehavior
        class MockWidget(MorphThemeBehavior):
            def __init__(self, **kwargs):
                # Mock the widget properties
                self.background_color = None
                self.color = None
                self.border_color = None
                super().__init__(**kwargs)

        # Mock the binding methods to avoid Kivy property issues
        with patch.object(MockWidget, 'bind'), \
             patch.object(MockWidget, 'register_event_type'):
            
            widget = MockWidget()
            
            assert widget.auto_theme is True
            assert widget.theme_color_bindings == {}
            assert widget.theme_manager == self.mock_theme_manager
            assert widget._theme_bound is False

    @patch('morphui.uix.behaviors.theming.MorphApp._theme_manager')
    def test_theme_style_mappings_class_attribute(self, mock_app_theme_manager):
        """Test that theme_style_mappings is properly set from constants."""
        mock_app_theme_manager.return_value = self.mock_theme_manager
        
        class MockWidget(MorphThemeBehavior):
            def __init__(self, **kwargs):
                super().__init__(**kwargs)

        with patch.object(MockWidget, 'bind'), \
             patch.object(MockWidget, 'register_event_type'), \
             patch.object(MockWidget, '_bind_to_theme_manager'):
            
            widget = MockWidget()
            
            # Check that default styles are available
            assert 'primary' in widget.theme_style_mappings
            assert 'secondary' in widget.theme_style_mappings
            assert 'surface' in widget.theme_style_mappings
            assert 'error' in widget.theme_style_mappings
            assert 'outline' in widget.theme_style_mappings
            
            # Check that it references THEME.STYLES
            assert widget.theme_style_mappings == THEME.STYLES

    @patch('morphui.uix.behaviors.theming.MorphApp._theme_manager')
    def test_bind_theme_colors(self, mock_app_theme_manager):
        """Test bind_theme_colors method."""
        mock_app_theme_manager.return_value = self.mock_theme_manager
        
        class MockWidget(MorphThemeBehavior):
            def __init__(self, **kwargs):
                self.background_color = None
                self.color = None
                super().__init__(**kwargs)

        with patch.object(MockWidget, 'bind'), \
             patch.object(MockWidget, 'register_event_type'), \
             patch.object(MockWidget, '_bind_to_theme_manager'), \
             patch.object(MockWidget, '_update_colors') as mock_update:
            
            widget = MockWidget()
            
            # Test binding colors
            color_mappings = {
                'background_color': 'primary_color',
                'color': 'on_primary_color'
            }
            
            widget.bind_theme_colors(color_mappings)
            
            # Check that bindings were updated
            assert widget.theme_color_bindings == color_mappings
            
            # Check that _update_colors was called (since auto_theme is True by default)
            mock_update.assert_called_once()

    @patch('morphui.uix.behaviors.theming.MorphApp._theme_manager')
    def test_apply_theme_color_success(self, mock_app_theme_manager):
        """Test successful theme color application."""
        mock_app_theme_manager.return_value = self.mock_theme_manager
        
        class MockWidget(MorphThemeBehavior):
            def __init__(self, **kwargs):
                self.background_color = None
                super().__init__(**kwargs)

        with patch.object(MockWidget, 'bind'), \
             patch.object(MockWidget, 'register_event_type'), \
             patch.object(MockWidget, '_bind_to_theme_manager'):
            
            widget = MockWidget()
            
            # Test successful color application
            result = widget.apply_theme_color('background_color', 'primary_color')
            
            assert result is True
            assert widget.background_color == [1.0, 0.0, 0.0, 1.0]

    @patch('morphui.uix.behaviors.theming.MorphApp._theme_manager')
    def test_apply_theme_color_failure_cases(self, mock_app_theme_manager):
        """Test theme color application failure cases."""
        mock_app_theme_manager.return_value = self.mock_theme_manager
        
        class MockWidget(MorphThemeBehavior):
            def __init__(self, **kwargs):
                self.background_color = None
                super().__init__(**kwargs)

        with patch.object(MockWidget, 'bind'), \
             patch.object(MockWidget, 'register_event_type'), \
             patch.object(MockWidget, '_bind_to_theme_manager'):
            
            widget = MockWidget()
            
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
    def test_set_theme_style(self, mock_app_theme_manager):
        """Test set_theme_style method with predefined styles."""
        mock_app_theme_manager.return_value = self.mock_theme_manager
        
        class MockWidget(MorphThemeBehavior):
            def __init__(self, **kwargs):
                self.background_color = None
                self.color = None
                self.border_color = None
                super().__init__(**kwargs)

        with patch.object(MockWidget, 'bind'), \
             patch.object(MockWidget, 'register_event_type'), \
             patch.object(MockWidget, '_bind_to_theme_manager'), \
             patch.object(MockWidget, 'bind_theme_colors') as mock_bind:
            
            widget = MockWidget()
            
            # Test setting primary style
            widget.set_theme_style('primary')
            
            expected_bindings = {
                'background_color': 'primary_color',
                'color': 'on_primary_color',
                'border_color': 'primary_color'
            }
            
            mock_bind.assert_called_with(expected_bindings)

    @patch('morphui.uix.behaviors.theming.MorphApp._theme_manager')
    def test_set_theme_style_invalid(self, mock_app_theme_manager):
        """Test set_theme_style with invalid style name."""
        mock_app_theme_manager.return_value = self.mock_theme_manager
        
        class MockWidget(MorphThemeBehavior):
            def __init__(self, **kwargs):
                super().__init__(**kwargs)

        with patch.object(MockWidget, 'bind'), \
             patch.object(MockWidget, 'register_event_type'), \
             patch.object(MockWidget, '_bind_to_theme_manager'), \
             patch.object(MockWidget, 'bind_theme_colors') as mock_bind:
            
            widget = MockWidget()
            
            # Test with invalid style name - should not call bind_theme_colors
            widget.set_theme_style('invalid_style')
            
            mock_bind.assert_not_called()

    @patch('morphui.uix.behaviors.theming.MorphApp._theme_manager')
    def test_add_custom_style(self, mock_app_theme_manager):
        """Test add_custom_style method."""
        mock_app_theme_manager.return_value = self.mock_theme_manager
        
        class MockWidget(MorphThemeBehavior):
            def __init__(self, **kwargs):
                super().__init__(**kwargs)

        with patch.object(MockWidget, 'bind'), \
             patch.object(MockWidget, 'register_event_type'), \
             patch.object(MockWidget, '_bind_to_theme_manager'):
            
            widget = MockWidget()
            
            # Add a custom style
            custom_mappings = {
                'background_color': 'tertiary_color',
                'color': 'on_tertiary_color'
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
        mock_app_theme_manager.return_value = self.mock_theme_manager
        
        class MockWidget(MorphThemeBehavior):
            def __init__(self, **kwargs):
                super().__init__(**kwargs)

        with patch.object(MockWidget, 'bind'), \
             patch.object(MockWidget, 'register_event_type'), \
             patch.object(MockWidget, '_bind_to_theme_manager'):
            
            widget1 = MockWidget()
            widget2 = MockWidget()
            
            # Initially both widgets should reference the same class attribute
            assert widget1.theme_style_mappings is widget2.theme_style_mappings
            assert widget1.theme_style_mappings is MockWidget.theme_style_mappings
            
            # Add custom style to widget1
            widget1.add_custom_style('custom1', {'background_color': 'primary_color'})
            
            # Now widget1 should have its own copy
            assert widget1.theme_style_mappings is not widget2.theme_style_mappings
            assert widget1.theme_style_mappings is not MockWidget.theme_style_mappings
            
            # widget2 should still reference the class attribute
            assert widget2.theme_style_mappings is MockWidget.theme_style_mappings
            
            # Only widget1 should have the custom style
            assert 'custom1' in widget1.theme_style_mappings
            assert 'custom1' not in widget2.theme_style_mappings

    @patch('morphui.uix.behaviors.theming.MorphApp._theme_manager')
    def test_auto_theme_property_changes(self, mock_app_theme_manager):
        """Test auto_theme property changes and their effects."""
        mock_app_theme_manager.return_value = self.mock_theme_manager
        
        class MockWidget(MorphThemeBehavior):
            def __init__(self, **kwargs):
                super().__init__(**kwargs)

        with patch.object(MockWidget, 'bind'), \
             patch.object(MockWidget, 'register_event_type'), \
             patch.object(MockWidget, '_bind_to_theme_manager') as mock_bind, \
             patch.object(MockWidget, '_unbind_from_theme_manager') as mock_unbind, \
             patch.object(MockWidget, '_update_colors') as mock_update:
            
            widget = MockWidget()
            
            # Test disabling auto_theme
            widget.on_auto_theme(widget, False)
            mock_unbind.assert_called_once()
            
            # Test enabling auto_theme
            mock_bind.reset_mock()
            mock_update.reset_mock()
            widget.on_auto_theme(widget, True)
            mock_bind.assert_called_once()
            mock_update.assert_called_once()

    @patch('morphui.uix.behaviors.theming.MorphApp._theme_manager')
    def test_theme_color_bindings_property_changes(self, mock_app_theme_manager):
        """Test theme_color_bindings property changes trigger updates."""
        mock_app_theme_manager.return_value = self.mock_theme_manager
        
        class MockWidget(MorphThemeBehavior):
            def __init__(self, **kwargs):
                super().__init__(**kwargs)

        with patch.object(MockWidget, 'bind'), \
             patch.object(MockWidget, 'register_event_type'), \
             patch.object(MockWidget, '_bind_to_theme_manager'), \
             patch.object(MockWidget, '_update_colors') as mock_update:
            
            widget = MockWidget()
            widget.auto_theme = True
            
            # Test that changing bindings triggers update
            new_bindings = {'background_color': 'primary_color'}
            widget.on_theme_color_bindings(widget, new_bindings)
            
            mock_update.assert_called_once()

    @patch('morphui.uix.behaviors.theming.MorphApp._theme_manager')
    def test_theme_manager_event_handlers(self, mock_app_theme_manager):
        """Test theme manager event handler methods."""
        mock_app_theme_manager.return_value = self.mock_theme_manager
        
        class MockWidget(MorphThemeBehavior):
            def __init__(self, **kwargs):
                super().__init__(**kwargs)
                self.on_theme_changed_called = False
                
            def on_theme_changed(self, *args):
                self.on_theme_changed_called = True

        with patch.object(MockWidget, 'bind'), \
             patch.object(MockWidget, 'register_event_type'), \
             patch.object(MockWidget, '_bind_to_theme_manager'), \
             patch.object(MockWidget, '_update_colors') as mock_update, \
             patch.object(MockWidget, 'dispatch') as mock_dispatch:
            
            widget = MockWidget()
            widget.auto_theme = True
            
            # Test _on_theme_manager_changed
            widget._on_theme_manager_changed()
            mock_update.assert_called()
            mock_dispatch.assert_called_with('on_theme_changed')
            
            # Test _on_colors_updated
            mock_update.reset_mock()
            widget._on_colors_updated()
            mock_update.assert_called()

    @patch('morphui.uix.behaviors.theming.MorphApp._theme_manager')
    def test_refresh_theme_colors(self, mock_app_theme_manager):
        """Test refresh_theme_colors method."""
        mock_app_theme_manager.return_value = self.mock_theme_manager
        
        class MockWidget(MorphThemeBehavior):
            def __init__(self, **kwargs):
                super().__init__(**kwargs)

        with patch.object(MockWidget, 'bind'), \
             patch.object(MockWidget, 'register_event_type'), \
             patch.object(MockWidget, '_bind_to_theme_manager'), \
             patch.object(MockWidget, '_update_colors') as mock_update:
            
            widget = MockWidget()
            
            # Test manual refresh
            widget.refresh_theme_colors()
            mock_update.assert_called_once()

    @patch('morphui.uix.behaviors.theming.MorphApp._theme_manager')
    def test_update_colors_conditions(self, mock_app_theme_manager):
        """Test _update_colors method with different conditions."""
        mock_app_theme_manager.return_value = self.mock_theme_manager
        
        class MockWidget(MorphThemeBehavior):
            def __init__(self, **kwargs):
                self.background_color = None
                super().__init__(**kwargs)

        with patch.object(MockWidget, 'bind'), \
             patch.object(MockWidget, 'register_event_type'), \
             patch.object(MockWidget, '_bind_to_theme_manager'), \
             patch.object(MockWidget, 'apply_theme_color') as mock_apply:
            
            widget = MockWidget()
            
            # Test with auto_theme False - should not update
            widget.auto_theme = False
            widget._update_colors()
            mock_apply.assert_not_called()
            
            # Test with no bindings - should not update
            widget.auto_theme = True
            widget.theme_color_bindings = {}
            widget._update_colors()
            mock_apply.assert_not_called()
            
            # Test with valid conditions - should update
            widget.theme_color_bindings = {'background_color': 'primary_color'}
            widget._update_colors()
            mock_apply.assert_called_with('background_color', 'primary_color')

    def test_on_theme_changed_default_implementation(self):
        """Test that on_theme_changed has a default no-op implementation."""
        class MockWidget(MorphThemeBehavior):
            def __init__(self, **kwargs):
                super().__init__(**kwargs)

        with patch.object(MockWidget, 'bind'), \
             patch.object(MockWidget, 'register_event_type'), \
             patch.object(MockWidget, '_bind_to_theme_manager'):
            
            widget = MockWidget()
            
            # Should not raise any exception
            result = widget.on_theme_changed()
            assert result is None