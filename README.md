# MorphUI

**MorphUI** is a modern, flexible UI framework for [Kivy](https://kivy.org) that brings beautiful, themeable components with dynamic color management. Built on Material You's dynamic color system, MorphUI provides an extensive set of widgets with automatic theming, smooth animations, and a powerful component architecture—all while giving you complete design freedom.

## ✨ Key Features

- 🎨 **Dynamic Theming**: Material You-inspired dynamic color system with automatic light/dark mode
- 🧩 **Rich Component Library**: Modern buttons, labels, text fields, dropdowns, layouts, and more
- 📊 **Data Visualization**: Optional matplotlib integration for charts and plots
- ⚡ **Smooth Animations**: Built-in ripple effects, hover states, and motion behaviors
- 🎯 **Powerful Behaviors**: Modular behavior system for easy customization
- 📱 **Cross-Platform**: Runs on Windows, macOS, Linux, Android, iOS, and web
- 🔧 **Developer-Friendly**: Clean API with comprehensive docstrings

## 📦 Installation

### Basic Installation

```bash
pip install morphui
```

### With Visualization Support

For data visualization features (charts and plots):

```bash
pip install morphui[visualization]
```

### From Source

```bash
git clone https://github.com/j4ggr/MorphUI.git
cd MorphUI
pip install -e .
```

## 🚀 Quick Start

Here's a minimal example to get you started:

```python
from morphui.app import MorphApp
from morphui.uix.boxlayout import MorphBoxLayout
from morphui.uix.label import MorphLabel
from morphui.uix.button import MorphButton

class MyApp(MorphApp):
    def build(self):
        # Configure theme
        self.theme_manager.theme_mode = 'Dark'
        self.theme_manager.seed_color = 'Blue'
        
        # Create layout
        layout = MorphBoxLayout(
            MorphLabel(text="Welcome to MorphUI!"),
            MorphButton(text="Click Me!"),
            orientation='vertical',
            spacing=10,
            padding=20
        )
        
        return layout

if __name__ == '__main__':
    MyApp().run()
```

## 🎨 Theme System

MorphUI's theme system is built on Material You's dynamic color algorithms, automatically generating harmonious color schemes from a single seed color.

### Theme Configuration

```python
from morphui.app import MorphApp

class MyApp(MorphApp):
    def build(self):
        # Set theme mode (Light or Dark)
        self.theme_manager.theme_mode = 'Dark'
        
        # Choose a seed color (any color name from Kivy's colormap)
        self.theme_manager.seed_color = 'Orange'
        
        # Select color scheme variant
        # Options: TONAL_SPOT, VIBRANT, EXPRESSIVE, NEUTRAL, 
        #          MONOCHROME, FIDELITY, CONTENT, RAINBOW, FRUIT_SALAD
        self.theme_manager.color_scheme = 'VIBRANT'
        
        # Adjust contrast (0.0 to 1.0)
        self.theme_manager.color_scheme_contrast = 0.0
        
        return self.create_ui()
```

### Custom Seed Colors

Register your own custom colors:

```python
# Register a custom color with hex value
self.theme_manager.register_seed_color('brand_blue', '#0066CC')
self.theme_manager.seed_color = 'brand_blue'
```

### Runtime Theme Switching

```python
# Toggle between light and dark mode
self.theme_manager.toggle_theme_mode()

# Or set explicitly
self.theme_manager.theme_mode = 'Light'  # or 'Dark'
```

## 📚 Core Components

### MorphApp

Base application class with integrated theme management:

```python
from morphui.app import MorphApp

class MyApp(MorphApp):
    def build(self):
        # Access theme manager
        self.theme_manager.theme_mode = 'Dark'
        
        # Access typography system
        icon_map = self.typography.icon_map
        
        return your_root_widget
```

### Buttons

#### MorphButton

Full-featured button with theming and animations:

```python
from morphui.uix.button import MorphButton

button = MorphButton(
    text="Click Me",
    on_release=lambda x: print("Button clicked!")
)
```

#### MorphIconButton

Icon-only button for compact interfaces:

```python
from morphui.uix.button import MorphIconButton

icon_btn = MorphIconButton(
    icon='close',  # Material icon name
    on_release=self.close_dialog
)
```

### Labels

#### MorphLabel

Themed label with auto-sizing:

```python
from morphui.uix.label import MorphLabel

label = MorphLabel(
    text="Hello, MorphUI!",
    auto_width=True,
    auto_height=True
)
```

#### MorphIconLabel

Label with an icon:

```python
from morphui.uix.label import MorphIconLabel

icon_label = MorphIconLabel(
    icon='star',
    text="Favorite"
)
```

### Text Fields

#### MorphTextField

Modern text input with validation:

```python
from morphui.uix.textfield import MorphTextField

text_field = MorphTextField(
    heading_text="Email",
    hint_text="Enter your email",
    required=True,
    validator='email'  # Built-in validators: email, url, int, float
)

# Check validation
if text_field.error:
    print(f"Error: {text_field.error_type}")
```

#### MorphTextFieldOutlined

Outlined variant:

```python
from morphui.uix.textfield import MorphTextFieldOutlined

email_field = MorphTextFieldOutlined(
    heading_text="Email Address",
    leading_icon='email',
    validator='email',
    required=True
)
```

### Dropdowns

#### MorphDropdownFilterField

Searchable dropdown with filtering:

```python
from morphui.uix.dropdown import MorphDropdownFilterField

items = [
    {'label_text': 'Apple', 'leading_icon': 'apple'},
    {'label_text': 'Banana', 'leading_icon': 'fruit-citrus'},
    {'label_text': 'Cherry', 'leading_icon': 'fruit-cherries'}
]

dropdown = MorphDropdownFilterField(
    items=items,
    heading_text='Select Fruit',
    leading_icon='magnify',
    item_release_callback=lambda item, index: print(f"Selected: {item.label_text}")
)
```

### Layouts

MorphUI provides themed versions of all standard Kivy layouts:

```python
from morphui.uix.boxlayout import MorphBoxLayout
from morphui.uix.floatlayout import MorphFloatLayout
from morphui.uix.gridlayout import MorphGridLayout

# BoxLayout with themed widgets as children
layout = MorphBoxLayout(
    widget1,
    widget2,
    widget3,
    orientation='vertical',
    spacing=10,
    padding=20
)
```

## 📊 Data Visualization

MorphUI includes optional matplotlib integration for creating beautiful, themed charts.

### Basic Chart Example

```python
from morphui.app import MorphApp
from morphui.uix.visualization import MorphChart
import matplotlib.pyplot as plt
import numpy as np

class ChartApp(MorphApp):
    def build(self):
        self.theme_manager.theme_mode = 'Dark'
        
        # Create chart widget
        chart = MorphChart()
        
        # Create matplotlib figure
        x = np.linspace(0, 10, 100)
        y = np.sin(x)
        
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(x, y, linewidth=2)
        ax.set_title('Sine Wave')
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.grid(True, alpha=0.3)
        
        # Set the figure
        chart.figure = fig
        
        return chart

if __name__ == '__main__':
    ChartApp().run()
```

### Interactive Features

MorphChart automatically includes:
- Zoom and pan controls
- Home/back/forward navigation
- Save figure option
- Automatic theme-aware styling

See [examples/visualization_example.py](examples/visualization_example.py) for more advanced usage.

## 💡 Complete Examples

### Theme Showcase App

```python
from morphui.app import MorphApp
from morphui.uix.boxlayout import MorphBoxLayout
from morphui.uix.label import MorphLabel
from morphui.uix.button import MorphIconButton

class ThemeShowcaseApp(MorphApp):
    def build(self):
        self.theme_manager.theme_mode = 'Dark'
        self.theme_manager.seed_color = 'Orange'
        
        layout = MorphBoxLayout(
            MorphIconButton(
                icon='brightness-3' if self.theme_manager.theme_mode == 'Light' else 'brightness-5',
                on_release=lambda x: self.toggle_theme()
            ),
            MorphLabel(text=f"Current theme: {self.theme_manager.theme_mode}"),
            orientation='vertical',
            spacing=20,
            padding=20
        )
        
        return layout
    
    def toggle_theme(self):
        self.theme_manager.toggle_theme_mode()

if __name__ == '__main__':
    ThemeShowcaseApp().run()
```

### Icon Picker Example

```python
from morphui.app import MorphApp
from morphui.uix.floatlayout import MorphFloatLayout
from morphui.uix.dropdown import MorphDropdownFilterField

class IconPickerApp(MorphApp):
    def build(self):
        self.theme_manager.theme_mode = 'Dark'
        self.theme_manager.seed_color = 'Blue'
        
        # Create items from available icons
        icon_items = [
            {
                'label_text': icon_name,
                'leading_icon': icon_name,
            }
            for icon_name in sorted(self.typography.icon_map.keys())
        ]
        
        layout = MorphFloatLayout(
            MorphDropdownFilterField(
                identity='icon_picker',
                items=icon_items,
                item_release_callback=self.icon_selected,
                heading_text='Search icons...',
                leading_icon='magnify',
                pos_hint={'center_x': 0.5, 'center_y': 0.9},
                size_hint=(0.8, None),
            )
        )
        
        self.icon_picker = layout.identities.icon_picker
        return layout
    
    def icon_selected(self, item, index):
        self.icon_picker.text = item.label_text
        self.icon_picker.leading_icon = item.label_text

if __name__ == '__main__':
    IconPickerApp().run()
```

## 📁 Examples Directory

Explore the `examples/` directory for complete, runnable applications:

- **[color_showcase_app.py](examples/color_showcase_app.py)** - Comprehensive color palette showcase with theme switching
- **[visualization_example.py](examples/visualization_example.py)** - Data visualization with multiple chart types

### Running Examples

To run an example:

```bash
cd examples
python color_showcase_app.py
# or
python visualization_example.py
```

## 🎯 Behavior System

MorphUI uses a modular behavior system that allows you to mix and match functionality:

- **MorphThemeBehavior** - Automatic theme color binding
- **MorphHoverBehavior** - Mouse hover detection and states
- **MorphRippleBehavior** - Material-style ripple effects
- **MorphScaleBehavior** - Scale animations
- **MorphElevationBehavior** - Shadow and elevation effects
- **MorphAutoSizingBehavior** - Automatic size calculations
- **MorphIdentificationBehavior** - Widget identification and lookup

These behaviors are composable and can be mixed into custom widgets.

## 🛠️ Development

### Setting Up Development Environment

```bash
git clone https://github.com/j4ggr/MorphUI.git
cd MorphUI
pip install -e ".[test,visualization]"
```

### Running Tests

```bash
pytest tests/
```

## 📖 Documentation

MorphUI components are extensively documented with docstrings. Access documentation in your IDE or use Python's help system:

```python
from morphui.uix.button import MorphButton
help(MorphButton)
```

## 🗺️ Roadmap

- [x] Dynamic color system with Material You
- [x] Core components (buttons, labels, text fields)
- [x] Layout containers
- [x] Data visualization integration
- [ ] More advanced components (sliders, switches, progress bars)
- [ ] Animation improvements
- [ ] Comprehensive documentation website
- [ ] PyPI package release
- [ ] Performance optimizations

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

### Guidelines

1. Follow the existing code style
2. Add docstrings to new components
3. Test your changes thoroughly
4. Update documentation as needed

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built on top of the excellent [Kivy](https://kivy.org) framework
- Material You color system via [material-color-utilities](https://github.com/material-foundation/material-color-utilities)
- Icons from [Material Design Icons](https://materialdesignicons.com/)
- Inspired by modern UI frameworks while maintaining design flexibility

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/j4ggr/MorphUI/issues)
- **Examples**: Check the `examples/` directory
- **Documentation**: See docstrings in source code

---

**MorphUI** - Beautiful, flexible UIs for Kivy applications.