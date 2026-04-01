# Layouts

MorphUI wraps all standard Kivy layout classes with theming and declarative composition support. All layouts accept child widgets as positional constructor arguments.

---

| Layout | Description |
|---|---|
| [Anchor Layout](anchorlayout.md) | Positions children at anchor points |
| [Box Layout](boxlayout.md) | Horizontal or vertical linear arrangement |
| [Container](container.md) | Prebuilt icon/label container helpers |
| [Float Layout](floatlayout.md) | Absolute positioning with `pos_hint` |
| [Grid Layout](gridlayout.md) | Grid arrangement by rows and columns |
| [Recycle Box Layout](recycleboxlayout.md) | Virtualized box layout for large lists |
| [Recycle Grid Layout](recyclegridlayout.md) | Virtualized grid layout for large collections |
| [Recycle View](recycleview.md) | Efficient scrollable list using view recycling |
| [Relative Layout](relativelayout.md) | Positioning relative to parent |
| [Screen Manager](screenmanager.md) | Multiple screens with transition support |
| [Scroll View](scrollview.md) | Scrollable content container |
| [Stack Layout](stacklayout.md) | Wrapping stack arrangement |
| [Widget](widget.md) | Themed base widget |

---

!!! tip "Declarative usage"
    All MorphUI layouts support the declarative pattern — pass children as positional arguments:

    ```python
    MorphBoxLayout(
        MorphLabel(text="Hello"),
        MorphButton(text="OK"),
        orientation='horizontal',
        spacing=8,
    )
    ```
