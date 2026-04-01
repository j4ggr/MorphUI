# Data View

The `dataview` package provides a paginated, scrollable table component for displaying structured tabular data. It is composed of independent sub-components that can be used together or separately.

---

## Component Overview

```
MorphDataViewTable
├── MorphDataViewHeader      ← column header row
├── MorphDataViewIndex       ← optional row index column
├── MorphDataViewBody        ← scrollable data cells
└── MorphDataViewNavigation  ← page navigation bar
```

---

| Module | Description |
|---|---|
| [Table](table.md) | Top-level table widget — the main entry point |
| [Header](header.md) | Column header row with sorting support |
| [Row Index](index.md) | Optional row index / line number column |
| [Body](body.md) | Scrollable data cell grid |
| [Navigation](navigation.md) | Page navigation bar with page size control |
| [Base Classes](base.md) | Shared label and layout base classes |

---

## Quick Example

```python
from morphui.uix.dataview import MorphDataViewTable

table = MorphDataViewTable(
    columns=['Name', 'Value', 'Unit'],
    data=[
        ['Temperature', '23.4', '°C'],
        ['Pressure',    '1013', 'hPa'],
        ['Humidity',    '55',   '%'],
    ],
)
```
