# Dropdown

<!-- ![Dropdown demo](../../assets/gifs/dropdown.gif) -->

Dropdowns present a list of options that appear below a trigger element. Filter field variants combine a text field with a dropdown for searchable selection.

## Variants

| Class | Description |
|---|---|
| `MorphDropdownList` | Scrollable option list |
| `MorphDropdownMenu` | Full dropdown menu with animation |
| `MorphDropdownFilterField` | Text field + dropdown for filtered selection |
| `MorphDropdownFilterFieldOutlined` | Outlined variant |
| `MorphDropdownFilterFieldRounded` | Rounded variant |
| `MorphDropdownFilterFieldFilled` | Filled variant |

## Usage

```python
from morphui.uix.dropdown import MorphDropdownFilterField

field = MorphDropdownFilterField(
    hint_text="Select category",
    options=['Electronics', 'Clothing', 'Books', 'Food'],
    on_select=self.on_category_selected,
)
```

---

::: morphui.uix.dropdown
