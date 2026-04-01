# Theme System

MorphUI's theme system is built on [Material You](https://m3.material.io/styles/color/dynamic-color/overview)'s dynamic color algorithm. A single seed color generates a full harmonious palette, and all themed widgets update automatically when the theme changes.

---

## How it Works

```
seed_color  ──►  DynamicScheme  ──►  MorphDynamicColorPalette
                 (Material You)            │
                                           ▼
                                    ThemeManager
                                           │
                          ┌────────────────┤
                          ▼                ▼
                   ThemeBehavior     Typography
                   (per widget)      (fonts/roles)
```

1. `ThemeManager` generates a `DynamicScheme` from the `seed_color` using the selected `color_scheme` variant.
2. `MorphDynamicColorPalette` exposes named color properties (`primary_color`, `surface_color`, etc.).
3. Widgets with `MorphColorThemeBehavior` subscribe to `on_theme_changed` and re-bind their colors automatically.

---

## Modules

| Module | Description |
|---|---|
| [Manager](manager.md) | `ThemeManager` — seed color, mode, scheme, contrast |
| [Palette](palette.md) | `MorphDynamicColorPalette` — all named color properties |
| [Typography](typography.md) | Font registration, type roles, icon map |

---

## Seed Colors

Any color name from [Kivy's colormap](https://kivy.org/doc/stable/api-kivy.utils.html) works as a seed color. You can also register custom hex colors:

```python
self.theme_manager.register_seed_color('brand_teal', '#00b8c2')
self.theme_manager.seed_color = 'brand_teal'
```

## Color Scheme Variants

| Variant | Character |
|---|---|
| `TONAL_SPOT` | Default Material You — balanced and restrained |
| `VIBRANT` | More saturated, vivid palette |
| `EXPRESSIVE` | Bold color expression across all roles |
| `NEUTRAL` | Muted, desaturated — good for professional UIs |
| `MONOCHROME` | Single-hue grayscale-like palette |
| `FIDELITY` | Stays closest to the seed color |
| `CONTENT` | Extracted from image content (advanced use) |
| `RAINBOW` | Full spectrum across the palette |
| `FRUIT_SALAD` | Analogous hues for a playful look |

## Auto-Theming

All MorphUI components have `auto_theme=True` by default. Setting `auto_theme=False` on a widget freezes its colors until manually refreshed:

```python
label = MorphLabel(text="Static color", auto_theme=False)
```
