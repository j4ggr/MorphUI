# MorphUI

**MorphUI** is a modern, flexible UI framework for [Kivy](https://kivy.org) that provides beautiful, themeable components with dynamic color management. Built on Material You's dynamic color system, it gives you a rich set of widgets with automatic theming, smooth animations, and a powerful behavior architecture — without being locked to Material Design rules.

---

## Key Features

<div class="grid cards" markdown>

- :material-palette: **Dynamic Theming**

    Material You-inspired color system. Switch between light/dark mode or reseed colors at runtime — all widgets update automatically.

- :material-widgets: **Rich Component Library**

    Buttons, chips, text fields, dialogs, dropdowns, tooltips, progress indicators, and more — all fully themed and animated.

- :material-chart-line: **Data Visualization**

    Optional matplotlib integration via `morphui[visualization]` for charts and inline plots inside your Kivy UI.

- :material-lightning-bolt: **Smooth Animations**

    Built-in ripple effects, hover states, motion behaviors, and value-animated progress indicators.

- :material-puzzle: **Modular Behaviors**

    Mix and match fine-grained behaviors — theming, hover, ripple, elevation, sizing, composition — to compose custom widgets.

- :material-cellphone: **Cross-Platform**

    Runs on Windows, macOS, Linux, Android, iOS, and web via Kivy's platform abstraction.

</div>

---

## Installation

=== "Basic"

    ```bash
    pip install morphui
    ```

=== "With Visualization"

    ```bash
    pip install morphui[visualization]
    ```

=== "From Source"

    ```bash
    git clone https://github.com/j4ggr/MorphUI.git
    cd MorphUI
    pip install -e .
    ```

---

## Quick Start

```python
from morphui.app import MorphApp
from morphui.uix.boxlayout import MorphBoxLayout
from morphui.uix.label import MorphLabel
from morphui.uix.button import MorphButton

class MyApp(MorphApp):
    def build(self):
        self.theme_manager.theme_mode = 'Dark'
        self.theme_manager.seed_color = 'Blue'

        return MorphBoxLayout(
            MorphLabel(text="Welcome to MorphUI!"),
            MorphButton(text="Click Me"),
            orientation='vertical',
            spacing=10,
            padding=20,
        )

if __name__ == '__main__':
    MyApp().run()
```

---

## Where to Go Next

| | |
|---|---|
| [Getting Started](guides/index.md) | Installation, first app, and theme setup |
| [Components](components/index.md) | Buttons, chips, dialogs, text fields, and more |
| [Layouts](layouts/index.md) | Layout containers and structural widgets |
| [Theme System](theme/index.md) | Dynamic color palette and typography |
| [Behaviors](behaviors/index.md) | Modular behavior mixins for custom widgets |
| [API Reference](api/index.md) | Full auto-generated API documentation |
