"""
DotDict - A dictionary that supports dot notation access
"""

from typing import Any, Dict


class DotDict(dict):
    """
    A dictionary subclass that allows attribute-style access to 
    dictionary items.
    
    Parameters
    ----------
    *args : tuple
        Arguments passed to dict constructor.
    **kwargs : dict
        Keyword arguments passed to dict constructor.
    
    Attributes
    ----------
    All dictionary keys become accessible as attributes.
    
    Notes
    -----
    - Access items using dot notation: obj.key instead of obj['key']
    - Supports all standard dictionary operations
    - Nested DotDict support for nested dictionaries
    - Safe attribute access with fallback to dict methods
    
    Examples
    --------
    Basic usage:
    
    ```python
    data = DotDict({'name': 'John', 'age': 30})
    print(data.name)  # 'John'
    print(data.age)   # 30
    data.city = 'New York'
    print(data['city'])  # 'New York'
    ```
    
    Nested dictionaries:
    
    ```python
    nested = DotDict({
        'user': {'name': 'Alice', 'profile': {'role': 'admin'}}
    })
    print(nested.user.name)  # 'Alice'
    print(nested.user.profile.role)  # 'admin'
    ```
    """
    
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        # Convert nested dictionaries to DotDict instances
        for key, value in self.items():
            if isinstance(value, dict) and not isinstance(value, DotDict):
                self[key] = DotDict(value)
    
    def __getattr__(self, key: str) -> Any:
        """
        Get an item using dot notation.
        
        Parameters
        ----------
        key : str
            The key to access.
            
        Returns
        -------
        Any
            The value associated with the key.
            
        Raises
        ------
        AttributeError
            If the key doesn't exist and isn't a dict method.
        """
        try:
            return self[key]
        except KeyError:
            # Check if it's a dictionary method/attribute
            if hasattr(dict, key):
                return getattr(dict, key)
            raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{key}'")
    
    def __setattr__(self, key: str, value: Any) -> None:
        """
        Set an item using dot notation.
        
        Parameters
        ----------
        key : str
            The key to set.
        value : Any
            The value to assign.
        """
        # Convert nested dictionaries to DotDict
        if isinstance(value, dict) and not isinstance(value, DotDict):
            value = DotDict(value)
        self[key] = value
    
    def __delattr__(self, key: str) -> None:
        """
        Delete an item using dot notation.
        
        Parameters
        ----------
        key : str
            The key to delete.
            
        Raises
        ------
        AttributeError
            If the key doesn't exist.
        """
        try:
            del self[key]
        except KeyError:
            raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{key}'")
    
    def __setitem__(self, key: str, value: Any) -> None:
        """
        Override setitem to convert nested dictionaries to DotDict.
        
        Parameters
        ----------
        key : str
            The key to set.
        value : Any
            The value to assign.
        """
        if isinstance(value, dict) and not isinstance(value, DotDict):
            value = DotDict(value)
        super().__setitem__(key, value)
    
    def update(self, *args, **kwargs) -> None:
        """
        Override update to convert nested dictionaries to DotDict.
        
        Parameters
        ----------
        *args : tuple
            Arguments passed to dict.update().
        **kwargs : dict
            Keyword arguments passed to dict.update().
        """
        if args:
            other = args[0]
            if hasattr(other, 'items'):
                for key, value in other.items():
                    self[key] = value
            else:
                for key, value in other:
                    self[key] = value
        
        for key, value in kwargs.items():
            self[key] = value
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get an item with a default value.
        
        Parameters
        ----------
        key : str
            The key to access.
        default : Any, optional
            Default value if key doesn't exist, by default None.
            
        Returns
        -------
        Any
            The value or default.
        """
        try:
            return self[key]
        except KeyError:
            return default
    
    def copy(self) -> 'DotDict':
        """
        Create a shallow copy of the DotDict.
        
        Returns
        -------
        DotDict
            A new DotDict instance.
        """
        return DotDict(dict.copy(self))
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert DotDict back to a regular dictionary (recursively).
        
        Returns
        -------
        Dict[str, Any]
            A regular dictionary.
        """
        result = {}
        for key, value in self.items():
            if isinstance(value, DotDict):
                result[key] = value.to_dict()
            else:
                result[key] = value
        return result
    
    def __repr__(self) -> str:
        """
        String representation of DotDict.
        
        Returns
        -------
        str
            String representation.
        """
        return f"{self.__class__.__name__}({dict.__repr__(self)})"


# Convenience function for creating DotDict from nested dictionaries
def dotdict(data: Dict[str, Any]) -> DotDict:
    """
    Create a DotDict from a regular dictionary.
    
    Parameters
    ----------
    data : Dict[str, Any]
        Dictionary to convert.
        
    Returns
    -------
    DotDict
        DotDict instance.
        
    Examples
    --------
    ```python
    config = dotdict({
        'database': {
            'host': 'localhost',
            'port': 5432
        }
    })
    print(config.database.host)  # 'localhost'
    ```
    """
    return DotDict(data)