# Tooltip

<!-- ![Tooltip demo](../../assets/gifs/tooltip.gif) -->

Tooltips appear on hover and provide brief contextual information about a UI element. MorphUI provides two ready-to-use tooltip variants.

## Variants

| Class | Description |
|---|---|
| `MorphSimpleTooltip` | Single plain text label |
| `MorphRichTooltip` | Bold heading + supporting detail text |

## Usage

Attach a tooltip via the `tooltip` keyword on any widget that uses `MorphTooltipBehavior` (all standard MorphUI buttons and labels):

```python
from morphui.uix.button import MorphIconButton
from morphui.uix.tooltip import MorphSimpleTooltip, MorphRichTooltip

# Simple
btn = MorphIconButton(
    icon='information',
    tooltip=MorphSimpleTooltip(text="Show details"),
)

# Rich
btn = MorphIconButton(
    icon='settings',
    tooltip=MorphRichTooltip(
        heading="Settings",
        supporting="Open application settings",
    ),
)
```

---

::: morphui.uix.tooltip
