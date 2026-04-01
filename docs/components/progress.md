# Progress

<!-- ![Progress demo](../../assets/gifs/progress.gif) -->

Progress indicators communicate ongoing operations. MorphUI provides linear and circular variants, each supporting both determinate (known progress) and indeterminate (unknown duration) modes. Optional wavy variants add a visual flair for indeterminate states.

## Variants

| Class | Shape | Mode |
|---|---|---|
| `MorphLinearProgress` | Horizontal bar | Determinate + Indeterminate |
| `MorphCircularProgress` | Arc / spinner | Determinate + Indeterminate |
| `MorphWavyLinearProgress` | Sinusoidal bar | Determinate + Indeterminate |
| `MorphWavyCircularProgress` | Sinusoidal arc | Determinate + Indeterminate |

## Usage

```python
from morphui.uix.progress import MorphLinearProgress, MorphCircularProgress

# Determinate — set value between 0.0 and 1.0
bar = MorphLinearProgress(value=0.6)

# Indeterminate — animates continuously
spinner = MorphCircularProgress(indeterminate=True)

# Update progress
bar.value = 0.9   # animates smoothly to new value
```

## Configuration

```python
bar = MorphLinearProgress(
    value=0.5,
    value_animation_duration=0.3,      # seconds
    value_animation_transition='out_quad',
    indeterminate_duration=1.33,       # seconds per cycle
)
```

---

::: morphui.uix.progress
