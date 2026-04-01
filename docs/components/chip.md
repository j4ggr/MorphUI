# Chip

<!-- ![Chip demo](../../assets/gifs/chip.gif) -->

Chips are compact, interactive elements used for actions, filtering, or input. They support leading icons, trailing close buttons, and toggle state.

## Variants

| Class | Use case |
|---|---|
| `MorphChip` | Basic action chip |
| `MorphFilterChip` | Toggle chip for filter selection |
| `MorphInputChip` | Represents an input token with a close button |

## Usage

```python
from morphui.uix.chip import MorphChip, MorphFilterChip

# Action chip
chip = MorphChip(text="Export", on_release=self.export)

# Filter chip (toggleable)
chip = MorphFilterChip(text="In Stock", on_release=self.filter)

# With leading icon
chip = MorphChip(text="Download", leading_icon='download')
```

---

::: morphui.uix.chip
