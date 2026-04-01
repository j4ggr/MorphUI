# Button

<!-- ![Button demo](../../assets/gifs/button.gif) -->

Buttons trigger actions. MorphUI provides several button variants — from full text buttons with ripple and elevation to compact icon-only buttons.

## Variants

| Class | Use case |
|---|---|
| `MorphButton` | Primary action button with text and optional icons |
| `MorphIconButton` | Icon-only button (leading icon) |
| `MorphTrailingIconButton` | Icon-only button (trailing) |
| `MorphIconTextButton` | Icon + text, icon on the left |
| `MorphTextIconButton` | Text + icon, icon on the right |
| `MorphTextIconToggleButton` | Toggle version of text+icon button |
| `MorphSimpleIconButton` | Lightweight icon button (no elevation) |

## Usage

```python
from morphui.uix.button import MorphButton, MorphIconButton, MorphIconTextButton

# Text button
btn = MorphButton(text="Save", on_release=self.save)

# Icon button
icon_btn = MorphIconButton(icon='content-save', on_release=self.save)

# Icon + text
combo = MorphIconTextButton(icon='plus', text="Add item")
```

## Tooltips

All button variants accept a `tooltip` keyword:

```python
from morphui.uix.tooltip import MorphSimpleTooltip

btn = MorphIconButton(
    icon='delete',
    tooltip=MorphSimpleTooltip(text="Delete selected"),
)
```

---

::: morphui.uix.button
