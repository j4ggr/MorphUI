# Dialog

<!-- ![Dialog demo](../../assets/gifs/dialog.gif) -->

Dialogs display content in a modal overlay and block interaction with the rest of the UI. A `MorphScrimLayer` is rendered behind the dialog to focus user attention.

## Usage

```python
from morphui.uix.dialog import MorphDialog
from morphui.uix.label import MorphLabel
from morphui.uix.button import MorphButton
from morphui.uix.boxlayout import MorphBoxLayout
from kivy.core.window import Window

dialog = MorphDialog(
    MorphLabel(text="Discard changes?"),
    MorphBoxLayout(
        MorphButton(text="Cancel", on_release=lambda b: dialog.dismiss()),
        MorphButton(text="Discard", on_release=self.discard),
        orientation='horizontal',
        spacing=8,
    ),
    orientation='vertical',
    padding=24,
    spacing=16,
)

Window.add_widget(dialog)
dialog.open()
```

## Open / Dismiss

```python
dialog.open()    # animate in
dialog.dismiss() # animate out and remove from window
```

---

::: morphui.uix.dialog
