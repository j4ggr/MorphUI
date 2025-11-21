from typing import Any
from typing import Dict

from morphui.utils import clean_config
from morphui.uix.label import MorphSimpleLabel
from morphui.uix.behaviors import MorphResizeBehavior
from morphui.uix.recycleboxlayout import MorphRecycleBoxLayout


class MorphDataViewHeaderLabel(
        MorphResizeBehavior,
        MorphSimpleLabel):
    """A simple label for data view headers."""
    
    default_config: Dict[str, Any] = dict(
        min_size=[80, None],
        auto_height=True,
        auto_width=False,)
    

class MorphDataViewHeaderLayout(
        MorphRecycleBoxLayout):
    
    default_config: Dict[str, Any] = dict(
        orientation='horizontal',
        auto_size=True,)

    def __init__(self, **kwargs) -> None:
        config = clean_config(self.default_config, kwargs)
        super().__init__(**config)

