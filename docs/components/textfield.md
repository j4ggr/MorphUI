# Text Field

<!-- ![Text Field demo](../../assets/gifs/textfield.gif) -->

Text fields let users enter and edit text. They support validation, error states, leading icons, trailing icon buttons, heading labels, and supporting text.

## Variants

| Class | Style |
|---|---|
| `MorphTextField` | Default filled style |
| `MorphTextFieldFilled` | Explicit filled variant |
| `MorphTextFieldOutlined` | Outlined border style |
| `MorphTextFieldRounded` | Fully rounded border style |

## Usage

```python
from morphui.uix.textfield import MorphTextField, MorphTextFieldOutlined

# Basic
field = MorphTextField(hint_text="Enter name")

# Required field
field = MorphTextField(hint_text="Email", required=True, validator='email')

# Outlined with max length
field = MorphTextFieldOutlined(
    hint_text="Username",
    max_text_length=32,
)
```

## Validation

Built-in validators are configured via the `validator` property:

```python
field = MorphTextField(validator='email')
field = MorphTextField(validator='numeric')
field = MorphTextField(validator='integer')
```

For custom validation, subclass `MorphTextValidator`.

## Error State

```python
# Set error manually
field.error = True
field.error_message = "This field is required"
```

---

::: morphui.uix.textfield
