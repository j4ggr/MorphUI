import sys
import pytest

from pathlib import Path

sys.path.append(str(Path(__file__).parent.resolve()))

from morphui.utils.dotdict import DotDict


class TestDotDict:

    def test_dotdict_basic(self) -> None:
        data = DotDict({'name': 'John', 'age': 30})
        assert data.name == 'John'
        assert data.age == 30
        data.city = 'New York'
        assert data['city'] == 'New York'

    def test_dotdict_nested(self) -> None:
        nested = DotDict({
            'user': {'name': 'Alice', 'profile': {'role': 'admin'}}
        })
        assert nested.user.name == 'Alice'
        assert nested.user.profile.role == 'admin'
    
    def test_dotdict_keyerror(self) -> None:
        data = DotDict({'name': 'John'})
        with pytest.raises(AttributeError):
            _ = data.age
    
    def test_dotdict_dict_methods(self) -> None:
        regular_dict = {'name': 'John', 'age': 30}
        data = DotDict(regular_dict)
        assert data.keys() == regular_dict.keys()
        assert data.items() == regular_dict.items()
        assert data.get('name') == 'John'
        assert data.get('nonexistent', 'default') == 'default'
        data.update({'city': 'New York'})
        assert data.city == 'New York'

