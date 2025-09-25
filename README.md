# MorphUI

MorphUI is a creative and flexible UI extension for Kivy, designed to provide developers with a modern and customizable set of components for building beautiful user interfaces. Unlike KivyMD, MorphUI is not bound to Material Design principles, allowing for greater freedom in design and styling.

## Features

- 🎨 **Flexible Design**: Not bound to Material Design - create your own visual style
- 🧩 **Modern Components**: Button, Label, Card, TextInput with contemporary styling
- 🎯 **Theme System**: Light/Dark themes with easy customization
- ⚡ **Smooth Animations**: Built-in animations for interactive elements
- 📱 **Cross-Platform**: Works on desktop, mobile, and web (via Kivy)
- 🔧 **Easy Integration**: Simple drop-in replacement for standard Kivy widgets

## Installation

### From PyPI (when published)
```bash
pip install morphui
```

### From Source
```bash
git clone https://github.com/j4ggr/MorphUI.git
cd MorphUI
pip install -e .
```

## Quick Start

```python
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout

from morphui.uix.button import MorphButton
from morphui.uix.label import MorphLabel
from morphui.uix.card import MorphCard

class MyApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        # Add a modern card
        card = MorphCard()
        
        # Add components to the card
        title = MorphLabel(text="Welcome to MorphUI!", text_style="headline")
        button = MorphButton(text="Get Started", button_style="filled")
        
        card.add_widget(title)
        card.add_widget(button)
        layout.add_widget(card)
        
        return layout

MyApp().run()
```

## Components

### MorphButton
Modern button with multiple styles and animations:

```python
from morphui.uix.button import MorphButton

# Filled button (default)
btn1 = MorphButton(text="Filled", button_style="filled")

# Outlined button  
btn2 = MorphButton(text="Outlined", button_style="outlined")

# Text button
btn3 = MorphButton(text="Text", button_style="text")
```

### MorphLabel
Enhanced label with typography system:

```python
from morphui.uix.label import MorphLabel

# Different text styles
title = MorphLabel(text="Title", text_style="headline")
body = MorphLabel(text="Body text", text_style="body")
caption = MorphLabel(text="Caption", text_style="caption")
```

### MorphCard
Container with modern styling and elevation:

```python
from morphui.uix.card import MorphCard

card = MorphCard(
    elevation=4,
    corner_radius=16
)
```

### MorphTextInput
Modern text input with focus states:

```python
from morphui.uix.textinput import MorphTextInput

text_input = MorphTextInput(
    hint_text="Enter text here",
    corner_radius=8
)

# Error state
text_input.set_error("This field is required")
```

## Theme System

MorphUI includes a comprehensive theme system:

```python
from morphui.theme.styles import theme_manager

# Switch themes
theme_manager.current_theme = "dark"  # or "light"

# Access theme colors
colors = theme_manager.colors
primary_color = colors.PRIMARY

# Access typography
typography = theme_manager.typography
title_style = typography.get_text_style("title")
```

### Custom Themes

Create your own themes:

```python
from morphui.theme.colors import ColorPalette
from morphui.theme.typography import Typography

class MyColorPalette(ColorPalette):
    PRIMARY = [0.8, 0.2, 0.4, 1.0]  # Custom red
    SECONDARY = [0.2, 0.8, 0.4, 1.0]  # Custom green

# Register custom theme
theme_manager.register_theme(
    "custom",
    MyColorPalette,
    Typography,
    "My Custom Theme"
)

theme_manager.current_theme = "custom"
```

## Examples

Check out the `examples/` directory for complete sample applications:

- `basic_example.py` - Showcase of all components
- More examples coming soon!

## Development

### Setting up Development Environment

```bash
git clone https://github.com/j4ggr/MorphUI.git
cd MorphUI
pip install -e ".[dev]"
```

### Running Examples

```bash
cd examples
python basic_example.py
```

## Roadmap

- [ ] Additional components (Switch, Slider, Progress Bar, etc.)
- [ ] Advanced animations and transitions
- [ ] More built-in themes
- [ ] Comprehensive documentation website
- [ ] Testing suite
- [ ] Performance optimizations

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Inspired by KivyMD but designed for greater design flexibility
- Built on top of the excellent [Kivy](https://kivy.org) framework
- Thanks to all contributors and the Kivy community
