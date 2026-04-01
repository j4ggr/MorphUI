# Getting Started

This guide walks you through installing MorphUI, creating your first application, and understanding the core concepts.

---

## Installation

**Requirements:** Python 3.13+, Kivy 2.3.1+

=== "pip"

    ```bash
    pip install morphui
    ```

=== "With visualization support"

    ```bash
    pip install morphui[visualization]
    ```

=== "Development install"

    ```bash
    git clone https://github.com/j4ggr/MorphUI.git
    cd MorphUI
    pip install -e ".[visualization]"
    ```

---

## Your First App

Every MorphUI application subclasses `MorphApp` instead of Kivy's `App`. This provides automatic access to the theme manager and typography system.

```python
from morphui.app import MorphApp
from morphui.uix.boxlayout import MorphBoxLayout
from morphui.uix.label import MorphLabel
from morphui.uix.button import MorphButton

class HelloApp(MorphApp):

    def build(self) -> MorphBoxLayout:
        self.theme_manager.theme_mode = 'Dark'
        self.theme_manager.seed_color = 'Blue'

        return MorphBoxLayout(
            MorphLabel(text="Hello, MorphUI!"),
            MorphButton(
                text="Press me",
                on_release=lambda btn: print("Clicked!"),
            ),
            orientation='vertical',
            spacing=12,
            padding=24,
        )

if __name__ == '__main__':
    HelloApp().run()
```

!!! tip "Declarative syntax"
    MorphUI supports a declarative widget tree — pass children directly as positional arguments to layout constructors, just like the example above.

---

## Theme Configuration

The theme manager is accessible via `self.theme_manager` in any `MorphApp` subclass. Configure it in `build()` before returning the widget tree.

### Light / Dark mode

```python
self.theme_manager.theme_mode = 'Light'   # or 'Dark'
self.theme_manager.toggle_theme_mode()    # flip at runtime
```

### Seed color

The seed color drives the entire dynamic palette using Material You's color algorithm.

```python
# Any named color from Kivy's colormap
self.theme_manager.seed_color = 'Orange'

# Or register a custom hex color first
self.theme_manager.register_seed_color('brand', '#00b8c2')
self.theme_manager.seed_color = 'brand'
```

### Color scheme variant

```python
# Options: TONAL_SPOT, VIBRANT, EXPRESSIVE, NEUTRAL,
#          MONOCHROME, FIDELITY, CONTENT, RAINBOW, FRUIT_SALAD
self.theme_manager.color_scheme = 'VIBRANT'
```

### Contrast

```python
self.theme_manager.color_scheme_contrast = 0.0  # 0.0 (none) – 1.0 (max)
```

---

## Declarative Widget Trees

MorphUI widgets support a declarative composition pattern. Pass child widgets as positional arguments and keyword properties together:

```python
from morphui.uix.boxlayout import MorphBoxLayout
from morphui.uix.label import MorphLabel
from morphui.uix.button import MorphButton, MorphIconButton
from morphui.uix.textfield import MorphTextField

layout = MorphBoxLayout(
    MorphLabel(text="Name"),
    MorphTextField(hint_text="Enter your name"),
    MorphBoxLayout(
        MorphButton(text="Cancel"),
        MorphButton(text="Submit"),
        orientation='horizontal',
        spacing=8,
    ),
    orientation='vertical',
    spacing=12,
    padding=[16, 24],
)
```

---

## Using Components

### Buttons

```python
from morphui.uix.button import MorphButton, MorphIconButton

# Text button
btn = MorphButton(text="Save", on_release=self.save)

# Icon button
icon_btn = MorphIconButton(icon='content-save', on_release=self.save)
```

### Text Fields

```python
from morphui.uix.textfield import MorphTextField, MorphTextFieldOutlined

# Filled (default)
field = MorphTextField(hint_text="Username", required=True)

# Outlined variant
field = MorphTextFieldOutlined(hint_text="Email", validator='email')
```

### Dialogs

```python
from morphui.uix.dialog import MorphDialog
from morphui.uix.label import MorphLabel
from morphui.uix.button import MorphButton
from morphui.uix.boxlayout import MorphBoxLayout
from kivy.core.window import Window

dialog = MorphDialog(
    MorphLabel(text="Are you sure?"),
    MorphBoxLayout(
        MorphButton(text="Cancel", on_release=lambda b: dialog.dismiss()),
        MorphButton(text="Confirm", on_release=self.confirm),
        orientation='horizontal',
    ),
    orientation='vertical',
)

# Show by adding to the window
Window.add_widget(dialog)
dialog.open()
```

### Tooltips

```python
from morphui.uix.button import MorphIconButton
from morphui.uix.tooltip import MorphSimpleTooltip

btn = MorphIconButton(
    icon='information',
    tooltip=MorphSimpleTooltip(text="More information"),
)
```

---

## Runtime Theme Switching

Bind UI elements to the theme toggle:

```python
from morphui.uix.button import MorphIconButton

toggle = MorphIconButton(
    icon='brightness-4',
    on_release=lambda b: self.theme_manager.toggle_theme_mode(),
)
```

All widgets with `auto_theme=True` (the default) update automatically when the theme changes.

---

## Next Steps

- Explore the [Components](../components/index.md) reference for all available widgets
- Read the [Theme System](../theme/index.md) docs for deep customization
- Look at the [Behaviors](../behaviors/index.md) guide for building custom widgets
- Browse the `examples/` folder in the repository for full runnable demos
