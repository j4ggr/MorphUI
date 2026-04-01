# Behaviors

Behaviors are modular mixin classes that add specific capabilities to widgets. Compose them via multiple inheritance to build custom widgets without duplicating logic.

---

## Architecture

MorphUI uses Python's MRO (Method Resolution Order) for behavior composition. Behaviors are always mixed in from left to right in the class signature, with the base Kivy widget last:

```python
class MyWidget(
        MorphHoverBehavior,      # hover detection
        MorphRippleBehavior,     # ripple effect on press
        MorphThemeBehavior,      # auto-theming
        MorphSurfaceLayerBehavior,
        Label):                  # Kivy base
    pass
```

---

## Available Behaviors

| Behavior | Module | Description |
|---|---|---|
| [Theming](theming.md) | `behaviors.theming` | Automatic color and typography theme integration |
| [Hover](hover.md) | `behaviors.hover` | Mouse enter/leave detection |
| [Layer](layer.md) | `behaviors.layer` | Surface, interaction, content, and overlay layers |
| [Touch & Ripple](touch.md) | `behaviors.touch` | Button press, ripple effect, toggle |
| [Motion](motion.md) | `behaviors.motion` | Menu and dialog animation |
| [Sizing](sizing.md) | `behaviors.sizing` | Auto-sizing, size bounds, interactive resize |
| [Composition](composition.md) | `behaviors.composition` | Leading/trailing/label widget slots |
| Elevation | `behaviors.elevation` | Drop shadow with configurable depth |
| Scale & Shape | `behaviors.shape` | Scale animation and rounded corners |
| Declarative | `behaviors.declarative` | Positional child argument support |
| App Reference | `behaviors.appreference` | Access to `MorphApp`, `ThemeManager`, `Typography` |

---

!!! info "Separation of concerns"
    Behaviors are intentionally fine-grained. For example, `MorphThemeBehavior` is a convenience alias that combines `MorphColorThemeBehavior` + `MorphTypographyBehavior`, but you can use them independently if you only need one of the two.
