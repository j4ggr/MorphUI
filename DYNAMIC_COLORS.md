# Dynamic Colors in MorphUI

This guide explains how to create dynamic colors in Kivy that automatically adjust when switching between light and dark themes.

## Overview

The MorphUI theme system provides dynamic colors that automatically update all widgets when you switch themes. This eliminates the need to manually update every widget's color properties.

## Basic Concept

Instead of setting static colors like `[1, 0, 0, 1]`, you use dynamic color objects that automatically change when the theme switches:

```python
from morphui.theme.styles import theme_manager

# Get a dynamic surface color
surface_color = theme_manager.get_dynamic_color("SURFACE")

# Use it in a widget - color will update automatically when theme changes
widget.background_color = surface_color.rgba
```

## Available Colors

The theme system provides these semantic colors:

### Primary Colors
- `PRIMARY` - Main brand color
- `PRIMARY_VARIANT` - Darker variant of primary
- `ON_PRIMARY` - Text color for primary backgrounds

### Secondary Colors  
- `SECONDARY` - Secondary brand color
- `SECONDARY_VARIANT` - Darker variant of secondary
- `ON_SECONDARY` - Text color for secondary backgrounds

### Surface Colors
- `SURFACE` - Card/panel backgrounds
- `SURFACE_VARIANT` - Alternative surface color
- `ON_SURFACE` - Text color for surface backgrounds

### Background Colors
- `BACKGROUND` - Main app background
- `ON_BACKGROUND` - Text color for background

### Semantic Colors
- `ERROR` - Error state color
- `SUCCESS` - Success state color  
- `WARNING` - Warning state color
- `INFO` - Information state color
- `ON_ERROR`, `ON_SUCCESS`, `ON_WARNING`, `ON_INFO` - Text colors

## Usage Examples

### 1. Basic Dynamic Color

```python
from morphui.theme.styles import theme_manager

# Get dynamic color
surface_color = theme_manager.get_dynamic_color("SURFACE")

# Use in widget
widget.background_color = surface_color.rgba

# Bind to updates (colors change automatically)
surface_color.bind(rgba=lambda instance, rgba: setattr(widget, 'background_color', rgba))
```

### 2. Convenience Functions

For common colors, use convenience functions:

```python
from morphui.theme.styles import surface_color, primary_color, on_surface_color

# These return DynamicColor objects
bg_color = surface_color()
btn_color = primary_color() 
text_color = on_surface_color()

widget.background_color = bg_color.rgba
```

### 3. Creating Dynamic Widgets

```python
from kivy.uix.button import Button
from morphui.theme.styles import theme_manager

class DynamicButton(Button):
    def __init__(self, bg_color_name="PRIMARY", text_color_name="ON_PRIMARY", **kwargs):
        super().__init__(**kwargs)
        
        # Get dynamic colors
        self.bg_color = theme_manager.get_dynamic_color(bg_color_name)
        self.text_color = theme_manager.get_dynamic_color(text_color_name)
        
        # Set initial colors
        self.background_color = self.bg_color.rgba
        self.color = self.text_color.rgba
        
        # Bind to updates
        self.bg_color.bind(rgba=self._update_bg_color)
        self.text_color.bind(rgba=self._update_text_color)
    
    def _update_bg_color(self, instance, rgba):
        self.background_color = rgba
    
    def _update_text_color(self, instance, rgba):
        self.color = rgba

# Usage
button = DynamicButton(text="My Button")
```

### 4. Canvas Instructions with Dynamic Colors

```python
from kivy.graphics import Color, Rectangle
from morphui.theme.styles import theme_manager

class DynamicWidget(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Get dynamic color
        self.surface_color = theme_manager.get_dynamic_color("SURFACE")
        
        # Create canvas
        with self.canvas:
            self.bg_color = Color(rgba=self.surface_color.rgba)
            self.bg_rect = Rectangle(pos=self.pos, size=self.size)
        
        # Bind to updates
        self.surface_color.bind(rgba=self._update_color)
        self.bind(pos=self._update_rect, size=self._update_rect)
    
    def _update_color(self, instance, rgba):
        self.bg_color.rgba = rgba
    
    def _update_rect(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size
```

## Switching Themes

```python
from morphui.theme.styles import theme_manager

# Switch to dark theme
theme_manager.current_theme = "dark"

# Switch to light theme  
theme_manager.current_theme = "light"

# All dynamic colors automatically update!
```

## Creating Custom Themes

```python
from morphui.theme.colors import ColorPalette
from morphui.theme.styles import theme_manager

class MyCustomPalette(ColorPalette):
    PRIMARY = [0.8, 0.2, 0.4, 1.0]  # Custom red
    SECONDARY = [0.2, 0.8, 0.4, 1.0]  # Custom green
    SURFACE = [0.95, 0.95, 0.95, 1.0]  # Light gray
    # ... define other colors

# Register the theme
theme_manager.register_theme(
    name="custom",
    color_palette_class=MyCustomPalette,
    typography_class=Typography,  # Use default typography
    display_name="My Custom Theme"
)

# Use the custom theme
theme_manager.current_theme = "custom"
```

## Best Practices

### 1. Use Semantic Colors
Always use semantic color names rather than specific colors:
```python
# Good
error_color = theme_manager.get_dynamic_color("ERROR")

# Avoid
red_color = [1, 0, 0, 1]  # Static red
```

### 2. Bind to Updates
Always bind dynamic colors to widget updates:
```python
dynamic_color = theme_manager.get_dynamic_color("SURFACE")
widget.background_color = dynamic_color.rgba
dynamic_color.bind(rgba=lambda instance, rgba: setattr(widget, 'background_color', rgba))
```

### 3. Use Appropriate Text Colors
Use corresponding `ON_*` colors for text:
```python
# If background is SURFACE, text should be ON_SURFACE
bg_color = theme_manager.get_dynamic_color("SURFACE")
text_color = theme_manager.get_dynamic_color("ON_SURFACE")
```

### 4. Create Reusable Components
Create widget classes that encapsulate dynamic color logic:
```python
class ThemeButton(Button):
    def __init__(self, color_scheme="primary", **kwargs):
        super().__init__(**kwargs)
        self._setup_colors(color_scheme)
    
    def _setup_colors(self, scheme):
        if scheme == "primary":
            self._setup_dynamic_colors("PRIMARY", "ON_PRIMARY")
        elif scheme == "secondary":
            self._setup_dynamic_colors("SECONDARY", "ON_SECONDARY")
        # etc.
```

## Complete Example

See `examples/simple_dynamic_colors.py` for a complete working example that demonstrates:
- Dynamic buttons with different color schemes
- Automatic color updates when switching themes
- Proper text color pairing with background colors

Run the example to see dynamic colors in action:
```bash
cd examples
python simple_dynamic_colors.py
```

## Troubleshooting

### Colors Not Updating
Make sure you're binding to the dynamic color's `rgba` property:
```python
dynamic_color.bind(rgba=your_callback_function)
```

### Wrong Text Colors
Ensure you're using the correct `ON_*` color for text:
```python
# If button background is PRIMARY, text should be ON_PRIMARY
bg_color = theme_manager.get_dynamic_color("PRIMARY")
text_color = theme_manager.get_dynamic_color("ON_PRIMARY")
```

### Theme Not Switching
Check that you're setting the theme correctly:
```python
# Correct
theme_manager.current_theme = "dark"

# Incorrect  
theme_manager.theme = "dark"  # Wrong property name
```