# MorphUI Coding Guidelines

## Default Configuration Pattern

### Overview
MorphUI uses a consistent pattern for defining default widget configurations using class attributes. This pattern provides clear documentation, easy inheritance, and efficient memory usage.

### Pattern Definition

Use the `default_config` class attribute to define default widget configurations:

```python
from typing import Any, Dict

class MorphWidget(BaseWidget):
    """Example widget following MorphUI patterns."""
    
    default_config: Dict[str, Any] = dict(
        # Alignment and positioning
        halign='left',
        valign='center',
        
        # Theme configuration
        theme_color_bindings=dict(
            content_color='content_surface_color',
            surface_color='transparent_color',
        ),
        
        # Typography settings
        typography_role='Body',
        typography_size='medium',
        typography_weight='Regular',
    )
    """Default configuration values applied during widget initialization.
    
    This dictionary defines the standard behavior and appearance of the widget.
    Values can be overridden by subclasses or during instantiation through kwargs.
    
    Structure:
        - Alignment properties (halign, valign, etc.)
        - Theme bindings and color mappings
        - Typography settings (role, size, weight)
        - Widget-specific configuration options
    """
    
    def __init__(self, **kwargs) -> None:
        # Apply default configuration with kwargs override
        config = self.default_config.copy()
        
        # Conditional configuration adjustments
        if 'theme_style' in kwargs:
            config.pop('theme_color_bindings', None)
        
        # Merge user-provided kwargs (kwargs take precedence)
        config.update(kwargs)
        
        super().__init__(**config)
```

### Naming Convention

- **Class attribute**: `default_config`
- **Local variable**: `config` (copy of default_config)
- **Documentation**: Always include comprehensive docstring explaining the structure

### Best Practices

#### 1. **Consistent Structure Organization**
```python
default_config: Dict[str, Any] = dict(
    # 1. Layout and positioning
    halign='left',
    valign='center',
    
    # 2. Theme and appearance
    theme_color_bindings=dict(...),
    
    # 3. Typography
    typography_role='Label',
    typography_size='medium',
    
    # 4. Widget-specific options
    auto_sizing=True,
)
```

#### 2. **Inheritance Override Pattern**
```python
class MorphIconLabel(MorphLabel):
    """Specialized label for icons."""
    
    default_config: Dict[str, Any] = dict(
        # Override parent defaults
        font_name='MaterialIcons',
        halign='center',  # Different from parent
        
        # Keep some parent settings
        typography_role='Label',
        typography_size='medium',
        
        # Add new defaults
        theme_color_bindings=dict(
            content_color='primary_color',
            surface_color='transparent_color',
        ),
    )
    """Icon-specific default configuration.
    
    Overrides MorphLabel defaults to provide icon-appropriate settings:
    - Uses MaterialIcons font for icon rendering
    - Centers alignment for better icon display
    - Sets primary color theme for prominence
    """
```

#### 3. **Documentation Requirements**
```python
default_config: Dict[str, Any] = dict(...)
"""[Widget Name] default configuration values.

Brief description of what these defaults achieve for the widget.

Structure:
    - Category 1: Description of settings
    - Category 2: Description of settings
    - Category N: Description of settings

Notes:
    - Any special behaviors or conditional logic
    - Inheritance considerations
    - Performance implications
"""
```

#### 4. **Conditional Configuration**
```python
def __init__(self, **kwargs) -> None:
    config = self.default_config.copy()
    
    # Handle conflicting or mutually exclusive options
    if 'theme_style' in kwargs:
        config.pop('theme_color_bindings', None)
    
    if 'custom_mode' in kwargs and kwargs['custom_mode']:
        config.update({
            'auto_theme': False,
            'custom_colors': True,
        })
    
    config.update(kwargs)
    super().__init__(**config)
```

### Why This Pattern?

#### ✅ **Advantages**
- **Discoverability**: Defaults are immediately visible at class level
- **Documentation**: Serves as clear API documentation
- **Inheritance**: Easy to override in subclasses
- **Memory Efficient**: Shared across instances
- **Testability**: Easy to test default behaviors
- **Consistency**: Uniform pattern across the codebase

#### ❌ **Avoid These Alternatives**
```python
# ❌ DON'T: Inline dictionary in __init__
def __init__(self, **kwargs):
    defaults = dict(halign='left', valign='center')  # Hidden, hard to override
    
# ❌ DON'T: Magic values scattered in code
def __init__(self, **kwargs):
    self.halign = kwargs.get('halign', 'left')  # No central definition
    
# ❌ DON'T: Multiple default dictionaries
_theme_defaults = dict(...)
_layout_defaults = dict(...)  # Fragmented, hard to understand
```

### Migration Guide

If you're updating existing code to follow this pattern:

1. **Find existing default definitions**
2. **Consolidate into single `default_config` class attribute**
3. **Add comprehensive docstring**
4. **Update `__init__` method to use the pattern**
5. **Test inheritance and override behavior**

### Example Implementation

```python
class MorphButton(MorphLabel):
    """Interactive button widget with Material Design styling."""
    
    default_config: Dict[str, Any] = dict(
        # Interaction
        auto_theme=True,
        
        # Layout
        halign='center',
        valign='center',
        
        # Appearance
        theme_color_bindings=dict(
            surface_color='primary_color',
            content_color='content_primary_color',
            border_color='primary_color',
        ),
        
        # Typography
        typography_role='Label',
        typography_size='medium',
        typography_weight='Medium',
        
        # Behavior
        size_hint=(None, None),
        auto_sizing=True,
    )
    """Button default configuration optimized for interactive elements.
    
    Provides Material Design button appearance and behavior:
    - Centered content alignment for button text
    - Primary theme colors for prominence
    - Medium weight typography for readability
    - Auto-sizing for content-appropriate dimensions
    
    Override theme_color_bindings when using theme_style parameter.
    """
    
    def __init__(self, **kwargs) -> None:
        config = self.default_config.copy()
        
        # Theme style overrides color bindings
        if 'theme_style' in kwargs:
            config.pop('theme_color_bindings', None)
        
        config.update(kwargs)
        super().__init__(**config)
```

This pattern ensures consistency, maintainability, and clear documentation across the MorphUI codebase.